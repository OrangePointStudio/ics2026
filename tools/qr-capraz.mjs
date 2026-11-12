// Çapraz test: (1) baskı SVG'si resvg ile PNG'ye çevrilip çözülür, (2) story görselindeki eğik QR tüm görselden çözülür.
import { Resvg } from '@resvg/resvg-js'; import jsQR from 'jsqr'; import { PNG } from 'pngjs'; import fs from 'node:fs';
const coz = (buf) => { const p = PNG.sync.read(buf); const d = jsQR(new Uint8ClampedArray(p.data), p.width, p.height); return d ? d.data : null; };
const out = {};
for (const ad of ['ics26-qr', 'ics26-flyer', 'ics26-ig']) {
  for (const w of [600, 250]) {
    const png = new Resvg(fs.readFileSync(`../qr/${ad}.svg`, 'utf8'), { fitTo: { mode: 'width', value: w }, background: '#fff' }).render().asPng();
    out[`${ad}.svg@${w}px`] = coz(png);
  }
}
out['story R3 (eğik QR, tüm görsel)'] = coz(fs.readFileSync('../sosyal/cikti/fv/FV-ICS-R3_story_1080x1920.png'));
console.log(JSON.stringify(out, null, 1));
fs.writeFileSync('../qr/QR-CAPRAZ-TEST.json', JSON.stringify({ zaman: new Date().toISOString(), sonuc: out }, null, 2));
