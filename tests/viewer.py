"""Viewer-only checks: crafted payloads, old-bookmark banner, persistence, layout."""
import base64, re, asyncio, json, os, struct, zlib
from playwright.async_api import async_playwright
APP='https://huynguyenkhac17.github.io/gmaps-media-viewer/'
HERE=os.path.dirname(os.path.abspath(__file__))
HTML=open(os.path.join(HERE,'..','index.html'),encoding='utf-8').read()
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
X='x'*30
def png(w,h):   # plain grey PNG of any size (the 1x1 above cannot show a photo too tall for the lightbox)
    c=lambda t,d: struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+c(b'IDAT',zlib.compress(b''.join(b'\x00'+b'\x80'*3*w for _ in range(h))))+c(b'IEND',b'')
TALL=png(900,1600)
async def lh3(route):
    u=route.request.url
    if u.endswith('=dv'):
        if 'VID' in u: await route.fulfill(status=302, headers={'Location':'https://drum.usercontent.google.com/x.mp4'})
        elif 'HANG' in u: await asyncio.sleep(20); await route.abort()
        else: await route.fulfill(status=500, body='err')
    else: await route.fulfill(status=200, body=TALL if 'TALL' in u else PNG, content_type='image/png', headers={'Access-Control-Allow-Origin':'*'})
SEND='''async (d) => { const raw = typeof d === 'string' ? d : JSON.stringify(d);
  const st = new Blob([raw]).stream().pipeThrough(new CompressionStream('deflate-raw'));
  const u = new Uint8Array(await new Response(st).arrayBuffer()); let b=''; u.forEach(c=>b+=String.fromCharCode(c));
  location.hash = 'z=' + btoa(b).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,''); }'''
STATE='''() => ({photos: document.querySelector('.col[data-kind=photo] [data-count]').textContent, videos: document.querySelector('.col[data-kind=video] [data-count]').textContent,
  warn: !document.querySelector('#warn').hidden, toast: document.querySelector('#toast').textContent, place: document.querySelector('#place').textContent,
  injected: !!window.__xss || !!document.querySelector('img[src="x"], .rv script, #place img'), status: document.querySelector('#status').textContent})'''
