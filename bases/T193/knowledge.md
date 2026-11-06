# T193 — Guardrails

**Nome canônico:** Guardrails  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T193  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controles de execução e saída

## T193:C01 — conceito

Conjunto de controles que limita entradas, saídas e ações conforme contratos e políticas. Pode incluir validação determinística, autorização, filtros e modelos classificadores. É uma família de mecanismos; uma frase no prompt ou um filtro isolado não constitui garantia completa de execução correta.

Como funciona:
- Definir invariantes da tarefa e pontos onde precisam ser aplicadas.
- Validar entrada e intenção antes de ações com efeito.
- Conferir saída e registrar rejeição, correção ou aprovação com motivo.

## T193:C02 — aplicacao

Quando usar:
- Agentes acessam ferramentas, dados de clientes ou fluxos com regras claras.
- Saídas precisam respeitar schema, escopo ou restrição operacional.

Quando não usar:
- Usar guardrail como substituto de correção do código, isolamento de dados ou avaliação de qualidade.

Implementação proposta:
- Aplicar autorização no backend, fora do texto gerado pela LLM.
- Separar controles obrigatórios de recomendações ajustáveis.
- Medir falsos bloqueios e manter diagnóstico sem vazar conteúdo sensível.

Aplicação LAI proposta:
Proposta: implementar contratos e permissões da Helena no runtime e avaliar controles de linguagem como complementos mensuráveis.

## T193:C03 — riscos_validacao

Armadilhas:
- Controles em apenas uma camada deixam outros caminhos de execução abertos.
- Classificador imperfeito pode bloquear uso legítimo ou aprovar violação.

Métricas sugeridas:
- Violações detectadas e não detectadas em testes.
- Taxa de bloqueio indevido e latência adicionada.

Testes propostos:
- Tentar acessar recurso fora do escopo e conferir bloqueio no executor.
- Testar pedido legítimo próximo da fronteira para medir falsos positivos.

## T193:C04 — perguntas_proveniencia

Pergunta: Guardrail é igual a censura textual?
Resposta: Não. Inclui regras operacionais como autorização, limite de custo e validação de argumentos.

Pergunta: Um framework de guardrails garante segurança total?
Resposta: Não. A cobertura e os caminhos de execução precisam ser verificados.

Pergunta: Prompt com regras é um guardrail completo?
Resposta: Não. Pode orientar o modelo, mas efeitos operacionais exigem controles no caminho que realmente os executa.

Pergunta: Falha do verificador significa saída inválida?
Resposta: Significa que a checagem não concluiu; a política deve decidir como proceder sem rotular desconhecimento como sucesso.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T193:C05 — mecanismo_avancado

O ponto em que um controle atua determina o que ele consegue impedir. Validar uma resposta textual depois que uma ferramenta já executou não desfaz o efeito produzido. Controles de ação precisam receber argumentos reais antes da execução e avaliar o resultado depois, enquanto controles de saída tratam o conteúdo entregue. Falhas de infraestrutura do verificador exigem política explícita, em vez de serem confundidas com aprovação.

Condição de contorno:
Um guardrail probabilístico pode ter falsos positivos e negativos; controles determinísticos também dependem da completude do contrato.

Contrato proposto:
- Entradas: Entrada, ação proposta, argumentos concretos, política versionada e resultado quando existente.
- Saídas: Decisão de permitir, bloquear ou corrigir, com motivo rastreável.
- Estado: Estado da operação, evidências, versão da regra e tentativas.
- Invariante: Uma ação sujeita a controle não contorna o ponto de validação por outro caminho.

Compromissos de projeto:
- Mais controles aumentam cobertura e latência.
- Regras rígidas simplificam auditoria e podem rejeitar casos legítimos não previstos.

## T193:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fazer a ferramenta ser chamada por uma rota alternativa sem passar no controlador e interromper o classificador. Esperar identificação do caminho descoberto e comportamento conforme a política de indisponibilidade.

Plano de avaliação proposto:
Plano proposto: avaliar casos permitidos, proibidos e ambíguos por ponto de aplicação. Medir falsos aceites, bloqueios indevidos, latência e cobertura de rotas; aprovar controles pelo comportamento observado e não apenas pela presença de configuração.

Comparações:
- T197 (complements): Schema valida forma dos argumentos, enquanto regras adicionais avaliam autorização e significado operacional.

Afirmação rastreável:
NeMo Guardrails distingue controles de entrada, diálogo, recuperação, execução de ferramentas e saída.
Suporte: direct; fontes: C-S046
Limite: Configurar uma biblioteca não prova que todas as rotas da aplicação passam pelos controles.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T193:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 localizou controles antes e depois de ações. O aprofundamento trata composição de regras, semântica de bloqueio e observabilidade de falsos positivos e lacunas.

