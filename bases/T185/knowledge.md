# T185 — Constitutional AI

**Nome canônico:** Constitutional AI  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T185  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** IA constitucional

## T185:C01 — conceito

Método de treinamento que usa princípios explícitos para orientar crítica, revisão e feedback produzido por IA. A proposta original inclui etapas supervisionadas e por reforço. Adicionar regras ao prompt pode ser útil, mas não reproduz automaticamente o processo de treinamento denominado Constitutional AI.

Como funciona:
- Definir princípios que servirão como referência para feedback.
- Gerar críticas, revisões ou preferências baseadas nesses princípios.
- Usar os sinais no treinamento e avaliar comportamentos resultantes.

## T185:C02 — aplicacao

Quando usar:
- Há objetivo de alinhamento comportamental e infraestrutura de treinamento.
- Princípios podem ser avaliados em casos claros e conflitantes.

Quando não usar:
- Tratar uma lista de regras textual como substituta de controles obrigatórios de acesso e execução.

Implementação proposta:
- Versionar princípios e exemplos de conflitos.
- Auditar amostras do feedback de IA para evitar avaliação circular.
- Medir fidelidade às tarefas legítimas junto com cumprimento das regras.

Aplicação LAI proposta:
Proposta: usar princípios explícitos nas avaliações da Helena, mantendo autorização e contratos no runtime; isso por si só não significa que seu modelo foi treinado com Constitutional AI.

## T185:C03 — riscos_validacao

Armadilhas:
- Princípios vagos podem produzir avaliações inconsistentes.
- Juiz e modelo podem compartilhar vieses e reforçar erros.

Métricas sugeridas:
- Cumprimento de critérios por categoria de caso.
- Falsas restrições, violações e consistência em conflitos de princípios.

Testes propostos:
- Construir conjunto reservado com casos em que dois princípios competem.
- Comparar avaliação de IA com referência humana ou verificador independente quando possível.

## T185:C04 — perguntas_proveniencia

Pergunta: Constitutional AI é só system prompt?
Resposta: Não. O nome do trabalho se refere a um processo de treinamento com feedback orientado por princípios.

Pergunta: Princípios garantem comportamento perfeito?
Resposta: Não. Aderência precisa ser medida.

Pergunta: Sem rótulos humanos significa sem escolhas humanas?
Resposta: Não. A escolha dos princípios, dados, critérios e avaliação continua definindo o comportamento pretendido.

Pergunta: Como mudar uma regra depois do treino?
Resposta: Versione a política e avalie a intervenção escolhida; um novo prompt pode influenciar respostas, mas não apaga automaticamente o comportamento aprendido.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T185:C05 — mecanismo_avancado

Princípios geram sinais de supervisão, mas a passagem de texto normativo para preferências envolve interpretação do avaliador. Regras conflitantes ou vagas podem criar rótulos inconsistentes; otimizar o reward model pode amplificar esses padrões. Portanto, é necessário separar adesão aos princípios, utilidade e correção factual. Uma resposta alinhada à preferência aprendida ainda pode conter informação falsa ou falhar em um contrato operacional.

Condição de contorno:
Alterar apenas a constituição em inferência não equivale a refazer o treinamento supervisionado e por reforço do método publicado.

Contrato proposto:
- Entradas: Princípios versionados, exemplos, críticas, revisões e preferências com proveniência.
- Saídas: Modelo treinado e avaliação por critérios independentes do gerador de preferências.
- Estado: Versões dos avaliadores, dataset de preferências e sinais de recompensa.
- Invariante: A mudança observada é atribuída à etapa efetivamente realizada, sem confundir prompting e treinamento.

Compromissos de projeto:
- Feedback automático amplia escala e herda vieses do avaliador.
- Princípios detalhados ajudam consistência e podem entrar em conflito em situações novas.

## T185:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar pares de princípios incompatíveis e exemplos factualmente errados que pareçam obedientes. Esperar detecção de conflito e reprovação factual independente da preferência automática.

Plano de avaliação proposto:
Plano proposto: comparar modelo inicial, etapa supervisionada e etapa com feedback de IA em conjuntos separados. Medir adesão, utilidade, factualidade e regressões; revisar casos discordantes com critérios explícitos antes de atribuir melhoria global.

Comparações:
- T192 (distinct_from): Autorrevisão em tempo de execução não reproduz, sozinha, as etapas de treinamento de Constitutional AI.

Afirmação rastreável:
O trabalho original inclui fine-tuning com revisões e reinforcement learning orientado por preferências geradas por IA.
Suporte: direct; fontes: C-S039
Limite: A fonte não demonstra que a constituição seja completa nem que preferências automáticas garantam verdade.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T185:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu interpretação e reward hacking. Esta camada propõe governança de princípios, testes de conflitos e separação entre norma treinada e regra operacional que precisa mudar imediatamente.

Princípios como especificação
Defina prioridade e exemplos de fronteira para regras que podem conflitar. Um princípio abstrato não determina sozinho a resposta correta em cada situação. Registre justificativa e versão dos rótulos produzidos por avaliadores, para detectar se uma mudança de interpretação alterou o dataset sem alteração explícita da política.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

