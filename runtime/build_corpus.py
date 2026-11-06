#!/usr/bin/env python3
"""Renderiza as bases individuais e os chunks a partir do corpus editorial JSONL.

Fonte editável: corpus/entries.jsonl. Fontes bibliográficas: fontes/sources.jsonl.
Não acessa a rede e não reescreve o conteúdo editorial desses dois arquivos.
"""
from collections import Counter
import csv
import html
import json
from pathlib import Path
import re

from rag import DEFAULT_ROOT, VERSION, SECTION_ORDER, atomic_bytes, build_index, normalize, read_jsonl
from contracts import depth_errors
from strategy_contracts import validate_registry
from strategic import advanced_sections, chunk_sources, write_strategic_outputs

CATEGORIES = {
    "contexto_recuperacao": "Contexto, compressão e recuperação",
    "memoria": "Memória, persistência e conhecimento",
    "inferencia": "Inferência, atenção, GPU e cache",
    "orquestracao": "Orquestração, execução e resiliência",
    "verificacao_treinamento": "Verificação, treinamento e especialização",
    "continuidade_programacao": "Continuidade, programação e controle operacional",
    "referencias": "Pesquisas, projetos e tecnologias de referência",
    "componentes_propostos": "Componentes arquiteturais propostos",
}
STATUS = {
    "supported": "Conceito sustentado pelas fontes associadas",
    "related_support": "Padrão editorial apoiado em conceitos relacionados",
    "ambiguous": "Identificação ou definição com incerteza explícita",
    "terminology_correction": "Correção terminológica do inventário original",
}


def write(path: Path, text: str):
    atomic_bytes(path, text.encode("utf-8"))


