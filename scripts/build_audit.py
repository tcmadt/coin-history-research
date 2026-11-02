"""Symmetric automated screen plus recorded review; flags are not automatic exclusions."""
import json,csv,datetime,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'dist/data';E=datetime.date(1970,1,1)
q=json.loads((D/'quality.json').read_text());cat=json.loads((D/'catalog.json').read_text())['assets'];events=[];gaps=0;total=0
fmt=lambda d:str(E+datetime.timedelta(days=d))
for m in cat:
 rows=json.loads((D/(m['id']+'.json')).read_text());total+=len(rows)
 assert all(r[1]>0 for r in rows) and all(a[0]<b[0] for a,b in zip(rows,rows[1:]))
 for a,b in zip(rows,rows[1:]):
  gap=b[0]-a[0];z=b[1]/a[1];gaps+=gap>30
  if (gap==1 and(z>=100 or z<=.01)) or (gap>30 and(z>=100 or z<=.01)):
   policy=q['valid_from'].get(m['id']) or q.get('valid_until',{}).get(m['id']);note=policy['reason'] if policy else q.get('review_flags',{}).get(m['id'],'Unresolved flag; retained pending source verification.')
   events.append(dict(asset=m['id'],name=m['name'],from_date=fmt(a[0]),to_date=fmt(b[0]),from_price=a[1],to_price=b[1],ratio=z,gap_days=gap,action='Segment quarantined' if policy else 'Retained: genuine loss' if m['id']=='luna' else 'Unresolved: retained',note=note,source=policy.get('source') if policy else 'https://libertystreeteconomics.newyorkfed.org/2023/07/runs-on-stablecoins/' if m['id']=='luna' else None))
raw=json.loads((D/'rolling-raw/summary.json').read_text());adjusted=json.loads((D/'rolling/summary.json').read_text());sensitivity=[]
for y in [1,2,3,4,5]:
 a=next(r for r in raw['summary'] if r['years']==y and r['cohort']=='available');b=next(r for r in adjusted['summary'] if r['years']==y and r['cohort']=='available');sensitivity.append(dict(years=y,raw_ever=a['ever_wins'],adjusted_ever=b['ever_wins'],raw_eligible=a['eligible'],adjusted_eligible=b['eligible'],raw_median=a['median_win_rate'],adjusted_median=b['median_win_rate']))
audit=dict(scanned_assets=len(cat),scanned_observations=total,large_gaps=gaps,flags=len(events),flagged_assets=len({x['asset'] for x in events}),events=events,sensitivity=sensitivity,rule='Flag adjacent observed quotes with at least 100x up or 100x down, for daily pairs and across gaps over 30 days. Review both gains and losses. Retain flagged outcomes absent a documented segment rule. Not a full liquidity, contract-identity or provider audit.',policies=q)
(D/'audit.json').write_text(json.dumps(audit,separators=(',',':')))
with (R/'dist/data_audit.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(events[0]));w.writeheader();w.writerows(events)
print('Audit:',len(cat),'assets;',total,'quotes;',len(events),'flags;',len({x['asset'] for x in events}),'flagged assets;',gaps,'gaps over 30 days')
print('Sensitivity:',sensitivity)
