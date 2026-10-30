# Showfront — salvage build (the runnable appliance)

One car, one flow, end to end: God's-Eye fly-in → 360 photo spin → **the
Closer** (sales agent that presents only from the verified vehicle record,
refuses off-sheet facts, books the test drive) → honest listing → lead
captured.

## Run it

```bash
python3 app.py            # serves on PORT (default 8902), stdlib only
```

Open `/` for the buyer experience, `/leads` for captured test-drive leads,
`/health` for liveness.

## The Closer's brain (read this before believing any claim)

`CLOSER_PROVIDER` selects the model, and **every run log under `runs/`
records which provider actually answered** (provider, model, hash of the
exchange):

- `baseten` — Muse Spark Open (Meta open weights),
  `meta-models/muse-spark-open-1026` via Baseten. The submission provider.
- `nebius` — a non-Meta substitute used ONLY so the build could be
  developed and tested while the Meta API key was unreachable (see
  NEW_WORK.md, Oct 30 addendum). A run served by this provider is
  development evidence, never a Meta-tooling claim.

## The guardrail is code, not a promise

After the model answers, a verification pass extracts every number in the
reply and checks it against `vehicle.json`. Any number that is not on the
sheet replaces the whole reply with the refusal line. Feature questions
are bounded by the record in the system prompt; the demo's trap question
(sunroof / heated leather / warranty) is answered with a refusal, on the
record, every time.

## Files

- `app.py` — the whole appliance (server, page, Closer, booking, leads).
- `vehicle.json` — the verified record for the demo car. Its `status`
  field says plainly that it is a SAMPLE record (spec §12 sanctions a
  sample record for the agent-first build); a real vehicle's record swaps
  in at intake without code changes.
- `assets/car/` — the demo photo set for the spin viewer, with credits.
- `runs/` — per-call run logs (created at runtime; the proof trail).
