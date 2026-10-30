# Showfront — New Work Statement (Meta Global AI Developer Hackathon, Oct 26 – Nov 4, 2026)

**Everything in this repository was written during the hackathon window.** The git history of this repo is the evidence: first commit Oct 26, 2026.

## Built during the event (new)
- The Showfront pipeline: intake → SAM 3.1 segmentation → SAM 3D car reconstruction → Muse Image scene pass → interactive viewer (God's Eye fly-in + splat lot + 3D cars) → Muse Spark / Muse Wonder copy + verification → commercial render → Postiz publish.
- The Closer: a dealership salesman agent (new agent, built for this event) — in-experience guide + lead follow-up, facts-only guardrails.
- The web viewer, results page, and all glue code in this repo.

## Pre-existing assets used (NOT presented as new work)
- Domain knowledge from LotVue360, the founder's separate year-long dealership-software project. **No LotVue360 code is in this repository or this entry.**
- Test photographs of vehicles and premises, taken by the founder / family dealership (rights held).
- The founder's Pegasus lab know-how (Gaussian-splat workflows proven before the event).
- Open-source components under their own licenses, credited in README (incl. Bilawal Sidhu's God's Eye View concept/repo — see README credits; Meta SAM 3D under the SAM License).

## Team
Solo participant: Ahmad Odeh (ABUZ8 LLC). AI coding agents were used as tools under his direction.

---

## Addendum — Oct 30, 2026 (build relocation + scope narrowing, disclosed)

On Oct 30, 2026, an area-wide power and internet outage took the founder's
build machine (Pegasus) offline indefinitely. The in-progress local build
had never been pushed and became unreachable. From Oct 30, the build
continues on the team's cloud machine, in this repository, inside the
same hackathon window — the git history shows exactly which commits are
which.

Per the spec's own fallback rule (decided Oct 30, never Nov 3), the demo
slice narrows to the agent-first flow: God's-Eye fly-in → 360 photo spin →
the Closer → honest listing → test-drive booking. Gaussian splatting,
SAM 3D reconstruction, the commercial render, and Postiz auto-publish move
to the roadmap for this entry and are NOT claimed as delivered.

Two further disclosures, in the open:
- The Closer in `app/` runs against a SAMPLE vehicle record (labeled as
  such in the record itself), per the spec's agent-first build order.
- Development and testing of the Closer used a non-Meta model substitute
  while the Meta API key was unreachable on the offline machine. Every run
  log records the provider that actually answered; no development run is
  presented as Meta tooling. The submission configuration targets Muse
  Spark Open (Meta open weights) via Baseten.
- The demo photo set is a freely licensed set, credited in
  `app/assets/car/CREDITS.md`, standing in for the founder's vehicle
  photographs, which are on the offline machine.
