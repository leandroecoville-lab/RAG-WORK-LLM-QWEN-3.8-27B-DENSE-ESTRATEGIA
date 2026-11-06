"""Gera schemas estruturais v4. Referências cruzadas são validadas em Python."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
S={'type':'string','minLength':1}
ID={**S,'pattern':'^[TRP][0-9]{3}$'}
IDS={'type':'array','items':S,'minItems':1,'uniqueItems':True}
def obj(fields,optional=()):
    return {'type':'object','properties':fields,'required':[k for k in fields if k not in optional],'additionalProperties':False}
def arr(item,n=1): return {'type':'array','items':item,'minItems':n}
def enum(values): return {'enum':values.split()}
basis=enum('engineering_proposal source_documented')
strategy=obj({
 'id':ID,'novelty':S,'deep_layers':arr(obj({'name':S,'detail':S,'basis':basis,'source_ids':IDS}),3),
 'advanced_uses':arr(obj({'name':S,'scenario':S,'strategy':S,'small_model_role':S,'acceptance':S,'basis':basis,'source_ids':IDS}),2),
 'small_model_fit':obj({k:S for k in ['3_7b','8_14b','15_30b','training_or_runtime_requirements','do_not_use_when']}),
 'connections':{**arr(obj({'target_id':ID,'relation':enum('feeds requires complements alternative conflicts'),'how':S,'interface':S,'condition':S,'acceptance':S,'basis':basis,'source_ids':IDS,'case_ids':{**IDS,'minItems':0}}),2),'maxItems':4},
 'failure_controls':arr(S,2),'frontier_comparison':S,'production_search':obj({'search_ids':IDS,'scope_note':S}),'source_ids':IDS})
case=obj({'case_id':{**S,'pattern':'^V4[A-D]-C[0-9]{3}$'},'company':S,'system':S,'title':S,'evidence_level':enum('production_documented operational_product research_only'),'observed_use':S,'technical_mechanism':S,'event_date':{'type':['string','null'],'format':'date'},'checked_on':{'type':'string','format':'date'},'source_ids':IDS,'mappings':arr(obj({'entry_id':ID,'match':enum('exact family analogy'),'rationale':S})),'small_model_transfer':S,'limits':S,'organization_class':enum('bigtech ai_lab technology_operator research_group'),'canonical_case_id':S,'deduplication_note':S,'deployment_domain':S,'review_note':S},['canonical_case_id','deduplication_note','deployment_domain','review_note'])
query=obj({'search_id':S,'query':S,'entry_ids':{**IDS,'items':ID},'checked_on':{'type':'string','format':'date'},'findings':S,'limits':S,'web_refs':{**IDS,'minItems':0}})
for name,schema in [('strategy',strategy),('case',case),('search',query)]:
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:lai:rag:'+name+':v4','title':'LAI RAG '+name,**schema}
    (ROOT/'schemas'/(name+'.schema.json')).write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'schemas/chunk.schema.json';chunk=json.loads(path.read_text())
chunk['$id']='urn:lai:rag:chunk:v4';chunk['properties']['chunk_id']['pattern']='^[TRP][0-9]{3}:C0[1-9]$'
chunk['properties']['section']['enum']=['conceito','aplicacao','riscos_validacao','perguntas_proveniencia','mecanismo_avancado','experimento_comparacao','estrategia_3_30b','casos_producao','conexoes_aceite']
path.write_text(json.dumps(chunk,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
