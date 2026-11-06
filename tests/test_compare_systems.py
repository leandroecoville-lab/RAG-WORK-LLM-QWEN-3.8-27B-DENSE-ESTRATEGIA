"""Dados sintéticos temporários verificam cálculo; não são benchmark de LLM."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
import compare_systems as comp


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'avaliacao/configuracao_exemplo.json').read_text())
        self.config.update(minimum_clusters=3,bootstrap_replicates=200,max_cost_per_success_ratio=.6,max_p95_latency_ratio=1.1)
        self.rows=[]
        for n in range(4):
            for sid,cost,latency in [('candidato',.01,10),('baseline',.02,20)]:
                self.rows.append({'task_id':str(n),'trial_id':'0','cluster_id':str(n),'system_id':sid,'success':True,'critical_failure':False,'latency_ms':latency,'runtime_cost_usd':cost,'input_tokens':10,'output_tokens':5,'evidence_uri':'synthetic-test-only/'+str(n)+'/'+sid})

    def test_paired_success_and_cost_are_computed_from_observations(self):
        r=comp.compare(self.config,self.rows)
        self.assertEqual(r['quality_delta_candidate_minus_baseline'],0)
        self.assertEqual(r['cost_per_accepted_ratio'],.5)
        self.assertEqual(r['latency_p95_ratio'],.5)
        self.assertEqual(r['status'],'criteria_met_on_this_dataset')
        self.assertEqual(r['external_calls'],0)

    def test_missing_or_duplicate_pair_is_rejected(self):
        with self.assertRaises(ValueError): comp.compare(self.config,self.rows[:-1])
        with self.assertRaises(ValueError): comp.compare(self.config,self.rows+[self.rows[0]])

    def test_invalid_numbers_and_moe_active_total_confusion_are_rejected(self):
        for invalid in [float('nan'),float('inf'),-1,True]:
            rows=copy.deepcopy(self.rows);rows[0]['runtime_cost_usd']=invalid
            with self.assertRaises(ValueError): comp.compare(self.config,rows)
        config=copy.deepcopy(self.config);config['candidate']['total_parameters_b']=70;config['candidate']['active_parameters_b']=7
        with self.assertRaises(ValueError): comp.compare(config,self.rows)

    def test_zero_accepted_cost_is_undefined_and_gate_fails(self):
        rows=copy.deepcopy(self.rows)
        for r in rows:
            if r['system_id']=='candidato':r['success']=False
        result=comp.compare(self.config,rows)
        self.assertIsNone(result['systems']['candidato']['cost_per_accepted_usd'])
        self.assertIsNone(result['cost_per_accepted_ratio'])
        self.assertFalse(result['checks']['cost_ratio_within_limit'])
        self.assertEqual(result['quality_delta_cluster_bootstrap_95ci'],[-1,-1])

    def test_insufficient_clusters_and_critical_failure_cannot_pass(self):
        config=copy.deepcopy(self.config);config['minimum_clusters']=10
        self.assertFalse(comp.compare(config,self.rows)['checks']['sample_size_sufficient'])
        rows=copy.deepcopy(self.rows);rows[0].update(success=False,critical_failure=True)
        self.assertFalse(comp.compare(self.config,rows)['checks']['observed_critical_failures_within_limit'])
        rows[0]['success']=True
        with self.assertRaises(ValueError): comp.compare(self.config,rows)

    def test_bootstrap_is_reproducible_and_cluster_pairing_is_required(self):
        rows=copy.deepcopy(self.rows);rows[0]['success']=False
        a=comp.compare(self.config,rows);b=comp.compare(self.config,rows)
        self.assertEqual(a,b)
        rows[0]['cluster_id']='divergente'
        with self.assertRaises(ValueError): comp.compare(self.config,rows)


if __name__=='__main__': unittest.main()
