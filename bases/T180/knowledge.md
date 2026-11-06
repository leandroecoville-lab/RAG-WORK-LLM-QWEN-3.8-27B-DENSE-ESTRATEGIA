# T180 — Prompt Distillation

**Nome canônico:** Prompt Distillation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T179  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** destilação de prompt

## T180:C01 — conceito

Especialização de destilação de contexto orientada a substituir instruções extensas por comportamento treinado. O professor recebe o prompt detalhado e gera exemplos; o aluno é ajustado para resolver a tarefa com instrução reduzida. Neste catálogo o termo se refere a treinamento, não a compressor textual de prompts.

Como funciona:
- Selecionar o comportamento repetitivo descrito pelo prompt.
- Gerar e revisar exemplos com professor condicionado por essas instruções.
- Treinar aluno e comparar com versões que ainda recebem o prompt completo.

Nota de nomenclatura: Variante próxima de T179; os dois nomes não devem ser contados como tecnologias inteiramente independentes.

## T180:C02 — aplicacao

Quando usar:
- Classificação ou extração com critérios estáveis.
- Prompt repetido representa parcela importante do custo de inferência.

Quando não usar:
- Instruções mudam frequentemente ou contêm restrições que precisam ser garantidas pelo runtime.

Implementação proposta:
- Versionar prompt-professor e dataset derivados como uma unidade.
- Separar dados sintéticos de avaliação independente.
- Planejar troca e reversão de adaptadores quando a instrução mudar.

Aplicação LAI proposta:
Proposta: considerar uma receita de destilação para tarefas padronizadas da Helena, sem presumir que ela ensina fatos atualizados sobre clientes.

## T180:C03 — riscos_validacao

Armadilhas:
- Dados sintéticos podem cobrir mal casos limítrofes do prompt.
- Reduzir prompt sem medir retenção pode perder exceções importantes.

Métricas sugeridas:
- Acerto com instrução curta e retenção das regras.
- Economia líquida após geração de dados, treino e manutenção.

Testes propostos:
- Testar exemplos novos que exigem cada exceção relevante da instrução.
- Comparar aluno treinado com aluno base usando o mesmo prompt curto.

## T180:C04 — perguntas_proveniencia

Pergunta: Prompt Distillation dispensa treino?
Resposta: Na acepção usada aqui, não; o comportamento é incorporado aos parâmetros ou adaptadores.

Pergunta: É independente de Context Distillation?
Resposta: É uma forma próxima e mais específica; mantemos o nome para recuperação.

Pergunta: Pode apagar o prompt original depois?
Resposta: Preserve-o como especificação versionada; ele ajuda a auditar e reconstruir o comportamento pretendido.

Pergunta: Um rótulo válido basta para avaliar?
Resposta: Não. Valide também sua correspondência com a entrada e as regras, especialmente exceções raras não cobertas pela geração sintética.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T180:C05 — mecanismo_avancado

Um prompt extenso costuma misturar regras estáveis, exemplos e parâmetros variáveis. Antes de destilar, é útil separar o que deverá virar comportamento dos valores que ainda precisam chegar a cada consulta. Instruções incompatíveis podem exigir identificador explícito de tarefa; treinar as mesmas entradas com saídas contraditórias não ensina ao aluno qual regime escolher. O contrato de saída também deve ser validado fora da própria geração do professor.

Condição de contorno:
Quando a política muda frequentemente, o custo de gerar dados, treinar e revalidar pode superar a economia de tokens.

Contrato proposto:
- Entradas: Prompt versionado, consultas representativas, parâmetros variáveis e respostas verificadas.
- Saídas: Modelo ajustado e instrução mínima necessária para selecionar o comportamento.
- Estado: Versão do comportamento, conjunto sintético e critérios de validação.
- Invariante: Parâmetros que variam por consulta não desaparecem sem outra forma de identificá-los.

Compromissos de projeto:
- Menos instruções repetidas reduzem contexto e aumentam custo de manutenção do modelo.
- Exemplos sintéticos amplificam cobertura e podem repetir erros sistemáticos do professor.

## T180:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar duas políticas que produzem rótulos diferentes para a mesma entrada, sem identificador de regime. Esperar falha diagnosticada; depois acrescentar a variável necessária e reavaliar.

Plano de avaliação proposto:
Plano proposto: comparar prompt integral, prompt reduzido sem treino e aluno destilado. Medir cumprimento de regras, casos limítrofes, custo total de manutenção e inferência; aprovar economia somente quando o comportamento necessário permanece demonstrável.

Comparações:
- T179 (specializes): Foca transferência de instruções recorrentes, mantendo explícita a informação variável indispensável.

