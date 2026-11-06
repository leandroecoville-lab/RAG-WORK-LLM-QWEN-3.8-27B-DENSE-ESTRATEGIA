"""Renderização das novas camadas v4 e dos grafos de uso. Sem rede."""
from collections import Counter
import csv
import html
import json
import re
from pathlib import Path

from strategy_contracts import cases_for_entry, production_coverage

LEVEL_LABELS={'production_documented':'produção documentada','operational_product':'produto/recurso disponível','research_only':'pesquisa; não comprova produção'}
BASIS_LABELS={'engineering_proposal':'proposta de engenharia; não medida neste pacote','source_documented':'combinação descrita em fonte; ver estágio do caso'}
MATCH_LABELS={'exact':'correspondência exata do mecanismo','family':'somente família relacionada','analogy':'analogia; não é adoção deste componente'}
ORG_LABELS={'bigtech':'Big Tech — núcleo definido nesta curadoria','ai_lab':'laboratório de IA — contado separadamente','technology_operator':'outro operador de tecnologia','research_group':'grupo de pesquisa'}
DOMAIN_LABELS={'llm_application':'aplicação com LLM','llm_serving':'infraestrutura de inferência de LLM','llm_training':'treinamento de LLM','llm_framework':'ferramenta/framework para LLM','llm_research':'pesquisa sobre LLM','non_generative_nlp':'NLP não generativo; não é LLM autoregressiva 3–30B','distributed_data_system':'sistema de dados distribuído; transferência para LLM é proposta','infrastructure':'infraestrutura geral; transferência para LLM é proposta','software_analysis_without_llm':'análise/reparo de software sem LLM demonstrada'}


def refs(ids): return ', '.join(ids)


def chunk_sources(entry,number,cases):
    if number<=4: return entry.get('legacy_source_ids',entry['source_ids'])
    if number<=6: return entry['depth']['source_ids']
    if number==8:
        found={sid for case in cases_for_entry(entry['id'],cases) for sid in case['source_ids']}
        return sorted(found or set(entry['strategy']['source_ids']))
    return entry['strategy']['source_ids']


