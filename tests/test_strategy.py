"""Contratos de evidência e filtros v4. Não prova a interpretação factual da fonte."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
import rag
from strategy_contracts import validate_registry, validate_strategy, validate_case, production_coverage


class StrategyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine=rag.Engine(ROOT)
        cls.entries=cls.engine.entries;cls.sources=cls.engine.sources
        cls.cases={c['case_id']:c for c in rag.read_jsonl(ROOT/'producao/casos.jsonl')}
        cls.queries={q['search_id']:q for q in rag.read_jsonl(ROOT/'pesquisa/CONSULTAS_V4.jsonl')}

    def errors(self,entry):
        return validate_strategy(entry,self.entries,self.sources,self.cases,self.queries)

    def test_actual_registry_resolves_all_references(self):
        self.assertEqual(validate_registry(list(self.entries.values()),list(self.sources.values()),list(self.cases.values()),list(self.queries.values())),[])

    def test_documented_edge_cannot_be_created_without_operational_case(self):
        entry=copy.deepcopy(self.entries['T001'])
        entry['strategy']['connections'][0].update(basis='source_documented',case_ids=[])
        self.assertTrue(any('caso operacional' in e for e in self.errors(entry)))

    def test_missing_source_search_and_identical_bands_are_detected(self):
        entry=copy.deepcopy(self.entries['T001'])
        entry['strategy']['source_ids'].append('FONTE_INEXISTENTE')
        entry['strategy']['production_search']['search_ids']=['QUERY_INEXISTENTE']
        entry['strategy']['small_model_fit']['8_14b']=entry['strategy']['small_model_fit']['3_7b']
        errors=self.errors(entry)
        self.assertTrue(any('FONTE_INEXISTENTE' in e for e in errors))
        self.assertTrue(any('QUERY_INEXISTENTE' in e for e in errors))
        self.assertTrue(any('bandas' in e for e in errors))

    def test_proposed_components_cannot_be_literal_production_cases(self):
        case=copy.deepcopy(self.cases['V4D-C002'])
        case['mappings']=[{'entry_id':'P004','match':'exact','rationale':'Fixture incorreta que deve ser rejeitada.'}]
        self.assertTrue(any('analogia' in e for e in validate_case(case,self.entries,self.sources)))

    def test_production_target_does_not_count_product_research_family_or_other_operators(self):
        base=copy.deepcopy(self.cases['V4D-C002'])
        base['mappings']=[{'entry_id':'T079','match':'exact','rationale':'Fixture de contagem.'}]
        base['canonical_case_id']=base['case_id']
        rows=[base]
        for n,changes in enumerate([{'evidence_level':'operational_product'},{'evidence_level':'research_only'},{'organization_class':'ai_lab'},{'organization_class':'technology_operator'}],90):
            item=copy.deepcopy(base);item.update(changes,case_id=f'V4D-C{n:03}',canonical_case_id=f'V4D-C{n:03}');rows.append(item)
        family=copy.deepcopy(base);family.update(case_id='V4D-C099',canonical_case_id='V4D-C099');family['mappings'][0]['match']='family';rows.append(family)
        c=production_coverage('T079',rows)
        self.assertEqual(c['verified_bigtech_production_exact'],1)
        self.assertEqual(c['verified_ai_lab_production_exact'],1)
        self.assertEqual(c['verified_other_operator_production_exact'],1)
        self.assertEqual(c['missing_to_target'],9)
        base['deployment_domain']='distributed_data_system'
        self.assertEqual(production_coverage('T079',[base])['verified_bigtech_llm_production_exact'],0)
        base['deployment_domain']='llm_serving'
        self.assertEqual(production_coverage('T079',[base])['verified_bigtech_llm_production_exact'],1)

    def test_duplicate_reports_of_same_deployment_count_once(self):
        base=copy.deepcopy(self.cases['V4D-C002']);base['canonical_case_id']=base['case_id']
        other=copy.deepcopy(base);other['case_id']='V4D-C099'
        self.assertEqual(production_coverage('T079',[base,other])['verified_bigtech_production_exact'],1)

    def test_layer_filter_applies_to_seeds_and_parent_expansion(self):
        for layer,sections in rag.LAYERS.items():
            hits=self.engine.search('T009',entry_id='T009',layer=layer,unique=False,top_k=20)
            self.assertTrue(hits)
            self.assertTrue(all(h['section'] in sections for h in hits))
            pack=self.engine.context('T009',entry_id='T009',layer=layer,max_chars=100000)
            selected=set(pack['selected_chunks'])
            self.assertTrue(selected)
            self.assertTrue(all(c['section'] in sections for c in self.engine.chunks if c['chunk_id'] in selected))
        with self.assertRaises(ValueError): self.engine.search('T009',layer='inventado')

    def test_new_chunks_are_citable_and_global_graph_matches_per_entry(self):
        self.assertTrue(rag.check_citations('Estratégia [T009:C07], casos [T009:C08], ligações [T009:C09].',['T009:C07','T009:C08','T009:C09'])['passed'])
        graph=json.loads((ROOT/'grafos/conexoes.json').read_text())
        self.assertEqual(len(graph['edges']),sum(len(e['strategy']['connections']) for e in self.entries.values()))
        for entry in self.entries.values():
            individual=json.loads((ROOT/'bases'/entry['id']/'connections.json').read_text())
            self.assertEqual(individual['edges'],[e for e in graph['edges'] if e['from']==entry['id']])


if __name__=='__main__': unittest.main()
