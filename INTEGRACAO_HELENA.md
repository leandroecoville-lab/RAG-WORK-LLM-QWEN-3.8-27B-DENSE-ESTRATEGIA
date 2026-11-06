# Integração proposta com Helena ou outro agente

## Contrato mínimo

Exponha a recuperação como ferramenta de leitura. O agente fornece pergunta e, opcionalmente, ID ou categoria. O executor chama `Engine.search` ou `Engine.context` e devolve trechos com citações. Não é necessário iniciar 287 agentes.

Exemplo de chamada Python, executada com a pasta `runtime` no caminho de importação:

```python
from pathlib import Path
from rag import Engine

engine = Engine(Path("/caminho/para/LAI_RAG_243_v4"))
resultados = engine.search(
    "Como guardar estado da missão fora do contexto?",
    top_k=4,
    entry_id="T053",
)
contexto = engine.context(
    "Compare scratchpad, memória episódica e destilação",
    top_k=5,
    max_chars=16000,
)
```

Schema de entrada sugerido:

```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string", "minLength": 1, "maxLength": 20000},
    "entry_id": {"type": "string", "pattern": "^[TRP][0-9]{3}$"},
    "category": {"type": "string"},
    "scope": {"type": "string", "enum": ["all", "inventario", "referencia", "proposta"]},
    "top_k": {"type": "integer", "minimum": 1, "maximum": 10}
  },
  "required": ["query"],
  "additionalProperties": false
}
```

O host deve mapear somente os argumentos permitidos. A entrada do usuário não deve ser interpolada em comandos de shell. Prefira importar a classe ou passar argumentos em lista ao iniciar um processo.

## Resultado e citação

Use `chunk_id` para citar o trecho local e `source_ids` para localizar as fontes externas. Preserve `evidence_status` e `content_role` no contexto. Os critérios de teste contidos nas fichas são propostas, e não resultados de testes já realizados.

Na geração, aceite como concluída somente a resposta com `status=generated`; trate `generation_truncated`, `completion_unconfirmed` e `citation_check_failed` como resultados que exigem resolução. Uma citação com ID válido não equivale a prova de sustentação semântica.

Quando houver uma expressão imprecisa, preserve a correção. Exemplo: T069 agora significa consolidação externa por resumos e tem canonical_id T069. T179 continua sendo destilação paramétrica. A migração precisa atualizar o conteúdo e os vetores de T069; preservar o ponteiro canônico antigo para T179 restauraria a confusão corrigida pelo usuário.

## Fluxo proposto

1. A Helena identifica a pergunta e o objetivo da consulta.
2. Recupera os conceitos e verifica os nomes canônicos.
3. Lê requisitos, limitações e fontes das técnicas candidatas.
4. Formula um plano pequeno com critérios de aceite observáveis.
5. Executa somente ações autorizadas pela aplicação hospedeira.
6. Registra os resultados reais em um acervo de experiências separado.

Este corpus de estudo não deve receber automaticamente toda saída da LLM como fato. Quando surgirem resultados reais de testes, registre versão, configuração, entrada, métrica, evidência e condições de aplicabilidade. Depois decida se eles corrigem uma ficha, adicionam uma nota local ou sustentam um novo procedimento.

## Escolha de integração

| Objetivo | Integração suficiente |
|---|---|
| Consultar manualmente | Catálogo HTML |
| Acessar pelo executor local | `Engine.search` |
| Montar mensagens para o modelo já usado pela Helena | `Engine.context` |
| Gerar uma resposta por servidor compatível | Comando `ask` |
| Usar o banco vetorial existente | Importar `corpus/chunks.jsonl` com metadados |

O caminho de menor dependência é integrar primeiro a busca lexical, medir erros de recuperação com perguntas da LAI e então avaliar embeddings ou reranking. Isso é uma proposta de implantação, não resultado medido em seu servidor.

## Migração v1 → v2

