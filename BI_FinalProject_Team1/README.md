# DERCO Chile — Business Intelligence Final Project

**Course:** IIB415A · Business Intelligence · Universidad del Desarrollo · 2026
**Team:** Vicente Rodríguez · Agustín Reyes · Luis-Felipe Cáceres · Baptiste Vial
**Client (role-play):** DERCO Chile, Commercial & Strategy leadership

## The problem

DERCO Chile sells vehicles through two channels: a dealer network (`ces`) and its own stores (`propio`). After 14
years of operation it has 550,033 recorded retail sales and no clear read on where that business is losing value.
The question put to us was:

> After 14 years of sales, where is DERCO's retail model leaking value, and what should change to grow margin?

The decision-maker is the Commercial Director, who controls brand mix, the channel split and the marketing budget.
The deliverable is therefore not a model score. It is a ranked set of moves that person can fund, each tied to a
number they can check.

Two sub-questions fall out of that, and each needs a different method:

1. **Who should DERCO keep?** A customer-level question with no labels, so it is answered by segmentation.
2. **Which deals leak margin?** A deal-level question with a labelled outcome, so it is answered by classification.

## The answer

One decision, three funded moves for FY2026:

1. **Retain.** Fund a Champions-retention and one-timer-conversion program. 14.0% of customers produce 25.7% of
   margin and are the only group that buys more than once (2.31 purchases on average); 85.9% of customers buy
   exactly once in 14 years.
2. **Formalise China.** Treat Chinese brands as a first-class portfolio in pricing, stock and marketing. Their share
   moved from 12.2% of sales in 2009 to 51.8% in 2022, so they are already the majority of the business.
3. **Plug the leak.** Run the loss-deal classifier as a pre-approval check on the riskiest 10% of deals, starting
   with the own-store channel. That review contains 50.6% of all loss-making deals.

## What is in this folder

| File | What it is | Original in the repository |
|---|---|---|
| `BI2026_FinalProject.ipynb` | The analysis. Five BI stages end to end, with all outputs saved. | `notebooks/BI2026_FinalProject.ipynb` |
| `derco_sales_clean.parquet` | The analysis-ready dataset the notebook produces: 550,032 rows, 15 columns, 51 MB. | `data/derco_sales_clean.parquet` |
| `BI2026_FinalProject_DERCO.pdf` | The 13-slide presentation of the findings. | `presentation/BI2026_FinalProject_DERCO.pdf` |
| `README.md` | This document. | `README.md` |

Read the notebook first: it carries the full argument, from the business question to the ethics review, with every
chart and printed result exactly as it ran. The PDF is the same argument compressed for a 15-minute presentation.

The raw source workbook is not included. It is course-provided material that is not redistributed, and the clean
table carries every column the analysis uses.

## The data

Provided by the course as the exam file for this project. DERCO Chile retail vehicle sales, 5 May 2009 to
28 March 2022. Full provenance is documented in `data/DATA_SOURCE.md` in the project repository.

- 550,033 rows, one row per car sale
- 464,226 unique customers, 9 brands, 1,543 model-and-trim strings, 511 comunas
- Raw fields: date, hashed customer ID, address, comuna, brand, model, margin, channel, year, list price
- The source is a single Excel sheet whose one column packs all ten fields pipe-delimited, so parsing is the first
  step, not the loading

Three properties constrain every conclusion drawn from it:

**The money is synthetic.** `precio_de_lista_synt` and `margen_retail` were obfuscated before release. Shares,
ranks, trends and relative comparisons hold, because they are ratios of the same transformed field. Absolute peso
amounts do not. Every CLP figure here, including the 6.8 bn leak, is a relative signal and not an audited financial.

**The customer key is pseudonymous, not anonymous.** `encrypt_rut` is a one-way hash of the customer RUT. A RUT is
short and check-digit-validated, so anyone with the same hash function can enumerate candidates and match them back.
It is treated as personal data: used only to group purchases for the segmentation, never a model feature, never
printed at row level.

