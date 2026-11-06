"""Validação reproduzível da edição v4. Sem chamadas reais a modelos."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html.parser
import io
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
import rag
from strategic import edges_for_entries
from strategy_contracts import production_coverage


def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def aggregate(report):
    return {'cases':report['semantic_cases'],'hits_at_5':sum(c['hit_at_5'] for c in report['cases']),'hit_at_5':report['semantic_hit_at_5'],'mrr_at_10':report['semantic_mrr_at_10'],'names_hit_at_3':report['name_lookup_hit_at_3'],'failed_queries':[c['case_id'] for c in report['cases'] if not c['hit_at_5']]}


class HTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.scripts=[];self.data=[];self.current=None;self.remote=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='details':self.ids.append(attrs.get('id'))
        if tag=='script':
            self.current='data' if attrs.get('type')=='application/json' else 'script'
            if attrs.get('src'):self.remote.append(attrs['src'])
    def handle_endtag(self,tag):
        if tag=='script':self.current=None
    def handle_data(self,data):
        if self.current=='data':self.data.append(data)
        elif self.current=='script':self.scripts.append(data)


def validate_html(entries,stats):
    reports={};node=shutil.which('node') or os.getenv('CODEX_PRIMARY_RUNTIME_NODE')
    for name in ['ABRIR_CATALOGO.html','ABRIR_GRAFO.html']:
        parser=HTMLParser();parser.feed((ROOT/name).read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as temp:
            js=Path(temp)/'app.js';js.write_text('\n'.join(parser.scripts),encoding='utf-8')
            result=subprocess.run([node,'--check',str(js)],capture_output=True,text=True) if node else None
        report={'html_sha256':rag.sha256(ROOT/name),'remote_scripts':parser.remote,'javascript_syntax_checked':result is not None,'javascript_syntax_valid':result.returncode==0 if result else None}
        if name=='ABRIR_CATALOGO.html':
            report['entries_complete']=len(parser.ids)==len(set(parser.ids))==len(entries) and set(parser.ids)==set(entries)
        else:
            data=json.loads(''.join(parser.data))
            report['entries_complete']=set(data['entries'])==set(entries)
            report['edges_complete']=len(data['edges'])==stats['strategy_edges']
            report['case_records_complete']=len(data['cases'])==stats['case_records']
        report['passed']=not parser.remote and report['entries_complete'] and report['javascript_syntax_valid'] is not False and report.get('edges_complete',True) and report.get('case_records_complete',True)
        reports[name]=report
    dom=None
    if node:
        run=subprocess.run([node,str(ROOT/'tests/check_graph_dom.js')],capture_output=True,text=True)
        dom={'passed':run.returncode==0,'exit_code':run.returncode,'mode':'minimal_simulated_DOM','visual_browser_rendering_tested':False}
        if run.returncode:dom['error']=run.stderr[-4000:]
    return {'passed':all(r['passed'] for r in reports.values()) and (dom is None or dom['passed']),'files':reports,'dom_smoke':dom,'note':'Estrutura, sintaxe e lógica em DOM simulado quando Node está disponível; não é renderização visual de navegador.'}


def prose(value,key=''):
    if key in {'source_ids','case_ids','search_ids','id','target_id','basis','relation'}:return []
    if isinstance(value,str):return [value]
    if isinstance(value,dict):return [x for k,v in value.items() for x in prose(v,k)]
    if isinstance(value,list):return [x for v in value for x in prose(v,key)]
    return []


def novelty(entries,old):
    records=[];sentences=Counter()
    for eid,e in entries.items():
        a=re.findall(r'\w+',' '.join(prose(old[eid])).casefold());b=re.findall(r'\w+',' '.join(prose(e['strategy'])).casefold())
        grams_a={tuple(a[i:i+12]) for i in range(max(0,len(a)-11))}
        grams_b=[tuple(b[i:i+12]) for i in range(max(0,len(b)-11))]
        repeated=sum(g in grams_a for g in grams_b)
        ratio=repeated/len(grams_b) if grams_b else 1
        records.append({'entry_id':eid,'new_strategy_words':len(b),'twelve_word_sequences_seen_in_v3':repeated,'sequence_overlap_fraction':ratio,'flag_for_editorial_review':ratio>.25})
        local=set()
        for field in prose(e['strategy']):
            for sentence in re.split(r'(?<=[.!?])\s+',field):
                if len(sentence.split())>=14:local.add(sentence)
        sentences.update(local)
    return {'method':'Comparação textual de sequências de 12 palavras por base e repetição exata de frases longas entre fichas. Não comprova novidade científica, correção factual ou ausência de paráfrase repetitiva.','entries':records,'strategy_words_total':sum(r['new_strategy_words'] for r in records),'entries_flagged':sum(r['flag_for_editorial_review'] for r in records),'repeated_long_sentences':[{'entries':n,'sentence':s} for s,n in sentences.most_common(20) if n>=8]}


def main():
    out=ROOT/'evidencias';out.mkdir(exist_ok=True)
    started=time.perf_counter()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    (out/'testes_runtime.log').write_text(log.getvalue(),encoding='utf-8')
    tests={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'passed':result.wasSuccessful(),'duration_seconds':round(time.perf_counter()-started,3),'external_model_calls':0,'external_embedding_calls':0,'note':'Recuperação local real; clientes externos e dados do comparador simulados nos testes.'}
    write(out/'testes_runtime.json',tests)
    structural=rag.validate_corpus(ROOT);write(out/'integridade_corpus.json',structural)
    if not tests['passed'] or not structural['passed']:
        print(json.dumps({'passed':False,'tests':tests,'structural':structural},ensure_ascii=False,indent=2));return 1
    engine=rag.Engine(ROOT);entries=engine.entries
    old={e['id']:e for e in rag.read_jsonl(ROOT/'historico/entries_v3.jsonl')}
    old_hashes=json.loads((ROOT/'historico/chunks_v3_text_hashes.json').read_text())
    current={c['chunk_id']:c for c in engine.chunks}
    expected_files={'knowledge.md','metadata.json','chunks.jsonl','sources.json','qa.json','research.json','strategy.json','production_cases.json','connections.json','graph.mmd'}
    migration={'entry_ids_preserved':set(entries)==set(old),'scope_counts':dict(Counter(e['scope'] for e in entries.values())),'all_legacy_fields_preserved':all(all(entries[eid].get(k)==v for k,v in item.items() if k!='source_ids') for eid,item in old.items()),'all_legacy_sources_preserved':all(set(item['source_ids'])<=set(entries[eid]['source_ids']) for eid,item in old.items()),'legacy_chunk_texts_preserved':all(cid in current and hashlib.sha256(current[cid]['text'].encode()).hexdigest()==h for cid,h in old_hashes.items()),'legacy_chunk_count':len(old_hashes),'base_count':len(list((ROOT/'bases').iterdir())),'individual_files_complete':all({p.name for p in (ROOT/'bases'/eid).iterdir()}==expected_files for eid in entries),'new_strategy_count':sum(bool(e.get('strategy')) for e in entries.values()),'qa_count':sum(len(e['qa']) for e in entries.values())}
    migration['passed']=all(migration[k] for k in ['entry_ids_preserved','all_legacy_fields_preserved','all_legacy_sources_preserved','legacy_chunk_texts_preserved','individual_files_complete']) and migration['base_count']==migration['new_strategy_count']==287 and migration['qa_count']==1148 and migration['scope_counts']=={'inventario':243,'referencia':27,'proposta':17}
    write(out/'cobertura_migracao.json',migration)
    cases=rag.read_jsonl(ROOT/'producao/casos.jsonl')
    graph=json.loads((ROOT/'grafos/conexoes.json').read_text())
    coverage=json.loads((ROOT/'producao/COBERTURA_10_POR_BASE.json').read_text())
    graph_check={'edges_identical_to_strategies':graph['edges']==edges_for_entries(list(entries.values()),cases),'all_coverage_recomputed':all(all(row[k]==v for k,v in production_coverage(row['entry_id'],cases).items()) for row in coverage['entries']),'proposal_cases_are_analogies':all(m['match']=='analogy' for c in cases for m in c['mappings'] if m['entry_id'].startswith('P'))}
    graph_check['passed']=all(graph_check.values());write(out/'grafos_e_contagens.json',graph_check)
    provenance=json.loads((ROOT/'pesquisa/PROVENIENCIA_V4.json').read_text())
    frozen=[]
    for group,receipt in provenance['groups'].items():
        directory=ROOT/'pesquisa/lotes_congelados'/group
        frozen.append(rag.sha256(directory/f'READY_{group}.json')==receipt['ready_sha256'])
        frozen.extend(rag.sha256(directory/name)==item['sha256'] for name,item in receipt['files'].items())
    if provenance.get('supplemental_sources_sha256'):
        frozen.append(rag.sha256(ROOT/'pesquisa/FONTES_SUPLEMENTARES_REVISAO.jsonl')==provenance['supplemental_sources_sha256'])
    if provenance.get('supplemental_searches_sha256'):
        frozen.append(rag.sha256(ROOT/'pesquisa/CONSULTAS_SUPLEMENTARES_REVISAO.jsonl')==provenance['supplemental_searches_sha256'])
    graph_check['frozen_research_batches_preserved']=bool(frozen) and all(frozen)
    review=json.loads((ROOT/'pesquisa/REVISAO_FACTUAL_V4.json').read_text())
    graph_check['editorial_review_resolutions_recorded']=review['all_required_findings_resolved'] and set(review['reviewed_case_ids'])=={c['case_id'] for c in cases}
    graph_check['audit_reports_intact']=all(rag.sha256(ROOT/'pesquisa/revisoes'/name)==h for name,h in review['audit_files'].items())
    graph_check['passed']=all(v for k,v in graph_check.items() if k!='passed')
    write(out/'grafos_e_contagens.json',graph_check)
    novelty_report=novelty(entries,old);write(out/'novidade_v3_v4.json',novelty_report)
    stats=json.loads((ROOT/'catalogo/estatisticas.json').read_text())
    html_report=validate_html(entries,stats);write(out/'html_estrutura_sintaxe.json',html_report)
    clean_env={k:v for k,v in os.environ.items() if not k.startswith('RAG_')};clean_env['PYTHONDONTWRITEBYTECODE']='1'
    checks=[('ID',['search','T243','--id','T243'],0),('new_layer',['context','T009','--id','T009','--layer','advanced'],0),('scope_conflict',['search','T243','--id','T243','--scope','proposta'],0),('no_server',['ask','T243'],2),('graph',['graph','T140'],0),('strict_cases',['cases','T079','--production-only','--bigtech-only','--exact-only'],0)]
    smoke=[]
    for name,args,code in checks:
        p=subprocess.run([sys.executable,'-B',str(ROOT/'runtime/rag.py'),*args],env=clean_env,capture_output=True,text=True)
        payload=json.loads(p.stdout or p.stderr);passed=p.returncode==code
        if name=='ID':passed &= bool(payload['results']) and all(c['entry_id']=='T243' for c in payload['results'])
        elif name=='new_layer':passed &= payload['selected_chunks']==['T009:C07']
        elif name=='scope_conflict':passed &= payload['results']==[]
        elif name=='no_server':passed &= 'Configure' in payload.get('error','')
        elif name=='graph':passed &= bool(payload['edges']) and all(e['from']=='T140' for e in payload['edges'])
        elif name=='strict_cases':passed &= all(c['evidence_level']=='production_documented' and c['organization_class']=='bigtech' and c['mapping']['match']=='exact' for c in payload['cases'])
        smoke.append({'name':name,'args':args,'exit_code':p.returncode,'passed':passed})
    write(out/'cli_smoke.json',{'passed':all(x['passed'] for x in smoke),'cases':smoke,'external_calls':0})
    if not (migration['passed'] and graph_check['passed'] and html_report['passed'] and all(x['passed'] for x in smoke)):
        print(json.dumps({'passed':False,'migration':migration,'graph':graph_check,'html':html_report,'smoke':smoke},ensure_ascii=False,indent=2));return 1
    evaluations={}
    for name,path,profile in [('historicas90_expandido',ROOT/'tests/semantic_queries.jsonl','expanded'),('historicas90_exato',ROOT/'tests/semantic_queries.jsonl','exact'),('reserva_v3_conhecida40_expandido',ROOT/'tests/reserved_queries_v3.jsonl','expanded'),('reserva_v3_conhecida40_exato',ROOT/'tests/reserved_queries_v3.jsonl','exact')]:
        evaluations[name]=rag.evaluate(engine,path,profile);write(out/(name+'.json'),evaluations[name])
    summary={name:aggregate(r) for name,r in evaluations.items()}
    write(out/'resumo_avaliacoes.json',{'classification':'regressao_conhecida; nao nova reserva cega','results':summary})
    code_names=['rag.py','build_corpus.py','contracts.py','strategy_contracts.py','strategic.py','compare_systems.py','validate_release.py','package_release.py']
    freeze={'evaluated_at':datetime.now(timezone.utc).isoformat(),'code_hashes':{n:rag.sha256(ROOT/'runtime'/n) for n in code_names},'corpus_sha256':engine.corpus_hash,'entries_sha256':rag.sha256(ROOT/'corpus/entries.jsonl'),'cases_sha256':rag.sha256(ROOT/'producao/casos.jsonl'),'sources_sha256':rag.sha256(ROOT/'fontes/sources.jsonl'),'known_queries_sha256':{n:rag.sha256(ROOT/'tests'/n) for n in ['semantic_queries.jsonl','reserved_queries_v3.jsonl']},'default_lexical_profile':'expanded','retrieval_parameters':{k:engine.index[k] for k in ['k1','b','variant_similarity','variant_weight','entry_weight']}}
    freeze['derived_hashes']={name:rag.sha256(ROOT/name) for name in ['grafos/conexoes.json','grafos/producao.json','producao/COBERTURA_10_POR_BASE.json','catalogo/estatisticas.json','ABRIR_CATALOGO.html','ABRIR_GRAFO.html','pesquisa/CONSULTAS_V4.jsonl']}
    freeze['derived_hashes']['pesquisa/REVISAO_FACTUAL_V4.json']=rag.sha256(ROOT/'pesquisa/REVISAO_FACTUAL_V4.json')
    freeze['test_hashes']={p.name:rag.sha256(p) for p in sorted((ROOT/'tests').glob('*')) if p.is_file() and p.suffix in {'.py','.js'}}
    write(out/'configuracao_avaliada.json',freeze)
    previous=json.loads((ROOT/'catalogo/migracao_v3_v4.json').read_text())
    manifest={'package':'LAI_RAG_243_COMPLETO_v4','version':rag.VERSION,'language':'pt-BR','curation_date':'2026-11-05','validated_at':freeze['evaluated_at'],'python':platform.python_version(),'platform':platform.platform(),'stats':stats,'corpus_sha256':engine.corpus_hash,'previous_package_sha256':previous['previous_package_sha256'],'verification':{'required_gates_passed':True,'unit_tests':tests,'structural':True,'migration':migration['passed'],'graph_counts':graph_check['passed'],'html':html_report['passed'],'evaluations':summary},'runtime':{'default_retrieval':'BM25 com variantes lexicais e pontuação por entrada','default_profile':'expanded','baseline_profile':'exact','optional_retrieval':['cosine','RRF'],'layers':list(rag.LAYERS),'generated_embeddings_included':False,'generation_client':'chat/completions; endpoint/modelo explícitos'},'not_executed':['inferencia_real_de_LLM','embeddings_reais','instalacao_na_Helena','benchmarks_de_GPU','experimentos_individuais_das_243_entradas','implementacao_dos_17_componentes_propostos','comparacao_real_com_modelo_de_fronteira'],'not_claimed':['dez_casos_comprovados_para_cada_base','maior_acervo_mundial','paridade_geral_com_fronteira','ausencia_absoluta_de_erros']}
    write(ROOT/'manifest.json',manifest)
    report(ROOT,stats,tests,summary,evaluations,freeze,novelty_report)
    print(json.dumps({'passed':True,'tests':tests,'migration':migration,'stats':stats,'evaluations':summary},ensure_ascii=False,indent=2));return 0


def report(root,stats,tests,summary,evaluations,freeze,novelty_report):
    text=f"""# Validação — LAI RAG estratégico v4

