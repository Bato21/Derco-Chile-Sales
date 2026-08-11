# DERCO Chile — Business Intelligence Final Project

**Course:** IIB415A · Business Intelligence · Universidad del Desarrollo · 2026
**Team:** Vicente Rodríguez · Agustín Reyes · Luis-Felipe Cáceres · Baptiste Vial
**Client (role-play):** DERCO Chile, Commercial & Strategy leadership

This folder is the graded submission for a complete BI project built on 14 years of DERCO Chile retail
vehicle sales (550,033 transactions, May 2009 to March 2022). It holds four files: the notebook that runs the
whole pipeline with its outputs saved, the analysis-ready dataset that notebook produces, the presentation as a
PDF, and this documentation. Everything needed to judge the work is here; the rest of the project repository is
described further down for anyone who wants to rerun it.

## The question and the answer

The brief was not "build a model". It was a business question:

> After 14 years of sales, where is DERCO's retail model leaking value, and what should change to grow margin?

The answer is one decision with three funded moves for FY2026:

1. **Retain.** Fund a Champions-retention and one-timer-conversion program. 14% of customers produce 26% of
   margin and are the only group that buys more than once; 86% of customers buy exactly once in 14 years.
2. **Formalise China.** Treat Chinese brands as a first-class portfolio in pricing, stock and marketing.
   They moved from 12% of sales in 2009 to 52% in 2022, so they are already the majority of the business.
3. **Plug the leak.** Deploy the loss-deal classifier as a pre-approval check on the riskiest 10% of deals,
   starting with the own-store channel. That review catches roughly half of all loss-making deals.

Each of those claims is computed in the notebook, exported to `presentation/metrics.json`, and read from that
file by the deck, so a figure cannot drift between the analysis and the slides.

## What is in this folder

| File | What it is | Original in the repository |
|---|---|---|
| `BI2026_FinalProject.ipynb` | The final notebook, with all outputs saved. Stages 1 to 5 plus the AI-use disclosure. | `notebooks/BI2026_FinalProject.ipynb` |
| `derco_sales_clean.parquet` | The full analysis-ready dataset, 550,032 rows by 15 columns, 51 MB on disk. | `data/derco_sales_clean.parquet` |
| `BI2026_FinalProject_DERCO.pdf` | The presentation, 13 pages at 297 × 167 mm (16:9). | `presentation/BI2026_FinalProject_DERCO.pdf` |
| `README.md` | This documentation. | `README.md` |

These four files are copies taken from the repository. Nothing syncs automatically: if an original changes,
it has to be copied across again.

Two things are deliberately absent. The raw source workbook is course-provided material that is not to be
redistributed, and the clean Parquet already carries every column the analysis uses. The HTML and PowerPoint
versions of the deck are not here either, because the PDF is the graded format; both live in the repository
under `presentation/`.

Read the notebook first. It contains the full argument, from the business question to the ethics review, with
every chart and printed result exactly as it ran. The PDF is the same argument compressed into 13 slides for a
15-minute presentation.

## Where these files come from

The project repository is laid out as follows. Paths mentioned anywhere below refer to it, not to this
submission folder.

```
.
├── BI_FinalProject_Team1/                              submission bundle (copies of the four deliverables)
├── data/
│   ├── ventas_derco_encrypt_exam_TOPD_2009_2022.xlsx   original source, 550,033 rows
│   ├── derco_sales_clean.parquet                       analysis-ready table, written by the notebook
│   ├── derco_sales_sample.csv                          2,000-row random sample for quick inspection
│   └── DATA_SOURCE.md                                  origin, licence, raw schema, how to regenerate
├── notebooks/
│   ├── BI2026_FinalProject.ipynb                       the deliverable notebook, five BI stages
│   └── 01_initial_exploration.ipynb                    early scoping work, kept for history
├── presentation/
│   ├── index.html                                      the deck we present, self-contained, animated
│   ├── BI2026_FinalProject_DERCO.pdf                   printed deck, the graded format
│   ├── BI2026_FinalProject_DERCO.pptx                  the same 13 slides as PowerPoint
│   ├── dashboard.png                                   static dashboard, written by the notebook
│   ├── metrics.json                                    KPI pack exported by the notebook
│   ├── speaker_notes.json                              single source for every speaker note
│   ├── build_notes.py                                  speaker_notes.json -> index.html + SCRIPT.md
│   ├── build_pptx.py                                   metrics.json + notes -> the .pptx
│   └── SCRIPT.md                                       generated speaking script, split by member
├── documents/                                          the course brief and reference screenshots
├── requirements.txt
└── README.md
```

