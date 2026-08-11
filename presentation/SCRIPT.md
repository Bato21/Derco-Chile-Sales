# Speaker notes — DERCO BI Final Project

> Generated from `presentation/speaker_notes.json` by `python presentation/build_notes.py`.
> Edit the JSON, not this file — the same source fills the PowerPoint notes pane and the
> **N** overlay in `index.html`.

**Format:** 15 min max + up to 5 min Q&A. Target 11:30-12:00, leaving slack.
**Deck:** 13 slides. Scripted runtime **11:35** — the rest is slack and hand-offs.

**Timing map**

| Block | Slides | Speaker | Time |
|---|---|---|---|
| Title · The client & the question · The dataset & how we worked | 1–3 | **Baptiste** | 2:30 |
| Prepare & audit · EDA · The headline | 4–6 | **Luis-Felipe** | 2:15 |
| EDA · Model A · Model B | 7–9 | **Agustín** | 3:40 |
| The dashboard · Five findings → one decision · Ethics, bias & limits · Close | 10–13 | **Vicente** | 3:10 |

Lead with the business question and the recommendation; keep technical depth honest but
proportionate. All four members speak and all four stay up for Q&A.

---

## ▶ BAPTISTE — slides 1–3 (≈2:30)

### Slide 1 · Title — 15s
**The point:** Set the frame: we are a BI unit reporting to a client, not students presenting a model.

**Say:**

> Good morning. We're the BI unit DERCO hired.

> Our job: turn 14 years of car sales — 550,000 of them — into ONE decision the Commercial Director can act on.

**Numbers to land:** `550,033 transactions` · `May 2009 → March 2022`

**Watch out:** Don't read the team names off the slide — they can see them. Don't apologise for anything.

**Transition:** "Let's start with what they actually asked us."

### Slide 2 · The client & the question — 45s
**The point:** This is a business question, not a modelling exercise. Name the decision-maker and what success means.

**Say:**

> DERCO didn't ask for a model. They asked a business question: after 14 years, where are we leaking value, and what should change to grow margin?

> Our decision-maker is the Commercial Director — they own brand mix, the dealer-versus-own-store channel, and the marketing budget.

> Success for us isn't a high accuracy score. It's a ranked, peso-valued list of moves they can fund next year.

**Numbers to land:** `14 years of sales`

**Watch out:** Say "pesos" or "CLP" — never euros or dollars. The client is Chilean.

**Transition:** "So what were we given to work with?"

### Slide 3 · The dataset & how we worked — 90s
*Baptiste → hands to Luis-Felipe*

**The point:** Three jobs at once: the scale of the data, the credibility of the method, and the honesty caveat — stated up front, not buried.

**Say:**

> The raw material: 550,000 transactions, 464,000 customers, 9 brands, over 1,500 models, 511 comunas, from 2009 to 2022. Every row is one car sale — date, an anonymised customer hash, location, brand, model, channel, list price and margin.

> Two channels matter: ces, the dealer network at 65%, and propio, DERCO's own stores at 35%. Remember those two names, they come back.

> This strip is how we worked: the full BI pipeline — frame, prepare, model, communicate, ethics — in one reproducible notebook with a fixed seed. Every number you'll see on a slide is exported by that notebook into a metrics file the deck reads, so nothing here is typed by hand.

> One honesty note up front: the money fields are synthetic, obfuscated for the exam. So everything we say about pesos is a relative signal — trends and rankings are real, absolute amounts are not.

**Numbers to land:** `550,033 raw rows → 550,032 after cleaning` · `464,226 customers` · `9 brands · 1,543 models` · `511 comunas` · `ces 65% / propio 35%` · `seed = 42`

**Watch out:** Don't linger on the pipeline strip — it buys credibility, it isn't content. The synthetic-money caveat MUST be said here; if a panellist raises it first, you look like you were hiding it.

**Transition:** "Luis-Felipe will take you through what the data actually said."

---

## ▶ LUIS-FELIPE — slides 4–6 (≈2:15)

### Slide 4 · Prepare & audit — 45s
**The point:** Earn trust with the audit, then reveal that the audit itself found the business problem.

**Say:**

> First question for any BI team: can we trust this data? Yes.

> Less than 1 percent of values are missing. There are no duplicate rows. The dates are all consistent.

> When the comuna was missing, we marked it UNKNOWN. We did not delete the row. Deleting rows would reduce the revenue totals, and that would hide money.

> But the audit found something real. 11,966 sales lose money. That is 2.18 percent of all deals. These cars were sold below cost.

> That is about 6.8 billion pesos of lost margin. It is around 2.7 percent of all retail margin. This becomes the target of our second model.

