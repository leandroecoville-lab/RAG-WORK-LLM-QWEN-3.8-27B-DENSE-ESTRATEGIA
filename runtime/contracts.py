"""Validação compartilhada do aprofundamento editorial de uma entrada RAG.

Não altera a entrada e não faz IO. Estruturas JSON malformadas são reportadas
como mensagens, para que o builder e o validador apliquem o mesmo contrato.
"""
from __future__ import annotations

import re


_ID_RE = re.compile(r"[TRP][0-9]{3}\Z")
_DEPTH_FIELDS = frozenset({
    "id", "technical_details", "boundary_condition", "implementation_contract",
    "tradeoffs", "failure_test", "evaluation_plan", "comparisons",
    "evidence_claim", "advanced_qa", "source_ids", "research_note",
})
_CONTRACT_FIELDS = frozenset({"inputs", "outputs", "state", "invariant"})
_COMPARISON_FIELDS = frozenset({"entry_id", "relation", "reason"})
_CLAIM_FIELDS = frozenset({"claim", "source_ids", "support", "caveat"})
_QA_FIELDS = frozenset({"question", "answer"})
_RELATIONS = frozenset({
    "complements", "alternative", "specializes", "distinct_from", "requires",
})
_SUPPORTS = frozenset({"direct", "related"})


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def depth_errors(
    entry: object,
    entry_ids: set[str] | dict[str, object],
    source_ids: set[str] | dict[str, object],
) -> list[str]:
    """Retorna violações estruturais e de referência, sem lançar por JSON inválido.

    ``entry_ids`` e ``source_ids`` podem ser conjuntos ou dicionários indexados
    pelo ID; seus valores não são examinados. O contrato verifica forma e
    consistência editorial, sem avaliar a veracidade do conteúdo das fontes.
    """
    if not isinstance(entry, dict):
        return ["?: entrada precisa ser um objeto JSON para validar depth"]

    eid = entry.get("id")
    label = eid if _nonempty_string(eid) else "?"
    errors: list[str] = []

    def error(path: str, message: str) -> None:
        errors.append(f"{label}: {path} {message}")

    def registry(value: object, path: str) -> set[str]:
        if not isinstance(value, (set, frozenset, dict)):
            error(path, "precisa ser um conjunto ou dicionário de IDs")
            return set()
        valid = {item for item in value if _nonempty_string(item)}
        if len(valid) != len(value):
            error(path, "contém ID que não é uma string não vazia")
        return valid

    def object_fields(value: object, fields: frozenset[str], path: str) -> bool:
        if not isinstance(value, dict):
            error(path, "precisa ser um objeto JSON")
            return False
        missing = fields - value.keys()
        extra = value.keys() - fields
        if missing:
            error(path, "tem campos ausentes: " + ", ".join(sorted(missing)))
        if extra:
            error(path, "tem campos desconhecidos: " + ", ".join(sorted(repr(k) for k in extra)))
        return True

    def text(value: object, path: str) -> None:
        if not _nonempty_string(value):
            error(path, "precisa ser uma string não vazia")

    def id_list(value: object, path: str) -> set[str]:
        if not isinstance(value, list):
            error(path, "precisa ser uma lista de IDs não vazia")
            return set()
        if not value:
            error(path, "precisa conter ao menos um ID")
        valid: set[str] = set()
        for index, item in enumerate(value):
            if not _nonempty_string(item):
                error(f"{path}[{index}]", "precisa ser uma string não vazia")
            elif item in valid:
                error(path, "contém ID duplicado: " + item)
            else:
                valid.add(item)
        return valid

    known_entries = registry(entry_ids, "entry_ids")
    known_sources = registry(source_ids, "source_ids")
    if not isinstance(eid, str) or not _ID_RE.fullmatch(eid):
        error("id", "precisa ter formato T001, R001 ou P001")
    elif eid not in known_entries:
        error("id", "não existe no inventário recebido")

    depth = entry.get("depth")
    if not object_fields(depth, _DEPTH_FIELDS, "depth"):
        return errors

    depth_id = depth.get("id")
    if not isinstance(depth_id, str) or not _ID_RE.fullmatch(depth_id):
        error("depth.id", "precisa ter formato T001, R001 ou P001")
    elif depth_id != eid:
        error("depth.id", "difere do ID da entrada")

    for field in (
        "technical_details", "boundary_condition", "failure_test",
        "evaluation_plan", "research_note",
    ):
        text(depth.get(field), "depth." + field)

    contract = depth.get("implementation_contract")
    if object_fields(contract, _CONTRACT_FIELDS, "depth.implementation_contract"):
        for field in sorted(_CONTRACT_FIELDS):
            text(contract.get(field), "depth.implementation_contract." + field)

    tradeoffs = depth.get("tradeoffs")
    if not isinstance(tradeoffs, list):
        error("depth.tradeoffs", "precisa ser uma lista com ao menos dois textos")
    else:
        if len(tradeoffs) < 2:
            error("depth.tradeoffs", "precisa conter ao menos dois textos")
        for index, tradeoff in enumerate(tradeoffs):
            text(tradeoff, f"depth.tradeoffs[{index}]")

    comparisons = depth.get("comparisons")
    if not isinstance(comparisons, list):
        error("depth.comparisons", "precisa ser uma lista com uma a três comparações")
    else:
        if not 1 <= len(comparisons) <= 3:
            error("depth.comparisons", "precisa conter uma a três comparações")
        for index, comparison in enumerate(comparisons):
            path = f"depth.comparisons[{index}]"
            if not object_fields(comparison, _COMPARISON_FIELDS, path):
                continue
            target = comparison.get("entry_id")
            if not isinstance(target, str) or not _ID_RE.fullmatch(target):
                error(path + ".entry_id", "precisa ser um ID válido")
            elif target == eid:
                error(path + ".entry_id", "não pode apontar para a própria entrada")
            elif target not in known_entries:
                error(path + ".entry_id", "não existe no inventário recebido")
            relation = comparison.get("relation")
            if not isinstance(relation, str) or relation not in _RELATIONS:
                error(path + ".relation", "não pertence às relações permitidas")
            text(comparison.get("reason"), path + ".reason")

    entry_sources = id_list(entry.get("source_ids"), "entry.source_ids")
    depth_sources = id_list(depth.get("source_ids"), "depth.source_ids")
    if entry_sources - known_sources:
        error("entry.source_ids", "contém fonte ausente do registro: " + ", ".join(sorted(entry_sources - known_sources)))
    if depth_sources - entry_sources:
        error("depth.source_ids", "contém fonte não vinculada à entrada: " + ", ".join(sorted(depth_sources - entry_sources)))
    if depth_sources - known_sources:
        error("depth.source_ids", "contém fonte ausente do registro: " + ", ".join(sorted(depth_sources - known_sources)))

    claim = depth.get("evidence_claim")
    if object_fields(claim, _CLAIM_FIELDS, "depth.evidence_claim"):
        text(claim.get("claim"), "depth.evidence_claim.claim")
        text(claim.get("caveat"), "depth.evidence_claim.caveat")
        claim_sources = id_list(claim.get("source_ids"), "depth.evidence_claim.source_ids")
        if claim_sources - depth_sources:
            error("depth.evidence_claim.source_ids", "contém fonte não vinculada ao aprofundamento: " + ", ".join(sorted(claim_sources - depth_sources)))
        support = claim.get("support")
        if not isinstance(support, str) or support not in _SUPPORTS:
            error("depth.evidence_claim.support", "precisa ser direct ou related")
        if ((isinstance(eid, str) and eid.startswith("P")) or entry.get("scope") == "proposta") and support != "related":
            error("depth.evidence_claim.support", "precisa ser related para propostas P")

    advanced_qa = depth.get("advanced_qa")
    if not isinstance(advanced_qa, list):
        error("depth.advanced_qa", "precisa ser uma lista com duas perguntas e respostas")
    else:
        if len(advanced_qa) != 2:
            error("depth.advanced_qa", "precisa conter exatamente duas perguntas e respostas")
        for index, qa in enumerate(advanced_qa):
            path = f"depth.advanced_qa[{index}]"
            if object_fields(qa, _QA_FIELDS, path):
                text(qa.get("question"), path + ".question")
                text(qa.get("answer"), path + ".answer")

    entry_qa = entry.get("qa")
    if not isinstance(entry_qa, list) or len(entry_qa) != 4:
        error("entry.qa", "precisa conter exatamente quatro perguntas e respostas")
    elif isinstance(advanced_qa, list) and advanced_qa != entry_qa[2:]:
        error("depth.advanced_qa", "difere das duas últimas perguntas e respostas de entry.qa")

    return errors
