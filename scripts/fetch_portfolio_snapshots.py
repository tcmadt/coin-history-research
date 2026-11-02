"""Public CMC historical pages, source records preserved; no authenticated endpoints."""
import concurrent.futures,datetime as dt,json,re,subprocess,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'research/cmc_snapshots';OUT.mkdir(parents=True,exist_ok=True)
START=dt.date(2019,7,21);END=dt.date(2026,10,14)
dates=[];d=START
while d<=END:
 dates.append(d);d+=dt.timedelta(days=30)
def fetch(d):
 key=d.strftime('%Y%m%d');p=OUT/(key+'.json')
 if p.exists():return key,'cached'
 url='https://coinmarketcap.com/historical/'+key+'/'
 for attempt in range(3):
  z=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','40',url],capture_output=True)
  if z.returncode==0:
   try:
    html=z.stdout.decode();data=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',html,re.S)[1]);props=data['props'];page=props['pageProps'];assert page['dateWithHyphens']==d.isoformat();records=json.loads(props['initialState'])['cryptocurrency']['listingHistorical']['data'];assert len(records)>=30
    assert records[0]['symbol']=='BTC'
    result=dict(source=url,date=d.isoformat(),retrieved_utc=dt.datetime.now(dt.timezone.utc).isoformat(),html_sha256=hashlib.sha256(z.stdout).hexdigest(),records=records)
    p.write_text(json.dumps(result,separators=(',',':')));return key,len(records)
   except (ValueError,KeyError,AssertionError,TypeError):pass
  time.sleep(1+attempt)
 return key,'FAILED'
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for i,(key,n) in enumerate(pool.map(fetch,dates),1):
  if i%10==0 or n=='FAILED':print(i,'/',len(dates),key,n,flush=True)
print('Source extraction complete',len(dates),flush=True)