## Entrega comprovada

- 287 bases: 243 entradas do inventário, 27 referências e 17 propostas.
- {stats['chunks']} chunks, {stats['qa']} perguntas de estudo, {stats['strategic_entries']} estratégias individuais.
- {stats['advanced_uses']} usos avançados; {stats['strategy_edges']} conexões com contrato; {stats['case_entry_mappings']} mapeamentos caso→base.
- {stats['unique_cases']} casos canônicos em {stats['case_records']} registros, {stats['search_queries']} consultas de pesquisa registradas.
- {stats['source_records']} registros de fontes e {stats['unique_source_urls']} URLs distintas.
- {tests['tests_run']} testes executados, {tests['failures']} falhas e {tests['errors']} erros. Nenhuma chamada real a modelos ou embeddings.
- IDs e campos anteriores preservados; textos C01–C06 conferidos contra hashes v3. Três camadas novas por base.
- Cada base possui dez arquivos, incluindo JSONs de estratégia/casos/conexões e Mermaid.

## Meta de dez exemplos reais por base

Solicitado: **{stats['requested_associations']} associações**. Comprovado no critério estrito de produção Big Tech + mecanismo exato: **{stats['verified_strict_associations']}**. Lacuna somada por base: **{stats['remaining_to_target']}**. Bases que atingiram dez: **{stats['entries_target_met']}/287**; bases com ao menos um caso estrito: **{stats['entries_with_strict_production']}**.

