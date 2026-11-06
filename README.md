# LAI RAG estratégico v4 — 287 bases, foco em LLMs de 3–30B

**243 entradas do inventário, 27 referências e 17 componentes propostos.** Cada base mantém seu ID e recebe estratégias novas, casos públicos classificados e conexões condicionais. Versão 4.0.0; curadoria em 5 de novembro de 2026.

## Comece pelo grafo

1. Extraia o ZIP e abra `ABRIR_GRAFO.html`.
2. Selecione o assunto. Veja como combinar, qual interface usar, quando a combinação é válida e como testar.
3. Filtre produção documentada, produto disponível ou proposta. Veja também a correspondência exata, de família ou por analogia de cada caso.
4. Leia `GUIA_ESTRATEGICO_3_30B.md` para arquitetura, especialização, memória, serving e comparação com fronteira.
5. Para somente os acréscimos, abra `NOVO_NESTA_VERSAO.md` e `exports/NOVAS_ESTRATEGIAS.md`.

`ABRIR_CATALOGO.html` contém todas as fichas. Os HTMLs funcionam localmente sem CDN ou servidor. Links de fontes abrem páginas externas quando clicados.

## O que foi entregue e o que foi medido

- **287 bases individuais**, **2.583 chunks** (C01–C09) e **1.148 perguntas de estudo**.
- C07: estratégias e usos avançados, com adequação específica a 3–7B, 8–14B e 15–30B.
- C08: casos públicos, estágio da evidência, correspondência com o assunto e lacuna para dez exemplos.
- C09: conexões com ordem, interface, condição, aceite e controles de falha.
- Grafo interativo, grafos JSON, um Mermaid por base, registro de consultas e casos com fontes.
- Runtime local de busca e montagem de contexto; geração e embeddings são integrações opcionais explícitas.
- Comparador executável de observações reais de candidato e baseline, sem gerar benchmarks fictícios.

A meta de **dez exemplos de produção de Big Tech por base** não foi preenchida artificialmente. A contagem real e as lacunas estão em `producao/COBERTURA_10_POR_BASE.csv` e no relatório. Uma implantação pode apoiar vários temas, mas conta uma vez por base. Labs de IA e outros operadores são identificados separadamente. As propostas P não são produtos que empresas tenham adotado sob esses nomes.

Os resultados executados ficam em `RELATORIO_VALIDACAO.md` e `evidencias/`. Não houve inferência real de LLM, embeddings reais, benchmark GPU ou implantação na Helena. Não há demonstração de paridade geral com fronteira nem comprovação de que este seja o maior acervo mundial.

## Consulta local

Python 3.10 ou superior; biblioteca padrão, sem instalação de dependências. No Windows, use `py -3` ou `python` conforme sua instalação. Abra o terminal na pasta extraída `LAI_RAG_243_v4`.

```bash
python3 runtime/rag.py search "Como especializar um modelo pequeno?"
python3 runtime/rag.py search "Como reduzir erros de recuperação?" --id T009 --layer advanced
python3 runtime/rag.py context "Como combinar LoRA e verificação?" --layer new
python3 runtime/rag.py graph T182
python3 runtime/rag.py graph T140 --documented-only
python3 runtime/rag.py cases T079 --production-only --bigtech-only --exact-only
python3 runtime/rag.py inspect T243
```

`--layer all` consulta tudo; `base` consulta C01–C06; `advanced`, C07; `production`, C08; `connections`, C09; `new`, C07–C09. O filtro `production` seleciona a seção sobre evidências e inclui seus rótulos e lacunas; **não exclui automaticamente casos de produto ou pesquisa**. Para apenas implantações confirmadas use o comando `cases` e seus filtros.

Outros filtros: `--id T009`, `--category inferencia`, `--scope inventario|referencia|proposta|all`. Eles são combinados sem fallback silencioso. São organização de consulta, não autenticação de usuários ou isolamento de tenants.

A busca padrão usa BM25 com variantes lexicais e pontuação por entrada. `--lexical-profile exact` permite comparar termos exatos normalizados com o perfil padrão `expanded`. As pontuações ordenam documentos; não medem verdade ou confiança. Os parâmetros de recuperação foram mantidos da v3. As 130 consultas históricas são conhecidas e servem como regressão, não como nova reserva cega.

## Uma base por ID

