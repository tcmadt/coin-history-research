import json,os
from pathlib import Path
DATA=Path(__file__).resolve().parents[1]/'dist/data'
QUALITY=json.loads((DATA/'quality.json').read_text());POLICY=QUALITY['valid_from']
def valid_rows(asset,rows):
 if os.environ.get('SNAPSHOT_RAW')=='1':return rows
 first=POLICY.get(asset,{}).get('day',-10**9);last=QUALITY.get('valid_until',{}).get(asset,{}).get('day',10**9)
 return [r for r in rows if first<=r[0]<=last]
