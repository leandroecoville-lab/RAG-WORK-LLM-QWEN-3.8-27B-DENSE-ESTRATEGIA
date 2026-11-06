# T201 — Agent Test-Time Scaling

**Nome canônico:** Agent Test-Time Scaling  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T201  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** escalada de computação em execução de agentes

## T201:C01 — conceito

Aumento de recursos durante a execução de um agente: mais candidatos, ferramentas, buscas, verificações ou especialistas. Diferencia-se de ampliar o treinamento. O ganho depende da qualidade das ações extras e do mecanismo de seleção; repetir a mesma falha não cria capacidade nova.

Como funciona:
- Identificar gargalo observável da tentativa inicial.
- Alocar recurso adicional à busca, geração ou verificação que possa resolvê-lo.
- Selecionar resultado e parar quando benefício adicional não justificar custo.

## T201:C02 — aplicacao

Quando usar:
- Tarefas difíceis e verificáveis que respondem a tentativas alternativas.
- Há evidências de que orçamento extra melhora a taxa de sucesso.

Quando não usar:
- Usar mais agentes ou tokens como substituto de ferramenta ausente ou requisito impossível.

Implementação proposta:
- Definir orçamento total, incluindo coordenação e verificações.
- Comparar escalada serial, paralela e recuperação adicional.
- Medir curvas de resultado versus custo em vez de apenas o melhor exemplo.

Aplicação LAI proposta:
Proposta: a Helena aumentar esforço onde testes indicarem retorno, preservando limites e evidências de que a computação extra ajudou.

## T201:C03 — riscos_validacao

Armadilhas:
- Verificador fraco pode escolher a pior de muitas soluções.
- Latência e custo podem crescer mais rápido que a qualidade.

Métricas sugeridas:
- Sucesso por orçamento e tempo até resultado aceito.
- Ganho marginal e proporção de tentativas redundantes.

Testes propostos:
- Comparar políticas sob o mesmo custo total.
- Aplicar tarefas sem resposta disponível e verificar abstenção em vez de geração infinita.

## T201:C04 — perguntas_proveniencia

Pergunta: Mais tempo transforma modelo pequeno em modelo de fronteira?
Resposta: Não há equivalência garantida; algumas capacidades podem continuar ausentes.

Pergunta: É a mesma coisa que treinar por mais épocas?
Resposta: Não. O recurso é gasto durante execução da tarefa.

Pergunta: Mais tokens é igual a mais computação útil?
Resposta: Não. Podem ser redundantes ou produzir candidatos que o verificador não sabe distinguir.

Pergunta: Como decidir parar?
Resposta: Use orçamento e evidência de progresso mensurável; satisfação verbal do agente não basta como critério de utilidade marginal.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T201:C05 — mecanismo_avancado

O orçamento extra pode ser investido em largura, como candidatos paralelos, ou profundidade, como revisões sequenciais. Essas escolhas têm latências diferentes mesmo com número parecido de tokens. A utilidade marginal depende da dificuldade e do verificador: se falta uma informação externa, mais tentativas sem buscá-la podem repetir a mesma falha. Uma política adaptativa precisa estimar quando o próximo passo provavelmente acrescentará evidência ou capacidade.

Condição de contorno:
Aumento de computação não garante melhoria monótona, sobretudo quando seleção e feedback são imperfeitos.

Contrato proposto:
- Entradas: Tarefa, orçamento de tokens/tempo/chamadas, ações adicionais e sinais de progresso.
- Saídas: Resultado selecionado ou abstenção com custo e razão de parada.
- Estado: Candidatos, evidências, avaliações e orçamento restante.
- Invariante: O sistema contabiliza custo de geração, ferramentas e verificação, sem esconder trabalho descartado.

Compromissos de projeto:
- Paralelismo reduz tempo de parede e aumenta recursos simultâneos.
- Revisão sequencial usa feedback intermediário e impõe dependências de latência.

