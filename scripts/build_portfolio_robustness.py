"""Focused robustness checks for the flagship top-10 cap-weighted basket."""
import csv, datetime as dt, json, statistics
from build_portfolios import SnapshotAdapter, simulate, day, date, anniversary, write_csv, ROOT, D

def build():
    source=SnapshotAdapter(D); first=day(source.policy['signal_start'])+1; cutoff=day(source.policy['cutoff'])
    starts=[first]; cursor=dt.date.fromisoformat(date(first)).replace(day=1)
    while True:
        cursor=(cursor.replace(day=28)+dt.timedelta(days=4)).replace(day=1)
        if day(cursor.isoformat())>cutoff: break
        starts.append(day(cursor.isoformat()))
    baseline=list(csv.DictReader((ROOT/'dist/portfolio_monthly_launches.csv').open()))
    baseline={(r['start'],r['years']):float(r['multiple']) for r in baseline if r['portfolio']=='top10_cap' and r['cost_bps']=='0' and r['status']=='observed'}
    rows=[]
    variants=[
        ('rebalanced','Rebalanced',set(),30),
        ('held','Buy and hold',set(),None),
        ('rebalanced_ex_eth','Rebalanced, excluding ETH',{'eth'},30),
        ('held_ex_eth','Buy and hold, excluding ETH',{'eth'},None),
    ]
    for start in starts:
        for key,label,excluded,frequency in variants:
            if key=='rebalanced':
                for years in (2,5,'all'):
                    multiple=baseline.get((date(start),str(years)))
                    rows.append(dict(variant=key,label=label,start=date(start),years=years,status='observed' if multiple is not None else 'unfinished',multiple=multiple))
                continue
            run=simulate(source,10,'cap',0,launch=start,exclude_assets=excluded,rebalance_days=frequency)
            path={p[0]:p for p in run['path']}
            for years in (2,5):
                point=path.get(anniversary(start,years))
                rows.append(dict(variant=key,label=label,start=date(start),years=years,status='observed' if point else 'unfinished',multiple=point[3] if point else None))
            rows.append(dict(variant=key,label=label,start=date(start),years='all',status='observed',multiple=path[cutoff][3]))
    write_csv('portfolio_robustness.csv',rows)
    summary=[]
    for key,label,_,_ in variants:
        for years in (2,5,'all'):
            z=[r['multiple'] for r in rows if r['variant']==key and r['years']==years and r['status']=='observed']
            summary.append(dict(variant=key,label=label,years=years,launches=len(z),win_rate=sum(x>1 for x in z)/len(z),median_multiple=statistics.median(z)))
    (D/'portfolio_robustness.json').write_text(json.dumps(summary,separators=(',',':'),allow_nan=False))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': build()
