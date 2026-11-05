# Altcoins against Bitcoin: methods and limits

Price snapshot: **14 October 2026**. Original question credited to Willy Woo's November 2016 studies. No new price observations were fetched for this revision.

## Coin histories

The catalog contains 846 source histories, including BTC; the explorer can display 845 other instruments. The broad catalog includes receipts and pegged assets excluded from the aggregate studies. All time uses each instrument's own first and last valid matched observation. A source's first observation need not be its first real trade, and quoted prices need not have been executable at scale.

Fixed 1/2/3/4/5 calendar-year views end at the snapshot and require exact matched start and end quotes. This selects surviving histories. Interior gaps remain gaps; no forward fill is used. Large selections are sampled weekly for display; CSV exports use valid daily source observations. Hover emphasizes the nearest plotted line without a floating caption or click lock. Moving away restores the view. Search spotlights a plotted coin without filtering the rest; clearing the search or pressing Escape releases it. An exhaustive daily winner-list hover is not used.

Relative wealth is (coin exit / coin entry) divided by (BTC exit / BTC entry). BTC is 1×. Most series use Coin Metrics daily USD prices. PONS and StonkFun's STONK use separately matched CoinGecko midnight BTC observations. Those conventions are not silently blended.

## Price-history audit

A symmetric automated pass scans all 846 original histories and 1,267,338 quotes for nonpositive/duplicate dates and prices, consecutive-day 100× upward or 100× downward changes, and similarly large changes across gaps exceeding 30 days. The pass found 12 extreme-discontinuity flags in 10 assets, plus three gaps over 30 days. The flag register, evidence and actions are available as data_audit.csv and data/audit.json. This is a scoped discontinuity audit, not verification of every venue, contract identity, liquidity or initial trade.

Original quotes are retained. data/quality.json defines documented derived-series rules:

- MEME: start 3 November 2023; quarantine nine identical pre-listing micro-quotes.
- APT: start 19 October 2022, after a micro-price segment discontinuous with the documented spot listing.
- CORE: start 8 February 2023, after a pre-listing segment discontinuous in the opposite direction.
- TAO: start 3 March 2023 under a conservative documented listing/discontinuity rule; the prior quoted identity or units remain unverified.
- SOON: start 16 January 2026, the first covered quote after its documented May 2025 listing. The prior segment ends before listing and is separated by a 248-day gap. No return is bridged across these incompatible segments.
- DATA: stop on 8 July 2026. The later segment begins with an unresolved 1,028× one-day jump; affected study exits become unknown. No rescaling factor is invented.

FXS, SUN and U retain unresolved flags pending corroboration. LUNA's genuine May 2022 collapse stays in the dataset. Size of a gain or loss alone is not an exclusion rule. Listing dates support review but do not prove no earlier market existed. Every quarantine is disclosed as a conservative research policy with unresolved causes.

Raw-source versus quality-adjusted rolling summary files expose sensitivity. At one year, raw data yields 467 confirmed ever-winners among 663 mature-entry coins; adjusted data yields 465/662. The median priced winning frequency remains approximately 8.8%. This does not imply all unflagged quotes are correct.

## Market-cap entry study

The aggregate fixes instrument-type and known migration/parallel-representation exclusions, retaining 746 assets. Its membership is not selected by returns. It is a per-token comparison, not a tradable index.

A coin qualifies when its first covered 30-calendar-day average circulating market cap crosses the selected $10M/$100M/$1B/$10B threshold. Thirty valid consecutive daily observations are required. Entry is the next daily close. A missing or quarantined entry is not moved forward. Some assets are already above the screen when capitalization coverage starts. Price and cap coverage can start at different times.

Fixed holding lengths are 365, 730, 1,096, 1,461, 1,826 and 3,652 days (1/2/3/4/5 years). These preserve the prior one-/four-year definitions. Since qualification exits at the snapshot and deliberately mixes holding lengths, so it is separated visually. There are no mature ten-year entry windows within this provider's covered cap history; that is unavailability, not zero success. The cap chart defaults to $100M.

Priced win rates exclude immature and unknown exits, both shown explicitly. Missing or quarantined exits stay unknown. Samples overlap, thresholds are nominal USD, and provider coverage is incomplete. Downloads include all threshold entries and summaries. Inflation, trading costs, taxes, rewards and airdrops are not included in the price study.

## Rolling windows

