import json
from scripts.snapshot_quality import valid_rows
from pathlib import Path
root=Path(__file__).parent/'dist/data'
catalog=json.loads((root/'catalog.json').read_text())
btcs={key:dict((r[0],r[1]) for r in json.loads((root/(key+'.json')).read_text())) for key in ['btc','btc-coingecko']}
out=[]
for meta in catalog['assets']:
    btc=btcs['btc-coingecko' if meta['source'].startswith('CoinGecko') else 'btc']
    rows=[r for r in valid_rows(meta['id'],json.loads((root/(meta['id']+'.json')).read_text())) if r[0] in btc]
    initial=rows[0][1]/btc[rows[0][0]]
    peak=initial; dd=0; points=[]; previous=None
    for i,r in enumerate(rows):
        ratio=r[1]/btc[r[0]]
        peak=max(peak,ratio); dd=min(dd,ratio/peak-1)
        if i==0 or i==len(rows)-1 or r[0]-points[-1][0]>=7 or (previous is not None and r[0]-previous>1):
            if previous is not None and r[0]-previous>1 and points[-1][0]!=previous:
                prev=rows[i-1]; points.append([prev[0],round((prev[1]/btc[prev[0]])/initial,10)])
            points.append([r[0],round(ratio/initial,10)])
        previous=r[0]
    out.append(dict(id=meta['id'],entry=rows[0][0],end=rows[-1][0],usdReturn=rows[-1][1]/rows[0][1]-1,multiple=(rows[-1][1]/btc[rows[-1][0]])/initial,maxDD=dd,n=len(rows),points=points))
(root/'overview.json').write_text(json.dumps(out,separators=(',',':')))
print(f'Overview: {len(out)} histories, {sum(len(r["points"]) for r in out):,} plotted samples')
