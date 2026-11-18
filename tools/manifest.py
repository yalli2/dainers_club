"""Site data for https://yalli2.github.io/dainers_club/

- write_meta(EN, ES, DATE): saves newsletters/<DATE>/meta.json (headlines in EN/ES + Korean)
- build_index(): rescans newsletters/ and rewrites newsletters/index.json

build.py calls both after each daily build. Run `python3 tools/manifest.py`
on its own to rebuild index.json after adding or removing folders by hand.
"""
import os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = os.path.join(ROOT, "newsletters")


def _edition(C):
    K = C.get("ko", {})
    ks = K.get("stories", [])
    stories = []
    for i, s in enumerate(C.get("stories", [])):
        k = ks[i] if i < len(ks) else {}
        stories.append({"tag": s.get("tag", ""), "head": s.get("head", ""),
                        "ko": k.get("head", ""), "src": s.get("src", "")})
    return {"title": C.get("title", ""), "sub": C.get("sub", ""), "date": C.get("date", ""),
            "title_ko": K.get("title", ""), "sub_ko": K.get("sub", ""), "stories": stories,
            "vocab": [v[0] for v in C.get("vocab", [])]}


def write_meta(EN, ES, DATE, date_ko=""):
    d = os.path.join(NL, DATE)
    os.makedirs(d, exist_ok=True)
    meta = {"date": DATE, "date_ko": date_ko, "en": _edition(EN), "es": _edition(ES)}
    with open(os.path.join(d, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


def build_index():
    days = []
    for name in sorted(os.listdir(NL), reverse=True):
        p = os.path.join(NL, name)
        if not (os.path.isdir(p) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", name)):
            continue
        day = {"date": name, "langs": {}}
        for lang in ("en", "es"):
            lp = os.path.join(p, lang)
            if os.path.isdir(lp):
                day["langs"][lang] = sorted(f for f in os.listdir(lp) if not f.startswith("_"))
        mp = os.path.join(p, "meta.json")
        if os.path.exists(mp):
            with open(mp, encoding="utf-8") as f:
                day["meta"] = json.load(f)
        if day["langs"]:
            days.append(day)
    with open(os.path.join(NL, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"days": days}, f, ensure_ascii=False, indent=1)
    return len(days)


if __name__ == "__main__":
    print(build_index(), "days in newsletters/index.json")
