// QR PNG -> çözülen URL -> canlı sayfa -> sayfadaki dış bağlantılar (HTTP durumu). Çıktı: ../qr/UCTAN-UCA-TEST.json
import jsQR from 'jsqr'; import { PNG } from 'pngjs'; import fs from 'node:fs';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1';
const sonuc = { zaman: new Date().toISOString(), qr: [] };
for (const ad of ['ics26-qr', 'ics26-flyer', 'ics26-ig']) {
  const p = PNG.sync.read(fs.readFileSync(`../qr/${ad}-buyuk.png`));
  const url = jsQR(new Uint8ClampedArray(p.data), p.width, p.height)?.data;
  const r = await fetch(url, { headers: { 'User-Agent': UA } });
  const html = await r.text();
  const s = new URL(url).searchParams.get('s');
  const store = html.match(/href="(https:\/\/apps\.apple\.com[^"]+)"/)[1].replace(/&amp;/g, '&');
  // sayfa JS'inin yapacağı ct dönüşümünü uygula
  const storeFinal = store.replace(/ct=ics26f-land(?:-[a-z]+)?/, 'ct=ics26f-land-' + s);
  sonuc.qr.push({ ad, url, sayfa: r.status, baslik: html.match(/<title>(.*?)<\/title>/)[1], appStore: storeFinal });
}
const linkler = {};
for (const u of [sonuc.qr[0].appStore, 'https://www.instagram.com/app.fusionvision/', 'https://www.instagram.com/orangepointstudio/', 'https://fusionvision.app/privacy']) {
  let r = await fetch(u, { headers: { 'User-Agent': UA }, redirect: 'manual' });
  const ilk = { durum: r.status, yonlendirme: r.headers.get('location') };
  if (r.status >= 300 && r.status < 400 && /^https?:/.test(ilk.yonlendirme || '')) r = await fetch(new URL(ilk.yonlendirme, u), { headers: { 'User-Agent': UA } });
  const t = r.status < 300 ? await r.text() : '';
  linkler[u] = { ...ilk, sonDurum: r.status, uygulamaAdi: /Fusion Vision/i.test(t), ctKorundu: (ilk.yonlendirme || u).includes('ct=') };
}
sonuc.linkler = linkler;
fs.writeFileSync('../qr/UCTAN-UCA-TEST.json', JSON.stringify(sonuc, null, 2));
console.log(JSON.stringify(sonuc, null, 1));
