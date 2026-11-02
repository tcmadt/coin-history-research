"""Build reader-facing extensions: dilution, categories, yield, and breadth."""
import bisect, csv, datetime as dt, json, math, statistics
from pathlib import Path
from snapshot_quality import valid_rows

R=Path(__file__).resolve().parents[1]; D=R/'dist/data'; E=dt.date(1970,1,1); CUT=20740
CAT=json.loads((D/'catalog.json').read_text())['assets']
META={x['id']:x for x in CAT}; INCLUDED=[x for x in CAT if x['included'] and x['id']!='btc']
BTC={d:(p,c) for d,p,c in json.loads((D/'btc.json').read_text())}
CG={d:(p,c) for d,p,c in json.loads((D/'btc-coingecko.json').read_text())}

def add_years(day, years):
    x=E+dt.timedelta(days=day)
    try: y=x.replace(year=x.year+years)
    except ValueError: y=x.replace(year=x.year+years,day=28)
    return (y-E).days
def med(xs): return statistics.median(xs) if xs else None
def mean(xs): return statistics.mean(xs) if xs else None
def ranks(xs):
    order=sorted(range(len(xs)),key=xs.__getitem__); out=[0.0]*len(xs); i=0
    while i<len(order):
        j=i+1
        while j<len(order) and xs[order[j]]==xs[order[i]]: j+=1
        r=(i+j-1)/2+1
        for k in order[i:j]: out[k]=r
        i=j
    return out
def corr(a,b):
    if len(a)<2:return None
    ra,rb=ranks(a),ranks(b); ma,mb=mean(ra),mean(rb)
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); den=math.sqrt(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))
    return num/den if den else None
def write_csv(name, rows, fields=None):
    if not rows:return
    fields=fields or list(rows[0]);
    with (R/'dist'/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)

series={}; benchmarks={}
for m in INCLUDED:
    rows=[r for r in valid_rows(m['id'],json.loads((D/(m['id']+'.json')).read_text())) if r[0]<=CUT]
    series[m['id']]={d:(p,c) for d,p,c in rows if p and p>0}
    benchmarks[m['id']]=CG if m['source'].startswith('CoinGecko') else BTC

# Same coins and same start dates across all five holding periods.
rolling_summary=json.loads((D/'rolling/summary.json').read_text())['summary']
COMMON=set(next(x for x in rolling_summary if x['years']==5 and x['cohort']=='common')['coin_ids'])
common_start_by_h={h:[] for h in range(1,6)}
for cid in COMMON:
    rows=series[cid]; bm=benchmarks[cid]; vals={h:[] for h in range(1,6)}
    for d,(p,c) in rows.items():
        ends={h:add_years(d,h) for h in range(1,6)}
        if ends[5]>CUT or d not in bm or any(ends[h] not in rows or ends[h] not in bm for h in range(1,6)): continue
        for h,x in ends.items(): vals[h].append((rows[x][0]/p)/(bm[x][0]/bm[d][0]))
    if vals[5]:
        for h in range(1,6): common_start_by_h[h].append(dict(coin_id=cid,windows=len(vals[h]),wins=sum(x>1 for x in vals[h]),win_rate=sum(x>1 for x in vals[h])/len(vals[h]),median_multiple=med(vals[h])))
common_start_summary=[]
for h,z in common_start_by_h.items():
    common_start_summary.append(dict(horizon_years=h,coins=len(z),windows=sum(x['windows'] for x in z),ever_winners=sum(x['wins']>0 for x in z),ever_winner_pct=100*sum(x['wins']>0 for x in z)/len(z),reliable_winners=sum(x['win_rate']>.5 for x in z),reliable_winner_pct=100*sum(x['win_rate']>.5 for x in z)/len(z),median_coin_multiple=med([x['median_multiple'] for x in z])))
write_csv('common_start_horizons.csv',common_start_summary)

