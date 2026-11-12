#!/usr/bin/env python3
"""ICS 2026 sosyal setleri: HTML şablon -> başsız Chrome PNG.
Kullanım: python3 -I sosyal/uret.py   (repo kökünden)
Çıktı: sosyal/cikti/{fv,op}/*.png
"""
import subprocess, tempfile, shutil
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "sosyal" / "cikti"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = (KOK / "tools" / "fonts").as_uri()
ROZET = (KOK / "docs" / "assets" / "rozet-oncu-birlik.png").as_uri()
ROZET_ICS = (KOK / "src" / "rozet-ics26-1024.png").as_uri()
LOGO = (KOK / "docs" / "assets" / "fv-logo.jpg").as_uri()
QR_IG = (KOK / "qr" / "ics26-ig-buyuk.png").as_uri()

ORTAK = f"""
@font-face{{font-family:Unbounded;src:url('{FONT}/Unbounded.ttf');font-weight:200 900}}
@font-face{{font-family:Inter;src:url('{FONT}/Inter.ttf');font-weight:100 900}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:var(--w);height:var(--h);overflow:hidden}}
body{{position:relative;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}}
.gren::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.17;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
"""

FV = """
:root{--ink:#0B0B0C;--cream:#F3EADB;--or:#FF632C;--txt:#F5F2EC}
.koyu{background:radial-gradient(70% 38% at 18% 6%,rgba(255,99,44,.30),transparent 70%),radial-gradient(60% 30% at 95% 55%,rgba(138,125,255,.16),transparent 70%),radial-gradient(90% 40% at 50% 100%,rgba(255,99,44,.18),transparent 70%),#0B0B0C;color:var(--txt)}
.krem{background:radial-gradient(70% 36% at 15% 4%,#fff8ec,transparent 70%),radial-gradient(60% 30% at 100% 50%,rgba(255,99,44,.22),transparent 70%),radial-gradient(60% 30% at 0% 90%,rgba(95,215,255,.16),transparent 70%),var(--cream);color:var(--ink)}
.turuncu{background:radial-gradient(70% 36% at 15% 4%,#ff9a62,transparent 70%),radial-gradient(70% 40% at 100% 70%,#e2461a,transparent 70%),var(--or);color:var(--ink)}
.pad{position:absolute;left:84px;right:84px;top:110px}
.kunye{font:700 26px/1 Unbounded;letter-spacing:.18em;text-transform:uppercase;display:flex;gap:16px;align-items:center;margin-bottom:38px}
.kunye i{width:14px;height:14px;border-radius:50%;background:var(--or);display:inline-block}
.turuncu .kunye i{background:var(--ink)}
.baslik{font:800 104px/1.02 Unbounded;letter-spacing:-.035em}
.koyu .e,.krem .e{color:var(--or)} .turuncu .e{color:var(--cream)}
.alt{margin-top:28px;font:500 38px/1.3 Inter;max-width:860px}
.koyu .alt{color:#D3CDC3} .krem .alt{color:#4a4640} .turuncu .alt{color:#2a1408}
.rozet-img{position:absolute;filter:drop-shadow(0 40px 80px rgba(0,0,0,.45))}
.sticker{position:absolute;width:250px;height:250px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font:800 46px/1 Unbounded;letter-spacing:-.02em;box-shadow:0 24px 60px rgba(0,0,0,.30);transform:rotate(-10deg)}
.sticker span{display:block;font:700 19px/1.2 Unbounded;letter-spacing:.14em;margin-top:10px}
.serit{position:absolute;left:-40px;right:-40px;height:110px;display:flex;align-items:center;gap:60px;white-space:nowrap;
 font:800 38px/1 Unbounded;letter-spacing:.08em;color:var(--ink);padding-left:80px;
 background:linear-gradient(90deg,#ff5fa2,#ffb86b,#fff27a,#7dffb0,#5fd7ff,#8a7dff);box-shadow:0 30px 80px rgba(0,0,0,.35)}
.adim{display:grid;grid-template-columns:96px 1fr;gap:30px;align-items:center;margin-top:44px}
.adim b{width:96px;height:96px;border-radius:50%;display:grid;place-items:center;background:var(--or);color:var(--ink);font:800 44px/1 Unbounded}
.adim h3{font:800 50px/1.05 Unbounded;letter-spacing:-.03em}
.adim p{font:500 30px/1.3 Inter;margin-top:8px;color:#4a4640}
.qrkutu{position:absolute;z-index:3;background:#fff;border-radius:36px;padding:26px;box-shadow:0 30px 80px rgba(0,0,0,.35)}
.qrkutu img{display:block}
.qrkutu div{font:700 22px/1.2 Unbounded;letter-spacing:.12em;text-align:center;color:var(--ink);margin-top:14px;text-transform:uppercase}
.fv-logo{position:absolute;mix-blend-mode:screen;filter:brightness(1.05) contrast(1.2)}
.altbilgi{position:absolute;font:700 22px/1.3 Unbounded;letter-spacing:.16em;text-transform:uppercase}
"""

