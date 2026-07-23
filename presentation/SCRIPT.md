# Presentation script — DERCO BI Final Project

**Format:** 15 min max + up to 5 min Q&A. **Target: ~12 min** (≈3 min slack).
All four members speak. Deck: `presentation/index.html` (arrow keys / space to advance; press **P** → Save as PDF to export).

**Timing map (target 12:00)**

| Block | Slides | Speaker | Time |
|---|---|---|---|
| Open + framing | 1–4 | **Vicente** | 3:00 |
| Data prep + EDA | 5–8 | **Agustín** | 3:00 |
| Models A & B | 9–11 | **Luis-Felipe** | 3:15 |
| Insights → recommendation → ethics → close | 12–15 | **Baptiste** | 2:45 |

Lead with the business question and the recommendation; keep technical depth honest but proportionate.

---

## ▶ VICENTE — slides 1–4 (≈3:00)

**Slide 1 — Title (15s)**
"Good morning. We're the BI unit DERCO hired. Our job: turn 14 years of car sales — 550,000 of them — into *one* decision the Commercial Director can act on."

**Slide 2 — The ask (45s)**
"DERCO didn't ask for a model. They asked a business question: *after 14 years, where are we leaking value, and what should change to grow margin?* Our decision-maker is the Commercial Director — she owns brand mix, the dealer-vs-own-store channel, and the marketing budget. Success for us isn't a high accuracy score; it's a ranked, euro-valued list of moves she can fund next year."

**Slide 3 — The data (60s)**
"The raw material: 550,000 transactions, 464,000 customers, 9 brands, over 500 comunas, from 2009 to 2022. Every row is one car sale — date, an anonymised customer hash, location, brand, model, channel, list price and margin. Two channels matter: *ces*, the dealer network, and *propio*, DERCO's own stores. One honesty note up front — the money fields are synthetic, obfuscated for the exam. So everything we say about pesos is a *relative signal*: trends and rankings are real, absolute amounts are not."

**Slide 4 — Method (40s)**
"We ran the full BI pipeline: frame, prepare, model, communicate, and ethics — one reproducible notebook, fixed random seed, Python and scikit-learn. I'll hand to Agustín for how we cleaned it and what the data told us."

---

## ▶ AGUSTÍN — slides 5–8 (≈3:00)

**Slide 5 — Prepare & audit (50s)**
"First question of any BI team: can we trust this data? Yes — under 1% missing, zero duplicates, dates fully consistent. Missing comunas we *flagged* as unknown rather than deleting, so we don't quietly shrink revenue. But the audit surfaced something real: **11,966 sales — 2.18% — lose money.** Cars sold below cost. That's roughly 6.8 billion pesos of leaked margin, and it becomes a target for our second model."

**Slide 6 — Brand mix (40s)**
"Looking at *who* sells: Suzuki alone is 39% of volume. That's strength today but concentration risk — if Suzuki stumbles, DERCO feels it. Notice the colours: blue is incumbent brands, red is Chinese brands. Hold that thought."

**Slide 7 — The headline (55s)**
"Because this is the finding that reframes the whole business. Chinese brands went from **12% of sales in 2009 to 52% in 2022.** They now sell the *majority* of DERCO's cars. This isn't a side bet anymore — it's the core business, and any 2026 strategy that still treats it as a hedge is mispriced."

**Slide 8 — Channel, geography, rhythm (35s)**
"Three quick operational facts: the dealer channel does 65% of volume *and* runs a higher margin than own stores; a third of all sales sit in just ten comunas — dense but over-exposed to Santiago; and sales peak in August, bottom out in April. Luis will now turn this description into foresight."

---

## ▶ LUIS-FELIPE — slides 9–11 (≈3:15)

