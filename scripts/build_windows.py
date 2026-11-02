"""Small, exact-endpoint chart bundles for the six paper windows."""
import json,datetime
from snapshot_quality import valid_rows
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist/data';W=D/'windows';W.mkdir(exist_ok=True)
c=json.loads((D/'catalog.json').read_text())['assets'];end=datetime.date(2026,10,14);epoch=datetime.date(1970,1,1);e=(end-epoch).days
btc={d:p for d,p,_ in json.loads((D/'btc.json').read_text())};cg={d:p for d,p,_ in json.loads((D/'btc-coingecko.json').read_text())}
for years in [1,2,3,4,5,10]:
 start=(end.replace(year=end.year-years)-epoch).days;out=[]
 for m in c:
  if m['id']=='btc' or m['first']>start or m['last']<e:continue
  bm=cg if m['source'].startswith('CoinGecko') else btc
  rows=[r for r in valid_rows(m['id'],json.loads((D/(m['id']+'.json')).read_text())) if start<=r[0]<=e and r[0] in bm]
  if not rows or rows[0][0]!=start or rows[-1][0]!=e:continue
  initial=rows[0][1]/bm[start];points=[[d,(p/bm[d])/initial] for i,(d,p,_) in enumerate(rows) if i%7==0 or i==len(rows)-1]
  out.append(dict(id=m['id'],entry=start,end=e,n=len(rows),multiple=points[-1][1],points=points))
 (W/f'{years}y.json').write_text(json.dumps(out,separators=(',',':')));print(years,len(out))
