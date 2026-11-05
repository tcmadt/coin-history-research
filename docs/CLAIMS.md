# Public claims map

This file tells a reader or model where the paper's headline numbers come from. The executable check is `scripts/verify_publication_claims.py`.

## Opportunity is common, persistence is rare

**Claim:** Of the fixed 279-coin cohort, 98.2% beat Bitcoin from at least one one-year start, while 1.8% beat it from more than half of eligible one-year starts.

- Output: `dist/rolling_coin_results.csv`
- Generator: `scripts/build_rolling.py`
- Check: `scripts/verify_publication_claims.py`

These figures use every eligible one-year start for each coin in the fixed cohort.

## Median relative wealth falls with time

**Claim:** The median coin ended with 0.49x as much wealth as Bitcoin after one year and 0.06x after five years.

- Output: `dist/rolling_summary.csv`
- Generator: `scripts/build_rolling.py`
- Check: `scripts/verify_publication_claims.py`

## Matched-start robustness is a different question

**Claim:** On starts that have valid endpoints at every horizon from one to five years, the share of coins beating Bitcoin from most starts falls from 28.3% at one year to 5.4% at five years.

- Output: `dist/common_start_horizons.csv`
- Generator: `scripts/build_rolling.py`
- Check: `scripts/verify_research.py`

This does not contradict the 1.8% one-year result. The 1.8% figure uses every available one-year start. The 28.3% figure restricts the one-year comparison to the older starts that also have a five-year endpoint, removing later calendar periods from the one-year sample.

## The one-year result depends on buy dates, not just holding length

**Claim:** For the same 279 coins, the share beating Bitcoin from most one-year buy dates is 28.0% using buy dates through October 2021, then 13.3%, 7.9%, 3.2% and 1.8% as each later year of buy dates is added.

- Output: `dist/fig2_buy_window.csv`
- Generator: `scripts/build_buy_window.py`
- Check: `scripts/verify_publication_claims.py`

The final row reproduces the published 1.8% exactly. The October 2021 row differs slightly from the 28.3% common-start result, which also requires prices at every one- through five-year exit.

## Market-cap thresholds do not solve selection

**Claim:** Only 4.9% of coins with an observed five-year result after sustaining a $100 million market cap beat Bitcoin.

- Output: `dist/threshold_results.csv`
- Generator: `scripts/build_windows.py`
- Check: `scripts/verify_publication_claims.py`

## Diversification did not beat the benchmark over the common period

**Claim:** All six modeled portfolio rules trailed Bitcoin over their common July 2019 to October 2026 history.

- Outputs: `dist/portfolio_summary.csv`, `dist/portfolio_daily.csv`
- Generator: `scripts/build_portfolios.py`
- Checks: `scripts/verify_publication_claims.py`, `scripts/verify_portfolios.py`

This full-period result does not mean every launch date lost. `dist/portfolio_monthly_launches.csv` reports the share of monthly starts that beat Bitcoin at each horizon.

## Most of the five-year shortfall came from rerating

**Claim:** Relative supply growth explained 28.9% of the average five-year log shortfall, while changes in relative market value explained 71.1%.

- Output: `dist/supply_decomposition.csv`
- Generator: `scripts/build_extensions.py`
- Check: `scripts/verify_publication_claims.py`

This is an arithmetic decomposition of mean log relative returns. It is not a causal attribution and should not be compared directly with the median wealth ratios.

## Supplemental results

The paper also uses the following generated outputs:

- `dist/age_summary.csv`: results aligned by observed coin age
- `dist/cohort_summary.csv`: vintage-cohort summaries
- `dist/dilution_signal_monthly.csv`: association between supply growth and later relative returns
- `dist/winner_categories.csv`: exploratory categories for long-run winners
- `dist/altseason_breadth.csv`: market breadth through time
- `dist/five_year_missing_sensitivity.csv`: sensitivity to missing five-year exits
- `dist/steelman_yield.csv`: hypothetical altcoin-yield sensitivity

Consult `dist/methodology.md` before interpreting any result.