## The data

### Origin and handling

The dataset was provided by the course as the exam file for the 2026 Final Integrative Project. It covers
DERCO Chile retail vehicle sales from 5 May 2009 to 28 March 2022. Full provenance is in `data/DATA_SOURCE.md`.

Two properties shape everything downstream:

- **The customer key is a hash, not an anonymisation.** `encrypt_rut` is a one-way hash of the customer RUT.
  A RUT is short and check-digit-validated, so anyone with the same hash function can enumerate candidates and
  match them back. We treat the column as personal data: it is used only to group purchases for the RFM table,
  it is never a model feature, and it never appears at row level in any deliverable.
- **The money is synthetic.** `precio_de_lista_synt` and `margen_retail` were obfuscated before the file was
  released. Shares, ranks, trends and relative comparisons hold. Absolute peso amounts do not. Every CLP figure
  in this project, including the 6.8 bn leak, is a relative signal and not an audited financial.

The raw file also carries `direccion`, a free-text street address. It is dropped during cleaning as data
minimisation: it is not in the clean Parquet, not in the sample CSV, and not in any model. `comuna` is kept
because municipality is the geographic unit the business decision actually needs.

### Schema of the clean table

`derco_sales_clean.parquet` has 550,032 rows and 15 columns. Exactly one raw row is dropped, the one whose
list price cannot be parsed into a number; nothing else is deleted. The raw `year` column is also dropped
because it duplicates the transaction date, and is rebuilt from the date itself.

| Column | Type | Meaning |
|---|---|---|
| `fecha_transaccion` | datetime | sale date |
| `encrypt_rut` | string | hashed customer key, one person to one hash |
| `comuna` | string | Chilean municipality, `UNKNOWN` where the source was blank |
| `marca` | string | vehicle brand, 9 distinct |
| `detalle` | string | model and trim, 1,543 distinct |
| `brand_origin` | string | engineered: `Chinese` or `Incumbent`, the axis of the headline finding |
| `retail` | string | channel: `ces` (dealer network) or `propio` (DERCO-owned store) |
| `precio_de_lista_synt` | float | synthetic list price, CLP |
| `margen_retail` | float | retail margin per sale, CLP, synthetic |
| `margin_pct` | float | engineered: margin as a percentage of list price |
| `loss_making` | int | engineered: 1 when margin is below zero, the target of Model B |
| `price_band` | category | engineered: price tercile, `Economy` / `Mid` / `Premium` |
| `year`, `month`, `quarter` | int | engineered calendar parts for the time views |

### Reading the file

Parquet keeps the column types, which CSV does not, and at 51 MB it is less than half the size of the same
table as CSV (109 MB). Reading it needs `pandas` plus `pyarrow`, both in `requirements.txt`:

```python
import pandas as pd
df = pd.read_parquet('derco_sales_clean.parquet')     # BI_FinalProject_Team1/ or data/
df.shape                                              # (550032, 15)
```

If you need a CSV, write one from the same file rather than asking for a second copy of the data:

```python
df.to_csv('derco_sales_clean.csv', index=False)       # about 109 MB
```

`data/derco_sales_sample.csv` is a 2,000-row random sample (seed 42) for opening in a spreadsheet without
loading half a million rows.

## Reproducing the analysis