ok=True
def check(name, cond, info=''):
    global ok; ok &= bool(cond); print(('PASS ' if cond else 'FAIL ')+name, info if not cond else '')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(channel=os.environ.get('CHANNEL','chrome') or None)
    ctx=await b.new_context(viewport={'width':1300,'height':900})
    await ctx.grant_permissions(['clipboard-read','clipboard-write'],origin='https://huynguyenkhac17.github.io')
    await ctx.route(re.compile(r'https://lh\d\.googleusercontent\.com/.*'), lh3)
    await ctx.route('https://drum.usercontent.google.com/**', lambda r: r.fulfill(status=404))
    await ctx.route(APP+'**', lambda r: r.fulfill(body=HTML, content_type='text/html; charset=utf-8'))
    errs=[]; pg=await ctx.new_page(); pg.on('pageerror',lambda e: errs.append(str(e))); await pg.goto(APP)
    ver=await pg.evaluate('BM_VER')
    check('guide open on first visit', await pg.eval_on_selector('details','e=>e.open'))
    good={'bv':ver,'n':'Quán A','dg':'Bình luận: duyệt 2, có ảnh 1','r':[{'a':'An','s':5,'t':'Ngon','p':['gps-cs-s/P1'+X,'gps-cs-s/P2'+X],'m':0}],'x':['gps-cs-s/P3'+X],'v':[['gps-cs-s/VID1'+X,'Tháng 2 2024']]}
    await pg.evaluate(SEND, good); await pg.wait_for_timeout(1500); st=await pg.evaluate(STATE)
    check('good payload', st['photos']=='3' and st['videos']=='1' and not st['warn'], st)
    # menu tab: own column, not repeated under photos; hidden again for a place without menu photos
    MENUQ="({menu: document.querySelector('.col[data-kind=menu] [data-count]').textContent, shown: !document.querySelector('.col[data-kind=menu]').hidden, three: document.querySelector('.cols').classList.contains('three')})"
    withm=dict(good); withm['x']=['gps-cs-s/P3'+X,'gps-cs-s/M1'+X]; withm['m']=['gps-cs-s/M1'+X,'geougc-cs/P2'+X,'gps-cs-s/M2'+X,'javascript:x//'+X]
    await pg.evaluate(SEND, withm); await pg.wait_for_timeout(1200); st=await pg.evaluate(STATE); mq=await pg.evaluate(MENUQ)
    check('menu photos get their own column', st['photos']=='2' and st['videos']=='1' and mq=={'menu':'3','shown':True,'three':True}, (st,mq))
    await pg.click('.col[data-kind=menu] [data-all]'); await pg.click('.col[data-kind=menu] [data-copysel]'); clip=await pg.evaluate('navigator.clipboard.readText()')
    check('copy menu photos =s0', clip.count(',')==2 and all(u.endswith('=s0') for u in clip.split(',')) and 'thực đơn' in (await pg.evaluate(STATE))['toast'], clip)
    await pg.click('.col[data-kind=menu] .thumb'); await pg.wait_for_timeout(200); lbt=await pg.text_content('#lbt'); await pg.keyboard.press('Escape')
    check('lightbox steps through menu photos', lbt.startswith('Thực đơn 1/3'), lbt)
    await pg.reload(); await pg.wait_for_timeout(800); mq=await pg.evaluate(MENUQ)
    check('menu column kept after reload', mq['menu']=='3' and mq['shown'], mq)
    await pg.evaluate(SEND, good); await pg.wait_for_timeout(1200); st=await pg.evaluate(STATE); mq=await pg.evaluate(MENUQ)
    check('no menu photos -> two columns', st['photos']=='3' and mq=={'menu':'0','shown':False,'three':False}, (st,mq))
    # malformed payloads must not wipe the current list
    for name,bad in [('not json','{{{'),('array','[1,2]'),('null','null')]:
        await pg.evaluate(SEND, bad); await pg.wait_for_timeout(700); st=await pg.evaluate(STATE)
        check('malformed payload keeps list: '+name, st['photos']=='3' and 'hỏng' in st['toast'], st)
    await pg.evaluate("location.hash='z=!!!not-base64'"); await pg.wait_for_timeout(700); st=await pg.evaluate(STATE)
    check('garbage hash keeps list', st['photos']=='3', st)
    # hostile payload: HTML in text fields, bad ids, huge stars
    evil={'bv':ver,'n':'<img src=x onerror="window.__xss=1">','dg':'<script>window.__xss=1</script>','r':[{'a':'<img src=x onerror="window.__xss=1">','s':99999999,'t':'<script>window.__xss=1</script>','p':['gps-cs-s/E1'+X,'javascript:alert(1)//'+X,'../../evil/'+X,'gps-cs-s/E2'+X+'"onerror="x',5,None],'m':-4}, 'junk', None],
          'x':'notarray','v':[['gps-cs-s/VIDE'+X,{'a':1}],'junk',[7]]}
    await pg.evaluate(SEND, evil); await pg.wait_for_timeout(1500); st=await pg.evaluate(STATE)
    stars=await pg.eval_on_selector('.rv .stars','e=>e.textContent.length')
    check('hostile payload is inert', st['photos']=='1' and st['videos']=='1' and not st['injected'] and stars==5, (st,stars))
    await pg.click('.rv .thumb'); await pg.wait_for_timeout(300); st=await pg.evaluate(STATE); await pg.keyboard.press('Escape')
    check('hostile text inert in lightbox', not st['injected'])
    # old bookmark (no version) -> banner; legacy #p link -> banner
    old=dict(good); del old['bv']
    await pg.evaluate(SEND, old); await pg.wait_for_timeout(1200); st=await pg.evaluate(STATE)
    check('old bookmark shows update banner', st['warn'] and st['photos']=='3', st)
    await pg.evaluate(SEND, good); await pg.wait_for_timeout(1200); st=await pg.evaluate(STATE)
    check('current bookmark hides banner', not st['warn'], st)
    await pg.evaluate("location.hash='new=1&vt=1&n=Old&p='+encodeURIComponent('gps-cs-s/L1%s,gps-cs-s/L2%s')+'&v='+encodeURIComponent('gps-cs-s/VIDL%s')" % (X,X,X)); await pg.wait_for_timeout(1500); st=await pg.evaluate(STATE)
    check('legacy link still works + banner', st['photos']=='2' and st['videos']=='1' and st['warn'], st)
    # photo wrongly labelled as video -> moved; real video kept; hanging check keeps the label
    mix=dict(good); mix['v']=[['gps-cs-s/VIDOK'+X,'May 2024'],['gps-cs-s/NOTV'+X,'May 2024'],['gps-cs-s/HANG'+X,'May 2024']]
    await pg.evaluate(SEND, mix); await pg.wait_for_timeout(2500)
    await pg.reload(); await pg.wait_for_timeout(16000); st=await pg.evaluate(STATE)   # reload mid-check: must resume
    ids=await pg.evaluate("[...document.querySelectorAll('.col[data-kind=video] .id')].map(e=>e.title.split('/').pop().slice(0,5))")
    check('mislabelled photo moved, real + undecided videos kept (after reload)', st['photos']=='4' and sorted(ids)==['HANGx','VIDOK'], (st,ids))
    check('place name restored after reload', 'Quán A' in st['place'], st)
    # copy flows
    await pg.click('.col[data-kind=photo] [data-all]'); await pg.click('.col[data-kind=photo] [data-copysel]')
    clip=await pg.evaluate('navigator.clipboard.readText()')
    check('copy selected: comma separated =s0', clip.count(',')==3 and all(u.startswith('https://lh3.googleusercontent.com/') and u.endswith('=s0') for u in clip.split(',')), clip[:120])
    await pg.click('.col[data-kind=video] .cp'); clip=await pg.evaluate('navigator.clipboard.readText()')
    check('copy video url =dv', clip.endswith('=dv'), clip)
    await pg.click('.rv button:has-text("Copy bình luận")'); check('copy review text', await pg.evaluate('navigator.clipboard.readText()')=='Ngon')
    await pg.click('#status'); clip=await pg.evaluate('navigator.clipboard.readText()'); check('copy status line', 'Bình luận: duyệt 2' in clip and 'Quán A' in clip, clip)
    # manual paste of a plain place link finds nothing; a photo link adds one
    pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.fill('#src','https://www.google.com/maps/place/Over+The+Moon+Coffee/@10.3801512,107.1028381,17z/data=!4m16!1m9!3m8!1s0x317571e55117434b:0x2acc19bbe5fb8778!2sOver+The+Moon+Coffee!8m2!3d10.380172!4d107.1028045!9m1!1b1!16s%2Fg%2F11sryz220t?entry=ttu&g_ep=EgoyMDI2MTExMC4wIKXMDSoASAFQAw%3D%3D'); await pg.click('#add'); await pg.wait_for_timeout(300); st=await pg.evaluate(STATE)
    check('place link alone adds nothing, explains why', st['photos']=='4' and 'bookmark' in st['toast'], st)
    # layout: long status must not break the header; narrow screen
    long={'bv':ver,'n':'Học viện Hàng không Việt Nam - Cơ sở 2 (Vietnam Aviation Academy)','dg':'Bình luận: duyệt 1200, có ảnh 310 · Tất cả: 2100 ảnh, 14 video · Video: 14 · Ảnh bình luận có trong thư viện: 900/900','r':[{'a':'An','s':4,'t':'Dài '*300,'p':['gps-cs-s/P%d'%i+X for i in range(7)],'m':2}],'x':['gps-cs-s/Q%d'%i+X for i in range(9)],'v':[['gps-cs-s/VID%d'%i+X,'Tháng 2 2024'] for i in range(3)],'m':['gps-cs-s/MN%d'%i+X for i in range(5)]}
    await pg.evaluate(SEND, long); await pg.wait_for_timeout(1500)
    for w in (1300, 820, 390):
        await pg.set_viewport_size({'width':w,'height':800}); await pg.wait_for_timeout(200)
        m=await pg.evaluate("({h: document.querySelector('header').getBoundingClientRect().height, over: document.documentElement.scrollWidth > innerWidth + 1})")
        check('layout at %dpx: header one line, no sideways scroll'%w, m['h']<=54 and not m['over'], m)
    # lightbox: a photo taller than the screen must shrink to fit (16:9 laptop at 125% = 1536x730), caption or not
    await pg.set_viewport_size({'width':1536,'height':730})
    tall={'bv':ver,'n':'Q','dg':'','r':[{'a':'An','s':5,'t':'Ngon '*200,'p':['gps-cs-s/TALLR'+X],'m':0}],'x':['gps-cs-s/TALL'+X],'v':[]}
    await pg.evaluate(SEND, tall); await pg.wait_for_timeout(1200)
    for sel in ('.rv .thumb', '.rv:nth-child(2) .thumb'):
        await pg.click(sel); await pg.wait_for_timeout(600)
        fit=await pg.evaluate("(()=>{const i=document.querySelector('#lbbody img').getBoundingClientRect(),b=document.querySelector('#lbbody').getBoundingClientRect();return {img:[i.top,i.bottom,i.height],box:[b.top,b.bottom],fits:i.height>100&&i.top>=b.top-1&&i.bottom<=b.bottom+1&&i.right<=innerWidth}})()")
        await pg.keyboard.press('Escape')
        check('lightbox fits a tall photo at 1536x730: '+sel, fit['fits'], fit)
    check('no page errors', not errs, errs)
    print('ALL PASS' if ok else 'SOME FAILED')
    await b.close()
asyncio.run(main())