def advanced_sections(entry,cases):
    s=entry['strategy']
    text='NOVA CAMADA v4 — '+s['novelty']+'\n\n'
    for layer in s['deep_layers']:
        text+=layer['name']+'\n'+layer['detail']+'\nNatureza: '+BASIS_LABELS[layer['basis']]+'; fontes: '+refs(layer['source_ids'])+'.\n\n'
    for use in s['advanced_uses']:
        text+='USO AVANÇADO — '+use['name']+'\nCenário: '+use['scenario']+'\nEstratégia: '+use['strategy']+'\nPapel do modelo pequeno: '+use['small_model_role']+'\nAceite proposto: '+use['acceptance']+'\nNatureza: '+BASIS_LABELS[use['basis']]+'; fontes: '+refs(use['source_ids'])+'.\n\n'
    f=s['small_model_fit']
    text+='ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal\n'
    for key,label in [('3_7b','3–7B'),('8_14b','8–14B'),('15_30b','15–30B'),('training_or_runtime_requirements','Requisitos de treino/runtime'),('do_not_use_when','Não aplicar quando')]:
        text+=label+': '+f[key]+'\n'

    coverage=production_coverage(entry['id'],cases)
    production=(f"META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: {coverage['verified_bigtech_production_exact']}. Lacuna: {coverage['missing_to_target']}. "
                f"Laboratórios de IA, contados separadamente: {coverage['verified_ai_lab_production_exact']}; outros operadores com produção exata: {coverage['verified_other_operator_production_exact']}.\n"
                f"Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): {coverage['verified_bigtech_llm_production_exact']}. Os demais podem documentar o mecanismo em infraestrutura sem LLM.\n"
                'A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.\n\n')
    if entry['scope']=='proposta': production+='Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.\n\n'
    selected=cases_for_entry(entry['id'],cases)
    if not selected: production+='Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.\n\n'
    for case in selected:
        m=case['mapping']
        production+=f"{case['case_id']} — {case['company']} / {case['system']}\n"
        production+='Evidência: '+LEVEL_LABELS[case['evidence_level']]+'; '+MATCH_LABELS[m['match']]+'. Organização: '+ORG_LABELS[case['organization_class']]+'.\n'
        if case.get('deployment_domain'): production+='Domínio observado: '+DOMAIN_LABELS.get(case['deployment_domain'],case['deployment_domain'])+'.\n'
        production+='Uso observado: '+case['observed_use']+'\nMecanismo documentado: '+case['technical_mechanism']+'\nCorrespondência com esta base: '+m['rationale']+'\nTransferência proposta para modelo pequeno: '+case['small_model_transfer']+'\n'
        production+='Limite: '+case['limits']+'\nFontes: '+refs(case['source_ids'])+'.\n\n'
    production+='Metadados completos dos casos: production_cases.json desta base.\nPesquisa: '+s['production_search']['scope_note']+'\nConsultas registradas: '+refs(s['production_search']['search_ids'])+'.'
    connections='CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste\n\nConexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.\n\n'
    for n,c in enumerate(s['connections'],1):
        connections+=f"{n}. {entry['id']} → {c['target_id']} [{c['relation']}]\n"
        connections+='Como combinar: '+c['how']+'\nInterface: '+c['interface']+'\nCondição: '+c['condition']+'\nAceite proposto: '+c['acceptance']+'\n'
        connections+='Natureza: '+BASIS_LABELS[c['basis']]+'. Fontes: '+refs(c['source_ids'])+'. Casos: '+(refs(c['case_ids']) or 'nenhum caso operacional comprova esta conexão proposta')+'.\n\n'
    connections+='CONTROLES DE FALHA\n'+'\n'.join('- '+v for v in s['failure_controls'])+'\n\n'
    connections+='COMPARAÇÃO COM FRONTEIRA — protocolo proposto\n'+s['frontier_comparison']+'\n\n'
    connections+='Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.'
    return [('estrategia_3_30b','Novas estratégias e usos avançados; fatos e propostas rotulados individualmente',text.rstrip()),
            ('casos_producao','Evidência de produção, produto e pesquisa com correspondência e lacunas explícitas',production.rstrip()),
            ('conexoes_aceite','Conexões condicionais, contratos, controles e comparação proposta',connections.rstrip())]


def edges_for_entries(entries,cases):
    by_case={c['case_id']:c for c in cases}
    out=[]
    for entry in entries:
        for n,c in enumerate(entry['strategy']['connections'],1):
            levels={by_case[cid]['evidence_level'] for cid in c['case_ids'] if cid in by_case}
            stage='engineering_proposal'
            if c['basis']=='source_documented':
                stage='production_documented' if 'production_documented' in levels else 'operational_product'
            out.append({'edge_id':f"E-{entry['id']}-{n:02}",'from':entry['id'],'to':c['target_id'],**{k:v for k,v in c.items() if k!='target_id'},'evidence_stage':stage})
    return out


def mermaid(entry,entries_by_id,edges):
    eid=entry['id']; selected=[e for e in edges if e['from']==eid]
    def label(e): return (e['id']+' '+e['name']).replace('"',"'").replace('\n',' ')
    lines=['flowchart TD',f'    {eid}["{label(entry)}"]']
    seen={eid}
    for e in selected:
        target=e['to']
        if target not in seen: lines.append(f'    {target}["{label(entries_by_id[target])}"]');seen.add(target)
        stage={'engineering_proposal':'proposta','operational_product':'produto documentado','production_documented':'produção documentada'}[e['evidence_stage']]
        if e['basis']=='engineering_proposal': lines.append(f'    {eid} -. "{e["relation"]}: {stage}" .-> {target}')
        else: lines.append(f'    {eid} -->|"{e["relation"]}: {stage}"| {target}')
    return '\n'.join(lines)+'\n'


