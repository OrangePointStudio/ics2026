#!/usr/bin/env python3
"""ICS26F yayın kiti üreticisi — posts.json tek kaynak.

Çıktılar (sosyal/kit/ altında):
  telefon/        numaralı görsel + metin dosyaları (AirDrop ile telefona)
  onay/<ID>.html  post başına onay sayfası (KR-5): görsel, birebir metin, sayaç, rozetler
  YAYIN-KITI.html tek sayfalık kit (gömülü küçük görseller, kopyala düğmeleri)
  ONAY-KAYDI.json boş onay kaydı şablonu (GO alanları Alperen'in)
  KONTROL.json    otomatik kural denetimi sonuçları
"""
import base64, html, io, json, re, shutil, sys
from pathlib import Path
from PIL import Image

KIT = Path(__file__).resolve().parent
SOSYAL = KIT.parent
CIKTI = SOSYAL / "cikti"
HAM = SOSYAL / "ham"
D = json.loads((KIT / "posts.json").read_text(encoding="utf-8"))
AMBARGO = re.compile(r"cardinal ?app|fusionvision\.app|ct=FV|1 saniye|apps\.apple\.com", re.I)
LIMIT = {"ig-fv": 2200, "ig-op": 2200, "threads-fv": 500, "linkedin-op": 3000}
OLCU = {"1080x1350": (1080, 1350), "1080x1920": (1080, 1920), "1080x1080": (1080, 1080)}


def gorsel_yolu(g):
    if g.startswith("ham/"):
        return HAM / g[4:]
    p = CIKTI / g
    return p if p.exists() else None


def hikaye(p):
    return "story" in p["kanal"].lower()


def denetle(p, tum):
    s = []  # (seviye, mesaj)
    m = p["metin"]
    if not hikaye(p):
        lim = LIMIT.get(p["yuzey"])
        if lim and len(m) > lim:
            s.append(("HATA", f"{len(m)} karakter > {lim}"))
        if "?" in m:
            s.append(("UYARI", "soru işareti var (retorik soru yasağı)"))
        if m.count("—") >= 2:
            s.append(("UYARI", "em-dash zinciri"))
    if p["yuzey"] == "threads-fv" and "#" in m:
        s.append(("HATA", "Threads'te hashtag yasak"))
    if p["marka"] == "OP":
        if AMBARGO.search(m):
            s.append(("HATA", "OP metninde FV link/CTA izi (ambargo regex)"))
        if re.search(r"https?://|fusionvision://|indir|App Store", m, re.I):
            s.append(("HATA", "OP metninde link/indirme çağrısı"))
    if "[SAYAC" in m:
        s.append(("BİLGİ", "yer tutucu var — yayından önce doldurulur"))
    # K5: aynı cümle başka posttа
    cum = {c.strip() for c in re.split(r"[.\n]", m) if len(c.strip()) > 25}
    for q in tum:
        if q["id"] == p["id"] or hikaye(q) or hikaye(p):
            continue
        ort = cum & {c.strip() for c in re.split(r"[.\n]", q["metin"]) if len(c.strip()) > 25}
        for c in ort:
            s.append(("HATA", f"K5: '{c[:50]}…' {q['id']} ile aynı"))
    # görseller
    for g in p.get("gorsel", []) + p.get("gorsel_ham", []):
        if g.startswith("FUARDA"):
            s.append(("BİLGİ", "görsel fuarda çekilecek"))
            continue
        y = gorsel_yolu(g)
        if not y or not y.exists():
            s.append(("HATA", f"görsel yok: {g}"))
            continue
        w, h = Image.open(y).size
        bek = next((v for k, v in OLCU.items() if k in p["format"]), None)
        if bek and (w, h) != bek:
            s.append(("HATA", f"{g} {w}x{h}, beklenen {bek[0]}x{bek[1]}"))
    if p.get("link", "yok").startswith("http") and "s=ig" not in p["link"]:
        s.append(("UYARI", "story bağlantısı ?s=ig değil"))
    return s


def kucuk(y, gen=540):
    im = Image.open(y).convert("RGB")
    im.thumbnail((gen, gen * 2))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


