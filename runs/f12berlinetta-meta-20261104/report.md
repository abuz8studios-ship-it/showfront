# Showfront run f12berlinetta-meta-20261104 — DONE
Started 2026-11-04T21:44:26Z, finished 2026-11-04T21:46:44Z (137.83s).

Vehicle: 2013 Ferrari F12berlinetta

## Stages
| # | stage | provider | in | out | t(s) |
|---|-------|----------|----|-----|------|
| 1 | intake | local:intake-validator | 13 | 1 | 0.14 |
| 2 | segment | meta:sam-3.1 | 12 | 13 | 16.05 |
| 3 | scene | meta:muse-image | 13 | 12 | 24.52 |
| 4 | spin | local:imageio-ffmpeg-spin | 12 | 4 | 24.83 |
| 5 | splat | local:proxy-splat | 12 | 4 | 50.93 |
| 6 | mesh3d | skipped | 0 | 0 | 50.95 |
| 7 | interior | hloc+opencv-stitcher | 0 | 1 | 50.95 |
| 8 | copy | meta:muse-spark+meta:muse-wonder | 1 | 5 | 130.06 |
| 9 | commercial | local:ffmpeg-commercial+local:sapi | 2 | 3 | 137.67 |
| 10 | publish | local:staged (no POSTIZ_API_URL/KEY) | 2 | 1 | 137.69 |

## Models touched

- `hloc+opencv-stitcher`
- `local:ffmpeg-commercial+local:sapi`
- `local:imageio-ffmpeg-spin`
- `local:intake-validator`
- `local:proxy-splat`
- `local:staged (no POSTIZ_API_URL/KEY)`
- `meta:muse-image`
- `meta:muse-spark+meta:muse-wonder`
- `meta:sam-3.1`
- `skipped`

## Acceptance probes
| probe | stage | status | detail | evidence |
|-------|-------|--------|--------|----------|
| photos-in-range | intake | pass | 12 unique photos (need 12-40) | `stage/intake.json` |
| blur-qc | intake | pass | 0 blurry flagged (backend: cv2) | `stage/intake.json` |
| segment-mask-qc | segment | pass | mean_coverage=0.3883 | `stage/mask_qc.json` |
| spin-full-360 | spin | pass | full_360=True missing=[] | `stage/spin/spin_qc.json` |
| splat-present | splat | pass | splat.ply present=True synthetic_demo=True | `stage/splat/splat_meta.json` |
| mesh3d-true3d | mesh3d | not-run | skipped: SHOWFRONT_MESH3D=off | `stage/mesh3d/mesh3d.json` |
| interior-eyes | interior | fail | 0 eye points / 0 details | `stage/interior/interior.json` |
| copy-verified | copy | pass | violations=0 script_words=81 features=16 | `stage/copy/listing.json` |
| commercial-script-audio-match | commercial | pass | script_matches_audio=True duration_s=76.7 voiceover=sapi:offline-windows-voice | `stage/commercial/commercial_meta.json` |
| publish-honest | publish | pass | status=staged-local urls=0 | `stage/publish/publish_manifest.json` |
| closer-guardrail | closer | pass | price reply verifies clean; sunroof refused=True; violations=0 | `closer/SYSTEM_PROMPT.md` |