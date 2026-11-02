"""Frozen-source explorer and observed-age summaries. No price interpolation."""
import json,datetime,csv,math
from pathlib import Path
from snapshot_quality import valid_rows
R=Path(__file__).resolve().parents[1];D=R/'dist/data';CUT=20740;E=datetime.date(1970,1,1)
def q(v,p):
 v=sorted(v)
 if not v:return None
 x=(len(v)-1)*p;i=int(x);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(x-i)
def year(d):return (E+datetime.timedelta(days=d)).year
cat=json.loads((D/'catalog.json').read_text())['assets'];btc={d:p for d,p,c in json.loads((D/'btc.json').read_text())};cg={d:p for d,p,c in json.loads((D/'btc-coingecko.json').read_text())};entries=[];bycohort={};fixed=set()
for y in [1,2,3,4,5]:
 t=E+datetime.timedelta(days=CUT)
 try:s=t.replace(year=t.year-y)
 except ValueError:s=t.replace(year=t.year-y,day=28)
 fixed.add((s-E).days)
for m in cat:
 if m['id']=='btc':continue
 bm=cg if m['source'].startswith('CoinGecko') else btc
 rows=[r for r in valid_rows(m['id'],json.loads((D/(m['id']+'.json')).read_text())) if r[0]<=CUT and r[0] in bm]
 if not rows:continue
 first,last=rows[0][0],rows[-1][0];ratios={d:p/bm[d] for d,p,c in rows};base=ratios[first];cross={}
 for cap in [1e7,1e8,1e9,1e10]:
  z=next((d for d,p,c in rows if c is not None and math.isfinite(c) and c>=cap),None)
  cross[str(int(cap))]=z
 special=fixed|{last}|{x for x in cross.values() if x is not None};points=[[d,ratios[d]/base] for i,(d,p,c) in enumerate(rows) if i%7==0 or d in special]
 entries.append(dict(id=m['id'],first=first,last=last,n=len(rows),vintage=year(first),age_at_cutoff=(CUT-first)/365.25,crossings=cross,points=points))
 if m['included']:
  bycohort[m['id']]=(first,ratios,base,year(first))
cohorts={}
for v in ['all']+[str(x) for x in sorted({a[3] for a in bycohort.values()})]:
 selected=[a for a in bycohort.values() if v=='all' or str(a[3])==v];records=[]
 for age in list(range(0,3651,30))+[3652]:
  vals=[ratio[first+age]/base for first,ratio,base,y in selected if first+age<=CUT and first+age in ratio];elapsed=sum(first+age<=CUT for first,ratio,base,y in selected)
  records.append(dict(age_days=age,n=len(vals),elapsed=elapsed,missing=elapsed-len(vals),q25=q(vals,.25),median=q(vals,.5),q75=q(vals,.75)))
 cohorts[v]=dict(coins=len(selected),points=records)
(D/'explorer.json').write_text(json.dumps(entries,separators=(',',':'),allow_nan=False));(D/'age_summary.json').write_text(json.dumps(dict(cutoff='2026-10-14',universe=len(bycohort),step_days=30,cohorts=cohorts),separators=(',',':'),allow_nan=False))
with (R/'dist/age_summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['first_observed_year','age_days','n','elapsed','missing','q25','median','q75']);w.writeheader();w.writerows(dict(first_observed_year=v,**x) for v,z in cohorts.items() for x in z['points'])
print('Explorer:',len(entries),'histories; observed-age sample:',len(bycohort),'coins; exact observations only.')
# Reader-facing headline and frequency-quartile export, separate from raw rolling output.
summary=json.loads((D/'rolling/summary.json').read_text());headlines=[]
for y in [1,2,3,4,5]:
 records=json.loads((D/f'rolling/{y}y.json').read_text())
 for cohort in ['available','common']:
  ids=set(next(x for x in summary['summary'] if x['years']==y and x['cohort']==cohort)['coin_ids']);group=[x for x in records if x['id'] in ids];priced=[x for x in group if x['observed']];rates=[x['win_rate'] for x in priced]
  typical=[x['median_multiple'] for x in priced];winner_typical=[x['median_winning_multiple'] for x in priced if x['median_winning_multiple'] is not None]
  headlines.append(dict(years=y,cohort=cohort,eligible=len(group),priced=len(priced),ever_winner_pct=100*sum(x['wins']>0 for x in group)/len(group) if group else None,majority_winner_pct=100*sum(x['win_rate']>.5 for x in priced)/len(priced) if priced else None,median_coin_multiple=q(typical,.5),median_ever_winner_multiple=q(winner_typical,.5),win_frequency_q25=q(rates,.25),win_frequency_median=q(rates,.5),win_frequency_q75=q(rates,.75)))
with (R/'dist/paper_summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(headlines[0]),lineterminator='\n');w.writeheader();w.writerows(headlines)
