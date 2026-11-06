# Relatório de validação — LAI RAG 218

## Resultado desta execução

- Bases: **218** — 206 entradas originais e 12 referências.
- Trechos indexados: **872**.
- Perguntas de estudo: **436**.
- Texto editorial: **68,068 palavras** aproximadamente, contando os quatro blocos de cada ficha uma vez; exclui duplicações de exportação e bibliografias.
- Registros de fontes: **147**, correspondentes a **141 URLs distintas**.
- Integridade estrutural do corpus: **APROVADA**.
- Testes de runtime: **24/24 aprovados**, sem chamadas a modelos externos.
- Recuperação pelo nome original, presença do item nos três primeiros resultados: **218/218**.
- Consultas descritivas, presença de ao menos um ID esperado nos cinco primeiros resultados: **46/48** (95.8%).
- MRR@10 nas consultas descritivas: **0.7986**.
- Catálogo HTML: **218 cards**, IDs únicos, sem scripts remotos. Layout não foi validado por renderização em navegador.

## O que esses resultados demonstram

O corpus cobre todos os IDs esperados, suas referências internas são resolvíveis e o motor recupera os trechos no ambiente testado. Foram verificadas filtragem por namespace/categoria, normalização de acentos, orçamento de contexto, detecção de índice desatualizado, checagem estrutural de citações, contratos de embeddings e preservação do índice anterior quando uma geração de vetores falha.

O teste por nome demonstra endereçabilidade, não compreensão semântica. O conjunto descritivo contém perguntas elaboradas para este pacote, sem pretensão de representar toda a distribuição de perguntas futuras. Os resultados completos, inclusive erros, estão em `evidencias/avaliacao_recuperacao.json`.

## O que não foi comprovado

Não foi executada inferência real de Qwen, GPT ou outra LLM. Não foram produzidos embeddings reais nem medido o ganho do modo híbrido. Os clientes HTTP foram exercitados com respostas simuladas; isso verifica contratos e falhas, não compatibilidade integral com um servidor real. Também não foram instaladas técnicas na Helena nem executados os experimentos propostos nas 218 fichas.

A checagem de citações valida IDs fornecidos ao modelo. Não valida automaticamente a sustentação de cada frase pelas fontes. As fontes bibliográficas têm estados de consulta diferentes e podem mudar após a curadoria.

## Ambiente

- Python: 3.12.14.
- Plataforma: Linux-6.18.57-x86_64-with-glibc2.39.
- Dependências Python externas: nenhuma.
- Hash SHA-256 do corpus: `d5e9e25469580d4105d06e2654b9f9a1facdda540bb97cc00fc9375180601809`.
- Data e hora de validação: 2026-11-05T09:39:40.561330-03:00.

## Consulta das evidências

| Arquivo | Evidência |
|---|---|
| `testes_runtime.log` | Nome e resultado de cada teste |
| `testes_runtime.json` | Contagem, duração e escopo |
| `integridade_corpus.json` | IDs, chunks, fontes e erros estruturais |
| `avaliacao_recuperacao.json` | Cada pergunta, IDs esperados, ranking e métricas |
| `catalogo_html.json` | Presença dos 218 cards e ausência de scripts externos |

## Limitações observadas na recuperação

As consultas abaixo não colocaram um ID esperado entre os cinco primeiros. Isso pode resultar de variação lexical, sobreposição entre técnicas ou ordenação. O relatório preserva os resultados sem ocultar falhas. Embeddings ou reranking precisam de avaliação própria antes de se afirmar melhoria.

- Q14: Organizar memória do agente em camadas e trazer detalhes apenas quando solicitados Esperados: T062, T063, R001; encontrados primeiro: T048, T002, T014, T119, T145.
- Q24: Distribuir tensores das mesmas camadas entre várias GPUs Esperados: T118; encontrados primeiro: T101, T119, T127, T163, T136.
