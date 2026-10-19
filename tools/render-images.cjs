// Renders static/img/og.png (1200x630) and apple-touch-icon.png (180x180).
// Usage: node tools/render-images.cjs   (needs Playwright + Chromium)
const path = require("path");
const fs = require("fs");
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node22/lib/node_modules/playwright"); }
const img = path.join(__dirname, "..", "static", "img");
const mark = fs.readFileSync(path.join(img, "logo-mark.svg"), "utf8");
const fonts = '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=DM+Mono:wght@500&family=DM+Sans:wght@500&display=swap" rel="stylesheet">';
const og = `<html><head>${fonts}<style>
body{margin:0;width:1200px;height:630px;background:#F6F5F0;font-family:'DM Sans';display:flex;flex-direction:column;justify-content:center;padding:0 80px;box-sizing:border-box;position:relative;overflow:hidden}
body:before{content:"";position:absolute;right:-200px;top:-260px;width:800px;height:800px;background:radial-gradient(closest-side,rgba(52,199,58,.28),rgba(52,199,58,0))}
.b{display:flex;align-items:center;gap:16px;font:800 44px 'Bricolage Grotesque';letter-spacing:-.04em}
.b svg{width:72px;height:72px;border-radius:18px}
.hl{background:linear-gradient(transparent 56%,#34C73A 56%,#34C73A 94%,transparent 94%)}
h1{font:800 84px/1 'Bricolage Grotesque';letter-spacing:-.045em;margin:44px 0 26px}
p{font:500 20px 'DM Mono';letter-spacing:.12em;color:#64665F;margin:0}
</style></head><body><div class="b">${mark}<span>Iowa <span class="hl">AEO</span></span></div>
<h1>Get recommended<br>by <span class="hl">AI in Iowa.</span></h1><p>DES MOINES · CEDAR RAPIDS · IOWA CITY · QUAD CITIES</p></body></html>`;
const icon = `<html><body style="margin:0;width:180px;height:180px">${mark.replace('<svg ', '<svg style="width:180px;height:180px" ')}</body></html>`;
(async () => {
  const b = await pw.chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.setContent(og, { waitUntil: "networkidle" });
  await p.screenshot({ path: path.join(img, "og.png") });
  await p.setViewportSize({ width: 180, height: 180 });
  await p.setContent(icon);
  await p.screenshot({ path: path.join(img, "apple-touch-icon.png") });
  await b.close();
})();
