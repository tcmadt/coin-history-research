"""Check age statistics and explorer endpoints against original daily quotes."""
import json,math,statistics
from pathlib import Path
from snapshot_quality import valid_rows
D=Path(__file__).resolve().parents[1]/'dist/data';btc={d:p for d,p,c in json.loads((D/'btc.json').read_text())};cat=json.loads((D/'catalog.json').read_text())['assets'];expl={x['id']:x for x in json.loads((D/'explorer.json').read_text())};age=json.loads((D/'age_summary.json').read_text())
def q(v,p):
 v=sorted(v)
 if not v:return None
 # Independent weighted-order-statistic formula.
 x=(len(v)-1)*p;l=int(x);h=min(l+1,len(v)-1)
 return v[l]*(h-x)+v[h]*(x-l) if h!=l else v[l]
for offset in [0,360,1080,1830,3652]:
 values=[];elapsed=0
 for m in cat:
  if not m['included']:continue
  rows=valid_rows(m['id'],json.loads((D/(m['id']+'.json')).read_text()));ratio={d:p/btc[d] for d,p,c in rows if d in btc and d<=20740};first=min(ratio);end=first+offset;elapsed+=end<=20740
  if end in ratio:values.append(ratio[end]/ratio[first])
 result=next(x for x in age['cohorts']['all']['points'] if x['age_days']==offset)
 assert result['n']==len(values) and result['elapsed']==elapsed
 for k,p in [('q25',.25),('median',.5),('q75',.75)]:assert math.isclose(result[k],q(values,p),rel_tol=1e-12,abs_tol=1e-12)
for a in ['eth','near','meme','soon','data']:
 e=expl[a];rows=[r for r in valid_rows(a,json.loads((D/(a+'.json')).read_text())) if r[0] in btc];ratio={d:p/btc[d] for d,p,c in rows};points=dict(e['points'])
 for t,cross in e['crossings'].items():
  actual=next((d for d,p,c in rows if c is not None and c>=int(t)),None);assert cross==actual
  if cross is not None:assert cross in points and math.isclose(points[cross],ratio[cross]/ratio[e['first']],rel_tol=1e-12)
 assert e['first'] in points and e['last'] in points
assert all(x['q25']<=x['median']<=x['q75'] for g in age['cohorts'].values() for x in g['points'] if x['n'])
print('PASS: independently recomputed age quartiles and counts; exact threshold-touch endpoints; retained source gaps; percentile order.')
