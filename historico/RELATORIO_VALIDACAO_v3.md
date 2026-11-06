# Validação — LAI RAG completo v3

## Entrega e escopo comprovado

- **287 bases:** 243 entradas do inventário, 27 referências e 17 propostas.
- **1722 chunks**, **1148 perguntas de estudo**, **287 aprofundamentos**.
- **338 registros de fontes**, **303 URLs distintas**.
- Aproximadamente **207,203 palavras editoriais**, contando os seis blocos de cada ficha uma vez; exports e bibliografias não são somados novamente.
- **41/41 testes aprovados**, cinco comandos da CLI conferidos e integridade estrutural aprovada.
- IDs, nomes, aliases, IDs canônicos e C01–C04 preservados. C05–C06 acrescentados a cada base.
- Catálogo com 287 fichas; estrutura e JavaScript verificados. Renderização visual em navegador não executada.

## Recuperação executada

| Conjunto e perfil | Casos | Acertos nos 5 primeiros | Hit@5 | MRR@10 | Nomes Hit@3 |
|---|---:|---:|---:|---:|---:|
| desenvolvimento_expandido | 90 | 87 | 96.7% | 0.8599 | 100.0% |
| desenvolvimento_exato | 90 | 84 | 93.3% | 0.8275 | 100.0% |
| reserva_expandida | 40 | 38 | 95.0% | 0.7863 | 100.0% |
| reserva_exata | 40 | 38 | 95.0% | 0.7360 | 100.0% |

O conjunto de desenvolvimento contém as 90 consultas históricas. O gabarito foi preservado nesta versão. A reserva possui 40 perguntas criadas e congeladas antes da mudança do ranking e da incorporação do aprofundamento; não foi usada para escolher parâmetros. É uma avaliação local elaborada nesta tarefa, não um benchmark externo nem prova estatística de generalização. Esta execução da reserva está marcada como **primeira_execucao**; a primeira execução permanece em `evidencias/primeira_reserva_v3.json`.

Hit@5 aceita algum dos IDs esperados entre os cinco primeiros; não exige todos, não avalia a resposta gerada e pode ser sensível a um gabarito incompleto em famílias sobrepostas. MRR@10 usa o inverso da posição do primeiro ID esperado e zero quando ele não aparece nos dez primeiros. Busca por nome mede endereçabilidade. Nenhuma dessas métricas mede verdade ou sucesso de implantação.

O perfil exato usa termos normalizados e bônus de título/alias. O expandido acrescenta variantes por proximidade de caracteres e a pontuação do documento pai. Essa combinação é uma heurística própria; não é tradução, lematização completa, reranking neural nem compreensão semântica. A comparação no mesmo corpus permite observar ganhos e perdas da política, sem atribuir automaticamente a mudança a um único componente.

## O que foi testado

Busca sem rede, filtros por ID/categoria/escopo, conflitos sem fallback, hashes e índices incompatíveis, estrutura de citações inclusive C05/C06, orçamento de contexto, migração, preservação de aliases, quatro QAs por base, preflight do compilador e clientes HTTP com respostas simuladas. Os testes de vetores usam valores artificiais para verificar contratos, não qualidade de embeddings.

## O que permanece proposto

Os 287 protocolos experimentais pertencem ao conteúdo de estudo. Não foram executados como experimentos de sistemas reais. Também não houve inferência real de LLM, embeddings reais, instalação na Helena ou benchmark de GPU. As 17 propostas P são componentes editoriais. Uma fonte associada a uma afirmação não certifica todas as decisões de engenharia da ficha.

## Reprodutibilidade

- Python: 3.12.14; dependências externas do runtime: nenhuma.
- Data/hora: 2026-11-05T17:14:28.117042-03:00.
- Corpus SHA-256: `1ab5db8ce6a48b7b0b476275f4a08a5a398f98542b5bb3b19da2e34e7ac25c00`.
- Perguntas reservadas SHA-256: `6a4b7ccb1363c4cdfbc0a15991cbbe14f4912b264a0cc9bc9f56a7b15fe81308`.
- Parâmetros e hashes do código: `evidencias/configuracao_avaliada.json`.
- A primeira avaliação reservada é preservada. Novas alterações após consultar seus resultados exigem um novo conjunto reservado para alegar avaliação sem ajuste sobre ele.

## Falhas observadas no perfil padrão

### desenvolvimento_expandido

- **Q50** — Separar o agente que planeja daquele que executa passos e retorna resultados Esperados: T208, T143; primeiros: T055, R021, R017, T144, T237.
- **Q82** — Materializar uma imagem consistente do estado em determinado instante Esperados: T240; primeiros: T056, T083, T164, T090, T188.
- **Q90** — Qual componente proposto da LAI reuniria memória de trabalho episódios e procedimentos? Esperados: P004, P005; primeiros: T049, T070, T071, T058, T062.

### reserva_expandida

- **H05** — Uma restrição antiga deve continuar recuperável mesmo depois de várias sessões terem sido sintetizadas em textos menores. Esperados: T069, T008, T023; primeiros: T084, T212, T063, T154, P002.
- **H31** — A sessão nova não conhece a meta nem o último comando executado. Quero um registro explícito para a passagem de trabalho. Esperados: T211, T234; primeiros: T210, T015, P004, T056, T084.