Faça upsert de todos os 1.148 chunks por ID, atualizando texto, título, aliases, escopo, fontes e versão. Há 287 namespaces; 69 são novos em relação às 218 bases anteriores. Em um armazenamento com upsert, atualize os IDs reaproveitados sem apagá-los depois: isso poderia excluir os registros novos. Se usar coleções ou versões separadas, valide a nova carga, troque a referência ativa e só então descarte a coleção antiga identificada. Não duplique T069 como se fosse um conceito novo. Recrie embeddings porque o conteúdo e o hash do corpus mudaram. Consulte `catalogo/migracao_v1_v2.json` para caminhos e nomes anteriores.

## Migração v2 → v3

Faça upsert dos **1.722 chunks**, mantendo os mesmos 287 namespaces. C01–C04 conservam seus identificadores; C05–C06 são novos. Quatro perguntas didáticas por base substituem o conjunto de duas. Atualize `knowledge_version`, texto, fontes, escopo e metadados juntos. Recrie embeddings; o índice vetorial anterior tem outro hash de corpus e deve ser recusado.

Importe `research.json` como material de estudo e preserve a indicação de proposta nos contratos e experimentos. `pesquisa/AFIRMACOES_RASTREAVEIS.jsonl` permite expor a fonte de uma afirmação delimitada; não transforma a fonte em prova de toda a implementação sugerida. `exports/comparacoes.csv` contém relações tipadas, sem afirmar um grafo universal de dependências.

O parâmetro opcional `lexical_profile` aceita `expanded` e `exact`. O padrão é expandido. Não permita que campos arbitrários fornecidos pelo usuário sejam repassados ao processo executor ou à configuração de endpoints. As 90 consultas históricas são desenvolvimento; as 40 reservadas documentam a primeira rodada desta versão, mas já não serão inéditas em uma próxima otimização.

**Aceite sugerido para sua integração:** importar todos os IDs sem duplicatas; recuperar fontes e correções de nomenclatura; aplicar filtros em todas as etapas; testar perguntas reais separadas das QAs; avaliar respostas efetivamente geradas com o modelo escolhido; medir custo por tarefa aceita e executar o plano de rollback. Esses passos não foram realizados no servidor da Helena nesta entrega.

## Migração v3 → v4

Faça upsert dos **2.583 chunks** nos mesmos 287 namespaces. C01–C06 mantêm IDs; C07–C09 acrescentam estratégias, casos e conexões. Atualize fontes por seção e versão junto do texto; refaça embeddings. Preserve os campos de estágio da evidência e correspondência ao importar casos. Um registro `research_only` ou `family` não pode virar exemplo de produção por perda de metadados.

Use `corpus/chunks.jsonl` como conjunto canônico de ingestão. HTML, exports, lotes congelados e histórico repetem representações para leitura ou auditoria; indexar todas essas cópias aumentaria duplicação e distorceria a recuperação. Os lotes em `pesquisa/lotes_congelados/` preservam entradas anteriores à revisão factual e não substituem o corpus consolidado.

O parâmetro `layer` permite `all`, `base`, `advanced`, `production`, `connections` e `new`. Restrinja seu schema de ferramenta aos valores aceitos. `production` seleciona a seção que descreve evidências; essa seção também contém lacunas, produtos e pesquisas rotulados. Para uma lista estrita, use `production_coverage`/`cases_for_entry` e filtre `production_documented`, `exact` e a organização desejada.

Importe `grafos/conexoes.json` como recomendações condicionais. `engineering_proposal` não autoriza executar a ligação nem demonstra ganho. Uma aresta documentada pode corresponder apenas a produto disponível. O executor continua responsável por autorização, idempotência e confirmação dos efeitos.

As 130 consultas anteriores são regressão conhecida na v4. Para medir desempenho da integração, use tarefas novas e resultados reais do seu modelo. O programa `runtime/compare_systems.py` pode analisar observações pareadas; ele não executa a coleta nem certifica equivalência geral com fronteira.
