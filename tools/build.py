import sys, os, html, base64, subprocess, shutil
sys.path.insert(0, os.path.dirname(__file__))
from content import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = "data:image/jpeg;base64,"+base64.b64encode(open(f"{ROOT}/assets/dain_logo.jpg","rb").read()).decode()
e = html.escape
CSS = """
*{box-sizing:border-box;margin:0}body{font-family:Inter,'WenQuanYi Zen Hei','DejaVu Sans',sans-serif;color:#14213D}
.ko{font-size:25px;line-height:1.4;color:#C0392B;margin-top:4px}.kh{font-size:32px;font-weight:700;color:#C0392B;margin-bottom:22px}
"""
def logo(pos, color):
    return f'<div class="logo" style="{pos};color:{color}">{LOGO}</div>'
def slide(inner, bg="#F7F3EA", n=0, total=10, dark=False, lang="en"):
    fg = "#fff" if dark else "#14213D"
    return f"""<html><head><meta charset=utf-8><style>{CSS}
.s{{width:1080px;height:1350px;position:relative;background:{bg};color:{fg};padding:70px 80px;overflow:hidden}}
.tag{{display:inline-block;background:#FFC83D;color:#14213D;font-weight:800;letter-spacing:2px;font-size:26px;padding:10px 22px;border-radius:30px}}
h1{{font-size:56px;line-height:1.08;font-weight:800;margin:28px 0 12px}}
li{{font-size:30px;line-height:1.3;margin-bottom:16px;list-style:none;padding-left:44px;position:relative}}
li:before{{content:'';position:absolute;left:0;top:18px;width:18px;height:18px;background:#FFC83D;border-radius:50%}}
.kw{{position:absolute;left:80px;right:80px;bottom:120px;background:#14213D;color:#fff;border-radius:28px;padding:22px 30px}}
.kw b{{color:#FFC83D}}.kw div{{font-size:23px;line-height:1.45}}.kw h4{{font-size:22px;letter-spacing:3px;color:#FFC83D;margin-bottom:10px}}
.foot{{position:absolute;left:80px;right:80px;bottom:50px;font-size:22px;opacity:.7;display:flex;justify-content:space-between}}
</style></head><body><div class=s>{inner}
<div class=foot><span>{n}/{total}</span></div></div></body></html>"""


PUB = [("발행처","다인에듀"),("발행인","황부연"),("발행일","2026년 11월 9일"),("사업자등록번호","892-35-00546"),("연락처","031-429-0701"),("홈페이지","www.dainedu.net")]
def pubbox(fs=26):
    rows="".join(f"<div><b>{k}</b> : {v}</div>" for k,v in PUB)
    return f'<div style="border:3px solid #14213D;border-radius:18px;padding:22px 30px;background:#fff;font-size:{fs}px;line-height:1.55;color:#14213D;display:flex;gap:16px;align-items:center"><img src="{LOGO}" style="width:110px;height:110px;border-radius:12px"><div>{rows}</div></div>'
def dlogo(pos, size=84):
    return f'<img src="{LOGO}" style="position:absolute;{pos};width:{size}px;height:{size}px;border-radius:12px">'