Afirmação rastreável:
A receita Tinker gera respostas com um prompt no professor e treina o aluno para prevê-las sem receber esse prompt.
Suporte: direct; fontes: C-S034
Limite: A receita ilustrativa não garante internalização completa de regras extensas ou contraditórias.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T180:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou regras e parâmetros variáveis. A nova camada trata compressão de instruções como contrato de interface, com testes de seleção de regime, atualização e interação com o template.

Prompt mínimo explícito
Reduzir o prompt não significa eliminar toda instrução. Preserve identificador da tarefa, parâmetros variáveis e formato que ainda precisa ser selecionado. Defina o conjunto mínimo por ablação, removendo blocos separadamente; uma redução grande de tokens pode ocultar regressões em casos raros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

Contrato de comportamento
O adapter ou checkpoint passa a carregar parte das regras. Versione essa política junto ao endpoint e evite combinar um prompt antigo com pesos novos sem teste. Templates e tokens de sistema podem ativar comportamentos diferentes; a destilação deve ser avaliada no caminho de chat usado pelo produto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

Economia real
Menos tokens de entrada pode reduzir prefill e custo, mas respostas mais longas, retries ou validações adicionais podem consumir a economia. Meça o pedido completo e o custo de atualizar dados. Learning Zone descreve especialização com prompt reduzido e guardrails; isso não equivale a multiplicação geral de inteligência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

USO AVANÇADO — Objetos de domínio repetidos
Cenário: O serviço sempre gera o mesmo tipo de estrutura.
Estratégia: Treine exemplos variados e mantenha schema explícito ou decodificação restrita. Remova instruções apenas depois de verificar formato e conteúdo em casos inéditos.
Papel do modelo pequeno: Um 3–7B pode produzir objetos estreitos com baixa carga de prompt.
Aceite proposto: Reduzir tokens de entrada sem elevar rejeição ou erro por campo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

USO AVANÇADO — Múltiplas rotinas especializadas
Cenário: O mesmo aluno executa contratos parecidos.
Estratégia: Use identificadores de tarefa e exemplos que distinguem situações próximas. Se houver conflito persistente, separe adapters ou endpoints em vez de esconder a ambiguidade.
Papel do modelo pequeno: Um 8–14B pode compartilhar capacidade entre rotinas relacionadas, com seleção verificável.
Aceite proposto: Testar troca de tarefa e resistência a instruções que contradizem o contrato vigente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S034, V3D-S008, V4B-S012, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Boa hipótese para formatos e procedimentos fixos; fatos por usuário continuam externos.
8–14B: Avalie interferência entre tarefas e escolha explícita do comportamento.
15–30B: Compare economia de prefill com custo de manutenção de modelos e adapters adicionais.
Requisitos de treino/runtime: Exige ajuste de pesos/adapters; encurtar manualmente um prompt sem treino é outra intervenção.
Não aplicar quando: Não remover campos que distinguem respostas corretas apenas porque o dataset usa valores quase constantes.

## T180:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Parte das instruções foi absorvida no adaptador; avaliação continua necessária.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: A receita específica reduz instruções na entrada do aluno.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q009.

## T180:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T180 → T182 [complements]
Como combinar: A especialização por LoRA pode absorver parte das instruções, como no caso Learning Zone.
Interface: Adapter, prompt reduzido e versão da tarefa.
Condição: Escopo documentado é especializado e continua sujeito a validação.
Aceite proposto: Comparar resposta e rejeição com a versão de prompt completo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S012. Casos: V4D-C006.

2. T180 → T193 [complements]
Como combinar: Guardrails verificam restrições que não devem depender da memória do modelo.
Interface: Saída estruturada e regras externas.
Condição: Critérios explícitos e atualizados.
Aceite proposto: Testar casos adversos que o treino não cobriu.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S034, V3D-S008, V4B-S012, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Acompanhar tokens de saída e retries para não anunciar economia só de entrada.
- Manter baseline com instruções completas para diagnosticar regressões.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a rotina destilada com um modelo de fronteira usando o mesmo contrato de saída. Redução de prompt pode melhorar custo e consistência local, sem comprovar paridade fora da rotina.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T155, T179, R012

## Fontes primárias associadas

### C-S034 — Prompt Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receita gera dados com professor e treina aluno para tarefa de classificação com prompt reduzido.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S033 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treinar saídas produzidas com contexto privilegiado para reproduzi-las sem esse contexto pode internalizar comportamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3D-S008 — Prompt Distillation — Tinker Cookbook

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Professor usa prompt e consulta; estudante é treinado para prever resposta sem o prompt.

Limite: Receita de treinamento não reproduzida; generalização e economia dependem da tarefa.

### V4B-S012 — Model Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receitas on-policy/off-policy, LoRA e avaliação; documentação atual diferencia modelos disponíveis dos históricos.

Limite: Receita e resultados experimentais não comprovam deployment do aluno nem treino realizado neste pacote.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
