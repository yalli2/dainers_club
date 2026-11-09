import sys, os, html, base64, subprocess, shutil
sys.path.insert(0, os.path.dirname(__file__))
from content import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = open(f"{ROOT}/assets/logo.svg").read()
e = html.escape
CSS = """
*{box-sizing:border-box;margin:0}body{font-family:Inter,'DejaVu Sans',sans-serif;color:#14213D}
.logo{position:absolute;width:150px;height:40px;opacity:.9}.logo svg{width:100%;height:100%}
"""
def logo(pos, color):
    return f'<div class="logo" style="{pos};color:{color}">{LOGO}</div>'
def slide(inner, bg="#F7F3EA", n=0, total=10, dark=False, lang="en"):
    fg = "#fff" if dark else "#14213D"
    return f"""<html><head><meta charset=utf-8><style>{CSS}
.s{{width:1080px;height:1350px;position:relative;background:{bg};color:{fg};padding:90px 80px;overflow:hidden}}
.tag{{display:inline-block;background:#FFC83D;color:#14213D;font-weight:800;letter-spacing:2px;font-size:26px;padding:10px 22px;border-radius:30px}}
h1{{font-size:68px;line-height:1.08;font-weight:800;margin:36px 0 30px}}
li{{font-size:35px;line-height:1.35;margin-bottom:20px;list-style:none;padding-left:44px;position:relative}}
li:before{{content:'';position:absolute;left:0;top:18px;width:18px;height:18px;background:#FFC83D;border-radius:50%}}
.kw{{position:absolute;left:80px;right:80px;bottom:150px;background:#14213D;color:#fff;border-radius:28px;padding:30px 36px}}
.kw b{{color:#FFC83D}}.kw div{{font-size:27px;line-height:1.5}}.kw h4{{font-size:22px;letter-spacing:3px;color:#FFC83D;margin-bottom:10px}}
.foot{{position:absolute;left:80px;right:80px;bottom:50px;font-size:22px;opacity:.7;display:flex;justify-content:space-between}}
</style></head><body><div class=s>{inner}
<div class=foot><span>{n}/{total}</span></div></div></body></html>"""

def slides(C):
    out=[]; T=10
    # cover
    out.append(slide(f"""<div class=tag>{e(C['date'])}</div>
    <div style="position:absolute;top:330px;left:80px;right:80px"><h1 style="font-size:104px;color:#FFC83D">{e(C['title'])}</h1>
    <p style="font-size:46px;line-height:1.35">{e(C['sub'])}</p></div>
    <p style="position:absolute;bottom:130px;left:80px;font-size:36px;opacity:.85">{e(C['video_hook'])} →</p>
    {logo('top:60px;right:70px','#fff')}""", bg="#14213D", n=1, dark=True))
    for i,s in enumerate(C['stories']):
        words="".join(f"<div><b>{e(w)}</b> — {e(d)}</div>" for w,d in s['words'])
        out.append(slide(f"""<div class=tag>{e(s['tag'])}</div><h1>{e(s['head'])}</h1>
        <ul style="padding:0">{''.join(f'<li>{e(b)}</li>' for b in s['body'])}</ul>
        <div class=kw><h4>{'KEY WORDS' if C['lang']=='en' else 'PALABRAS CLAVE'}</h4>{words}</div>
        {logo('bottom:40px;right:70px','#14213D')}""", n=i+2))
    out.append(slide(f"""<div class=tag>{'VOCAB' if C['lang']=='en' else 'VOCABULARIO'}</div><h1>{e(C['vocab_title'])}</h1><p style="font-size:34px;margin-bottom:40px">{e(C['vocab_intro'])}</p>
    {''.join(f'<div style="background:#fff;border-radius:22px;padding:22px 30px;margin-bottom:20px"><span style="font-size:44px;font-weight:800">{e(w)}</span> <i style="opacity:.6;font-size:26px">{e(t)}</i><div style="font-size:30px;margin-top:6px">{e(x)}</div></div>' for w,t,x in C['vocab'])}
    {logo('bottom:40px;right:70px','#14213D')}""", n=7))
    out.append(slide(f"""<div class=tag>{'GRAMMAR' if C['lang']=='en' else 'GRAMÁTICA'}</div><h1>{e(C['grammar_title'])}</h1>
    <ul style="padding:0">{''.join(f'<li>{e(g)}</li>' for g in C['grammar'])}</ul>{logo('bottom:40px;right:70px','#14213D')}""", n=8))
    out.append(slide(f"""<div class=tag>QUIZ</div><h1>{e(C['quiz_title'])}</h1>
    {''.join(f'<div style="margin-bottom:34px"><div style="font-size:40px;font-weight:700">{i+1}. {e(q)}</div><div style="font-size:30px;opacity:.55;margin-top:6px">{"Answer" if C["lang"]=="en" else "Respuesta"}: {e(a)}</div></div>' for i,(q,a) in enumerate(C['quiz']))}
    {logo('bottom:40px;right:70px','#14213D')}""", n=9))
    srcs=sorted({x.strip() for s in C['stories'] for x in s['src'].split(',')})
    out.append(slide(f"""<div style="margin-top:260px"><h1 style="font-size:84px;color:#FFC83D">{e(C['outro'])}</h1></div>
    <p style="font-size:28px;line-height:1.5;margin-top:50px;opacity:.85"><b>{e(C['sources_title'])}:</b> {e(', '.join(srcs))}</p>
    <p style="font-size:24px;margin-top:30px;opacity:.7">{e(C['note'])}</p>{logo('top:60px;right:70px','#fff')}""", bg="#14213D", n=10, dark=True))
    return out