def write_strategic_outputs(root,entries,sources,cases,searches,write,write_json,jsonl):
    root=Path(root)
    by_id={e['id']:e for e in entries}
    edges=edges_for_entries(entries,cases)
    coverage=[production_coverage(e['id'],cases) for e in entries]
    for row in coverage:
        row['name']=by_id[row['entry_id']]['name'];row['scope']=by_id[row['entry_id']]['scope']
    case_edges=[{'from':c['case_id'],'canonical_case_id':c.get('canonical_case_id',c['case_id']),'to':m['entry_id'],'relation':'evidence_mapping','evidence_level':c['evidence_level'],'organization_class':c['organization_class'],'deployment_domain':c.get('deployment_domain','unclassified'),'match':m['match'],'rationale':m['rationale'],'source_ids':c['source_ids']} for c in cases for m in c['mappings']]
    graph={'version':'4.0.0','nodes':[{'id':e['id'],'name':e['name'],'scope':e['scope'],'category':e['category']} for e in entries],'edges':edges,'note':'Somente source_documented exprime uma combinação descrita em caso operacional; seu estágio pode ser produto disponível, não implantação comprovada. Propostas têm interface, condição e teste, não ganho medido.'}
    write_json(root/'grafos/conexoes.json',graph)
    write_json(root/'grafos/producao.json',{'case_nodes':[{**{k:c[k] for k in ['case_id','company','system','evidence_level','organization_class']},'canonical_case_id':c.get('canonical_case_id',c['case_id']),'deployment_domain':c.get('deployment_domain','unclassified')} for c in cases],'entry_nodes':graph['nodes'],'edges':case_edges,'note':'Nós preservam os registros de evidência; canonical_case_id identifica a implantação sem duplicar contagem. Aresta de correspondência caso→tema não prova integração entre todos os temas associados ao caso. Ver rationale e o tipo exact/family/analogy.'})
    total={'requested_associations':10*len(entries),'verified_strict_associations':sum(r['verified_bigtech_production_exact'] for r in coverage),'remaining_to_target':sum(r['missing_to_target'] for r in coverage),'entries_target_met':sum(r['target_met'] for r in coverage),'entries_with_strict_production':sum(r['verified_bigtech_production_exact']>0 for r in coverage),'unique_cases':len({c.get('canonical_case_id',c['case_id']) for c in cases}),'case_records':len(cases),'cases_by_evidence_level':dict(Counter(c['evidence_level'] for c in cases)),'cases_by_organization_class':dict(Counter(c['organization_class'] for c in cases)),'strategy_edges':len(edges),'strategy_edges_by_stage':dict(Counter(e['evidence_stage'] for e in edges)),'case_entry_mappings':len(case_edges),'search_queries':len(searches)}
    canonical={c.get('canonical_case_id',c['case_id']):c for c in cases}
    total['unique_cases_by_evidence_level']=dict(Counter(c['evidence_level'] for c in canonical.values()))
    total['verified_strict_llm_associations']=sum(r['verified_bigtech_llm_production_exact'] for r in coverage)
    inventory_rows=[r for r in coverage if r['scope']=='inventario']
    total['requested_inventory_associations']=10*len(inventory_rows)
    total['verified_strict_inventory_associations']=sum(r['verified_bigtech_production_exact'] for r in inventory_rows)
    total['inventory_entries_target_met']=sum(r['target_met'] for r in inventory_rows)
    write_json(root/'producao/COBERTURA_10_POR_BASE.json',{'policy':'Produção documentada + correspondência exata + organização bigtech. Labs de IA e outros operadores permanecem separados. Uma implantação canônica conta uma vez por base.','summary':total,'entries':coverage})
    (root/'producao').mkdir(exist_ok=True)
    columns=['entry_id','name','scope','requested_bigtech_production_examples','verified_bigtech_production_exact','verified_bigtech_llm_production_exact','verified_ai_lab_production_exact','verified_other_operator_production_exact','missing_to_target','unique_cases_associated','operational_product_cases','research_cases','family_or_analogy_cases','target_met']
    with (root/'producao/COBERTURA_10_POR_BASE.csv').open('w',encoding='utf-8-sig',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=columns);writer.writeheader();writer.writerows({k:r[k] for k in columns} for r in coverage)
    for entry,cov in zip(entries,coverage,strict=True):
        base=root/'bases'/entry['id']
        write_json(base/'strategy.json',entry['strategy'])
        write_json(base/'production_cases.json',{'coverage':cov,'cases':cases_for_entry(entry['id'],cases)})
        own=[e for e in edges if e['from']==entry['id']]
        write_json(base/'connections.json',{'entry_id':entry['id'],'edges':own,'note':graph['note']})
        write(base/'graph.mmd',mermaid(entry,by_id,edges))
    write(root/'ABRIR_GRAFO.html',render_graph(entries,sources,cases,edges,coverage,total))
    write(root/'producao/CASOS_COM_FONTES.md',render_case_catalog(cases,sources))
    write(root/'NOVO_NESTA_VERSAO.md',render_delta(entries,cases,total))
    return total


