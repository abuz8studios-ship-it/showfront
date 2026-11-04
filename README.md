# Showfront

**An autonomous showroom for car enthusiasts.**

You photograph your car - because you love it, and it deserves to be seen properly. Showfront turns those photos into an interactive 360 spin, a 3D Gaussian-splat walkaround a buyer can explore from home, a finished video commercial, and a written listing - packaged ready to publish.

For an enthusiast, it runs on the car in your driveway - your build, your classic, the one you're selling to someone who'll love it next. For a dealership, it runs on every new arrival. Same button, same love.

Built for the **Meta Global AI Developer Hackathon** (Oct 26 - Nov 4, 2026) - **Startup track**, theme **Build for Your World** - by Ahmad Odeh, solo founder of ABUZ8 LLC (Dayton, Ohio).

## The pipeline

1. **Intake** - a walk-around photo set of one vehicle + a small vehicle form.
2. **Segment** - SAM 3.1 (Meta Model API) isolates the vehicle from its surroundings.
3. **Scene** - Muse Image builds the showroom environment; the vehicle is composited in.
4. **Spin** - an interactive 360 viewer for the buyer.
5. **Walkaround** - a 3D Gaussian splat of the vehicle, explorable in the browser like you're standing next to it.
6. **Copy** - Muse Spark writes the listing and the commercial script - only from facts in the vehicle form and what's visible in the photos. Nothing invented. Muse Wonder independently verifies every claim against the vehicle record before anything ships.
7. **Commercial** - a rendered video from the walkaround, with voiceover and branding.
8. **Publish** - the package is staged for social posting (Postiz, self-hosted) with a full publish manifest; live auto-posting activates with channel credentials.

Full build spec: [SPEC.md](SPEC.md)

## Why

Everyone who has a car is an enthusiast to a degree - and anyone who loves their car loses something when it's presented with bad photos. Private sellers compete against dealer-grade presentation; small dealers compete against national chains. Showfront gives the person who loves the car the presentation it deserves. Real-world test cases: DriveSmart Auto Sales (Dayton, OH), the founder's brother's dealership - and the founder's own cars, the enthusiast case.

## Built during the hackathon - disclosure

Every line of code in this repository was written during the hackathon window, Oct 26 - Nov 4, 2026. This project's git history is the evidence.

Pre-existing assets, used with rights and disclosed honestly:

- **Domain knowledge** from the author's earlier dealer tooling (LotVue360). That product is NOT part of this entry and no code from it is presented here.
- **Test vehicle photographs** taken by/for the author.
- **Lab know-how** for Gaussian splatting from experiments on the author's own GPU workstation earlier in October 2026. All code in this repo is new.

## Status

Complete and verified Nov 4, 2026. Final end-to-end run on the test vehicle (2013 Ferrari F12berlinetta): **DONE in 137.8 seconds** - segment `meta:sam-3.1`, scene `meta:muse-image`, copy `meta:muse-spark` + `meta:muse-wonder`, commercial rendered locally, publish staged with manifest. The run report is committed under `runs/`. A full local run (no API key) also completes - every stage keeps a local fallback provider, and the run report logs which provider produced each artifact.

Known limits, stated plainly: the 3D mesh stage is optional and skipped in the verified run; the interior stage produces stitched views, not a true 360 panorama; publish is staged, not live-posted, in this build.

## Links

- Live demo: https://f12berlinetta-360.pages.dev
- Founder: https://abuz8ai.com
- GitHub: https://github.com/abuz8studios-ship-it
- Hugging Face: https://huggingface.co/abuz8studios

MIT licensed - see [LICENSE](LICENSE).