**Slide 9 — Segmentation (55s)**
"Model A answers: *who should DERCO retain?* We describe every customer by three numbers the retail industry lives on — Recency, Frequency, Monetary — then cluster them with KMeans. We didn't pick the number of groups by hand: we tested 2 through 7 with the elbow and silhouette methods and chose four, because four gives both a clean statistical break *and* a marketing playbook. The result: Champions, big-ticket one-timers, mainstream, and dormant."

**Slide 10 — The segmentation insight (60s)**
"Here's what it means. Champions — just 14% of customers — drive 26% of all margin, and they're the *only* group that buys more than once. Meanwhile 86% of customers buy exactly once in 14 years. So DERCO behaves like a *transactional* business, not a *relationship* one. The single cheapest margin to grow is converting one-time buyers into repeat buyers."

**Slide 11 — Loss-deal classifier (60s)**
"Model B is operational: predict which deals lose money *before* they close. Critically, we exclude margin from the inputs — that would be leakage, predicting the answer from the answer. Using only pre-sale features — brand, channel, comuna, price, timing — a gradient-boosting model reaches 0.855 ROC-AUC on the hold-out and a stable 0.83 across 5-fold cross-validation. The decision framing: if the pricing team reviews just the riskiest 10% of deals, they catch *half* of all the money-losers. We're honest that losses are only 2.18% of deals, so this is a triage aid — a human still reviews every flag. Over to Baptiste for what DERCO should do."

---

## ▶ BAPTISTE — slides 12–15 (≈2:45)

**Slide 12 — Insights ranked (45s)**
"Five insights, ranked by impact. One: China won the shelf — 12 to 52%. Two: DERCO is transactional, not relational — 14% of customers make 26% of margin. Three: 6.8 billion pesos leak through loss-making deals, and we can catch half. Four: single-brand dependence on Suzuki. Five: geographic over-exposure to ten comunas."

**Slide 13 — Recommendation (50s)**
"That collapses into one decision with three moves for FY2026. **Retain:** fund a loyalty program aimed at Champions and at converting one-timers — highest-return margin in the business. **Formalise China:** treat Chinese brands as a first-class portfolio in pricing, stock and marketing — they're already the majority. **Plug the leak:** deploy our classifier as a pre-approval check on the riskiest 10% of deals."

**Slide 14 — Ethics & limits (45s)**
"We're deliberate about what this *can't* say. The money is synthetic — direction trustworthy, absolute level not. The customer hash is re-identifiable, so we treat it as personal data and dropped addresses entirely. Our data over-represents Santiago, so 'valuable customer' really means 'urban customer' — a retention program mustn't redline rural comunas. And with an imbalanced target and no causal claims, the models advise; people decide."

**Slide 15 — Close (25s)**
"So: one dataset, one decision — retain Champions, formalise China, plug the margin leak. Thank you. We're happy to take your questions."

---

## Q&A prep — likely panel questions

- **"Why k=4 and not k=2 (higher silhouette)?"** → k=2 only splits recent-vs-old; it isn't *actionable*. k=4 sits at the elbow, keeps a healthy silhouette, and maps to four distinct marketing actions. Defensible on quality *and* business grounds.
- **"Isn't PR-AUC of 0.14 low?"** → Against a 2.18% base rate it's ~6.5× lift, and the *decision metric* is what matters: top-10% review captures ~50% of losses. It's triage, not auto-reject.
- **"How did you avoid leakage?"** → The target is derived from margin, so margin and margin% are excluded from features; only pre-sale-knowable fields are used.
- **"Can you trust the money numbers?"** → No, not the absolute levels — they're synthetic. We only claim shares, ranks and trends.
- **"Why is repeat rate so low — real or a data artifact?"** → Could be a genuinely long purchase cycle *or* an unstable customer key across 14 years. We flag it as needing business confirmation before committing loyalty budget.
- **"Justify one line of code."** → e.g. `stratify=y` in the train/test split keeps the 2.18% loss rate identical in both sets, so the test estimate isn't biased by an unlucky split.