**The address is dropped.** `direccion` is removed during cleaning as data minimisation. It is not in the clean
table and not in any model. `comuna` is kept because municipality is the geographic unit the decision needs.

## Stage 2 — preparing the data

The audit runs before any modelling, and its result is what makes the later findings credible.

| Check | Result |
|---|---|
| Exact duplicate rows | 0 |
| Rows where the date's year disagrees with the `year` column | 0 |
| Missing values | 0.72%, confined to `direccion` and `comuna` |
| Unparseable list price | 1 row |
| Sales with margin below zero | 11,966 (2.18%) |
| Sales with margin exactly zero | 26 |

Every cleaning decision and its reason:

| Issue | Decision | Why |
|---|---|---|
| `comuna` missing (0.72%) | fill with `UNKNOWN`, keep the row | the row still has a valid brand, price and margin; dropping it would quietly shrink revenue and margin totals |
| 1 row with no list price | drop | no price means no margin and no KPI; it cannot answer any question |
| `year` column | drop, rebuild from the date | 0 mismatches means it is redundant, and two sources of truth is one too many |
| negative margins (2.18%) | keep and flag as `loss_making` | they are the finding, not noise; removing them would delete the result and leave the classifier with no target |
| extreme monetary values | log-transform later, do not delete | a few fleet buyers are real customers |

Engineered columns, each encoding business logic the raw file only implies:

- `brand_origin` — `Chinese` (JAC Cars, Great Wall, Changan, Geely, Haval) or `Incumbent`. The strategic question is
  about origin, not about nine individual brands. The set is explicit in the notebook so it can be challenged.
- `margin_pct` — margin over list price. Absolute margin confounds ticket size with pricing health.
- `loss_making` — 1 when margin is below zero. The classifier target.
- `price_band` — price tercile: `Economy`, `Mid`, `Premium`.
- `year`, `month`, `quarter` — rebuilt from the transaction date for the time views.

The clean table is 550,032 rows by 15 columns. Reading it needs `pandas` and `pyarrow`:

```python
import pandas as pd
df = pd.read_parquet('derco_sales_clean.parquet')     # the copy in this folder
df.shape                                              # (550032, 15)
df.to_csv('derco_sales_clean.csv', index=False)       # if CSV is needed: about 109 MB
```

Parquet is used rather than CSV because it preserves column types and is less than half the size. The
repository also carries `data/derco_sales_sample.csv`, a 2,000-row seeded sample for inspection in a spreadsheet.

## Stage 2 — what the exploration showed

| Finding | Numbers |
|---|---|
| Brand concentration | Suzuki 38.8%, Mazda 17.8%, Renault 10.9%, then six brands under 10% |
| The structural shift | Chinese-brand share 12.2% (2009) to 51.8% (2022); peaked at 31.1% in 2012, fell to 19.5% in 2016, climbed from 2019 |
| Channel | `ces` 357,983 deals at 6.24% margin; `propio` 192,049 deals at 5.20% margin |
| Where the leak sits | `propio` closes 5.38% of deals below cost against 0.46% at `ces`, about 11 times more often |
| Leak by brand | Mazda 4.15% loss rate and -3.42 bn of the -6.84 bn total; Suzuki 1.78% but -1.61 bn on volume |
| Geography | top 10 comunas 33.4% of sales, top 20 49.8%, top 50 74.6%, of 511 comunas |
| Seasonality | August peaks at 10.6% of volume, December 10.3%, April troughs at 6.9% |

The channel gap is the finding that decides where the classifier is deployed first. It is correlational: this
dataset has no field explaining *why* own stores price worse, which is why the recommendation is to review those
deals, not to restructure the channel.

## Stage 3A — segmentation: who should DERCO keep

Each customer is described by three numbers: recency (days since last purchase, measured against the last date in
the file plus one day), frequency (purchases), monetary (total list price). Frequency and monetary are heavily
right-skewed because a few fleet buyers spend orders of magnitude more than the median, so both are `log1p`
transformed and all three axes standardised. KMeans measures Euclidean distance, so an untransformed axis would
dominate the geometry.

