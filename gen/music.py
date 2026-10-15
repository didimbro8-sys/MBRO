"""Musique signature AM.Digital : afro-house 122 BPM synthétisée (numpy), libre de droits."""
import numpy as np, wave, sys
SR=44100
def env(n,a=0.002,d=0.2):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/d); return e
def kick(n=int(SR*.45)):
    t=np.arange(n)/SR; f=48+120*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7)*1.0 + np.sin(ph*2)*np.exp(-t*30)*.15
def clap(n=int(SR*.25)):
    rng=np.random.default_rng(1); x=rng.normal(0,1,n); e=np.zeros(n)
    for o in (0,.011,.022): i=int(o*SR); e[i:]+=np.exp(-np.arange(n-i)/SR*38)
    from numpy.fft import rfft,irfft
    X=rfft(x); fr=np.fft.rfftfreq(n,1/SR); X[(fr<900)|(fr>5000)]*=0.15; return irfft(X,n)*e*.5
def hat(n=int(SR*.06),dec=60):
    rng=np.random.default_rng(2); x=rng.normal(0,1,n); x=np.diff(np.concatenate([[0],x])); from numpy.fft import rfft,irfft
    X=rfft(x); fr=np.fft.rfftfreq(n,1/SR); X[(fr<6000)|(fr>14000)]*=0.1; x=irfft(X,n)
    return x*np.exp(-np.arange(n)/SR*dec)*.035
def shaker(n=int(SR*.09)):
    rng=np.random.default_rng(3); x=rng.normal(0,1,n); t=np.arange(n)/SR; return x*np.sin(np.pi*t/(n/SR))**2*.012
def logdrum(freq,n=int(SR*.5)):
    t=np.arange(n)/SR; f=freq*(1+0.6*np.exp(-t*30)); ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)+.3*np.sin(2*ph)+.1*np.sin(3*ph))*np.exp(-t*5)*.55
def marimba(freq,n=int(SR*.6)):
    t=np.arange(n)/SR; return (np.sin(2*np.pi*freq*t)+.25*np.sin(2*np.pi*freq*4*t)*np.exp(-t*20))*np.exp(-t*6)*env(n,.002,5)*.22
def pad(freqs,n):
    t=np.arange(n)/SR; x=sum(np.sin(2*np.pi*f*t+np.sin(2*np.pi*.3*t))+.5*np.sin(2*np.pi*f*1.005*t) for f in freqs)/len(freqs)
    a=np.minimum(1,t/.4)*np.minimum(1,(n/SR-t)/.4); return x*a*.06
def riser(n):
    rng=np.random.default_rng(4); x=rng.normal(0,1,n); t=np.linspace(0,1,n)
    from numpy.fft import rfft,irfft
    out=np.zeros(n); seg=2048
    for i in range(0,n,seg):
        s=x[i:i+seg]; X=rfft(s); fr=np.fft.rfftfreq(len(s),1/SR); cut=300+8000*t[i]**2; X[fr>cut]=0; out[i:i+len(s)]=irfft(X,len(s))
    return out*t**2*.25
def impact(n=int(SR*1.2)):
    t=np.arange(n)/SR; return (np.sin(2*np.pi*(40+60*np.exp(-t*8))*t)*np.exp(-t*3)*.8+np.random.default_rng(5).normal(0,1,n)*np.exp(-t*12)*.15)
def note(m): return 440*2**((m-69)/12)
def make(dur, out, bpm=122, seed=0, impacts=()):
    n=int(dur*SR)+SR; L=np.zeros(n); R=np.zeros(n)
    beat=60/bpm; s16=beat/4
    def add(x,t,pan=0.,g=1.):
        i=int(t*SR); j=min(n,i+len(x)); 
        if i>=n: return
        L[i:j]+=x[:j-i]*g*(1-max(0,pan)); R[i:j]+=x[:j-i]*g*(1+min(0,pan))
    chords=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]  # Am F C G
    bass=[45,41,36,43]
    bars=int(dur/(beat*4))+1
    K,C,Hh,Sh=kick(),clap(),hat(),shaker()
    for b in range(bars):
        t0=b*beat*4; ch=chords[b%4]
        intro = b<1
        add(pad([note(m) for m in ch],int(beat*4*SR)),t0,0,1)
        for k in range(4):
            if not intro: add(K,t0+k*beat,0,1)
            if k in (1,3) and not intro: add(C,t0+k*beat,.1,.9)
        for k in range(16):
            sw=0.012 if k%2 else 0
            add(Hh,t0+k*s16+sw,-.3,.9 if k%4==2 else .45)
            add(Sh,t0+k*s16+sw,.35,1)
        # log drum bass syncopé
        for k,off in enumerate([0,3,6,10,12,14]):
            if not intro: add(logdrum(note(bass[b%4]+(12 if k==4 else 0))),t0+off*s16,0,.9)
        # marimba arpège
        arp=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+24,ch[2]+12,ch[0]+24,ch[1]+12,ch[2]+12]
        for k,m in enumerate(arp):
            add(marimba(note(m)),t0+k*2*s16+(0.01 if k%2 else 0),(-.4 if k%2 else .4),1)
        if b%4==3: add(riser(int(beat*4*SR)),t0,0,1)
    for it in impacts: add(impact(),it,0,.9)
    mix=np.stack([L,R],1)[:int(dur*SR)]
    # compression douce + normalisation
    mix/=np.max(np.abs(mix)); mix=np.tanh(mix*1.1)/np.tanh(1.1); mix*=0.89
    fade=int(1.0*SR); mix[-fade:]*=np.linspace(1,0,fade)[:,None]
    w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()
if __name__=="__main__":
    make(float(sys.argv[1]), sys.argv[2])
