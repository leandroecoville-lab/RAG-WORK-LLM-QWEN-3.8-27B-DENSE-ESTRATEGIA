/* Exercita lógica e eventos em DOM mínimo simulado. Não renderiza um navegador. */
'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),file=path.join(root,'ABRIR_GRAFO.html'),html=fs.readFileSync(file,'utf8');
const data=html.match(/<script id="graph-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code=[...html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)].filter(m=>!m[0].includes('type="application/json"')).map(m=>m[1]).join('\n');
class Node {
 constructor(tag){this.tagName=tag;this.children=[];this.attrs={};this.events={};this.style={};this._text='';this.value='';}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(c=>typeof c==='string'?c:c.textContent).join('');}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this._text='';this.children=[...nodes];}
 setAttribute(k,v){this.attrs[k]=String(v);}
 addEventListener(k,fn){(this.events[k]??=[]).push(fn);}
 fire(k){for(const fn of this.events[k]||[])fn({target:this,key:'Enter'});}
}
const nodes=new Map();
for(const m of html.matchAll(/<([a-z0-9]+)[^>]*\bid="([^"]+)"[^>]*>/g))nodes.set(m[2],new Node(m[1]));
nodes.get('graph-data').textContent=data;
for(const[id,value]of [['edge-filter','all'],['size','3_7b'],['case-filter','all']])nodes.get(id).value=value;
const location={hash:''};
const context={document:{getElementById:id=>nodes.get(id),createElement:t=>new Node(t),createElementNS:(_,t)=>new Node(t),createTextNode:t=>{const n=new Node('#text');n.textContent=t;return n;}},location,history:{replaceState:(_,__,hash)=>{location.hash=hash;}},window:{addEventListener(){}},console,fetch:()=>{throw Error('Rede não permitida');}};
vm.runInNewContext(code,context,{filename:file,timeout:10000});
const D=JSON.parse(data),checks=[];
function verify(name,condition){assert(condition,name);checks.push(name);}
verify('all_topics_are_present',nodes.get('topics').children.length===Object.keys(D.entries).length);
verify('initial_topic_and_contract_render',nodes.get('title').textContent.startsWith('T009')&&nodes.get('edge-details').textContent.includes('Interface'));
nodes.get('search').value='T079';nodes.get('search').fire('input');
verify('topic_search_filters',nodes.get('topics').children.length===1);
nodes.get('topics').children[0].fire('click');
verify('selection_updates_title',nodes.get('title').textContent.startsWith('T079'));
nodes.get('size').value='15_30b';nodes.get('size').fire('change');
verify('size_band_changes_guidance',nodes.get('fit').textContent.includes(D.entries.T079.fit['15_30b']));
nodes.get('case-filter').value='strict';nodes.get('case-filter').fire('change');
const shown=nodes.get('cases').children.filter(c=>c.tagName==='details').length;
verify('strict_cases_equal_coverage',shown===D.coverage.T079.verified_bigtech_production_exact);
nodes.get('edge-filter').value='production_documented';nodes.get('edge-filter').fire('change');
const expected=D.edges.filter(e=>e.from==='T079'&&e.evidence_stage==='production_documented').length;
verify('edge_filter_handles_empty_or_matching_graph',expected?nodes.get('graph').children.some(c=>c.tagName==='svg'):nodes.get('graph').textContent.includes('Nenhuma conexão'));
const report={passed:true,checks,html_sha256:crypto.createHash('sha256').update(html).digest('hex'),runtime:process.version,mode:'minimal_simulated_DOM',visual_browser_rendering_tested:false,external_calls:0,limits:'Exercita execução JavaScript, seleção, filtros e contratos em DOM simulado; não verifica layout, acessibilidade completa ou comportamento de navegador real.'};
fs.mkdirSync(path.join(root,'evidencias'),{recursive:true});fs.writeFileSync(path.join(root,'evidencias','grafo_dom_simulado.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
