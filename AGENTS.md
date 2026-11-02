# Research agent guide

## Objective

Help readers inspect, reproduce and extend *Do Altcoins Outperform Bitcoin?* without silently changing the study's definitions.

## Read order

1. `README.md`
2. `PROJECT_MANIFEST.json`
3. `docs/CLAIMS.md`
4. `dist/methodology.md`
5. `docs/DATA_DICTIONARY.md`
6. The relevant generator and output file

## Source hierarchy

When files appear to disagree, use this order:

1. Frozen observations in `dist/data/`
2. Explicit research rules in `research/portfolio_policy.json` and `scripts/snapshot_quality.py`
3. Generated CSV and JSON outputs
4. Prose in the paper or documentation

Report any disagreement rather than choosing the more convenient value.

## Definitions that must not drift

- Every comparison uses equal starting dollars in an altcoin and Bitcoin over identical dates.
- A relative result of `1.0x` means the investments finish with equal wealth. Above `1.0x` is an altcoin win.
- A reliable winner beats Bitcoin from more than half of eligible start dates.
- Missing entry or exit prices remain unknown. Do not set them to zero or carry prices forward.
- Overlapping daily windows describe historical experiences. They are not independent bets.
- Cross-horizon comparisons use the fixed 279-coin cohort unless a file explicitly says otherwise.
- The 71.1% market-value and 28.9% supply split is a mean log-return decomposition, not a median result or causal estimate.

## Change protocol

1. Identify the output and claim affected by the change.
2. Change the generator, not just a generated file.
3. Rebuild the smallest relevant set of outputs.
4. Run `make verify`.
5. Update the paper, claim map and data dictionary if definitions or public numbers changed.
6. Inspect the diff for accidental changes to the snapshot date, sample or missing-data rules.

## Commands

```bash
make serve
make verify
```

See `docs/REPRODUCIBILITY.md` for the full rebuild sequence and the upstream-data boundary.
