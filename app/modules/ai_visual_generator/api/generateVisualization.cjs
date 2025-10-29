// Minimal HTTP server with concept registry and specialized templates
const http = require('http');
const fs = require('fs');
const path = require('path');

const baseDir = path.resolve(__dirname, '..');
const generatedDir = path.join(baseDir, 'generated');
if (!fs.existsSync(generatedDir)) fs.mkdirSync(generatedDir, { recursive: true });

const registryPath = path.join(baseDir, 'concepts.json');
let registry = {};
try { if (fs.existsSync(registryPath)) registry = JSON.parse(fs.readFileSync(registryPath, 'utf8')); } catch {}

function nowStamp(){const d=new Date();const p=n=>String(n).padStart(2,'0');return `${d.getFullYear()}${p(d.getMonth()+1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`}

function matchConcept(prompt){
  const k = Object.keys(registry||{});
  const p = String(prompt||'');
  for (const key of k){ if (p.includes(key)) return registry[key]; }
  return null;
}

function getLib(vizType){
  const t = String(vizType||'').toLowerCase();
  if (t.includes('统计')) return 'plotly';
  if (t.includes('网络')) return 'd3';
  if (t.includes('几何') || t.includes('3d') || t.includes('仿真')) return 'three';
  return 'plotly';
}

