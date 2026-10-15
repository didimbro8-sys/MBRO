"""Voix off AM.Digital : mastering de la voix du fondateur + mixage sur une vidéo motion3.
Usage : python3 voice.py VIDEO.mp4 VOIX.(m4a|mp3|wav) SORTIE.mp4 [decalage_s=0.3] [musique.wav]
Chaîne voix : passe-haut 80 Hz, débruitage FFT, coupe 250 Hz, présence +3 dB à 3,5 kHz, air +2 dB à 10 kHz,
de-esser, compression 3:1, limiteur, -16 LUFS. Musique : baissée automatiquement (sidechain) quand la voix parle."""
import subprocess, sys, os
def master(src, out):
    chain=("highpass=f=80,afftdn=nf=-25:tn=1,silenceremove=start_periods=1:start_threshold=-45dB,"
           "equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=3,equalizer=f=10000:t=h:w=0.8:g=2,"
           "deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,"
           "alimiter=limit=0.89,loudnorm=I=-16:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-af",chain,"-ar","48000","-ac","1",out],check=True)
def mix(video, voice, out, delay=0.3, music=None):
    v=out+".voice.wav"; master(voice, v)
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",video]).strip())
    ms=int(delay*1000)
    if music: inputs=["-i",video,"-i",v,"-i",music]; mus="[2:a]"
    else: inputs=["-i",video,"-i",v]; mus="[0:a]"
    fc=(f"[1:a]adelay={ms}|{ms},apad,atrim=0:{dur},aformat=channel_layouts=stereo,asplit=2[vo][sc];"
        f"{mus}atrim=0:{dur},volume=0.9[m];"
        f"[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350:makeup=1[md];"
        f"[md][vo]amix=inputs=2:duration=first:weights=0.55 1,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    subprocess.run(["ffmpeg","-v","error","-y",*inputs,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","44100",out],check=True)
    os.remove(v); return out
if __name__=="__main__":
    a=sys.argv; mix(a[1],a[2],a[3],float(a[4]) if len(a)>4 else 0.3, a[5] if len(a)>5 else None)
