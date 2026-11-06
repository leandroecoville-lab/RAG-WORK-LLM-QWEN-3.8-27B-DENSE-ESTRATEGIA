# T194 — Process Supervision

**Nome canônico:** Process Supervision  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T194  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** supervisão de processo

## T194:C01 — conceito

Supervisão de treinamento que fornece sinais sobre etapas intermediárias, em vez de avaliar somente o resultado final. Pode ensinar um avaliador a identificar erros de processo ou fornecer sinal de aprendizagem ao modelo. Exige definição de etapas e rótulos confiáveis; texto longo não implica processo correto.

Como funciona:
- Coletar soluções ou trajetórias com passos observáveis.
- Rotular validade ou qualidade de passos segundo critérios consistentes.
- Treinar com esses sinais e avaliar se a conclusão melhora em tarefas novas.

## T194:C02 — aplicacao

Quando usar:
- Erros intermediários importam e podem ser identificados por anotadores ou verificadores.
- Resultado final sozinho não revela onde o procedimento falhou.

Quando não usar:
- Anotações apenas reproduzem plausibilidade linguística ou penalizam caminhos alternativos válidos.

Implementação proposta:
- Definir unidade de passo e rubrica de anotação.
- Medir concordância entre avaliadores e resolver conflitos.
- Comparar supervisão de processo e de resultado com dados e orçamento controlados.

Aplicação LAI proposta:
Proposta: registrar passos e evidências de tarefas verificáveis da Helena como candidatos a dados de supervisão, sem chamar todo trace de exemplo correto.

## T194:C03 — riscos_validacao

Armadilhas:
- Custo de anotação pode ser alto e rótulos inconsistentes ensinam critérios ruins.
- Passos aparentemente corretos podem terminar em resultado errado.

Métricas sugeridas:
- Precisão de detecção de erros intermediários.
- Qualidade final em teste reservado e custo de anotação.

Testes propostos:
- Inserir erro em etapa intermediária mantendo final plausível e testar localização.
- Incluir solução alternativa válida e verificar que não é rejeitada pelo estilo.

## T194:C04 — perguntas_proveniencia

Pergunta: Process supervision é só revisar uma resposta?
Resposta: Não. Refere-se ao sinal de treinamento sobre etapas; revisão em inferência é outro uso.

Pergunta: Exige acesso a pensamentos privados?
Resposta: Não. Pode supervisionar ações, resultados e passos explicitamente observáveis.

Pergunta: Resposta final correta basta como rótulo de todas as etapas?
Resposta: Não. Ela pode resultar de cancelamento de erros ou acerto casual.

Pergunta: Como evitar premiar enrolação?
Resposta: Avalie progresso e requisitos por etapa, distinguindo passos válidos úteis de repetições neutras sem avanço.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T194:C05 — mecanismo_avancado

A unidade de supervisão precisa ser definida: uma linha textual pode conter várias inferências, e uma inferência pode atravessar linhas. Rótulos de etapas ajudam a localizar erro, mas dependem da informação anterior e de critérios sobre progresso. Uma conclusão correta por coincidência não torna cada transição válida; inversamente, etapas neutras podem ser corretas sem avançar a solução. O dataset deve representar essas distinções.

Condição de contorno:
Rótulos inconsistentes ou segmentação inadequada podem ensinar o avaliador a preferir estilo e comprimento em vez de validade.

Contrato proposto:
- Entradas: Trajetórias segmentadas, contexto por etapa, critérios de rótulo e anotadores ou verificadores.
- Saídas: Modelo avaliador ou sinal de treinamento com feedback localizado.
- Estado: Proveniência dos rótulos, discordâncias e separação por problema de origem.
- Invariante: Etapas do mesmo problema não vazam entre treino e avaliação final sem controle explícito.

Compromissos de projeto:
- Feedback fino melhora atribuição de erro e custa anotação.
- Selecionar erros convincentes pode ser informativo e alterar a distribuição dos exemplos.

## T194:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir solução com resposta final correta e etapa intermediária inválida, além de sequência longa de passos neutros. Esperar avaliação diferenciada de validade e progresso.

Plano de avaliação proposto:
Plano proposto: comparar supervisão de resultado e de processo com orçamento de anotação declarado. Medir localização de erros, qualidade final, consistência entre anotadores e custo; usar problemas inéditos, não somente novas trajetórias dos mesmos enunciados.

Comparações:
- T206 (distinct_from): Supervisão de processo treina com sinais intermediários; verificação de processo pode apenas inspecionar uma execução.