function normalHtml(){
  const cssLink = '../../../assets/style.css';
  return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="${cssLink}">
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.26.0/plotly.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>body{font-family:'Noto Sans SC',system-ui,-apple-system; margin:0;} .wrap{max-width:960px;margin:20px auto;padding:16px} .card{background:#f9f9fb;border-radius:16px;padding:16px;box-shadow:0 12px 30px rgba(0,0,0,.12)} .row{display:grid;grid-template-columns:1fr 1fr;gap:16px} .ctrl{display:flex;gap:12px;align-items:center;margin:10px 0}</style>
</head><body>
<header style="padding:16px;background:linear-gradient(135deg,#4A65F6,#6C8BFA);color:#fff;"><h1 style="margin:0;font-size:22px;">正态分布交互式可视化</h1><p style="margin:4px 0 0;opacity:.9;">PDF/CDF 随均值 μ 和标准差 σ 变化</p><a href="../../../../index.html" style="color:#fff;text-decoration:underline;">返回首页</a></header>
<div class="wrap">
  <div class="card">
    <div>公式：<span>\\( f(x)=\frac{1}{\sqrt{2\pi}\,\sigma}\exp\Big(-\frac{(x-\mu)^2}{2\sigma^2}\Big) \\)</span>；<span>\\( F(x)=\Phi\Big(\frac{x-\mu}{\sigma}\Big) \\)</span></div>
    <div class="ctrl"><label>均值 μ：</label><input id="mu" type="range" min="-3" max="3" step="0.1" value="0"><span id="muVal">0</span></div>
    <div class="ctrl"><label>标准差 σ：</label><input id="sigma" type="range" min="0.3" max="3" step="0.1" value="1"><span id="sigmaVal">1</span></div>
    <div class="row"><div id="pdf" style="height:360px"></div><div id="cdf" style="height:360px"></div></div>
  </div>
</div>
<script>(function(){
  function range(a,b,step){const r=[];for(let x=a;x<=b;x+=step) r.push(+x.toFixed(4));return r}
  function pdf(x,mu,sigma){const c=1/(Math.sqrt(2*Math.PI)*sigma);const e=Math.exp(-Math.pow(x-mu,2)/(2*sigma*sigma));return c*e}
  function cdf(x,mu,sigma){ // approx using error function
    const z=(x-mu)/(sigma*Math.SQRT2); // erf-based approximation
    const sign = z<0?-1:1; const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911; const t=1/(1+p*sign*z*sign); const y=1-((((a5*t+a4)*t+a3)*t+a2)*t+a1)*t*Math.exp(-z*z); const erf = sign*y; return 0.5*(1+erf);
  }
  const xs=range(-5,5,0.05);
  function draw(mu,sigma){
    const ysPDF=xs.map(x=>pdf(x,mu,sigma));
    const ysCDF=xs.map(x=>cdf(x,mu,sigma));
    Plotly.newPlot('pdf',[{x:xs,y:ysPDF,mode:'lines',line:{color:'#4A65F6'}},{x:[mu],y:[pdf(mu,mu,sigma)],mode:'markers',marker:{color:'#e93',size:8}}],{title:'PDF',margin:{t:30}});
    Plotly.newPlot('cdf',[{x:xs,y:ysCDF,mode:'lines',line:{color:'#6C8BFA'}}],{title:'CDF',margin:{t:30}});
    document.getElementById('muVal').textContent=mu.toFixed(1);
    document.getElementById('sigmaVal').textContent=sigma.toFixed(1);
  }
  const muEl=document.getElementById('mu'); const sigmaEl=document.getElementById('sigma');
  function update(){draw(parseFloat(muEl.value),parseFloat(sigmaEl.value));}
  muEl.addEventListener('input',update); sigmaEl.addEventListener('input',update); draw(0,1);
})();</script>
</body></html>`;
}

function getHtmlForViz(prompt, vizType, complexity){
  const lib = getLib(vizType);
  const p = String(prompt||'');
  if (p.includes('正态分布')||p.toLowerCase().includes('gaussian')) return normalHtml();
  const cssLink='../../../assets/style.css';
  if (lib==='three'){
    return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="${cssLink}"><script src="https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.min.js"></script></head><body><header style="padding:16px;background:linear-gradient(135deg,#4A65F6,#6C8BFA);color:#fff;"><h1 style="margin:0;font-size:22px;">AI 生成的交互式可视化</h1><a href="../../../../index.html" style="color:#fff;text-decoration:underline;">返回首页</a></header><div class="wrap"><div class="card"><canvas id="c" style="width:100%;height:420px"></canvas></div></div><script>(function(){const w=800,h=420;const r= new THREE.WebGLRenderer({canvas:document.getElementById('c')});r.setSize(w,h);const scene=new THREE.Scene();const cam=new THREE.PerspectiveCamera(45,w/h,0.1,100);cam.position.set(3,3,6);scene.add(new THREE.AmbientLight(0xffffff,0.6));const g=new THREE.BoxGeometry(1,1,1);const m=new THREE.MeshPhongMaterial({color:0x4A65F6});const cube=new THREE.Mesh(g,m);scene.add(cube);function loop(){cube.rotation.x+=0.01;cube.rotation.y+=0.015;r.render(scene,cam);requestAnimationFrame(loop);}loop();})();</script></body></html>`;
  }
  if (lib==='plotly'){
    return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="${cssLink}"><script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.26.0/plotly.min.js"></script></head><body><header style="padding:16px;background:linear-gradient(135deg,#4A65F6,#6C8BFA);color:#fff;"><h1 style="margin:0;font-size:22px;">AI 生成的交互式可视化</h1><a href="../../../../index.html" style="color:#fff;text-decoration:underline;">返回首页</a></header><div class="wrap"><div class="card"><div id="chart" style="height:420px"></div></div></div><script>(function(){const x=[...Array(100)].map((_,i)=>i);const y=x.map(i=>Math.sin(i/10)+Math.random()*0.2);Plotly.newPlot('chart',[{x,y,type:'scatter',mode:'lines',line:{color:'#4A65F6'}}]);})();</script></body></html>`;
  }
  return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="${cssLink}"><script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script></head><body><header style="padding:16px;background:linear-gradient(135deg,#4A65F6,#6C8BFA);color:#fff;"><h1 style="margin:0;font-size:22px;">AI 生成的交互式可视化</h1><a href="../../../../index.html" style="color:#fff;text-decoration:underline;">返回首页</a></header><div class="wrap"><div class="card"><svg id="viz" width="100%" height="520"></svg></div></div><script>(function(){const svg=d3.select('#viz');const w=svg.node().clientWidth,h=520;svg.attr('viewBox','0 0 '+w+' '+h);const nodes=d3.range(40).map(i=>({radius:6+Math.random()*12}));const sim=d3.forceSimulation(nodes).force('charge',d3.forceManyBody().strength(-40)).force('center',d3.forceCenter(w/2,h/2)).force('collision',d3.forceCollide().radius(d=>d.radius+2));const g=svg.append('g');const cs=g.selectAll('circle').data(nodes).enter().append('circle').attr('r',d=>d.radius).attr('fill','#4A65F6').attr('opacity',.85);svg.call(d3.zoom().on('zoom',e=>g.attr('transform',e.transform)));sim.on('tick',()=>{cs.attr('cx',d=>d.x).attr('cy',d=>d.y);});})();</script></body></html>`;
}

const server = http.createServer((req,res)=>{
  const {method,url}=req;
  res.setHeader('Access-Control-Allow-Origin','*');
  res.setHeader('Access-Control-Allow-Methods','POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers','Content-Type');
  if (method==='OPTIONS'){res.statusCode=204;return res.end();}
  if (method==='POST' && url==='/api/generateVisualization'){
    let body='';
    req.on('data',c=>{body+=c;if(body.length>1e6) req.destroy();});
    req.on('end',()=>{
      try {
        const payload=JSON.parse(body||'{}');
        const {prompt='',vizType='自定义',complexity='中等'}=payload;
        const direct = matchConcept(prompt);
        if (direct){ res.setHeader('Content-Type','application/json'); return res.end(JSON.stringify({status:'success',path:direct,source:'registry'})); }
        const html=getHtmlForViz(prompt,vizType,complexity);
        const fname=`viz_${nowStamp()}.html`; const fpath=path.join(generatedDir,fname); fs.writeFileSync(fpath,html,'utf8');
        const relPath=`/app/modules/ai_visual_generator/generated/${fname}`;
        res.setHeader('Content-Type','application/json');
        res.end(JSON.stringify({status:'success',file:fname,path:relPath}));
      } catch(err){ res.statusCode=500; res.end('服务器错误：'+err.message); }
    });
    return;
  }
  res.statusCode=404; res.end('Not Found');
});

const PORT=process.env.PORT||5050;
server.listen(PORT,()=>{ console.log(`AI Visualization Generator API listening on http://localhost:${PORT}`); });