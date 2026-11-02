"""Reconcile every modeled signal against the matching public CMC snapshot.
Never infer identity from a ticker when the normalized name disagrees.
"""
import json,csv,re,collections
from pathlib import Path
from build_portfolios import ROOT,D,SnapshotAdapter,day,date,write_csv
source=SnapshotAdapter(D)
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
ALIASES={1839:'bnb',3635:'cro',825:'usdt',3408:'usdc',4172:'luna',2416:'theta',37263:'cc',2239:'lend',5690:'rndr',6892:'egld',22974:'tao_bittensor',3718:'bttc',6536:'om'}
# Numeric IDs prevent historical Acash Coin/Storeum from becoming modern ACA/STO.
REJECT={4598:'Historical Acash Coin is not Acala',4162:'Historical Storeum is not StakeStone'}
STABLE_IDS={18579,825,3408,7129,4943,4687,2563,20935,29470,36148,33440,36380,33039,28081,33685}
rows=[];identities={};a=collections.Counter();reconciled=[]
for p in sorted((ROOT/'research/cmc_snapshots').glob('*.json')):
 snap=json.loads(p.read_text());signal=day(snap['date']);cm=source.rank(signal,20);cm10=cm[:10];candidates=[]
 for r in snap['records']:
  sym=r['symbol'].lower();name=r['name'];mapped=None;method='unmapped'
  if r['id'] in REJECT:method=REJECT[r['id']]
  elif r['id'] in ALIASES:mapped=ALIASES[r['id']];method='explicit CMC-ID alias'
  elif sym in source.meta and norm(name)==norm(source.meta[sym]['name']):mapped=sym;method='exact normalized name and ticker'
  meta=source.meta.get(mapped,{})
  pegged=(r['id'] in STABLE_IDS or meta.get('exclusion')=='pegged asset or underlying-asset receipt' or 'stablecoin' in r.get('tags',[]) or 'wrapped-tokens' in r.get('tags',[]))
  if r['id']==1 or sym=='btc' or pegged:continue
  candidates.append((r,mapped,method))
  identities[r['id']]=dict(cmc_id=r['id'],cmc_symbol=r['symbol'],cmc_name=name,cm_asset=mapped or '',mapping=method)
  if len(candidates)>=20:break
 unrepresented=[];excluded=[];quarantined=[]
 for rank,(r,mapped,method) in enumerate(candidates,1):
  if not mapped:reason='not mapped in frozen catalog';unrepresented.append(r['symbol'])
  elif not source.meta[mapped]['included']:reason=source.meta[mapped]['exclusion'];excluded.append(mapped)
  elif mapped in source.policy['quarantined']:reason='portfolio source-quality quarantine';quarantined.append(mapped)
  elif mapped not in source.caps[signal]:reason='no positive signal cap in CM';unrepresented.append(mapped)
  elif mapped not in cm:reason='different rank or 30-day eligibility under CM'
  else:reason='selected in CM top 20'
  rows.append(dict(signal_date=snap['date'],source_url=snap['source'],cmc_alt_rank=rank,cmc_id=r['id'],cmc_symbol=r['symbol'],cmc_name=r['name'],cmc_cap=r['quote']['USD']['marketCap'],cm_asset=mapped or '',mapping=method,disposition=reason))
 cmcids=[m for r,m,method in candidates];overlap=len(set(cm)&set(cmcids));overlap10=len(set(cm10)&set(cmcids[:10]));a['signal_dates']+=1;a['unmapped_observations']+=sum(not m for r,m,me in candidates);a['excluded_observations']+=len(excluded);a['missing_cap_observations']+=len(unrepresented);a['matched_top20_members']+=overlap
 reconciled.append(dict(signal_date=snap['date'],cmc_source=snap['source'],top10_overlap=overlap10,top20_overlap=overlap,cmc_unrepresented=unrepresented,cmc_excluded_by_model=excluded,cmc_quality_quarantined=quarantined,cm_top20=cm,cmc_top20=[r['symbol'] for r,m,me in candidates]))
write_csv('portfolio_reconciliation.csv',rows);write_csv('portfolio_identity_map.csv',list(identities.values()))
report=dict(status='restricted_universe_only',**a,mean_top20_overlap=a['matched_top20_members']/a['signal_dates'],min_top20_overlap=min(x['top20_overlap'] for x in reconciled),max_top20_overlap=max(x['top20_overlap'] for x in reconciled),dates_with_full_top20_match=sum(x['top20_overlap']==20 for x in reconciled),first_signal=reconciled[0]['signal_date'],last_signal=reconciled[-1]['signal_date'],unmapped_symbols=sorted(set(r['cmc_symbol'] for r in rows if not r['cm_asset'])),scope='All modeled signals have a matching CMC page. This reconciles observed source differences, not historical market completeness or migration economics.',signals=reconciled)
(D/'portfolio_reconciliation.json').write_text(json.dumps(report,separators=(',',':')))
print(json.dumps({k:v for k,v in report.items() if k!='signals'},indent=2))