# Five-year missing-exit sensitivity on the fixed cohort.
missing_rows=[]
for treatment in ('observed_only','freeze_last_relative','zero'):
    coin_stats=[]; observed=missing=0
    for cid in COMMON:
        rows=series[cid]; bm=benchmarks[cid]; dates=sorted(d for d in rows if d in bm); vals=[]; wins=0; n=0
        for d in dates:
            x=add_years(d,5)
            if x>CUT or x not in bm: continue
            n+=1
            if x in rows:
                multiple=(rows[x][0]/rows[d][0])/(bm[x][0]/bm[d][0]); observed+=1
            else:
                missing+=1
                if treatment=='observed_only': continue
                if treatment=='zero': multiple=0.0
                else:
                    i=bisect.bisect_right(dates,x)-1
                    if i<0 or dates[i]<=d: continue
                    last=dates[i]; multiple=(rows[last][0]/rows[d][0])/(bm[last][0]/bm[d][0])
            vals.append(multiple); wins+=multiple>1
        if vals: coin_stats.append(dict(median=med(vals),win_rate=wins/len(vals),ever=wins>0))
    missing_rows.append(dict(treatment=treatment,coins=len(coin_stats),observed_windows=observed,missing_windows=missing,median_coin_multiple=med([x['median'] for x in coin_stats]),ever_winner_pct=100*sum(x['ever'] for x in coin_stats)/len(coin_stats),reliable_winner_pct=100*sum(x['win_rate']>.5 for x in coin_stats)/len(coin_stats)))
write_csv('five_year_missing_sensitivity.csv',missing_rows)

# Exact price/market-cap/supply decomposition at 1, 3, and 5 years.
decomp=[]
for cid,rows in series.items():
    bm=benchmarks[cid]
    for h in (1,3,5):
        vals=[]
        for d,(p,c) in rows.items():
            x=add_years(d,h)
            if x>CUT or x not in rows or d not in bm or x not in bm:continue
            p1,c1=rows[x]; bp0,bc0=bm[d]; bp1,bc1=bm[x]
            if not all(v and v>0 and math.isfinite(v) for v in (p,c,p1,c1,bp0,bc0,bp1,bc1)):continue
            price=(p1/p)/(bp1/bp0); cap=(c1/c)/(bc1/bc0); supply=(c1/p1)/(c/p); btc_supply=(bc1/bp1)/(bc0/bp0)
            vals.append((math.log(price),math.log(cap),math.log(supply/btc_supply)))
        if vals:
            decomp.append(dict(coin_id=cid,horizon_years=h,windows=len(vals),mean_log_price_vs_btc=mean([x[0] for x in vals]),mean_log_cap_vs_btc=mean([x[1] for x in vals]),mean_log_relative_supply_growth=mean([x[2] for x in vals]),median_price_vs_btc=math.exp(med([x[0] for x in vals])),median_cap_vs_btc=math.exp(med([x[1] for x in vals])),median_relative_supply_growth=math.exp(med([x[2] for x in vals]))))
write_csv('supply_decomposition.csv',decomp)

decomp_summary=[]
for h in (1,3,5):
    z=[x for x in decomp if x['horizon_years']==h]; pl=[x['mean_log_price_vs_btc'] for x in z]; cl=[x['mean_log_cap_vs_btc'] for x in z]; dl=[x['mean_log_relative_supply_growth'] for x in z]
    mp,mc,md=mean(pl),mean(cl),mean(dl)
    decomp_summary.append(dict(horizon_years=h,coins=len(z),median_price_vs_btc=med([x['median_price_vs_btc'] for x in z]),median_cap_vs_btc=med([x['median_cap_vs_btc'] for x in z]),median_relative_supply_growth=med([x['median_relative_supply_growth'] for x in z]),mean_log_price_vs_btc=mp,mean_log_cap_vs_btc=mc,mean_log_relative_supply_growth=md,dilution_share=(md/-mp if mp and mp<0 else None),cap_grew_but_price_lost=sum(x['mean_log_cap_vs_btc']>0 and x['mean_log_price_vs_btc']<=0 for x in z),cap_grew=sum(x['mean_log_cap_vs_btc']>0 for x in z)))

