# ICS 2026 · Fusion Vision rozet sayfası

Istanbul Card Show 2026 Sonbahar (14–15 Kasım, Lütfi Kırdar) standı için QR → landing → uygulama.
Yayın: GitHub Pages, `docs/` klasörü (main dalı). Adres: https://orangepointstudio.github.io/ics2026/

## Karar (12 Kas 2026)
Fuarda QR'la gelen **Öncü Birlik** (Vanguard) rozetini açar: `fusionvision://vanguard`. Build 17 ve öncesinde tanınan tek uygun rozet bu.
ICS 2026 promo kart rozeti (`src/rozet-ics26.svg`) sonraki build'e eklenecek; uygulamada yeni rozet kimliği + `AchievementManager` eşlemesi gerekir. Eklenince `docs/index.html` → `CONFIG.badgeLink` değişir.

## Ayar (`docs/index.html` → `CONFIG`)
- `playUrl`: Android çıkınca Google Play adresi. `null` iken düğme "yakında" ve kapalı.
- `badgeLink`: rozet derin bağlantısı. Sayfa `?s=` varsa `&ct=ics26f-land-<s>` ekler.
- `allowedSurfaces`: `?s=` → App Store `ct=ics26f-land-<s>` (qr, flyer, ig, press, comm).

## QR (`qr/`)
| Dosya | Adres | Nereye |
|---|---|---|
| `ics26-qr.svg` | `…/ics2026/?s=qr` | stant masası, tent, poster |
| `ics26-flyer.svg` | `…/ics2026/?s=flyer` | broşür |
| `ics26-ig.svg` | `…/ics2026/?s=ig` | story / görsel içi |

Baskıya **SVG** gider. En küçük kenar: masa/tent 4 cm, broşür 3 cm, poster 15 cm. Beyaz kenar kırpılmaz.
Kanıt: `qr/QR-KANIT.json` (üretim + PNG geri okuma), `qr/QR-CAPRAZ-TEST.json` (SVG ve story görselinden çözme).
Yeniden üretmek: `cd tools && npm ci && node qr.mjs && node qr-capraz.mjs`

## Gizlilik
Sayfa çerez, takip kodu ve üçüncü taraf isteği kullanmaz; fontlar `docs/assets/fonts/` altında (Unbounded, Inter — OFL).

## Sosyal setler
`sosyal/METINLER.md` + `sosyal/cikti/`. Üretim: `python3 -I sosyal/uret.py` (başsız Chrome).
