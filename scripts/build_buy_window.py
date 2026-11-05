"""Figure 2 buy-date window: one- to five-year results for the fixed cohort as later buy dates are added.

Uses the same calendar-year rules as build_rolling.py: every valid daily entry, exact
calendar-year exits (29 February exits on 28 February), observed prices for the
coin and BTC at both ends, nothing carried forward. The coin set never changes;
only the last buy date included changes. Each horizon’s final cutoff must reproduce its published rolling summary.
"""
import csv, datetime, json
from pathlib import Path
from snapshot_quality import valid_rows

R = Path(__file__).resolve().parents[1]
D = R / 'dist/data'
E = datetime.date(1970, 1, 1)
CUT = 20740  # 2026-10-14


def ds(n):
    return str(E + datetime.timedelta(days=n))


def anniv(n, y):
    d = E + datetime.timedelta(days=n)
    try:
        return (d.replace(year=d.year + y) - E).days
    except ValueError:
        return (d.replace(year=d.year + y, day=28) - E).days


def cutoffs(years):
    out, y, m = [], 2021, 10
    while (y, m) <= (2026 - years, 10):
        out.append((datetime.date(y, m, 14) - E).days)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


summary = json.loads((D / 'rolling/summary.json').read_text())
fig2 = next(x for x in summary['summary'] if x['cohort'] == 'common' and x['years'] == 1)
cohort = fig2['coin_ids']
btc = {d: p for d, p, _ in json.loads((D / 'btc.json').read_text())}

ratios = {}
for cid in cohort:
    rows = valid_rows(cid, json.loads((D / (cid + '.json')).read_text()))
    ratios[cid] = {d: p / btc[d] for d, p, _ in rows if d in btc}


def build_records(years):
    fig2 = next(x for x in summary['summary'] if x['cohort'] == 'common' and x['years'] == years)
    assert set(fig2['coin_ids']) == set(cohort)
    windows = {}
    for cid, ratio in ratios.items():
        w = []
        for start in sorted(ratio):
            end = anniv(start, years)
            if end > CUT:
                continue
            w.append((start, None if end not in ratio else ratio[end] / ratio[start] > 1))
        windows[cid] = w

    records = []
    for c in cutoffs(years):
        eligible = priced = ever = majority = unknown_only = 0
        for cid in cohort:
            z = [s for d, s in windows[cid] if d <= c]
            if not z:
                continue
            eligible += 1
            known = [s for s in z if s is not None]
            wins = sum(known)
            if wins:
                ever += 1
            elif len(known) < len(z):
                unknown_only += 1
            if known:
                priced += 1
                if wins / len(known) > .5:
                    majority += 1
        records.append(dict(cutoff=ds(c), cohort_coins=len(cohort), eligible=eligible, priced=priced,
                            ever_wins=ever, ever_unknown=unknown_only, majority_wins=majority,
                            ever_share=ever / eligible if eligible else None,
                            majority_share=majority / priced if priced else None))

    last = records[-1]
    assert last['cutoff'] == ds(anniv(CUT, -years))
    assert (last['eligible'], last['priced'], last['ever_wins'], last['ever_unknown']) == \
        (fig2['eligible'], fig2['priced'], fig2['ever_wins'], fig2['ever_unknown']), last
    rolling = {r['id']: r for r in json.loads((D / f'rolling/{years}y.json').read_text())}
    assert last['majority_wins'] == sum(1 for cid in cohort if rolling[cid]['observed'] and rolling[cid]['win_rate'] > .5), last

    return records


by_horizon = {years: build_records(years) for years in range(1, 6)}
records = by_horizon.pop(1)
(D / 'fig2_buy_window.json').write_text(json.dumps(dict(
    cutoff=ds(CUT), horizon_years=1, cohort='common', five_year_eligible_through='2021-10-14',
    first_buy_date=ds(min(min(ratio) for ratio in ratios.values())),
    note='Fixed cohort; only the last one-year buy date included changes. Shares use the same denominators as Figure 2.',
    records=records, by_horizon=by_horizon), separators=(',', ':')))
with (R / 'dist/fig2_buy_window.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(records)
for r in records:
    if r['cutoff'].endswith('-10-14'):
        print(r['cutoff'], f"ever {r['ever_wins']}/{r['eligible']} ({100*r['ever_share']:.1f}%)",
              f"majority {r['majority_wins']}/{r['priced']} ({100*r['majority_share']:.1f}%)")
