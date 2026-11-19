// 크롬(야후 파이낸스 탭)에서 실행하는 시세 수집 — scripts/fetch_market.py 와 같은 파일을 만든다.
// 결과: window.__F = {파일이름: 내용}. GitHub Actions 수집이 막힐 때 대신 쓴다.
(async () => {
const SUMMARY=['^IXIC','^GSPC','^DJI','SOXX','QQQ','SPY','^VIX','^TNX','DX-Y.NYB','KRW=X','CL=F','^SOX','^RUT','GC=F','NVDA','SNDK','MU'];
const IDX={'^IXIC':[1,'QQQ'],'^GSPC':[10,'SPY'],'SOXX':[100,'SOXX']};
const MOVERS='AAPL ADBE AMD AMZN ARM ASML ASTS AVGO BA BAC BRK-B COIN COST CRM CRWD CVX DIS GLD GOOGL HOOD IBIT INTC IONQ JNJ JPM KO LLY MA MCD META MSFT MSTR MU NFLX NKE NOW NVDA OKLO ORCL PANW PEP PFE PLTR QCOM QQQ RIVN RKLB SBUX SCHD SHOP SMCI SNDK SNOW SOFI SOXL SOXX SPY STX TLT TQQQ TSLA TSM UBER UNH V VOO WDC WMT XOM SPCX SNXX ANT'.split(' ');
const TOP=(window.__TOP||[]).map(r=>r.length===3?[r[0],r[1],0,r[2]]:r); // [[t,w,(ch),name]] slickcharts
const base='https://query1.finance.yahoo.com/v8/finance/chart/';
async function chart(s,rng='1y',itv='1d'){try{const j=await fetch(base+encodeURIComponent(s)+`?range=${rng}&interval=${itv}`).then(r=>r.json());const r=j.chart.result[0],q=r.indicators.quote[0],off=r.meta.gmtoffset||0;
 return (r.timestamp||[]).map((t,i)=>[new Date((t+(itv==='1d'?off:-5*3600))*1000).toISOString().slice(0,10),q.open[i],q.high[i],q.low[i],q.close[i],q.volume[i]||0]).filter(x=>x[4]!=null)}catch(e){return []}}
async function daily(s){let rows=await chart(s);if(rows.length<30){const by={};(await chart(s,'3mo','1h')).forEach(([d,o,h,l,c,v])=>{const b=by[d]||(by[d]=[d,o,h,l,c,0]);b[2]=Math.max(b[2],h);b[3]=Math.min(b[3],l);b[4]=c;b[5]+=v});const a=Object.values(by);if(a.length>rows.length)rows=a}return rows}
const avg=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
const ma=(cl,n,i)=>{i=i==null?cl.length-1:i;return i-n+1>=0?avg(cl.slice(i-n+1,i+1)):null};
const rsi=(cl,n=14)=>{if(cl.length<=n)return null;const g=[],l=[];for(let i=1;i<cl.length;i++){g.push(Math.max(cl[i]-cl[i-1],0));l.push(Math.max(cl[i-1]-cl[i],0))}let ag=avg(g.slice(0,n)),al=avg(l.slice(0,n));for(let i=n;i<g.length;i++){ag=(ag*(n-1)+g[i])/n;al=(al*(n-1)+l[i])/n}return al===0?100:100-100/(1+ag/al)};
const pct=(a,b)=>a!=null&&b?(a/b-1)*100:null;const r2=(v,k=2)=>v==null?'':v.toFixed(k);
const b64=arr=>btoa(String.fromCharCode(...arr));
const pack=(vals,mn,mx,top=254,nul=true)=>b64(vals.map(v=>v==null?(nul?255:0):Math.max(0,Math.min(top,Math.round((v-mn)/(mx-mn)*top)))));
const D={};const syms=[...new Set([...SUMMARY,...MOVERS,'QQQ','SPY','SOXX',...TOP.map(t=>t[0].replace('.','-'))])];
for(let i=0;i<syms.length;i+=8){await Promise.all(syms.slice(i,i+8).map(async s=>{D[s]=await daily(s)}))}
const F={};
const sumRow=rows=>{const cl=rows.map(r=>r[4]),vo=rows.map(r=>r[5]),L=rows[rows.length-1],n=cl.length,w=rows.slice(-252);
 const hi=w.reduce((a,r)=>r[2]>a[2]?r:a),lo=w.reduce((a,r)=>r[3]<a[3]?r:a),v20=avg(vo.slice(-21,-1)),back=k=>n>k?cl[n-1-k]:null;
 return [L[0],r2(L[4]),r2(cl[n-2]),r2(pct(L[4],cl[n-2])),r2(L[1]),r2(L[2]),r2(L[3]),r2(ma(cl,20)),r2(ma(cl,50)),r2(ma(cl,200)),r2(ma(cl,20,n-2)),r2(ma(cl,50,n-2)),r2(ma(cl,200,n-2)),r2(hi[2]),hi[0],r2(lo[3]),lo[0],r2(rsi(cl),1),
  String(vo[n-1]||''),v20?String(Math.round(v20)):'',r2(vo[n-1]&&v20?vo[n-1]/v20:null),r2(Math.max(...rows.slice(-20).map(r=>r[2]))),r2(Math.min(...rows.slice(-20).map(r=>r[3]))),r2(Math.max(...rows.slice(-60).map(r=>r[2]))),r2(Math.min(...rows.slice(-60).map(r=>r[3]))),
  r2(pct(L[4],back(5))),r2(pct(L[4],back(21))),r2(pct(L[4],back(63)))].join(',')};
F['summary.txt']=['sym|date,close,prev,chg,open,high,low,ma20,ma50,ma200,ma20p,ma50p,ma200p,hi52,hi52d,lo52,lo52d,rsi,vol,vol20,volr,res20,sup20,res60,sup60,w1,m1,m3',...SUMMARY.filter(s=>(D[s]||[]).length>25).map(s=>s+'|'+sumRow(D[s]))].join('\n')+'\n';
const dates=D.SPY.slice(-120).map(r=>r[0]);const rs=['D|'+dates.map(d=>d.slice(5,7)+d.slice(8,10)).join(' ')];const C3={};
for(const [s,[sc,vs]] of Object.entries(IDX)){const rows=Object.fromEntries(D[s].map(r=>[r[0],r])),vr=Object.fromEntries(D[vs].map(r=>[r[0],r])),cl=D[s].map(r=>r[4]),ix=Object.fromEntries(D[s].map((r,i)=>[r[0],i]));
 const sel=dates.map(d=>rows[d]||null);const mas={};[5,20,50,60,120,200].forEach(m=>mas[m]=dates.map(d=>d in ix?ma(cl,m,ix[d]):null));const vol=dates.map(d=>vr[d]?vr[d][5]:0);
 const ev=a=>a.filter((_,i)=>i%3===0).map(v=>Math.round((v||0)*sc)).join(' ');
 rs.push([s,sel.map(r=>r?Math.round(r[4]*sc):0).join(' '),vol.map(v=>Math.round(v/1e5)).join(' '),ev(mas[20]),ev(mas[50]),ev(mas[200])].join('|'));
 const allv=[...sel.filter(Boolean).flatMap(r=>r.slice(1,5)),...[5,20,60,120,200].flatMap(m=>mas[m].filter(v=>v!=null))];const mn=Math.min(...allv),mx=Math.max(...allv);
 const flat=sel.flatMap((r,i)=>[...(r?r.slice(1,5):[null,null,null,null]),...[5,20,60,120,200].map(m=>mas[m][i])]);const vmax=Math.max(...vol)||1;
 C3[s]={d0:dates[0],d1:dates[119],n:120,mn:+mn.toFixed(4),mx:+mx.toFixed(4),mas:[5,20,60,120,200],b:pack(flat,mn,mx),vb:b64(vol.map(v=>Math.round(v/vmax*255))),vmax}}
F['raw_series.txt']=rs.join('\n')+'\n';F['idx_candles.json']=JSON.stringify({idx:C3});
const mv=[],mini={};
for(const t of MOVERS){const rows=D[t]||[];if(rows.length<25){mini[t]=null;continue}const cl=rows.map(r=>r[4]),vo=rows.map(r=>r[5]),L=rows[rows.length-1],n=cl.length;const hi52=Math.max(...rows.slice(-252).map(r=>r[2])),m50=ma(cl,50),m200=ma(cl,200);
 mv.push([t,L[0].slice(5),L[4].toFixed(2),pct(L[4],cl[n-2]).toFixed(2),pct(L[4],cl[n-6]).toFixed(1),n>22?pct(L[4],cl[n-22]).toFixed(1):'0',pct(L[4],hi52).toFixed(1),m50&&L[4]>m50?1:0,m200&&L[4]>m200?1:0,Math.round(rsi(cl)||50)].join(','));
 const l22=rows.slice(-22),mn=Math.min(...l22.map(r=>r[3])),mx=Math.max(...l22.map(r=>r[2])),v20=avg(vo.slice(-21,-1));const rr=x=>x==null?null:+x.toFixed(2);
 mini[t]=[+mn.toFixed(4),+mx.toFixed(4),pack(l22.flatMap(r=>r.slice(1,5)),mn,mx,255,false),rr(Math.max(...rows.slice(-20).map(r=>r[2]))),rr(Math.min(...rows.slice(-20).map(r=>r[3]))),rr(ma(cl,5)),rr(ma(cl,20)),rr(ma(cl,50)),rr(ma(cl,200)),v20?rr(vo[n-1]/v20):null]}
F['movers_raw.txt']=mv.join('\n')+'\n';F['tickers_mini.json']=JSON.stringify(mini);
if(D.SNDK)F['sndk_daily.json']=JSON.stringify(D.SNDK.slice(-66).map(r=>[r[0],...r.slice(1,5).map(x=>+x.toFixed(2)),r[5]]));
if(TOP.length){const td={};for(const [t] of TOP){const ys=t.replace('.','-');let rows=D[ys]||[];if(rows.length<25){td[ys]='ERR';continue}rows=rows.slice(-63);const n=rows.length,cl=rows.map(r=>r[4]),vo=rows.map(r=>r[5]),L=rows[n-1],v20=avg(vo.slice(-21,-1));const rr=(x,k=2)=>+x.toFixed(k);
 td[ys]=[L[0],...L.slice(1,5).map(x=>rr(x)),rr(pct(L[4],cl[n-2])),L[5],v20?rr(L[5]/v20):null,rr(pct(L[4],cl[n-6]),1),rr(pct(L[4],cl[Math.max(0,n-22)]),1),rr(ma(cl,20)),rr(ma(cl,50)),rr(Math.max(...rows.map(r=>r[2]))),rr(Math.min(...rows.map(r=>r[3]))),n]}
 F['tm_daily.json']=JSON.stringify(td);F['sp500_top100.txt']=TOP.map(t=>{const d=td[t[0].replace('.','-')];return [t[0],t[1].toFixed(2),(d&&d!=='ERR'?d[5]:t[2]).toFixed(2),t[3]].join(',')}).join(';')+'\n'}
F['market_meta.json']=JSON.stringify({fetched_utc:new Date().toISOString().slice(0,19),last_session:D.SPY[D.SPY.length-1][0],missing:Object.keys(D).filter(s=>D[s].length<25),via:'chrome'});
window.__F=F;window.__D=D;return Object.fromEntries(Object.entries(F).map(([k,v])=>[k,v.length]));
})()