The notebook in this folder is the executed record: every output it shows was produced by the run that
generated `derco_sales_clean.parquet`. To rerun it you need the project repository and the course source
workbook, because the raw `.xlsx` is not redistributed here.

Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run everything top to bottom
jupyter nbconvert --to notebook --execute --inplace notebooks/BI2026_FinalProject.ipynb

# or work interactively and use Kernel -> Restart & Run All
jupyter notebook notebooks/BI2026_FinalProject.ipynb
```

A full run takes about five to ten minutes on a laptop. `SEED = 42` governs every random step (the KMeans
initialisation, the train/test split, the cross-validation folds and the CSV sample), so a rerun reproduces the
same numbers rather than numbers that are merely close.

A run rewrites four artifacts, which is why the deck never needs hand-editing:

- `data/derco_sales_clean.parquet` and `data/derco_sales_sample.csv`
- `presentation/dashboard.png`
- `presentation/metrics.json`, which the HTML deck and the PowerPoint builder both read

Paths are resolved at run time rather than hard-coded. The notebook walks up from the working directory looking
for a `data/` folder or the source workbook, so it runs unchanged from `notebooks/`, from the repository root,
from this submission folder, or from Google Colab. It prints the two folders it settled on in the setup cell,
so a wrong guess is visible immediately rather than three cells later. To run the copy in this folder, drop
`ventas_derco_encrypt_exam_TOPD_2009_2022.xlsx` next to it; the notebook will then read from here and write its
outputs here as well.

## What the notebook does

The five stages map onto the course rubric. Each opens with the reasoning before the code, so the notebook can
be read by someone who does not write Python.

**Stage 1, frame and KPIs.** States the business question, names the decision-maker (the Commercial Director,
who owns brand mix, the channel split and the marketing budget), lists the six KPIs the analysis is measured
against, and defines what success means for the project itself: a ranked, peso-valued list of moves, not a high
accuracy score.

**Stage 2, prepare the data.** The source workbook has a single sheet whose one column packs all ten fields
pipe-delimited, so the first job is to split and type it, converting with `errors='coerce'` so bad values
surface as nulls instead of being silently guessed. Then a five-part quality audit: shape, missing values,
duplicates, logical consistency, outliers. The results are good (0.72% missing comuna, no duplicate rows, no
date-versus-year contradictions), which is what makes the one genuine finding credible: 11,966 sales, 2.18% of
the file, closed below cost.

Two cleaning decisions are worth defending in questions. Missing comunas become `UNKNOWN` rather than dropped
rows, because dropping them would quietly reduce every revenue total and hide money. Negative margins are kept
rather than treated as outliers, because they are the signal that Model B is built to predict; removing them
would remove the finding. Feature engineering then adds `brand_origin`, `margin_pct`, `loss_making`,
`price_band` and the calendar parts, and the exploratory analysis covers brand mix, channel, the 14-year trend,
seasonality, the Chinese-versus-incumbent shift, geography and margin health.

**Stage 3, model and evaluate.** Two models, chosen because the business question has two halves.

Model A answers "who should DERCO keep". It builds an RFM table (recency, frequency, monetary value per
customer), log-scales it because monetary value is heavily skewed, and clusters with KMeans. `k` is chosen with
the elbow method and the silhouette score across k = 2 to 7 rather than by hand. k = 2 scores highest on
silhouette (0.54) but only separates recent from old customers, which no one can act on; k = 5 scores 0.400
against 0.393 for k = 4, a gap inside the noise. k = 4 is chosen because it sits at the elbow, holds a
reasonable silhouette, and produces four groups that map onto four different marketing plays. The notebook says
this out loud instead of presenting k = 4 as if it were obvious.

Model B answers "which deals will lose money". The most important choice in it is what the model is not
allowed to see: the target is derived from `margen_retail`, so margin and every margin-derived column are
excluded. Leaving them in would be leakage, and the model would score beautifully by reading the answer. The
features are restricted to what is known before a sale closes: brand, channel, comuna, list price and timing.
A dummy classifier and a logistic regression set the floor, then `HistGradientBoostingClassifier` is fitted on
a stratified hold-out and validated with 5-fold cross-validation. The reported number is the business one: at a
review capacity of the riskiest 10% of deals, the queue contains half of all loss-making deals.

**Stage 4, communicate.** Five insights ranked by decision impact, one recommendation with three moves, and a
six-tile dashboard rendered both as `dashboard.png` and as the live HTML deck. The stage ends by writing
`metrics.json`, which is the contract between the analysis and everything presented.

**Stage 5, ethics, privacy and bias.** Privacy (the hash is pseudonymous, address dropped, aggregates only),
bias (geographic skew toward Santiago, survivorship, the feedback loop a deployed Model B would create, the
moderate silhouette), and honest limitations. Written as decisions the team took, with the mitigation named
next to each risk.

## Headline results

Every figure below is produced by the notebook and exported to `presentation/metrics.json`.

| Finding | Numbers | Where |
|---|---|---|
| Chinese brands became the majority of sales | 12.2% in 2009 to 51.8% in 2022, with a dip to 19.5% in 2016 | Stage 2.7(e) |
| The business is transactional, not relational | 85.9% of customers buy exactly once; Champions are 14.0% of customers and 25.7% of margin, averaging 2.31 purchases | Stage 3A |
| Margin leaks through loss-making deals | 11,966 deals, 2.18% of the file, about 6.8 bn CLP, roughly 2.7% of all retail margin | Stage 2.4 |
| The leak is concentrated in own stores | 5.38% of `propio` deals close below cost against 0.46% at dealers, an 11-fold gap | Stage 2.7(g) |
| The classifier is usable as a triage aid | ROC-AUC 0.855 on the hold-out, 0.828 ± 0.016 across 5 folds, PR-AUC 0.142 against a 0.022 base rate | Stage 3B |
| Reviewing the riskiest 10% pays | catches 50.6% of loss-making deals, 5.1 times better than random, 11.0% precision inside the flagged set | Stage 3B.5 |
| Brand concentration | Suzuki is 38.8% of volume | Stage 2.7(a) |
| Geographic concentration | the top 10 comunas hold 33.4% of sales | Stage 2.7(f) |

## The presentation

`BI2026_FinalProject_DERCO.pdf` in this folder is the graded format. It is one of three builds of the same
deck, all fed by the same numbers; the other two live in the repository.

| File | Use |
|---|---|
| `presentation/index.html` | What we present. 13 slides, self-contained: no external fonts, scripts or network calls. Keyboard driven and animated. |
| `presentation/BI2026_FinalProject_DERCO.pdf` | The graded format. 13 pages at 297 × 167 mm, one slide per page, backgrounds included. |
| `presentation/BI2026_FinalProject_DERCO.pptx` | For rooms that require PowerPoint. Native editable charts, notes in the presenter pane. |

Navigate the HTML deck with the arrow keys or space, Home and End to jump. Press `N` for the speaker-notes
drawer, which follows the current slide and never prints. Press `P` to open the print dialog with the notes
closed and every animation resolved.

### Regenerating the PDF

The print stylesheet fixes the page geometry (`@page { size: 297mm 167mm; margin: 0 }`), forces one slide per
page, resolves the reveal animations, and sets `print-color-adjust: exact` so the red backgrounds and chart
fills survive even when the print dialog has background graphics switched off. Headless Chrome therefore
reproduces the file without any manual settings:

```bash
chrome --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=6000 \
  --print-to-pdf="<absolute path>/BI2026_FinalProject_DERCO.pdf" \
  "<absolute path>/presentation/index.html"
