# Do Altcoins Outperform Bitcoin?

An interactive working paper and reproducible research snapshot by [Tobé Madu](https://www.linkedin.com/in/tobemadu/).

- **Live paper:** https://coin-history-research.teeceem5.chatgpt.site/
- **Data snapshot:** 14 October 2026
- **Benchmark:** Bitcoin (BTC)
- **Formal screened sample:** 746 altcoins
- **Fixed five-year cohort:** 279 coins

## Research question

Nearly every altcoin beats BTC at some point. This project asks a harder question: how often does an altcoin beat BTC over the same dates, and how durable is that outperformance?

The study compares equal starting dollars invested in an altcoin and BTC over identical entry and exit dates. It examines daily rolling holding periods, observed age, sustained market-cap thresholds, six portfolio rules, supply growth, exploratory winner categories and market breadth.

## Headline findings

1. Among the 279 coins with at least one complete five-year price window, 98.2% beat BTC from at least one one-year start, but only 1.8% beat it from most one-year starts.
2. The median coin finished a one-year window with 0.49× as much wealth as BTC and a five-year window with 0.06×.
3. Only 4.9% of coins with an observed five-year result after sustaining a $100 million market cap beat BTC.
4. All six modeled portfolios trailed BTC over the common July 2019 to October 2026 period.
5. Relative supply growth explained 28.9% of the average five-year log shortfall; changes in relative market value explained the remaining 71.1%.

Every highlighted number is checked by `scripts/verify_publication_claims.py`.

## Start here

### Human readers

1. Read the [live paper](https://coin-history-research.teeceem5.chatgpt.site/).
2. Read [dist/methodology.md](dist/methodology.md) for definitions and research rules.
3. Use [docs/CLAIMS.md](docs/CLAIMS.md) to trace each headline result to its output file.
4. Use [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) to interpret the datasets.

### LLMs and coding agents

Read these files in order:

1. [AGENTS.md](AGENTS.md)
2. [PROJECT_MANIFEST.json](PROJECT_MANIFEST.json)
3. [docs/CLAIMS.md](docs/CLAIMS.md)
4. [dist/methodology.md](dist/methodology.md)
5. [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)
6. The relevant script and generated output

The repository includes a frozen published snapshot. Do not infer missing prices as zero, carry prices forward or treat overlapping windows as independent observations.

## Quick start

```bash
# Serve the published snapshot
make serve

# In another terminal, open http://localhost:8000

# Run the independent checks
make verify
```

The verification suite uses Python's standard library and Node.js. `pandas` is only required for the upstream ingestion script.

## Repository map

| Path | Purpose |
|---|---|
| `dist/index.html` | Published paper and interface |
| `dist/app.js` | Interactive charts, tables and filters |
| `dist/style.css` | Screen and print styles |
| `dist/data/` | Frozen daily histories and generated JSON bundles |
| `dist/*.csv` | Reader-facing and audit output tables |
| `dist/methodology.md` | Detailed research methodology |
| `scripts/` | Build, audit and verification scripts |
| `research/` | Portfolio policy and preserved historical membership snapshots |
| `docs/` | LLM navigation, claims map, data dictionary and reproducibility notes |

## Reproducibility boundary

The repository is self-contained for inspecting the publication, rerunning the derived analyses from the frozen `dist/data` snapshot and executing the verification suite.

The original upstream ingestion inputs referenced by `build_data.py` are not included. Those inputs contained the source aggregation workspace used to produce the frozen daily JSON histories. See [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

## Important limitations

- The sample is incomplete and is not every coin ever traded.
- Overlapping daily windows are historical experiences, not independent bets.
- Missing exit prices remain unknown rather than being set to zero.
- Returns exclude staking rewards, airdrops, spreads and market impact unless explicitly tested.
- Portfolio results are model outputs, not records of an investable fund.
- This is descriptive research, not investment advice.

## Citation

Tobé Madu, “Do Altcoins Outperform Bitcoin?”, 2026.

https://coin-history-research.teeceem5.chatgpt.site/
