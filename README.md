# Movidence

**No agent gets to say "your video has been sent" until Kane CLI has opened the actual file, pressed play, and seen real frames move.**

Movidence (motion + evidence) is a delivery gate for AI agents. When an agent wants to report that a video was delivered — "sent", "ready to watch", "here it is" — the claim goes through the gate first. The gate hands the real file to Kane CLI, which opens it in a real browser, plays it, and runs a visual verification. The claim is **RELEASED** only if Kane's run produces visual evidence of moving frames with real picture content. Otherwise the claim is **BLOCKED**, rewritten honestly ("Not sent. The delivery could not be verified…"), and logged with Kane's own session recording as the witness.

## Why this exists

On 15 November 2026, an AI assistant delivered a video that was blank — a black screen from first frame to last — and reported it as sent. The recipient opened it, saw nothing, and had to rename the file by hand just to open it at all. Nothing in the pipeline had ever *watched* the file. Every check had taken the sender's word for it.

This gate removes the sender's word from the loop. The file itself is the only witness that counts, and Kane CLI is the one who questions it.

## How it works

```
agent claim ──► gate.mjs ──► Kane CLI (visual run, real browser)
                    │                │
                    │        evidence: moving frames? black screen?
                    ▼                ▼
            RELEASED (claim sent as-is, witness attached)
            BLOCKED  (claim rewritten honestly, witness attached)
                    │
                    ▼
        verdicts.json + index.html (the verdict page)
```

- `gate/gate.mjs` — the gate. It builds a unique check for each delivery, calls Kane CLI directly (no shell in between — see "What Kane caught" below), and reads Kane's **evidence**, not just its pass/fail headline.
- **Fail-closed by design:** a release requires positive visual evidence in Kane's run record — a "moving frames" variable that is true and a "black/blank screen" variable that is false, with no contradicting values. A run that passes but produces no visual proof is treated as **not verified** and the claim is blocked.
- Every attempt is appended to `verdicts.json` and rendered to `index.html`, each with a link to Kane's witness recording. The page also draws a strip of frames sampled from each checked sample file — what Kane saw, made visible: real picture frames for the released video, black frames for the blank one, empty frames for the file that could not play.

## Run it yourself (judges)

You need Node.js, Kane CLI, and about 30 Kane credits per check (a fresh account gets 10,000 free).

```bash
npm install -g @testmuai/kane-cli
kane-cli login --oauth

# from the repo root, serve the files locally:
npx --yes serve -l 8000 .

# in a second terminal, put a delivery claim through the gate:
node gate/gate.mjs http://localhost:8000/samples/good.mp4    "Your video has been sent and is ready to watch."
node gate/gate.mjs http://localhost:8000/samples/blank.mp4   "Your video has been sent and is ready to watch."
node gate/gate.mjs http://localhost:8000/samples/corrupt.mp4 "Your video has been sent and is ready to watch."
```

Expected results (these exact runs are committed in `verdicts.json`):

| File | What it is | Verdict |
|---|---|---|
| `samples/good.mp4` | Real moving video (colour test pattern, 6s) | **RELEASED** — Kane saw moving frames, no black screen |
| `samples/blank.mp4` | 5s of pure black frames | **BLOCKED** — Kane's visual checks recorded moving frames: false, black/blank screen: true |
| `samples/corrupt.mp4` | A truncated, unplayable file | **BLOCKED** — the player could not play it at all; no visual proof exists |

Witness recordings for the committed runs:

- good → RELEASED: https://test-manager.lambdatest.com/projects/01M84G8RKNGTA7ADEM5WB5K3S6/test-cases/01M8BY6CD0GC21FZYXH4MT0RWZ/dashboard/share/US_7HCV7MW1KBB2NECMC6570EEP66XXA1ZINPANZUXVO9QRALOO833OA1MV9BNEZQ6G?type=summary&agentView=true&fqdn=summary-page
- blank → BLOCKED: https://test-manager.lambdatest.com/projects/01M84G8RKNGTA7ADEM5WB5K3S6/test-cases/01M8BYJ1AMFM7N53E6BH6031JK/dashboard/share/US_5O76VO9M148V8DCKSZKK3UO29VPB3HHGXL5LEW4VV0AMLYBKFY6FX364LJCFKNBC?type=summary&agentView=true&fqdn=summary-page
- corrupt → BLOCKED: https://test-manager.lambdatest.com/projects/01M84G8RKNGTA7ADEM5WB5K3S6/test-cases/01M8BZ3ZSBJ0TV5TQDWR0Q3FDZ/dashboard/share/US_IOISKTYVVK08AIUHMXET4UDB0XPU1Z5EYB53VVELCNYGVN61643RFJKH81R17XEV?type=summary&agentView=true&fqdn=summary-page

If you don't want to run anything, open `index.html` — it is the verdict page from the committed runs, with the same witness links.

## What Kane caught while we built this

The gate's own development is the best evidence for why it exists. Four times, a check looked green while proving nothing — and each time, Kane's records are what exposed it:

1. **The replay.** Asking Kane the identical question twice returned the previous run's verdict at a tenth of the credits — a replay, not a fresh watch. Fix: every delivery check carries a unique ID, so no two checks are ever the same question.
2. **The wrapper.** Pointed at a playback page instead of the raw file, Kane counted "played to the end" as success and never let the picture check decide. Fix: the gate hands Kane the file itself.
3. **The vacuous pass.** One run reported success with an *empty* evidence record — a pass that had seen nothing. Fix: the fail-closed evidence rule above. No proof, no release, whatever the headline says.
4. **The mangled instruction.** The gate originally launched Kane through a Windows shell, which passed the check's wording through unquoted — Kane received a thinner instruction than the one written, and its runs came back hollow. Fix: the gate now resolves Kane CLI's JavaScript entry point and spawns it directly, with no shell.

Each catch closed the loop the same way: Kane's evidence showed the gap, the gate changed, the same file was re-checked until the verdict was earned.

## The phone chapter (honest status)

The gate was designed to verify playback **on a phone**, because that is where the original blank video landed. A minimal Android player app (`tests/player.apk`, source in `player-app/`) accepts a video URL and plays it, and a Kane test (`tests/phone-spike_test.md`) loads a delivered video into it on a cloud Pixel 8 Pro (Android 14) and verifies real frames.

What is proven: the test plan validates cleanly against the remote grid, the device resolves, and the app uploaded successfully to TestMu (app id `APP10160321641795624873061412`).

What is **not** proven: the remote run itself. Both dispatch attempts failed inside TestMu's HyperExecute grid with a server-side error (`Push secret failed: 500` from the grid's secrets service) before any test step ran — no credits were consumed and no test executed. The desktop-browser gate above is the verified path and the one used for every verdict in this repo. The phone artefacts are included so the attempt, and its evidence, can be inspected.

## Files

- `gate/gate.mjs` — the gate script
- `verdicts.json` / `index.html` — the verdict log and page (committed runs)
- `samples/` — the three controlled sample files (good / blank / corrupt)
- `player.html` — a minimal standalone playback page (kept for reference; the gate verifies raw files)
- `tests/phone-spike_test.md`, `tests/player.apk` — the phone verification test and player app
- `player-app/` — the player app's source

## Credits and licence

Built by Precious Azuka for the Kane CLI Hackathon (TestMu AI). Verified with Kane CLI on a free TestMu account. The committed sample videos are synthetic test files generated for this project.
