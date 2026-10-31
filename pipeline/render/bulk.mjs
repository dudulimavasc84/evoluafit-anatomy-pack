import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const MIME={'.html':'text/html','.js':'text/javascript','.glb':'model/gltf-binary','.mjs':'text/javascript','.wasm':'application/wasm'};
const srv=http.createServer((q,r)=>{const p=path.join(process.cwd(),decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return;}r.writeHead(200,{'content-type':MIME[path.extname(p)]||'application/octet-stream'});r.end(d);});}).listen(8766);
const groups=fs.readdirSync('glb').map(f=>f.replace('.glb','')).filter(g=>g!=='musculo_outro');
groups.push('musculo_outro');
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage({viewport:{width:800,height:1600}});
pg.on('console',m=>console.log('console:',m.text())); pg.on('pageerror',e=>console.log('err',e.message));
await pg.goto('http://localhost:8766/bulk.html?groups='+groups.join(','));
await pg.waitForFunction('window.__done',{timeout:240000});
console.log(await pg.evaluate('window.__groups'));
const jobs=JSON.parse(process.argv[2]);
fs.mkdirSync('out',{recursive:true});
for(const j of jobs){const d=await pg.evaluate(s=>window.renderSpec(s),j);fs.writeFileSync('out/'+j.name+'.png',Buffer.from(d.split(',')[1],'base64'));console.log('ok',j.name);}
await b.close();srv.close();
