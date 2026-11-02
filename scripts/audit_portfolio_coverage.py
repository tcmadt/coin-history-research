"""Audit frozen inputs for historical portfolio construction. Not a backtest."""
import csv, datetime as dt, gzip, json, math, argparse
from pathlib import Path
from snapshot_quality import valid_rows

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'dist/data'
p = argparse.ArgumentParser()
p.add_argument('--snapshot-csv', type=Path, required=True)
args = p.parse_args()
catalog = json.loads((D/'catalog.json').read_text())['assets']
meta = {r['id']: r for r in catalog}
prices = {r['id']: {x[0] for x in valid_rows(r['id'], json.loads((D/(r['id']+'.json')).read_text()))} for r in catalog}
caps = {}
with gzip.open(args.snapshot_csv, 'rt') as f:
    for r in csv.DictReader(f):
        if not r['CapMrktEstUSD']: continue
        c = float(r['CapMrktEstUSD'])
        if not math.isfinite(c) or c <= 0: continue
        date = r['date'][:10]
        caps.setdefault(date, []).append((r['asset'], c))
dates = sorted(caps)
first, cutoff = dt.date.fromisoformat('2013-10-16'), dt.date.fromisoformat('2026-10-14')
out = []
d = first
while d <= cutoff:
    key = d.isoformat()
    day = (d-dt.date(1970,1,1)).days
    ranked = sorted([r for r in caps.get(key, []) if r[0] != 'btc'], key=lambda x:x[1], reverse=True)
    screened = [r for r in ranked if meta.get(r[0], {}).get('included')]
    top = ranked[:20]
    excluded = [a for a,c in top if not meta.get(a,{}).get('included')]
    missing = [a for a,c in screened[:20] if day+1 not in prices.get(a,set())]
    out.append(dict(signal_date=key,source_altcoins_with_cap=len(ranked),screened_altcoins_with_cap=len(screened),top20_source_assets='|'.join(a for a,c in top),top20_source_excluded='|'.join(excluded),screened_top20_missing_next_day_price='|'.join(missing)))
    d += dt.timedelta(days=30)
with (ROOT/'dist/portfolio_coverage_audit.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
report = dict(status='not_ready',cutoff=cutoff.isoformat(),first_positive_cap_date=dates[0],last_positive_cap_date=dates[-1],rebalance_dates=len(out),dates_with_fewer_than_20_screened=sum(r['screened_altcoins_with_cap']<20 for r in out),dates_with_excluded_top20=sum(bool(r['top20_source_excluded']) for r in out),dates_with_missing_next_day_prices=sum(bool(r['screened_top20_missing_next_day_price']) for r in out),original_period_covered=dates[0]<=first.isoformat(),blockers=[
    'No independently reconciled historical market-wide constituent list. Provider omissions cannot be measured from this catalog alone.',
    'The per-token study excludes both sides of some migrations, including AAVE/LEND. Index construction needs dated economic-asset mappings and conversion rules.',
    'Missing or quarantined holdings require a documented liquidation, recovery or valuation policy. They cannot silently disappear or be carried forever.',
    'Trading costs, historical liquidity and next-period executions have not been validated.'
])
(D/'portfolio_coverage.json').write_text(json.dumps(report,separators=(',',':')))
print(json.dumps(report,indent=2))