def render_case_catalog(cases,sources):
    out='# Casos públicos e limites de transferência\n\nUm caso pode mapear vários mecanismos; não são implantações independentes. Só produção documentada, correspondência exata e organização do núcleo Big Tech contam na meta estrita. Não há exigência de que todo sistema histórico seja um agente LLM: a transferência para LLM é identificada como proposta.\n\n'
    for c in cases:
        out+=f"## {c['case_id']} — {c['company']} / {c['system']}\n\n"
        out+=f"**Classe:** {LEVEL_LABELS[c['evidence_level']]} · {ORG_LABELS[c['organization_class']]}\n\n"
        if c.get('deployment_domain'):out+='**Domínio observado:** '+DOMAIN_LABELS.get(c['deployment_domain'],c['deployment_domain'])+'.\n\n'
        out+=c['observed_use']+'\n\n**Mecanismo confirmado:** '+c['technical_mechanism']+'\n\n**Transferência proposta:** '+c['small_model_transfer']+'\n\n**Limites:** '+c['limits']+'\n\n'
        if c.get('canonical_case_id',c['case_id'])!=c['case_id']: out+='**Mesmo caso canônico:** '+c['canonical_case_id']+'. Não somado novamente por base.\n\n'
        out+='| Base | Correspondência | Justificativa |\n|---|---|---|\n'
        for m in c['mappings']: out+=f"| {m['entry_id']} | {m['match']} | {m['rationale'].replace('|','/')} |\n"
        out+='\n**Fontes:**\n\n'
        for sid in c['source_ids']: out+=f"- [{sid} — {sources[sid]['title']}]({sources[sid]['url']})\n"
        out+='\n'
    return out


def render_delta(entries,cases,total):
    out='# v4 — conteúdo novo e limite da entrega\n\nA versão anterior permanece preservada nas bases e no histórico. As novas camadas C07, C08 e C09 aprofundam estratégias, casos e conexões. Para ler somente o acréscimo, use este índice e `exports/NOVAS_ESTRATEGIAS.md`; o runtime permite `--layer advanced`, `production` ou `connections`.\n\n'
    out+=f"Meta solicitada: {total['requested_associations']} associações (10 por base). Comprovadas sob o critério estrito: {total['verified_strict_associations']}. Lacunas: {total['remaining_to_target']}. Bases com dez casos estritos: {total['entries_target_met']}/{len(entries)}. Não há preenchimento fictício. Labs de IA e operadores adicionais estão identificados, sem serem reclassificados silenciosamente como Big Tech.\n\n"
    out+='A maior parte das transferências para modelos 3–30B é uma proposta de engenharia. Este pacote não executou esses modelos e não demonstra paridade geral com modelos de fronteira. Sua originalidade foi examinada por comparação textual com v3 e revisão editorial; similaridade baixa não prova novidade científica.\n\n'
    out+='| ID | O que se aprofunda agora |\n|---|---|\n'
    for e in entries: out+=f"| [{e['id']}](bases/{e['id']}/knowledge.md) | {e['strategy']['novelty'].replace('|','/')} |\n"
    return out


