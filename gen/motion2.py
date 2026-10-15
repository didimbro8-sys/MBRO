"""Moteur motion design AM.Digital v2 : rendu HTML/CSS image par image (Playwright) -> MP4 1080x1920.
Effets : fond aurore animé, particules pixels en parallaxe, typo cinétique (flou -> net, rebond), balayage de lumière sur les mots or,
transitions (zoom-through + flash, volet de pixels, glitch RGB), compteur animé, poussée caméra, logo final assemblé en pixels, synchro musique."""
import json, subprocess, sys, os
from playwright.sync_api import sync_playwright
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
FONT="".join(f"@font-face{{font-family:M;font-weight:{w};src:url('file://{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2')}}" for w in (500,600,700,800))
LOGO=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
W,H,FPS=1080,1920,30
HTML=r"""<!doctype html><html><head><meta charset=utf-8><style>%FONT%
*{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#1e0017;font-family:M,Arial,sans-serif;color:#fff}
#bg{position:absolute;inset:-200px;filter:blur(60px)}
.blob{position:absolute;border-radius:50%;opacity:.85}
#grain{position:absolute;inset:0;opacity:.07;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}
#px{position:absolute;inset:0}.p{position:absolute;background:#f1bc18}
#cam{position:absolute;inset:0}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 90px;gap:34px}
.lab{font-size:34px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#f1bc18}
.ttl{font-weight:800;line-height:1.02;text-transform:uppercase;letter-spacing:-.01em}
.w{display:inline-block;margin-right:.24em;will-change:transform,filter,opacity}
.g{color:#f1bc18;background:linear-gradient(100deg,#f1bc18 0%,#f1bc18 40%,#fff6cf 50%,#f1bc18 60%,#f1bc18 100%);background-size:300% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.sub{font-size:46px;line-height:1.35;font-weight:500;color:#e6d3df}
.num{width:150px;height:150px;border-radius:30px;background:linear-gradient(135deg,#66004a,#8a1a68);display:flex;align-items:center;justify-content:center;font-size:84px;font-weight:800;color:#f1bc18;box-shadow:0 20px 60px rgba(0,0,0,.4)}
.big{font-weight:800;color:#f1bc18;letter-spacing:-.04em;line-height:.9;text-shadow:0 0 60px rgba(241,188,24,.35)}
.cta{align-self:flex-start;background:#f1bc18;color:#300024;font-size:52px;font-weight:800;padding:34px 64px;border-radius:999px;box-shadow:0 0 0 0 rgba(241,188,24,.6)}
#wipe{position:absolute;inset:0;display:grid;grid-template-columns:repeat(9,1fr);grid-template-rows:repeat(16,1fr);pointer-events:none}
#wipe div{background:#f1bc18;transform:scale(0)}
#flash{position:absolute;inset:0;background:#fff;opacity:0}
#bar{position:absolute;left:0;bottom:0;height:12px;background:#f1bc18;width:0}
#brand{position:absolute;left:90px;top:120px;display:flex;align-items:center;gap:22px;font-size:28px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#e6d3df}
#brand img{width:84px;height:84px;border-radius:14px}
#end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;opacity:0}
#end .logo{position:relative;width:360px;height:360px}
#end .logo img{width:100%;height:100%;border-radius:48px;box-shadow:0 30px 90px rgba(0,0,0,.5)}
#end .t1{font-size:70px;font-weight:800;text-transform:uppercase}#end .t2{font-size:40px;font-weight:600;color:#f1bc18}
</style></head><body>
<div id=bg></div><div id=px></div><div id=grain></div>
<div id=cam></div>
<div id=brand><img src="%LOGO%">AM.Digital · Abidjan</div>
<div id=end><div class=logo><img src="%LOGO%"></div><div class=t1>%ENDT1%</div><div class=t2>%ENDT2%</div></div>
<div id=wipe></div><div id=flash></div><div id=bar></div>
<script>
const SC=%SCENES%, TOTAL=%TOTAL%, END=%ENDDUR%;
const ease=x=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3), back=x=>{x=Math.min(1,Math.max(0,x));const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
// fond
const bg=document.getElementById('bg');const blobs=[['#66004a',900],['#3c0030',1100],['#8a1a68',700],['#c79613',420],['#300024',1000]].map(([c,s],i)=>{const d=document.createElement('div');d.className='blob';d.style.width=d.style.height=s+'px';d.style.background=c;bg.appendChild(d);return d});
// particules
const px=document.getElementById('px');const P=[];for(let i=0;i<46;i++){const d=document.createElement('div');d.className='p';const s=[10,14,18,24,32][i%5];d.style.width=d.style.height=s+'px';d.style.opacity=(.25+(i%7)/10).toFixed(2);if(i%4==0)d.style.background='#c79613';px.appendChild(d);P.push({d,x:(i*197)%1080,y:(i*331)%1920,v:20+(i%6)*14,z:s})}
// volet
const wipe=document.getElementById('wipe');const WC=[];for(let r=0;r<16;r++)for(let c=0;c<9;c++){const d=document.createElement('div');wipe.appendChild(d);WC.push({d,k:(r+c)/24})}
// scènes
const cam=document.getElementById('cam');
SC.forEach((s,i)=>{const e=document.createElement('div');e.className='scene';e.id='s'+i;e.style.opacity=0;let h='';
 if(s.num) h+=`<div class=num>${s.num}</div>`; if(s.label) h+=`<div class=lab>${s.label}</div>`;
 if(s.big) h+=`<div class=big style="font-size:${s.bigSize||300}px" data-count="${s.count||''}">${s.big}</div>`;
 if(s.title){const words=s.title.split(' ').map(w=>{const g=w.startsWith('*');w=w.replace(/\*/g,'');return `<span class="w${g?' g':''}">${w}</span>`}).join('');h+=`<div class=ttl style="font-size:${s.size||104}px">${words}</div>`}
 if(s.sub) h+=`<div class=sub>${s.sub}</div>`; if(s.cta) h+=`<div class=cta>${s.cta}</div>`;
 e.innerHTML=h;cam.appendChild(e)});
let acc=0;SC.forEach(s=>{s.t0=acc;acc+=s.dur});
function render(t){
 // fond aurore
 blobs.forEach((b,i)=>{const a=t*.18+i*1.3;b.style.left=(540+Math.cos(a)*380-parseInt(b.style.width)/2+200)+'px';b.style.top=(960+Math.sin(a*1.3+i)*700-parseInt(b.style.height)/2+200)+'px'});
 P.forEach(p=>{let y=(p.y - t*p.v)%1920; if(y<0)y+=1920; p.d.style.transform=`translate(${p.x+Math.sin(t*.8+p.z)*18}px,${y}px) rotate(${(t*20+p.z)%360}deg)`});
 cam.style.transform=`scale(${1+0.03*Math.sin(t*.35)}) rotate(${0.4*Math.sin(t*.25)}deg)`;
 document.getElementById('bar').style.width=(clamp(t/(TOTAL+END))*1080)+'px';
 let flash=0, wp=-1;
 SC.forEach((s,i)=>{const e=document.getElementById('s'+i);const lt=t-s.t0;const vis=lt>=-0.001&&lt<s.dur;
  if(!vis){e.style.opacity=0;return}
  const out=clamp((lt-(s.dur-0.35))/0.35);
  e.style.opacity=1-out; e.style.transform=`scale(${1+out*0.6})`; e.style.filter=out>0?`blur(${out*14}px)`:'none';
  if(lt<0.12) flash=Math.max(flash,(0.1-lt)/0.1*0.3);
  e.querySelectorAll('.lab,.num').forEach((el,k)=>{const x=ease((lt-0.05)/0.45);el.style.opacity=x;el.style.transform=`translateY(${(1-x)*-40}px)`});
  e.querySelectorAll('.w').forEach((el,k)=>{const x=clamp((lt-0.12-k*0.07)/0.42);const b=back(x);el.style.opacity=clamp(x*2);el.style.transform=`translateY(${(1-b)*120}px) scale(${0.6+0.4*b}) rotate(${(1-b)*-6}deg)`;el.style.filter=`blur(${(1-ease(x))*16}px)`;
    if(el.classList.contains('g')) el.style.backgroundPosition=`${100-((lt*55)%300)}% 0`});
  e.querySelectorAll('.big').forEach(el=>{const x=back((lt-0.1)/0.6);el.style.transform=`scale(${0.3+0.7*x})`;el.style.opacity=clamp(x*1.5);const c=el.dataset.count;if(c){const[v,suf]=c.split('|');el.textContent=Math.round(parseFloat(v)*ease((lt-0.1)/1.1)).toLocaleString('fr-FR')+(suf||'')}
    const gl=(lt>0.7&&lt<0.8)?1:0;el.style.textShadow=gl?'-8px 0 #ff2a6d, 8px 0 #2af0ff':'0 0 60px rgba(241,188,24,.35)'});
  e.querySelectorAll('.sub').forEach(el=>{const x=ease((lt-0.55)/0.5);el.style.opacity=x;el.style.transform=`translateY(${(1-x)*50}px)`});
  e.querySelectorAll('.cta').forEach(el=>{const x=back((lt-0.7)/0.5);el.style.transform=`scale(${x*(1+0.04*Math.sin(lt*7))})`;el.style.boxShadow=`0 0 0 ${((lt*40)%60)}px rgba(241,188,24,${0.5-((lt*40)%60)/120})`});
  if(s.wipe && lt>s.dur-0.45) wp=(lt-(s.dur-0.45))/0.45;
 });
 // volet pixels
 WC.forEach(c=>{let v=0;if(wp>=0){const a=clamp(wp*2-c.k), b=clamp(wp*2-1-c.k);v=a-b}c.d.style.transform=`scale(${v})`});
 // fin
 const et=t-TOTAL;const end=document.getElementById('end');const brand=document.getElementById('brand');
 if(et>=0){const x=back(et/0.6);end.style.opacity=clamp(et/0.3);end.querySelector('.logo').style.transform=`scale(${0.2+0.8*x}) rotate(${(1-x)*-20}deg)`;brand.style.opacity=0;if(et<0.1)flash=0.3}else{end.style.opacity=0;brand.style.opacity=clamp(t/0.5)}
 document.getElementById('flash').style.opacity=flash;
}
window.render=render;
</script></body></html>"""
def build(spec, out, music=None, endt1="Abonnez-vous", endt2="@amdigital204 · Facebook · TikTok", enddur=2.6):
    scenes=spec; total=sum(s["dur"] for s in scenes)
    html=HTML.replace("%FONT%",FONT).replace("%LOGO%",LOGO).replace("%SCENES%",json.dumps(scenes)).replace("%TOTAL%",str(total)).replace("%ENDDUR%",str(enddur)).replace("%ENDT1%",endt1).replace("%ENDT2%",endt2)
    tmp=S+"/gen/m2.html"; open(tmp,"w").write(html)
    dur=total+enddur; n=int(dur*FPS)
    vf=out+".video.mp4"
    ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",vf],stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--allow-file-access-from-files"]);pg=b.new_page(viewport={"width":W,"height":H})
        pg.goto("file://"+tmp);pg.evaluate("document.fonts.ready");pg.wait_for_timeout(400)
        for i in range(n):
            pg.evaluate(f"render({i/FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
        b.close()
    ff.stdin.close();ff.wait()
    if music and os.path.exists(music):
        subprocess.run(["ffmpeg","-v","error","-y","-i",vf,"-i",music,"-filter_complex",f"[1:a]atrim=0:{dur},afade=t=in:d=0.3,afade=t=out:st={dur-1.2}:d=1.2,volume=0.9[a]","-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out],check=True)
    else:
        subprocess.run(["ffmpeg","-v","error","-y","-i",vf,"-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-c:v","copy","-c:a","aac","-shortest",out],check=True)
    os.remove(vf); return dur
