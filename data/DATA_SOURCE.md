# Data source

## Files in this folder
| File | What it is |
|---|---|
| `ventas_derco_encrypt_exam_TOPD_2009_2022.xlsx` | **Original** source file, as provided by the course. Single sheet `in`; one column packs all 10 fields, pipe-delimited (`\|`). ~550k rows. |
| `derco_sales_clean.parquet` | **Analysis-ready** table produced by the notebook (Stage 2). Typed, cleaned, feature-engineered. This is what the models read. |
| `derco_sales_sample.csv` | A 2,000-row random sample (seed 42) of the clean table, for quick inspection without opening the full file. |

## Origin & license
- **Provider:** IIB415A · Business Intelligence (Prof. Christopher Castro Araya), Universidad del Desarrollo — provided as the exam dataset for the 2026 Final Integrative Project.
- **Subject:** DERCO Chile retail vehicle sales, **May 2009 → March 2022**.
- **Privacy / anonymisation:** the customer identifier `encrypt_rut` is a **hash** (no name, no plaintext RUT). List price (`precio_de_lista_synt`) and margin (`margen_retail`) are **synthetically generated / obfuscated** — treat money as *relative signal*, not audited financials.
- **License / use:** provided for academic use within the course. Not to be redistributed publicly. No personally identifying data is published in any deliverable.

## Reproducing the clean file
The clean Parquet + CSV sample are **regenerated automatically** by running the notebook top-to-bottom:

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/BI2026_FinalProject.ipynb
# writes data/derco_sales_clean.parquet, data/derco_sales_sample.csv, presentation/metrics.json
```

## Schema (raw file)
| Field | Type | Description |
|---|---|---|
| `fecha_transaccion` | date | sale date |
| `encrypt_rut` | hash | anonymised customer key |
| `direccion` | text | customer address (excluded from all models — data minimisation) |
| `comuna` | text | Chilean municipality |
| `marca` | text | vehicle brand |
| `detalle` | text | model + trim |
| `margen_retail` | float | retail margin, CLP (synthetic) |
| `retail` | cat | channel: `ces` (dealer) / `propio` (owned store) |
| `year` | int | transaction year (redundant with date; dropped in cleaning) |
| `precio_de_lista_synt` | float | synthetic list price, CLP |
