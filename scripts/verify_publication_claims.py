"""Verify every numeric claim highlighted in the paper."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

paper = list(csv.DictReader((DIST / "paper_summary.csv").open()))
available = {int(r["years"]): r for r in paper if r["cohort"] == "available"}
common = {int(r["years"]): r for r in paper if r["cohort"] == "common"}
assert int(common[5]["priced"]) == 279
assert round(float(common[1]["ever_winner_pct"]), 1) == 98.2
assert round(float(common[1]["majority_winner_pct"]), 1) == 1.8
assert round(float(common[5]["majority_winner_pct"]), 1) == 5.4
assert round(float(common[1]["median_coin_multiple"]), 2) == 0.49
assert round(float(common[5]["median_coin_multiple"]), 2) == 0.06
assert round(float(available[1]["ever_winner_pct"]), 1) == 70.2
assert round(float(available[1]["majority_winner_pct"]), 1) == 3.8
assert round(float(available[5]["ever_winner_pct"]), 1) == 24.8
assert 4.0 <= float(available[4]["majority_winner_pct"]) <= 5.5
assert 4.0 <= float(available[5]["majority_winner_pct"]) <= 5.5
assert round(float(available[1]["median_coin_multiple"]), 2) == 0.41
assert round(float(available[5]["median_coin_multiple"]), 2) == 0.06
assert round(float(available[1]["median_ever_winner_multiple"]), 2) == 1.43
assert round(float(available[5]["median_ever_winner_multiple"]), 2) == 1.34

cohorts = list(csv.DictReader((DIST / "cohort_summary.csv").open()))
cap = {(int(r["threshold"]), r["horizon"]): r for r in cohorts}
assert round(100 * float(cap[(100_000_000, "5y")]["win_rate_observed"]), 1) == 4.9
assert int(cap[(10_000_000_000, "5y")]["wins"]) == 3
assert int(cap[(10_000_000_000, "5y")]["observed"]) == 20
assert round(100 * float(cap[(10_000_000_000, "5y")]["win_rate_observed"]), 1) == 15.0

age = json.loads((DIST / "data" / "age_summary.json").read_text())
one_year = next(r for r in age["cohorts"]["2025"]["points"] if r["age_days"] == 360)
assert round(one_year["median"], 2) == 0.25

launches = list(csv.DictReader((DIST / "portfolio_monthly_launches.csv").open()))
def share(portfolio, years):
    rows = [r for r in launches if r["portfolio"] == portfolio and r["cost_bps"] == "0" and r["years"] == str(years) and r["status"] == "observed"]
    return sum(float(r["multiple"]) > 1 for r in rows) / len(rows), len(rows)

top10 = [100 * share("top10_cap", years)[0] for years in (1, 2, 3, 4)]
assert round(min(top10)) == 34 and round(max(top10)) == 42
assert round(100 * share("top10_cap", 2)[0], 1) == 34.4
top10_two_year = [float(r["multiple"]) for r in launches if r["portfolio"] == "top10_cap" and r["cost_bps"] == "0" and r["years"] == "2" and r["status"] == "observed"]
assert round(sorted(top10_two_year)[len(top10_two_year)//2], 2) == 0.73
all_time = [100 * share(p, "all")[0] for p in sorted({r["portfolio"] for r in launches})]
assert round(min(all_time), 1) == 5.7 and round(max(all_time), 1) == 8.0
assert all(share(p, "all")[1] == 88 for p in sorted({r["portfolio"] for r in launches}))

extensions = json.loads((DIST / "data" / "extensions.json").read_text())
five = next(r for r in extensions["decomposition"] if r["horizon_years"] == 5)
assert five["coins"] == 272
assert round(100 * five["dilution_share"], 1) == 28.9
assert five["cap_grew_but_price_lost"] == 16 and five["cap_grew"] == 28
assert extensions["signal"]["months"] == 52 and extensions["signal"]["negative_months"] == 47
exchange = next(r for r in extensions["categories"] if r["category"] == "Exchange tokens")
other = next(r for r in extensions["categories"] if r["category"] == "All other coins")
assert (exchange["reliable_winners"], exchange["priced"]) == (5, 12)
assert (other["reliable_winners"], other["priced"]) == (10, 267)
yield20 = next(r for r in extensions["yield_tests"] if r["horizon_years"] == 5 and r["added_yield_pct"] == 20)
assert round(yield20["reliable_winner_pct"], 1) == 11.8
assert round(yield20["median_coin_multiple"], 2) == 0.16
peaks = {int(r["date"][:4]): round(r["share_ahead_pct"]) for r in extensions["annual_breadth"]}
assert peaks[2020] == 73 and peaks[2021] == 86 and peaks[2022] == 88
assert max(peaks[y] for y in (2023, 2024, 2025, 2026)) <= 32

common_start = {int(r["horizon_years"]): r for r in csv.DictReader((DIST / "common_start_horizons.csv").open())}
assert int(common_start[1]["windows"]) == int(common_start[5]["windows"]) == 206471
assert round(float(common_start[1]["reliable_winner_pct"]), 1) == 28.3
assert round(float(common_start[5]["reliable_winner_pct"]), 1) == 5.4

missing = {r["treatment"]: r for r in csv.DictReader((DIST / "five_year_missing_sensitivity.csv").open())}
assert round(float(missing["observed_only"]["median_coin_multiple"]), 3) == 0.065
assert round(float(missing["freeze_last_relative"]["median_coin_multiple"]), 3) == 0.064
assert round(float(missing["zero"]["median_coin_multiple"]), 3) == 0.058

basket = {(r["variant"], str(r["years"])): r for r in json.loads((DIST / "data" / "portfolio_robustness.json").read_text())}
assert round(basket[("rebalanced", "5")]["median_multiple"], 2) == 0.78
assert round(100 * basket[("rebalanced", "5")]["win_rate"], 1) == 25.0
assert round(basket[("held", "5")]["median_multiple"], 2) == 0.86
assert round(100 * basket[("held", "5")]["win_rate"], 1) == 35.7
assert round(100 * basket[("held_ex_eth", "5")]["win_rate"], 1) == 10.7
assert round(100 * basket[("rebalanced_ex_eth", "5")]["win_rate"], 1) == 3.6

fixed_peaks = {int(r["date"][:4]): r["share_ahead_pct"] for r in extensions["fixed_annual_breadth"]}
assert max(fixed_peaks[y] for y in (2023, 2024, 2025, 2026)) < 30

print("PASS: every highlighted paper number matches generated study files.")
