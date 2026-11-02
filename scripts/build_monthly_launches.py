"""Fresh monthly portfolio launches using only signal-date information."""
import json,datetime as dt
from build_portfolios import BASKETS,SnapshotAdapter,simulate,day,date,anniversary,write_csv,ROOT,D

def build():
 source=SnapshotAdapter(D);first=day(source.policy['signal_start'])+1;cutoff=day(source.policy['cutoff'])
 starts=[first];cursor=dt.date.fromisoformat(date(first)).replace(day=1)
 while True:
  cursor=(cursor.replace(day=28)+dt.timedelta(days=4)).replace(day=1)
  if day(cursor.isoformat())>cutoff:break
  starts.append(day(cursor.isoformat()))
 results=[]
 for start in starts:
  for bps in source.policy['cost_bps']:
   for n,w,rank_start in BASKETS:
    run=simulate(source,n,w,bps,launch=start,rank_start=rank_start);path={p[0]:p for p in run['path']}
    for y in range(1,6):
     end=anniversary(start,y);point=path.get(end)
     results.append(dict(portfolio=run['id'],name=run['name'],cost_bps=bps,start=date(start),years=y,end=date(end),status='observed' if point else 'unfinished',multiple=point[3] if point else None))
    results.append(dict(portfolio=run['id'],name=run['name'],cost_bps=bps,start=date(start),years='all',end=date(cutoff),status='observed',multiple=path[cutoff][3]))
  print('Completed launch',date(start),flush=True)
 write_csv('portfolio_monthly_launches.csv',results)
 (D/'monthly_launches.json').write_text(json.dumps(dict(first=date(first),cutoff=date(cutoff),launches=len(starts),rule='Initial covered launch, then first calendar day of each month; fresh holdings; rebalance every 30 days from each launch.',results=results),separators=(',',':'),allow_nan=False))
if __name__=='__main__':build()