Camadas com escopo
Separe validação estrutural, autorização, regra de negócio e avaliação de conteúdo. Cada camada deve declarar o que prova e o que não examina. Bedrock Automated Reasoning verifica relações numa política formal; isso não equivale a checar toda verdade do mundo nem a tornar correta a tradução de texto automaticamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

Composição sem brechas
Todos os caminhos que executam uma ação precisam passar pela mesma decisão de autorização e pelo contrato aplicável. Uma alternativa de ferramenta ou retry não pode contornar a regra. Preserve identidade, argumentos efetivos e versão da política para que a decisão auditada corresponda à operação real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

Falhas e experiência
Defina resultados permitidos, bloqueados e inconclusivos. Falha do serviço de verificação pode exigir suspensão, redução de escopo ou encaminhamento conforme a operação, mas não aprovação silenciosa. Meça rejeições indevidas e explique ao fluxo de produto qual dado ou condição falta para continuar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

USO AVANÇADO — Geração de questões educacionais
Cenário: A saída precisa obedecer formato e restrições de conteúdo.
Estratégia: Use modelo especializado para propor e filtros antes de exibir. Learning Zone descreve a combinação, mas a configuração e escala atuais não são assumidas a partir do artigo de preparação.
Papel do modelo pequeno: Um 3–7B pode produzir objetos delimitados que passam por critérios externos.
Aceite proposto: Avaliar rejeição, correção e utilidade com revisão humana.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

USO AVANÇADO — Ação de negócio com efeitos
Cenário: O agente propõe alterar um registro.
Estratégia: Valide schema, identidade, permissão e pré-condição sobre o estado atual; execute somente após confirmação da decisão. Verifique pós-condição observada.
Papel do modelo pequeno: Um 8–14B pode interpretar intenção, enquanto controles determinísticos decidem a operação.
Aceite proposto: Nenhuma ação fora do contrato e distinção explícita entre falha e sucesso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S046, V4B-S027, V4D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Controles externos permitem tarefas estreitas, mas não compensam toda incapacidade do modelo.
8–14B: Especialização deve ser acompanhada de testes de cobertura e falsos bloqueios.
15–30B: Mesmo 15–30B continua sujeito às mesmas regras de autorização e validação.
Requisitos de treino/runtime: Runtime e serviços externos; pode coexistir com treinamento, sem ser equivalente a alinhamento dos pesos.
Não aplicar quando: Não chamar validação de JSON de verificação factual nem verificação formal de política de garantia universal.

## T193:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C022 — Amazon Web Services / Bedrock Automated Reasoning checks
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação descreve uma funcionalidade disponível de verificação por raciocínio automatizado para respostas em linguagem natural vinculadas a políticas.
Mecanismo documentado: Políticas são expressas formalmente e a tradução de texto para afirmações é analisada. O recurso é de detecção e possui restrições de idioma e resposta completa.
Correspondência com esta base: Guardrail verifica uma política expressa formalmente.
Transferência proposta para modelo pequeno: Proposta: usar um 3–30B para redigir respostas e um verificador externo para políticas formalizáveis, encaminhando traduções ambíguas para revisão.
Limite: Disponibilidade não comprova adoção específica. Validade em uma política não garante verdade externa, atualização dos fatos ou correção da tradução de linguagem natural.
Fontes: V4B-S027.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Restrições verificáveis rejeitam saídas inadequadas antes da exibição.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019.

## T193:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T193 → T182 [complements]
Como combinar: Learning Zone combina especialização LoRA e guardrails antes da exibição.
Interface: Adapter, contrato de saída e resultado dos filtros.
Condição: Escopo especializado documentado.
Aceite proposto: Comparar qualidade e rejeição com avaliação humana.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S012. Casos: V4D-C006.

2. T193 → T197 [requires]
Como combinar: Schema valida o contrato estrutural antes de regras semânticas.
Interface: Objeto parseado e schema versionado.
Condição: Recursos usados são suportados pelo validador.
Aceite proposto: Testar campos ausentes, extras e tipos incorretos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S046, V4B-S027, V4D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar qual camada bloqueou e qual propriedade foi realmente verificada.
- Não permitir bypass por retry, ferramenta alternativa ou saída parcial.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de resultados úteis e incorretos entregues, incluindo rejeições indevidas. Guardrails podem tornar uma aplicação pequena mais confiável no escopo, sem torná-la genericamente mais inteligente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T185, T197

## Fontes primárias associadas

### C-S046 — NeMo Guardrails

[https://github.com/NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ferramentas programáveis para impor controles a sistemas conversacionais; uso não substitui autorização no backend.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