Every valid source-covered daily entry in the same 746-asset universe is compared with BTC at the same calendar date 1/2/3/4/5 years later. February 29 maps to February 28 when needed. This differs slightly from the fixed day lengths in the cap-entry study. There is no rolling market-cap or liquidity screen.

Immature windows end after the snapshot. Mature windows lacking an exact exit quote remain unknown, including stops caused by delisting, source gaps or audit rules. No automatic zero or stale last-price exit is substituted.

A confirmed opportunity means at least one priced window with relative wealth strictly above 1. All coins with a mature entry enter the denominator, even if none of their exits is priced. A coin with no recorded win and any unknown exit is unresolved; the opportunity range counts those coins as never/ever winners. These are identification bounds, not confidence intervals.

Frequency is priced wins / priced windows for each coin. Summary medians weight each coin equally and exclude coins with no priced windows. Missing-exit bounds include every mature-entry coin, treating unknown windows as losses/wins. Overlapping daily windows are not independent trials. Selecting winning dates after the fact is not an executable entry rule or a forecast.

The optional fixed cohort contains the 16 assets with at least one priced ten-year window. It holds membership constant across horizons, not performance constant. Its control is in Methods. Individual entry-date inspection is optional on the main page.

## Skilled participation without trading

The question is whether informed protocol selection, staking and non-trading onchain contributions can add rewards relative to passive exposure. We exclude speculative swaps, trading timing, leverage and MEV-searcher P&L. Changes in the price of held capital remain market exposure and are not attributed to skill.

The passive ETH/SOL examples invest equal $10,000 amounts from 27 August 2022 to the snapshot. wstETH and mSOL quoted prices capture reward accrual and market premiums/discounts. They are liquid-staking return proxies, not reconstructed native validator balances. No additional APY is added.

Only the ETH case adds a constructed non-trading layer: $9,500 wstETH plus $400 ETH working capital after an assumed $100 upfront activity budget. A qualifying post-Nitro Arbitrum account bridges, uses applications/governance in two months, makes more than four qualifying transactions, and satisfies other eligibility/anti-Sybil rules. It receives a defined 625 ARB allocation and holds it to the snapshot. Working-capital token units are assumed unchanged. There is no hypothetical airdrop-sale strategy or trading profit. Actual costs, taxes, labor and protocol-loss risk are not reconstructed; the amount is not a median ecosystem reward.

The separate Jito example describes documented points and validator-client participation rewards. Holding mSOL does not confer JTO eligibility. Covered JitoSOL prices begin after the 2023 distribution, so we do not credit JTO to the mSOL investor or invent a matched early JitoSOL total return. The Jupiter swap-based allocation example has been removed.

These mechanisms do not establish a causal skill premium. A proper test would predefine protocol choices and actions, record all capital commitments, failed attempts, rewards, risk losses, fees and time, and compare net marked wealth against passive staking in the same L1 over the same dates.

## Coverage limitations

Missing first trades can omit early gains or losses. The source omits much of the Solana-era memecoin universe and other historical assets; the direction of its effect is unknown. No result is claimed to represent the entire market. Token histories with long coverage are a selected group. Woo's entire original 118-coin membership remains unrecovered; this is an extension of his question, not an exact reconstruction.

Reproduction scripts: build_overview.py; scripts/build_windows.py; scripts/extend_study.py (retained snapshot CSV input); scripts/build_rolling.py (SNAPSHOT_RAW=1 for sensitivity); scripts/build_participation.py; scripts/build_audit.py; scripts/verify_research.py. Raw per-coin JSON and original snapshot dates remain unchanged.


## Portfolio extension: covered-universe test

The main page separates individual outcomes, capitalization qualification and portfolio construction. The rolling individual-coin distribution counts each coin once by observed winning-window frequency. The second headline counts coins winning on strictly more than 50% of priced entry dates. Missing windows are excluded from that frequency; median missing-exit bounds remain visible. The denominator differs from the ever-winner headline, which includes all elapsed-entry coins. These are historical descriptions, not forecasts or selection-skill estimates.

### Scope and common start

This is a restricted Coin Metrics covered-universe backtest, not a complete historical crypto-market index. The frozen catalog is selected today and may omit former failures or leaders. The per-token instrument exclusions remove stablecoins, receipts and specified migrations/parallel representations. They are retained here rather than imputing conversion ratios. Three unresolved instruments (FXS, SUN, U) are additionally quarantined for source discontinuities. LUNA's genuine collapse remains. These exclusions can materially affect results and must not be interpreted as a universally executable ex-ante selection strategy.