def slides(C):
    K=C['ko']; out=[]; en=C['lang']=='en'
    kw_t='KEY WORDS · 핵심 단어' if en else 'PALABRAS CLAVE · 핵심 단어'
    out.append(slide(f"""<div class=tag>{e(C['date'])} · {DATE_KO}</div>
    <div style="position:absolute;top:300px;left:80px;right:80px"><h1 style="font-size:96px;color:#FFC83D">{e(C['title'])}</h1>
    <p style="font-size:50px;font-weight:700;margin-bottom:26px">{e(K['title'])}</p>
    <p style="font-size:42px;line-height:1.35">{e(C['sub'])}<br><span style="opacity:.8;font-size:36px">{e(K['sub'])}</span></p></div>
    <p style="position:absolute;bottom:130px;left:80px;font-size:34px;opacity:.85">{e(C['video_hook'])} →</p>
    {dlogo('top:60px;right:70px',130)}""", bg="#14213D", n=1, dark=True))
    for i,s in enumerate(C['stories']):
        k=K['stories'][i]
        words="".join(f"<div><b>{e(w)}</b> <span style='opacity:.85'>{e(kk)}</span> — {e(d)}</div>" for (w,d),kk in zip(s['words'],k['words']))
        bl="".join(f"<li>{e(b)}<div class=ko>{e(kb)}</div></li>" for b,kb in zip(s['body'],k['body']))
        out.append(slide(f"""<div class=tag>{e(s['tag'])}</div><h1>{e(s['head'])}</h1><div class=kh>{e(k['head'])}</div>
        <ul style="padding:0">{bl}</ul>
        <div class=kw><h4>{kw_t}</h4>{words}</div>{dlogo('bottom:34px;right:70px',70)}""", n=i+2))
    vl=''.join(f'<div style="background:#fff;border-radius:20px;padding:16px 28px;margin-bottom:16px"><span style="font-size:42px;font-weight:800">{e(w)}</span> <i style="opacity:.6;font-size:24px">{e(t)}</i> <b style="font-size:28px;color:#C0392B">{e(kv[0])}</b><div style="font-size:28px;margin-top:4px">{e(x)}</div><div class=ko style="margin:2px 0 0">{e(kv[1])}</div></div>' for (w,t,x),kv in zip(C['vocab'],K['vocab']))
    out.append(slide(f"""<div class=tag>{'VOCAB · 어휘' if en else 'VOCABULARIO · 어휘'}</div><h1 style="margin-bottom:6px">{e(C['vocab_title'])}</h1><div class=kh>{e(K['vocab_title'])} — {e(K['vocab_intro'])}</div>{vl}{dlogo('bottom:34px;right:70px',70)}""", n=7))
    gl="".join(f"<li style='font-size:31px'>{e(g)}<div class=ko>{e(kg)}</div></li>" for g,kg in zip(C['grammar'],K['grammar']))
    out.append(slide(f"""<div class=tag>{'GRAMMAR · 문법' if en else 'GRAMÁTICA · 문법'}</div><h1 style="margin-bottom:6px">{e(C['grammar_title'])}</h1><div class=kh>{e(K['grammar_title'])}</div>
    <ul style="padding:0">{gl}</ul><div style="background:#fff;border-radius:20px;padding:20px 28px;font-size:27px;line-height:1.5">💡 {e(K['grammar_detail'])}</div>{dlogo('bottom:34px;right:70px',70)}""", n=8))
    ql=''.join(f'<div style="margin-bottom:34px"><div style="font-size:40px;font-weight:700">{i+1}. {e(q)}</div><div class=ko style="font-size:30px">{e(kq)}</div></div>' for i,((q,a),kq) in enumerate(zip(C['quiz'],K['quiz'])))
    out.append(slide(f"""<div class=tag>QUIZ · 퀴즈</div><h1 style="margin-bottom:6px">{e(C['quiz_title'])}</h1><div class=kh>{e(K['quiz_title'])}</div>{ql}
    <p style="font-size:28px;opacity:.7;margin-top:40px">{'Answers are on the last page ▶' if en else 'Las respuestas están en la última página ▶'}<br>정답은 마지막 페이지에 있습니다 ▶</p>{dlogo('bottom:34px;right:70px',70)}""", n=9))
    al=''.join(f'<div style="font-size:30px;margin-bottom:12px"><b>{i+1}.</b> {e(a)} <span style="opacity:.75">/ {e(ka)}</span></div>' for i,((q,a),ka) in enumerate(zip(C['quiz'],K['answers_ko'])))
    out.append(slide(f"""<div class=tag>{'ANSWERS · 정답' if en else 'RESPUESTAS · 정답'}</div>
    <div style="margin-top:34px">{al}<div style="font-size:28px;margin-top:18px">✏️ {e(K['grammar_title'])}: <b>{e(K['grammar_answer'])}</b></div></div>
    <div style="position:absolute;left:80px;right:80px;bottom:80px">{pubbox(25)}</div>""", n=10))
    return out

