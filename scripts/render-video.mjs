#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';

const HELP = `Render HTML determinista a PNG o MP4.
--project DIR      Carpeta con index.html y recursos locales
--output FILE      PNG con --still, o MP4
--entry FILE       HTML relativo al proyecto (index.html por defecto)
--still SECONDS    Capturar un instante, sin codificar vídeo
--width N --height N --fps N --duration N  Sustituir videoSpec
--audio FILE       Mezcla local de voz/música/efectos para MP4
--start N --end N   Exportar intervalo del reloj original; recorta el audio igual
--subframes N      1, 2, 4 u 8 muestras temporales por fotograma (default 1)
--shutter N        Fracción de exposición 0..1 (default 0.5)
--overwrite        Permitir sustituir la exportación
--help             Mostrar ayuda
Requiere Playwright/Chromium; MP4 requiere FFmpeg.
Resolución de módulos: instalación normal, VIDEO_NODE_MODULES, runtime o
~/.cache/crear-videos-con-codigo (lo deja ahí scripts/preparar-entorno.sh).
No permite solicitudes de recursos externos durante el render.`;

function parse(args) {
  const opts = {};
  const flags = new Set(['help','overwrite']);
  const values = new Set(['project','output','entry','still','width','height','fps','duration','audio','start','end','subframes','shutter']);
  for (let i=0;i<args.length;i++) {
    const key=args[i].replace(/^--/,'');
    if (flags.has(key)) opts[key]=true;
    else if (values.has(key) && args[i+1] && !args[i+1].startsWith('--')) opts[key]=args[++i];
    else throw new Error(`Opción inválida o sin valor: ${args[i]}`);
  }
  return opts;
}
async function exists(file) {try {await fs.access(file);return true;} catch {return false;}}
function inside(root,file) {const rel=path.relative(root,file);return rel===''||(!rel.startsWith('..'+path.sep)&&rel!=='..'&&!path.isAbsolute(rel));}
async function run(command,args) {
  await new Promise((resolve,reject)=>{
    const p=spawn(command,args,{stdio:['ignore','ignore','pipe']});let errors='';
    p.stderr.on('data',d=>{errors=(errors+d.toString()).slice(-12000);});
    p.on('error',reject);p.on('close',code=>code===0?resolve():reject(new Error(`${command}: ${errors||'exit '+code}`)));
  });
}
function playwright() {
  const local=createRequire(import.meta.url);
  try {return local('playwright');} catch {}
  // La última ruta es donde instala Playwright scripts/preparar-entorno.sh.
  const prepared=path.join(os.homedir(),'.cache','crear-videos-con-codigo','node_modules');
  for (const dir of [process.env.VIDEO_NODE_MODULES,process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,prepared].filter(Boolean)) {
    try {return createRequire(path.join(dir,'package.json'))('playwright');} catch {}
  }
  throw new Error('Playwright no está disponible; resolver la instalación antes de producir.');
}
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf','.mp4':'video/mp4','.wav':'audio/wav','.json':'application/json'};
async function main() {
  const o=parse(process.argv.slice(2));
  if(o.help){console.log(HELP);return;}
  if(!o.project||!o.output)throw new Error('Se requieren --project y --output. Usar --help.');
  const root=await fs.realpath(path.resolve(o.project));
  const entry=o.entry||'index.html';
  const entryPath=await fs.realpath(path.resolve(root,entry));
  if(!inside(root,entryPath))throw new Error('El HTML debe estar dentro del proyecto.');
  const output=path.resolve(o.output),still=o.still!==undefined;
  if(path.extname(output).toLowerCase()!==(still?'.png':'.mp4'))throw new Error('Usar PNG para --still y MP4 para vídeo.');
  if(await exists(output)&&!o.overwrite)throw new Error('La exportación existe; usar otro nombre o --overwrite.');
  if(o.audio){o.audio=await fs.realpath(path.resolve(o.audio));if(still)throw new Error('--audio no se usa con --still.');}
  await fs.mkdir(path.dirname(output),{recursive:true});
  if(!still)await run('ffmpeg',['-version']);
  const failures=new Set();
  const server=http.createServer(async(req,res)=>{
    try {
      const url=new URL(req.url,'http://localhost');
      const wanted=path.resolve(root,'.'+decodeURIComponent(url.pathname));
      const real=await fs.realpath(wanted);
      if(!inside(root,real)){res.writeHead(403);res.end();return;}
      const stat=await fs.stat(real);if(!stat.isFile())throw new Error('not file');
      res.writeHead(200,{'Content-Type':types[path.extname(real)]||'application/octet-stream'});
      res.end(await fs.readFile(real));
    }catch {res.writeHead(404);res.end();}
  });
  let browser,temp;
  try {
    await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
    const origin=`http://127.0.0.1:${server.address().port}`;
    const {chromium}=playwright();
    const executable=process.env.VIDEO_CHROMIUM_PATH||(await exists(chromium.executablePath())?chromium.executablePath():undefined);
    browser=await chromium.launch({headless:true,...(executable?{executablePath:executable}:{})});
    const context=await browser.newContext({viewport:{width:1280,height:720},deviceScaleFactor:1,serviceWorkers:'block'});
    await context.route('**/*',async route=>{
      const url=route.request().url();
      if(url.startsWith(origin+'/')||url.startsWith('data:')||url.startsWith('blob:'))await route.continue();
      else {failures.add('Recurso externo bloqueado: '+url);await route.abort();}
    });
    const page=await context.newPage();
    page.on('pageerror',e=>failures.add(e.message));
    page.on('response',r=>{if(r.status()>=400)failures.add('HTTP '+r.status()+': '+r.url());});
    page.on('requestfailed',r=>failures.add('Solicitud fallida: '+r.url()));
    const relative=path.relative(root,entryPath).split(path.sep).map(encodeURIComponent).join('/');
    await page.goto(origin+'/'+relative,{waitUntil:'networkidle'});
    if(failures.size)throw new Error('Erro ao abrir a página (corrija antes de renderizar):\n'+[...failures].join('\n'));
    const spec=await page.evaluate(()=>window.videoSpec||{});
    const overrides={};for(const key of ['width','height','fps','duration'])overrides[key]=Number(o[key]??spec[key]);
    const {width,height,fps,duration}=overrides;
    if(!Number.isInteger(width)||!Number.isInteger(height)||width<=0||height<=0||width%2||height%2)throw new Error('Ancho/alto deben ser enteros positivos pares.');
    if(!Number.isInteger(fps)||fps<1||fps>120||!Number.isFinite(duration)||duration<=0)throw new Error('FPS debe estar entre 1 y 120; duración positiva.');
    await page.setViewportSize({width,height});
    await page.evaluate(async values=>{
      Object.assign(window.videoSpec,values);
      if(typeof window.seek!=='function')throw new Error('Falta window.seek(t).');
      if(!window.renderReady||typeof window.renderReady.then!=='function')throw new Error('Falta la promesa window.renderReady.');
      await window.renderReady;await document.fonts.ready;
    },overrides);
    function check(){if(failures.size)throw new Error('Errores durante render:\n'+[...failures].join('\n'));}
    async function capture(t,destination){
      await page.evaluate(async time=>{await window.seek(time);},t);
      check();await page.screenshot({path:destination,type:'png',fullPage:false});check();
    }
    check();
    if(still){
      const t=Number(o.still);if(!Number.isFinite(t)||t<0||t>=duration)throw new Error('--still debe estar dentro de la duración.');
      await capture(t,output);console.log(JSON.stringify({output,time:t,width,height}));return;
    }
    temp=await fs.mkdtemp(path.join(os.tmpdir(),'video-frames-'));
    const start=Number(o.start??0),end=Number(o.end??duration);
    const sub=Number(o.subframes??1),shutter=Number(o.shutter??.5);
    if(!Number.isFinite(start)||!Number.isFinite(end)||start<0||end<=start||end>duration)throw new Error('Intervalo fuera de duración.');
    if(![1,2,4,8].includes(sub)||!Number.isFinite(shutter)||shutter<0||shutter>1)throw new Error('Subframes o shutter inválidos.');
    const count=Math.ceil((end-start)*fps),actual=count/fps;
    // Verify arbitrary seeking at a nonzero instant, including a backwards jump.
    const checkTime=start+(end-start)*.37;
    await capture(checkTime,path.join(temp,'seek-a.png'));
    await page.evaluate(async t=>{await window.seek(t);},Math.max(0,duration*.73));
    await capture(checkTime,path.join(temp,'seek-b.png'));
    const [a,b]=await Promise.all([fs.readFile(path.join(temp,'seek-a.png')),fs.readFile(path.join(temp,'seek-b.png'))]);
    // Chrome puede variar el antialiasing de texto entre dos rasterizados del mismo DOM (medido: DOM
    // idéntico, 367 px con diferencia máxima 19/255). Se tolera ese ruido sub-perceptual; un cambio de
    // estado real (geometría, contenido) sigue haciendo fallar el render.
    if(!a.equals(b)){
      const diff=await page.evaluate(async([pa,pb])=>{
        const load=src=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=src;});
        const [ia,ib]=await Promise.all([load(pa),load(pb)]);
        const c=document.createElement('canvas');c.width=ia.width;c.height=ia.height;const g=c.getContext('2d');
        g.drawImage(ia,0,0);const da=g.getImageData(0,0,c.width,c.height).data;g.drawImage(ib,0,0);const db=g.getImageData(0,0,c.width,c.height).data;
        let n=0,mx=0;for(let i=0;i<da.length;i+=4){const d=Math.max(Math.abs(da[i]-db[i]),Math.abs(da[i+1]-db[i+1]),Math.abs(da[i+2]-db[i+2]));if(d>0)n++;if(d>mx)mx=d;}
        return {n,mx,total:da.length/4};
      },['data:image/png;base64,'+a.toString('base64'),'data:image/png;base64,'+b.toString('base64')]);
      console.error('Determinismo: diferencia de raster',JSON.stringify(diff));
      if(diff.mx>32||diff.n>diff.total*0.002)throw new Error('seek(t) no es determinista: el mismo instante cambió tras un salto.');
    }
    for(let i=0;i<count;i++){
      for(let j=0;j<sub;j++){
        const sample=Math.max(0,Math.min(duration-1e-9,start+i/fps+((j+.5)/sub-.5)*shutter/fps));
        await capture(sample,path.join(temp,`frame-${String(i*sub+j).padStart(6,'0')}.png`));
      }
      if(i===0||(i+1)%fps===0)console.error(`Frames ${i+1}/${count}`);
    }
    const args=['-v','error',o.overwrite?'-y':'-n','-framerate',String(fps*sub),'-i',path.join(temp,'frame-%06d.png')];
    if(o.audio)args.push('-ss',String(start),'-i',o.audio,'-map','0:v:0','-map','1:a:0','-af','apad','-c:a','aac','-b:a','192k');
    else args.push('-an');
    if(sub>1)args.push('-vf',`tmix=frames=${sub},select='eq(mod(n\\,${sub})\\,${sub-1})',setpts=N/${fps}/TB`);
    args.push('-r',String(fps),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-t',String(actual),'-movflags','+faststart',output);
    await run('ffmpeg',args);
    await fs.writeFile(output+'.render.json',JSON.stringify({output,width,height,fps,requested_duration:end-start,source_start:start,source_end:end,subframes:sub,shutter,duration:actual,frames:count,audio:!!o.audio,deterministic_seek_check:true},null,2));
    console.log(JSON.stringify({output,width,height,fps,duration:actual,frames:count,audio:!!o.audio}));
  } finally {
    if(browser)await browser.close();
    await new Promise(resolve=>server.close(resolve));
    if(temp)await fs.rm(temp,{recursive:true,force:true});
  }
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
