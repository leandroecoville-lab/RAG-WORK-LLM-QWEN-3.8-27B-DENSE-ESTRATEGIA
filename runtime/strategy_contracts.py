"""Contratos de estratégias, casos e conexões v4. Validação estrutural, sem rede.

Uma referência válida não comprova que a interpretação da fonte esteja correta.
Os controles impedem confundir categorias por erro de montagem do pacote.
"""
from __future__ import annotations

from collections import Counter
import re

BASIS = {'engineering_proposal', 'source_documented'}
LEVELS = {'production_documented', 'operational_product', 'research_only'}
MATCHES = {'exact', 'family', 'analogy'}
RELATIONS = {'feeds', 'requires', 'complements', 'alternative', 'conflicts'}
ORGANIZATIONS = {'bigtech', 'ai_lab', 'technology_operator', 'research_group'}
LLM_PRODUCTION_DOMAINS = {'llm_application', 'llm_serving', 'llm_training'}


def is_text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_strategy(entry, entries, sources, cases, searches):
    errors=[]
    eid=entry.get('id','?') if isinstance(entry,dict) else '?'
    def fail(path,message): errors.append(f'{eid}: strategy.{path} {message}')
    def obj(value, required, path):
        if not isinstance(value,dict):
            fail(path,'deve ser objeto'); return False
        missing=set(required)-value.keys()
        extra=value.keys()-set(required)
        if missing: fail(path,'campos ausentes: '+', '.join(sorted(missing)))
        if extra: fail(path,'campos desconhecidos: '+', '.join(sorted(extra)))
        return True
    def text(value,path):
        if not is_text(value): fail(path,'deve ser texto não vazio')
    def ids(value,registry,path,allow_empty=False):
        if not isinstance(value,list): fail(path,'deve ser lista'); return set()
        if not value and not allow_empty: fail(path,'lista vazia')
        valid={i for i in value if is_text(i)}
        if len(valid)!=len(value): fail(path,'IDs inválidos ou duplicados')
        if valid-set(registry): fail(path,'referências ausentes: '+', '.join(sorted(valid-set(registry))))
        return valid
    if not isinstance(entry,dict): return ['entrada inválida para estratégia']
    s=entry.get('strategy')
    fields={'id','novelty','deep_layers','advanced_uses','small_model_fit','connections','failure_controls','frontier_comparison','production_search','source_ids'}
    if not obj(s,fields,''): return errors
    if s.get('id')!=eid: fail('id','difere da entrada')
    declared=ids(s.get('source_ids'),sources,'source_ids')
    if declared-set(entry.get('source_ids',[])): fail('source_ids','faltam fontes no registro pai')
    for k in ['novelty','frontier_comparison']: text(s.get(k),k)
    def basis_sources(item,path):
        if not is_text(item.get('basis')) or item.get('basis') not in BASIS: fail(path+'.basis','classificação inválida')
        refs=ids(item.get('source_ids'),sources,path+'.source_ids')
        if refs-declared: fail(path+'.source_ids','não declaradas na estratégia')
    for field,minimum,required in [
        ('deep_layers',3,{'name','detail','basis','source_ids'}),
        ('advanced_uses',2,{'name','scenario','strategy','small_model_role','acceptance','basis','source_ids'}),
        ('connections',2,{'target_id','relation','how','interface','condition','acceptance','basis','source_ids','case_ids'})]:
        items=s.get(field)
        if not isinstance(items,list): fail(field,'deve ser lista'); continue
        if len(items)<minimum: fail(field,f'exige ao menos {minimum} itens')
        if field=='connections' and len(items)>4: fail(field,'máximo de quatro conexões por ficha')
        seen=set()
        for n,item in enumerate(items):
            p=f'{field}[{n}]'
            if not obj(item,required,p): continue
            for key in required-{'basis','source_ids','case_ids'}: text(item.get(key),p+'.'+key)
            basis_sources(item,p)
            if field=='connections':
                target=item.get('target_id')
                if not is_text(target) or target not in entries or target==eid:
                    fail(p+'.target_id','alvo ausente ou autoaresta')
                    continue
                pair=(target,item.get('relation'))
                if not is_text(item.get('relation')):
                    fail(p+'.relation','inválida');continue
                if pair in seen: fail(p,'conexão repetida')
                seen.add(pair)
                if item.get('relation') not in RELATIONS: fail(p+'.relation','inválida')
                cids=ids(item.get('case_ids'),cases,p+'.case_ids',True)
                if item.get('basis')=='source_documented':
                    if not cids: fail(p+'.case_ids','conexão documentada exige caso operacional')
                    if str(eid).startswith('P') or str(target).startswith('P'):
                        fail(p,'componente editorial P não tem adoção documentada sob esse nome')
                    support=False
                    for cid in cids:
                        case=cases.get(cid,{})
                        matches={m.get('entry_id'):m.get('match') for m in case.get('mappings',[]) if isinstance(m,dict)}
                        if case.get('evidence_level') in {'production_documented','operational_product'} and matches.get(eid)=='exact' and matches.get(target)=='exact' and set(item.get('source_ids',[])) & set(case.get('source_ids',[])):
                            support=True
                    if not support: fail(p,'nenhum caso operacional mapeia exatamente os dois mecanismos com fonte em comum')
    fit=s.get('small_model_fit')
    keys={'3_7b','8_14b','15_30b','training_or_runtime_requirements','do_not_use_when'}
    if obj(fit,keys,'small_model_fit'):
        for k in keys: text(fit.get(k),'small_model_fit.'+k)
        if len({fit.get(k) for k in ['3_7b','8_14b','15_30b'] if is_text(fit.get(k))})!=3:
            fail('small_model_fit','bandas precisam de orientações distintas')
    controls=s.get('failure_controls')
    if not isinstance(controls,list) or len(controls)<2: fail('failure_controls','exige ao menos dois controles')
    elif any(not is_text(v) for v in controls): fail('failure_controls','controle inválido')
    search=s.get('production_search')
    if obj(search,{'search_ids','scope_note'},'production_search'):
        qids=ids(search.get('search_ids'),searches,'production_search.search_ids')
        text(search.get('scope_note'),'production_search.scope_note')
        if qids and not any(eid in searches.get(q,{}).get('entry_ids',[]) for q in qids):
            fail('production_search','nenhuma consulta citada registra cobertura deste ID')
    return errors