Treino versus controle externo
Comportamento aprendido pode persistir após uma regra mudar. Políticas que exigem atualização imediata devem ter uma camada externa verificável, além do treinamento. A constituição atual da Anthropic é descrita como parte do processo de treino; colocá-la num prompt de um modelo comum é uma intervenção diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

Avaliar utilidade e erro
Uma resposta pode seguir estilo e princípios enquanto fornece fatos errados ou recusa tarefas válidas. Meça adesão, utilidade, correção e recusas excessivas separadamente. Avaliadores baseados no mesmo texto de princípios podem compartilhar pontos cegos; inclua revisão humana e casos que tensionem prioridades.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

USO AVANÇADO — Assistente de domínio regulado internamente
Cenário: A empresa possui regras de atendimento claras.
Estratégia: Traduza regras em exemplos revisados, mantenha controles externos para requisitos objetivos e avalie conflitos. Não apresente o treinamento como garantia de conformidade universal.
Papel do modelo pequeno: Um 3–7B pode executar uma rotina de atendimento estreita com limites verificáveis.
Aceite proposto: Aceitação por regra e categoria, incluindo respostas úteis que não devem ser recusadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

USO AVANÇADO — Política que evolui
Cenário: Novas regras tornam parte do comportamento anterior inadequada.
Estratégia: Versione dados e avaliadores, aplique controle externo enquanto prepara atualização e teste regressões. Preserve casos que distingam versões para verificar se a mudança ocorreu.
Papel do modelo pequeno: Um 8–14B pode ser atualizado por adaptação, sujeito à validação de comportamento.
Aceite proposto: Confirmar mudança desejada sem ampliar erros factuais ou recusas fora do escopo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S039, V4B-S021, V3B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Princípios simples e exemplos consistentes são preferíveis a constituições extensas sem cobertura de teste.
8–14B: Capacidade de seguir nuances precisa ser medida; aumentar texto normativo não garante compreensão.
15–30B: Maior porte pode melhorar interpretação, mas não elimina conflitos nem necessidade de governança.
Requisitos de treino/runtime: Constitutional AI envolve processo de treinamento/feedback; prompting constitucional isolado não é reprodução integral do método.
Não aplicar quando: Não usar concordância de um juiz com a política como prova de verdade externa ou de cumprimento perfeito.

## T185:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C017 — Anthropic / Claude — treinamento com constituição
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: treinamento de LLM.
Uso observado: A Anthropic descreve uso direto da constituição no processo que treina Claude, incluindo geração de exemplos e orientação de avaliações. O registro delimita a prática de treinamento do operador.
Mecanismo documentado: Princípios textuais orientam dados e julgamentos usados para ajustar comportamento; o documento evolui entre versões.
Correspondência com esta base: Princípios constitucionais são usados no treinamento por feedback de IA.
Transferência proposta para modelo pequeno: Proposta: criar princípios restritos ao domínio e validar com julgamentos humanos antes de usá-los em dados para 3–30B.
Limite: Laboratório de IA, separado de bigtech na contagem estrita. Não comprova receita reproduzível, porte 3–30B nem cumprimento perfeito dos princípios.
Fontes: V4B-S021.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q010.

## T185:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T185 → T193 [complements]
Como combinar: Guardrails externos implementam requisitos verificáveis e atualizáveis.
Interface: Política versionada e resultados de checagem.
Condição: Norma externa não contradiz silenciosamente o comportamento treinado.
Aceite proposto: Testar conflitos e registrar qual regra determinou o resultado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S039, V4B-S021, V3B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T185 → T198 [complements]
Como combinar: Confiança e abstenção devem ser avaliadas separadamente da adesão normativa.
Interface: Predições, rótulos e razões de recusa.
Condição: Conjunto cobre casos permitidos e proibidos.
Aceite proposto: Medir erro e recusa por categoria, sem recompensa por estilo apenas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S039, V4B-S021, V3B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir política do operador com consenso moral universal.
- Auditar exemplos sintéticos para evitar repetição sistemática de interpretações erradas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare adesão e utilidade no domínio definido. Uma constituição pode orientar comportamento, mas não transmite automaticamente conhecimento ou raciocínio de um modelo de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T177, T193, T194

## Fontes primárias associadas

### C-S039 — Constitutional AI: Harmlessness from AI Feedback

[https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinamento usa princípios para crítica/revisão e feedback de IA em fases supervisionada e por reforço.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S021 — Claude's new constitution

[https://www.anthropic.com/news/claude-new-constitution](https://www.anthropic.com/news/claude-new-constitution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Constituição usada em treinamento e síntese de exemplos/rankings; método evoluiu desde Constitutional AI.

Limite: Texto de princípios e treinamento não garantem aderência de toda saída; parâmetros do modelo não são publicados nesta fonte.

### V3B-S018 — Scaling Laws for Reward Model Overoptimization

[https://arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Risco de otimizar reward proxy e estudo de best-of-N em ambiente sintético.

Limite: O padrão observado em reward models não fornece uma lei universal de correção factual nem prova resultados de qualquer verificador.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