`k` was not chosen by hand. k = 2 through 7 were tested with the elbow and the silhouette:

| k | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|
| silhouette | 0.539 | 0.468 | **0.393** | 0.400 | 0.391 | 0.384 |

Silhouette alone does not settle it, so the trade-off is stated rather than hidden. k = 2 scores highest but only
separates recent from old customers, which is one bit of information and no marketing action. k = 5 beats k = 4 by
0.007, which is noise, and splits a group the CRM would treat identically. k = 4 sits at the elbow, holds a usable
silhouette, and maps onto four distinct plays.

| Segment | Customers | Margin | Avg purchases | Play |
|---|---|---|---|---|
| Champions (repeat, high-value) | 14.0% | 25.7% | 2.31 | Retain |
| Big-ticket one-timers | 22.8% | 30.6% | 1.00 | Grow |
| Mainstream one-timers | 32.5% | 24.3% | 1.00 | Nurture |
| Dormant / lapsed | 30.8% | 19.5% | 1.00 | Cap spend |

85.9% of customers buy exactly once across 14 years. DERCO behaves as a transactional business, not a relational
one, and the cheapest margin available is converting one-timers into repeat buyers.

## Stage 3B — classification: which deals leak margin

Target: `loss_making`. Base rate 2.18%.

**The leakage rule is the single most important choice in the model.** The target is derived from `margen_retail`,
so `margen_retail` and `margin_pct` are excluded, along with anything else derived from margin. Feeding them in
would let the model read the answer instead of predicting it, and would be useless in production, where margin is
unknown at quotation time. The features are restricted to what is known before a deal closes: list price, month and
year as numeric; brand, channel and comuna as categorical, with comuna limited to the 30 largest and the tail
bucketed as `OTHER` to control cardinality. Scaling and one-hot encoding happen inside a pipeline, so they are
fitted on the training fold only.

Validation: a stratified 75/25 split (412,524 train, 137,508 test) keeping the 2.18% rate in both, then 5-fold
cross-validation on the full dataset. Two baselines run first, because a score means nothing without one.

| Model | ROC-AUC | PR-AUC | Read |
|---|---|---|---|
| Dummy (stratified) | 0.501 | 0.022 | the floor; equals random |
| Logistic regression, balanced | 0.813 | 0.077 | a linear model already beats random |
| HistGradientBoosting, balanced | **0.855** | **0.142** | chosen; 5-fold CV 0.828, std 0.016, folds 0.808–0.849 |

The quoted headline is the cross-validated 0.83, not the 0.855 hold-out, because the hold-out sits at the top of the
fold range. Accuracy is not reported: at a 2.18% base rate, predicting "never a loss" scores 97.8% and finds
nothing. PR-AUC is the honest measure under that imbalance, and 0.142 against a 0.022 base rate is about 6.5 times
random.

The score becomes a decision through a capacity rule rather than a 0.5 threshold. Deals are ranked by predicted
risk and the pricing team reviews as many as it can handle. At 10%:

- 50.6% of all loss-making deals are inside the queue
- 11.0% of flagged deals truly lose money, which is 5.1 times better than reviewing a random 10%

Permutation importance (drop in ROC-AUC when a feature is shuffled) puts brand, list price and channel first,
consistent with the exploratory findings. Precision of 11% is good for triage and unacceptable for automatic
rejection, so the output is a review queue and a human decides every flag.

## Stage 5 — limits

Stated here, not only in the notebook, because a reader who stops at the README should still see them.

- The money is synthetic. Directions and rankings are trustworthy; absolute pesos are not.
- Nothing here is causal. Chinese-brand growth, the channel gap and the segment margins are all correlational.
- Loss-making deals are 2.18% of the data. The classifier is a triage aid, never an automatic reject.
- The k = 4 silhouette is 0.39. The segments are a usable marketing partition, not four natural populations.
- The top 10 comunas hold a third of the data, so "valuable customer" is partly a proxy for "urban customer". A
  retention budget allocated straight off the segment table would under-serve rural comunas.