def render_graph(entries,sources,cases,edges,coverage,total):
    data={'entries':{e['id']:{'id':e['id'],'name':e['name'],'scope':e['scope'],'category':e['category'],'fit':e['strategy']['small_model_fit'],'novelty':e['strategy']['novelty'],'frontier':e['strategy']['frontier_comparison']} for e in entries},'sources':sources,'cases':cases,'edges':edges,'coverage':{c['entry_id']:c for c in coverage},'total':total,'domain_labels':DOMAIN_LABELS}
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LAI — Grafo estratégico 3–30B</title><style>
:root{--ink:#15283c;--muted:#506377;--paper:#f3f5f6;--line:#cdd6de;--green:#006c56;--orange:#9b5b04;--blue:#245bb2}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,sans-serif}header{padding:28px max(4vw,20px);background:var(--ink);color:white}h1{font-size:30px;margin:0 0 8px}header p{max-width:1000px;color:#d7e2e8;margin:5px 0}.layout{display:grid;grid-template-columns:285px minmax(0,1fr);gap:20px;max-width:1500px;margin:20px auto;padding:0 20px}aside{position:sticky;top:15px;align-self:start;max-height:95vh;display:flex;flex-direction:column;background:white;border:1px solid var(--line);border-radius:9px;padding:15px}input,select,button{font:inherit}input,select{width:100%;padding:10px;border:1px solid #abbac6;border-radius:5px;background:white;color:var(--ink)}label{font-size:12px;font-weight:700;display:block;margin:8px 0 4px}#topics{overflow:auto;margin:12px -5px 0}button{cursor:pointer}#topics button{display:block;width:100%;text-align:left;background:white;border:0;border-bottom:1px solid #edf0f3;padding:9px 7px;color:var(--ink)}#topics button:hover,#topics button[aria-current=true]{background:#e1eeea}#topics small{color:var(--muted);display:block}main{min-width:0}.card{background:white;border:1px solid var(--line);border-radius:9px;padding:20px;margin-bottom:16px}h2{font-size:25px;margin:0 0 7px}h3{font-size:18px;margin:8px 0}.muted{color:var(--muted);font-size:13px}.badge{display:inline-block;font-size:12px;font-weight:700;padding:3px 7px;border-radius:4px;background:#e7edf2;margin:0 6px 5px 0}.prod{color:var(--green)}.product{color:var(--blue)}.proposal{color:var(--orange)}a{color:#155ea5;overflow-wrap:anywhere}.toolbar{display:grid;grid-template-columns:1fr 1fr;gap:15px}.legend{font-size:12px;color:var(--muted)}svg{width:100%;height:auto;display:block}.node{fill:#eef4f5;stroke:#91a8b7;stroke-width:1.4}.current{fill:#d4e9df;stroke:#006c56}.svg-label{font:12px system-ui;fill:#15283c}.svg-id{font:bold 13px system-ui;fill:#15283c}.edge-line{stroke-width:2;fill:none}.edge-hit{stroke:transparent;stroke-width:16;fill:none;cursor:pointer}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--line);vertical-align:top}th{width:145px}details{border-top:1px solid var(--line);padding:12px 0}summary{cursor:pointer;font-weight:650}#edge-details:empty{display:none}code{font-size:12px}.empty{padding:15px;background:#f5f1e9}.count{font-variant-numeric:tabular-nums}footer{max-width:1100px;margin:20px auto 40px;padding:0 20px;color:var(--muted);font-size:12px}@media(max-width:900px){.layout{grid-template-columns:1fr}aside{position:static;max-height:280px}.toolbar{grid-template-columns:1fr}h1{font-size:25px}}
</style></head><body><header><h1>Conexões estratégicas para LLMs de 3–30B</h1><p>287 bases. Cada conexão informa como combinar, qual artefato passar, em que condição e como testar. Casos reais, recursos disponíveis e propostas têm rótulos próprios.</p><p id="global-count" class="legend"></p></header><div class="layout"><aside><label for="search">LOCALIZAR BASE</label><input id="search" type="search" placeholder="ID ou assunto…"><p id="topic-count" class="muted"></p><div id="topics"></div></aside><main><section class="card"><h2 id="title"></h2><p id="novelty"></p><div id="coverage"></div><p id="base-link"></p><div class="toolbar"><div><label for="edge-filter">CONEXÕES A EXIBIR</label><select id="edge-filter"><option value="all">Todas, com classificação</option><option value="documented">Somente descritas em fonte operacional</option><option value="production_documented">Somente produção documentada</option><option value="engineering_proposal">Somente propostas de engenharia</option></select></div><div><label for="size">ORIENTAÇÃO POR PORTE</label><select id="size"><option value="3_7b">3–7B parâmetros totais</option><option value="8_14b">8–14B parâmetros totais</option><option value="15_30b">15–30B parâmetros totais</option></select></div></div><p id="fit"></p><p class="legend">Linha verde: produção descrita. Azul: combinação documentada em produto disponível. Tracejada âmbar: proposta. Clique em uma conexão para abrir seu contrato; clique em um nó para mudar de assunto.</p><div id="graph"></div></section><section id="edge-details" class="card"></section><section class="card"><h3>Casos e correspondência individual</h3><p class="muted">A presença de dois temas no mesmo caso não prova integração entre eles. O grafo de conexões exige evidência adicional ou classifica a combinação como proposta. Sistemas históricos de dados podem fornecer analogias de engenharia sem usarem LLM.</p><label for="case-filter">EVIDÊNCIA</label><select id="case-filter"><option value="all">Todos os níveis e correspondências</option><option value="strict">Produção Big Tech + mecanismo exato</option><option value="production_documented">Produção documentada, qualquer organização</option><option value="operational_product">Produto/recurso disponível</option><option value="research_only">Pesquisa</option></select><div id="cases"></div></section><section class="card"><h3>Como comparar com fronteira</h3><p id="frontier"></p><p class="muted">Protocolo proposto. O pacote não mediu LLMs, GPU, custo de serviço ou equivalência com fronteira. Porte não substitui avaliação de arquitetura, treino, idiomas e hardware. O arquivo GUIA_ESTRATEGICO_3_30B.md contém a metodologia global.</p></section></main></div><footer>Funciona localmente; não chama APIs, não envia consultas e não exige CDN. Links de fontes abrem páginas externas somente quando clicados. <a href="ABRIR_CATALOGO.html">Catálogo completo</a> · <a href="producao/COBERTURA_10_POR_BASE.csv">Cobertura por base</a> · <a href="grafos/conexoes.json">Grafo em JSON</a></footer>
<script id="graph-data" type="application/json">__DATA__</script><script>
'use strict';
const D=JSON.parse(document.getElementById('graph-data').textContent),$=id=>document.getElementById(id),norm=s=>s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
const stage={production_documented:'Produção documentada',operational_product:'Produto disponível',engineering_proposal:'Proposta de engenharia',research_only:'Pesquisa'},matches={exact:'Mecanismo exato',family:'Família relacionada',analogy:'Analogia'};
let selected=D.entries[location.hash.slice(1)]?location.hash.slice(1):(D.entries.T009?'T009':Object.keys(D.entries)[0]);
function el(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function link(label,url){const a=el('a',label);a.href=url;if(/^https?:/.test(url)){a.target='_blank';a.rel='noopener noreferrer';}return a;}
function addSources(node,ids){const p=el('p');p.append(el('strong','Fontes: '));for(const sid of ids){const s=D.sources[sid];if(s){p.append(link(sid+' — '+s.title,s.url));p.append(document.createTextNode(' · '));}}node.append(p);}
function badge(text,cls){return el('span',text,'badge '+(cls||''));}
function topics(){const q=norm($('search').value);$('topics').replaceChildren();let n=0;for(const e of Object.values(D.entries)){if(!norm(e.id+' '+e.name).includes(q))continue;const b=el('button',e.id+' · '+e.name);b.setAttribute('aria-current',String(e.id===selected));b.append(el('small',e.scope));b.addEventListener('click',()=>select(e.id));$('topics').append(b);n++;}$('topic-count').textContent=n+' bases encontradas';}
function select(id){selected=id;history.replaceState(null,'','#'+id);topics();render();}
function detail(edge){const target=$('edge-details');target.replaceChildren(el('h3',edge.from+' → '+edge.to+' · '+edge.relation),badge(stage[edge.evidence_stage]));const table=el('table');for(const [title,key] of [['Como combinar','how'],['Interface','interface'],['Condição','condition'],['Aceite proposto','acceptance']]){const tr=el('tr');tr.append(el('th',title),el('td',edge[key]));table.append(tr);}target.append(table,el('p','A classificação documenta a combinação. Interface, condições e aceite orientam sua adaptação; não são uma API oficial nem resultado medido.','muted'));if(edge.case_ids.length)target.append(el('p','Casos que sustentam a combinação: '+edge.case_ids.join(', ')));addSources(target,edge.source_ids);}
function draw(){const filter=$('edge-filter').value;const edges=D.edges.filter(e=>e.from===selected&&(filter==='all'||(filter==='documented'&&e.basis==='source_documented')||e.evidence_stage===filter));const holder=$('graph');holder.replaceChildren();$('edge-details').replaceChildren();if(!edges.length){holder.append(el('p','Nenhuma conexão corresponde a este filtro. Isso não comprova inexistência; as propostas e lacunas continuam identificadas na ficha.','empty'));return;}const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');const h=Math.max(210,edges.length*110+25);svg.setAttribute('viewBox','0 0 900 '+h);svg.setAttribute('role','img');svg.setAttribute('aria-label','Conexões de '+selected);const make=(tag,attrs)=>{const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,String(v));svg.append(n);return n;};function node(id,x,y,current){const g=make('g',{tabindex:0,role:'button','aria-label':D.entries[id].name});const rect=document.createElementNS(ns,'rect');for(const[k,v]of Object.entries({x,y,width:280,height:65,rx:7,class:'node'+(current?' current':'')}))rect.setAttribute(k,v);g.append(rect);const t=document.createElementNS(ns,'text');t.setAttribute('x',x+12);t.setAttribute('y',y+23);t.setAttribute('class','svg-id');t.textContent=id;g.append(t);const text=document.createElementNS(ns,'text');text.setAttribute('x',x+12);text.setAttribute('y',y+46);text.setAttribute('class','svg-label');const name=D.entries[id].name;text.textContent=name.length>37?name.slice(0,35)+'…':name;g.append(text);const title=document.createElementNS(ns,'title');title.textContent=name;g.append(title);g.addEventListener('click',()=>select(id));g.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' ')select(id);});}const cy=h/2-33;for(let i=0;i<edges.length;i++){const e=edges[i],ty=25+i*110;const color=e.evidence_stage==='production_documented'?'#006c56':e.evidence_stage==='operational_product'?'#245bb2':'#9b5b04';const path='M 295 '+(cy+32)+' C 440 '+(cy+32)+', 435 '+(ty+32)+', 600 '+(ty+32);make('path',{d:path,class:'edge-line',stroke:color,'stroke-dasharray':e.basis==='engineering_proposal'?'7 5':'none'});const hit=make('path',{d:path,class:'edge-hit',tabindex:0,role:'button','aria-label':e.from+' '+e.relation+' '+e.to});hit.addEventListener('click',()=>detail(e));hit.addEventListener('keydown',ev=>{if(ev.key==='Enter')detail(e);});const label=make('text',{x:440,y:ty+20,class:'svg-label'});label.textContent=e.relation;node(e.to,600,ty,false);}node(selected,15,cy,true);holder.append(svg);const list=el('p');for(const e of edges){const b=el('button',e.to+' · '+e.relation);b.style.margin='4px';b.addEventListener('click',()=>detail(e));list.append(b);}holder.append(list);detail(edges[0]);}
function showCases(){const filter=$('case-filter').value;const chosen=new Map(),rank={exact:0,family:1,analogy:2};for(const c of D.cases){const m=c.mappings.find(m=>m.entry_id===selected);if(!m)continue;const key=c.canonical_case_id||c.case_id,old=chosen.get(key);if(!old||rank[m.match]<rank[old.mappings.find(m=>m.entry_id===selected).match]||(rank[m.match]===rank[old.mappings.find(m=>m.entry_id===selected).match]&&c.case_id<old.case_id))chosen.set(key,c);}const all=[...chosen.values()];const seen=new Set(),rows=[];for(const c of all){const m=c.mappings.find(x=>x.entry_id===selected);if(filter==='strict'&&!(c.evidence_level==='production_documented'&&m.match==='exact'&&c.organization_class==='bigtech'))continue;if(!['all','strict'].includes(filter)&&c.evidence_level!==filter)continue;const key=c.canonical_case_id||c.case_id;if(seen.has(key))continue;seen.add(key);rows.push([c,m]);}const holder=$('cases');holder.replaceChildren(el('p',rows.length+' casos únicos neste filtro.','muted'));if(!rows.length)holder.append(el('p','Nenhum caso comprovado nesta combinação de base e filtro.','empty'));for(const[c,m]of rows){const d=el('details');d.append(el('summary',c.case_id+' · '+c.company+' / '+c.system));d.append(badge(stage[c.evidence_level]),badge(matches[m.match]),badge(c.organization_class));if(c.deployment_domain)d.append(el('p','Domínio observado: '+(D.domain_labels[c.deployment_domain]||c.deployment_domain),'muted'));for(const[label,text]of [['Uso observado',c.observed_use],['Mecanismo',c.technical_mechanism],['Correspondência com esta base',m.rationale],['Transferência proposta',c.small_model_transfer],['Limites',c.limits]]){const p=el('p');p.append(el('strong',label+': '),document.createTextNode(text));d.append(p);}addSources(d,c.source_ids);holder.append(d);}}
function fit(){const e=D.entries[selected];$('fit').textContent=e.fit[$('size').value]+' Requisitos: '+e.fit.training_or_runtime_requirements;}
function render(){const e=D.entries[selected],c=D.coverage[selected];$('title').textContent=e.id+' · '+e.name;$('novelty').textContent=e.novelty;$('coverage').replaceChildren(badge(c.verified_bigtech_production_exact+'/10 produção Big Tech exata','prod'),badge('Lacuna: '+c.missing_to_target),badge(c.verified_bigtech_llm_production_exact+' dos casos estritos aplicados a LLMs'),badge(c.verified_ai_lab_production_exact+' casos exatos em labs de IA'),badge(c.verified_other_operator_production_exact+' em outros operadores'));$('base-link').replaceChildren(link('Abrir a base completa','bases/'+selected+'/knowledge.md'));$('frontier').textContent=e.frontier;fit();draw();showCases();}
$('global-count').textContent=D.total.strategy_edges+' conexões condicionais · '+D.total.unique_cases+' casos únicos · '+D.total.verified_strict_associations+'/'+D.total.requested_associations+' associações estritas comprovadas. Lacunas são preservadas.';
$('search').addEventListener('input',topics);$('edge-filter').addEventListener('change',draw);$('case-filter').addEventListener('change',showCases);$('size').addEventListener('change',fit);window.addEventListener('hashchange',()=>{if(D.entries[location.hash.slice(1)]){selected=location.hash.slice(1);topics();render();}});topics();render();
</script></body></html>'''
    return template.replace('__DATA__',payload)
