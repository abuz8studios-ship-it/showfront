# SHOWFRONT — Build Spec
Meta Global AI Developer Hackathon · Indie track · Theme: Build for Your World
Builder: Ahmad Odeh (solo), ABUZ8 LLC · Window: Oct 26 – Nov 4, 2026 · Submit Nov 3

## 1. SCOPE
**One sentence:** A car enthusiast photographs their car; Showfront — new code, written entirely during the hackathon — turns those photos into an interactive 360 spin, a 3D Gaussian-splat walkaround a buyer can explore from home, a finished video commercial, and a written listing, then publishes the package by itself. **Audience (Ahmad's direction, Oct 26, refined same day): FOR CAR ENTHUSIASTS — not dealers-only, and not "anyone with a car" either. His framing: everyone who has a car is an enthusiast to a degree, so the product speaks to people who love their car — the collector, the builder, the private seller who cares how their car is presented, and the dealer whose lot is full of cars they love.** A dealer runs it for every arrival; an enthusiast runs it for the car in their driveway — to sell it, or just to show it the way it deserves.

**In scope (the demo slice — ONE car, ONE lot, ONE flow, bulletproof):**
1. Photo intake: a folder/phone upload of 12–40 walk-around photos of one vehicle.
2. Vehicle isolation + scene build (SAM 3.1, Muse Image).
3. Interactive 360 spin (web viewer).
4. Interactive 3D Gaussian-splat walkaround (web viewer, orbit + move).
5. Listing copy + commercial script (Muse Spark).
6. Commercial render: splat-orbit footage + voiceover + store branding, exported MP4.
7. Auto-publish: package posts to the store's social channels via Postiz (self-hosted).
8. A public results page (the "showfront") where the buyer opens the car: spin, walkaround, commercial, listing.

**Out of scope (roadmap, never demoed as done):** multi-lot/multi-tenant, in-store kiosk hardware, CRM/DMS integrations, payments, inventory feeds, interior splats, more than one vehicle per run.

**New-work compliance (hard law for this entry):**
- Every line of presented code is written Oct 26 – Nov 4, 2026 in ONE new public repo: `showfront`.
- Pre-existing assets used and DISCLOSED in the README: (a) domain knowledge from the author's earlier dealer tooling (LotVue360, not part of this entry); (b) the test vehicle's photographs (author has rights); (c) Pegasus lab know-how for Gaussian splatting (FreeSplatter pipeline tested Oct 2026) — code in this repo is newly written for the event.
- The demo video shows ONLY features built during the event.
- Anti-project check: not an image analyzer (imaging is step 2 of an 8-step autonomous pipeline), not a dashboard (output is a published buyer experience, not charts), not RAG, not a chatbot, not Streamlit.

## 2. PRD — the product in plain words
- **User 1 (the car's owner — dealer OR enthusiast/private seller):** drops photos of the car into Showfront, adds year/make/model/mileage/price in one small form, presses Run. Touches nothing else. For a dealer it's every new arrival; for an enthusiast it's their own car — listed for sale, or showcased as a build.
- **User 2 (buyer / viewer):** opens a link. Walks around the car in 3D from their couch. Watches the commercial. Reads an honest listing. Sends a lead / contacts the seller.
- **Why it matters (Impact, 30%):** anyone selling a car loses money to bad photos — independent dealers AND the millions of private sellers on marketplaces, whose driveway photos compete against dealer-grade presentation. Showfront gives any seller, lot or driveway, the presentation power of a national franchise, the same day. Firsthand test case: DriveSmart Auto Sales (Dayton, OH), the founder's brother's dealership — with the founder's own cars as the enthusiast test case. Audience expansion is POSITIONING only: the demo slice stays one car, one flow — the same pipeline serves both users unchanged.
- **Success = the demo runs end-to-end live, on a real car, in under 10 minutes of processing.**

## 3. TECHNICAL SPEC
**Stack:** Python pipeline + static web viewer. Meta Model API: SAM 3.1 (segmentation), Muse Image (scene generation), Muse Spark (listing copy, commercial script, run narration). Muse Voice Transcribe optional for dealer voice notes on the vehicle. Muse Code as the coding agent (Meta stack rule). Gaussian splatting: pose-free splat generation from the photo set (FreeSplatter-class pipeline) on Pegasus (2× RTX 5090); PLY export; web splat viewer (GaussianSplats3D / Spark-class JS viewer). 360 spin: frame sequencing from the walk-around set with the segmented vehicle composited on the generated scene. Commercial: orbit render of the splat → MP4 with TTS voiceover (script by Muse Spark) + store logo/end-card. Publishing: Postiz (self-hosted, already registered in the author's stack) to Instagram, Facebook, TikTok, X. Hosting: static page on Cloudflare Pages + repo on GitHub (public).

**Pipeline stages (each stage logs input → output + hash; a stage failure stops the run loudly, never fakes an output):**
1. `intake` — validate photo set (count, blur, coverage), read the vehicle form.
2. `segment` — SAM 3.1 vehicle mask per frame; QC: mask coverage report.
3. `scene` — Muse Image showroom environment; composite vehicle.
4. `spin` — ordered frames → interactive 360 viewer data + a spin MP4.
5. `splat` — photo set → Gaussian splat (PLY) + web walkaround viewer.
6. `copy` — Muse Spark: listing (title, features honestly limited to visible/form data — no invented options), social captions, commercial script (30–45 s).
7. `commercial` — splat orbit render + voiceover + branding → MP4.
8. `publish` — Postiz posts the package; results page goes live; run report written.

**Repo layout:** `pipeline/` (stages 1–8), `viewer/` (spin + splat + results page), `assets/` (test vehicle set, disclosed), `runs/` (run reports), `README.md` (with the Built-During-The-Hackathon disclosure section), `LICENSE` (MIT).

## 4. BLUEPRINT — build order (each step ends with a proof artifact)
1. **D0 Oct 26:** repo created public; spec + README disclosure committed. Credits claimed (Ahmad). Meta API key live in a local env file (never committed).
2. **D1 Oct 27:** intake + segment working on the test car; mask QC report committed. (Agents 101 session 12:00 — attend.)
3. **D2 Oct 28:** scene + spin viewer live on a test page. (Agents 102 session 12:00 — attend.)
4. **D3 Oct 29:** splat walkaround viewer live (Muse free-limit reset 14:23 — heavy build afternoon).
5. **D4 Oct 30:** copy + commercial render end-to-end. (Fireworks session 12:00 optional.)
6. **D5 Oct 31:** publish leg (Postiz) fires a real post from a real run. Grok adversarial review of the demo plan.
7. **D6 Nov 1:** full end-to-end run on the final car, timed; results page frozen.
8. **D7 Nov 2:** demo video recorded + locked (3:00 max). X post drafted for the Most Viral entry.
9. **D8 Nov 3:** SUBMIT (a day early). Buffer Nov 4. Finals Nov 9.

## 5. STORYBOARD — the 3-minute demo video
1. 0:00–0:20 — The problem, real: a good car on a small lot, phone photos that undersell it. Ahmad on camera or voiceover: "This car deserves better than this."
2. 0:20–0:40 — Photos dropped into Showfront. One form. Run.
3. 0:40–1:20 — The pipeline visibly working: SAM 3.1 mask, scene built, spin assembling.
4. 1:20–2:00 — The walkaround: buyer view, orbiting and moving around the car in the browser. The wow beat.
5. 2:00–2:30 — The commercial plays — generated from the same walkaround, store branding, voiceover.
6. 2:30–2:50 — The posts appear on the store's socials by themselves; the listing is live.
7. 2:50–3:00 — Close: "Built in ten days by one person, for the lot his brother runs. Showfront."

## 6. ACCEPTANCE PROBES (pass/fail, evidence or it didn't happen)
1. Repo public, first commit dated within Oct 26 – Nov 4, README carries the new-work disclosure. 
2. SAM 3.1 call is real: API response/log for the test run on file; masks shown in the run report.
3. Splat viewer loads the test car's PLY in a browser and orbits — screen recording.
4. Spin viewer completes a full 360 with no missing quadrant.
5. Commercial MP4 plays with voiceover + end card; script file matches the audio.
6. Listing copy contains ZERO facts not in the vehicle form or visible in photos (manual check against the form).
7. One real publish lands on at least one live social account with a URL.
8. Full run from intake to published in one sitting, timed, run report committed.
9. Demo video ≤ 3:00, shows only in-window features.
10. Submission form filed Nov 3 with: public repo link, video link, disclosure text — screenshot of the submitted state.

## 7. RISKS + FALLBACKS
- Splat quality from phone photos is the #1 technical risk → fallback: splat from the spin frame set; if splat fails the probe by Oct 30, the entry narrows to spin + commercial (still a complete pipeline) and splat moves to roadmap — decided Oct 30, never Nov 3.
- Meta API credits lag (up to 2 business days) → claim filed Oct 26; Baseten/Modal partner credits as bridge.
- Postiz publish failure → manual post of the same package with the run report as proof of generation; publish leg retried once.

## 8. ARCHITECTURE v2 — research inputs (Ahmad, Oct 26, from his own viewing)
Three layers, each with a named source:
1. **God's Eye layer (place):** Bilawal Sidhu's open-source God's Eye View (github.com/bilawalsidhu/gods-eye-view) — map/satellite data assembles the location in 3D; camera flies sky → city → lot. (License/stack audit = Aisha's night job Oct 26.)
2. **Splat layer (truth on the ground):** filmed walkthrough video → frames → splat trained locally on Pegasus (Postshot or LichtFeld Studio; training is now ~3x faster per Radiance Fields' Oct 2026 reporting) → streamed in the browser via an open splat viewer (Aholo / Spark.js class: LOD + streaming + collision, so a buyer can WALK the lot, not just orbit). UE5 (NanoGS-class plugins) is the later Ready-Player-One client, not the hackathon slice.
3. **Car layer (Meta-native):** SAM 3.1 (Meta Model API) segments the car; Meta's SAM 3D Objects (open weights, facebookresearch/sam-3d-objects, SAM License) reconstructs a textured 3D model of the car from even ONE photo — GLB/PLY out. SAM 3.1's mask is literally SAM 3D's required input: the Meta stack chains. SAM 3D runs on Pegasus (needs ~16GB+ VRAM; the 5090s have 32GB). Fallback/quality path: multi-photo splat of the hero car when time allows.
Demo arc (updated): God's-eye flight to the lot → walk the splat lot in the browser → tap the hero car → its SAM 3D model spins → commercial (rendered from the walkaround) → package auto-posts.

## 9. MODULE — THE CLOSER: a dealership salesman agent (Ahmad, Oct 26)
The experience brings the buyer; the agent sells. Two jobs:
1. **In-experience guide:** lives inside the walkaround — greets the visitor, presents the car from VERIFIED facts only (inventory record + photos; invents nothing), answers questions, books the test drive.
2. **Follow-up agent:** works captured leads by message — re-engagement, objection handling, appointment setting (the BDC job, 24/7).
**Brain:** built from Ahmad's own sales library (the 66-books system): Jeremy Miner (NEPQ question frameworks), Alex Hormozi (offer framing, value stacking), Andy Elliott (closing energy, word tracks), Robert Greene (buyer psychology), Adam Young. FRAMEWORKS AND PRINCIPLES, not copied book text. Honesty guardrails (his brand): AI disclosure where required, no invented car facts, no pressure tactics that misrepresent — teacher-seller, not trick-seller.
**Why it's in the Meta build:** it is the agentic layer of Showfront (Best Agentic Use-Case bonus lane) and the revenue bridge to Mohammed: Showfront makes the showcase, the Closer works the leads it captures.
**Credits map (confirmed Oct 26 by Ahmad):** Meta Model API $150 (SAM 3.1 / Muse Spark / Muse Image calls) · Modal ~$30 (GPU bursts: splat training + SAM 3D jobs as endpoints) · Baseten account live (Muse Spark Open inference, hackathon string meta-models/muse-spark-open-1026; $100 partner request pending review).

## 10. NORTH STAR — DEALER SIMULATOR (Ahmad, Oct 26)
"Microsoft Flight Simulator, but for buying a car." Flight Sim's paradigm: real-world data streamed into a 1:1 world you move through. Dealer Simulator: the dealership and its cars as a living 1:1 world — walk the lot, open the door, get in, start it, configure it, then do the real deal without leaving the world.
**The fusion Ahmad named:**
- **vAuto** = the pricing/inventory brain (market data, days-supply, pricing intelligence)
- **DealerCenter + Dealertrack + Frazer** = the DMS/CRM backbone (deals, financing, paperwork, compliance)
- **AutoTempest** = the shopper front door (every listing, one search)
- **Mercedes/BMW** = the experience standard (configurator-grade polish, cinematic brand film)
- **The Closer (Module 9)** = the salesman inside the world
- **Showfront (this build)** = the world layer: God's Eye place + splat lot + SAM 3D cars
**Technical truth:** splats cannot open doors — the world is splat, the CARS are interactive meshes (SAM 3D GLB, later rigged: doors/hood/trunk open, interior view = captured 360 interior). Hybrid is the architecture.
**Ladder:** L1 Showfront (hackathon, Nov 2026: fly-in, walkable lot, tappable 3D cars, the Closer, commercial, auto-post) → L2 Interactive Car (one hero car: open the door, sit inside, start it) → L3 Dealer Simulator (full fusion: inventory brain + DMS + finance + signature inside the world; this is the company-scale product, the true successor to the LotVue year).

## 11. THE COUNCIL — every Meta model, one job each (Ahmad's order, Oct 26)
- **SAM 3.1** (Meta Model API): segments every car and lot object; masks feed everything downstream.
- **SAM 3D Objects** (Meta open weights, on Pegasus): one photo + SAM mask → textured 3D car (GLB).
- **Muse Image** (API): scene dressing, commercial key frames, listing hero images.
- **Muse Spark** (API): the Closer's live brain + listing copywriter — fast, in the experience.
- **Muse Wonder** (API): the director/verifier — writes the commercial script + storyboard, then VERIFIES Spark's listing against the vehicle record before anything publishes (verifiable-agent pattern: no unverified fact ships).
- **Muse Voice Transcribe** (API): turns the dealer's spoken walkthrough + buyer voice messages into structured facts the pipeline and the Closer use.
- **Muse Spark Open / Glimmer** (open weights, Baseten + Pegasus): the Closer's second engine — the same agent running on Meta open weights (open-weights bonus lane; also the privacy lane for dealer data).
- **Muse Code**: the build tool — credited in README as tooling, never presented as a model in the product.
Every model call is logged per vehicle run; the run report (acceptance probe 6) lists which models touched the car — tooling usage is provable, not claimed.