Afirmação rastreável:
Let’s Verify Step by Step utiliza rótulos positivos, negativos e neutros para etapas intermediárias de soluções.
Suporte: direct; fontes: C-S047
Limite: A evidência estudada é principalmente matemática; não certifica que toda narrativa textual represente o processo interno real.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T194:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu unidades e rótulos de etapa. Esta camada examina qualidade do sinal local, custo de anotação e diferença entre supervisionar processo no treino e verificar uma execução em runtime.

O que uma etapa demonstra
Um passo pode ser válido, irrelevante, incompleto ou depender de premissa falsa. Use rótulos que preservem essas distinções quando úteis ao objetivo. Julgar somente fluência ou plausibilidade pode ensinar o avaliador a premiar explicações elegantes, sem detectar o primeiro erro que compromete a solução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

Trajetórias parciais
Para treinar um avaliador de processo, mantenha contexto suficiente e não forneça o resultado futuro como pista indevida. Inclua erros próximos de passos corretos e trajetórias que chegam à resposta certa por coincidência. Separe problemas de origem entre treino e teste para evitar memorização de soluções.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

Processo e execução observável
Relatos de busca como AlphaEvolve usam avaliadores de programas e desempenho, mas isso não comprova supervisão de cada passo interno de raciocínio. Em agentes, estados de ferramenta e transições oferecem observáveis mais concretos que uma narrativa retrospectiva. Escolha a unidade de supervisão conforme o que pode ser validado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

USO AVANÇADO — Resolução técnica segmentada
Cenário: Uma tarefa possui etapas com critérios locais verificáveis.
Estratégia: Anote o primeiro erro e requisitos por transição, treine ou avalie o verificador e use-o para orientar revisão. Confirme se aprovação local leva a sucesso final.
Papel do modelo pequeno: Um 8–14B pode aprender procedimentos com feedback específico, sem presumir generalização irrestrita.
Aceite proposto: Medir detecção do primeiro erro e resultado final em problemas novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

USO AVANÇADO — Agente com ferramentas
Cenário: O workflow exige pré-condições antes de cada ação.
Estratégia: Use estados reais e resultados das ferramentas como sinais de etapa. Não aceite um texto dizendo que a condição foi satisfeita sem observação correspondente.
Papel do modelo pequeno: Um 3–7B pode executar etapas estreitas sob supervisão externa.
Aceite proposto: Verificar transições válidas e ausência de efeitos fora do plano.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S047, V3B-S018, V4B-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Critérios locais simples podem tornar feedback mais útil que uma nota final genérica.
8–14B: Avaliar processos mais longos exige cobertura de dependências e erros acumulados.
15–30B: Maior porte pode produzir trajetórias mais complexas, elevando custo e ambiguidade da anotação.
Requisitos de treino/runtime: Supervisão de processo é treino ou avaliação de etapas; verificação em runtime é uso relacionado, não reprodução automática do método.
Não aplicar quando: Não equiparar cadeia de pensamento escrita a registro fiel de todos os mecanismos internos do modelo.

## T194:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q011.

## T194:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T194 → T206 [complements]
Como combinar: Eventos observáveis podem fornecer unidades de processo verificáveis.
Interface: Estado anterior, ação e pós-condição.
Condição: Logs representam operações reais e possuem identidade.
Aceite proposto: Comparar narrativa com estado externo observado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S047, V3B-S018, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T194 → T199 [feeds]
Como combinar: Falhas localizadas podem orientar novos dados ou mudanças persistentes.
Interface: Etapa, tipo de erro e versão do componente.
Condição: Atualização explícita e avaliação independente.
Aceite proposto: Medir melhora em trajetórias novas, não só nos exemplos corrigidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S047, V3B-S018, V4B-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar validade local, progresso e correção final.
- Auditar discordâncias de anotadores antes de transformar rótulos em recompensa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare competência em processos definidos e verificáveis. Supervisão mais granular pode ajudar, mas não garante que um modelo pequeno tenha a capacidade necessária para todos os passos de uma tarefa de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T177, T190, T206

## Fontes primárias associadas

### C-S047 — Let's Verify Step by Step

[https://arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão por etapas difere de rotular apenas o resultado final.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S018 — Scaling Laws for Reward Model Overoptimization

[https://arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Risco de otimizar reward proxy e estudo de best-of-N em ambiente sintético.

Limite: O padrão observado em reward models não fornece uma lei universal de correção factual nem prova resultados de qualquer verificador.

### V4B-S022 — AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms

[https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração evolutiva com avaliadores executáveis; heurística descoberta implantada em Borg e verificações de circuitos.

Limite: Não confundir ensemble de proponentes com votação nem transferir ganhos de sistemas Google a modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
