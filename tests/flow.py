"""Full-flow test on a mock that mimics the real Maps structure reported so far.
env: NET=slow  CLS=none  PREFIX=1  DIRECT=1  PRESS=skip|send  """
import base64, re, asyncio, json, os, sys
from playwright.async_api import async_playwright
E=os.environ.get
SLOW=E('NET')=='slow'; CLS=E('CLS','all'); PREFIX=bool(E('PREFIX')); DIRECT=bool(E('DIRECT')); PRESS=E('PRESS','')
APP='https://huynguyenkhac17.github.io/gmaps-media-viewer/'
HERE=os.path.dirname(os.path.abspath(__file__))
HTML=open(os.path.join(HERE,'..','index.html'),encoding='utf-8').read()
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
MP4=open(os.path.join(HERE,'tiny.mp4'),'rb').read()
P=dict(slow=SLOW, cls=CLS, prefix=PREFIX)
MAPS=r'''<html><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="require-trusted-types-for 'script'"><title>Học viện Test - Google Maps</title></head><body style="margin:0">
<div role="main" id="main" style="width:420px;height:760px;display:flex;flex-direction:column"></div>
<div id="vdate" style="position:fixed;left:450px;top:10px"></div>
<script>
const P=__P__, L=(fast,slow)=>P.slow?slow:fast;
const X='x'.repeat(28);
function E(t,a,txt){const e=document.createElement(t);for(const k in a)e.setAttribute(k,a[k]);if(txt)e.textContent=txt;return e;}
const N=60, REVS=[];
for(let i=0;i<N;i++){const np=i%3===0?(i%4)+1:0;const ps=[];for(let j=0;j<np;j++)ps.push('R'+String(i).padStart(3,'0')+'_'+j+X);
  if(i===9)ps.push('VIDREV'+X);
  REVS.push({id:'rv'+i,a:'Khách '+i,s:(i%5)+1,full:i%6===0?'':'Bình luận số '+i+'. Món ăn ngon, phục vụ nhanh, sẽ quay lại lần sau nhé mọi người!',ps,more:i===3?3:0});}
const revPre=P.prefix?'geougc-cs/':'gps-cs-s/';
function review(r){
  const d=E('div',{'data-review-id':r.id,'aria-label':r.a,'class':'jftiEf'});d.style.cssText='padding:8px;border-bottom:1px solid #ccc';
  d.append(E('img',{src:'https://lh3.googleusercontent.com/a-/AVATAR'+r.id+X+'=w36'}),E('div',{class:'d4r55'},r.a),E('div',{class:'RfnDt'},'Local Guide · 12 bài đánh giá · 30 ảnh'),E('span',{role:'img','aria-label':r.s+' sao'}),E('span',{class:'rsqaWe'},'2 tháng trước'));
  if(r.full){const t=E('span',P.cls==='all'?{class:'wiI7pd'}:{},r.full.slice(0,30)+'…');d.append(t);
    const more=E('button',{'aria-label':'Xem thêm','data-review-id':r.id},'Thêm');more.onclick=()=>setTimeout(()=>{t.textContent=r.full;more.remove();},150);d.append(more);}
  const ph=E('div',{});r.ps.forEach((p,k)=>{const b=E('button',{'data-review-id':r.id,'data-photo-index':k,class:'Tya61d','aria-label':'Ảnh '+(k+1)+' trong bài đánh giá của '+r.a});b.style.cssText='display:inline-block;width:60px;height:60px;background-image:url("https://lh3.googleusercontent.com/'+revPre+p+'=w300-h300-k-no")';b.onclick=()=>{window.__misclick=1;};ph.append(b);});
  if(r.more)ph.append(E('div',{},'+'+r.more));d.append(ph);
  if(r.id==='rv6'||r.id==='rv12'){const o=E('div',{class:'CDe7pd'});o.append(E('span',P.cls==='all'?{class:'wiI7pd'}:{},'Phản hồi của chủ sở hữu: Cảm ơn quý khách rất nhiều vì đã ủng hộ quán, hẹn gặp lại quý khách lần sau ạ!!!'));d.append(o);}
  return d;}
const main=document.getElementById('main');
let pane, placeTabs;
function place(sel){main.replaceChildren();main.append(E('h1',{},'Học viện Test'));
  placeTabs=E('div',{});for(const n of ['Tổng quan','Bài đánh giá','Giới thiệu']){const b=E('button',{role:'tab','aria-selected':n===sel,'aria-label':n==='Bài đánh giá'?'Bài đánh giá về Học viện Test':n},n);b.onclick=()=>{placeTabs.querySelectorAll('button').forEach(x=>x.setAttribute('aria-selected',x===b));(n==='Bài đánh giá'?reviews:overview)();};placeTabs.append(b);}
  pane=E('div',{id:'pane'});pane.style.cssText='flex:1;overflow-y:auto';main.append(placeTabs,pane);}
let gen=0;
function overview(){const g=++gen;pane.replaceChildren(E('div',{},'đang tải…'));pane.onscroll=null;setTimeout(()=>{if(g!==gen)return;pane.replaceChildren();
  const h=E('button',{jsaction:'pane.heroHeaderImage.click',id:'hero','aria-label':'Ảnh của Học viện Test'});h.append(E('img',{src:'https://lh3.googleusercontent.com/gps-cs-s/HERO'+X+'xx=w400',width:40}));h.onclick=gallery;
  pane.append(h,E('div',{},'Tổng quan…'),review(REVS[0]),review(REVS[3]));},L(300,6000));}
function reviews(){const g=++gen;pane.replaceChildren(E('div',{},'đang tải…'));pane.onscroll=null;let shown=0,busy=0,batch=0;
  const add=()=>{const n=Math.min(shown+10,N);for(;shown<n;shown++)pane.append(review(REVS[shown]));};
  setTimeout(()=>{if(g!==gen)return;pane.replaceChildren();add();
    pane.onscroll=()=>{if(pane.scrollTop+pane.clientHeight>=pane.scrollHeight-4&&!busy&&shown<N){busy=1;setTimeout(()=>{if(g===gen)add();busy=0},L(700,[9000,3000,6000,2500,7000][batch++%5]))}};},L(300,5000));}
const OWN=[];for(let k=0;k<8;k++)OWN.push('OWN'+k+X+'xx');
const VIDS=['VIDA'+X+'xx','VIDREV'+X,'VIDB'+X+'xx'];
const VD={VIDA:'Tháng 6 2025',VIDREV:'Aug 2024',VIDB:'3 tuần trước'};
function gallery(){const g=++gen;setTimeout(()=>{if(g!==gen)return;main.replaceChildren();main.append(E('h1',{},'Ảnh'));
  const tabs=E('div',{role:'tablist'});const list=E('div',{id:'glist'});list.style.cssText='flex:1;overflow-y:auto';
  const tile=(id,i)=>{const isV=VIDS.includes(id),sv=id==='SV';const t=E('div',{'data-photo-index':i,'aria-label':isV?'Video':'Ảnh '+(i+1)});t.style.cssText='height:100px;margin:4px;background:#eee';const c=E('div',{});c.style.height='100%';t.append(c);
     const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.disconnect();setTimeout(()=>{c.style.backgroundImage=sv?'url("https://streetviewpixels-pa.googleapis.com/v1/thumbnail?x=1")':'url("https://lh3.googleusercontent.com/gps-cs-s/'+id+'=w200-k-no")'},L(100,1500))}}));io.observe(t);
     t.onclick=()=>setTimeout(()=>{document.getElementById('vdate').textContent=VD[id.replace(/x+$/,'')]||'Tháng 1 2020'},300);return t;};
  let fg=0;
  const fill=(arr,delay)=>{const f=++fg;list.replaceChildren();list.onscroll=null;setTimeout(()=>{if(f!==fg)return;let shown=0,busy=0;
     const add=()=>{const n=Math.min(shown+12,arr.length);for(;shown<n;shown++)list.append(tile(arr[shown],shown));};add();
     list.onscroll=()=>{if(list.scrollTop+list.clientHeight>=list.scrollHeight-4&&!busy&&shown<arr.length){busy=1;setTimeout(()=>{if(f===fg)add();busy=0},L(500,5000))}};},delay);};
  const all=[...REVS.flatMap(r=>r.ps).filter(x=>!x.startsWith('VIDREV')),...OWN.slice(0,4),VIDS[0],'SV',VIDS[1],...OWN.slice(4),VIDS[2]];
  for(const [n,arr] of [['Tất cả',all],['Mới nhất',all.slice(0,5)],['Video',VIDS],['Thực đơn',OWN.slice(0,2)]]){const b=E('button',{role:'tab','aria-selected':n==='Mới nhất'});b.append(E('img',{src:'https://lh3.googleusercontent.com/gps-cs-s/TABICON'+n.length+X+'xx=w60'}),E('span',{},n));
     b.onclick=()=>{tabs.querySelectorAll('button').forEach(x=>x.setAttribute('aria-selected',x===b));if(n==='Video'&&P.slow){/* old tiles stay on screen while loading */setTimeout(()=>fill(arr,0),7000)}else fill(arr,L(0,2000))};tabs.append(b);}
  main.append(tabs,list);fill(all.slice(0,5),0);},L(600,5000));}
place('Tổng quan');overview();
</script></body></html>'''.replace('__P__',json.dumps(P))
async def lh3(route):
    u=route.request.url
    if u.endswith('=dv'):
        if 'VID' in u:
            if DIRECT: await route.fulfill(status=200, body=MP4, content_type='video/mp4')
            else: await route.fulfill(status=302, headers={'Location':'https://drum.usercontent.google.com/x.mp4'})
        else: await route.fulfill(status=500, body='err')
    else: await route.fulfill(status=200, body=PNG, content_type='image/png', headers={'Access-Control-Allow-Origin':'*'})
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(channel='chrome')
    ctx=await b.new_context(viewport={'width':1300,'height':900})
    await ctx.grant_permissions(['clipboard-read','clipboard-write'],origin='https://huynguyenkhac17.github.io')
    await ctx.route(re.compile(r'https://lh\d\.googleusercontent\.com/.*'), lh3)
    await ctx.route('https://drum.usercontent.google.com/**', lambda r: r.fulfill(status=404))
    await ctx.route('https://streetviewpixels-pa.googleapis.com/**', lambda r: r.fulfill(status=200, body=PNG, content_type='image/png'))
    await ctx.route(APP+'**', lambda r: r.fulfill(body=HTML, content_type='text/html; charset=utf-8'))
    await ctx.route('https://www.google.com/maps/**', lambda r: r.fulfill(body=MAPS, content_type='text/html; charset=utf-8'))
    errs=[]
    pg=await ctx.new_page(); await pg.goto(APP)
    bm=await pg.eval_on_selector('#bm','a=>decodeURIComponent(a.getAttribute("href").slice(11))')
    maps=await ctx.new_page(); maps.on('pageerror',lambda e: errs.append('maps:'+str(e)))
    await maps.goto('https://www.google.com/maps/place/test'); await maps.wait_for_timeout(L:=7000 if SLOW else 800)
    t0=asyncio.get_event_loop().time(); last=''
    async with ctx.expect_page(timeout=600000) as newp:
        await maps.evaluate(bm)
        pressed=False
        for k in range(600):
            await maps.wait_for_timeout(1000)
            try: txt=await maps.evaluate("(()=>{const b=[...document.querySelectorAll('body>div')].find(d=>d.style.zIndex==='2147483647');return b?b.children[0].textContent:''})()")
            except Exception: break
            if txt!=last: print('  %3ds %s'%(asyncio.get_event_loop().time()-t0, txt), flush=True); last=txt
            if PRESS and not pressed and 'duyệt bình luận' in txt and k>3:
                pressed=True; await maps.evaluate("(l)=>{const b=[...document.querySelectorAll('body>div')].find(d=>d.style.zIndex==='2147483647');[...b.querySelectorAll('button')].find(x=>x.textContent===l).click()}", 'Bỏ qua bước' if PRESS=='skip' else 'Gửi ngay')
            if not txt: break
    app=await newp.value; app.on('pageerror',lambda e: errs.append('app:'+str(e)))
    await app.wait_for_load_state(); await app.wait_for_timeout(5000)
    print('took %.0fs'%(asyncio.get_event_loop().time()-t0), 'misclick', await maps.evaluate('window.__misclick||0'))
    rv=await app.evaluate("JSON.parse(localStorage.getItem('gmv.reviews.v1'))"); items=await app.evaluate("JSON.parse(localStorage.getItem('gmv.items.v1'))")
    photos=[i for i in items if i[1]=='photo']; vids=[i for i in items if i[1]=='video']
    exp_rev=sum(1 for i in range(60) if i%3==0); exp_rp=sum((i%4)+1 for i in range(60) if i%3==0)
    print('reviews %d (exp %d) | photos %d (exp %d review + 8 owner = %d) | videos %s'%(len(rv),exp_rev,len(photos),exp_rp,exp_rp+8,[(v[0].split('/')[1][:6],v[2],v[4],v[5]) for v in vids]))
    print('no-text review ->', [r['t'] for r in rv if r['a']=='Khách 0'], '| rv6 ->', [r['t'][:40] for r in rv if r['a']=='Khách 6'], '| rv3 text ok:', [r['t'].endswith('mọi người!') for r in rv if r['a']=='Khách 3'])
    print('leaks:', [k for k in ('TABICON','HERO','AVATAR','streetview','SV') if k in json.dumps(items)])
    print('place:', await app.text_content('#place'), '| warn hidden:', await app.eval_on_selector('#warn','e=>e.hidden'))
    print('status:', await app.get_attribute('#status','title') and await app.text_content('#status'))
    print('errors',errs)
    await b.close()
asyncio.run(main())