CSS = """
:root{--bg:#f6f3ee;--yuzey:#ffffff;--metin:#1b1b1d;--soluk:#5f6268;--cizgi:#e2ddd4;--vurgu:#d9531e;--hata:#b3261e;--uyari:#8a5a00;--ok:#1f7a3a;--kod:#f1ece4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e0e10;--yuzey:#18181b;--metin:#f2efe9;--soluk:#a3a6ad;--cizgi:#2c2c31;--vurgu:#ff7a45;--hata:#ff8a80;--uyari:#ffcc66;--ok:#7ddc9a;--kod:#202024;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0e0e10;--yuzey:#18181b;--metin:#f2efe9;--soluk:#a3a6ad;--cizgi:#2c2c31;--vurgu:#ff7a45;--hata:#ff8a80;--uyari:#ffcc66;--ok:#7ddc9a;--kod:#202024;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--metin);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Inter",system-ui,sans-serif}
main{max-width:980px;margin:0 auto;padding-block:24px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.kart>div{min-width:0}
h1{font-size:24px;margin:0 0 4px}h2{font-size:18px;margin:32px 0 10px}.soluk{color:var(--soluk)}
.kart{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:14px;padding:16px;margin:14px 0;display:grid;grid-template-columns:200px 1fr;gap:16px}
@media (max-width:640px){.kart{grid-template-columns:1fr}}
.kart img{width:100%;border-radius:8px;border:1px solid var(--cizgi);display:block}
.gorseller{display:flex;flex-direction:column;gap:8px}
.ust{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline}.ust b{font-size:16px}
.etiket{font-size:12px;padding:2px 8px;border-radius:99px;border:1px solid var(--cizgi);color:var(--soluk)}
.etiket.fv{color:var(--vurgu);border-color:var(--vurgu)}
pre{white-space:pre-wrap;word-break:break-word;background:var(--kod);padding:12px;border-radius:8px;margin:10px 0 6px;font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
button{font:inherit;font-size:13px;padding:6px 12px;border-radius:8px;border:1px solid var(--cizgi);background:var(--yuzey);color:var(--metin);cursor:pointer}
button:active{transform:translateY(1px)}
ul.d{margin:6px 0 0;padding-left:18px;font-size:13px}.HATA{color:var(--hata)}.UYARI{color:var(--uyari)}.BİLGİ{color:var(--soluk)}.ok{color:var(--ok);font-size:13px}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid var(--cizgi);padding:6px 8px;text-align:left;vertical-align:top}
.kutu{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:14px;padding:14px 16px}
.tablo-sar{overflow-x:auto}
"""

JS = """
function kopyala(id,btn){const t=document.getElementById(id).innerText;navigator.clipboard.writeText(t).then(()=>{const o=btn.textContent;btn.textContent='Kopyalandı';setTimeout(()=>btn.textContent=o,1400)}).catch(()=>{const r=document.createRange();r.selectNodeContents(document.getElementById(id));const s=getSelection();s.removeAllRanges();s.addRange(r)})}
document.querySelectorAll('[data-say]').forEach(e=>{const t=document.getElementById(e.dataset.say).innerText;e.textContent=[...t].length+' karakter'});
"""


def kart(p, denet, gom):
    e = html.escape
    imgs = []
    for g in p.get("gorsel", []):
        if g.startswith("FUARDA"):
            imgs.append(f'<div class="kutu soluk" style="font-size:13px">{e(g)}</div>')
            for yg in p.get("gorsel_yedek", []):
                y = gorsel_yolu(yg)
                imgs.append(f'<img alt="yedek" src="{kucuk(y) if gom else "../gorsel/" + y.name}"><span class="soluk" style="font-size:12px">yedek görsel</span>')
            continue
        y = gorsel_yolu(g)
        if y:
            imgs.append(f'<img alt="{e(p.get("alt",""))}" src="{kucuk(y) if gom else "../gorsel/" + y.name}">')
    for g in p.get("gorsel_ham", []):
        y = gorsel_yolu(g)
        imgs.append(f'<img alt="ham" src="{kucuk(y) if gom else "../gorsel/" + y.name}"><span class="soluk" style="font-size:12px">ham-mod alternatifi</span>')
    mid = "m-" + p["id"]
    d = "".join(f'<li class="{s}">{s}: {e(m)}</li>' for s, m in denet) or '<li class="ok">otomatik denetim temiz</li>'
    notlar = "".join(f"<li>{e(n)}</li>" for n in p.get("notlar", []))
    cik = f'<div style="font-size:13px">Çıkartma: <b>{e(p["cikartma"])}</b> → <code>{e(p["link"])}</code></div>' if p.get("cikartma") else ""
    return f"""<section class="kart" id="{p['id']}"><div class="gorseller">{''.join(imgs) or '<span class="soluk">görsel yok — düz metin</span>'}</div>
<div><div class="ust"><b>{p['sira']}. {e(p['id'])}</b><span class="etiket {'fv' if p['marka']=='FV' else ''}">{e(p['marka'])} · {e(p['kanal'])}</span><span class="soluk">{e(p['gun'])} · {e(p['zaman'][-5:] if p['zaman'][:2]=='20' else p['zaman'])}</span></div>
<div class="soluk" style="font-size:13px">{e(p['hesap'])} · {e(p['nereden'])} · {e(p['format'])}</div>
<pre id="{mid}">{e(p['metin'])}</pre>
<div style="display:flex;gap:10px;align-items:center"><button onclick="kopyala('{mid}',this)">Metni kopyala</button><span class="soluk" style="font-size:13px" data-say="{mid}"></span></div>
{cik}<ul class="d">{d}</ul>{'<ul class="d soluk">'+notlar+'</ul>' if notlar else ''}</div></section>"""


def parca(baslik, govde):
    return f"""<title>{html.escape(baslik)}</title><meta name="claude:viewport-fit-sides" content="cover"><style>{CSS}</style><main>{govde}</main><script>{JS}</script>"""