def write_json(path: Path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def jsonl(rows):
    return "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)


def bullets(values):
    return "\n".join("- " + value for value in values)


def entry_sections(entry, cases=()):
    sections = [
        ("conceito", "Definição editorial de componente proposto" if entry.get("scope") == "proposta" else "Síntese conceitual com fontes associadas",
         entry["summary"] + "\n\nComo funciona:\n" + bullets(entry["mechanism"]) + ("\n\nNota de nomenclatura: " + entry["notes"] if entry.get("notes") else "")),
        ("aplicacao", "Cenários e proposta editorial de implementação; não executada",
         "Quando usar:\n" + bullets(entry["when_to_use"]) + "\n\nQuando não usar:\n" + bullets(entry["when_not_to_use"]) + "\n\nImplementação proposta:\n" + bullets(entry["implementation"]) + "\n\nAplicação LAI proposta:\n" + entry["lai_application"]),
        ("riscos_validacao", "Riscos e critérios de teste propostos; não são resultados medidos",
         "Armadilhas:\n" + bullets(entry["pitfalls"]) + "\n\nMétricas sugeridas:\n" + bullets(entry["metrics"]) + "\n\nTestes propostos:\n" + bullets(entry["validation"])),
        ("perguntas_proveniencia", "Perguntas de estudo e notas de proveniência editoriais",
         "\n\n".join("Pergunta: " + qa["question"] + "\nResposta: " + qa["answer"] for qa in entry["qa"]) + "\n\nEscopo das fontes:\n" + entry["source_notes"]),
    ]
    depth = entry["depth"]
    contract = depth["implementation_contract"]
    sections.extend([
        ("mecanismo_avancado", "Aprofundamento técnico com fontes; contrato proposto",
         depth["technical_details"] + "\n\nCondição de contorno:\n" + depth["boundary_condition"] +
         "\n\nContrato proposto:\n" + bullets(["Entradas: " + contract["inputs"], "Saídas: " + contract["outputs"], "Estado: " + contract["state"], "Invariante: " + contract["invariant"]]) +
         "\n\nCompromissos de projeto:\n" + bullets(depth["tradeoffs"])),
        ("experimento_comparacao", "Comparação e experimento propostos; afirmação rastreável e limites",
         "Falha a injetar e resultado esperado — proposta:\n" + depth["failure_test"] +
         "\n\nPlano de avaliação proposto:\n" + depth["evaluation_plan"] +
         "\n\nComparações:\n" + bullets([f"{c['entry_id']} ({c['relation']}): {c['reason']}" for c in depth["comparisons"]]) +
         "\n\nAfirmação rastreável:\n" + depth["evidence_claim"]["claim"] +
         "\nSuporte: " + depth["evidence_claim"]["support"] + "; fontes: " + ", ".join(depth["evidence_claim"]["source_ids"]) +
         "\nLimite: " + depth["evidence_claim"]["caveat"] + "\n\nNota de pesquisa:\n" + depth["research_note"]),
    ])
    sections.extend(advanced_sections(entry,cases))
    assert tuple(section for section, _, _ in sections) == SECTION_ORDER
    return sections


def render_markdown(entry, sources, chunks):
    text = f"# {entry['id']} — {entry['name']}\n\n"
    text += f"**Nome canônico:** {entry['canonical_name']}  \n**Grupo:** {CATEGORIES[entry['category']]}  \n**Escopo:** {entry['scope']}  \n**Natureza:** {entry['kind']}  \n**Estado da evidência:** {STATUS[entry['evidence_status']]}  \n**ID canônico:** {entry['canonical_id']}  \n**Data da curadoria:** 2026-11-05\n\n"
    if entry.get("aliases"):
        text += "**Nomes de busca:** " + "; ".join(entry["aliases"]) + "\n\n"
    for chunk in chunks:
        text += f"## {chunk['chunk_id']} — {chunk['section']}\n\n{chunk['text']}\n\n"
    text += "## Relações\n\n" + (", ".join(entry["relationships"]) or "Nenhuma relação editorial registrada.") + "\n\n"
    text += "## Fontes primárias associadas\n\n"
    for sid in entry["source_ids"]:
        source = sources[sid]
        text += f"### {sid} — {source['title']}\n\n[{source['url']}]({source['url']})\n\n"
        text += f"Consulta: {source['checked_on']}; estado: `{source['verification']}`.\n\nSustenta: {source['supports']}\n\nLimite: {source['limitations']}\n\n"
    text += "As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.\n"
    return text


def render_html(entries, sources, cases):
    esc = html.escape
    cards = []
    for entry in entries:
        sections = []
        for name, role, text in entry_sections(entry,cases):
            sections.append(f"<section><h3>{esc(name.replace('_',' ').capitalize())}</h3><p class='role'>{esc(role)}</p><div class='prose'>{esc(text)}</div></section>")
        source_html = "".join(f"<li><a href='{esc(sources[sid]['url'], quote=True)}' target='_blank' rel='noopener noreferrer'>{esc(sid + ' — ' + sources[sid]['title'])}</a><span> {esc(sources[sid]['verification'])}</span></li>" for sid in entry["source_ids"])
        searchable = normalize(" ".join([entry["id"], entry["name"], entry["canonical_name"], *entry["aliases"], entry["summary"]]))
        cards.append(f"<details id='{entry['id']}' data-category='{entry['category']}' data-search='{esc(searchable, quote=True)}'><summary><span class='tag'>{entry['id']}</span><strong>{esc(entry['name'])}</strong><span class='kind'>{esc(entry['kind'])}</span></summary><div class='inside'><p class='canonical'>Nome canônico: {esc(entry['canonical_name'])} · {esc(entry['canonical_id'])}</p><p class='state'>{esc(STATUS[entry['evidence_status']])}</p>{''.join(sections)}<section><h3>Fontes</h3><ul>{source_html}</ul><p>Relações: {esc(', '.join(entry['relationships']))}</p></section></div></details>")
    options = "".join(f"<option value='{key}'>{esc(label)}</option>" for key, label in CATEGORIES.items())
    document = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>LAI · __BASE_COUNT__ bases de conhecimento</title>
<style>
:root{color-scheme:light;--ink:#132337;--muted:#546575;--line:#d6dde2;--accent:#11605c;--paper:#f5f4ee}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.55}header{background:var(--ink);color:white;padding:44px max(5vw,20px) 32px}header p{max-width:840px;color:#cedde5}.eyebrow{font-size:12px;letter-spacing:2px;color:#a8d9cd}h1{font-size:clamp(28px,5vw,48px);line-height:1.12;margin:12px 0}.stats{display:flex;gap:24px;flex-wrap:wrap;color:#c7ddd7;font-size:14px}main{max-width:1120px;margin:auto;padding:24px 20px 70px}.tools{position:sticky;top:0;background:var(--paper);padding:16px 0;display:grid;grid-template-columns:1.8fr 1fr;gap:12px;z-index:2}label{font-size:12px;font-weight:700;display:block}input,select{width:100%;padding:12px;border:1px solid #b8c4ca;border-radius:7px;background:white;color:var(--ink);font:inherit;font-size:15px}#count{color:var(--muted);font-size:14px}.note{border-left:3px solid var(--accent);padding:8px 14px;margin:0 0 20px;background:#e8eeea;font-size:14px}details{background:#fff;border:1px solid var(--line);border-radius:8px;margin:10px 0;overflow:hidden}summary{display:flex;align-items:center;gap:12px;padding:16px;cursor:pointer;list-style:none}summary:before{content:'+';font-size:20px;color:var(--accent)}details[open]>summary:before{content:'−'}summary strong{flex:1}.tag{font:12px ui-monospace,monospace;color:var(--accent);background:#e8f0eb;border-radius:5px;padding:3px 6px}.kind{font-size:11px;color:var(--muted)}.inside{padding:0 24px 24px;border-top:1px solid var(--line)}.canonical,.state{font-size:13px;color:var(--muted)}section{border-top:1px solid #e6ebed;margin-top:20px;padding-top:2px}h3{font-size:16px;margin:16px 0 4px}.role{font-size:12px;color:var(--muted)}.prose{white-space:pre-wrap;font-size:15px}a{color:#0b625b;overflow-wrap:anywhere}li{margin-bottom:8px;font-size:14px}li span{font-size:11px;color:var(--muted)}footer{font-size:12px;color:var(--muted);margin-top:32px}@media(max-width:650px){.tools{grid-template-columns:1fr}summary{gap:8px;padding:12px}.kind{display:none}.inside{padding:0 15px 20px}}
</style></head><body>
<header><div class="eyebrow">LAI · MEMÓRIA TÉCNICA CONSULTÁVEL</div><h1>__BASE_COUNT__ bases.<br>Conhecimento com origem.</h1><p>__TECH_COUNT__ entradas do inventário, __REF_COUNT__ referências e __PROPOSAL_COUNT__ componentes propostos. Referências e propostas ficam fora da contagem principal. Abra um item para estudar conceito, aplicação, limites, testes propostos e fontes. Este catálogo funciona localmente.</p><div class="stats"><span>__BASE_COUNT__ namespaces</span><span>__CHUNKS_COUNT__ trechos recuperáveis</span><span>05 nov 2026 · v__VERSION__</span></div></header>
<main><div class="tools"><label>BUSCAR NO CATÁLOGO<input id="q" type="search" placeholder="Nome, ID, alias ou conceito…" autocomplete="off"></label><label>GRUPO<select id="category"><option value="">Todos os grupos</option>__OPTIONS__</select></label></div><p id="count" aria-live="polite"></p><p class="note">Consulta visual por termos. Para busca BM25, contexto com citações e integração com modelo, veja README.md. O pacote contém conhecimento sobre as técnicas; não instala automaticamente essas capacidades na Helena.</p><div id="entries">__CARDS__</div><footer>Fontes e propostas editoriais são identificadas. Pontuações de recuperação não medem verdade. As URLs externas abrem somente quando você clica.</footer></main>
<script>
const q=document.querySelector('#q'),category=document.querySelector('#category'),cards=[...document.querySelectorAll('details')];
const norm=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
function filter(){const words=norm(q.value).split(' ').filter(Boolean);let shown=0;for(const card of cards){const ok=(!category.value||category.value===card.dataset.category)&&words.every(w=>card.dataset.search.includes(w));card.hidden=!ok;if(ok)shown++;}document.querySelector('#count').textContent=shown+' de '+cards.length+' itens';}
q.addEventListener('input',filter);category.addEventListener('change',filter);filter();
if(location.hash){const target=document.getElementById(location.hash.slice(1));if(target&&target.tagName==='DETAILS'){target.open=true;target.scrollIntoView();}}
</script></body></html>"""
    scopes = Counter(entry["scope"] for entry in entries)
    return (document.replace("__OPTIONS__", options).replace("__CARDS__", "\n".join(cards))
            .replace("__BASE_COUNT__", str(len(entries))).replace("__CHUNKS_COUNT__", str(len(SECTION_ORDER)*len(entries)))
            .replace("__TECH_COUNT__", str(scopes["inventario"])).replace("__REF_COUNT__", str(scopes["referencia"]))
            .replace("__PROPOSAL_COUNT__", str(scopes["proposta"])).replace("__VERSION__", VERSION))


def build(root=DEFAULT_ROOT):
    root = Path(root).resolve()
    entries = read_jsonl(root / "corpus/entries.jsonl")
    source_rows = read_jsonl(root / "fontes/sources.jsonl")
    sources = {s["source_id"]: s for s in source_rows}
    cases = read_jsonl(root / "producao/casos.jsonl")
    searches = read_jsonl(root / "pesquisa/CONSULTAS_V4.jsonl")
    original = json.loads((root / "catalogo/inventario_original.json").read_text(encoding="utf-8"))
    scope_by_prefix = {"T": "inventario", "R": "referencia", "P": "proposta"}
    # Preflight completo de identidade antes de gerar qualquer arquivo.
    for label, rows in [("inventário", original), ("corpus", entries)]:
        seen = set()
        for row in rows:
            eid = row.get("id")
            if not isinstance(eid, str) or not re.fullmatch(r"[TRP][0-9]{3}", eid):
                raise ValueError(f"ID inválido no {label}: {eid!r}")
            if eid in seen:
                raise ValueError(f"ID duplicado no {label}: {eid}")
            seen.add(eid)
            if row.get("scope") != scope_by_prefix[eid[0]]:
                raise ValueError(f"Escopo incompatível com prefixo: {eid}")
            if row.get("category") not in CATEGORIES:
                raise ValueError(f"Categoria inválida: {eid}")
    expected = {item["id"]: item["name"] for item in original}
    if len(entries) != len(original) or {e["id"] for e in entries} != set(expected):
        raise ValueError("O corpus precisa preservar todos os IDs do inventário versionado")
    inventory_by_id = {item["id"]: item for item in original}
    if len(sources) != len(source_rows):
        raise ValueError("ID de fonte duplicado")
    for entry in entries:
        eid = entry["id"]
        if any(entry.get(key) != inventory_by_id[eid].get(key) for key in ["name", "category", "scope"]):
            raise ValueError("Metadados diferem do inventário: " + eid)
        if entry.get("canonical_id") not in expected or set(entry.get("relationships", [])) - set(expected):
            raise ValueError("Referência interna inválida: " + eid)
        if not entry.get("source_ids") or set(entry["source_ids"]) - set(sources):
            raise ValueError("Fonte ausente: " + eid)
        if entry.get("scope") == "proposta" and entry.get("evidence_status") != "related_support":
            raise ValueError("Proposta precisa de classificação editorial: " + eid)
        research_errors = depth_errors(entry, set(expected), set(sources))
        if research_errors:
            raise ValueError("Aprofundamento inválido: " + "; ".join(research_errors))
        try:
            entry_sections(entry,cases)
        except (KeyError, TypeError) as exc:
            raise ValueError("Aprofundamento incompleto ou inválido: " + eid) from exc
    strategic_errors=validate_registry(entries,source_rows,cases,searches)
    if strategic_errors:
        raise ValueError("Camada estratégica inválida: "+"; ".join(strategic_errors))
    output_dirs = [root / name for name in ["bases", "corpus", "fontes", "catalogo", "exports", "indexes", "pesquisa", "grafos", "producao"]]
    output_dirs.extend(root / "bases" / eid for eid in expected)
    if any(not path.resolve().is_relative_to(root) for path in output_dirs):
        raise ValueError("Destino de geração fora da pasta do pacote")
    if (root / "bases").exists():
        stale = [path.name for path in (root / "bases").iterdir() if path.is_dir() and path.name not in expected]
        if stale:
            raise ValueError("Pastas antigas ou desconhecidas em bases/: " + ", ".join(sorted(stale)) + ". Preserve-as fora de bases/ antes de reconstruir.")
    chunks = []
    inventory = []
    all_qa = []
    category_text = {key: "# " + title + "\n\nExportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.\n\n" for key, title in CATEGORIES.items()}
    for entry in entries:
        if entry["name"] != expected[entry["id"]]:
            raise ValueError("Nome original alterado: " + entry["id"])
        directory = f"bases/{entry['id']}"
        per_entry = []
        for number, (section, role, text) in enumerate(entry_sections(entry,cases), 1):
            chunk = {
                "chunk_id": f"{entry['id']}:C{number:02}", "entry_id": entry["id"],
                "namespace": entry["id"], "name": entry["name"], "canonical_name": entry["canonical_name"],
                "canonical_id": entry["canonical_id"], "aliases": entry["aliases"],
                "category": entry["category"], "kind": entry["kind"], "scope": entry["scope"], "section": section,
                "text": text, "source_ids": chunk_sources(entry,number,cases), "content_role": role,
                "evidence_status": entry["evidence_status"], "language": "pt-BR", "knowledge_version": VERSION,
                "curated_on": "2026-11-05", "document_path": directory + "/knowledge.md",
            }
            per_entry.append(chunk)
        chunks.extend(per_entry)
        metadata = {k: entry[k] for k in ["id", "name", "canonical_name", "canonical_id", "aliases", "category", "kind", "scope", "evidence_status", "relationships", "source_ids"]}
        metadata.update(namespace=entry["id"], knowledge_version=VERSION, curated_on="2026-11-05", directory=directory, chunk_count=len(per_entry))
        inventory.append(metadata)
        target = root / directory
        markdown = render_markdown(entry, sources, per_entry)
        write(target / "knowledge.md", markdown)
        category_text[entry["category"]] += "\n\n---\n\n" + markdown
        write_json(target / "metadata.json", metadata)
        write_json(target / "sources.json", [sources[sid] for sid in entry["source_ids"]])
        write_json(target / "qa.json", entry["qa"])
        write_json(target / "research.json", entry["depth"])
        write(target / "chunks.jsonl", jsonl(per_entry))
        for index, qa in enumerate(entry["qa"], 1):
            all_qa.append({"qa_id": f"{entry['id']}:Q{index:02}", "entry_id": entry["id"], **qa, "purpose": "estudo; não benchmark independente", "source_ids": entry["source_ids"]})
    write(root / "corpus/chunks.jsonl", jsonl(chunks))
    write(root / "corpus/qa.jsonl", jsonl(all_qa))
    write_json(root / "catalogo/catalogo.json", inventory)
    relations = [{"from": e["id"], "to": related, "relation": "related_editorially"} for e in entries for related in e["relationships"]]
    relations += [{"from": e["id"], "to": e["canonical_id"], "relation": "canonical_alias"} for e in entries if e["id"] != e["canonical_id"]]
    write_json(root / "catalogo/relacoes.json", {"nodes": [{"id":e["id"],"name":e["name"]} for e in entries], "edges": relations, "note": "Associações editoriais; não constituem grafo causal nem dependências obrigatórias."})
    detailed = [{"from": e["id"], "to": c["entry_id"], "relation": c["relation"], "reason": c["reason"], "source_ids": e["depth"]["source_ids"]} for e in entries for c in e["depth"]["comparisons"]]
    write_json(root / "catalogo/relacoes_detalhadas.json", {"edges": detailed, "note": "Relações editoriais tipadas. requires expressa dependência proposta no escopo descrito; nenhuma aresta comprova implantação."})
    write(root / "pesquisa/AFIRMACOES_RASTREAVEIS.jsonl", jsonl([{"entry_id":e["id"], **e["depth"]["evidence_claim"]} for e in entries]))
    write(root / "pesquisa/PROTOCOLOS_AVALIACAO.jsonl", jsonl([{"entry_id": e["id"], "failure_test": e["depth"]["failure_test"], "evaluation_plan": e["depth"]["evaluation_plan"], "status": "proposto; não executado"} for e in entries]))
    (root / "exports").mkdir(exist_ok=True)
    for category, text in category_text.items():
        write(root / "exports" / ("conhecimento_" + category + ".md"), text)
    with (root / "exports/chunks.csv").open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["chunk_id", "entry_id", "scope", "category", "name", "section", "text", "source_ids", "document_path"])
        writer.writeheader()
        for chunk in chunks:
            row = {key: chunk[key] for key in writer.fieldnames}
            row["source_ids"] = json.dumps(row["source_ids"], ensure_ascii=False)
            writer.writerow(row)
    with (root / "catalogo/catalogo.csv").open("w", encoding="utf-8-sig", newline="") as out:
        fields = ["id", "name", "canonical_name", "canonical_id", "scope", "category", "kind", "evidence_status", "directory"]
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: row[key] for key in fields} for row in inventory)
    with (root / "exports/comparacoes.csv").open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["from", "to", "relation", "reason", "source_ids"])
        writer.writeheader()
        writer.writerows({**row, "source_ids": json.dumps(row["source_ids"])} for row in detailed)
    write(root / "ABRIR_CATALOGO.html", render_html(entries, sources,cases))
    strategic_stats=write_strategic_outputs(root,entries,sources,cases,searches,write,write_json,jsonl)
    new_text="# Novas estratégias v4 — somente acréscimos\n\nC07–C09 de cada base. Os conceitos anteriores permanecem em knowledge.md.\n\n"
    for entry in entries:
        new_text+=f"## {entry['id']} — {entry['name']}\n\n"
        for name,role,text in advanced_sections(entry,cases):
            new_text+=f"### {name}\n\n{role}\n\n{text}\n\n"
    write(root/"exports/NOVAS_ESTRATEGIAS.md",new_text)
    table = f"# Índice das {len(entries)} bases\n\nEntradas T pertencem ao inventário principal; R são referências e P são propostas arquiteturais.\n\n| ID | Entrada | Grupo | Natureza |\n|---|---|---|---|\n"
    for entry, item in zip(entries, inventory, strict=True):
        table += f"| {entry['id']} | [{entry['name']}](../{item['directory']}/knowledge.md) | {CATEGORIES[entry['category']]} | {entry['kind']} |\n"
    write(root / "catalogo/INDICE.md", table)
    corrections = "# Taxonomia e equivalências\n\nOs IDs T001–T206 foram preservados e T207–T243 foram acrescentados. R e P ficam fora da contagem de 243. IDs canônicos indicam equivalência editorial; relações indicam proximidade, não identidade. T069 agora define consolidação externa por resumos; a destilação paramétrica permanece em T179.\n\n| ID | Nome atual | Nome canônico | Referência canônica | Nota |\n|---|---|---|---|---|\n"
    for entry in entries:
        if entry["id"] != entry["canonical_id"] or entry.get("notes") or entry["evidence_status"] in {"ambiguous", "terminology_correction"}:
            note = entry.get("notes") or STATUS[entry["evidence_status"]]
            corrections += f"| {entry['id']} | {entry['name']} | {entry['canonical_name']} | {entry['canonical_id']} | {note.replace('|', '/')} |\n"
    write(root / "CORRECOES_DE_TAXONOMIA.md", corrections)
    bibliography = "# Registro de fontes\n\n`opened`: conteúdo aberto pela ferramenta. `search_result`: resultado de busca examinado, sem abertura integral confirmada. `unverified`: referência ainda não confirmada. Consulta em 2026-11-05. Isso não é uma auditoria de cada afirmação nem um espelho integral dos sites.\n\n"
    for source in source_rows:
        bibliography += f"## {source['source_id']} — {source['title']}\n\n[{source['url']}]({source['url']})\n\n**Origem:** {source['publisher']}; **tipo:** {source['source_type']}; **consulta:** {source['verification']}.\n\n**Suporte:** {source['supports']}\n\n**Limites:** {source['limitations']}\n\n"
    write(root / "fontes/REFERENCIAS.md", bibliography)
    stats = {"entries": len(entries), "chunks": len(chunks), "qa": len(all_qa), "source_records": len(source_rows), "unique_source_urls": len({s["url"] for s in source_rows}), "entries_by_scope": dict(Counter(e["scope"] for e in entries)), "categories": dict(Counter(e["category"] for e in entries)), "evidence_status": dict(Counter(e["evidence_status"] for e in entries)), "source_verification": dict(Counter(s["verification"] for s in source_rows)), "canonical_ids": len({e["canonical_id"] for e in entries}), "words_editorial": sum(len(" ".join(text for _,_,text in entry_sections(e,cases)).split()) for e in entries), "words_new_layers":sum(len(" ".join(text for _,_,text in advanced_sections(e,cases)).split()) for e in entries), "deepened_entries": sum(bool(e.get("depth")) for e in entries), "typed_relations": len(detailed), "traceable_claims": len(entries), "proposed_experiment_protocols": len(entries),"strategic_entries":sum(bool(e.get('strategy')) for e in entries),"advanced_uses":sum(len(e['strategy']['advanced_uses']) for e in entries),**strategic_stats}
    technical = [e for e in entries if e["scope"] == "inventario"]
    write_json(root / "catalogo/inventario_243.json", [{"number": int(e["id"][1:]), "id": e["id"], "name": e["name"], "category": e["category"], "kind": e["kind"], "canonical_id": e["canonical_id"], "aliases": e["aliases"]} for e in technical])
    listing = f"# Lista completa atualizada — {len(technical)} entradas\n\n206 entradas anteriores + 37 acréscimos. IDs anteriores preservados. São itens de um inventário, não tecnologias independentes: há técnicas, variantes, componentes e formatos.\n\n"
    for category, label in CATEGORIES.items():
        group = [e for e in entries if e["category"] == category]
        listing += f"## {label} — {len(group)}\n\n"
        if category in {"referencias", "componentes_propostos"}:
            listing += "Fora da contagem de 243 entradas principais.\n\n"
            listing += "\n".join(f"- **{e['id']}** — {e['name']}" for e in group) + "\n\n"
        else:
            listing += "\n".join(f"{int(e['id'][1:])}. {e['name']}" for e in group) + "\n\n"
        if category == "memoria":
            listing += "**Correção T069:** consolidar sessões em um resumo externo não é destilar contexto nos pesos. A destilação paramétrica permanece em T179.\n\n"
    write(root / "LISTA_COMPLETA_243.md", listing)
    write_json(root / "catalogo/estatisticas.json", stats)
    index_stats = build_index(root)
    print(json.dumps({**stats, "index": index_stats}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