OP = """
:root{--op:#EB5E28;--siyah:#252422;--krem:#FFFCF2;--gri:#CCC5B9}
.opk{background:radial-gradient(60% 40% at 85% 10%,rgba(235,94,40,.22),transparent 70%),var(--siyah);color:var(--krem)}
.opa{background:var(--krem);color:var(--siyah)}
.pad{position:absolute;left:90px;right:90px;top:96px}
.marka{display:flex;justify-content:space-between;align-items:center;font:800 30px/1 Inter;letter-spacing:.22em}
.marka i{display:inline-block;width:18px;height:18px;border-radius:50%;background:var(--op);margin-left:8px;vertical-align:2px}
.marka small{font:600 20px/1 Inter;letter-spacing:.16em;opacity:.7}
.kod{margin-top:70px;font:700 24px/1 Inter;letter-spacing:.2em;color:var(--op)}
.baslik{margin-top:24px;font:800 98px/1.02 Inter;letter-spacing:-.04em}
.baslik .e{color:var(--op)}
.alt{margin-top:30px;font:500 36px/1.35 Inter;max-width:860px}
.opk .alt{color:var(--gri)} .opa .alt{color:#403D39}
.motto{position:absolute;left:90px;right:90px;bottom:84px;display:flex;justify-content:space-between;font:600 22px/1.3 Inter;letter-spacing:.06em;border-top:2px solid currentColor;padding-top:26px;opacity:.85}
.akis{display:flex;align-items:center;gap:22px;margin-top:70px}
.kutu{flex:1 1 0;min-width:0;align-self:stretch;border:3px solid var(--siyah);border-radius:26px;padding:28px 24px;min-height:250px;background:#fff}
.kutu b{font:800 22px/1 Inter;letter-spacing:.18em;color:var(--op)}
.kutu h4{font:800 40px/1.05 Inter;letter-spacing:-.03em;margin-top:18px}
.kutu p{font:500 24px/1.3 Inter;margin-top:12px;color:#403D39}
.ok{font:800 50px/1 Inter;color:var(--op)}
.fv-logo{position:absolute;mix-blend-mode:screen;filter:brightness(1.05) contrast(1.2)}
"""


def sayfa(w, h, css, govde, sinif):
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{ORTAK}{css}</style></head>
<body><div class="{sinif} gren" style="position:absolute;inset:0;overflow:hidden">{govde}</div></body></html>"""


SERIT = "<span>ICS 2026</span><span>İSTANBUL CARD SHOW</span><span>14–15 KASIM</span><span>LÜTFİ KIRDAR</span><span>FUSION VISION</span><span>ICS 2026</span>"

ISLER = {
    # ---------- FUSION VISION ----------
    ("fv", "FV-ICS-R1_feed_1080x1350"): (1080, 1350, FV, "koyu", f"""
<div class="pad"><div class="kunye"><i></i>ICS 2026 · 14–15 Kasım</div>
<div class="baslik">Kartını getir.<br><span class="e">Rozetini al.</span></div>
<div class="alt">Standımıza uğra, kartını tarat. Öncü Birlik rozeti uygulamada seni bekliyor.</div></div>
<img class="rozet-img" src="{ROZET}" style="width:700px;left:300px;top:560px">
<div class="sticker" style="background:var(--or);color:var(--ink);left:84px;top:780px">ÖNCÜ<span>BİRLİK<br>ROZETİ</span></div>
<div class="serit" style="bottom:70px;transform:rotate(-3deg)">{SERIT}</div>"""),

    ("fv", "FV-ICS-R2_feed_1080x1350"): (1080, 1350, FV, "krem", f"""
<div class="pad"><div class="kunye"><i></i>Fuar rozeti · 3 adım</div>
<div class="baslik" style="font-size:92px">Rozet<br><span class="e">üç dokunuş.</span></div>
<div class="adim"><b>1</b><div><h3>İndir</h3><p>Fusion Vision, App Store'da ücretsiz.</p></div></div>
<div class="adim"><b>2</b><div><h3>Giriş yap</h3><p>Rozet hesabına bağlanır.</p></div></div>
<div class="adim"><b>3</b><div><h3>Rozetini aç</h3><p>Stanttaki QR'ı okut, düğmeye dokun.</p></div></div></div>
<img class="rozet-img" src="{ROZET}" style="width:430px;right:40px;bottom:50px">"""),

    ("fv", "FV-ICS-R3_story_1080x1920"): (1080, 1920, FV, "turuncu", f"""
