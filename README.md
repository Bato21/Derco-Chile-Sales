# DERCO Chile — Business Intelligence Final Project

**Course:** IIB415A · Business Intelligence · Universidad del Desarrollo · 2026
**Team:** Vicente Rodríguez · Agustín Reyes · Luis-Felipe Cáceres · Baptiste Vial
**Client (role-play):** DERCO Chile — Commercial & Strategy leadership

> **Business question:** *After 14 years of sales, where is DERCO's retail model leaking value, and what should change to grow margin?*
>
> **Answer (one decision, three moves for FY2026):** **(1) Retain** — fund a Champions-retention + one-timer-conversion loyalty program; **(2) Formalise China** — treat Chinese brands as a first-class portfolio; **(3) Plug the leak** — deploy a classifier as a pre-approval check on the riskiest 10% of deals, starting with the own-store channel.

---

## What's in this repo

```
.
├── data/
│   ├── ventas_derco_encrypt_exam_TOPD_2009_2022.xlsx   # original source (550,033 rows)
│   ├── derco_sales_clean.parquet                       # analysis-ready (built by the notebook)
│   ├── derco_sales_sample.csv                          # 2,000-row sample for quick inspection
│   └── DATA_SOURCE.md                                  # origin, license, schema, how to reproduce
├── notebooks/
│   ├── BI2026_FinalProject.ipynb                       # ⭐ the deliverable — full 5-stage BI pipeline
│   └── 01_initial_exploration.ipynb                    # early scoping notebook (kept for history)
├── presentation/
│   ├── index.html                                      # animated stakeholder deck (self-contained)
│   ├── BI2026_FinalProject_DERCO.pptx                  # the same deck as PowerPoint
│   ├── build_pptx.py                                   # regenerates the .pptx from metrics.json
│   ├── dashboard.png                                   # static dashboard, written by the notebook
│   ├── speaker_notes.json                              # ⭐ single source for all speaker notes
│   ├── build_notes.py                                  # notes -> index.html (N key) + SCRIPT.md
│   ├── SCRIPT.md                                       # generated speaker script, split across the 4 members
│   └── metrics.json                                    # KPI pack exported by the notebook
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
It is **seeded** (`SEED = 42`) — every run reproduces the same numbers. Runtime ≈ 5–10 min on a laptop.

Running it writes four artifacts: `data/derco_sales_clean.parquet`, `data/derco_sales_sample.csv`,
`presentation/metrics.json` and `presentation/dashboard.png`.

## The presentation — two formats, one source of truth

| File | What it is |
|---|---|
| `presentation/index.html` | The deck we present — **13 slides**. Self-contained (no fonts, scripts or network calls), keyboard-driven, animated. |
| `presentation/BI2026_FinalProject_DERCO.pptx` | The same 13 slides as PowerPoint (16:9), for rooms that need it. Native PowerPoint charts, editable. |

**Both are generated from `presentation/metrics.json`**, which the notebook writes in Stage 4 — so a number
can never differ between the notebook, the HTML deck and the PowerPoint.

- **View the HTML deck:** open `presentation/index.html` in any modern browser. Navigate with ↑ / ↓ / space
  (or Home / End). Press **N** for the speaker-notes drawer — it follows the current slide and never prints.
- **Export the PDF (the graded deliverable):** press **P** in the deck (or Ctrl/Cmd-P) → *Save as PDF* →
  layout **Landscape**, margins **None**, **Background graphics ON**. The page is pre-sized to 297 × 167 mm
  (16:9), one slide per page. Save as `BI2026_FinalProject_Team.pdf`.
- **Rebuild the PowerPoint** after re-running the notebook:
  ```bash
  pip install python-pptx
  python presentation/build_pptx.py      # slides + speaker notes in the notes pane
  ```

### Speaker notes — one source, three places
Edit **`presentation/speaker_notes.json`** only. It carries, per slide: the speaker, the target seconds, the
point of the slide, what to say, the numbers to land, what to watch out for, and the transition line. Then:

```bash
python presentation/build_notes.py     # -> index.html (press N) + SCRIPT.md
python presentation/build_pptx.py      # -> the PowerPoint notes pane (presenter view)
```

Scripted runtime is **11:35** across 13 slides, split Vicente (1–3) · Agustín (4–7) · Luis-Felipe (8–10) ·
Baptiste (11–13), leaving slack inside the 15-minute limit. `SCRIPT.md` is **generated** — don't hand-edit it.

### Visual identity
DERCO's own colours: **deep red `#c00512` on white** (6.4:1 contrast — AA-clean at any text size). Every chart colour is checked for ≥3:1 contrast on the white
surface and for colour-vision-deficiency separation, so no finding depends on distinguishing two similar hues.
The four ranked customer segments use a single ordered red ramp (dark = most valuable) rather than four
unrelated colours, because the segments *are* ordered.