## T201:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: oferecer tarefa sem dado indispensável e permitir muitas tentativas internas. Esperar que a política busque o dado ou declare a lacuna, em vez de contar repetição como progresso.

Plano de avaliação proposto:
Plano proposto: comparar resposta única, amostragem paralela, revisão e busca com orçamento equivalente. Estratificar dificuldade; medir qualidade externa, latência e custo total. Aprovar a política pela curva de benefício marginal e pelos prazos de uso.

Comparações:
- T189 (complements): Best-of-N é uma alocação possível do orçamento adicional, dependente da qualidade do seletor.

Afirmação rastreável:
O estudo de test-time compute encontra dependência da estratégia eficiente em relação à dificuldade do prompt.
Suporte: direct; fontes: V3B-S020
Limite: Os resultados não definem política ótima universal para agentes, ferramentas ou cargas do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T201:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou largura, profundidade e custo de ferramentas. Esta camada propõe alocação marginal de orçamento, controle de caminhos improdutivos e comparação entre busca e obtenção de nova informação.

Valor da próxima ação
Decida entre gerar outro candidato, revisar, executar teste ou buscar evidência conforme a falha atual. Se todos os candidatos usam a mesma premissa falsa, mais geração tem pouco valor. Uma política proposta estima benefício esperado e custo, mas precisa ser validada; a estimativa do próprio modelo não é uma probabilidade confiável por definição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

Portfólio de busca
Combine algumas alternativas independentes com refinamento dos candidatos promissores, preservando diversidade relevante. AlphaEvolve usa busca evolutiva com avaliadores, em um domínio executável. A transferência para um agente pequeno exige oráculos e representações adequados, sem transportar automaticamente os resultados da infraestrutura Google.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

Custo e parada
Inclua tokens, ferramentas, filas e verificadores no orçamento. Pare por sucesso verificado, benefício marginal baixo ou limite explícito; não apenas quando o agente se declara satisfeito. Guarde a melhor solução válida e pendências, evitando que uma última tentativa pior destrua progresso anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

USO AVANÇADO — Otimização de função pequena
Cenário: Há desempenho mensurável e testes de correção.
Estratégia: Gere diversidade inicial, elimine incorretas e refine soluções válidas. Use entradas reservadas para evitar explorar particularidades do benchmark de desenvolvimento.
Papel do modelo pequeno: Um 8–14B pode explorar um espaço local com avaliações baratas.
Aceite proposto: Melhora reproduzível em entradas novas e custo total de busca conhecido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

USO AVANÇADO — Tarefa de pesquisa delimitada
Cenário: Uma resposta depende de poucas evidências ainda ausentes.
Estratégia: Invista chamadas em localizar e confrontar fontes antes de aumentar amostras de redação. Reavalie necessidade de refinamento quando a informação estiver completa.
Papel do modelo pequeno: Um 3–7B pode organizar trabalho e síntese curta com recuperação confiável.
Aceite proposto: Cobertura factual e tempo até resposta sustentada, não número de pensamentos produzidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S020, V4B-S022, V4B-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Computação adicional ajuda quando o modelo já produz candidatos úteis ou consegue usar ferramentas.
8–14B: Aumente orçamento por dificuldade observada e capacidade do verificador.
15–30B: Compare custo de várias tentativas 15–30B com uma chamada mais forte, incluindo latência serial.
Requisitos de treino/runtime: Orquestração em inferência; pode usar modelos fixos. Treinamento para aproveitar orçamento é outra intervenção.
Não aplicar quando: Não assumir que dobrar tokens duplica qualidade nem chamar repetição sem evidência de raciocínio superior.

