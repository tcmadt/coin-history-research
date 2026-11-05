# Reproducibility

## What is included

This repository is self-contained for:

- serving the published paper locally
- inspecting the frozen observations and generated outputs
- rerunning the derived analyses from `dist/data/`
- validating the public claims and portfolio calculations

Run:

```bash
make verify
```

Serve the publication locally with:

```bash
make serve
```

Then open `http://localhost:8000`.

## Verification suite

`make verify` performs a JavaScript syntax check and runs five independent Python checks:

1. `verify_publication_claims.py`
2. `verify_research.py`
3. `verify_portfolios.py`
4. `verify_monthly_launches.py`
5. `verify_paper_summaries.py`

These checks use Python's standard library. Node.js is used only to syntax-check the browser application.

## Rebuilding derived outputs

From the repository root, the intended dependency order is:

```bash
python3 scripts/build_windows.py
python3 scripts/build_rolling.py
python3 scripts/build_buy_window.py
python3 scripts/build_portfolios.py
python3 scripts/build_monthly_launches.py
python3 scripts/build_portfolio_robustness.py
python3 scripts/build_extensions.py
python3 scripts/build_paper_summaries.py
python3 build_overview.py
make verify
```

Run rebuilds on a branch and inspect the complete diff. Several scripts regenerate public CSV or JSON files, so a definition change can affect the paper in more than one place.

## Upstream boundary

The initial source aggregation workspace is not included. `build_data.py` expects upstream inputs such as:

- `output/daily_market_data.csv.gz`
- `output/universe.csv`
- `output/study_data.json`
- `work/raw/asset-catalog.json`
- supplemental raw price histories

Those inputs were used to create the frozen daily histories committed under `dist/data/`. For that reason, this repository supports full audit and regeneration of the published derived analyses, but not a clean-room refetch of every upstream quote from third-party providers.

`requirements.txt` lists `pandas`, which is needed only by that upstream ingestion step.

## Deterministic research rules

- Compare an altcoin and Bitcoin over identical entry and exit dates.
- Require observed endpoint prices for both assets.
- Do not carry prices forward.
- Do not convert missing exits to zero outside an explicit sensitivity test.
- Use only information available before each portfolio rebalance.
- Preserve the published snapshot date and cohort definitions when reproducing the paper.

For complete definitions, exclusions and limitations, read `dist/methodology.md`.
