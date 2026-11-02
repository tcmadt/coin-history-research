"""Reproducible restricted-universe backtest. Source access is isolated in adapter."""
import csv,json,math,statistics,datetime as dt,collections,hashlib
from pathlib import Path
from snapshot_quality import valid_rows
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist/data';EPOCH=dt.date(1970,1,1)
BASKETS=[(10,'cap',1),(10,'equal',1),(20,'cap',1),(20,'equal',1),(10,'cap',11),(10,'equal',11)]
def day(s):return (dt.date.fromisoformat(s)-EPOCH).days
def date(n):return (EPOCH+dt.timedelta(days=n)).isoformat()
def anniversary(n,y):
 d=EPOCH+dt.timedelta(days=n)
 try:return (d.replace(year=d.year+y)-EPOCH).days
 except ValueError:return (d.replace(year=d.year+y,day=28)-EPOCH).days
class SnapshotAdapter:
 def __init__(self,root):
  self.meta={m['id']:m for m in json.loads((root/'catalog.json').read_text())['assets']};self.prices={};self.caps=collections.defaultdict(dict)
  self.rank_cache={}
  self.policy=json.loads((ROOT/'research/portfolio_policy.json').read_text())
  for a,m in self.meta.items():
   rows=valid_rows(a,json.loads((root/(a+'.json')).read_text()));self.prices[a]={d:p for d,p,c in rows}
   if m['included'] and a not in self.policy['quarantined']:
    for d,p,c in rows:
     if c is not None and math.isfinite(c) and c>0:self.caps[d][a]=c
 def rank(self,signal,n):
  if (signal,n) in self.rank_cache:return self.rank_cache[signal,n]
  assets=[a for a in self.caps[signal] if all(a in self.caps[d] for d in range(signal-29,signal+1))]
  result=sorted(assets,key=lambda a:(-self.caps[signal][a],a))[:n];self.rank_cache[signal,n]=result;return result
def rebalance(holdings,cash,prices,weights,fee):
 """Solve post-cost holdings and cash without borrowing or dropping old holdings."""
 values={a:q*prices[a] for a,q in holdings.items()};before=cash+sum(values.values());assets=set(values)|set(weights)
 def notional(v):return sum(abs(v*weights.get(a,0)-values.get(a,0)) for a in assets)
 lo,hi=0.,before
 for _ in range(64):
  mid=(lo+hi)/2
  if mid+fee*notional(mid)>before:hi=mid
  else:lo=mid
 after=(lo+hi)/2;traded=notional(after);cost=fee*traded
 new={a:after*w/prices[a] for a,w in weights.items() if w>0};cash=after*(1-sum(weights.values()))
 assert math.isclose(sum(new[a]*prices[a] for a in new)+cash+cost,before,rel_tol=1e-10,abs_tol=1e-12)
 return new,cash,cost,traded,before

def basket_id(n,weighting,rank_start):return f'top{n}_{weighting}' if rank_start==1 else f'top{rank_start}_{rank_start+n-1}_{weighting}'
def basket_name(n,weighting,rank_start):
 label=f'Top {n}' if rank_start==1 else f'Top {rank_start}–{rank_start+n-1}'
 return label+' · '+('equal weighted' if weighting=='equal' else 'cap weighted')