## T201:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C019 — Google DeepMind / AlphaEvolve em infraestrutura Google
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador relata heurística incorporada ao Borg e aplicações posteriores na infraestrutura, além de melhorias de algoritmos e projetos de hardware. É contado como um sistema, não como vários exemplos artificiais.
Mecanismo documentado: Modelos propõem programas; avaliadores automáticos executam e pontuam candidatos; um banco evolutivo alimenta novas iterações. No caso de circuito, verificações preservaram funcionalidade antes da integração descrita.
Correspondência com esta base: Há busca entre candidatos, mas não é simplesmente best-of-N independente.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para gerar alterações pequenas com avaliadores baratos, preservando um baseline e um orçamento de busca.
Limite: Modelos Gemini de fronteira foram usados; não demonstra a mesma capacidade com 3–30B. Uma melhoria de uma função avaliada não prova correção geral do software.
Fontes: V4B-S022, V4B-S023.

V4D-C005 — DeepSeek-AI / DeepSeek-R1-Distill 7B/8B/14B
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: Autores disponibilizam modelos menores afinados com amostras do professor e publicam avaliações.
Mecanismo documentado: SFT/destilação de respostas de um modelo maior para modelos densos menores.
Correspondência com esta base: Avaliação inclui diferentes regimes de amostragem; não prova política ótima de compute adaptativo em produção.
Transferência proposta para modelo pequeno: Proposta: selecionar tarefas verificáveis, filtrar demonstrações por teste externo, isolar famílias entre treino/teste e comparar custo total incluindo o professor.
Limite: Pesquisa, não produção. Comparadores são versões históricas; 32B/70B não pertencem à faixa solicitada. Mais amostras têm custo e consenso não elimina erros correlacionados.
Fontes: V4D-S008, V4D-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T201:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T201 → T189 [complements]
Como combinar: Best-of-N investe orçamento em alternativas selecionadas por verificação.
Interface: Candidatos e custos marginais.
Condição: Verificador distingue qualidade real.
Aceite proposto: Comparar largura com profundidade em orçamento equivalente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S020, V4B-S022, V4B-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T201 → T202 [complements]
Como combinar: Planejamento por incerteza decide quando observar em vez de gerar.
Interface: Lacunas e ações de aquisição de informação.
Condição: Observações são acessíveis e relevantes.
Aceite proposto: Medir redução de erro por ação adicional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S020, V4B-S022, V4B-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Cobrar no custo tentativas descartadas e verificações inconclusivas.
- Não ajustar a política de busca sobre os casos finais de avaliação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie curvas de sucesso versus custo e prazo. Em tarefas verificáveis, busca pode reduzir uma lacuna específica; fora delas, mais computação pode apenas ampliar erro e custo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T145, T146, T169, T189

## Fontes primárias associadas

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S043 — Training Verifiers to Solve Math Word Problems

[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificador pontua soluções candidatas; seleção é distinta de votação simples.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S020 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alocação adaptativa de computação e dependência da dificuldade do problema.

Limite: Resumo e resultados conceituais consultados; ganhos publicados não foram reproduzidos nem extrapolados.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

### V4B-S023 — AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields

[https://deepmind.google/blog/alphaevolve-impact/](https://deepmind.google/blog/alphaevolve-impact/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso continuado de algoritmos descobertos em infraestrutura Google, incluindo refinamento de heurísticas de Spanner.

Limite: Aplicações diferentes não serão multiplicadas artificialmente em dez casos do mesmo sistema; detalhes experimentais e operacionais variam.

### V4D-S008 — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

[https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesquisa sobre RL de raciocínio e transferência de capacidades a modelos menores.

Limite: Pesquisa e benchmarks, não evidência de implantação de cada variante. Registro atual é v2, revisado em 2026-01-04; comparação histórica não define fronteira de novembro de 2026.

### V4D-S010 — DeepSeek-R1 official model repository

[https://github.com/deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints destilados 7B, 8B e 14B dentro da faixa pedida; tabelas de avaliação com configuração de amostragem e modelos comparadores identificados.

Limite: 32B e 70B estão fora da faixa 3–30B. Pass@1 e consenso@64 não são a mesma métrica. Benchmarks históricos e resultados do autor não demonstram paridade geral ou produção.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