The earliest positive estimated cap quote in the download is 3 May 2018, but fewer than 20 eligible cap series exist until 22 June 2019. Thirty consecutive positive daily cap observations produce the first shared signal on 21 July 2019 and execution on 22 July. All portfolios end on 14 October 2026. The period is about 7.2 years, not eight years and not a replication of Woo's 2013–2016 sample.

### Formation and costs

Rank the restricted universe by signal-day CapMrktEstUSD. Require 30 consecutive daily positive cap observations through the signal date; do not require future survival. Choose top 10 cap weighted, top 20 cap weighted, or top 20 equal weighted. Signal dates advance every 30 days; execute at the next daily close. Weights drift between rebalances. A separate source adapter and research/portfolio_policy.json hold data and rule choices. Replacing the source still requires explicit identity, timestamp and supply-definition reconciliation.

If a selected purchase lacks its execution quote, keep its target allocation in zero-interest USD cash, without substituting a lower-ranked asset. If a held asset lacks a quote, retain units, leave NAV unknown and defer any scheduled rebalance until its next scheduled date with complete held marks. Never erase a holding, silently forward-fill, or assign zero because coverage stops. The present run has no missing held daily marks or failed purchase quotes.

Gross and illustrative 25/100 basis-point costs are separate scenarios. Charge per dollar bought or sold, including initial purchases. Solve post-fee wealth W from pre-trade wealth V = W + fee × sum(abs(W × target weight − current holding value)); this avoids borrowing to pay costs. BTC bears the same initial purchase rate. No terminal liquidation charge, staking, airdrop, fork distribution, lending, tax or cash interest is included. Costs are assumptions, not estimates of historical spreads, liquidity or achievable execution.

### Measures

BTC-relative wealth divides portfolio NAV by the buy-and-hold BTC wealth from equal initial capital. Maximum USD drawdown uses daily NAV. Annual one-way turnover sums half of traded notional divided by pre-trade NAV at each rebalance after inception and divides by elapsed years. Rolling 1–5 calendar-year windows measure an investment in the pre-existing modeled portfolio path at each daily observation, with February 29 mapping to February 28. Ongoing modeled rebalance costs are included; an additional new-investor subscription/redemption trade is not. Overlapping windows are not independent observations.

Constituent P&L sums units actually held before each daily price change times that change. Summed dollar P&L less paid costs equals terminal NAV minus initial wealth. The top-five concentration statistic divides those positive contributors by all positive contributions; offsetting negative contributions are shown separately. It is not a decomposition of BTC-relative wealth or Bessembinder's market-wide net wealth-creation measure.

### Historical reconciliation

All 89 model signal dates have a preserved public CoinMarketCap historical-page extract, with original CMC IDs, source URL, retrieval timestamp and hash of downloaded HTML. Exact normalized name plus ticker gives a mapping candidate; documented numeric-ID aliases cover name changes. Historical Acash Coin and Storeum are explicitly not mapped to modern Acala and StakeStone merely because tickers collide. Broader CMC top-20 comparison excludes identified stablecoins and receipts but retains migration candidates to expose our restricted-universe omissions.

On average 17.97 of 20 constituents overlap; the range is 15–20, with five exact matches. There are 56 unmapped member-date observations and 82 excluded migration/parallel-representation member-date observations. Missing cap data and rank/eligibility differences are separate dispositions. These observations are not counts of unique assets. The audit reconciles discrepancies into a ledger; it does not establish complete historical membership or solve excluded migrations. CMC prices/caps are not spliced into the model. Historical vendor records may be revised; these are retrieved historical records, not a guaranteed vintage-as-published archive. The portfolio bundle includes a SHA-256 fingerprint of the frozen input files and policy.

Downloads: portfolio_membership.csv, portfolio_reconciliation.csv, portfolio_identity_map.csv, portfolio_exclusions.csv, portfolio_daily.csv, portfolio_summary.csv, portfolio_rolling.csv, portfolio_contributions.csv and the compressed CMC source records. Reproduce with scripts/build_portfolios.py, scripts/reconcile_portfolio_membership.py and scripts/verify_portfolios.py. Raw public snapshot extraction is isolated in scripts/fetch_portfolio_snapshots.py.

The research questions follow Hendrik Bessembinder, *Do stocks outperform Treasury bills?*, Journal of Financial Economics 129(3), 2018, https://doi.org/10.1016/j.jfineco.2018.06.004, and Willy Woo, *Crypto-currency Index Funds, the simulations have surprising results*, 18 October 2016, https://woobull.com/crypto-currency-index-funds-the-simulations-have-surprising-results/. Stock findings motivate the questions; Bitcoin is not a diversified crypto index.