def simulate(source,n,weighting,bps,launch=None,rank_start=1,exclude_assets=None,rebalance_days=30):
 policy=source.policy;start=launch if launch is not None else day(policy['signal_start'])+1;end=day(policy['cutoff']);fee=bps/10000;holdings={};cash=1.;paths=[];ledger=[];contrib=collections.defaultdict(float);last_prices={};total_fees=0.;turnover=0.;unknown=[]
 exclude_assets=set(exclude_assets or [])
 for d in range(start,end+1):
  missing=[a for a in holdings if d not in source.prices[a]]
  # Attribute price P&L before executing today's trades. Missing marks do not erase units.
  for a,q in holdings.items():
   if d in source.prices[a]:
    p=source.prices[a][d]
    if a in last_prices:contrib[a]+=q*(p-last_prices[a])
    last_prices[a]=p
  if d==start or (rebalance_days and (d-start)%rebalance_days==0):
   signal=d-1;needed=rank_start+n-1+len(exclude_assets);ranked=[a for a in source.rank(signal,needed) if a not in exclude_assets][rank_start-1:rank_start-1+n];assert len(ranked)==n,(date(d),len(ranked),n,rank_start)
   capsum=sum(source.caps[signal][a] for a in ranked);target={a:(1/n if weighting=='equal' else source.caps[signal][a]/capsum) for a in ranked};failed=[a for a in target if d not in source.prices[a]]
   if not missing:
    weights={a:w for a,w in target.items() if a not in failed};prices={a:source.prices[a][d] for a in set(holdings)|set(weights)}
    holdings,cash,cost,traded,before=rebalance(holdings,cash,prices,weights,fee);total_fees+=cost
    if d>start:turnover+=.5*traded/before
    last_prices={a:source.prices[a][d] for a in holdings}
    ledger.append(dict(signal_day=signal,execution_day=d,selected=ranked,weights=target,failed_execution=failed,skipped=False,cost=cost,turnover_two_sided=traded/before,cash_weight=cash/(before-cost)))
   else:ledger.append(dict(signal_day=signal,execution_day=d,selected=ranked,skipped=True,missing=missing))
  nav=None if missing else cash+sum(q*source.prices[a][d] for a,q in holdings.items());btc=source.prices['btc'][d]/source.prices['btc'][start]/(1+fee)
  paths.append([d,nav,btc,None if nav is None else nav/btc])
  if nav is None:unknown.append(d)
 assert not unknown,('Unresolved holding marks; do not publish continuous path',unknown[:5])
 assert math.isclose(sum(contrib.values())-total_fees,paths[-1][1]-1,abs_tol=1e-9)
 peak=0.;mdd=0.
 for d,nav,b,r in paths:peak=max(peak,nav);mdd=min(mdd,nav/peak-1)
 yearspan=(end-start)/365.25;byday={x[0]:x for x in paths};rolling=[]
 for y in range(1,6):
  vals=[]
  for d,nav,b,r in paths:
   e=anniversary(d,y)
   if e in byday:vals.append(byday[e][3]/r)
  rolling.append(dict(years=y,observed=len(vals),wins=sum(x>1 for x in vals),win_rate=sum(x>1 for x in vals)/len(vals) if vals else None,median_relative=statistics.median(vals) if vals else None))
 return dict(id=basket_id(n,weighting,rank_start),name=basket_name(n,weighting,rank_start),rank_start=rank_start,rank_end=rank_start+n-1,bps=bps,start=date(start),end=date(end),end_wealth=paths[-1][1],end_relative=paths[-1][3],max_drawdown_usd=mdd,annual_one_way_turnover=turnover/yearspan,cost_dollars_per_initial_dollar=total_fees,path=paths,rolling=rolling,contributions=sorted([dict(asset=a,pnl=v) for a,v in contrib.items()],key=lambda x:x['pnl'],reverse=True),ledger=ledger)

def write_csv(name,rows):
 with (ROOT/'dist'/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
def build():
 source=SnapshotAdapter(D);runs=[simulate(source,n,w,c,rank_start=rank_start) for c in source.policy['cost_bps'] for n,w,rank_start in BASKETS]
 # Exact signal history, not inception weights reused through time.
 membership=[]
 for run in runs:
  if run['bps']!=0:continue
  for event in run['ledger']:
   for rank,a in enumerate(event['selected'],run['rank_start']):membership.append(dict(portfolio=run['id'],signal_date=date(event['signal_day']),execution_date=date(event['execution_day']),rank=rank,asset=a,name=source.meta[a]['name'],signal_cap=source.caps[event['signal_day']][a],target_weight=event['weights'][a],execution_price=source.prices[a].get(event['execution_day']),failed_execution=a in event.get('failed_execution',[])))
 write_csv('portfolio_membership.csv',membership)
 excluded=[dict(asset=a,name=m['name'],reason=source.policy['quarantined'].get(a,m['exclusion'])) for a,m in source.meta.items() if not m['included'] or a in source.policy['quarantined']]
 write_csv('portfolio_exclusions.csv',excluded)
 navrows=[dict(portfolio=r['id'],cost_bps=r['bps'],date=date(d),wealth=nav,btc_wealth=btc,wealth_vs_btc=rel) for r in runs for d,nav,btc,rel in r['path']];write_csv('portfolio_daily.csv',navrows)
 summary=[{k:v for k,v in r.items() if k not in ['path','rolling','ledger','contributions']} for r in runs];write_csv('portfolio_summary.csv',summary)
 write_csv('portfolio_rolling.csv',[dict(portfolio=r['id'],cost_bps=r['bps'],**x) for r in runs for x in r['rolling']])
 write_csv('portfolio_contributions.csv',[dict(portfolio=r['id'],cost_bps=r['bps'],**x) for r in runs for x in r['contributions']])
 for r in runs:r.pop('ledger')
 fingerprint=hashlib.sha256()
 for path in [D/'catalog.json',D/'quality.json',ROOT/'research/portfolio_policy.json']+[D/(a+'.json') for a in sorted(source.meta)]:fingerprint.update(path.name.encode());fingerprint.update(path.read_bytes())
 output=dict(input_sha256=fingerprint.hexdigest(),scope='restricted_universe',policy=source.policy,universe_count=sum(m['included'] and a not in source.policy['quarantined'] for a,m in source.meta.items()),runs=runs)
 (D/'portfolios.json').write_text(json.dumps(output,separators=(',',':'),allow_nan=False))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':build()