# Monthly trailing-dilution signal and forward two-year outcome.
signal=[]; cur=dt.date(2020,7,1)
while cur<=dt.date(2024,10,1):
    d=(cur-E).days; prior=(cur.replace(year=cur.year-1)-E).days; future=(cur.replace(year=cur.year+2)-E).days; obs=[]
    for cid,rows in series.items():
        bm=benchmarks[cid]
        if d not in rows or future not in rows or d not in bm or future not in bm:continue
        q=next((rows[x] for x in range(prior,prior+4) if x in rows and rows[x][1] and rows[x][1]>0),None)
        p,c=rows[d]; pf,cf=rows[future]
        if not q or not c or c<=0 or not all(v and v>0 for v in (p,pf,bm[d][0],bm[future][0])):continue
        pp,pc=q; supply_now=c/p; supply_prior=pc/pp
        if supply_prior<=0:continue
        growth=supply_now/supply_prior-1; outcome=(pf/p)/(bm[future][0]/bm[d][0]); obs.append((growth,outcome))
    if len(obs)>=20:
        obs.sort(); k=max(1,len(obs)//5); lo=obs[:k]; hi=obs[-k:]
        signal.append(dict(month=cur.isoformat(),coins=len(obs),spearman_rho=corr([x[0] for x in obs],[x[1] for x in obs]),low_dilution_median_growth=med([x[0] for x in lo]),low_dilution_median_outcome=med([x[1] for x in lo]),low_dilution_win_rate=sum(x[1]>1 for x in lo)/len(lo),high_dilution_median_growth=med([x[0] for x in hi]),high_dilution_median_outcome=med([x[1] for x in hi]),high_dilution_win_rate=sum(x[1]>1 for x in hi)/len(hi)))
    cur=(cur.replace(day=28)+dt.timedelta(days=4)).replace(day=1)
write_csv('dilution_signal_monthly.csv',signal)

# Winner categories on fixed five-year cohort.
roll=json.loads((D/'rolling/5y.json').read_text()); common=set(next(x for x in json.loads((D/'rolling/summary.json').read_text())['summary'] if x['years']==5 and x['cohort']=='common')['coin_ids']); rr={x['id']:x for x in roll if x['id'] in common and x['observed']}
cats={
 'Exchange tokens':['bnb','okb','gt','mx','ht','cro','ftt','lcx','wrx','woo','qash','oax','leo','kcs','bgb','wbt','cet','bmx'],
 'Bitcoin forks':['bch','bsv','btg','bcd','xec'],
 'Would-be digital cash':['ltc','dash','xmr','zec','nano','dgb','dcr','grin','xvg','rvn']}
catrows=[]
for name,ids in cats.items():
    z=[rr[x] for x in ids if x in rr]; catrows.append(dict(category=name,priced=len(z),reliable_winners=sum(x['win_rate']>.5 for x in z),reliable_winner_pct=100*sum(x['win_rate']>.5 for x in z)/len(z) if z else None,median_coin_multiple=med([x['median_multiple'] for x in z])))
ex=set(cats['Exchange tokens']); z=[x for cid,x in rr.items() if cid not in ex]; catrows.insert(1,dict(category='All other coins',priced=len(z),reliable_winners=sum(x['win_rate']>.5 for x in z),reliable_winner_pct=100*sum(x['win_rate']>.5 for x in z)/len(z),median_coin_multiple=med([x['median_multiple'] for x in z])))
write_csv('winner_categories.csv',catrows)

# Yield steelman applied to every exact rolling window, then summarized coin by coin.
yieldrows=[]
for h in (1,5):
    common_h=set(next(x for x in json.loads((D/'rolling/summary.json').read_text())['summary'] if x['years']==h and x['cohort']==('common' if h==5 else 'available'))['coin_ids']); rec=[x for x in json.loads((D/f'rolling/{h}y.json').read_text()) if x['id'] in common_h and x['observed']]
    base=med([x['median_multiple'] for x in rec]);
    for y in (0,.10,.20):
        factor=(1+y)**h; reliable=0
        for cid in common_h:
            rows=series[cid]; bm=benchmarks[cid]; wins=n=0
            for d,(p,c) in rows.items():
                x=add_years(d,h)
                if x>CUT or x not in rows or d not in bm or x not in bm:continue
                multiple=(rows[x][0]/p)/(bm[x][0]/bm[d][0])*factor; wins+=multiple>1; n+=1
            reliable+=n>0 and wins/n>.5
        yieldrows.append(dict(horizon_years=h,added_yield_pct=100*y,coins=len(rec),median_coin_multiple=base*factor,reliable_winner_pct=100*reliable/len(rec),median_breakeven_yield_pct=100*(base**(-1/h)-1)))
write_csv('steelman_yield.csv',yieldrows)

# Trailing one-year altcoin breadth sampled every three days.
breadth=[]
start=(dt.date(2016,1,1)-E).days
for d in range(start,CUT+1,3):
    vals=[]
    for cid,rows in series.items():
        bm=benchmarks[cid]
        if d in rows and d-365 in rows and d in bm and d-365 in bm:
            vals.append((rows[d][0]/rows[d-365][0])/(bm[d][0]/bm[d-365][0]))
    if len(vals)>=15: breadth.append(dict(date=(E+dt.timedelta(days=d)).isoformat(),coins=len(vals),share_ahead_pct=100*sum(x>1 for x in vals)/len(vals)))
write_csv('altseason_breadth.csv',breadth)
annual=[]
for y in sorted({x['date'][:4] for x in breadth}):
    z=[x for x in breadth if x['date'].startswith(y)]; annual.append(max(z,key=lambda x:x['share_ahead_pct']))

fixed_breadth=[]
for d in range(start,CUT+1,3):
    vals=[]
    for cid in COMMON:
        rows=series[cid]; bm=benchmarks[cid]
        if d in rows and d-365 in rows and d in bm and d-365 in bm:
            vals.append((rows[d][0]/rows[d-365][0])/(bm[d][0]/bm[d-365][0]))
    if len(vals)>=15: fixed_breadth.append(dict(date=(E+dt.timedelta(days=d)).isoformat(),coins=len(vals),share_ahead_pct=100*sum(x>1 for x in vals)/len(vals)))
write_csv('altseason_breadth_fixed.csv',fixed_breadth)
fixed_annual=[]
for y in sorted({x['date'][:4] for x in fixed_breadth}):
    z=[x for x in fixed_breadth if x['date'].startswith(y)]; fixed_annual.append(max(z,key=lambda x:x['share_ahead_pct']))

out=dict(decomposition=decomp_summary,signal=dict(months=len(signal),average_coins=mean([x['coins'] for x in signal]),mean_rho=mean([x['spearman_rho'] for x in signal]),negative_months=sum(x['spearman_rho']<0 for x in signal),low_outcome=med([x['low_dilution_median_outcome'] for x in signal]),high_outcome=med([x['high_dilution_median_outcome'] for x in signal]),low_win_rate=med([x['low_dilution_win_rate'] for x in signal]),high_win_rate=med([x['high_dilution_win_rate'] for x in signal])),signal_monthly=signal,categories=catrows,yield_tests=yieldrows,common_start=common_start_summary,missing_sensitivity=missing_rows,annual_breadth=annual,breadth=breadth,fixed_annual_breadth=fixed_annual,fixed_breadth=fixed_breadth)
(D/'extensions.json').write_text(json.dumps(out,separators=(',',':'),allow_nan=False))
print(json.dumps(out,indent=2))