def pdf_html(C):
    srcs=sorted({x.strip() for s in C['stories'] for x in s['src'].split(',')})
    st="".join(f"""<section><span class=tag>{e(s['tag'])}</span><h2>{e(s['head'])}</h2><ul>{''.join(f'<li>{e(b)}</li>' for b in s['body'])}</ul>
      <table>{''.join(f'<tr><td><b>{e(w)}</b></td><td>{e(d)}</td></tr>' for w,d in s['words'])}</table><small>{e(s['src'])}</small></section>""" for s in C['stories'])
    return f"""<html><head><meta charset=utf-8><style>{CSS}
@page{{size:A4;margin:16mm 15mm 18mm}}body{{font-size:11pt;line-height:1.45}}
header{{background:#14213D;color:#fff;padding:16px 20px;border-radius:10px;margin-bottom:14px;position:relative}}header h1{{color:#FFC83D;font-size:22pt}}
header .logo{{top:14px;right:16px;width:110px;height:30px}}
section{{break-inside:avoid;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #ddd}}
.tag{{background:#FFC83D;font-weight:800;font-size:8pt;padding:3px 10px;border-radius:12px;letter-spacing:1px}}
h2{{font-size:15pt;margin:6px 0}}ul{{padding-left:18px;margin:4px 0}}table{{margin-top:6px;font-size:9.5pt;background:#F7F3EA;width:100%;border-radius:6px}}td{{padding:3px 8px;vertical-align:top}}
small{{color:#666}}h3{{margin:10px 0 4px}}.pb{{break-before:page}}
.f{{position:fixed;bottom:-12mm;right:0;width:80px;height:22px;color:#14213D}}.f svg{{width:100%;height:100%}}
</style></head><body><div class=f>{LOGO}</div>
<header>{logo('','#fff')}<div style="font-size:9pt">{e(C['date'])}</div><h1>{e(C['title'])}</h1><div>{e(C['sub'])}</div></header>
{st}
<div class=pb></div><h3>{e(C['vocab_title'])}</h3><p>{e(C['vocab_intro'])}</p><table>{''.join(f'<tr><td><b>{e(w)}</b> <i>{e(t)}</i></td><td>{e(x)}</td></tr>' for w,t,x in C['vocab'])}</table>
<h3>{e(C['grammar_title'])}</h3><ul>{''.join(f'<li>{e(g)}</li>' for g in C['grammar'])}</ul>
<h3>{e(C['quiz_title'])}</h3><ol>{''.join(f'<li>{e(q)} <small>→ {e(a)}</small></li>' for q,a in C['quiz'])}</ol>
<p style="margin-top:14px"><b>{e(C['sources_title'])}:</b> {e(', '.join(srcs))}</p><small>{e(C['note'])}</small></body></html>"""

def build(C, code):
    d=f"{ROOT}/newsletters/{DATE}/{code}"; os.makedirs(d,exist_ok=True)
    import json
    hs=slides(C)
    for i,h in enumerate(hs,1): open(f"{d}/_s{i:02d}.html","w").write(h)
    open(f"{d}/_pdf.html","w").write(pdf_html(C))
    subprocess.run(["node",f"{ROOT}/tools/render.js",d,str(len(hs)),f"newsletter_{code}_{DATE}.pdf"],check=True)
    for f in os.listdir(d):
        if f.startswith("_"): os.remove(f"{d}/{f}")
    # 60s video: 10 slides x 6s, fade transitions
    inputs=[]; 
    for i in range(1,11): inputs+=["-loop","1","-t","6.5","-i",f"{d}/slide_{i:02d}.png"]
    f=""; 
    for i in range(10): f+=f"[{i}:v]scale=1080:1350,setsar=1,fps=30,format=yuv420p[v{i}];"
    last="v0"
    for i in range(1,10):
        f+=f"[{last}][v{i}]xfade=transition=fade:duration=0.5:offset={6*i}[x{i}];"; last=f"x{i}"
    subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",f.rstrip(';'),"-map",f"[{last}]","-t","60","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",f"{d}/video_{code}_{DATE}.mp4"],check=True)
build(EN,"en"); build(ES,"es")
