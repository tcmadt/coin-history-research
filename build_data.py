from pathlib import Path
import pandas as pd,json,shutil
ROOT=Path(__file__).resolve().parents[2];SITE=Path(__file__).parent;DIST=SITE/'dist';DATA=DIST/'data';DATA.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(ROOT/'output/daily_market_data.csv.gz',parse_dates=['date']);names={x['asset']:x['full_name'] for x in json.loads((ROOT/'work/raw/asset-catalog.json').read_text())['data']}
ledger=pd.read_csv(ROOT/'output/universe.csv').set_index('asset').to_dict('index'); epoch=pd.Timestamp('1970-01-01');catalog=[]
for asset,g in df.groupby('asset'):
 g=g.dropna(subset=['PriceUSD']).sort_values('date');g=g[g.PriceUSD>0]
 if g.empty:continue
 rows=[[int((r.date-epoch).days),float(f'{r.PriceUSD:.12g}'),None if pd.isna(r.CapMrktEstUSD) else float(f'{r.CapMrktEstUSD:.12g}')] for r in g.itertuples()]
 (DATA/f'{asset}.json').write_text(json.dumps(rows,separators=(',',':'),allow_nan=False))
 item=ledger.get(asset,{});catalog.append({'id':asset,'name':names.get(asset,asset),'first':rows[0][0],'last':rows[-1][0],'n':len(rows),'cap':next((r[2] for r in reversed(rows) if r[2]),None),'included':bool(item.get('included',False)),'exclusion':item.get('reason',''),'source':'Coin Metrics'})
# Retain older price-only source histories absent from the circulating-cap catalog.
for asset in ['maid']:
 p=ROOT/f'work/raw/extra-{asset}.json'
 if not p.exists():continue
 z=[r for r in json.loads(p.read_text()) if r.get('PriceUSD') and float(r['PriceUSD'])>0];z.sort(key=lambda x:x['time']);rows=[[int((pd.Timestamp(r['time'][:10])-epoch).days),float(r['PriceUSD']),None] for r in z if r['time'][:10]<='2026-10-14']
 (DATA/f'{asset}.json').write_text(json.dumps(rows,separators=(',',':')));catalog.append({'id':asset,'name':'MaidSafeCoin (legacy)','first':rows[0][0],'last':rows[-1][0],'n':len(rows),'cap':None,'included':False,'exclusion':'Legacy history ends before study cutoff; not assumed worthless.','source':'Coin Metrics'})
# Separate young-token midnight series; never silently blend with CM daily-close series.
for slug,asset,name in [('pons','pons','Pons'),('stonk-3','stonk','STONK (StonkFun)')]:
 z=json.loads((ROOT/f'work/raw/cg-{slug}.json').read_text());cap={int(t//86400000):v for t,v in z['market_caps']};rows=[[int(t//86400000),p,cap.get(int(t//86400000))] for t,p in z['prices'] if t%86400000==0 and int(t//86400000)<=int((pd.Timestamp('2026-10-14')-epoch).days)]
 (DATA/f'{asset}.json').write_text(json.dumps(rows,separators=(',',':')));catalog.append({'id':asset,'name':name,'first':rows[0][0],'last':rows[-1][0],'n':len(rows),'cap':rows[-1][2],'included':False,'exclusion':'Young case study. CoinGecko midnight observations use a separately matched BTC series.','source':'CoinGecko (00:00 UTC)'})
bz=json.loads((ROOT/'work/raw/probe-cg.json').read_text());(DATA/'btc-coingecko.json').write_text(json.dumps([[int(t//86400000),p,None] for t,p in bz['prices'] if t%86400000==0],separators=(',',':')))
catalog.sort(key=lambda x:x['name'].lower());(DATA/'catalog.json').write_text(json.dumps({'cutoff':'2026-10-14','assets':catalog},separators=(',',':')))
study=json.loads((ROOT/'output/study_data.json').read_text());(DATA/'study.json').write_text(json.dumps({k:study[k] for k in ['cutoff','summary','threshold_results','original','spotlight']},separators=(',',':')))
for f in ['methodology.md','threshold_results.csv','universe.csv','cohort_summary.csv','observed_crossing_sensitivity.csv']:
 shutil.copy2(ROOT/'output'/f,DIST/f)
(DIST/'figures').mkdir(exist_ok=True)
for p in (ROOT/'output').glob('0[1-5]_*.png'):shutil.copy2(p,DIST/'figures'/p.name)
print('Built',len(catalog),'asset histories;',sum(p.stat().st_size for p in DATA.glob('*.json')),'JSON bytes')
