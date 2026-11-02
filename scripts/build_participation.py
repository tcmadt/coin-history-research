"""Non-trading participation illustration and passive receipt-price benchmarks."""
import json,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'dist/data';E=datetime.date(1970,1,1);CUT=20740
P={a:{d:p for d,p,_ in json.loads((D/(a+'.json')).read_text())} for a in ['eth','sol','btc','wsteth','msol','arb']};start=max(min(P[a]) for a in ['eth','sol','btc','wsteth','msol']);ds=lambda d:str(E+datetime.timedelta(days=d));examples=[]
for base,receipt in [('eth','wsteth'),('sol','msol')]:
 growth=P[base][CUT]/P[base][start];rg=P[receipt][CUT]/P[receipt][start];r=dict(base=base,receipt=receipt,start=ds(start),end=ds(CUT),capital=10000,hold_base=10000*growth,passive=10000*rg,hold_eth=10000*P['eth'][CUT]/P['eth'][start],hold_btc=10000*P['btc'][CUT]/P['btc'][start],receipt_vs_base=rg/growth)
 if base=='eth':
  before=9500*rg+400*growth;value=625*P['arb'][CUT];r.update(drop='arb',allocation=625,active_before_drop=before,active_hold=before+value,airdrop_terminal_price=P['arb'][CUT],airdrop_held_value=value)
 examples.append(r)
(D/'participation.json').write_text(json.dumps(dict(cutoff=ds(CUT),start=ds(start),examples=examples,sources={'wsteth':'https://help.lido.fi/en/articles/5231836-what-is-lido-s-wsteth','msol':'https://docs.marinade.finance/marinade-protocol/protocol-overview/marinade-liquid/what-is-msol','arb':'https://docs.arbitrum.foundation/airdrop-eligibility-distribution','jito':'https://www.jito.network/blog/jto-airdrop-eligibility-and-allocation-specifications/'}),separators=(',',':')))
print('Built passive ETH/SOL receipt benchmarks and held-ARB non-trading illustration; no trading or sale-timing outcomes.')