def validate_case(case, entries, sources):
    errors=[]
    cid=case.get('case_id','?') if isinstance(case,dict) else '?'
    def fail(m): errors.append(f'{cid}: {m}')
    if not isinstance(case,dict): return ['caso deve ser objeto']
    required={'case_id','company','system','title','evidence_level','observed_use','technical_mechanism','event_date','checked_on','source_ids','mappings','small_model_transfer','limits','organization_class'}
    allowed=required|{'canonical_case_id','deduplication_note','deployment_domain','review_note'}
    if required-case.keys(): fail('campos ausentes: '+', '.join(sorted(required-case.keys())))
    if case.keys()-allowed: fail('campos desconhecidos: '+', '.join(sorted(case.keys()-allowed)))
    if not isinstance(cid,str) or not re.fullmatch(r'V4[A-D]-C\d{3}',cid): fail('ID inválido')
    for k in required-{'event_date','source_ids','mappings'}:
        if not is_text(case.get(k)): fail(k+' deve ser texto não vazio')
    if not is_text(case.get('evidence_level')) or case.get('evidence_level') not in LEVELS: fail('evidence_level inválido')
    if not is_text(case.get('organization_class')) or case.get('organization_class') not in ORGANIZATIONS: fail('organization_class inválido')
    for k in ['event_date','checked_on']:
        value=case.get(k)
        if value is not None and (not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value)):
            fail(k+' deve usar ISO YYYY-MM-DD ou null')
    refs=case.get('source_ids')
    if not isinstance(refs,list) or not refs or any(not is_text(v) for v in refs): fail('source_ids inválido')
    else:
        if len(set(refs))!=len(refs) or set(refs)-set(sources): fail('fontes ausentes ou duplicadas')
        if case.get('evidence_level')=='production_documented' and not any(sources.get(s,{}).get('verification')=='opened' for s in refs): fail('produção exige fonte efetivamente aberta')
    mappings=case.get('mappings')
    if not isinstance(mappings,list) or not mappings: fail('mappings deve ser lista não vazia'); return errors
    seen=set()
    for m in mappings:
        if not isinstance(m,dict) or set(m)!={'entry_id','match','rationale'}: fail('mapeamento malformado'); continue
        eid=m.get('entry_id')
        if not is_text(eid): fail('entry_id inválido no mapeamento');continue
        if eid not in entries or eid in seen: fail('entry_id ausente ou duplicado no caso')
        seen.add(eid)
        if not is_text(m.get('match')) or m.get('match') not in MATCHES or not is_text(m.get('rationale')): fail('mapeamento sem tipo ou justificativa')
        if str(eid).startswith('P') and m.get('match')!='analogy': fail('componente P só pode ser analogia')
    return errors