Não se preencheu a meta com exemplos inventados. Labs de IA e outros operadores são contados separadamente. Produtos, pesquisas e analogias não são reclassificados como implantação. Casos que mapeiam vários temas continuam sendo uma implantação canônica, não várias. A tabela completa está em `producao/COBERTURA_10_POR_BASE.csv`.

Casos canônicos por nível: {json.dumps(stats['unique_cases_by_evidence_level'],ensure_ascii=False)}. Registros antes da deduplicação: {json.dumps(stats['cases_by_evidence_level'],ensure_ascii=False)}.

Das associações estritas de mecanismos, {stats['verified_strict_llm_associations']} são de aplicações, serving ou treino de LLMs. As restantes podem comprovar mecanismos de infraestrutura geral; isso não comprova uso em LLM pequena.

Conexões por estágio: {json.dumps(stats['strategy_edges_by_stage'],ensure_ascii=False)}.

## Regressão de recuperação executada

| Conjunto/perfil | Consultas | Acertos @5 | Hit@5 | MRR@10 | Nomes Hit@3 |
|---|---:|---:|---:|---:|---:|
"""
    for name,v in summary.items():text+=f"| {name} | {v['cases']} | {v['hits_at_5']} | {v['hit_at_5']:.1%} | {v['mrr_at_10']:.4f} | {v['names_hit_at_3']:.1%} |\n"
    text+='\nAs 130 consultas são conhecidas das versões anteriores. Esta é regressão local, não nova reserva cega, benchmark externo ou prova de qualidade de resposta de LLM. Os parâmetros da v3 foram mantidos. Alterar o corpus pode mudar os rankings; a comparação não identifica automaticamente qual componente causou a mudança. Hit@5 aceita algum ID esperado, não todos.\n\n'
    text+='## Integridade, novidade e grafos\n\n'
    text+=f"A validação verifica identidade, campos, fontes, consultas, casos, classes, contagem canônica e coerência dos grafos. Conexão documentada exige caso operacional com origem/alvo exatos e fonte em comum. Isso é uma restrição estrutural e não substitui leitura factual.\n\nO diagnóstico de novidade encontrou {novelty_report['entries_flagged']} bases acima do limiar de revisão textual de 25% de sequências de 12 palavras presentes na própria v3. O limiar é uma heurística editorial, não certificado de novidade ou ausência de redundância. Foram contadas {novelty_report['strategy_words_total']:,} palavras nos campos das estratégias novas; exports repetidos não aumentam essa contagem.\n\n"
    text+='HTMLs tiveram estrutura e sintaxe JavaScript verificadas. Quando Node está disponível, seleção, filtros e contratos do grafo são exercitados em DOM mínimo simulado, com hash do HTML no relatório. Não houve renderização visual de navegador; simulação DOM não comprova layout ou acessibilidade completa.\n\n'
    text+='## O que não foi demonstrado\n\nNão houve inferência real de 3–30B, treinamento, embeddings reais, benchmark GPU, implantação na Helena ou execução das receitas industriais. O comparador de sistemas recebeu dados sintéticos apenas nos testes de contrato. Não há medição de paridade com fronteira, certificação de acervo mundialmente superior ou garantia de ausência de erro factual.\n\n'
    text+='## Reprodutibilidade\n\n'
    text+=f"- Python: {platform.python_version()}.\n- Avaliado em: {freeze['evaluated_at']}.\n- Corpus SHA-256: `{freeze['corpus_sha256']}`.\n- Hashes de código, entradas, fontes, casos e consultas: `evidencias/configuracao_avaliada.json`.\n- Integridade do ZIP e hashes dos arquivos são conferidos pelo empacotador; hashes não comprovam a verdade das fontes.\n\n"
    text+='## Falhas observadas no perfil padrão\n\n'
    for name in ['historicas90_expandido','reserva_v3_conhecida40_expandido']:
        text+='### '+name+'\n\n'
        failures=[c for c in evaluations[name]['cases'] if not c['hit_at_5']]
        if not failures:text+='Todas as consultas tiveram algum ID esperado entre os cinco primeiros.\n\n'
        for c in failures:text+=f"- {c['case_id']}: {c['query']} Esperados: {', '.join(c['expected_ids'])}. Recuperados: {', '.join(c['retrieved_ids'][:5])}.\n"
        text+='\n'
    (root/'RELATORIO_VALIDACAO.md').write_text(text,encoding='utf-8')


if __name__=='__main__':raise SystemExit(main())
