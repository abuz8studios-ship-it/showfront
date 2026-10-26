# Showfront

**An autonomous showroom for anyone with a car.**

You photograph your car. Showfront turns those photos into an interactive 360 spin, a 3D Gaussian-splat walkaround a buyer can explore from home, a finished video commercial, and a written listing - then publishes the package by itself.

For a dealership, it runs on every new arrival. For an enthusiast or private seller, it runs on the car in your driveway - to sell it, or to show it the way it deserves.

Built for the **Meta Global AI Developer Hackathon** (Oct 26 - Nov 4, 2026) - **Indie track**, theme **Build for Your World** - by Ahmad Odeh, solo founder of ABUZ8 LLC (Dayton, Ohio).

## The pipeline

1. **Intake** - a walk-around photo set of one vehicle + a small vehicle form.
2. **Segment** - SAM 3.1 (Meta Model API) isolates the vehicle from its surroundings.
3. **Scene** - Muse Image builds the showroom environment; the vehicle is composited in.
4. **Spin** - an interactive 360 viewer for the buyer.
5. **Walkaround** - a 3D Gaussian splat of the vehicle, explorable in the browser like you're standing next to it.
6. **Copy** - Muse Spark writes the listing and the commercial script - only from facts in the vehicle form and what's visible in the photos. Nothing invented.
7. **Commercial** - a rendered video from the walkaround, with voiceover and branding.
8. **Publish** - the full package posts to social channels automatically (Postiz, self-hosted).

Full build spec: [SPEC.md](SPEC.md)

## Why

Anyone selling a car loses money to bad photos - independent dealers, and the millions of private sellers whose driveway photos compete against dealer-grade presentation. Showfront gives any seller, lot or driveway, the presentation power of a national franchise, the same day. Real-world test cases: DriveSmart Auto Sales (Dayton, OH), the founder's brother's dealership - and the founder's own cars, as the enthusiast case.

## Built during the hackathon - disclosure

Every line of code in this repository was written during the hackathon window, Oct 26 - Nov 4, 2026. This project's git history is the evidence.

Pre-existing assets, used with rights and disclosed honestly:

- **Domain knowledge** from the author's earlier dealer tooling (LotVue360). That product is NOT part of this entry and no code from it is presented here.
- **Test vehicle photographs** taken by/for the author.
- **Lab know-how** for Gaussian splatting from experiments on the author's own GPU workstation earlier in October 2026. All code in this repo is new.

## Status

Day 0 (Oct 26): repo live, spec committed. Build log lands here as each stage passes its acceptance probe - see SPEC.md section 6.

## Links

- Founder: https://abuz8ai.com
- GitHub: https://github.com/abuz8studios-ship-it
- Hugging Face: https://huggingface.co/abuz8studios

MIT licensed - see [LICENSE](LICENSE).