<div class="pad" style="top:290px"><div class="kunye"><i></i>Lütfi Kırdar · ICS 2026</div>
<div class="baslik" style="font-size:118px">Bugün<br><span class="e">stanttayız.</span></div>
<div class="alt">Kartını tarat, Öncü Birlik rozetini al. QR'ı okut ya da bağlantıya dokun.</div></div>
<img class="rozet-img" src="{ROZET}" style="width:600px;left:20px;top:900px">
<div class="qrkutu" style="right:84px;top:980px;transform:rotate(4deg)"><img src="{QR_IG}" width="290" height="290"><div>Rozetini al</div></div>"""),

    ("fv", "FV-ICS-R4_story_1080x1920"): (1080, 1920, FV, "koyu", f"""
<img class="fv-logo" src="{LOGO}" style="width:520px;left:280px;top:270px">
<div class="pad" style="top:820px;text-align:center"><div class="kunye" style="justify-content:center"><i></i>14–15 Kasım · ICS 2026</div>
<div class="baslik" style="font-size:96px">Masaya gelen<br><span class="e">herkese teşekkürler.</span></div>
<div class="alt" style="margin:30px auto 0">Rozetini almadıysan sayfa hâlâ açık.</div></div>
<img class="rozet-img" src="{ROZET}" style="width:330px;left:375px;top:1250px">"""),

    # ---------- ORANGE POINT (yalnız kurumsal haber çerçevesi; FV CTA/link yok) ----------
    ("op", "OP-ICS-01_feed_1080x1350"): (1080, 1350, OP, "opk", f"""
<div class="pad"><div class="marka"><span>ORANGE POINT<i></i></span><small>stüdyo · lab · akademi</small></div>
<div class="kod">OP-FV · ICS 2026</div>
<div class="baslik">Bu hafta sonu<br><span class="e">sahadayız.</span></div>
<div class="alt">Stüdyomuzun ürünü Fusion Vision, Istanbul Card Show'da. 14–15 Kasım, Lütfi Kırdar.</div></div>
<img class="fv-logo" src="{LOGO}" style="width:500px;right:90px;top:700px;mix-blend-mode:screen">
<div class="motto"><span>Do less. Do it right. Show the process.</span><span>@orangepointstudio</span></div>"""),

    ("op", "OP-ICS-02_feed_1080x1350"): (1080, 1350, OP, "opa", f"""
<div class="pad"><div class="marka"><span>ORANGE POINT<i></i></span><small>stüdyo · lab · akademi</small></div>
<div class="kod">OP-FV · SÜREÇ NOTU</div>
<div class="baslik" style="font-size:84px">Fuar rozeti<br><span class="e">böyle çalışıyor.</span></div>
<div class="akis">
 <div class="kutu"><b>01</b><h4>QR</h4><p>Masada durur. Kaynak etiketi taşır.</p></div><div class="ok">→</div>
 <div class="kutu"><b>02</b><h4>Sayfa</h4><p>Tek ekran. Çerez ve takip kodu yok.</p></div><div class="ok">→</div>
 <div class="kutu"><b>03</b><h4>Rozet</h4><p>Ürün içinde hesaba işlenir.</p></div>
</div>
<div class="alt" style="font-size:30px;margin-top:44px">Hangi yüzeyin (masa, broşür, story) ne getirdiğini fuardan bir hafta sonra yazacağız.</div></div>
<div class="motto"><span>Do less. Do it right. Show the process.</span><span>OP-FV</span></div>"""),

    ("op", "OP-ICS-03_story_1080x1920"): (1080, 1920, OP, "opk", f"""
<div class="pad" style="top:280px"><div class="marka"><span>ORANGE POINT<i></i></span><small>stüdyo · lab · akademi</small></div>
<div class="kod" style="margin-top:90px">OP-FV · ICS 2026</div>
<div class="baslik" style="font-size:110px">14–15<br>Kasım.<br><span class="e">Lütfi Kırdar.</span></div>
<div class="alt">Fusion Vision ile Istanbul Card Show'dayız.</div></div>
<img class="fv-logo" src="{LOGO}" style="width:430px;left:325px;top:1000px;mix-blend-mode:screen">
<div class="motto" style="bottom:380px"><span>Do less. Do it right. Show the process.</span><span>@orangepointstudio</span></div>"""),

    ("op", "OP-ICS-01_linkedin_1080x1080"): (1080, 1080, OP, "opk", f"""