def sayfa(baslik, govde):
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(baslik)}</title><style>{CSS}</style></head><body><main>{govde}</main><script>{JS}</script></body></html>"""


def main():
    P = D["postlar"]
    kontrol = {p["id"]: denetle(p, P) for p in P}
    # görseller + telefon klasörü
    for k in ["gorsel", "telefon", "onay"]:
        (KIT / k).mkdir(exist_ok=True)
    for p in P:
        for g in p.get("gorsel", []) + p.get("gorsel_ham", []) + p.get("gorsel_yedek", []):
            y = gorsel_yolu(g) if not g.startswith("FUARDA") else None
            if y:
                shutil.copy2(y, KIT / "gorsel" / y.name)
        on = f"{p['sira']:02d}_{p['gun'].replace(' ', '')}_{p['id']}"
        (KIT / "telefon" / f"{on}.txt").write_text(p["metin"] + ("\n\nBağlantı: " + p["link"] if p.get("link", "").startswith("http") else "") + "\n", encoding="utf-8")
        for i, g in enumerate(p.get("gorsel", [])):
            y = gorsel_yolu(g) if not g.startswith("FUARDA") else None
            if y:
                shutil.copy2(y, KIT / "telefon" / f"{on}_{i+1}.png")
        for i, g in enumerate(p.get("gorsel_ham", [])):
            shutil.copy2(gorsel_yolu(g), KIT / "telefon" / f"{on}_HAM_{i+1}.png")
        # onay sayfası
        (KIT / "onay" / f"{p['id']}.html").write_text(sayfa(f"Onay {p['id']}", f"<h1>Onay · {html.escape(p['id'])}</h1><p class='soluk'>Bu sayfa görülmeden post basılmaz (KR-5). GO yazılı verilir ve ONAY-KAYDI.json'a işlenir.</p>" + kart(p, kontrol[p["id"]], False)), encoding="utf-8")
    # kit sayfası
    satir = "".join(f"<tr><td>{p['sira']}</td><td>{html.escape(p['gun'])}</td><td>{html.escape(p['zaman'][-5:] if p['zaman'][:2]=='20' else '—')}</td><td>{html.escape(p['id'])}</td><td>{html.escape(p['kanal'])}</td><td>{html.escape(p['nereden'].split(' (')[0].split(' —')[0])}</td></tr>" for p in P)
    yedek = "".join(f"<tr><td>{html.escape(y['id'])}</td><td>{html.escape(y['kanal'])}</td><td>{html.escape(y['durum'])}</td></tr>" for y in D["yedek"])
    hata = sum(1 for v in kontrol.values() for s, _ in v if s == "HATA")
    govde = f"""<h1>ICS 2026 yayın kiti</h1><p class="soluk">Fusion Vision ve Orange Point · 12–16 Kasım · {len(P)} post · hiçbiri yayınlanmadı. Her post ayrı yazılı GO ister (SMK-004).</p>
<div class="kutu"><b>Rozet sayfası:</b> <a href="{D['landing']}">{D['landing']}</a> · story bağlantısı <code>?s=ig</code><br><span class="soluk" style="font-size:13px">Otomatik denetim: {hata} hata. Tam çözünürlüklü görseller ve metin dosyaları Mac masaüstündeki ICS2026-SOSYAL klasöründe, yayın sırasıyla numaralı (AirDrop ile telefona).</span></div>
<h2>Sıra</h2><div class="tablo-sar"><table><tr><th>#</th><th>Gün</th><th>Saat</th><th>Slot</th><th>Kanal</th><th>Nereden</th></tr>{satir}</table></div>
<h2>Postlar</h2>{''.join(kart(p, kontrol[p['id']], True) for p in P)}
<h2>Kullanılmayanlar</h2><div class="tablo-sar"><table>{yedek}</table></div>"""
    (KIT / "YAYIN-KITI.html").write_text(sayfa("ICS yayın kiti", govde), encoding="utf-8")
    (KIT / "ics-yayin-kiti.html").write_text(parca("ICS yayın kiti", govde), encoding="utf-8")
    # onay kaydı şablonu
    # ONAY-KAYDI: var olan kayıtlar EZİLMEZ; yalnız yeni id eklenir
    ok_yol = KIT / "ONAY-KAYDI.json"
    eski = json.loads(ok_yol.read_text(encoding="utf-8")) if ok_yol.exists() else {"kural": "SMK-004: her post ayrı yazılı GO; GO metni Alperen'in kendi sözü birebir yazılır", "kayitlar": []}
    var = {k["id"] for k in eski["kayitlar"]}
    for p in P:
        if p["id"] not in var:
            eski["kayitlar"].append({"id": p["id"], "go": None, "go_metni": None, "go_zamani": None, "gorsel_secimi": ("tasarim|ham" if p.get("gorsel_ham") else None), "basildi": None, "public_url": None, "dogrulama_kademesi": None})
    ok_yol.write_text(json.dumps(eski, ensure_ascii=False, indent=2), encoding="utf-8")
    (KIT / "KONTROL.json").write_text(json.dumps({k: [{"seviye": s, "mesaj": m} for s, m in v] for k, v in kontrol.items()}, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in kontrol.items():
        for s, m in v:
            print(f"{k:12} {s:6} {m}")
    print(f"HATA toplam: {hata}")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
