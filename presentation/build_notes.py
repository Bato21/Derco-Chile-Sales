#!/usr/bin/env python
"""
Distribute presentation/speaker_notes.json to the two places a presenter reads it:

  1. index.html  — inlined into the <script id="speaker-notes"> block, shown by pressing N
  2. SCRIPT.md   — regenerated speaker script, split by member

(build_pptx.py reads the same JSON and writes it into the PowerPoint notes pane.)

    python presentation/build_notes.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = json.loads((HERE / "speaker_notes.json").read_text(encoding="utf-8"))
SLIDES = NOTES["slides"]

# ------------------------------------------------------------------ 1. index.html
html_path = HERE / "index.html"
html = html_path.read_text(encoding="utf-8")

n_sections = html.count('<section class="slide')
if n_sections != len(SLIDES):
    sys.exit(f"slide count mismatch: index.html has {n_sections}, speaker_notes.json has {len(SLIDES)}")

payload = json.dumps(
    [{"n": s["n"], "title": s["title"], "speaker": s["speaker"], "seconds": s["seconds"],
      "point": s["point"], "say": s["say"], "numbers": s["numbers"],
      "watch": s["watch"], "next": s["next"]} for s in SLIDES],
    ensure_ascii=False, separators=(",", ":"))

block = re.compile(
    r'(<script type="application/json" id="speaker-notes">).*?(</script>)', re.S)
if not block.search(html):
    sys.exit("index.html is missing the <script id=\"speaker-notes\"> block")
html = block.sub(lambda m: m.group(1) + payload + m.group(2), html, count=1)
html_path.write_text(html, encoding="utf-8")
print(f"index.html   <- {len(SLIDES)} slides of notes inlined")

# ------------------------------------------------------------------- 2. SCRIPT.md
by_speaker: list[tuple[str, list[dict]]] = []
for s in SLIDES:
    who = s["speaker"].split(" →")[0].strip()
    if not by_speaker or by_speaker[-1][0] != who:
        by_speaker.append((who, []))
    by_speaker[-1][1].append(s)

total = sum(s["seconds"] for s in SLIDES)
out: list[str] = []
w = out.append

w("# Speaker notes — DERCO BI Final Project\n")
w(f"> Generated from `presentation/speaker_notes.json` by `python presentation/build_notes.py`.")
w("> Edit the JSON, not this file — the same source fills the PowerPoint notes pane and the")
w("> **N** overlay in `index.html`.\n")
w(f"**Format:** {NOTES['format']}")
w(f"**Deck:** 13 slides. Scripted runtime **{total // 60}:{total % 60:02d}** — the rest is slack and hand-offs.\n")
w("**Timing map**\n")
w("| Block | Slides | Speaker | Time |")
w("|---|---|---|---|")
for who, group in by_speaker:
    secs = sum(g["seconds"] for g in group)
    rng = f"{group[0]['n']}" if len(group) == 1 else f"{group[0]['n']}–{group[-1]['n']}"
    topic = " · ".join(g["title"].split(" — ")[0] for g in group)
    w(f"| {topic} | {rng} | **{who}** | {secs // 60}:{secs % 60:02d} |")
w("")
w("Lead with the business question and the recommendation; keep technical depth honest but")
w("proportionate. All four members speak and all four stay up for Q&A.\n")
w("---\n")

for who, group in by_speaker:
    secs = sum(g["seconds"] for g in group)
    rng = f"slide {group[0]['n']}" if len(group) == 1 else \
        f"slides {group[0]['n']}–{group[-1]['n']}"
    w(f"## ▶ {who.upper()} — {rng} (≈{secs // 60}:{secs % 60:02d})\n")
    for s in group:
        w(f"### Slide {s['n']} · {s['title']} — {s['seconds']}s")
        if "→" in s["speaker"]:
            w(f"*{s['speaker']}*\n")
        w(f"**The point:** {s['point']}\n")
        w("**Say:**\n")
        for line in s["say"]:
            w(f"> {line}\n")
        if s["numbers"]:
            w("**Numbers to land:** " + " · ".join(f"`{x}`" for x in s["numbers"]) + "\n")
        w(f"**Watch out:** {s['watch']}\n")
        w(f"**Transition:** {s['next']}\n")
    w("---\n")

w("## Timing discipline\n")
w(f"- **Running long?** {NOTES['if_running_long']}")
w(f"- **Running short?** {NOTES['if_running_short']}\n")

w("## Q&A — who takes what\n")
w("| Owner | Fields questions on |")
w("|---|---|")
for who, scope in NOTES["qa_owners"]:
    w(f"| **{who}** | {scope} |")
w("")
w("If a question lands on the wrong person, hand it over out loud (\"Luis-Felipe owns that one\") —")
w("that reads as a team that knows its own work, not as hesitation.\n")

w("### Likely panel questions\n")
for q, a in [
    ("Why k=4? Isn't k=2 higher on silhouette — and isn't k=5 higher than k=4?",
     "Both true, and the slide says so. k=2 scores 0.54 but only splits recent-versus-old — nothing to act on. "
     "k=5 scores 0.400 against k=4's 0.393, a 0.007 gap that is noise, and it splits a group marketing would "
     "treat identically. k=4 sits at the elbow and maps one-to-one onto four real CRM plays. We broke the tie "
     "on actionability and stated it openly."),
    ("Isn't a PR-AUC of 0.14 low?",
     "In absolute terms yes, and we say so. Against a 2.18% base rate it's ~6.5× lift, and the decision metric "
     "is what matters: reviewing the top 10% captures ~50% of losses, 5.1× better than random. Triage, not auto-reject."),
    ("How did you avoid leakage?",
     "The target is derived from margin, so margin and margin% are excluded from the features. Only "
     "pre-sale-knowable fields are used: brand, channel, comuna, list price, timing."),
    ("Can you trust the money numbers?",
     "Not the absolute levels — they're synthetic. We only ever claim shares, ranks and trends."),
    ("Why is the repeat rate so low — real, or a data artifact?",
     "Could be a genuinely long purchase cycle, or a customer key that isn't stable across 14 years. We flag it "
     "as needing business confirmation before loyalty budget is committed. It's in our limitations, not buried."),
    ("Why do your own stores lose so much more per deal?",
     "We can measure the gap — 5.4% of deals below cost versus 0.5% at dealers — but not its cause; this is "
     "correlational. Plausible drivers are discount authority sitting with store managers, or own stores "
     "absorbing trade-ins and fleet deals. That's exactly why we recommend reviewing those deals, not closing "
     "the channel."),
    ("Isn't the Chinese-brand rise just Suzuki declining?",
     "No — the chart is a share of transactions, so it's relative by construction, and absolute Chinese volume "
     "grows too. But we don't claim why it rose; we have the trend, not the cause."),
    ("Justify one line of code.",
     "`stratify=y` in the train/test split keeps the 2.18% loss rate identical in both sets, so the test "
     "estimate isn't biased by an unlucky split. Or `np.log1p` on frequency and monetary before KMeans: both "
     "are heavily right-skewed and KMeans measures Euclidean distance, so without it a handful of fleet buyers "
     "would dominate every cluster."),
    ("Why partial years at both ends?",
     "2009 starts in May and 2022 ends in March. We compare shares at the edges, never totals — that caveat is "
     "on the headline slide and in the notebook."),
]:
    w(f"- **“{q}”**\n  → {a}\n")

(HERE / "SCRIPT.md").write_text("\n".join(out), encoding="utf-8")
print(f"SCRIPT.md    <- regenerated, {len(by_speaker)} speaker blocks, {total // 60}:{total % 60:02d} scripted")
