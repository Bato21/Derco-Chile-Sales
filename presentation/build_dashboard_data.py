"""Export the aggregate cubes the BI dashboard reads.

The dashboard (presentation/dashboard.html) is a self-contained file: it embeds the
JSON written here so it opens with a double-click, no server and no network. Nothing
is typed by hand — every figure on screen is an aggregate of the cleaned parquet, so
the dashboard cannot drift away from the notebook.

Cubes are emitted as column-oriented arrays (one list per field) rather than a list of
row objects: same information, roughly a third of the bytes, and the browser rebuilds
the rows once at load.

    python presentation/build_dashboard_data.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PARQUET = ROOT / "data" / "derco_sales_clean.parquet"
METRICS = ROOT / "presentation" / "metrics.json"
OUT = ROOT / "presentation" / "dashboard_data.json"

TOP_COMUNAS = 60
TOP_MODELS = 60


def cube(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Group to `keys` and attach the five measures every view is built from."""
    g = df.groupby(keys, observed=True, sort=False)
    out = g.agg(
        units=("margen_retail", "size"),
        revenue=("precio_de_lista_synt", "sum"),
        margin=("margen_retail", "sum"),
        losses=("loss_making", "sum"),
    )
    # margin destroyed by the below-cost deals only — the size of the leak
    neg = df.loc[df.loss_making == 1].groupby(keys, observed=True, sort=False)["margen_retail"].sum()
    out["loss_margin"] = neg.reindex(out.index).fillna(0.0)
    return out.reset_index()


def columns(df: pd.DataFrame, ints: tuple[str, ...] = (), rounds: dict[str, int] | None = None) -> dict:
    """Column-oriented dict, with the money fields rounded to whole CLP."""
    rounds = rounds or {}
    out = {}
    for c in df.columns:
        s = df[c]
        if c in ints:
            out[c] = s.astype(int).tolist()
        elif pd.api.types.is_numeric_dtype(s):
            out[c] = s.round(rounds.get(c, 0)).tolist()
        else:
            out[c] = s.astype(str).tolist()
    return out


def main() -> None:
    df = pd.read_parquet(PARQUET)
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))

    ints = ("year", "month", "units", "losses", "revenue", "margin", "loss_margin", "customers")

    # ---- main cube: everything the Overview / Brand / Channel pages slice on -------
    main_cube = cube(df, ["year", "month", "marca", "brand_origin", "retail"])

    # ---- geography: top comunas by volume, the tail folded into one bucket --------
    top = df.comuna.value_counts().head(TOP_COMUNAS).index
    geo = df.assign(comuna=df.comuna.where(df.comuna.isin(top), "OTRAS COMUNAS"))
    geo_cube = cube(geo, ["comuna", "year", "retail"])

    # ---- models: the long tail is 1,543 nameplates, only the head is decision-grade
    top_m = df.detalle.value_counts().head(TOP_MODELS).index
    mod = df[df.detalle.isin(top_m)]
    model_cube = cube(mod, ["detalle", "marca", "year", "retail"])

    # ---- price bands --------------------------------------------------------------
    band_cube = cube(df, ["price_band", "year", "retail"])

    # ---- per-year distinct customers (a count that cannot be summed from the cube) --
    cust = df.groupby("year", observed=True).encrypt_rut.nunique().reset_index(name="customers")

    # ---- repeat-purchase distribution: the evidence behind "transactional" ---------
    freq = df.encrypt_rut.value_counts()
    buckets = pd.cut(freq, [0, 1, 2, 3, 4, np.inf], labels=["1", "2", "3", "4", "5+"])
    repeat = buckets.value_counts().sort_index()
    repeat_dist = {
        "labels": repeat.index.astype(str).tolist(),
        "customers": repeat.values.astype(int).tolist(),
        "pct": (repeat.values / len(freq) * 100).round(2).tolist(),
    }

    # ---- seasonality: month-of-year index, 100 = the average month ------------------
    m = df.groupby("month", observed=True).size()
    season = {
        "month": m.index.astype(int).tolist(),
        "units": m.values.astype(int).tolist(),
        "index": (m.values / m.values.mean() * 100).round(1).tolist(),
    }

    # ---- margin-percent distribution, for the risk page -----------------------------
    edges = [-np.inf, -0.10, -0.05, 0.0, 0.025, 0.05, 0.075, 0.10, np.inf]
    labels = ["< -10%", "-10..-5%", "-5..0%", "0-2.5%", "2.5-5%", "5-7.5%", "7.5-10%", "> 10%"]
    hist = pd.cut(df.margin_pct, edges, labels=labels).value_counts().reindex(labels)
    margin_hist = {"labels": labels, "deals": hist.values.astype(int).tolist()}

    payload = {
        "generated_from": "data/derco_sales_clean.parquet",
        "rows": int(len(df)),
        "customers": int(df.encrypt_rut.nunique()),
        "date_min": str(df.fecha_transaccion.min().date()),
        "date_max": str(df.fecha_transaccion.max().date()),
        "years": sorted(df.year.unique().astype(int).tolist()),
        "brands": sorted(df.marca.unique().tolist()),
        "channels": sorted(df.retail.unique().tolist()),
        # UNKNOWN is a real bucket in the data (missing comuna, kept rather than dropped)
        # but it is not a comuna — the deck counts 511 and so does this.
        "comunas_total": int(df.loc[df.comuna != "UNKNOWN", "comuna"].nunique()),
        "unknown_comuna_pct": round(float((df.comuna == "UNKNOWN").mean() * 100), 2),
        "models_total": int(df.detalle.nunique()),
        "cube": columns(main_cube, ints),
        "geo": columns(geo_cube, ints),
        "models": columns(model_cube, ints),
        "bands": columns(band_cube, ints),
        "customers_by_year": columns(cust, ints),
        "repeat_dist": repeat_dist,
        "season": season,
        "margin_hist": margin_hist,
        "metrics": metrics,
    }

    OUT.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(ROOT)}  ({kb:,.0f} KB)")
    print(f"  cube {len(main_cube):,} rows · geo {len(geo_cube):,} · models {len(model_cube):,} · bands {len(band_cube):,}")


if __name__ == "__main__":
    main()
