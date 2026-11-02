"""Recalculate additional cap screens from the unchanged 2026-10-14 snapshot."""
import json,csv,statistics,datetime,math,gzip,argparse
from pathlib import Path
from collections import deque
from snapshot_quality import valid_rows,QUALITY
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'dist/data'; cutoff=20740
catalog=json.loads((D/'catalog.json').read_text())['assets']; btc=dict((r[0],r[1]) for r in json.loads((D/'btc.json').read_text()))
old=json.loads((D/'study.json').read_text()); previous={(r['asset'],r['threshold']):r for r in old['threshold_results'] if r['threshold'] in [100_000_000,1_000_000_000]}
results=[]
# Capitalization coverage may start before usable prices. Preserve those signal
# windows rather than moving an entry forward to the first available price.
cap_source={};day_cache={}
parser=argparse.ArgumentParser();parser.add_argument('--snapshot-csv',type=Path,required=True);raw=parser.parse_args().snapshot_csv
with gzip.open(raw,'rt') as f:
 for row in csv.DictReader(f):
  dt=row['date'][:10]
  if dt not in day_cache:day_cache[dt]=(datetime.date.fromisoformat(dt)-datetime.date(1970,1,1)).days
  c=float(row['CapMrktEstUSD']) if row['CapMrktEstUSD'] else None
  if c is not None and not math.isfinite(c):c=None
  cap_source.setdefault(row['asset'],[]).append((day_cache[dt],0,c))
def date(n):return str(datetime.date(1970,1,1)+datetime.timedelta(days=n))
for meta in catalog:
 if not meta['included']:continue
 rows=valid_rows(meta['id'],json.loads((D/(meta['id']+'.json')).read_text())); prices={d:p/btc[d] for d,p,c in rows if d in btc}; caprows=[r for r in cap_source.get(meta['id'],[]) if r[2] is not None]
 for threshold in [10_000_000,100_000_000,1_000_000_000,10_000_000_000]:
  q=deque();total=0;last=None;known=False;signal=None
  for d,p,c in cap_source.get(meta['id'],[]):
   if c is None or (last is not None and d!=last+1):q.clear();total=0
   last=d
   if c is None:continue
   q.append(c);total+=c
   if len(q)>30:total-=q.popleft()
   if len(q)==30:
    if total/30>=threshold:signal=d;break
    known=True
  if signal is None or signal+1 not in prices:continue
  entry=signal+1
  r=dict(asset=meta['id'],name=meta['name'],threshold=threshold,cap_start=date(caprows[0][0]),signal_date=date(signal),entry_date=date(entry),first_crossing_observed=known,last_price_date=date(max(prices)))
  for h,days in [('1y',365),('2y',730),('3y',1096),('4y',1461),('5y',1826),('10y',3652),('to_cutoff',None)]:
   end=cutoff if days is None else entry+days
   r[h+'_status']='not_mature' if end>cutoff else 'observed' if end in prices else 'missing_endpoint'
   r[h+'_multiple']=prices[end]/prices[entry] if r[h+'_status']=='observed' else None
  if (meta['id'],threshold) in previous and meta['id'] not in set(QUALITY['valid_from'])|set(QUALITY.get('valid_until',{})):
   prev=previous[(meta['id'],threshold)]
   assert r['entry_date']==prev['entry_date'],(meta['id'],threshold,r['entry_date'],prev['entry_date'])
   for h in ['1y','4y','to_cutoff']:
    assert r[h+'_status']==prev[h+'_status']
    if r[h+'_multiple'] is not None: assert math.isclose(r[h+'_multiple'],prev[h+'_multiple'],rel_tol=1e-9),(meta['id'],h)
  results.append(r)
actual={(r['asset'],r['threshold']) for r in results if r['threshold'] in [100_000_000,1_000_000_000]}; assert {k for k in actual if k[0] not in set(QUALITY['valid_from'])|set(QUALITY.get('valid_until',{}))}=={k for k in previous if k[0] not in set(QUALITY['valid_from'])|set(QUALITY.get('valid_until',{}))}, ('missing', set(previous)-actual, 'extra', actual-set(previous))
summary=[]
for t in [10_000_000,100_000_000,1_000_000_000,10_000_000_000]:
 for h in ['1y','2y','3y','4y','5y','10y','to_cutoff']:
  z=[r for r in results if r['threshold']==t];obs=[r[h+'_multiple'] for r in z if r[h+'_status']=='observed'];n=len(obs);wins=sum(v>1 for v in obs);missing=sum(r[h+'_status']=='missing_endpoint' for r in z)
  summary.append(dict(threshold=t,horizon=h,qualified=len(z),observed=n,wins=wins,losses=n-wins,missing=missing,not_mature=sum(r[h+'_status']=='not_mature' for r in z),win_rate_observed=wins/n if n else None,median_multiple=statistics.median(obs) if n else None,mean_multiple=statistics.mean(obs) if n else None,win_rate_lower_bound=wins/(n+missing) if n+missing else None,win_rate_upper_bound=(wins+missing)/(n+missing) if n+missing else None))
# Additional screens are derived from the existing snapshot, not refreshed prices.
old['threshold_results']=results;old['summary']=summary;(D/'study.json').write_text(json.dumps(old,separators=(',',':'),allow_nan=False))
for filename,data in [('threshold_results.csv',results),('cohort_summary.csv',summary)]:
 with (ROOT/'dist'/filename).open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
print('Cross-checked unchanged assets against',len(previous),'prior entries; audited assets recomputed. Screens:')
for s in summary:print(s['threshold'],s['horizon'],s['wins'],s['observed'],s['missing'],s['not_mature'])
