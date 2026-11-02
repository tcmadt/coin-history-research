# Data dictionary

The repository contains a frozen published snapshot dated 14 October 2026. CSV files are UTF-8 with a header row. JSON schemas should be confirmed against the file before use because some bundles are optimized for the browser.

## Core daily histories

Top-level asset files in `dist/data/` encode each daily observation as:

```text
[day_number, price_usd, estimated_market_cap_usd]
```

- `day_number`: integer days since 1970-01-01 UTC
- `price_usd`: observed USD price
- `estimated_market_cap_usd`: observed or estimated USD market capitalization, or null

Do not fill missing prices, reuse stale prices or infer a zero return from an absent exit.

## Principal outputs

| File | Grain | Purpose |
|---|---|---|
| `paper_summary.csv` | metric | Canonical values displayed in the paper |
| `rolling_coin_results.csv` | coin and horizon | Coin-level rolling-window outcomes |
| `rolling_summary.csv` | horizon | Aggregate rolling-window statistics |
| `common_start_horizons.csv` | horizon | Results restricted to starts valid at all one-to-five-year horizons |
| `age_summary.csv` | observed age | Relative outcomes aligned by coin age |
| `threshold_results.csv` | coin, threshold and horizon | Outcomes after sustained market-cap milestones |
| `cohort_summary.csv` | cohort and horizon | Results grouped by coin vintage |
| `portfolio_daily.csv` | date and portfolio | Daily modeled portfolio values |
| `portfolio_summary.csv` | portfolio | Full-period portfolio outcomes |
| `portfolio_monthly_launches.csv` | portfolio, launch and horizon | Outcomes from monthly simulated launches |
| `portfolio_membership.csv` | rebalance and portfolio member | Historical basket composition |
| `portfolio_reconciliation.csv` | snapshot | Checks on historical membership inputs |
| `supply_decomposition.csv` | coin | Five-year supply and market-value decomposition |
| `dilution_signal_monthly.csv` | month or bucket | Supply-growth signal analysis |
| `winner_categories.csv` | coin or category | Exploratory classification of winners |
| `altseason_breadth.csv` | date | Share of the eligible universe beating Bitcoin |
| `five_year_missing_sensitivity.csv` | scenario | Sensitivity to missing five-year endpoints |
| `steelman_yield.csv` | yield scenario | Hypothetical altcoin-yield sensitivity |
| `universe.csv` | asset | Inclusion, identity and source metadata |
| `data_audit.csv` | asset or check | Data-quality audit results |

The `_raw` rolling files preserve the broader pre-screen output used during validation. Reader-facing files apply the published cohort rules.

## Common concepts

- **Relative wealth multiple:** ending altcoin wealth divided by ending Bitcoin wealth over the same dates.
- **Win:** relative wealth multiple greater than `1.0`.
- **Win share:** fraction of eligible start dates on which the altcoin beats Bitcoin.
- **Reliable winner:** a coin with a win share greater than 50%.
- **Horizon:** the specified one-to-five-year holding period, using the date rules in `dist/methodology.md`.
- **Eligible:** has valid prices at both matched endpoints and meets the relevant sample rule.
- **Unknown:** an outcome with a missing entry or exit quote. Unknown outcomes are not losses unless a named sensitivity scenario explicitly imposes that assumption.

## Portfolio inputs

`research/portfolio_policy.json` contains the formal basket rules. `research/cmc_snapshots/` preserves the historical CoinMarketCap membership snapshots used to avoid selecting constituents with future information. Coverage and exclusions are documented in the portfolio audit and reconciliation outputs.
