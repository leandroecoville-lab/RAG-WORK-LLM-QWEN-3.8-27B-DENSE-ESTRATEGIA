# Validação — LAI RAG estratégico v4

## Entrega comprovada

- 287 bases: 243 entradas do inventário, 27 referências e 17 propostas.
- 2583 chunks, 1148 perguntas de estudo, 287 estratégias individuais.
- 574 usos avançados; 584 conexões com contrato; 409 mapeamentos caso→base.
- 93 casos canônicos em 98 registros, 105 consultas de pesquisa registradas.
- 449 registros de fontes e 414 URLs distintas.
- 55 testes executados, 0 falhas e 0 erros. Nenhuma chamada real a modelos ou embeddings.
- IDs e campos anteriores preservados; textos C01–C06 conferidos contra hashes v3. Três camadas novas por base.
- Cada base possui dez arquivos, incluindo JSONs de estratégia/casos/conexões e Mermaid.

## Meta de dez exemplos reais por base

Solicitado: **2870 associações**. Comprovado no critério estrito de produção Big Tech + mecanismo exato: **50**. Lacuna somada por base: **2820**. Bases que atingiram dez: **0/287**; bases com ao menos um caso estrito: **36**.

Não se preencheu a meta com exemplos inventados. Labs de IA e outros operadores são contados separadamente. Produtos, pesquisas e analogias não são reclassificados como implantação. Casos que mapeiam vários temas continuam sendo uma implantação canônica, não várias. A tabela completa está em `producao/COBERTURA_10_POR_BASE.csv`.

Casos canônicos por nível: {"production_documented": 48, "operational_product": 28, "research_only": 17}. Registros antes da deduplicação: {"production_documented": 53, "operational_product": 28, "research_only": 17}.

Das associações estritas de mecanismos, 34 são de aplicações, serving ou treino de LLMs. As restantes podem comprovar mecanismos de infraestrutura geral; isso não comprova uso em LLM pequena.

Conexões por estágio: {"engineering_proposal": 526, "production_documented": 50, "operational_product": 8}.

## Regressão de recuperação executada

| Conjunto/perfil | Consultas | Acertos @5 | Hit@5 | MRR@10 | Nomes Hit@3 |
|---|---:|---:|---:|---:|---:|
| historicas90_expandido | 90 | 87 | 96.7% | 0.8586 | 100.0% |
| historicas90_exato | 90 | 86 | 95.6% | 0.8223 | 100.0% |
| reserva_v3_conhecida40_expandido | 40 | 37 | 92.5% | 0.8231 | 100.0% |
| reserva_v3_conhecida40_exato | 40 | 37 | 92.5% | 0.7815 | 100.0% |

As 130 consultas são conhecidas das versões anteriores. Esta é regressão local, não nova reserva cega, benchmark externo ou prova de qualidade de resposta de LLM. Os parâmetros da v3 foram mantidos. Alterar o corpus pode mudar os rankings; a comparação não identifica automaticamente qual componente causou a mudança. Hit@5 aceita algum ID esperado, não todos.

## Integridade, novidade e grafos

A validação verifica identidade, campos, fontes, consultas, casos, classes, contagem canônica e coerência dos grafos. Conexão documentada exige caso operacional com origem/alvo exatos e fonte em comum. Isso é uma restrição estrutural e não substitui leitura factual.

O diagnóstico de novidade encontrou 0 bases acima do limiar de revisão textual de 25% de sequências de 12 palavras presentes na própria v3. O limiar é uma heurística editorial, não certificado de novidade ou ausência de redundância. Foram contadas 135,015 palavras nos campos das estratégias novas; exports repetidos não aumentam essa contagem.

HTMLs tiveram estrutura e sintaxe JavaScript verificadas. Quando Node está disponível, seleção, filtros e contratos do grafo são exercitados em DOM mínimo simulado, com hash do HTML no relatório. Não houve renderização visual de navegador; simulação DOM não comprova layout ou acessibilidade completa.

## O que não foi demonstrado

Não houve inferência real de 3–30B, treinamento, embeddings reais, benchmark GPU, implantação na Helena ou execução das receitas industriais. O comparador de sistemas recebeu dados sintéticos apenas nos testes de contrato. Não há medição de paridade com fronteira, certificação de acervo mundialmente superior ou garantia de ausência de erro factual.

## Reprodutibilidade

- Python: 3.12.14.
- Avaliado em: 2026-11-05T23:41:26.055794+00:00.
- Corpus SHA-256: `a959686a86fae91e2f3635e8f2db3fb9f0da7bc36b8d9ab02b484d3f2f22dc8c`.
- Hashes de código, entradas, fontes, casos e consultas: `evidencias/configuracao_avaliada.json`.
- Integridade do ZIP e hashes dos arquivos são conferidos pelo empacotador; hashes não comprovam a verdade das fontes.

## Falhas observadas no perfil padrão

### historicas90_expandido

- Q50: Separar o agente que planeja daquele que executa passos e retorna resultados Esperados: T208, T143. Recuperados: T055, T144, R021, R017, T206.
- Q82: Materializar uma imagem consistente do estado em determinado instante Esperados: T240. Recuperados: T056, T083, T139, T077, T173.
- Q90: Qual componente proposto da LAI reuniria memória de trabalho episódios e procedimentos? Esperados: P004, P005. Recuperados: T049, T070, T071, T058, T062.

### reserva_v3_conhecida40_expandido

- H01: A fonte mudou, mas perguntas parecidas ainda recebem uma resposta armazenada antiga. Qual política deve remover essa resposta? Esperados: T031, T005. Recuperados: T054, T149, T158, T048, T003.
- H02: Preciso localizar um parágrafo preciso e depois fornecer a seção maior à resposta, mantendo a ligação entre as duas escalas. Esperados: T032. Recuperados: T026, T012, T033, T086, T123.
- H05: Uma restrição antiga deve continuar recuperável mesmo depois de várias sessões terem sido sintetizadas em textos menores. Esperados: T069, T008, T023. Recuperados: T154, T212, T084, T063, T036.


## Revisão documental dos casos

Os 98 registros de casos de origem receberam revisão independente de mecanismos centrais e evidência, com profundidade e fontes explicitadas em seis relatórios. As correções necessárias foram registradas; isso não certifica cada frase ou as implementações das empresas. Veja `pesquisa/REVISAO_FACTUAL_V4.md`.

A revisão de novidade encontrou e corrigiu repetição substantiva em P012/P015. O diagnóstico textual e suas limitações estão em `evidencias/REVISAO_NOVIDADE.md`.
