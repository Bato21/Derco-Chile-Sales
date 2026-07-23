# DERCO Chile — Business Intelligence Final Project

**Course:** IIB415A · Business Intelligence · Universidad del Desarrollo · 2026
**Team:** Vicente Rodríguez · Agustín Reyes · Luis-Felipe Cáceres · Baptiste Vial
**Client (role-play):** DERCO Chile — Commercial & Strategy leadership

> **Business question:** *After 14 years of sales, where is DERCO's retail model leaking value, and what should change to grow margin?*
>
> **Answer (one decision, three moves for FY2026):** **(1) Retain** — fund a Champions-retention + one-timer-conversion loyalty program; **(2) Formalise China** — treat Chinese brands as a first-class portfolio; **(3) Plug the leak** — deploy a classifier as a pre-approval check on the riskiest 10% of deals.

---

## What's in this repo

```
.
├── data/
│   ├── ventas_derco_encrypt_exam_TOPD_2009_2022.xlsx   # original source (~550k rows)
│   ├── derco_sales_clean.parquet                        # analysis-ready (built by the notebook)
│   ├── derco_sales_sample.csv                           # 2,000-row sample for quick inspection
│   └── DATA_SOURCE.md                                   # origin, license, schema, how to reproduce
├── notebooks/
│   ├── BI2026_FinalProject.ipynb                        # ⭐ the deliverable — full 5-stage BI pipeline
│   └── 01_initial_exploration.ipynb                     # early scoping notebook (kept for history)
├── presentation/
│   ├── index.html                                       # animated stakeholder deck (self-contained)
│   ├── SCRIPT.md                                         # speaker script, split across the 4 members
│   └── metrics.json                                     # KPI pack exported by the notebook
├── requirements.txt
└── README.md
```

---

## How to run the notebook (from scratch)

Requires Python 3.10+. From the repo root:

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run everything top-to-bottom (regenerates every figure, the clean dataset, and metrics.json):
jupyter nbconvert --to notebook --execute --inplace notebooks/BI2026_FinalProject.ipynb

# ...or open it interactively and use  Kernel → Restart & Run All
jupyter notebook notebooks/BI2026_FinalProject.ipynb
```

The notebook is **Google-Colab compatible**: upload the `.xlsx`, adjust the `SRC` path in Stage 2, Run All.
It is **seeded** (`SEED = 42`) — every run reproduces the same numbers. Runtime ≈ 2–4 min on a laptop.

## How to view / export the presentation

Open `presentation/index.html` in any modern browser.
- **Navigate:** ↑ / ↓ / space (or Home / End).
- **Export to PDF (the graded deliverable):** press **P** (or Ctrl/Cmd-P) → *Save as PDF* → set layout **Landscape**, margins **None**, enable **Background graphics**. Save as `BI2026_FinalProject_Team.pdf`.

The deck is fully self-contained (no external fonts, scripts, or network calls) and its numbers trace back to notebook cells (`presentation/metrics.json`).

---

## The five BI stages (map to the rubric)

| Stage | Where | Highlights |
|---|---|---|
| **1 · Frame & KPIs** | notebook §1 | business question, named decision-maker, 6 KPIs, success metric |
| **2 · Prepare data** | notebook §2 | quality audit, missing/outlier handling, feature engineering, EDA, clean Parquet |
| **3 · Model & evaluate** | notebook §3 | **A)** RFM + KMeans segmentation (elbow + silhouette, k=4); **B)** loss-deal classifier (leakage-safe, baseline → GBM, train/test + 5-fold CV, ROC/PR-AUC) |
| **4 · Communicate** | notebook §4 + deck | 5 ranked insights, one recommendation, dashboard |
| **5 · Ethics & limits** | notebook §5 | privacy (hash ≠ anonymous), geographic bias, synthetic-money caveat, human-in-the-loop |

## Headline findings
- **Chinese brands 12% → 52%** of sales (2009 → 2022) — now the majority of the business.
- **86% of customers buy once**; **Champions (14%) drive ~26% of margin** → DERCO is transactional, not relational.
- **~6.8 bn CLP (synthetic)** leaks through loss-making deals (2.18%); the classifier catches **~50%** by reviewing the top-10% riskiest.
- Suzuki ≈ 39% of volume (concentration risk); top-10 comunas ≈ 33% of sales (geographic over-exposure).

> **Money caveat:** `precio_de_lista_synt` / `margen_retail` are synthetic. All CLP figures are **relative signals**, not audited financials.

---

## Contribution table

| Member | Responsibilities | Deliverables owned |
|---|---|---|
| **Vicente Rodríguez** | Business framing & KPIs; repo setup, reproducibility, environment | Notebook Stage 1; `requirements.txt`; `README.md`; DATA_SOURCE.md |
| **Agustín Reyes** | Data preparation, quality audit, EDA | Notebook Stage 2 (cleaning + EDA charts); clean dataset pipeline |
| **Luis-Felipe Cáceres** | Modeling & validation | Notebook Stage 3A (segmentation) + 3B (classifier); metrics & validation |
| **Baptiste Vial** | Insight synthesis, dashboard & ethics | Notebook Stage 4–5; `presentation/index.html`; `SCRIPT.md` |

*All four members contributed to the analysis and all four present.*

## AI-use disclosure (course policy §7)

An AI coding assistant (Claude) was used as a **pair-programmer** — scaffolding boilerplate (plot styling, pipeline wiring), suggesting the RFM/KMeans and leakage-safe classifier structure, and drafting explanatory prose. The team owns all business framing, methodological choices (k=4, leakage rule), result interpretation, and the final recommendation; **every line was reviewed and can be defended in Q&A.** No data or numbers were fabricated — all figures are computed by the notebook and reproduce on *Restart & Run All*. Full disclosure is in notebook §6.

## License
Academic use within IIB415A. Dataset provided by the course; not for public redistribution. No personally identifying data is published.
