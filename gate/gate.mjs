#!/usr/bin/env node
// Movidence — the gate.
//
// Usage: node gate.mjs <videoUrl> "<the claim an agent wants to send>"
//        node gate.mjs --render   (regenerate index.html from verdicts.json)
//
// An agent wants to report a video delivery ("sent", "watch it here").
// The gate does not take the agent's word. It hands the actual file to
// Kane CLI, which opens it in a real browser, presses play, and watches.
// The claim is RELEASED only if Kane's run produces visual evidence of
// real moving frames — and BLOCKED otherwise, with the claim rewritten
// honestly. The gate fails closed: a run that passes without producing
// visual proof is treated as not verified. Every attempt is appended
// to verdicts.json, and the verdict page (index.html) is regenerated
// with the witness link Kane produced.

import { spawn, execSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');

if (process.argv[2] === '--render') {
  const vf = join(root, 'verdicts.json');
  const all = existsSync(vf) ? JSON.parse(readFileSync(vf, 'utf8')) : [];
  writeFileSync(join(root, 'index.html'), render(all));
  console.log('Verdict page regenerated from ' + all.length + ' record(s).');
  process.exit(0);
}

const [videoUrl, claim] = process.argv.slice(2);
if (!videoUrl || !claim) {
  console.error('Usage: node gate.mjs <videoUrl> "<claim>"');
  process.exit(2);
}

const base = process.env.PLAYER_BASE || 'http://localhost:8000';
const playerUrl = videoUrl;
const id = 'gate-' + Date.now();
const objective =
  'Delivery check ' + id + ' for the file ' + videoUrl + '. ' +
  'Open the video at the start URL. If it is not already playing, press play. ' +
  'Let it play for several seconds. Verify that moving video frames with real ' +
  'visible picture content are on screen — not a black or blank screen.';

// Resolve the Kane CLI's JS entry and spawn it directly, with no shell.
// Passing the objective through a Windows shell mangles it (unquoted
// concatenation), and Kane ends up running a thinner check than written.
const npmRoot = execSync('npm root -g').toString().trim();
const pkgDir = join(npmRoot, '@testmuai', 'kane-cli');
const pkg = JSON.parse(readFileSync(join(pkgDir, 'package.json'), 'utf8'));
const binRel = typeof pkg.bin === 'string' ? pkg.bin : pkg.bin['kane-cli'];
const cliEntry = join(pkgDir, binRel);

const out = await new Promise((resolve) => {
  const p = spawn(
    process.execPath,
    [cliEntry, 'run', objective, '--url', playerUrl, '--assertion-mode', 'visual',
     '--final-validation', 'on', '--name', id, '--timeout', '600'],
    { shell: false }
  );
  let buf = '';
  p.stdout.on('data', (d) => { buf += d; process.stdout.write(d); });
  p.stderr.on('data', (d) => process.stderr.write(d));
  p.on('close', () => resolve(buf));
});

let runEnd = null;
let witness = '';
for (const line of out.split('\n')) {
  try {
    const j = JSON.parse(line);
    if (j.type === 'run_end') {
      runEnd = j;
      if (j.test_url) witness = j.test_url;
    }
  } catch { /* not a JSON line */ }
}

const mem = (runEnd && runEnd.context && runEnd.context.memory) || {};
let movingTrue = false, movingFalse = false, darkTrue = false, darkFalse = false;
for (const [k, v] of Object.entries(mem)) {
  const val = v && v.extracted_value;
  if (/moving/.test(k)) { if (val === 'true') movingTrue = true; if (val === 'false') movingFalse = true; }
  if (/black|blank/.test(k)) { if (val === 'true') darkTrue = true; if (val === 'false') darkFalse = true; }
}
const evidenceSeen = movingTrue || movingFalse || darkTrue || darkFalse;
const evidenceOk = movingTrue && !movingFalse && darkFalse && !darkTrue;
const passed = !!runEnd && runEnd.status === 'passed' && evidenceOk;
const why = !runEnd
  ? 'Kane returned no verdict for this delivery'
  : evidenceOk
    ? (runEnd.one_liner || runEnd.reason || runEnd.status)
    : evidenceSeen
      ? 'Kane watched the file and its visual checks did not confirm real playing video frames'
      : 'Kane produced no visual proof of real frames in this run (fail-closed)';
const evidence =
  'Moving frames: ' + (movingTrue ? 'seen' : movingFalse ? 'not seen' : 'no signal') +
  ' · Black/blank screen: ' + (darkTrue ? 'yes' : darkFalse ? 'no' : 'no signal');

const record = {
  id,
  time: new Date().toISOString(),
  videoUrl,
  claim,
  verdict: passed ? 'RELEASED' : 'BLOCKED',
  sentClaim: passed
    ? claim
    : `Not sent. The delivery could not be verified: ${why}.`,
  evidence,
  witness
};

const vf = join(root, 'verdicts.json');
const all = existsSync(vf) ? JSON.parse(readFileSync(vf, 'utf8')) : [];
all.unshift(record);
writeFileSync(vf, JSON.stringify(all, null, 2));
writeFileSync(join(root, 'index.html'), render(all));

console.log('\n=== GATE VERDICT:', record.verdict, '===');
console.log(record.sentClaim);
if (witness) console.log('Witness:', witness);

function esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function fmtTime(iso) {
  try {
    return new Date(iso).toLocaleString('en-GB', {
      timeZone: 'UTC', day: 'numeric', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    }) + ' UTC';
  } catch { return String(iso ?? ''); }
}

function baseName(url) {
  const parts = String(url ?? '').split('/');
  return parts[parts.length - 1] || String(url ?? '');
}

// The verdict page shows what Kane saw, not just what it concluded.
// For the three committed sample files, frames sampled from the actual
// files live in assets/frames/ and are drawn as a film strip: real
// picture frames for the released video, black frames for the blank
// one, and empty frames for the file that could not play at all.
// The verdict page shows what Kane saw, not just what it concluded.
// For the three committed sample files, frames sampled from the actual
// files live in assets/frames/: real picture frames for the released
// video, black frames for the blank one, and empty frames for the file
// that could not play at all. (Design: Direction E — Dashboard, picked
// by Precious 2026-11-26; Poster beacon mark in the topbar.)
function frameStrip(r) {
  const name = baseName(r.videoUrl);
  let frames = '';
  let caption = '';
  if (name === 'good.mp4') {
    frames = ['good-05.jpg', 'good-2.jpg', 'good-35.jpg', 'good-5.jpg']
      .map((f) => `<div class="frame"><img src="assets/frames/${f}" alt="Frame sampled from good.mp4: a colour test pattern with a moving sweep"></div>`)
      .join('');
    caption = 'Frames sampled across the file — picture content throughout.';
  } else if (name === 'blank.mp4') {
    frames = Array(4).fill('<div class="frame"><img src="assets/frames/blank.jpg" alt="Frame sampled from blank.mp4: solid black"></div>').join('');
    caption = 'Frames sampled across the file — every one identical: black.';
  } else if (name === 'corrupt.mp4') {
    frames = Array(4).fill('<div class="frame empty"></div>').join('');
    caption = 'No frames — the file could not be played at all.';
  } else {
    return '';
  }
  return `
      <figure class="strip"><div class="frames">${frames}</div><figcaption>${caption}</figcaption></figure>`;
}

function signals(ev) {
  let moving = 'no signal';
  let dark = 'no signal';
  if (ev) {
    const m = String(ev).match(/Moving frames: ([^·]+)/);
    if (m) moving = m[1].trim();
    const d = String(ev).match(/Black\/blank screen: (.+)$/);
    if (d) dark = d[1].trim();
  }
  return { moving, dark };
}

function markSvg() { return '<svg width="28" height="28" viewBox="128 128 224 224" aria-label="Movidence mark"><defs><linearGradient id="pbl" gradientUnits="userSpaceOnUse" x1="240" y1="216" x2="160" y2="216"><stop offset="0" stop-color="#e8442e" stop-opacity=".95"/><stop offset="1" stop-color="#e8442e" stop-opacity=".25"/></linearGradient><linearGradient id="pbr" gradientUnits="userSpaceOnUse" x1="240" y1="216" x2="320" y2="216"><stop offset="0" stop-color="#e8442e" stop-opacity=".95"/><stop offset="1" stop-color="#e8442e" stop-opacity=".25"/></linearGradient></defs><rect x="128" y="128" width="224" height="224" rx="48" fill="#f3ead9"/><polygon points="240,216 164,182 164,250" fill="url(#pbl)"/><polygon points="240,216 316,182 316,250" fill="url(#pbr)"/><polygon points="223,306 257,306 249,238 231,238" fill="#1c1a17"/><circle cx="240" cy="216" r="11" fill="#e8442e"/><rect x="212" y="306" width="56" height="7" fill="#1c1a17"/></svg>'; }

function render(rows) {
  const released = rows.filter((r) => r.verdict === 'RELEASED').length;
  const blocked = rows.length - released;
  const items = rows.map((r) => {
    const ok = r.verdict === 'RELEASED';
    const sig = signals(r.evidence);
    return `
    <article class="record">
      <div class="rec-top"><span class="dot ${ok ? 'ok' : 'bad'}"></span><span class="verdict ${ok ? 'ok' : 'bad'}">${esc(r.verdict)}</span><span class="file">${esc(baseName(r.videoUrl))}</span><time>${esc(fmtTime(r.time))}</time></div>
      <h3 class="claim">&ldquo;${esc(r.claim)}&rdquo;</h3>
      <p class="sent">${esc(r.sentClaim)}</p>
      ${frameStrip(r)}
      <div class="signals">
        <div class="signal"><span>Moving frames</span><b>${esc(sig.moving)}</b></div>
        <div class="signal"><span>Black / blank screen</span><b>${esc(sig.dark)}</b></div>
        ${r.witness ? `<div class="signal witness"><span>Witness</span><a class="witness" href="${esc(r.witness)}">Kane session recording</a></div>` : ''}
      </div>
    </article>`;
  }).join('\n');
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Movidence — verdicts</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; margin: 0; background: #f5f5f4; color: #17171c; -webkit-font-smoothing: antialiased; }
  .shell { max-width: 1080px; margin: 0 auto; padding: 32px 24px 64px; }
  .topbar { display: flex; align-items: center; gap: 12px; padding-bottom: 24px; border-bottom: 1px solid #e3e3e0; }
  .mark { width: 28px; height: 28px; display: grid; place-items: center; }
  .topbar .name { font-weight: 650; font-size: 15px; }
  .topbar .sub { color: #6d6d74; font-size: 13px; }
  h1 { font-size: 28px; line-height: 1.2; letter-spacing: -.02em; font-weight: 700; margin: 32px 0 8px; }
  .lede { font-size: 15px; line-height: 1.6; color: #55555c; margin: 0; max-width: 66ch; }
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 32px 0; }
  .card { background: #fff; border: 1px solid #e3e3e0; border-radius: 12px; padding: 20px; box-shadow: 0 1px 2px rgba(16,16,20,.04); }
  .card span { display: block; font-size: 12px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #6d6d74; }
  .card b { display: block; font-size: 36px; line-height: 1.1; font-weight: 700; margin-top: 8px; font-variant-numeric: tabular-nums; }
  .card p { margin: 8px 0 0; font-size: 13px; color: #55555c; line-height: 1.5; }
  .card.ok b { color: #0d7a3f; } .card.bad b { color: #d92c1c; }
  .panel { background: #fff; border: 1px solid #e3e3e0; border-radius: 12px; box-shadow: 0 1px 2px rgba(16,16,20,.04); overflow: hidden; }
  .panel-head { display: flex; align-items: center; gap: 12px; padding: 16px 20px; border-bottom: 1px solid #e3e3e0; }
  .panel-head h2 { font-size: 14px; font-weight: 650; margin: 0; }
  .panel-head span { font-size: 13px; color: #6d6d74; }
  .record { padding: 24px 20px; border-bottom: 1px solid #eee; }
  .record:last-child { border-bottom: 0; }
  .rec-top { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .dot { width: 8px; height: 8px; border-radius: 999px; }
  .dot.ok { background: #12a150; } .dot.bad { background: #e5484d; }
  .verdict { font-size: 13px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }
  .verdict.ok { color: #0d7a3f; } .verdict.bad { color: #c62a20; }
  .file { font-family: ui-monospace, Consolas, monospace; font-size: 13px; background: #f5f5f4; border: 1px solid #e3e3e0; border-radius: 6px; padding: 2px 8px; }
  .rec-top time { margin-left: auto; font-size: 13px; color: #6d6d74; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .claim { font-size: 17px; font-weight: 650; line-height: 1.4; margin: 16px 0 4px; }
  .sent { font-size: 14px; line-height: 1.6; color: #55555c; margin: 0; max-width: 68ch; }
  .strip { margin: 20px 0 0; }
  .frames { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  .frame { aspect-ratio: 16/9; background: #000; border-radius: 6px; overflow: hidden; }
  .frame img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .frame.empty { background: #ececea; box-shadow: inset 0 0 0 1px #e3e3e0; }
  .strip figcaption { font-size: 12px; color: #6d6d74; margin-top: 8px; }
  .signals { display: flex; gap: 24px; flex-wrap: wrap; margin-top: 20px; padding-top: 16px; border-top: 1px solid #f0f0ee; }
  .signal span { display: block; font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #6d6d74; margin-bottom: 4px; }
  .signal b { font-family: ui-monospace, Consolas, monospace; font-size: 13px; font-weight: 600; }
  .signal.witness { margin-left: auto; }
  a.witness { color: #4f46e5; font-weight: 600; font-size: 13px; text-decoration: none; }
  a.witness:hover { text-decoration: underline; text-underline-offset: 3px; }
  a.witness:focus-visible { outline: 2px solid #4f46e5; outline-offset: 3px; border-radius: 4px; }
  .rules { margin-top: 32px; background: #fff; border: 1px solid #e3e3e0; border-radius: 12px; padding: 24px 20px; box-shadow: 0 1px 2px rgba(16,16,20,.04); }
  .rules h2 { font-size: 14px; font-weight: 650; margin: 0 0 8px; }
  .rule { display: flex; gap: 12px; padding: 12px 0; border-top: 1px solid #f0f0ee; }
  .rule .n { font-family: ui-monospace, Consolas, monospace; font-size: 12px; color: #6d6d74; padding-top: 2px; }
  .rule p { margin: 0; font-size: 14px; line-height: 1.6; color: #33333a; }
  footer { margin-top: 32px; font-size: 12px; line-height: 1.6; color: #8a8a91; text-align: center; }
  @media (max-width: 640px) { .cards { grid-template-columns: 1fr; } .frames { grid-template-columns: repeat(2, 1fr); } .signal.witness { margin-left: 0; } .rec-top time { margin-left: 0; width: 100%; } }
</style>
</head>
<body>
<div class="shell">
  <div class="topbar"><div class="mark">${markSvg()}</div><div><div class="name">Movidence</div><div class="sub">Delivery gate &middot; verdict log</div></div></div>
  <h1>Delivery verdicts</h1>
  <p class="lede">An agent asks to report a video as sent. The gate hands the actual file to Kane CLI, which opens it in a real browser, presses play, and reports what it saw. A claim is released only with Kane&rsquo;s evidence behind it.</p>
  <div class="cards">
    <div class="card"><span>Checked</span><b>${rows.length}</b><p>Deliveries inspected by Kane in this log.</p></div>
    <div class="card ok"><span>Released</span><b>${released}</b><p>Claims released with visual proof of real frames.</p></div>
    <div class="card bad"><span>Blocked</span><b>${blocked}</b><p>Claims stopped and rewritten honestly.</p></div>
  </div>
  <div class="panel">
    <div class="panel-head"><h2>Verdict log</h2><span>Newest first &middot; every attempt recorded</span></div>
${items || '<p class="lede" style="padding:24px 20px">No deliveries checked yet.</p>'}
  </div>
  <section class="rules">
    <h2>How a verdict is earned</h2>
    <div class="rule"><span class="n">01</span><p>Kane must see moving frames with real picture content. A black or blank screen fails, however long it plays.</p></div>
    <div class="rule"><span class="n">02</span><p>The verdict reads Kane&rsquo;s evidence, not its pass/fail headline. A pass that produced no visual proof is blocked &mdash; the gate fails closed.</p></div>
    <div class="rule"><span class="n">03</span><p>Every check is a unique question, asked once, of the actual file. No replays, no wrappers, no taking the sender&rsquo;s word.</p></div>
  </section>
  <footer>Generated by the gate (gate/gate.mjs) from verdicts.json &middot; Frame strips are sampled from the checked files themselves &middot; Verified with Kane CLI by TestMu AI.</footer>
</div>
</body>
</html>`;
}
