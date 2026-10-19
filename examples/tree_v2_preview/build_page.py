"""Build design/examples/Tree_v2_Preview.html from results.json (numbers are never retyped). SYNTHETIC."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "design" / "examples" / "Tree_v2_Preview.html"

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tree Architecture Preview</title>
<style>
:root{--bg:#f6f7f9;--panel:#fff;--text:#1c2230;--muted:#5c6575;--line:#cdd3dc;--edge:#9aa3b2;
--n-fill:#e4f0fa;--n:#0072b2;--d-fill:#fdf0d5;--d:#b77900;--c-fill:#fbe2d6;--c:#c4510b;
--sell:#c4510b;--add:#1b7f3b;--refi:#6a1b9a;--lever:#0b5cad;--fund:#455a64;--pace:#8d6e00;--sel:#111}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#10141b;--panel:#1a202a;--text:#e8ecf2;--muted:#9ba5b6;--line:#343c4a;--edge:#5f6a7d;
--n-fill:#10283b;--n:#56b4e9;--d-fill:#33280f;--d:#f0c25a;--c-fill:#3a1e12;--c:#ff9a5c;--sell:#ff9a5c;--add:#6fd08c;--refi:#d7a7ff;--lever:#7fb8ff;--fund:#b0bec5;--pace:#f0c25a;--sel:#fff}}
:root[data-theme="dark"]{--bg:#10141b;--panel:#1a202a;--text:#e8ecf2;--muted:#9ba5b6;--line:#343c4a;--edge:#5f6a7d;
--n-fill:#10283b;--n:#56b4e9;--d-fill:#33280f;--d:#f0c25a;--c-fill:#3a1e12;--c:#ff9a5c;--sell:#ff9a5c;--add:#6fd08c;--refi:#d7a7ff;--lever:#7fb8ff;--fund:#b0bec5;--pace:#f0c25a;--sel:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 "Segoe UI",system-ui,Arial,sans-serif}
header,main,footer{max-width:1500px;margin:0 auto;padding:0 16px}h1{font-size:24px;margin:16px 0 4px}.sub{color:var(--muted);margin:0 0 8px}
.badge{border:1px dashed var(--muted);border-radius:4px;padding:1px 8px;font-size:12px;font-weight:600}
button{font:inherit;border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:6px;padding:5px 12px;cursor:pointer}
button[aria-pressed="true"]{box-shadow:inset 0 0 0 2px var(--lever);font-weight:600}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:8px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 420px;gap:14px;align-items:start}@media(max-width:1150px){.grid{grid-template-columns:1fr}}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}
.kpi{background:var(--bg);border-radius:8px;padding:10px}.kpi h3{margin:0 0 4px;font-size:13px}.kpi .big{font-size:24px;font-weight:700}.kpi small{color:var(--muted)}
svg#tree{width:100%;height:auto;display:block;min-width:820px}.wrap{overflow-x:auto}
.edge{fill:none;stroke:var(--edge);stroke-width:1.3}.colh{font-size:14px;font-weight:700;fill:var(--text)}.cols{font-size:11.5px;fill:var(--muted)}
.nd rect{stroke-width:1.5;cursor:pointer}.nd text{font-size:11.5px;fill:var(--text);pointer-events:none}.nd .m{fill:var(--muted)}
.rN rect{fill:var(--n-fill);stroke:var(--n)}.rD rect{fill:var(--d-fill);stroke:var(--d)}.rC rect{fill:var(--c-fill);stroke:var(--c)}
.nd.sel rect{stroke:var(--sel);stroke-width:3}.nd:focus{outline:none}.nd:focus rect{stroke-width:3}
.chip{display:inline-block;border-radius:10px;padding:0 7px;font-size:11.5px;font-weight:700;color:#fff;margin-right:4px}
.SELL{background:var(--sell)}.ADD{background:var(--add)}.REFINANCE{background:var(--refi)}.LEVER{background:var(--lever)}.FUND{background:var(--fund)}.PACE{background:var(--pace)}.REPAY{background:#78909c}
table{border-collapse:collapse;width:100%;font-size:12.5px}td,th{padding:3px 5px;border-bottom:1px solid var(--line);text-align:left}td.v,th.v{text-align:right;font-variant-numeric:tabular-nums}
h2{font-size:16px;margin:2px 0 8px}h3.sec{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin:12px 0 4px}
.barrow{display:grid;grid-template-columns:150px 1fr 60px;gap:8px;align-items:center;margin:4px 0}.track{background:var(--bg);border-radius:4px;height:14px}.fill{background:var(--lever);height:14px;border-radius:4px}
footer{color:var(--muted);font-size:12px;margin:18px auto 28px}
</style></head><body>
<header><div class="bar" style="justify-content:space-between"><h1>Tree Architecture Preview</h1><div><span class="badge">SYNTHETIC – NOT ADIC DATA</span> <button id="theme" type="button">Dark theme</button></div></div>
<p class="sub" id="metaLine"></p></header>
<main>
<div class="card"><h2>What the optimizer adds (same tree, same limits)</h2><div class="kpis" id="kpis"></div>
<p class="sub" style="margin-top:8px">Goal = 10% a year over 3 years, gross of the owner's draws. All plans pay the owner at every node, keep the 4% cash floor, the 1.30× leverage cap and the borrowing limits. The two optimized plans also keep the worst-10% average no worse than −3% a year.</p></div>
<div class="bar"><span>Show actions of:</span><button type="button" id="pGoal" aria-pressed="true">Goal-seeking plan</button><button type="button" id="pCrra" aria-pressed="false">Risk-averse plan</button>
<span class="sub" style="margin:0">Click a Year-1 box to see its 5 Year-2 branches; click a Year-2 box to see its 4 Year-3 outcomes.</span></div>
<div class="grid"><div class="card wrap"><svg id="tree" viewBox="0 0 1060 760" role="img" aria-label="Scenario tree"></svg></div>
<aside class="card" id="panel" aria-live="polite"></aside></div>
<div class="grid" style="margin-top:14px"><div class="card"><h2>Where the gain comes from (goal-seeking plan, one action family switched off at a time)</h2><div id="abl"></div>
<p class="sub">Each bar is the probability of reaching the goal when that family of actions is removed and the plan re-optimized. SELL cannot be removed: the owner's draws could not be paid.</p></div>
<div class="card"><h2>Three marks → one belief, per holding</h2><div style="max-height:420px;overflow:auto"><table id="fus"></table></div></div></div>
<div class="card" style="margin-top:14px"><h2>How to read this</h2><ol>
<li>Each box is a possible future. Colour = regime (blue normal, amber PE drought, orange crisis with an oil shock); <b>p</b> = probability of reaching it.</li>
<li>Today's box holds the only decisions executed now. Every other box is the plan if that branch happens; the whole tree is re-solved each quarter.</li>
<li>At every box the optimizer chooses for each of the 24 holdings: <span class="chip SELL">SELL</span><span class="chip ADD">ADD</span><span class="chip REFINANCE">REFINANCE</span> (cash-out borrowing against the holding), plus <span class="chip LEVER">LEVER</span> (synthetic exposure, or adds funded by new debt), <span class="chip FUND">FUND</span> (revolver) and <span class="chip PACE">PACE</span> (cut new PE commitments).</li>
<li>One linear program decides all 61 decision boxes together; the same inputs always give the same plan.</li></ol></div>
</main>
<footer>Source: examples/tree_v2_preview/results.json (tree_v2.py). Preview built in 30 minutes; the full verified prototype (examples/mpo_v2) adds ~60 holdings, all instruments, buffered-probability selection and out-of-sample probabilities. SYNTHETIC.</footer>
<script id="data" type="application/json">{{DATA}}</script>
<script>
(function(){
const D=JSON.parse(document.getElementById('data').textContent);
const N=Object.fromEntries(D.nodes.map(n=>[n.id,n]));
let plan='goal', selT1=null, selT2=null, selNode=0;
const pct=v=>v==null?'n/a':(v*100).toFixed(1)+'%', bn=v=>v==null?'':v.toFixed(2);
const REG={N:'Normal',D:'PE drought',C:'Crisis + oil shock'};
document.getElementById('metaLine').textContent=`${D.meta.tree}. ${D.meta.holdings} holdings across eight groups. Goal: ${D.meta.goal}. Solver: ${D.meta.solver}; all runs and ablations in ${D.meta.runtime_s}s.`;
function kpis(){const r=D.runs;const k=[['Status quo (sell liquid only)',r.status_quo_sell_liquid_only],['Optimized: risk-averse',r.optimized_crra],['Optimized: goal-seeking',r.goal_seeking]];
document.getElementById('kpis').innerHTML=k.map(([t,s])=>`<div class="kpi"><h3>${t}</h3><div class="big">${pct(s.p_goal)}</div><small>P(reach 10% a year)</small><br><small>expected ${pct(s.expected_ann)} a yr · median ${pct(s.median_ann)} · worst-10% avg ${pct(s.cvar10_ann)} a yr · P(loss) ${pct(s.p_loss)}</small></div>`).join('')}
function abl(){const base=D.runs.goal_seeking.p_goal;const rows=[['All actions (goal-seeking)',base]].concat(Object.entries(D.ablation_goal_seeking).map(([k,v])=>['without '+k,v.p_goal]));
const mx=Math.max(...rows.map(r=>r[1]||0),0.01);document.getElementById('abl').innerHTML=rows.map(([k,v])=>`<div class="barrow"><span>${k}</span><div class="track"><div class="fill" style="width:${v==null?0:100*v/mx}%"></div></div><span>${v==null?'infeasible':pct(v)}</span></div>`).join('')}
function fus(){document.getElementById('fus').innerHTML='<tr><th>Holding</th><th class="v">Value</th><th class="v">Underwritten</th><th class="v">Actual</th><th class="v">Forecast</th><th class="v">Fused</th></tr>'+D.fusion.map(f=>`<tr><td>${f.holding}<br><span style="color:var(--muted)">${D.groups[f.group]}</span></td><td class="v">${bn(f.value)}</td><td class="v">${pct(f.underwritten)}</td><td class="v">${pct(f.actual)}</td><td class="v">${pct(f.forecast)}</td><td class="v"><b>${pct(f.fused)}</b></td></tr>`).join('')}
function acts(n){return (plan==='goal'?n.actions_goal:n.actions_crra)||[]}
function summaryChips(n){const a=acts(n);const c={};a.forEach(x=>{const l=x.lens.startsWith('ADD (')?'LEVER':x.lens;c[l]=(c[l]||0)+x.amt});return Object.entries(c).map(([l,v])=>`${l} ${v.toFixed(1)}`).join(' · ')||'HOLD'}
function box(n,x,y,w,h,label){const t=`<g class="nd r${n.regime}${selNode===n.id?' sel':''}" data-id="${n.id}" tabindex="0" role="button" aria-label="${n.path} p=${n.p.toFixed(3)}"><title>${n.path} · ${REG[n.regime]} · p=${n.p.toFixed(3)}</title><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="7"/>`+label+'</g>';return t}
function edge(x1,y1,x2,y2){const m=(x1+x2)/2;return `<path class="edge" d="M${x1},${y1} C${m},${y1} ${m},${y2} ${x2},${y2}"/>`}
function render(){
 const root=N[0], t1=root.children.map(i=>N[i]);
 if(selT1==null)selT1=t1[0].id; const t2=N[selT1].children.map(i=>N[i]); if(selT2==null||!N[selT1].children.includes(selT2))selT2=t2[0].id; const t3=N[selT2].children.map(i=>N[i]);
 let s='';const X=[10,230,520,800],W=[200,260,250,250];
 s+=`<text class="colh" x="${X[0]}" y="20">Today (t0)</text><text class="cols" x="${X[0]}" y="36">executed now</text>`;
 s+=`<text class="colh" x="${X[1]}" y="20">Year 1: 10 scenarios</text><text class="cols" x="${X[1]}" y="36">contingent plans</text>`;
 s+=`<text class="colh" x="${X[2]}" y="20">Year 2: 5 branches of ${N[selT1].path}</text><text class="cols" x="${X[2]}" y="36">contingent plans</text>`;
 s+=`<text class="colh" x="${X[3]}" y="20">Year 3: 4 outcomes of ${N[selT2].path}</text><text class="cols" x="${X[3]}" y="36">return a year incl. draws</text>`;
 const top=50,H1=78,G1=5; const y1=t1.map((n,i)=>top+i*(H1+G1)); const tot=t1.length*(H1+G1);
 const yr=top+tot/2-60;
 t1.forEach((n,i)=>{s+=edge(X[0]+W[0],yr+60,X[1],y1[i]+H1/2)});
 s+=box(root,X[0],yr,W[0],120,`<text x="${X[0]+10}" y="${yr+18}" font-weight="700">TODAY · PE drought</text>`+wrap(summaryChips(root),X[0]+10,yr+38,30)+`<text class="m" x="${X[0]+10}" y="${yr+112}">click for the change list</text>`);
 t1.forEach((n,i)=>{const y=y1[i];s+=box(n,X[1],y,W[1],H1,`<text x="${X[1]+8}" y="${y+16}" font-weight="700">${n.path} <tspan class="m">p=${n.p.toFixed(3)} · equity ${pct(n.factor_return)}</tspan></text>`+wrap(summaryChips(n),X[1]+8,y+32,40)+`<text class="m" x="${X[1]+8}" y="${y+H1-6}">draw ${bn(n.owner_draw)} · NAV ${bn(n.nav)}</text>`)});
 const iSel=t1.findIndex(n=>n.id===selT1);const H2=110,G2=12;const y2=t2.map((n,i)=>top+i*(H2+G2)+20);
 t2.forEach((n,i)=>{s+=edge(X[1]+W[1],y1[iSel]+H1/2,X[2],y2[i]+H2/2)});
 t2.forEach((n,i)=>{const y=y2[i];s+=box(n,X[2],y,W[2],H2,`<text x="${X[2]+8}" y="${y+16}" font-weight="700">${n.path} <tspan class="m">p=${n.p.toFixed(4)}</tspan></text><text class="m" x="${X[2]+8}" y="${y+32}">equity ${pct(n.factor_return)} · draw ${bn(n.owner_draw)}</text>`+wrap(summaryChips(n),X[2]+8,y+50,38)+`<text class="m" x="${X[2]+8}" y="${y+H2-6}">cash ${bn(n.cash)} · revolver ${bn(n.revolver)} · loans ${bn(n.loans)}</text>`)});
 const j=t2.findIndex(n=>n.id===selT2);const H3=70,G3=16;const y3=t3.map((n,i)=>top+40+i*(H3+G3)+j*40);
 t3.forEach((n,i)=>{s+=edge(X[2]+W[2],y2[j]+H2/2,X[3],y3[i]+H3/2)});
 t3.forEach((n,i)=>{const y=y3[i];const wm=plan==='goal'?n.wealth_multiple_goal:n.wealth_multiple_crra;const ann=Math.pow(wm,1/3)-1;s+=box(n,X[3],y,W[3],H3,`<text x="${X[3]+8}" y="${y+17}" font-weight="700">${n.path} <tspan class="m">p=${n.p.toFixed(4)}</tspan></text><text x="${X[3]+8}" y="${y+38}">${pct(ann)} a year ${ann>=0.1?'✓ goal':''}</text><text class="m" x="${X[3]+8}" y="${y+58}">equity ${pct(n.factor_return)} · NAV ${bn(n.nav)}</text>`)});
 const svg=document.getElementById('tree');svg.innerHTML=s;svg.setAttribute('viewBox',`0 0 1060 ${Math.max(top+tot+10,760)}`);
 svg.querySelectorAll('.nd').forEach(g=>{const id=+g.dataset.id;const go=()=>{const n=N[id];if(n.stage===1){selT1=id;selT2=null}if(n.stage===2){selT2=id}selNode=id;render();show(id)};g.addEventListener('click',go);g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}})});
}
function wrap(txt,x,y,maxc){const words=txt.split(' · ');let lines=[''];words.forEach(w=>{const cur=lines[lines.length-1];if((cur+' · '+w).length>maxc&&cur){lines.push(w)}else{lines[lines.length-1]=cur?cur+' · '+w:w}});return lines.slice(0,4).map((l,i)=>`<text x="${x}" y="${y+i*15}">${l}</text>`).join('')}
function show(id){const n=N[id];let h=`<h2>${n.stage===0?'Today: the change list':n.path.replaceAll('>',' › ')}</h2><p>${REG[n.regime]} · probability ${n.p.toFixed(4)}${n.stage>0?` · equity factor ${pct(n.factor_return)} · owner draw $${bn(n.owner_draw)}bn`:''}</p>`;
 if(n.stage<3){const a=acts(n);if(!a.length)h+='<p>HOLD everything.</p>';else{h+=`<h3 class="sec">Actions (${plan==='goal'?'goal-seeking':'risk-averse'} plan, $bn)</h3><table>`+a.map(x=>{const l=x.lens.startsWith('ADD (')?'LEVER':x.lens;return `<tr><td><span class="chip ${l}">${l}</span></td><td>${x.h}<br><span style="color:var(--muted)">${D.groups[x.g]||x.g}${x.why?' · '+x.why:''}${x.lens.startsWith('ADD (')?' · add funded by new debt':''}</span></td><td class="v">${bn(x.amt)}</td></tr>`}).join('')+'</table>'}
 h+=`<h3 class="sec">After the decisions ($bn)</h3><table><tr><td>Cash</td><td class="v">${bn(n.cash)}</td></tr><tr><td>Revolver drawn</td><td class="v">${bn(n.revolver)}</td></tr><tr><td>Holding-secured loans (REFINANCE)</td><td class="v">${bn(n.loans)}</td></tr><tr><td>Synthetic equity exposure</td><td class="v">${bn(n.synthetic)}</td></tr><tr><td>NAV</td><td class="v">${bn(n.nav)}</td></tr></table>`}
 else{const wm=plan==='goal'?n.wealth_multiple_goal:n.wealth_multiple_crra;h+=`<p>Outcome: ${pct(Math.pow(wm,1/3)-1)} a year over 3 years (draws accrued). ${Math.pow(wm,1/3)-1>=0.1?'Reaches the goal.':'Misses the goal.'}</p>`}
 document.getElementById('panel').innerHTML=h}
function setPlan(p){plan=p;document.getElementById('pGoal').setAttribute('aria-pressed',p==='goal');document.getElementById('pCrra').setAttribute('aria-pressed',p==='crra');render();show(selNode)}
document.getElementById('pGoal').onclick=()=>setPlan('goal');document.getElementById('pCrra').onclick=()=>setPlan('crra');
const tb=document.getElementById('theme');function setTheme(t){document.documentElement.setAttribute('data-theme',t);tb.textContent=t==='dark'?'Light theme':'Dark theme';try{localStorage.setItem('t2theme',t)}catch(e){}}
let sv=null;try{sv=localStorage.getItem('t2theme')}catch(e){}if(sv)setTheme(sv);
tb.onclick=()=>{const cur=document.documentElement.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');setTheme(cur==='dark'?'light':'dark')};
kpis();abl();fus();render();show(0);
})();
</script></body></html>"""


def main() -> None:
    data = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(PAGE.replace("{{DATA}}", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