- Only closed DERCO sales are visible. Customers who walked away or bought elsewhere are absent, so 85.9% describes
  DERCO's record, not loyalty in the Chilean market.
- A low repeat rate over 14 years cannot distinguish a genuine one-time buyer from an unstable customer key. The
  loyalty conclusion needs CRM confirmation before budget is committed.
- 2009 starts in May and 2022 ends in March. Shares at the two ends are valid; totals are not.
- A deployed classifier would flag `propio` deals more often, so reviewers would confirm the pattern. Flag rate by
  channel and comuna has to be monitored and the model refitted on post-deployment data.

## Reproducing the analysis

The notebook in this folder is the executed record: every output it shows comes from the run that produced
`derco_sales_clean.parquet`. Rerunning it needs the project repository and the course source workbook, which is not
redistributed here.

Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run everything top to bottom
jupyter nbconvert --to notebook --execute --inplace notebooks/BI2026_FinalProject.ipynb

# or work interactively and use Kernel -> Restart & Run All
jupyter notebook notebooks/BI2026_FinalProject.ipynb
```

A full run takes five to ten minutes. `SEED = 42` governs every random step: the KMeans initialisation, the
silhouette sample, the train/test split, the cross-validation folds, the permutation-importance sample and the CSV
sample. A rerun reproduces the same numbers, not numbers that are merely close. This was verified: re-running
regenerates `metrics.json`, `dashboard.png` and the CSV sample byte-identical.

A run writes `data/derco_sales_clean.parquet`, `data/derco_sales_sample.csv`, `presentation/dashboard.png` and
`presentation/metrics.json`. Every figure quoted in the slides comes from that metrics file, so no number is typed
by hand.

Paths are resolved at run time. The notebook walks up from the working directory looking for a `data/` folder or the
source workbook, so it runs unchanged from `notebooks/`, from the repository root, from this folder, or from Colab.
It prints the folders it resolved in the setup cell. To run the copy in this folder, put
`ventas_derco_encrypt_exam_TOPD_2009_2022.xlsx` next to it; the notebook will then read and write here.

## Where these files come from

The project repository is laid out as follows. Paths named anywhere in this document refer to it, not to this folder.

```
.
├── BI_FinalProject_Team1/    the four submitted files (this folder)
├── data/                     source workbook, clean Parquet, CSV sample, DATA_SOURCE.md
├── notebooks/                BI2026_FinalProject.ipynb (deliverable) + early scoping notebook
├── presentation/             deck sources and builds, dashboard.png, metrics.json, Q&A defence pack
├── documents/                course brief and reference material
├── requirements.txt
└── README.md
```

## Team contributions

| Member | Responsibilities |
|---|---|
| Vicente Rodríguez | Business framing and KPIs; repository, reproducibility and environment; `README.md` and `DATA_SOURCE.md` |
| Agustín Reyes | Data preparation, quality audit, feature engineering, exploratory analysis (Stage 2) |
| Luis-Felipe Cáceres | Both models and their validation (Stage 3A and 3B) |
| Baptiste Vial | Insight synthesis, dashboard, ethics and limits (Stages 4 and 5) |

All four members contributed to the analysis and all four present.

## Use of AI tools (course policy §7)

An AI coding assistant (Claude) was used as a pair-programmer: boilerplate such as plot styling and pipeline wiring,
structural suggestions for the RFM and classifier code, and drafts of explanatory prose. The team owns the business
framing, the methodological choices (k = 4, the leakage rule, the 10% review threshold), the interpretation and the
recommendation. Every line was reviewed and can be defended. No number was written by hand; all of them are computed
by the notebook and reappear on a Restart and Run All. Full disclosure in notebook section 6.

## Licence

Academic use within IIB415A. The dataset is course-provided and not for public redistribution. No personally
identifying data is published in any deliverable.