<div class="pad" style="top:84px"><div class="marka"><span>ORANGE POINT<i></i></span><small>stüdyo · lab · akademi</small></div>
<div class="kod" style="margin-top:56px">OP-FV · ICS 2026</div>
<div class="baslik" style="font-size:88px">Bu hafta sonu<br><span class="e">sahadayız.</span></div>
<div class="alt" style="font-size:32px;max-width:560px">Stüdyomuzun ürünü Fusion Vision, Istanbul Card Show'da. 14–15 Kasım, Lütfi Kırdar.</div></div>
<img class="fv-logo" src="{LOGO}" style="width:380px;right:70px;top:500px;mix-blend-mode:screen">
<div class="motto" style="bottom:64px"><span>Do less. Do it right. Show the process.</span><span>@orangepointstudio</span></div>"""),

    ("op", "OP-ICS-02_linkedin_1080x1080"): (1080, 1080, OP, "opa", f"""
<div class="pad" style="top:84px"><div class="marka"><span>ORANGE POINT<i></i></span><small>stüdyo · lab · akademi</small></div>
<div class="kod" style="margin-top:56px">OP-FV · SÜREÇ NOTU</div>
<div class="baslik" style="font-size:72px">Fuar rozeti<br><span class="e">böyle çalışıyor.</span></div>
<div class="akis" style="margin-top:50px">
 <div class="kutu" style="min-height:220px"><b>01</b><h4>QR</h4><p>Masada durur. Kaynak etiketi taşır.</p></div><div class="ok">→</div>
 <div class="kutu" style="min-height:220px"><b>02</b><h4>Sayfa</h4><p>Tek ekran. Çerez ve takip kodu yok.</p></div><div class="ok">→</div>
 <div class="kutu" style="min-height:220px"><b>03</b><h4>Rozet</h4><p>Ürün içinde hesaba işlenir.</p></div>
</div></div>
<div class="motto" style="bottom:64px"><span>Do less. Do it right. Show the process.</span><span>OP-FV</span></div>"""),

    # ---------- OG (sayfa paylaşım önizlemesi) ----------
    ("og", "og_1200x630"): (1200, 630, FV, "koyu", f"""
<div class="pad" style="top:96px;left:76px"><div class="kunye" style="font-size:22px"><i></i>ICS 2026 · 14–15 Kasım</div>
<div class="baslik" style="font-size:72px">Öncü Birlik<br><span class="e">rozetin hazır.</span></div>
<div class="alt" style="font-size:28px;max-width:600px">Istanbul Card Show · Lütfi Kırdar · Fusion Vision</div></div>
<img class="rozet-img" src="{ROZET}" style="width:500px;right:50px;top:65px">"""),

    # ---------- Sonraki build: ICS promo kart rozeti duyurusu ----------
    ("fv", "FV-ICS-R5_sonra_feed_1080x1350"): (1080, 1350, FV, "koyu", f"""
<div class="pad"><div class="kunye"><i></i>Güncellemeyle geliyor</div>
<div class="baslik">ICS 2026<br><span class="e">promo rozeti.</span></div>
<div class="alt">Fuarda masaya gelenlere özel kart rozeti. Güncelleme çıkınca duyuracağız.</div></div>
<img class="rozet-img" src="{ROZET_ICS}" style="width:720px;left:280px;top:560px;transform:rotate(4deg)">
<div class="serit" style="bottom:70px;transform:rotate(-3deg)">{SERIT}</div>"""),
}


def main():
    profil = Path(tempfile.mkdtemp(prefix="ics26-chrome-"))
    gec = Path(tempfile.mkdtemp(prefix="ics26-html-"))
    try:
        for (grup, ad), (w, h, css, sinif, govde) in ISLER.items():
            hedef = CIKTI / grup
            hedef.mkdir(parents=True, exist_ok=True)
            html = gec / f"{ad}.html"
            html.write_text(sayfa(w, h, css, govde, sinif), encoding="utf-8")
            (hedef / f"{ad}.html").write_text(html.read_text(encoding="utf-8"), encoding="utf-8")
            png = hedef / f"{ad}.png"
            if png.exists():
                png.unlink()
            subprocess.run([CHROME, "--headless=new", f"--user-data-dir={profil}", "--no-first-run",
                            "--no-default-browser-check", "--disable-extensions", "--disable-sync",
                            "--hide-scrollbars", "--allow-file-access-from-files", "--force-device-scale-factor=1",
                            f"--window-size={w},{h}", "--virtual-time-budget=5000", f"--screenshot={png}",
                            html.as_uri()], capture_output=True, text=True, timeout=120)
            print(("OK  " if png.exists() else "HATA") + f" {grup}/{ad}.png")
    finally:
        shutil.rmtree(profil, ignore_errors=True)
        shutil.rmtree(gec, ignore_errors=True)


if __name__ == "__main__":
    main()