def pdf_html(C):
    K=C['ko']; en=C['lang']=='en'
    srcs=sorted({x.strip() for s in C['stories'] for x in s['src'].split(',')})
    st=""
    for s,k in zip(C['stories'],K['stories']):
        st+=f"""<section><span class=tag>{e(s['tag'])}</span><h2>{e(s['head'])}</h2><div class=kh>{e(k['head'])}</div>
        <ul>{''.join(f'<li>{e(b)}<div class=kp>{e(kb)}</div></li>' for b,kb in zip(s['body'],k['body']))}</ul>
        <table>{''.join(f'<tr><td><b>{e(w)}</b></td><td>{e(kk)}</td><td>{e(d)}</td></tr>' for (w,d),kk in zip(s['words'],k['words']))}</table>
        <div class=det><b>자세한 설명</b> {e(k['detail'])}</div><small>{'Source' if en else 'Fuente'}: {e(s['src'])}</small></section>"""
    return f"""<html><head><meta charset=utf-8><style>{CSS}
@page{{size:A4;margin:14mm 15mm 16mm}}body{{font-size:10.5pt;line-height:1.45}}
header{{background:#14213D;color:#fff;padding:14px 20px;border-radius:10px;margin-bottom:14px;display:flex;gap:16px;align-items:center}}header h1{{color:#FFC83D;font-size:21pt}}
header img{{width:70px;height:70px;border-radius:8px}}
section{{break-inside:avoid;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #ddd}}
.tag{{background:#FFC83D;font-weight:800;font-size:8pt;padding:3px 10px;border-radius:12px;letter-spacing:1px}}
h2{{font-size:14.5pt;margin:6px 0 0}}.kh{{font-size:11pt;font-weight:700;color:#C0392B;margin-bottom:4px}}.kp{{font-size:9.5pt;color:#444}}
ul{{padding-left:18px;margin:4px 0}}table{{margin-top:6px;font-size:9pt;background:#F7F3EA;width:100%;border-radius:6px}}td{{padding:3px 8px;vertical-align:top}}
.det{{background:#EEF2FA;border-radius:8px;padding:7px 10px;margin:6px 0;font-size:9.5pt}}
small{{color:#666}}h3{{margin:10px 0 4px}}.pb{{break-before:page}}
.last{{break-before:page;min-height:262mm;display:flex;flex-direction:column;justify-content:space-between}}
.fl{{position:fixed;bottom:-11mm;right:0}}.fl img{{width:26px;height:26px;border-radius:5px}}
</style></head><body><div class=fl><img src="{LOGO}"></div>
<header><img src="{LOGO}"><div><div style="font-size:9pt">{e(C['date'])} · {DATE_KO}</div><h1>{e(C['title'])}</h1><div>{e(K['title'])} · {e(K['sub'])}</div></div></header>
{st}
<div class=pb></div><h3>{e(C['vocab_title'])} · {e(K['vocab_title'])}</h3><p>{e(K['vocab_intro'])}</p>
<table>{''.join(f'<tr><td><b>{e(w)}</b> <i>{e(t)}</i></td><td><b>{e(kv[0])}</b></td><td>{e(x)}<br><span class=kp>{e(kv[1])}</span></td></tr>' for (w,t,x),kv in zip(C['vocab'],K['vocab']))}</table>
<h3>{e(C['grammar_title'])} · {e(K['grammar_title'])}</h3><ul>{''.join(f'<li>{e(g)}<div class=kp>{e(kg)}</div></li>' for g,kg in zip(C['grammar'],K['grammar']))}</ul><div class=det>{e(K['grammar_detail'])}</div>
<h3>{e(C['quiz_title'])} · {e(K['quiz_title'])}</h3><ol>{''.join(f'<li>{e(q)}<div class=kp>{e(kq)}</div></li>' for (q,a),kq in zip(C['quiz'],K['quiz']))}</ol>
<p style="margin-top:10px"><b>{e(C['sources_title'])}:</b> {e(', '.join(srcs))}</p><small>{e(C['note'])}</small>
<div class=last><div><h3>{'ANSWERS' if en else 'RESPUESTAS'} · 정답</h3><ol>{''.join(f'<li>{e(a)} / {e(ka)}</li>' for (q,a),ka in zip(C['quiz'],K['answers_ko']))}</ol>
<p>✏️ {e(K['grammar_title'])}: <b>{e(K['grammar_answer'])}</b></p></div>{pubbox(15).replace('width:110px;height:110px','width:70px;height:70px')}</div></body></html>"""

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