## Paper revision: observed age and reader controls

Headlines lead with percentages; counts remain below them. Ever-winner percentages divide by coins with at least one elapsed entry window. Majority-win percentages divide by coins with at least one priced window and require strictly more than 50% observed wins. The denominators differ. Missing end-date prices stay unknown.

All reported 25th/50th/75th percentiles use linear interpolation at order index (n−1)p (the common type-7 convention). Individual winning-frequency quartiles give each priced coin one observation; cap-screen return quartiles use the priced qualified coin returns. Portfolio return quartiles use the priced rolling fund-return windows. Those are distinct distributions, not interchangeable estimates.

The observed-age study uses the 746 instrument-screened histories with the existing source-quality rules. Age zero is each coin's first valid BTC-matched source price, which may follow its first real trade. At ages 0,30,60,…,3630 days plus 3652 days, compute the exact daily coin/BTC price ratio divided by its age-zero ratio. No nearest-date substitution or forward fill is used. Each coin counts once at each age. Elapsed means the target age falls on or before the snapshot; missing means that target lacks a source price. Cohorts can be filtered by first observed calendar year. The band is a cross-sectional interquartile range, not a confidence or prediction interval. Membership changes with age, so gaps and survivor selection may distort the pattern. No age-based forecasting rule or out-of-sample skill is claimed.

The explorer keeps all 845 non-BTC catalog instruments, including those excluded from aggregate research. First-observed-year and age-at-snapshot filters use the same audited source start. Its cap hurdle is the first valid daily observation at or above the chosen CapMrktEstUSD level. This differs from the cap study's 30-day average and next-day execution. In all-time explorer views, prices before that touch are removed, and wealth is reset to 1× at the exact touch observation. This is a descriptive same-day view, not an executable strategy. In fixed-window views, the hurdle must have been crossed by the shared start date. Future lifetime peaks are never used to select earlier returns. Missing cap series do not pass a cap hurdle.

The age x-axis always measures time since the first valid source price, even when the displayed investment begins later after a cap touch. Minimum/maximum age filters refer to elapsed time to the snapshot, not the length of an uninterrupted traded history. Large selections use weekly plotted observations plus exact cap-touch, fixed-window and final endpoints; selections of up to 12 use daily records.

Rolling portfolio charts show each calendar-anniversary window at its ending date, using the same fund-relative-wealth ratios as the existing rolling outcome table. The main paper defaults to gross returns. Cost assumptions remain available in the full methods and are visibly labeled when used.

Rebuild observed-age and explorer data with scripts/build_paper_summaries.py. Verify counts, quartiles and exact cap-touch anchors with scripts/verify_paper_summaries.py. No new market data was fetched for this revision.


## Monthly launches and explorer presentation (27 October 2026)

Six baskets: top 10, top 20 and ranks 11–20, each cap weighted and equal weighted. Monthly launch tests start with fresh capital on 22 July 2019, then the first day of each following month, through 1 October 2026 (88 launches). Each uses previous-day ranking and its own 30-day rebalance schedule, with the existing eligibility, exact quote and fee policies. Outcomes use calendar anniversaries at 1–5 years. Unfinished endpoints are excluded and counted. Results and cost scenarios are in portfolio_monthly_launches.csv. These are overlapping scenarios, not independent trials. Existing CMC reconciliation covers 89 scheduled signals beginning 21 July 2019, not every new monthly-launch rebalance. Daily rolling fund-entry results remain a separate download. Five years remains the main long-term comparator, with four years shown alongside it.

The explorer's percentage axis is 100 × (date − first valid matched source date) / (last valid matched source date − first valid matched source date). Plot bounds are 0–100%; filters can leave only part of a history visible. A one-observation history is placed at zero. Actual elapsed age and calendar date remain available. This is retrospective alignment, not a predictive timing rule. Highlight labels show the last plotted observation's relative wealth and date. Tiny nonzero percentages use ordinary decimals to the first significant digit. Exact zero displays 0%.


## Presentation update (27 October 2026)

Hover or search emphasizes a single coin and labels its final plotted point with its ticker and BTC-relative multiple. The dashed reference is labeled BTC at its right end. Filters and downloads start collapsed. Supplemental chart notes are grouped behind information controls that support hover, focus, click/tap and Escape. Data calculations are unchanged. The introduction separates a network's usefulness from its token's return against BTC.


