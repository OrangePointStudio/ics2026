# ICS 2026 · Fusion Vision rozet sayfası

Istanbul Card Show 2026 Sonbahar (14–15 Kasım, Lütfi Kırdar) standı için QR → landing.
Yayın: GitHub Pages, `site/` klasörü (Actions ile).

## Ayar (site/index.html → `CONFIG`)
- `playUrl`: Android çıkınca Google Play adresi. `null` iken düğme "yakında" ve kapalı.
- `badgeLink`: rozet derin bağlantısı. Bugün `fusionvision://vanguard` (build 17 ve öncesinde tanınan rozet).
  Gerçek "ICS 2026" rozeti için uygulamada yeni rozet kimliği gerekir (AchievementManager eşlemesi) → yeni build.
- `allowedSurfaces`: `?s=` → App Store `ct=ics26f-land-<s>`.

## QR
`qr/` klasörü: `ics26-qr.svg/png` → `https://orangepointstudio.github.io/ics2026/?s=qr`.
Üretim + geri okuma kanıtı: `qr/QR-KANIT.json`.

## Rozet
`src/rozet-ics26.svg` (1024×1024, şeffaf) — uygulamadaki `Assets.xcassets/Achievements` setine uygun boyut.
