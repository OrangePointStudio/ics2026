// SVG -> PNG (resvg). Kullanım: node render.mjs <girdi.svg> <çıktı.png> [genişlik]
import { Resvg } from '@resvg/resvg-js';
import fs from 'node:fs';
const [, , inp, out, w] = process.argv;
const svg = fs.readFileSync(inp, 'utf8');
const r = new Resvg(svg, {
  fitTo: w ? { mode: 'width', value: Number(w) } : { mode: 'original' },
  font: { loadSystemFonts: true, defaultFontFamily: 'Avenir Next' },
  background: 'rgba(0,0,0,0)',
});
fs.writeFileSync(out, r.render().asPng());
console.log('ok', out);
