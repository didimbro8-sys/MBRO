"""Moteur motion design AM.Digital v3 « cinéma » : rendu HTML/CSS 3D image par image (Playwright) -> MP4 1080x1920 30 i/s.
Effets : caméra 3D (perspective, dolly, roulis), sol grille néon en perspective, cubes-pixels 3D en orbite, fond liquide,
typo cinétique lettre par lettre (bascule 3D + masque), mots or avec reflet balayé et halo, flare anamorphique,
chiffre « slam » avec onde de choc + tremblement + aberration chromatique, éclats de particules,
transitions alternées (cube 3D, iris or, tranches, zoom traversant), logo final assemblé par pixels volants.
Musique : piste fournie, sinon musique afro-house synthétisée (gen/music.py)."""
import json, subprocess, os, sys
from playwright.sync_api import sync_playwright
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
sys.path.insert(0,S+"/gen")
FONT="".join(f"@font-face{{font-family:M;font-weight:{w};src:url('file://{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2')}}" for w in (500,600,700,800))
LOGO=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
W,H,FPS=1080,1920,30
HTML=r"""<!doctype html><html><head><meta charset=utf-8><style>%FONT%
*{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#14000f;font-family:M,Arial,sans-serif;color:#fff}
#bg{position:absolute;inset:0;overflow:hidden}
#liq{position:absolute;inset:-300px;filter:blur(80px)}#liq div{position:absolute;border-radius:50%}
#floorwrap{position:absolute;left:-600px;right:-600px;bottom:-200px;height:1100px;perspective:700px;perspective-origin:50% 0%;overflow:hidden}
#floor{position:absolute;inset:0;transform-origin:50% 0;transform:rotateX(72deg);background-image:linear-gradient(rgba(241,188,24,.55) 2px,transparent 2px),linear-gradient(90deg,rgba(241,188,24,.55) 2px,transparent 2px);background-size:120px 120px;-webkit-mask-image:linear-gradient(transparent,#000 35%,#000)}
#horizon{position:absolute;left:0;right:0;bottom:880px;height:6px;background:#f1bc18;box-shadow:0 0 60px 20px rgba(241,188,24,.35);opacity:.6}
#stage{position:absolute;inset:0;perspective:1600px;perspective-origin:50% 45%}
#world{position:absolute;inset:0;transform-style:preserve-3d}
.cube{position:absolute;left:0;top:0;transform-style:preserve-3d}
.cube i{position:absolute;inset:0;background:linear-gradient(135deg,#ffd75a,#c79613);border:1px solid rgba(255,255,255,.35)}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 88px;gap:36px;transform-style:preserve-3d;backface-visibility:hidden}
.lab{font-size:34px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#f1bc18;display:flex;align-items:center;gap:20px}
.lab:before{content:"";width:0;height:6px;background:#f1bc18;display:block;width:var(--lw,0px)}
.ttl{font-weight:800;line-height:1.04;text-transform:uppercase;letter-spacing:-.01em;transform-style:preserve-3d}
.wd{display:inline-block;margin-right:.26em;white-space:nowrap;transform-style:preserve-3d}
.ch{display:inline-block;transform-origin:50% 100%;will-change:transform}
.g .ch{color:#f1bc18;text-shadow:0 0 40px rgba(241,188,24,.45)}
.sub{font-size:46px;line-height:1.35;font-weight:500;color:#ecdbe6}
.num{width:160px;height:160px;border-radius:34px;background:linear-gradient(135deg,#7a0858,#3c0030);border:3px solid #f1bc18;display:flex;align-items:center;justify-content:center;font-size:88px;font-weight:800;color:#f1bc18;box-shadow:0 0 60px rgba(241,188,24,.35)}
.big{font-weight:800;color:#f1bc18;letter-spacing:-.04em;line-height:.88;position:relative}
.ring{position:absolute;left:50%;top:50%;width:200px;height:200px;margin:-100px;border:10px solid #f1bc18;border-radius:50%;opacity:0}
.cta{align-self:flex-start;background:linear-gradient(90deg,#f1bc18,#ffd75a,#f1bc18);background-size:200% 100%;color:#300024;font-size:52px;font-weight:800;padding:34px 66px;border-radius:999px}
.ul{height:8px;background:#f1bc18;width:0;border-radius:4px;box-shadow:0 0 30px rgba(241,188,24,.6)}
#flare{position:absolute;left:0;top:0;width:1600px;height:14px;margin-left:-800px;border-radius:50%;background:radial-gradient(closest-side,#fff,rgba(255,215,90,.9) 30%,rgba(241,188,24,0));opacity:0;filter:blur(2px)}
#flare2{position:absolute;width:420px;height:420px;margin:-210px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,240,190,.55),rgba(241,188,24,0));opacity:0}
#burst{position:absolute;inset:0;pointer-events:none}#burst b{position:absolute;width:18px;height:18px;background:#f1bc18;opacity:0}
#iris{position:absolute;left:50%;top:50%;border-radius:50%;background:#f1bc18;width:10px;height:10px;transform:translate(-50%,-50%) scale(0)}
#slices{position:absolute;inset:0;pointer-events:none}#slices div{position:absolute;left:0;width:100%;background:#66004a;transform:translateX(-101%)}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.55));pointer-events:none}
#grain{position:absolute;inset:0;opacity:.06;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}
#brand{position:absolute;left:88px;top:120px;display:flex;align-items:center;gap:22px;font-size:28px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#ecdbe6}
#brand img{width:84px;height:84px;border-radius:14px}
#bar{position:absolute;left:0;bottom:0;height:12px;background:#f1bc18;width:0;box-shadow:0 0 20px #f1bc18}
#end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px;opacity:0;transform-style:preserve-3d}
#end .logo{position:relative;width:380px;height:380px;transform-style:preserve-3d}
#end .logo img{position:absolute;inset:0;width:100%;height:100%;border-radius:52px;box-shadow:0 30px 120px rgba(241,188,24,.35)}
#end .pix{position:absolute;width:76px;height:76px;background:#f1bc18}
#end .t1{font-size:74px;font-weight:800;text-transform:uppercase}#end .t2{font-size:40px;font-weight:600;color:#f1bc18}
</style></head><body>
<div id=bg><div id=liq></div><div id=horizon></div><div id=floorwrap><div id=floor></div></div></div>
<div id=stage><div id=world></div></div>
<div id=burst></div>
<div id=brand><img src="%LOGO%">AM.Digital · Abidjan</div>
<div id=end><div class=logo></div><div class=t1>%ENDT1%</div><div class=t2>%ENDT2%</div></div>
<div id=flare></div><div id=flare2></div>
<div id=slices></div><div id=iris></div>
<div id=vig></div><div id=grain></div><div id=bar></div>
<script>
const SC=%SCENES%, TOTAL=%TOTAL%, END=%ENDDUR%;
const C=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), E=x=>1-Math.pow(1-C(x),3), EI=x=>{x=C(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2},
 B=x=>{x=C(x);const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}, R=i=>{const s=Math.sin(i*127.1+311.7)*43758.5453;return s-Math.floor(s)};
// fond liquide
const liq=document.getElementById('liq');const BL=[['#7a0858',1000],['#3c0030',1200],['#a3176f',700],['#c79613',460],['#1e0017',1100],['#66004a',800]].map(([c,s])=>{const d=document.createElement('div');d.style.width=d.style.height=s+'px';d.style.background=c;liq.appendChild(d);return {d,s}});
// cubes 3D
const world=document.getElementById('world');const CU=[];
for(let i=0;i<14;i++){const s=[40,56,72,90,30][i%5];const c=document.createElement('div');c.className='cube';c.style.width=c.style.height=s+'px';
 const h=s/2;['translateZ('+h+'px)','rotateY(180deg) translateZ('+h+'px)','rotateY(90deg) translateZ('+h+'px)','rotateY(-90deg) translateZ('+h+'px)','rotateX(90deg) translateZ('+h+'px)','rotateX(-90deg) translateZ('+h+'px)'].forEach((t,k)=>{const f=document.createElement('i');f.style.transform=t;f.style.filter=`brightness(${[1,.6,.8,.75,1.15,.5][k]})`;c.appendChild(f)});
 world.appendChild(c);CU.push({c,s,a:R(i)*6.28,r:470+R(i+9)*300,y:-760+R(i+3)*1520,z:-650-R(i+5)*900,v:.15+R(i+7)*.35})}
// scènes
const T=['cube','iris','slices','zoom'];let acc=0;
SC.forEach((s,i)=>{s.t0=acc;acc+=s.dur;s.tr=s.tr||T[i%4];const e=document.createElement('div');e.className='scene';e.id='s'+i;e.style.opacity=0;let h='';
 if(s.num) h+=`<div class=num>${s.num}</div>`; if(s.label) h+=`<div class=lab>${s.label}</div>`;
 if(s.big) h+=`<div class=big style="font-size:${s.bigSize||300}px" data-count="${s.count||''}"><span class=bt>${s.big}</span><div class=ring></div></div>`;
 if(s.title){let k=0;const words=s.title.split(' ').map(w=>{const g=w.startsWith('*');w=w.replace(/\*/g,'');return `<span class="wd${g?' g':''}">`+[...w].map(ch=>`<span class=ch data-k="${k++}">${ch}</span>`).join('')+`</span>`}).join(' ');h+=`<div class=ttl style="font-size:${s.size||104}px">${words}</div><div class=ul></div>`}
 if(s.sub) h+=`<div class=sub>${s.sub}</div>`; if(s.cta) h+=`<div class=cta>${s.cta}</div>`;
 e.innerHTML=h;world.appendChild(e)});
// éclats
const burst=document.getElementById('burst');const BU=[];for(let i=0;i<28;i++){const b=document.createElement('b');burst.appendChild(b);BU.push({b,a:R(i+40)*6.28,v:300+R(i+60)*700,s:8+R(i+80)*22})}
const sl=document.getElementById('slices');const SL=[];for(let i=0;i<8;i++){const d=document.createElement('div');d.style.top=(i*240)+'px';d.style.height='241px';d.style.background=i%2?'#66004a':'#f1bc18';sl.appendChild(d);SL.push(d)}
// logo pixels
const lg=document.querySelector('#end .logo');const LP=[];for(let r=0;r<5;r++)for(let c=0;c<5;c++){const p=document.createElement('div');p.className='pix';p.style.left=(c*76)+'px';p.style.top=(r*76)+'px';p.style.background=(r+c)%3?'#f1bc18':'#c79613';lg.appendChild(p);LP.push({p,x:(R(r*5+c)-.5)*2400,y:(R(r*5+c+50)-.5)*3000,z:400+R(r*5+c+90)*1600,k:(r+c)/8})}
const im=document.createElement('img');im.src="%LOGO%";lg.appendChild(im);
function render(t){
 let shake=0, rgb=0, fl=-1, bt=-1, bx=540, by=900, iris=0, slices=-1;
 BL.forEach((o,i)=>{const a=t*.22+i*1.1;o.d.style.left=(840+Math.cos(a*1.1)*520-o.s/2)+'px';o.d.style.top=(1260+Math.sin(a*.9+i)*900-o.s/2)+'px'});
 document.getElementById('floor').style.backgroundPosition=`0 ${(t*160)%120}px`;
 CU.forEach(o=>{const a=o.a+t*o.v;o.c.style.transform=`translate3d(${540+Math.cos(a)*o.r-o.s/2}px,${960+o.y+Math.sin(t*.6+o.a)*60}px,${o.z+Math.sin(a)*180}px) rotateX(${t*40*o.v+o.a*50}deg) rotateY(${t*60*o.v}deg)`});
 // caméra
 let camZ=0,camRY=0,camRX=0;
 SC.forEach((s,i)=>{const e=document.getElementById('s'+i);const lt=t-s.t0;const d=s.dur;
  if(lt<-0.6||lt>d+0.6){e.style.opacity=0;return}
  // entrée / sortie selon transition
  const inP=E(lt/0.55), outP=EI((lt-(d-0.45))/0.45);let tf='',op=1,fi='none';
  const prevTr=i>0?SC[i-1].tr:'zoom';
  if(lt<0){e.style.opacity=0;return}
  if(prevTr=='cube'){tf+=`translateZ(-540px) rotateY(${(1-inP)*90}deg) translateZ(540px) `}
  else if(prevTr=='zoom'){tf+=`translateZ(${(1-inP)*-1200}px) `;fi=inP<1?`blur(${(1-inP)*20}px)`:'none'}
  else if(prevTr=='slices'){tf+=`translateX(${(1-inP)*200}px) `}
  else {tf+=`scale(${1.15-0.15*inP}) `}
  if(lt>d-0.45&&lt<=d){ if(s.tr=='cube'){tf=`translateZ(-540px) rotateY(${-outP*90}deg) translateZ(540px) `+tf;op=1-outP*.6}
   else if(s.tr=='zoom'){tf=`translateZ(${outP*900}px) `+tf;op=1-outP;fi=`blur(${outP*24}px)`}
   else if(s.tr=='slices'){slices=outP;op=1-C(outP*2-1)}
   else {iris=Math.max(iris,outP);op=1-C(outP*2-1)} }
  if(lt>d) {op=0}
  e.style.opacity=C(op*(prevTr=='zoom'?C(inP*1.6):1));e.style.transform=tf;e.style.filter=fi;
  if(lt<0.5&&i>0){iris=Math.max(iris, SC[i-1].tr=='iris'?1-E(lt/0.5):0); if(SC[i-1].tr=='slices') slices=Math.max(slices,1+E(lt/0.5))}
  camZ+= (lt>=0&&lt<d)? 60*Math.sin(lt/d*Math.PI):0; camRY+= (lt>=0&&lt<d)? (i%2?1:-1)*3*(lt/d-.5):0; camRX+= (lt>=0&&lt<d)? 1.5*Math.sin(lt*1.3):0;
  // flare à l'entrée
  if(lt>=0&&lt<0.7&&fl<0){fl=lt/0.7}
  // label
  e.querySelectorAll('.lab').forEach(el=>{const x=E((lt-0.05)/0.5);el.style.opacity=x;el.style.transform=`translateX(${(1-x)*-80}px)`;el.style.setProperty('--lw',(x*70)+'px')});
  e.querySelectorAll('.num').forEach(el=>{const x=B((lt-0.02)/0.55);el.style.opacity=C(x*2);el.style.transform=`rotateY(${(1-x)*-180}deg) scale(${.4+.6*x})`});
  // lettres
  const chs=e.querySelectorAll('.ch');const n=chs.length;const per=Math.min(0.035,0.9/Math.max(1,n));
  chs.forEach(el=>{const k=+el.dataset.k;const x=C((lt-0.15-k*per)/0.5);const b=B(x);el.style.opacity=C(x*3);
   el.style.transform=`translateY(${(1-b)*90}px) rotateX(${(1-E(x))*-95}deg) scale(${.7+.3*b})`;
   if(el.parentNode.classList.contains('g')){const sh=(Math.sin(lt*3-k*.35)+1)/2;el.style.textShadow=`0 0 ${30+40*sh}px rgba(241,188,24,${.35+.35*sh})`;el.style.color=sh>.92?'#fff4c8':'#f1bc18'}});
  const g=e.querySelector('.g .ch');if(g){const gx=C((lt-0.15-(+g.dataset.k)*per-0.3)/0.6);if(gx>0&&gx<1&&bt<0){bt=gx;const r=g.getBoundingClientRect();bx=r.left+r.width/2;by=r.top+r.height/2}}
  e.querySelectorAll('.ul').forEach(el=>{el.style.width=(E((lt-0.15-n*per-0.25)/0.6)*360)+'px'});
  // big
  e.querySelectorAll('.big').forEach(el=>{const x=E((lt-0.08)/0.42);const s2=lt<0.5?(3.2-2.2*x):1+0.02*Math.sin(lt*6);el.style.transform=`scale(${s2})`;el.style.opacity=C(x*2);
   const c=el.dataset.count;const btxt=el.querySelector('.bt');if(c){const[v,suf]=c.split('|');btxt.textContent=Math.round(parseFloat(v)*E((lt-0.1)/1.1)).toLocaleString('fr-FR')+(suf||'')}
   const hit=lt-0.5;if(hit>=0&&hit<0.35){shake=Math.max(shake,(1-hit/0.35)*26);rgb=Math.max(rgb,(1-hit/0.35))}
   const ring=el.querySelector('.ring');const rx=C(hit/0.9);ring.style.opacity=hit>=0?(1-rx):0;ring.style.transform=`scale(${1+rx*9})`;ring.style.borderWidth=(10*(1-rx)+1)+'px';
   btxt.style.textShadow=rgb>0?`${-14*rgb}px 0 #ff2a6d, ${14*rgb}px 0 #2af0ff, 0 0 80px rgba(241,188,24,.5)`:'0 0 80px rgba(241,188,24,.45)'});
  e.querySelectorAll('.sub').forEach(el=>{const x=E((lt-0.75)/0.6);el.style.opacity=x;el.style.transform=`translateY(${(1-x)*60}px)`;el.style.filter=`blur(${(1-x)*10}px)`});
  e.querySelectorAll('.cta').forEach(el=>{const x=B((lt-0.9)/0.55);el.style.transform=`scale(${x*(1+0.035*Math.sin(lt*8))})`;el.style.backgroundPosition=`${(lt*80)%200}% 0`;el.style.boxShadow=`0 0 0 ${((lt*46)%70)}px rgba(241,188,24,${Math.max(0,.55-((lt*46)%70)/127)}), 0 20px 60px rgba(0,0,0,.4)`});
 });
 const sx=shake?(R(t*97)-.5)*shake:0, sy=shake?(R(t*53)-.5)*shake:0;
 world.style.transform=`translate(${sx}px,${sy}px) translateZ(${camZ}px) rotateY(${camRY}deg) rotateX(${camRX}deg)`;
 document.getElementById('bg').style.transform=`translate(${sx*.5}px,${sy*.5}px) scale(1.04)`;
 // flare
 const F=document.getElementById('flare'),F2=document.getElementById('flare2');
 if(fl>=0&&fl<1){const x=-300+fl*1680;F.style.opacity=Math.sin(fl*Math.PI);F.style.transform=`translate(${x}px,700px) scaleY(${1+2*Math.sin(fl*Math.PI)})`;F2.style.opacity=Math.sin(fl*Math.PI)*.8;F2.style.left=x+'px';F2.style.top='707px'}else{F.style.opacity=0;F2.style.opacity=0}
 // éclats
 BU.forEach(o=>{if(bt>=0&&bt<1){const x=E(bt);o.b.style.opacity=1-bt;o.b.style.width=o.b.style.height=o.s*(1-bt*.6)+'px';o.b.style.transform=`translate(${bx+Math.cos(o.a)*o.v*x}px,${by+Math.sin(o.a)*o.v*x}px) rotate(${bt*400}deg)`}else o.b.style.opacity=0});
 // iris / tranches
 const ir=document.getElementById('iris');ir.style.transform=`translate(-50%,-50%) scale(${iris*460})`;ir.style.opacity=iris>0?1:0;
 SL.forEach((d,k)=>{let x=-101;if(slices>=0&&slices<=1)x=-101+101*E(slices*1.3-k*.04);else if(slices>1)x=101*E((slices-1)*1.3-k*.04);d.style.transform=`translateX(${x}%)`});
 document.getElementById('bar').style.width=(C(t/(TOTAL+END))*1080)+'px';
 // fin
 const et=t-TOTAL;const end=document.getElementById('end');const brand=document.getElementById('brand');
 if(et>=-0.2){end.style.opacity=C((et+.2)/0.3);brand.style.opacity=0;
  LP.forEach(o=>{const x=EI((et-o.k*0.25)/0.7);o.p.style.transform=`translate3d(${o.x*(1-x)}px,${o.y*(1-x)}px,${o.z*(1-x)}px) rotateX(${(1-x)*360}deg)`;o.p.style.opacity=et>0.95?C(1-(et-0.95)/0.2):1});
  const lx=B((et-0.9)/0.5);im.style.opacity=C((et-0.85)/0.15);im.style.transform=`scale(${.6+.4*lx}) rotateY(${(1-lx)*90}deg)`;
  end.querySelector('.t1').style.opacity=E((et-1.1)/0.4);end.querySelector('.t1').style.transform=`translateY(${(1-E((et-1.1)/0.4))*40}px)`;
  end.querySelector('.t2').style.opacity=E((et-1.35)/0.4);
  if(et>0.85&&et<1.1){rgb=Math.max(rgb,1-(et-.85)/.25)}
  world.style.opacity=C(1-(et+.2)/0.3)}
 else{end.style.opacity=0;brand.style.opacity=C(t/0.6);world.style.opacity=1}
 document.body.style.filter=rgb>0.05?`saturate(${1+rgb*.6}) contrast(${1+rgb*.15})`:'none';
}
window.render=render;
</script></body></html>"""
def build(spec, out, music=None, endt1="Abonnez-vous", endt2="@amdigital204 · Facebook · TikTok", enddur=2.8, seed=0):
    total=sum(s["dur"] for s in spec)
    html=HTML.replace("%FONT%",FONT).replace("%LOGO%",LOGO).replace("%SCENES%",json.dumps(spec)).replace("%TOTAL%",str(total)).replace("%ENDDUR%",str(enddur)).replace("%ENDT1%",endt1).replace("%ENDT2%",endt2)
    tmp=out+".html"; open(tmp,"w").write(html)
    dur=total+enddur; n=int(round(dur*FPS)); vf=out+".video.mp4"
    ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",vf],stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--allow-file-access-from-files"]);pg=b.new_page(viewport={"width":W,"height":H})
        pg.goto("file://"+tmp);pg.evaluate("document.fonts.ready");pg.wait_for_timeout(500)
        for i in range(n):
            pg.evaluate(f"render({i/FPS})"); ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
        b.close()
    ff.stdin.close();ff.wait()
    if not music:
        import music as M
        music=out+".wav"; acc=0; hits=[]
        for s in spec:
            if s.get("big"): hits.append(acc+0.5)
            acc+=s["dur"]
        M.make(dur+1, music, seed=seed, impacts=tuple(hits)+(total+0.85,))
    subprocess.run(["ffmpeg","-v","error","-y","-i",vf,"-i",music,"-filter_complex",f"[1:a]atrim=0:{dur},afade=t=in:d=0.2,afade=t=out:st={dur-1.0}:d=1.0,loudnorm=I=-14:TP=-1.5:LRA=9[a]","-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","44100","-shortest",out],check=True)
    os.remove(vf); os.remove(tmp); return dur
