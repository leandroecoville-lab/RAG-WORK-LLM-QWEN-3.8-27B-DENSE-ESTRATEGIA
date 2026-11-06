"""Empacota a edição v4 já validada e verifica CRC e hashes de todos os membros."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'LAI_RAG_243_COMPLETO_v4.zip'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    freeze=json.loads((ROOT/'evidencias/configuracao_avaliada.json').read_text(encoding='utf-8'))
    assert manifest['version']=='4.0.0'
    assert manifest['verification']['required_gates_passed']
    assert manifest['stats']['entries_by_scope']=={'inventario':243,'referencia':27,'proposta':17}
    assert manifest['stats']['chunks']==2583 and manifest['stats']['qa']==1148
    assert manifest['stats']==json.loads((ROOT/'catalogo/estatisticas.json').read_text(encoding='utf-8'))
    assert manifest['corpus_sha256']==digest(ROOT/'corpus/chunks.jsonl')
    for name,expected in freeze['code_hashes'].items():assert expected==digest(ROOT/'runtime'/name),name
    for name,expected in freeze['known_queries_sha256'].items():assert expected==digest(ROOT/'tests'/name),name
    for key,name in [('entries_sha256','corpus/entries.jsonl'),('cases_sha256','producao/casos.jsonl'),('sources_sha256','fontes/sources.jsonl')]:assert freeze[key]==digest(ROOT/name),name
    for name,expected in freeze.get('derived_hashes',{}).items():assert expected==digest(ROOT/name),name
    for name,expected in freeze.get('test_hashes',{}).items():assert expected==digest(ROOT/'tests'/name),name
    for path in sorted(ROOT.rglob('__pycache__'),reverse=True):
        if path.is_dir():shutil.rmtree(path)
    files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json']
    assert not any(p.is_symlink() for p in files)
    hashes={str(p.relative_to(ROOT)):digest(p) for p in files}
    (ROOT/'SHA256SUMS.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files.append(ROOT/'SHA256SUMS.json');files.sort()
    with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in files:archive.write(path,arcname=str(path.relative_to(ROOT.parent)))
    with zipfile.ZipFile(DEST) as archive:
        assert archive.testzip() is None
        names=archive.namelist()
        assert len(names)==len(set(names))==len(files)
        per_base={}
        for name in names:
            parts=name.split('/')
            assert '..' not in parts and not name.startswith('/')
            if len(parts)==4 and parts[1]=='bases':per_base.setdefault(parts[2],set()).add(parts[3])
        expected={'knowledge.md','metadata.json','chunks.jsonl','sources.json','qa.json','research.json','strategy.json','production_cases.json','connections.json','graph.mmd'}
        assert len(per_base)==287 and all(items==expected for items in per_base.values())
        archived_hashes=json.loads(archive.read(ROOT.name+'/SHA256SUMS.json'))
        for name,expected_hash in archived_hashes.items():
            assert hashlib.sha256(archive.read(ROOT.name+'/'+name)).hexdigest()==expected_hash,name
    report={'file':str(DEST),'bytes':DEST.stat().st_size,'sha256':digest(DEST),'zip_members':len(files),
            'crc_passed':True,'hashed_files':len(hashes),'file_hashes_passed':True,
            'individual_bases':len(per_base),'files_per_base':10,'version':manifest['version']}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':main()
