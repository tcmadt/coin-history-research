"""Independent gross replay of fresh monthly starts and horizon accounting."""
import json,math,datetime as dt
from build_portfolios import BASKETS,SnapshotAdapter,D,ROOT,basket_id,day,date,anniversary
source=SnapshotAdapter(D);data=json.loads((D/'monthly_launches.json').read_text());rows=data['results'];base=json.loads((D/'portfolios.json').read_text())
starts=sorted({day(x['start']) for x in rows});assert len(starts)==88
assert all(dt.date.fromisoformat(date(x)).day==1 for x in starts[1:])
for start in starts:
 for n,weighting,rank_start in BASKETS:
  basket=basket_id(n,weighting,rank_start);expected={day(x['end']):x for x in rows if x['start']==date(start) and x['portfolio']==basket and x['cost_bps']==0 and x['status']=='observed'}
  if not expected:continue
  holdings={};cash=1.;btc0=source.prices['btc'][start]
  for d in range(start,max(expected)+1):
   value=cash+sum(q*source.prices[a][d] for a,q in holdings.items())
   if (d-start)%30==0:
    signal=d-1
    eligible=[a for a in source.caps[signal] if all(a in source.caps[t] for t in range(signal-29,signal+1))]
    ranked=sorted(eligible,key=lambda a:(-source.caps[signal][a],a))[rank_start-1:rank_start+n-1]
    caps=sum(source.caps[signal][a] for a in ranked)
    weights={a:1/n if weighting=='equal' else source.caps[signal][a]/caps for a in ranked}
    holdings={a:value*w/source.prices[a][d] for a,w in weights.items() if d in source.prices[a]};cash=value*sum(w for a,w in weights.items() if d not in source.prices[a])
   if d in expected:
    actual=(cash+sum(q*source.prices[a][d] for a,q in holdings.items()))/(source.prices['btc'][d]/btc0)
    assert math.isclose(actual,expected[d]['multiple'],rel_tol=1e-10),(basket,date(start),date(d))
assert len([r for r in rows if r['years']=='all'])==88*len(BASKETS)*3
for r in rows:
 assert day(r['end'])==(day(data['cutoff']) if r['years']=='all' else anniversary(day(r['start']),r['years']))
 assert (r['status']=='observed')==(day(r['end'])<=day(data['cutoff']))
 if r['status']=='unfinished':assert r['multiple'] is None
 if r['start']==date(starts[0]) and r['status']=='observed':
  original=next(x for x in base['runs'] if x['id']==r['portfolio'] and x['bps']==r['cost_bps']);p=next(x for x in original['path'] if x[0]==day(r['end']));assert math.isclose(p[3],r['multiple'],rel_tol=1e-12)
print('PASS: independent fresh-launch rankings, gross holdings and all completed endpoints; 88 launch dates; unfinished counts; matching inception and fee-scenario endpoints.')