def validate_registry(entries,sources,cases,searches):
    errors=[]
    registries={}
    for label,rows,key in [('entries',entries,'id'),('sources',sources,'source_id'),('cases',cases,'case_id'),('searches',searches,'search_id')]:
        if not isinstance(rows,list): errors.append(label+' deve ser lista'); rows=[]
        valid={}
        for row in rows:
            if not isinstance(row,dict) or not is_text(row.get(key)):
                errors.append(label+' contém objeto ou ID inválido'); continue
            if row[key] in valid: errors.append(label+' contém ID repetido: '+row[key])
            valid[row[key]]=row
        registries[label]=valid
    e,s,c,q=(registries[k] for k in ['entries','sources','cases','searches'])
    for query in q.values():
        qid=query['search_id']
        fields={'search_id','query','entry_ids','checked_on','findings','limits','web_refs'}
        if set(query)!=fields: errors.append(qid+': campos de consulta inválidos')
        for k in ['query','checked_on','findings','limits']:
            if not is_text(query.get(k)): errors.append(qid+': '+k+' vazio')
        ids=query.get('entry_ids')
        if not isinstance(ids,list) or not ids or any(not is_text(i) or i not in e for i in ids): errors.append(qid+': entry_ids inválidos')
        if not isinstance(query.get('web_refs'),list) or any(not is_text(r) for r in query.get('web_refs',[])): errors.append(qid+': web_refs inválidos')
    for case in c.values():
        errors.extend(validate_case(case,e,s))
        canonical=case.get('canonical_case_id',case['case_id'])
        if not is_text(canonical) or canonical not in c: errors.append(case['case_id']+': canonical_case_id ausente')
        elif c[canonical].get('canonical_case_id',canonical)!=canonical: errors.append(case['case_id']+': alias de caso em cadeia/ciclo')
    for entry in e.values(): errors.extend(validate_strategy(entry,e,s,c,q))
    return errors


def cases_for_entry(eid,cases):
    """Uma implantação canônica conta uma vez por entrada, mesmo com fontes extras."""
    rows={}
    for case in cases:
        match=next((m for m in case['mappings'] if m['entry_id']==eid),None)
        if match is None: continue
        key=case.get('canonical_case_id',case['case_id'])
        item={**case,'mapping':match}
        old=rows.get(key)
        # Preferir correspondência exata; todos os registros permanecem no registry.
        rank={'exact':0,'family':1,'analogy':2}
        if old is None or (rank[match['match']],case['case_id']) < (rank[old['mapping']['match']],old['case_id']): rows[key]=item
    return sorted(rows.values(),key=lambda c:({'production_documented':0,'operational_product':1,'research_only':2}[c['evidence_level']],{'exact':0,'family':1,'analogy':2}[c['mapping']['match']],c['company'],c['case_id']))


def production_coverage(eid,cases,target=10):
    rows=cases_for_entry(eid,cases)
    strict=[c for c in rows if c['evidence_level']=='production_documented' and c['mapping']['match']=='exact' and c['organization_class']=='bigtech']
    labs=[c for c in rows if c['evidence_level']=='production_documented' and c['mapping']['match']=='exact' and c['organization_class']=='ai_lab']
    operators=[c for c in rows if c['evidence_level']=='production_documented' and c['mapping']['match']=='exact' and c['organization_class'] not in {'bigtech','ai_lab'}]
    return {'entry_id':eid,'requested_bigtech_production_examples':target,'verified_bigtech_production_exact':len(strict),'verified_bigtech_llm_production_exact':sum(c.get('deployment_domain') in LLM_PRODUCTION_DOMAINS for c in strict),'verified_ai_lab_production_exact':len(labs),'verified_other_operator_production_exact':len(operators),'unique_cases_associated':len(rows),'operational_product_cases':sum(c['evidence_level']=='operational_product' for c in rows),'research_cases':sum(c['evidence_level']=='research_only' for c in rows),'family_or_analogy_cases':sum(c['mapping']['match']!='exact' for c in rows),'missing_to_target':max(0,target-len(strict)),'target_met':len(strict)>=target,'strict_case_ids':[c['case_id'] for c in strict],'gap_meaning':'Não comprovado nesta curadoria; não significa inexistência mundial. A contagem do mecanismo pode incluir infraestrutura sem LLM; o subconjunto LLM é exposto separadamente.'}