```

Both paths must be absolute; Chrome refuses relative output paths. On Windows the binary is
`"C:\Program Files\Google\Chrome\Application\chrome.exe"`.

By hand: open `index.html`, press `P`, choose Save as PDF, landscape, margins None, background graphics on.
Verify the result is 13 pages before submitting.

### Regenerating the PowerPoint

```bash
pip install python-pptx
python presentation/build_pptx.py
```

### Speaker notes

Edit `presentation/speaker_notes.json` and nothing else. It holds, per slide, the speaker, the target duration,
the point of the slide, what to say, the numbers to land, what to watch out for, and the transition line. Then
regenerate the three places those notes appear:

```bash
python presentation/build_notes.py     # writes the drawer in index.html and SCRIPT.md
python presentation/build_pptx.py      # writes the PowerPoint notes pane
```

`SCRIPT.md` is generated. Do not hand-edit it, the next build will overwrite it.

The scripted runtime is 11 minutes 35 seconds across 13 slides, split Baptiste (1 to 3), Luis-Felipe (4 to 6),
Agustín (7 to 9), Vicente (10 to 13), which leaves slack inside the 15-minute limit. Each slide footer names
its speaker and the same name appears in the notes, so the three formats can be checked against each other.

Presenting order and Q&A ownership differ on purpose. You present the slide in front of you, but whoever built
that part answers the deep question, so hand over out loud. The routing is in `SCRIPT.md` and follows the
contribution table below.

### Visual identity

DERCO's own colours: deep red `#c00512` on white, which is 6.4:1 against white and passes AA at any text size.
Every chart colour is checked for at least 3:1 contrast on the white surface and for separation under
colour-vision deficiency, so no finding depends on telling two similar hues apart. The four customer segments
use a single ordered red ramp, dark for the most valuable, rather than four unrelated colours, because the
segments are ranked and the colour should say so.

