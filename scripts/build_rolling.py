"""Every available daily entry; exact calendar-year matched exits; frozen prices."""
import json,datetime,statistics,csv,os
from snapshot_quality import valid_rows
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'dist/data';OUT=D/('rolling-raw' if os.environ.get('SNAPSHOT_RAW')=='1' else 'rolling');OUT.mkdir(exist_ok=True)
E=datetime.date(1970,1,1);CUT=20740;YEARS=[1,2,3,4,5]
def ds(n):return str(E+datetime.timedelta(days=n))
def anniv(n,y):
 d=E+datetime.timedelta(days=n)
 try:return (d.replace(year=d.year+y)-E).days
 except ValueError:return (d.replace(year=d.year+y,day=28)-E).days
catalog=json.loads((D/'catalog.json').read_text())['assets'];btc={d:p for d,p,_ in json.loads((D/'btc.json').read_text())};dategrid={y:{d:anniv(d,y) for d in range(min(btc),CUT+1)} for y in YEARS}
assets=[m for m in catalog if m['included']];byyear={y:[] for y in YEARS}
for m in assets:
 rows=valid_rows(m['id'],json.loads((D/(m['id']+'.json')).read_text()));ratio={d:p/btc[d] for d,p,_ in rows if d in btc};entries=sorted(ratio)
 for y in YEARS:
  wins=observed=unknown=immature=0;runs=[];multiples=[];winning_multiples=[];first_win=last_win=None;best=None;first=None;last=None
  for start in entries:
   end=dategrid[y][start]
   if end>CUT:immature+=1;continue
   first=start if first is None else first;last=start
   if end not in ratio:unknown+=1;status='unknown'
   else:
    observed+=1;multiple=ratio[end]/ratio[start];multiples.append(multiple);win=multiple>1;wins+=win;status='win' if win else 'loss';best=max(best or multiple,multiple)
    if win:winning_multiples.append(multiple)
    if win:first_win=start if first_win is None else first_win;last_win=start
   if runs and runs[-1][2]==status and runs[-1][1]+1==start:runs[-1][1]=start
   else:runs.append([start,start,status])
  byyear[y].append(dict(id=m['id'],name=m['name'],observed=observed,wins=wins,unknown=unknown,immature=immature,matured=observed+unknown,win_rate=wins/observed if observed else None,lower=wins/(observed+unknown) if observed+unknown else None,upper=(wins+unknown)/(observed+unknown) if observed+unknown else None,median_multiple=statistics.median(multiples) if multiples else None,median_winning_multiple=statistics.median(winning_multiples) if winning_multiples else None,first=first,last=last,first_win=first_win,last_win=last_win,best_multiple=best,runs=runs))
common={r['id'] for r in byyear[max(YEARS)] if r['observed']>0}
summary=[]
for y,records in byyear.items():
 for cohort in ['available','common']:
  z=[r for r in records if cohort=='available' or r['id'] in common];eligible=[r for r in z if r['matured']];priced=[r for r in eligible if r['observed']];ever=sum(r['wins']>0 for r in eligible);uncertain=sum(r['wins']==0 and r['unknown']>0 for r in eligible)
  rates=[r['win_rate'] for r in priced];typical=[r['median_multiple'] for r in priced];winner_typical=[r['median_winning_multiple'] for r in priced if r['median_winning_multiple'] is not None];summary.append(dict(years=y,cohort=cohort,eligible=len(eligible),priced=len(priced),ever_wins=ever,ever_unknown=uncertain,ever_lower=ever/len(eligible) if eligible else None,ever_upper=(ever+uncertain)/len(eligible) if eligible else None,median_win_rate=statistics.median(rates) if rates else None,median_coin_multiple=statistics.median(typical) if typical else None,median_ever_winner_multiple=statistics.median(winner_typical) if winner_typical else None,median_lower=statistics.median([r['lower'] for r in eligible]) if eligible else None,median_upper=statistics.median([r['upper'] for r in eligible]) if eligible else None,mean_coin_win_rate=statistics.mean(rates) if rates else None,known_windows=sum(r['observed'] for r in eligible),unknown_windows=sum(r['unknown'] for r in eligible),immature_windows=sum(r['immature'] for r in z),coin_ids=[r['id'] for r in eligible]))
 (OUT/f'{y}y.json').write_text(json.dumps(records,separators=(',',':')))
(OUT/'summary.json').write_text(json.dumps(dict(cutoff=ds(CUT),universe=len(assets),common_ids=sorted(common),summary=summary),separators=(',',':')))
flat=[dict(years=y,**{k:v for k,v in r.items() if k!='runs'}) for y,records in byyear.items() for r in records]
with (R/('dist/rolling_coin_results_raw.csv' if os.environ.get('SNAPSHOT_RAW')=='1' else 'dist/rolling_coin_results.csv')).open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator="\n");w.writeheader();w.writerows(flat)
with (R/('dist/rolling_summary_raw.csv' if os.environ.get('SNAPSHOT_RAW')=='1' else 'dist/rolling_summary.csv')).open('w',newline='') as f:
 keys=[k for k in summary[0] if k!='coin_ids'];w=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");w.writeheader();w.writerows([{k:r[k] for k in keys} for r in summary])
for r in summary:
 if r['cohort']=='available':print(r['years'],'years:',r['ever_wins'],'known winners /',r['eligible'],'eligible coins;',r['ever_unknown'],'uncertain; median',r['median_win_rate'])
print('Same-coin cohort:',len(common),'assets; source universe',len(assets))
