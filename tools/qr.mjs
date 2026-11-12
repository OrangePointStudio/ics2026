// QR üret (SVG + PNG 1024/300) ve PNG'yi jsQR ile geri oku. Kanıt: ../qr/QR-KANIT.json
import QRCode from 'qrcode'; import jsQR from 'jsqr'; import { PNG } from 'pngjs'; import fs from 'node:fs';
const BASE = 'https://orangepointstudio.github.io/ics2026/';
const set = [
  { ad: 'ics26-qr', url: BASE + '?s=qr', nereye: 'Stant ana QR (masa, tent, poster)' },
  { ad: 'ics26-flyer', url: BASE + '?s=flyer', nereye: 'Broşür / el ilanı' },
  { ad: 'ics26-ig', url: BASE + '?s=ig', nereye: 'Instagram story bağlantısı / görsel içi QR' },
];
fs.mkdirSync('../qr', { recursive: true });
const kanit = { uretim: new Date().toISOString(), arac: 'qrcode@1.5.4 ECC H margin 4 + jsqr@1.4.0', baski: 'Matbaaya SVG gönder. En küçük kenar: masa/tent 4 cm, broşür 3 cm, poster 15 cm. Sessiz alan (beyaz kenar) kırpılmaz.', set: [] };
for (const q of set) {
  const opt = { errorCorrectionLevel: 'H', margin: 4, color: { dark: '#0B0B0C', light: '#FFFFFF' } };
  fs.writeFileSync(`../qr/${q.ad}.svg`, await QRCode.toString(q.url, { ...opt, type: 'svg' }));
  const r = { ...q };
  for (const [etiket, scale] of [['buyuk', 24], ['kucuk', 8]]) {
    const f = `../qr/${q.ad}-${etiket}.png`;
    await QRCode.toFile(f, q.url, { ...opt, scale });
    const png = PNG.sync.read(fs.readFileSync(f));
    const d = jsQR(new Uint8ClampedArray(png.data), png.width, png.height);
    r['decode_' + etiket] = (d && d.data === q.url ? 'EŞLEŞTİ' : 'HATA:' + (d && d.data)) + ` (${png.width}px)`;
  }
  r.version = QRCode.create(q.url, { errorCorrectionLevel: 'H' }).version;
  kanit.set.push(r);
}
fs.writeFileSync('../qr/QR-KANIT.json', JSON.stringify(kanit, null, 2));
console.log(JSON.stringify(kanit.set.map(x => [x.ad, x.decode_buyuk, x.decode_kucuk, 'v' + x.version])));
