# Relatório de validação — LAI RAG v2

## Resultado desta execução

- Bases: **287** — **243** entradas principais, **27** referências e **17** propostas arquiteturais.
- Trechos indexados: **1148**; perguntas de estudo: **574**.
- Texto editorial: aproximadamente **97,720 palavras**, contando os quatro blocos de cada ficha uma vez, sem exports e bibliografias duplicados.
- Fontes: **203 registros**, **188 URLs distintas**; estados de consulta em `fontes/sources.jsonl`.
- Integridade estrutural: **APROVADA**.
- Migração: **APROVADA**; todos os 218 IDs anteriores presentes, 69 bases acrescentadas, 30 nomes anteriores preservados como aliases.
- Testes do runtime: **33/33 aprovados**, sem chamadas externas.
- CLI: **4/4 casos aprovados**.
- Busca pelo nome atual, ID entre os três primeiros: **287/287**.
- Consultas descritivas, algum ID esperado entre os cinco primeiros: **84/90** (93.3%).
- MRR@10 descritivo: **0.7802**.
- HTML: **287 fichas**, verificação de IDs e JavaScript. Renderização visual em navegador não executada.

## Grupos da avaliação descritiva

| Grupo | Casos | Acertos nos 5 primeiros | Hit@5 | MRR@10 |
|---|---:|---:|---:|---:|
| baseline_v1_retestada | 48 | 46 | 95.8% | 0.7686 |
| escopos_revisados_v2 | 5 | 4 | 80.0% | 0.7000 |
| novos_itens_v2 | 37 | 34 | 91.9% | 0.8061 |

As 48 consultas anteriores foram retestadas no acervo ampliado. O caso Q13 teve seu conjunto esperado ajustado para retirar T069, cujo significado mudou por solicitação do usuário. Os 37 casos novos cobrem T207–T243; cinco casos adicionais cobrem escopos revisados. Os resultados históricos estão separados em `historico/`, não no índice atual.

## O que a validação demonstra

IDs, fontes, relações, namespaces e metadados são resolvíveis. Os testes verificam filtros por ID/categoria/escopo, isolamento de propostas, citações com prefixo P, aliases históricos, distinção canônica T069/T179, orçamento de contexto, índice desatualizado, contratos de vetores e respostas truncadas. A busca lexical foi executada sobre o corpus entregue.

Recuperação pelo nome mede endereçabilidade. As consultas descritivas são uma avaliação local elaborada para este pacote, separada das perguntas de estudo. Não são benchmark externo nem medida de compreensão de uma LLM. Hit@5 aceita um dos IDs relacionados previstos, não exige que todos apareçam. As consultas e seus rankings completos estão no JSON de evidências.

## Limites comprovadamente não cobertos

Não houve inferência real de LLM, produção de embeddings reais, medição do modo híbrido com modelos, instalação na Helena nem experimento de cada técnica. Clientes HTTP foram exercitados com respostas simuladas; isso valida contratos e tratamento de falhas, não certifica um servidor externo.

A checagem de citações verifica IDs fornecidos ao modelo, sem provar sustentação semântica das frases. Fontes bibliográficas têm estados de consulta explícitos e podem mudar. Os componentes P são propostas editoriais, sem alegação de produto implementado ou padrão universal.

## Ambiente e evidências

- Python: 3.12.14; plataforma: Linux-6.18.57-x86_64-with-glibc2.39.
- Dependências Python externas do runtime: nenhuma.
- Hash do corpus: `201e97a867ef3fbe9434c2a8c0b47f61247791b513980b78d93bded014c78207`.
- Validação: 2026-11-05T11:19:39.051874-03:00.

| Arquivo em evidencias/ | Conteúdo |
|---|---|
| `testes_runtime.log` / `testes_runtime.json` | Casos de teste, contagem e duração |
| `integridade_corpus.json` | Estrutura, fontes, IDs e metadados |
| `cobertura_migracao.json` | Preservação de IDs, aliases e escopos |
| `avaliacao_recuperacao.json` | Perguntas, IDs esperados, rankings, acertos e falhas |
| `catalogo_html.json` | Quantidade de fichas e sintaxe do script |
| `cli_smoke.json` | Execução efetiva de quatro comandos offline |

## Limitações observadas na recuperação

As consultas abaixo não recuperaram um ID esperado entre os cinco primeiros. Os erros permanecem registrados. Variação lexical e sobreposição entre fichas podem afetar o ranking; embeddings ou reranking precisam de avaliação antes de se afirmar melhoria.

- **Q14** — Organizar memória do agente em camadas e trazer detalhes apenas quando solicitados Esperados: T062, T063, R001; primeiros: T048, T002, R002, T014, T119.
- **Q24** — Distribuir tensores das mesmas camadas entre várias GPUs Esperados: T118; primeiros: T101, T119, T136, T109, T127.
- **Q50** — Separar o agente que planeja daquele que executa passos e retorna resultados Esperados: T208, T143; primeiros: R021, T237, T235, T144, R002.
- **Q71** — Modificar apenas os trechos necessários de um arquivo usando patches verificáveis Esperados: T229; primeiros: T238, T233, T053, T028, T073.
- **Q82** — Materializar uma imagem consistente do estado em determinado instante Esperados: T240; primeiros: T164, T148, T154, P007, T090.
- **Q90** — Qual componente proposto da LAI reuniria memória de trabalho episódios e procedimentos? Esperados: P004, P005; primeiros: P012, T070, T071, T062, T047.
