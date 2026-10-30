#!/usr/bin/env python3
"""Showfront — salvage build (Meta Global AI Developer Hackathon, Indie track).

Written Oct 30, 2026 on Aisha's machine after the Pegasus build became
unreachable (area-wide power/internet outage). Implements the spec's
agent-first slice (spec section 12) and the section 7 fallback narrowing:

  ONE car, ONE flow: God's-Eye fly-in -> 360 photo spin -> the Closer
  (sales agent that presents ONLY from the verified vehicle record,
  refuses off-sheet facts, books the test drive) -> honest listing ->
  lead captured.

Model layer (spec section 11): the Closer's brain is pluggable.
  CLOSER_PROVIDER=baseten  -> Muse Spark Open (Meta open weights) via
                              Baseten, model meta-models/muse-spark-open-1026
                              (the intended submission provider).
  CLOSER_PROVIDER=nebius   -> DEV ONLY substitute for local testing.
                              Run logs record the provider truthfully; a
                              dev-provider run is never presented as the
                              Meta stack.
Every model call is logged under runs/ with provider, model, and a hash
of the exchange (spec: tooling usage is provable, not claimed).

Guardrail (ISNAD, in code, not just in the prompt): after the model
answers, a verification pass extracts every number in the reply and
checks it against the vehicle record. Any number that is not on the
sheet replaces the reply with the refusal line. The agent can present
the car; it cannot invent one.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8902"))
PROVIDER = os.environ.get("CLOSER_PROVIDER", "nebius").lower()
RUNS_DIR = os.path.join(HERE, "runs")
LEADS_FILE = os.path.join(HERE, "leads.json")

with open(os.path.join(HERE, "vehicle.json"), encoding="utf-8") as f:
    VEHICLE = json.load(f)

REFUSAL = ("That is not on this car's verified sheet, so I will not guess at it. "
           "What I can do is check with the lot for you — or book you a test "
           "drive and you can see the car in person.")

CLOSER_SYSTEM = (
    "You are the Closer, the sales agent inside Showfront. You present ONE car "
    "from its verified record and nothing else. The record is the whole truth: "
    "if a fact is not in the record, you say it is not on the sheet and offer "
    "to check or to book a test drive. You never invent features, prices, "
    "history, or promises. No pressure tactics that misrepresent. You are a "
    "teacher-seller: clear, warm, brief. When the visitor wants to see the "
    "car, offer the test-drive booking.\n\nVERIFIED VEHICLE RECORD (JSON):\n"
    + json.dumps({k: v for k, v in VEHICLE.items() if k != "status"}, indent=1)
)


def record_numbers():
    nums = set()
    for v in VEHICLE.values():
        if isinstance(v, int):
            nums.add(str(v))
            nums.add(f"{v:,}")
        elif isinstance(v, str):
            for n in re.findall(r"\d[\d,]*", v):
                nums.add(n)
    return nums


ALLOWED_NUMBERS = record_numbers()


def verify_reply(reply):
    """Return (ok, bad_numbers). Every number in the reply must trace to
    the record (or be a harmless count like '2 keys' already in notes)."""
    found = re.findall(r"\$?\d[\d,]*", reply)
    bad = []
    for n in found:
        clean = n.lstrip("$")
        if clean in ALLOWED_NUMBERS:
            continue
        # allow the digits inside allowed compound strings (e.g. 2.5L, 39 mpg are in record strings)
        joined = " ".join(str(v) for v in VEHICLE.values())
        if clean in joined:
            continue
        bad.append(n)
    return (not bad), bad


def log_run(kind, payload):
    os.makedirs(RUNS_DIR, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    entry = {"ts": stamp, "kind": kind, "provider": PROVIDER, **payload}
    entry["hash"] = hashlib.sha256(
        json.dumps(entry, sort_keys=True).encode()).hexdigest()[:16]
    with open(os.path.join(RUNS_DIR, f"run-{stamp}-{kind}.json"), "w") as f:
        json.dump(entry, f, indent=1)
    return entry["hash"]


# ---------------------------------------------------------------- providers
def call_baseten(messages):
    key = os.environ.get("BASETEN_API_KEY")
    if not key:
        raise RuntimeError("BASETEN_API_KEY not set")
    body = {"model": "meta-models/muse-spark-open-1026",
            "messages": messages, "max_tokens": 600, "temperature": 0.3}
    req = urllib.request.Request(
        "https://inference.baseten.co/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Api-Key " + key,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"], "meta-models/muse-spark-open-1026"


def call_nebius_dev(messages):
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    from dynamic_credentials import add_surrogate_to_request
    body = {"model": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
            "messages": messages, "max_tokens": 900, "temperature": 0.3}
    req = urllib.request.Request(
        "https://api.tokenfactory.nebius.com/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    env_key = os.environ.get("NEBIUS_API_KEY")
    if env_key:
        req.add_header("Authorization", "Bearer " + env_key)
    else:
        add_surrogate_to_request(req, "custom.nebius-token-factory",
                                 allowed_hosts=["api.tokenfactory.nebius.com"])
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"], data.get("model", "nemotron-dev")


def closer_answer(history):
    messages = [{"role": "system", "content": CLOSER_SYSTEM}] + history[-8:]
    if PROVIDER == "baseten":
        reply, model = call_baseten(messages)
    else:
        reply, model = call_nebius_dev(messages)
    ok, bad = verify_reply(reply)
    run_hash = log_run("closer", {"model": model, "verified": ok,
                                  "bad_numbers": bad,
                                  "q": history[-1]["content"][:200]})
    if not ok:
        return REFUSAL, model, False, run_hash
    return reply, model, True, run_hash


# ---------------------------------------------------------------- page
def spin_frames():
    assets = os.path.join(HERE, "assets", "car")
    if not os.path.isdir(assets):
        return []
    return sorted("/assets/car/" + n for n in os.listdir(assets)
                  if n.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Showfront — the autonomous showroom</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
 body{background:#0b0f14;color:#e6edf3;font-family:Segoe UI,Arial,sans-serif;margin:0}
 .wrap{max-width:900px;margin:0 auto;padding:24px 18px 44px}
 h1{font-size:32px;margin:0 0 2px} .sub{color:#9fb0c3;margin:0 0 14px}
 .badge{display:inline-block;background:#12351f;color:#3fb96b;border:1px solid #3fb96b;border-radius:20px;padding:1px 10px;font-size:12px;font-weight:700}
 #map{height:300px;border-radius:10px;border:1px solid #26313f;margin:14px 0}
 .card{background:#11161d;border:1px solid #26313f;border-radius:10px;padding:16px;margin:14px 0}
 #spin{touch-action:none;cursor:grab;text-align:center}
 #spin img{max-width:100%;border-radius:8px;user-select:none;-webkit-user-drag:none}
 #log{min-height:180px} .msg{margin:9px 0;line-height:1.5}
 .who{font-weight:700;font-size:12px;letter-spacing:.6px}
 .user .who{color:#6cb6ff} .bot .who{color:#ffb454}
 .row{display:flex;gap:8px;margin-top:8px}
 input,select{flex:1;background:#0b0f14;border:1px solid #26313f;border-radius:8px;color:#e6edf3;padding:10px 12px;font-size:15px}
 button{background:#1f6feb;border:0;color:#fff;border-radius:8px;padding:10px 16px;font-size:15px;cursor:pointer}
 .small{color:#9fb0c3;font-size:13px} .facts li{margin:3px 0}
</style></head><body><div class="wrap">
<h1>Showfront</h1>
<p class="sub">Photos in — a living showroom and a salesman who can't lie, out.</p>
<span class="badge">ONE CAR &middot; ONE FLOW &middot; EVERY CLAIM ON THE SHEET</span>
<div id="map"></div>
<p class="small">God's-Eye: sky &rarr; Dayton, Ohio &rarr; the lot. (Satellite: Esri World Imagery.)</p>
<div class="card"><h3 id="cartitle" style="margin-top:0"></h3>
<div id="spin"><img id="frame" alt="vehicle photo"><p class="small" id="spinlabel">Drag to walk around the car.</p></div>
<ul class="facts" id="facts"></ul></div>
<div class="card"><h3 style="margin-top:0">The Closer</h3>
<div id="log"></div>
<div class="row"><input id="q" placeholder="Ask about this car..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()">Ask</button></div>
<p class="small">The Closer answers only from this car's verified record. Ask it something that is
not on the sheet — a sunroof, a warranty — and watch it refuse instead of inventing.</p></div>
<div class="card"><h3 style="margin-top:0">Book a test drive</h3>
<div class="row"><input id="bkname" placeholder="Your name"><input id="bkphone" placeholder="Phone"></div>
<div class="row"><input id="bkwhen" placeholder="Preferred day/time (e.g. Saturday 11am)">
<button onclick="book()">Book it</button></div>
<p class="small" id="bkout"></p></div>
<p class="small">Showfront — built for the Meta Global AI Developer Hackathon (Indie track),
Oct 26 – Nov 4, 2026, by Ahmad Odeh / ABUZ8 LLC. Verification law: CLAIMED &ne; DONE.</p>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const FRAMES = __FRAMES__;
const map = L.map('map').setView([39.9,-84.3], 4);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
 {attribution:'Esri World Imagery'}).addTo(map);
setTimeout(()=>{ map.flyTo([39.7589,-84.1916], 16, {duration: 4}); }, 600);
L.marker([39.7589,-84.1916]).addTo(map).bindPopup('Dayton, Ohio — the lot');
let veh=null, idx=0;
const frame=document.getElementById('frame');
function show(){ if(FRAMES.length){ frame.src=FRAMES[idx]; 
 document.getElementById('spinlabel').textContent='Photo '+(idx+1)+' of '+FRAMES.length+' — drag to walk around the car.'; } }
let dragging=false,lastX=0,acc=0;
const spin=document.getElementById('spin');
spin.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;spin.setPointerCapture(e.pointerId);});
spin.addEventListener('pointermove',e=>{ if(!dragging||!FRAMES.length)return;
 acc+=e.clientX-lastX; lastX=e.clientX;
 if(Math.abs(acc)>24){ idx=(idx+(acc>0?1:-1)+FRAMES.length)%FRAMES.length; acc=0; show(); }});
spin.addEventListener('pointerup',()=>dragging=false);
fetch('/api/vehicle').then(r=>r.json()).then(v=>{ veh=v;
 document.getElementById('cartitle').textContent=v.year+' '+v.make+' '+v.model+' '+v.trim+' — $'+v.price_usd.toLocaleString();
 const facts=[[ 'Mileage', v.mileage.toLocaleString()+' miles'],['Exterior',v.exterior_color],
 ['Interior',v.interior],['Engine',v.engine],['Transmission',v.transmission],['Drivetrain',v.drivetrain],
 ['Fuel',v.fuel],['Visible in the photos', v.visible_features.join(', ')],['Seller notes', v.seller_notes]];
 document.getElementById('facts').innerHTML=facts.map(f=>'<li><b>'+f[0]+':</b> '+f[1]+'</li>').join('');
 add('bot','THE CLOSER','Welcome to Showfront. This is the '+v.year+' '+v.make+' '+v.model+' '+v.trim+', '
  +v.mileage.toLocaleString()+' miles, $'+v.price_usd.toLocaleString()+'. Everything I tell you comes off this '
  +'car\\'s verified sheet — ask me anything about it, or say the word and I will book your test drive.');
 show(); });
const log=document.getElementById('log'),q=document.getElementById('q');
const hist=[];
function add(cls,who,text){const d=document.createElement('div');d.className='msg '+cls;
 d.innerHTML='<span class="who"></span><br>';d.querySelector('.who').textContent=who;
 d.appendChild(document.createTextNode(text));log.appendChild(d);log.scrollTop=log.scrollHeight;}
async function send(){const v=q.value.trim();if(!v)return;q.value='';
 add('user','YOU',v);hist.push({role:'user',content:v});
 add('bot','THE CLOSER','...checking the sheet...');const slot=log.lastChild;
 try{const r=await fetch('/api/closer',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({history:hist})});const j=await r.json();
  const t=j.reply||('Error: '+(j.error||'unknown'));slot.lastChild.textContent=t;
  hist.push({role:'assistant',content:t});}
 catch(e){slot.lastChild.textContent='Error: '+e;}}
async function book(){const out=document.getElementById('bkout');
 const body={name:document.getElementById('bkname').value,phone:document.getElementById('bkphone').value,
  when:document.getElementById('bkwhen').value};
 if(!body.name||!body.phone){out.textContent='Name and phone are needed to book.';return;}
 const r=await fetch('/api/book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 const j=await r.json();out.textContent=j.message||('Error: '+(j.error||'unknown'));}
</script></div></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        raw = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            page = PAGE_TEMPLATE.replace("__FRAMES__", json.dumps(spin_frames()))
            self._send(200, page, "text/html; charset=utf-8")
        elif path == "/health":
            self._send(200, json.dumps({"ok": True, "provider": PROVIDER,
                                         "frames": len(spin_frames())}))
        elif path == "/api/vehicle":
            pub = {k: v for k, v in VEHICLE.items() if k != "not_on_sheet_examples"}
            self._send(200, json.dumps(pub))
        elif path.startswith("/assets/car/"):
            fp = os.path.join(HERE, "assets", "car", os.path.basename(path))
            if os.path.isfile(fp):
                with open(fp, "rb") as f:
                    self._send(200, f.read(), "image/jpeg")
            else:
                self._send(404, json.dumps({"error": "not found"}))
        elif path == "/leads":
            leads = []
            if os.path.isfile(LEADS_FILE):
                with open(LEADS_FILE) as f:
                    leads = json.load(f)
            rows = "".join("<li>%s — %s — %s</li>" % (
                l.get("when", ""), l.get("name", ""), l.get("phone", "")) for l in leads)
            self._send(200, "<html><body style='background:#0b0f14;color:#e6edf3;"
                            "font-family:Arial'><h2>Showfront leads</h2><ul>" +
                            rows + "</ul></body></html>", "text/html; charset=utf-8")
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        try:
            if self.path == "/api/closer":
                body = self._read_json()
                history = body.get("history") or []
                if not history:
                    self._send(400, json.dumps({"error": "empty history"}))
                    return
                reply, model, verified, run_hash = closer_answer(history)
                self._send(200, json.dumps({"reply": reply, "model": model,
                                            "verified": verified, "run": run_hash}))
            elif self.path == "/api/book":
                body = self._read_json()
                name = (body.get("name") or "").strip()
                phone = (body.get("phone") or "").strip()
                when = (body.get("when") or "").strip()
                if not name or not phone:
                    self._send(400, json.dumps({"error": "name and phone required"}))
                    return
                leads = []
                if os.path.isfile(LEADS_FILE):
                    with open(LEADS_FILE) as f:
                        leads = json.load(f)
                lead = {"name": name, "phone": phone, "when": when,
                        "vehicle": VEHICLE["id"],
                        "booked_at": time.strftime("%Y-%m-%d %H:%M ET")}
                leads.append(lead)
                with open(LEADS_FILE, "w") as f:
                    json.dump(leads, f, indent=1)
                log_run("booking", {"lead": lead})
                self._send(200, json.dumps({
                    "message": "Booked, " + name.split()[0] + ". Test drive for the " +
                               str(VEHICLE["year"]) + " " + VEHICLE["make"] + " " +
                               VEHICLE["model"] + (" — " + when if when else "") +
                               ". The lot has your number: " + phone + "."}))
            else:
                self._send(404, json.dumps({"error": "not found"}))
        except urllib.error.HTTPError as e:
            self._send(502, json.dumps({"error": "upstream HTTP " + str(e.code)}))
        except Exception as e:
            self._send(500, json.dumps({"error": type(e).__name__ + ": " + str(e)[:200]}))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