## What this analysis cannot say

Stated here as well as in the deck and notebook §5, because a reader who only opens the README should still see
the limits.

- The money is synthetic. Directions and rankings are trustworthy, absolute pesos are not.
- Loss-making deals are 2.18% of the data. PR-AUC of 0.142 is modest in absolute terms even though it is about
  6.5 times the base rate, so Model B produces a review queue, never an automatic rejection.
- The k = 4 silhouette is 0.39. The segments are a usable marketing partition, not four naturally separated
  populations.
- The top 10 comunas hold a third of the data, so "valuable customer" is partly a proxy for "urban customer".
  A retention budget allocated straight off the segment table would under-serve rural comunas.
- Only closed DERCO sales are visible. Customers who walked away or bought elsewhere are absent, so the 86%
  one-time figure describes DERCO's record and not loyalty in the Chilean market.
- Nothing here is causal. 2009 starts in May and 2022 ends in March, so the end years are partial and their
  totals must never be compared with full years; shares are safe, totals are not.

## Team contributions

| Member | Responsibilities | Deliverables owned |
|---|---|---|
| Vicente Rodríguez | Business framing and KPIs, repository setup, reproducibility, environment | Notebook Stage 1, `requirements.txt`, `README.md`, `DATA_SOURCE.md` |
| Agustín Reyes | Data preparation, quality audit, exploratory analysis | Notebook Stage 2, cleaning pipeline and EDA charts |
| Luis-Felipe Cáceres | Modelling and validation | Notebook Stage 3A and 3B, metrics and validation |
| Baptiste Vial | Insight synthesis, dashboard, ethics | Notebook Stages 4 and 5, `presentation/index.html`, `build_pptx.py`, `SCRIPT.md` |

All four members contributed to the analysis and all four present.

## Use of AI tools (course policy §7)

An AI coding assistant (Claude) was used as a pair-programmer: scaffolding boilerplate such as plot styling and
pipeline wiring, suggesting the RFM and KMeans structure and the leakage-safe classifier design, and drafting
explanatory prose. The team owns the business framing, the methodological choices (k = 4, the leakage rule, the
10% review threshold), the interpretation of the results and the final recommendation. Every line was reviewed
and can be defended in questions. No data or numbers were invented; every figure is computed by the notebook
and reappears on a Restart and Run All. The full disclosure is in notebook §6.

## Licence

Academic use within IIB415A. The dataset is course-provided and is not for public redistribution. No
personally identifying data is published in any deliverable.
