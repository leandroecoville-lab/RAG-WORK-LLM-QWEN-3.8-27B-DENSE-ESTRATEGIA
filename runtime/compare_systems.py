#!/usr/bin/env python3
"""Compara observações PAREADAS de um sistema 3–30B e um baseline explícito.

Não executa modelos, não estima preços de terceiros e não gera resultados.
Configuração e dados são entradas do usuário. CI é bootstrap por cluster,
aproximado, e não constitui prova de paridade geral ou ausência de risco.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
import sys


def finite(value,minimum=0):
    return not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value) and value>=minimum


def percentile(values,p):
    if not values: return None
    ordered=sorted(values)
    return ordered[max(0,math.ceil(p*len(ordered))-1)]


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def compare(config,observations):
    if not isinstance(config,dict) or not isinstance(observations,list) or not observations:
        raise ValueError('Configuração deve ser objeto; observações devem ser lista não vazia')
    required={'experiment_id','dataset_revision','candidate','baseline','quality_margin','minimum_clusters','max_cost_per_success_ratio','max_p95_latency_ratio','max_critical_failures','bootstrap_replicates','seed','cost_accounting'}
    if set(config)!=required: raise ValueError('Campos da configuração divergentes: '+str(sorted(set(config)^required)))
    for key in ['experiment_id','dataset_revision','cost_accounting']:
        if not isinstance(config[key],str) or not config[key].strip(): raise ValueError(key+' vazio')
    if not finite(config['quality_margin']) or config['quality_margin']>1: raise ValueError('quality_margin deve estar em [0,1]')
    for key in ['minimum_clusters','max_critical_failures','bootstrap_replicates','seed']:
        if type(config[key]) is not int or config[key]<0: raise ValueError(key+' deve ser inteiro não negativo')
    if config['minimum_clusters']<2 or not 100<=config['bootstrap_replicates']<=20000: raise ValueError('Exigir >=2 clusters e 100–20000 réplicas')
    for key in ['max_cost_per_success_ratio','max_p95_latency_ratio']:
        if not finite(config[key]) or config[key]<=0: raise ValueError(key+' deve ser positivo')
    model_fields={'system_id','model_revision','total_parameters_b','active_parameters_b','hardware','runtime_revision','policy_revision','amortized_fixed_cost_per_request_usd'}
    models={}
    for label in ['candidate','baseline']:
        model=config[label]
        if not isinstance(model,dict) or set(model)!=model_fields: raise ValueError('Metadados incompletos: '+label)
        for k in ['system_id','model_revision','hardware','runtime_revision','policy_revision']:
            if not isinstance(model[k],str) or not model[k].strip(): raise ValueError(label+'.'+k+' vazio')
        if not finite(model['amortized_fixed_cost_per_request_usd']): raise ValueError('Custo fixo amortizado inválido')
        for k in ['total_parameters_b','active_parameters_b']:
            if model[k] is not None and not finite(model[k],0.001): raise ValueError(k+' inválido')
        if model['active_parameters_b'] is not None and model['total_parameters_b'] is not None and model['active_parameters_b']>model['total_parameters_b']: raise ValueError('Parâmetros ativos maiores que totais')
        if model['system_id'] in models: raise ValueError('Candidate e baseline devem ter IDs distintos')
        models[model['system_id']]=model
    candidate=config['candidate']['system_id'];baseline=config['baseline']['system_id']
    size=config['candidate']['total_parameters_b']
    if size is None or not 3<=size<=30: raise ValueError('Candidate deve declarar 3–30B parâmetros TOTAIS')
    fields={'task_id','trial_id','cluster_id','system_id','success','critical_failure','latency_ms','runtime_cost_usd','input_tokens','output_tokens','evidence_uri'}
    paired=defaultdict(dict);systems=defaultdict(list)
    for row in observations:
        if not isinstance(row,dict) or set(row)!=fields: raise ValueError('Observação com campos divergentes')
        for key in ['task_id','trial_id','cluster_id','system_id','evidence_uri']:
            if not isinstance(row[key],str) or not row[key].strip(): raise ValueError('Observação com '+key+' inválido')
        sid=row['system_id']
        if sid not in models: raise ValueError('Sistema não declarado')
        for key in ['success','critical_failure']:
            if type(row[key]) is not bool: raise ValueError(key+' exige booleano')
        if row['success'] and row['critical_failure']: raise ValueError('Falha crítica não pode ser marcada como sucesso')
        for key in ['latency_ms','runtime_cost_usd']:
            if not finite(row[key]): raise ValueError(key+' deve ser finito e não negativo')
        for key in ['input_tokens','output_tokens']:
            if type(row[key]) is not int or row[key]<0: raise ValueError(key+' deve ser inteiro não negativo')
        key=(row['task_id'],row['trial_id'])
        if sid in paired[key]: raise ValueError('Execução duplicada para task/trial/system')
        paired[key][sid]=row;systems[sid].append(row)
    clusters=defaultdict(list);task_clusters={}
    for key,pair in paired.items():
        if set(pair)!={candidate,baseline}: raise ValueError('Pareamento incompleto: '+str(key))
        a,b=pair[candidate],pair[baseline]
        if a['cluster_id']!=b['cluster_id']: raise ValueError('Cluster difere entre sistemas')
        old_cluster=task_clusters.setdefault(a['task_id'],a['cluster_id'])
        if old_cluster!=a['cluster_id']: raise ValueError('Repetições da mesma tarefa não podem ser clusters independentes')
        clusters[a['cluster_id']].append(int(a['success'])-int(b['success']))
    if len(clusters)<2: raise ValueError('Bootstrap por cluster exige ao menos dois clusters')
    summary={}
    for sid,rows in systems.items():
        accepted=sum(r['success'] for r in rows)
        runtime=sum(r['runtime_cost_usd'] for r in rows)
        all_in=runtime+models[sid]['amortized_fixed_cost_per_request_usd']*len(rows)
        summary[sid]={'requests':len(rows),'accepted':accepted,'success_rate':accepted/len(rows),'critical_failures_observed':sum(r['critical_failure'] for r in rows),'latency_p50_ms':percentile([r['latency_ms'] for r in rows],.5),'latency_p95_ms':percentile([r['latency_ms'] for r in rows],.95),'runtime_cost_usd':runtime,'all_in_cost_usd':all_in,'cost_per_accepted_usd':all_in/accepted if accepted else None,'input_tokens':sum(r['input_tokens'] for r in rows),'output_tokens':sum(r['output_tokens'] for r in rows)}
    groups=list(clusters.values());rng=random.Random(config['seed']);samples=[]
    for _ in range(config['bootstrap_replicates']):
        sampled=[groups[rng.randrange(len(groups))] for _ in groups]
        samples.append(sum(sum(v) for v in sampled)/sum(len(v) for v in sampled))
    delta=sum(sum(v) for v in groups)/sum(map(len,groups))
    ci=[percentile(samples,.025),percentile(samples,.975)]
    a,b=summary[candidate],summary[baseline]
    def ratio(n,d): return n/d if n is not None and d is not None and d>0 else None
    cost_ratio=ratio(a['cost_per_accepted_usd'],b['cost_per_accepted_usd'])
    latency_ratio=ratio(a['latency_p95_ms'],b['latency_p95_ms'])
    checks={'sample_size_sufficient':len(clusters)>=config['minimum_clusters'],'quality_noninferiority_on_declared_margin':ci[0]>=-config['quality_margin'],'observed_critical_failures_within_limit':a['critical_failures_observed']<=config['max_critical_failures'],'cost_ratio_within_limit':cost_ratio is not None and cost_ratio<=config['max_cost_per_success_ratio'],'p95_latency_ratio_within_limit':latency_ratio is not None and latency_ratio<=config['max_p95_latency_ratio']}
    return {'experiment_id':config['experiment_id'],'dataset_revision':config['dataset_revision'],'config_sha256':digest(config),'observations_sha256':digest(observations),'systems':summary,'paired_trials':len(paired),'independent_clusters_declared':len(groups),'quality_delta_candidate_minus_baseline':delta,'quality_delta_cluster_bootstrap_95ci':ci,'cost_per_accepted_ratio':cost_ratio,'latency_p95_ratio':latency_ratio,'checks':checks,'status':'criteria_met_on_this_dataset' if all(checks.values()) else 'criteria_not_met_or_insufficient_evidence','limits':['Não comprova paridade geral, liderança mundial ou independência real dos clusters declarados.','Bootstrap de clusters é aproximado; poucos clusters ou seleção enviesada podem produzir intervalo enganoso.','Não verificou se as margens foram definidas antes da coleta, se o juiz está correto ou se houve contaminação.','Latência e custo são limites sobre medidas observadas; não há intervalo de confiança para suas razões nesta versão.','Zero falhas críticas observadas não demonstra risco zero.','Custo deve incluir chamadas de professor, retries, ferramentas, infraestrutura e amortização coerente; valores são fornecidos pelo usuário.'],'external_calls':0}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path,required=True);p.add_argument('--observations',type=Path,required=True);p.add_argument('--out',type=Path)
    args=p.parse_args()
    try:
        config=json.loads(args.config.read_text(encoding='utf-8'))
        rows=[json.loads(line) for line in args.observations.read_text(encoding='utf-8').splitlines() if line.strip()]
        result=compare(config,rows)
        raw=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
        if args.out:
            args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(raw,encoding='utf-8')
        print(raw,end='');return 0
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr);return 2


if __name__=='__main__': raise SystemExit(main())