| Arquivo em cada pasta `bases/ID/` | Função |
|---|---|
| `knowledge.md` | Ficha completa, conteúdo anterior e aprofundamento novo |
| `metadata.json` | Identidade, aliases, escopo e referências |
| `chunks.jsonl` | Nove trechos identificáveis e indexáveis |
| `sources.json` | Fontes e limitações |
| `qa.json` | Quatro perguntas de estudo |
| `research.json` | Aprofundamento anterior, contratos e protocolos propostos |
| `strategy.json` | Estratégias novas e adequação por porte |
| `production_cases.json` | Casos completos associados e cobertura da meta |
| `connections.json` | Conexões com contratos e estágio da evidência |
| `graph.mmd` | Grafo Mermaid das conexões desta base |

São namespaces documentais em um motor compartilhado. O pacote não cria 287 servidores nem implementa as 243 técnicas. Cada JSONL pode ser importado separadamente se a aplicação exigir coleções independentes.

T069 permanece consolidação externa por resumos; T179 é destilação paramétrica. T106 abrange MQA/GQA. R014 é equivalente editorial de R013. IDs P são propostas. A lista não apresenta 243 tecnologias independentes.

## Geração e embeddings opcionais

O comando `context` monta mensagens com citações e não chama uma LLM no modo lexical. O orçamento é de **caracteres dos documentos recuperados**, não de tokens do modelo. Pergunta, instruções e resposta também devem caber na janela. Trechos são inteiros: um bloco maior que o orçamento pode ficar de fora. Confira `selected_chunks` e `omitted_chunks`; para leitura documental completa, use a base.

Para gerar, forneça explicitamente um servidor compatível com `POST /chat/completions`:

```bash
python3 runtime/rag.py ask "Como usar T182 nesta tarefa?" --id T182 --layer new \
  --base-url http://127.0.0.1:8000/v1 --model NOME_EXATO_DO_MODELO
```

O endereço é ilustrativo; não há servidor incluído ou iniciado. Variáveis equivalentes: `RAG_LLM_BASE_URL`, `RAG_LLM_MODEL` e `RAG_LLM_API_KEY`. O comando envia a pergunta e trechos ao endpoint escolhido. Sem configuração, termina com erro; não escolhe um serviço externo.

Para embeddings opcionais:

```bash
python3 runtime/rag.py embed --base-url http://127.0.0.1:8001/v1 --model MODELO_DE_EMBEDDINGS
python3 runtime/rag.py search "reduzir custo sem perder evidência" --mode hybrid \
  --embedding-base-url http://127.0.0.1:8001/v1 --embedding-model MODELO_DE_EMBEDDINGS
```

`vector` usa cosseno; `hybrid` combina rankings por RRF. Não foram fornecidos vetores reais. O índice registra hash do corpus e identidade do endpoint/modelo; mudança de pesos sob o mesmo nome exige controle externo de versão.

A validação de citações detecta IDs inválidos, ausência de citação e término incompleto. **Não comprova sustentação semântica da resposta.** Consumidores devem aceitar somente `status=generated`, preservando os outros estados para revisão.

## Verificação e reconstrução

```bash
python3 runtime/rag.py validate
python3 runtime/rag.py verify
python3 runtime/rag.py evaluate --lexical-profile expanded
python3 runtime/build_corpus.py
python3 runtime/validate_release.py
python3 runtime/package_release.py
```

Reconstruir altera arquivos derivados e hashes; gere uma nova validação e pacote. Os dados editáveis são `corpus/entries.jsonl`, `fontes/sources.jsonl`, `producao/casos.jsonl` e `pesquisa/CONSULTAS_V4.jsonl`. Não edite apenas um export e espere que a mudança sobreviva à recompilação.

`runtime/compare_systems.py` recebe resultados reais coletados por você; seu contrato está em `avaliacao/COMPARAR_SISTEMAS.md`. O arquivo de configuração é um exemplo, não um experimento executado.

## Evidência e limites

`production_documented` registra implantação descrita na fonte; `operational_product`, recurso disponível sem comprovar implantação/escala específica; `research_only`, pesquisa. `exact`, `family` e `analogy` são relações diferentes. `engineering_proposal` não é resultado medido.

Fontes abertas, consultas executadas e limites são registrados. Não há cópia integral de todos os sites; a documentação pode mudar. Hashes comprovam integridade dos arquivos, não verdade factual. Veja `METODOLOGIA_E_LIMITES.md`, `producao/POLITICA_DE_EVIDENCIA.md` e o relatório final.

`pesquisa/REVISAO_FACTUAL_V4.md` registra a revisão documental dos 98 registros de casos, as correções e seus limites. As seis auditorias originais, seus insumos e os lotes congelados foram preservados. Para ingestão, use `corpus/chunks.jsonl`; versões históricas e cópias de auditoria não devem entrar como documentos adicionais do mesmo índice.