## Presentation and horizon update (27 October 2026)

The paper presents one- to five-year holding periods. Ten-year holding comparisons are omitted because only 16 covered coins had priced windows. This is a selected long-lived group; the missing original coin population must be reconstructed before estimating the size of survivor bias. It has not been established that most missing coins became worthless. The optional fixed cohort now uses coins with at least one priced five-year window (279 quality-adjusted; 280 raw). Historical 10-year rolling files are retired from the current analysis. The observed-age plot remains an age description, with contribution counts labeled on the median curve and available in the downloadable data. Observed age is not a fixed holding-period win-rate comparison.

The subtitle and median-frequency paragraph are removed. The explorer is part of Introduction. The study rules are reached by a link in the Data and methods paragraph. The individual-coin and cap-screen comparison figures are otherwise unchanged pending design selection. Source-ending reviews and delisting-to-zero proposals have not changed any return calculation.


## Working-paper framing and launch-to-cutoff comparison (27 October 2026)

The introduction links Woo’s 3 November 2016 visualization, which he called “shit runs downhill.” This study revisits that question and invites replication rather than claiming a complete market census or an exact reconstruction of his original sample. Author voice uses I for author decisions and this study for analysis. ANT redemption and NU conversion are discussed as counterexamples to equating a delisting or ended series with zero recovery. No automatic zero-return rule is applied.

The monthly launch selector also offers All time: each launch runs to the same frozen cutoff, 14 October 2026. The exported years field is the string all for these rows, and remains numeric for 1–5-year rows. Holding lengths differ across launch dates. The first all-time launch must reproduce the original full-period portfolio endpoint for the same cost setting. Later launch portfolios use fresh initial holdings and their own 30-day rebalance calendars. These endpoint results are not the daily wealth trajectory shown above them.

Observed-age sample counts are printed beside selected points of the median curve; every median observation has an exact n in its hover title. The separate count curve and table are removed. Full counts, missingness and spread remain in age_summary.csv. Supporting files and the study rules appear in References. Two image comparison sheets at the bottom are temporary design previews, with no selected replacement chart yet applied.


## Focused robustness checks (1 November 2026)

The main rolling comparison uses every completed start date available to each horizon. Because one-year windows can start four years later than five-year windows, cross-horizon changes can reflect both holding length and calendar composition. The common-start check restricts all five horizons to the same 206,471 coin-date starts across the same 279 coins. Each observation requires valid coin and BTC prices at entry and at every one- through five-year anniversary. The total counts coin-date pairs, not unique calendar dates. Results are in common_start_horizons.csv.

The missing-exit check applies three treatments to mature five-year windows in the fixed cohort: retain only exact observed exits; freeze wealth at the last observed coin/BTC relative value before the missing endpoint; or assign zero. The freeze is a sensitivity case, not an executable sale assumption. Results are in five_year_missing_sensitivity.csv.

The portfolio robustness check uses the same prior-day market-cap ranking, source-quality rules and monthly launch dates as the flagship top-10 cap-weighted basket. Buy-and-hold forms the basket once and does not rebalance. Ex-ETH variants remove ETH before selecting the first ten eligible coins. Results are gross of trading costs and appear in portfolio_robustness.csv. Reproduce with scripts/build_portfolio_robustness.py.

The fixed-cohort breadth check repeats trailing one-year breadth using only the 279 coins in the five-year fixed cohort. Coins count on a date only when exact prices exist at both endpoints; no price is filled. Results are in altseason_breadth_fixed.csv. Reproduce the common-start, missing-exit and breadth checks with scripts/build_extensions.py.

## Figure 2 buy-date window (5 November 2026)

Figure 2 has a slider that changes the last one-year buy date included, from 14 October 2021 to 14 October 2025 in monthly steps. The coin set never changes: it is the fixed 279-coin cohort. Each step uses the same one-year rules as the main rolling comparison: every valid daily entry on or before the chosen date, an exact calendar-year exit (29 February exits on 28 February), observed coin and BTC prices at entry and exit, and no carried-forward or filled prices. The two shares use the same denominators as the published figure: coins with at least one winning window out of coins with matured windows, and coins winning on more than half of their priced windows out of coins with priced windows. The final step reproduces the published 98.2% and 1.8% exactly. At 14 October 2021, every included buy date could also be held for five years; that step (28.0%) differs slightly from the 28.3% common-start result because the common-start check also requires prices at every one- through five-year exit. Results are in fig2_buy_window.csv. Reproduce with scripts/build_buy_window.py.