---

## The five BI stages (map to the rubric)

| Stage | Where | Highlights |
|---|---|---|
| **1 · Frame & KPIs** | notebook §1 | business question, named decision-maker, 6 KPIs, success metric |
| **2 · Prepare data** | notebook §2 | quality audit, missing/outlier handling, feature engineering, EDA, clean Parquet |
| **3 · Model & evaluate** | notebook §3 | **A)** RFM + KMeans segmentation (elbow + silhouette, k=4); **B)** loss-deal classifier (leakage-safe, baseline → GBM, train/test + 5-fold CV, ROC/PR-AUC) |
| **4 · Communicate** | notebook §4 + deck | 5 ranked insights, one recommendation, dashboard (`dashboard.png` + `index.html`) |
| **5 · Ethics & limits** | notebook §5 | privacy (hash ≠ anonymous), geographic bias, synthetic-money caveat, human-in-the-loop |

## Headline findings
- **Chinese brands 12% → 52%** of sales (2009 → 2022) — now the majority of the business.
- **86% of customers buy once**; **Champions (14%) drive ~26% of margin** → DERCO is transactional, not relational.
- **~6.8 bn CLP (synthetic)** leaks through loss-making deals (2.18%, ≈2.7% of all retail margin); the classifier
  catches **~50%** by reviewing the top-10% riskiest — 5.1× better than random.
- The leak is **concentrated in DERCO's own stores**: 5.4% of `propio` deals close below cost vs 0.5% at dealers.
- Suzuki ≈ 39% of volume (concentration risk); top-10 comunas ≈ 33% of sales (geographic over-exposure).

> **Money caveat:** `precio_de_lista_synt` / `margen_retail` are synthetic. All CLP figures are **relative signals**, not audited financials.

---

## Contribution table

| Member | Responsibilities | Deliverables owned |
|---|---|---|
| **Vicente Rodríguez** | Business framing & KPIs; repo setup, reproducibility, environment | Notebook Stage 1; `requirements.txt`; `README.md`; `DATA_SOURCE.md` |
| **Agustín Reyes** | Data preparation, quality audit, EDA | Notebook Stage 2 (cleaning + EDA charts); clean dataset pipeline |
| **Luis-Felipe Cáceres** | Modeling & validation | Notebook Stage 3A (segmentation) + 3B (classifier); metrics & validation |
| **Baptiste Vial** | Insight synthesis, dashboard & ethics | Notebook Stage 4–5; `presentation/index.html`; `build_pptx.py`; `SCRIPT.md` |

*All four members contributed to the analysis and all four present.*

## AI-use disclosure (course policy §7)

An AI coding assistant (Claude) was used as a **pair-programmer** — scaffolding boilerplate (plot styling, pipeline wiring), suggesting the RFM/KMeans and leakage-safe classifier structure, and drafting explanatory prose. The team owns all business framing, methodological choices (k=4, leakage rule), result interpretation, and the final recommendation; **every line was reviewed and can be defended in Q&A.** No data or numbers were fabricated — all figures are computed by the notebook and reproduce on *Restart & Run All*. Full disclosure is in notebook §6.

## License
Academic use within IIB415A. Dataset provided by the course; not for public redistribution. No personally identifying data is published.