**Numbers to land:** `0.72% missing comuna` · `0 duplicates` · `0 date mismatches` · `11,966 loss-making sales = 2.18%` · `≈6.8 bn CLP ≈ 2.7% of retail margin`

**Watch out:** Say "sold below cost", not "sold at a loss to the customer". If they ask why we kept the negative margins: they are signal, not noise. If we delete them, we delete the finding. Keep your sentences short and pause at each full stop.

**Transition:** "Before we follow that leak, look at who sells the cars."

### Slide 5 · EDA — brand mix — 35s
**The point:** Concentration risk — and plant the colour code that makes the next slide land.

**Say:**

> Now look at who sells. Suzuki alone is 39 percent of all volume.

> That is a strength today. But it is also a risk. If Suzuki has a bad year, DERCO feels it immediately.

> Look at the colours. Blue is the incumbent brands. Red is the Chinese brands. The length of the bar is volume. The colour is the origin.

> Remember the red. It matters on the next slide.

**Numbers to land:** `Suzuki 38.8%` · `Mazda 17.8%` · `Renault 10.9%` · `JAC Cars 9.1% · Great Wall 8.5% · Changan 8.2%`

**Watch out:** This is the easiest slide to shorten. If you are behind on time, say only the Suzuki line and move on. Do not read all nine brands.

**Transition:** "Now watch what the red does over time."

### Slide 6 · The headline — China won the shelf — 55s
*Luis-Felipe → hands to Agustín*

**The point:** The single finding that reframes the business. Slow down here.

**Say:**

> This is the finding that changes the whole business.

> In 2009, Chinese brands were 12 percent of sales. In 2022, they are 52 percent. They now sell most of DERCO's cars.

> The line is not straight. The share grew to 31 percent in 2012. Then it fell back to about 20 percent in 2015 and 2016. Then it grew again from 2019.

> But the direction is clear. In the last year, Chinese brands crossed the 50 percent line.

> This is not a side bet any more. It is the core business. A 2026 strategy that treats it as a small bet is wrong.

**Numbers to land:** `12.2% in 2009 → 51.8% in 2022` · `dip to 19.5% in 2016` · `crossed 50% in 2022`

**Watch out:** Say the partial-year point yourself, before they ask. 2009 starts in May. 2022 ends in March. So we compare shares, never totals, at the two ends. Saying it first is worth more than answering it later.

**Transition:** "Agustín now turns this description into foresight."

---

## ▶ AGUSTÍN — slides 7–9 (≈3:40)

### Slide 7 · EDA — channel, geography, rhythm — 60s
**The point:** Three operational facts, then the channel gap that tells Model B where to look.

**Say:**

> Three operational facts. The dealer channel does 65% of volume and prices better — 6.2% margin against 5.2% at our own stores. A third of all sales sit in just ten comunas, dense but over-exposed to Santiago. And sales peak in August and bottom out in April, with December a close second peak.

> Then the finding that points our second model: DERCO's own stores close 5.4% of their deals below cost, against 0.5% at dealers. An eleven-fold gap.

> The leak isn't spread evenly across the business — it's concentrated exactly where DERCO controls the pricing.

**Numbers to land:** `ces 6.24% margin vs propio 5.20%` · `top-10 comunas 33.4%` · `Aug peak, Apr trough` · `propio 5.38% loss rate vs ces 0.46% → ~11×`

**Watch out:** This is correlation, not cause. If pushed on why, say so plainly: plausible drivers are discount authority at store level or own stores absorbing trade-ins, but we have no causal evidence — which is exactly why we recommend REVIEWING those deals, not closing the channel.

**Transition:** "Luis-Felipe now turns this description into foresight."

### Slide 8 · Model A — segmentation & what it means — 95s
**The point:** Two parts on one slide: how we built the segments (left), and the result that matters (right). Slow down for the right side.

**Say:**

> Model A answers one question: who should DERCO keep?

> We describe each customer with three numbers. Recency: how long since the last purchase. Frequency: how many purchases. Monetary: how much they spent in total.

> Then we group similar customers together with KMeans. We did not choose the number of groups by hand. We tested k from 2 to 7. We used the elbow method and the silhouette score. We chose four groups.

> Four groups is useful for marketing. The table shows each group: the share of customers, the share of margin, and the action. Retain, grow, nurture, cap spend.

> Now the key result. Champions are only 14 percent of customers. But they produce 26 percent of all margin.

> They are also the only group that comes back. They buy 2.3 times on average. Every other group buys one time.

> And 86 percent of all customers buy only once in 14 years.

> So DERCO is a transactional business, not a relationship business. The cheapest way to grow margin is to make one-time buyers come back.

