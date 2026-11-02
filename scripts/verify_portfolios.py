"""Independent holdings-ledger replay and boundary checks for portfolio outputs."""
import csv,json,math,datetime as dt,collections
from pathlib import Path
from build_portfolios import rebalance
R=Path(__file__).resolve().parents[1];D=R/'dist/data';data=json.loads((D/'portfolios.json').read_text());runs=data['runs'];members=list(csv.DictReader((R/'dist/portfolio_membership.csv').open()));epoch=dt.date(1970,1,1)
def d(s):return (dt.date.fromisoformat(s)-epoch).days
prices={a:{row[0]:row[1] for row in json.loads((D/(a+'.json')).read_text())} for a in set(x['asset'] for x in members)|{'btc'}}
for run in [r for r in runs if r['bps']==0]:
 events=collections.defaultdict(list)
 for x in members:
  if x['portfolio']==run['id']:events[d(x['execution_date'])].append(x)
 holdings={};cash=1
 for day,expected,btc,relative in run['path']:
  value=cash+sum(q*prices[a][day] for a,q in holdings.items())
  if day in events:
   e=events[day];assert all(d(x['signal_date'])==day-1 for x in e);assert math.isclose(sum(float(x['target_weight']) for x in e),1)
   holdings={x['asset']:value*float(x['target_weight'])/prices[x['asset']][day] for x in e};cash=0
  actual=cash+sum(q*prices[a][day] for a,q in holdings.items())
  assert math.isclose(actual,expected,rel_tol=1e-10),(run['id'],day,actual,expected)
  assert math.isclose(relative,actual/btc,rel_tol=1e-10)
 assert len(events)==89
for run in runs:
 gross=next(r for r in runs if r['id']==run['id'] and r['bps']==0)
 assert run['end_wealth']<=gross['end_wealth']+1e-10
 assert math.isclose(sum(x['pnl'] for x in run['contributions'])-run['cost_dollars_per_initial_dollar'],run['end_wealth']-1,abs_tol=1e-9)
 for y in range(1,6):
  byday={x[0]:x for x in run['path']};vals=[]
  for start,nav,btc,relative in run['path']:
   a=epoch+dt.timedelta(days=start)
   end=dt.date(a.year+y,a.month,min(a.day,28) if a.month==2 and a.day==29 else a.day)
   stop=(end-epoch).days
   if stop in byday:vals.append(byday[stop][1]/nav/(byday[stop][2]/btc))
  v=next(x for x in run['rolling'] if x['years']==y)
  assert v['observed']==len(vals) and v['wins']==sum(x>1 for x in vals)
# Known self-financing purchase and full-rotation cases, distinct from output replay.
h,c,cost,t,b=rebalance({},1,{'a':2},{'a':1},.01)
assert math.isclose(h['a']*2,1/1.01) and math.isclose(cost,.01/1.01)
h,c,cost,t,b=rebalance({'a':1},0,{'a':1,'b':2},{'b':1},.01)
assert math.isclose(h['b']*2,.99/1.01)
# Failed purchase allocation remains cash; do not replace it with another candidate.
h,c,cost,t,b=rebalance({},1,{'a':1},{'a':.5},0)
assert h=={'a':.5} and c==.5
assert all(x['asset'] not in data['policy']['quarantined'] for x in members)
assert any(x['asset']=='luna' for x in members), 'Do not trim genuine crash losses'
for signal in {x['signal_date'] for x in members}:
 top10={x['asset'] for x in members if x['signal_date']==signal and x['portfolio']=='top10_cap'}
 next10={x['asset'] for x in members if x['signal_date']==signal and x['portfolio']=='top11_20_cap'}
 assert len(top10)==len(next10)==10 and not top10&next10
a=json.loads((D/'portfolio_reconciliation.json').read_text());assert a['signal_dates']==89
assert len(list((R/'research/cmc_snapshots').glob('*.json')))==89
print('PASS: independent daily holdings replay; all 89 memberships; disjoint top-10 and ranks 11–20 sleeves; calendar rolling windows; fees/self-financing; missing-purchase cash; constituent P&L reconciliation; source-quarantine policy and retained LUNA loss.')
