"""Independent checks for calendar anniversaries, unknown exits and normalization."""
import json,datetime,math,statistics
from pathlib import Path
from snapshot_quality import valid_rows
D=Path(__file__).resolve().parents[1]/'dist/data';E=datetime.date(1970,1,1);CUT=20740
prices=lambda a:{d:p for d,p,_ in valid_rows(a,json.loads((D/(a+'.json')).read_text()))}
btc=prices('btc')
def end(d,y):
 t=E+datetime.timedelta(days=d)
 try:t=t.replace(year=t.year+y)
 except ValueError:t=t.replace(year=t.year+y,day=28)
 return (t-E).days
assert E+datetime.timedelta(days=end((datetime.date(2016,2,29)-E).days,1))==datetime.date(2017,2,28)
for asset in ['near','eth','anc','meme','soon','data']:
 p=prices(asset)
 for y in [1,4]:
  result=next(r for r in json.loads((D/f'rolling/{y}y.json').read_text()) if r['id']==asset);w=o=u=i=0
  for d in p:
   if d not in btc:continue
   e=end(d,y)
   if e>CUT:i+=1
   elif e not in p or e not in btc:u+=1
   else:o+=1;w+=(p[e]/p[d])/(btc[e]/btc[d])>1
  assert (w,o,u,i)==(result['wins'],result['observed'],result['unknown'],result['immature']),(asset,y)
r=next(x for x in json.loads((D/'overview.json').read_text()) if x['id']=='meme');assert r['entry']==19664 and r['multiple']<1
part=json.loads((D/'participation.json').read_text())
for r in [x for x in part['examples'] if x['base']=='eth']:
 assert math.isclose(r['active_hold']-r['active_before_drop'],r['allocation']*r['airdrop_terminal_price'],rel_tol=1e-10)
 assert r['capital']==9500+400+100
for y in [1,2,3,4,5]:
 for r in json.loads((D/f'rolling/{y}y.json').read_text()):
  lengths={s:sum(b-a+1 for a,b,k in r['runs'] if k==s) for s in ['win','loss','unknown']}
  assert lengths['win']==r['wins'] and lengths['win']+lengths['loss']==r['observed'] and lengths['unknown']==r['unknown']
print('PASS: independent exact-price rolling outcomes, calendar leap handling, ceased histories as unknown, MEME valid start, reward cash-flow arithmetic, and entry-strip counts.')