**Numbers to land:** `Champions 14.0% cust / 25.7% margin / 2.31 buys` · `Big-ticket 22.8% / 30.6%` · `Mainstream 32.5% / 24.3%` · `Dormant 30.8% / 19.5%, last bought ~9 yrs ago` · `85.9% buy exactly once`

**Watch out:** Be ready for the k question: k=2 has the highest silhouette (0.54) but only splits recent-versus-old, which isn't actionable; k=5 scores 0.400 against k=4's 0.393, a gap that is noise. We broke the tie on actionability and say so on the slide. Luis-Felipe built this model — if the question gets deep, hand it to him out loud.

**Transition:** "Model A tells us WHO. Model B tells us WHICH DEALS."

### Slide 9 · Model B — the loss-deal classifier — 65s
*Agustín → hands to Vicente*

**The point:** An operational model. Lead with the leakage decision — that is what separates a BI team from a leaderboard score.

**Say:**

> Model B is operational. It predicts which deals will lose money, before they close.

> One choice is critical. We do not give margin to the model. The target comes from margin. So using margin would be leakage — the model would simply read the answer.

> We use only information known before the sale: brand, channel, comuna, list price, and date.

> We compared three models. A dummy baseline. A logistic regression. And gradient boosting.

> Gradient boosting is the best. ROC-AUC is 0.855 on the test set. Cross-validation gives 0.83, with a standard deviation of 0.016. So the score is stable, not lucky.

> But the business result matters more. The pricing team reviews only the riskiest 10 percent of deals. With that, they find half of all the money-losing deals. This is 5.1 times better than reviewing at random.

**Numbers to land:** `ROC-AUC 0.855 hold-out / 0.828 CV mean, std 0.016` · `PR-AUC 0.142 vs 0.022 base rate` · `top-10% review → 50.6% of losses caught` · `5.1× lift, 11.0% precision in the flagged set`

**Watch out:** Say the honest note before anyone challenges it: losses are only 2.18% of deals, PR-AUC is 0.14, so this is a triage aid and not an auto-reject — a human reviews every flag. Owning the weakness is worth more than hiding it. Luis-Felipe owns the modelling detail in Q&A.

**Transition:** "Vicente will bring all the results together."

---

## ▶ VICENTE — slides 10–13 (≈3:10)

### Slide 10 · The dashboard — 40s
**The point:** The results block closes here. Show that the analysis produced a working artifact, not only slides.

**Say:**

> All our results come together here. Six numbers, one screen. This is what the Commercial Director sees.

> Chinese brands are 52 percent of 2022 sales. 86 percent of customers buy only once. Champions make 26 percent of the margin. 2.18 percent of deals lose money. Suzuki is 39 percent of volume. And we recover half of the leak.

> The dashboard is a self-contained HTML file. The notebook also saves a static image of it. Both read the same metrics file. So the dashboard always matches the analysis. No number is typed by hand.

**Numbers to land:** `51.8% · 85.9% · 25.7% · 2.18% · 38.8% · 50.6%`

**Watch out:** Do not explain the six numbers again — the panel has heard all of them. This slide is about traceability. Point at the screen, name the number, move on.

**Transition:** "Those six numbers collapse into five findings, and the five into one decision."

### Slide 11 · Five findings → one decision — 85s
**The point:** The answer to the brief. This is the slide the grade hangs on — never cut it, never rush it.

**Say:**

> Five findings, ranked by impact. One: China won the shelf — 12 to 52%. Two: DERCO is transactional, not relational — 14% of customers make 26% of margin. Three: 6.8 billion pesos leak through loss-making deals, concentrated in our own stores. Four: single-brand dependence on Suzuki. Five: geographic over-exposure to ten comunas.

> That collapses into one decision with three funded moves for FY2026.

> Retain: fund a loyalty program aimed at Champions and at converting one-timers — the highest-return margin in the business, because those customers already come back.

> Formalise China: treat Chinese brands as a first-class portfolio in pricing, stock and marketing. They're already the majority; the org chart just hasn't caught up.

> Plug the leak: deploy our classifier as a pre-approval check on the riskiest 10% of deals, starting with the own-store channel, because that's where the leak lives.

**Numbers to land:** `12% → 52%` · `86% buy once / 14% drive 26%` · `~6.8 bn CLP at 2.18%` · `Suzuki ≈ 39%` · `top-10 comunas ≈ 33%`

**Watch out:** Go fast on the five findings — the panel has already seen every one of them — and slow on the three moves. Time spent here beats time spent anywhere else in the deck.

**Transition:** "And we're equally clear about what this can't say."

### Slide 12 · Ethics, bias & limits — 45s
**The point:** Credibility comes from naming real limits, not token ones. Each item is specific to THIS analysis.

**Say:**

> We're deliberate about what this can't say. The money is synthetic — direction trustworthy, absolute level not.

> The customer hash is re-identifiable by anyone who can hash a candidate RUT, so we treat it as personal data and we dropped street addresses from every model.

> Our data over-represents Santiago, so 'valuable customer' really means 'urban customer' — a retention program mustn't quietly redline rural comunas.

> Our silhouette is 0.39, so the segments are a useful marketing convenience, not a natural law.

> And with an imbalanced target and no causal claims, the models advise; people decide. We'd re-check all of it yearly.

**Numbers to land:** `silhouette 0.39` · `2.18% class imbalance` · `top-10 comunas 33.4% of data`

**Watch out:** Say these as decisions the team made, not as apologies. If you have a spare 10 seconds, add the survivorship point: we only see closed DERCO sales, never the customers who walked away or bought a competitor.

**Transition:** "To close."

### Slide 13 · Close — 20s
**The point:** Land the decision one last time, then stop talking.

**Say:**

> So: one dataset, one decision — retain Champions, formalise China, plug the margin leak.

> Thank you. We're happy to take your questions.

**Watch out:** Stop. Don't add a summary of the summary. All four of you stay standing and facing the panel for Q&A.

**Transition:** Q&A — route by owner (see the Q&A map in SCRIPT.md).

---

## Timing discipline

- **Running long?** Cut slide 5 (brand mix) to 15s — Suzuki 39% is the only line that matters — and drop the seasonality third of slide 7. Never cut slide 11: it is the answer to the brief.
- **Running short?** Expand slide 8 with the elbow and silhouette reasoning, and slide 12 with the survivorship-bias point (we only see closed DERCO sales, never the customers who walked).

## Q&A — who takes what

| Owner | Fields questions on |
|---|---|
| **Vicente** | business framing, KPIs, why this dataset, reproducibility / packaging |
| **Agustín** | data quality, cleaning decisions, any EDA chart, the channel gap |
| **Luis-Felipe** | both models: choice of k, leakage, metrics, validation, any line of modelling code |
| **Baptiste** | the recommendation, cost/benefit of the three moves, ethics, bias, limitations |

If a question lands on the wrong person, hand it over out loud ("Luis-Felipe owns that one") —
that reads as a team that knows its own work, not as hesitation.

### Likely panel questions

- **“Why k=4? Isn't k=2 higher on silhouette — and isn't k=5 higher than k=4?”**
  → Both true, and the slide says so. k=2 scores 0.54 but only splits recent-versus-old — nothing to act on. k=5 scores 0.400 against k=4's 0.393, a 0.007 gap that is noise, and it splits a group marketing would treat identically. k=4 sits at the elbow and maps one-to-one onto four real CRM plays. We broke the tie on actionability and stated it openly.

- **“Isn't a PR-AUC of 0.14 low?”**
  → In absolute terms yes, and we say so. Against a 2.18% base rate it's ~6.5× lift, and the decision metric is what matters: reviewing the top 10% captures ~50% of losses, 5.1× better than random. Triage, not auto-reject.

- **“How did you avoid leakage?”**
  → The target is derived from margin, so margin and margin% are excluded from the features. Only pre-sale-knowable fields are used: brand, channel, comuna, list price, timing.

- **“Can you trust the money numbers?”**
  → Not the absolute levels — they're synthetic. We only ever claim shares, ranks and trends.

- **“Why is the repeat rate so low — real, or a data artifact?”**
  → Could be a genuinely long purchase cycle, or a customer key that isn't stable across 14 years. We flag it as needing business confirmation before loyalty budget is committed. It's in our limitations, not buried.

- **“Why do your own stores lose so much more per deal?”**
  → We can measure the gap — 5.4% of deals below cost versus 0.5% at dealers — but not its cause; this is correlational. Plausible drivers are discount authority sitting with store managers, or own stores absorbing trade-ins and fleet deals. That's exactly why we recommend reviewing those deals, not closing the channel.

- **“Isn't the Chinese-brand rise just Suzuki declining?”**
  → No — the chart is a share of transactions, so it's relative by construction, and absolute Chinese volume grows too. But we don't claim why it rose; we have the trend, not the cause.

- **“Justify one line of code.”**
  → `stratify=y` in the train/test split keeps the 2.18% loss rate identical in both sets, so the test estimate isn't biased by an unlucky split. Or `np.log1p` on frequency and monetary before KMeans: both are heavily right-skewed and KMeans measures Euclidean distance, so without it a handful of fleet buyers would dominate every cluster.

- **“Why partial years at both ends?”**
  → 2009 starts in May and 2022 ends in March. We compare shares at the edges, never totals — that caveat is on the headline slide and in the notebook.
