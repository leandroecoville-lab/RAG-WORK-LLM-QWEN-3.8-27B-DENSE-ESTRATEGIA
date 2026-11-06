# T135 — Model Cascade

**Nome canônico:** Model Cascade  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T135  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cascata de modelos

## T135:C01 — conceito

Cascata executa modelos em sequência e decide, após cada resposta, se já existe qualidade suficiente ou se deve escalar. Diferencia-se do roteamento inicial porque consome o resultado de uma etapa para escolher a próxima. O custo inclui todas as etapas percorridas.

Como funciona:
- Consultar o estágio inicial de menor custo admissível.
- Validar a resposta por critérios externos ou estimativa calibrada.
- Encerrar quando aceita ou encaminhar ao próximo estágio dentro do orçamento.

## T135:C02 — aplicacao

Quando usar:
- Tarefas com verificador barato e objetivo.
- Muitos casos fáceis e uma minoria que exige modelo mais capaz.

Quando não usar:
- Quando quase todas as tarefas percorrem a cascata inteira ou o avaliador não distingue erros.

Implementação proposta:
- Definir estágios, saída padronizada e critério de aceite.
- Calibrar o limiar usando casos não utilizados para ajustar a política.
- Registrar custo acumulado, motivo de escalada e mudança de resposta.

Aplicação LAI proposta:
Proposta: testar extração estruturada local seguida de validação; escalar somente falhas de conteúdo ou incerteza real, sem repetir chamadas que já atenderam ao contrato.

## T135:C03 — riscos_validacao

Armadilhas:
- Confiança declarada pelo próprio modelo pode aceitar resposta errada.
- Vários estágios ampliam latência de cauda e custo de tarefas difíceis.

Métricas sugeridas:
- Fração resolvida em cada estágio.
- Custo e latência por resultado correto, comparados ao melhor destino único.

Testes propostos:
- Injetar resposta plausível porém errada no primeiro estágio e verificar a rejeição.
- Comparar a cascata em orçamento total equivalente ao baseline.

## T135:C04 — perguntas_proveniencia

Pergunta: Cascata sempre economiza?
Resposta: Não. Muitas escaladas podem custar mais que chamar diretamente o modelo final.

Pergunta: Um erro de rede é o mesmo que baixa qualidade?
Resposta: Não. Falhas operacionais e de conteúdo precisam de políticas separadas.

Pergunta: Uma primeira chamada barata sempre reduz a conta?
Resposta: Não. Seu custo soma-se ao avaliador e às escaladas; pode acrescentar despesa a todas as tarefas difíceis.

Pergunta: Devo passar a primeira resposta ao modelo seguinte?
Resposta: É uma opção experimental: comparar reaproveitamento com resolução independente para medir ancoragem e consumo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T135:C05 — mecanismo_avancado

Para uma cascata de dois modelos, um modelo simplificado de custo é E[C]=c₁+cᵥ+pₑ·c₂, onde c₁ e c₂ são custos médios das chamadas, cᵥ o custo de avaliação e pₑ a probabilidade de escalonamento. A fórmula exige explicitar se o segundo modelo recebe a primeira resposta, pois isso muda custo e pode propagar seu erro. A latência de quem escala inclui a etapa anterior, mesmo quando a média global diminui.

Condição de contorno:
Se a primeira etapa aceita erros difíceis de detectar ou quase todas as tarefas escalam, a economia prevista pode desaparecer.

Contrato proposto:
- Entradas: Pergunta, candidatos de modelos, contrato de aceitação e orçamento total.
- Saídas: Resposta aceita ou escalonamento, trilha de custos e resultados dos verificadores.
- Estado: Ordem da cascata, limiares e histórico de tentativas.
- Invariante: Cada nova etapa consome o orçamento remanescente e preserva a identidade da tarefa.

Compromissos de projeto:
- Um avaliador forte detecta mais erros, mas pode custar tanto quanto executar diretamente o modelo seguinte.
- Reutilizar a tentativa anterior economiza trabalho e pode ancorar o próximo modelo em uma conclusão errada.

## T135:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer respostas curtas e convincentes, porém incorretas, ao critério de aceitação; observar se erros atravessam a cascata sem escalonamento.

Plano de avaliação proposto:
Comparar execução direta, roteamento inicial e cascata com o mesmo conjunto. Medir falsa aceitação, custo completo e latência dos casos escalados. Separar custo do avaliador e dos modelos; decidir por qualidade exigida e distribuição real de escalonamento.

Comparações:
- T133 (alternative): Um roteador pode evitar pagar pela etapa inicial nas tarefas já reconhecidas como difíceis.

Afirmação rastreável:
FrugalGPT trata cascatas de modelos como estratégia de controle conjunto de custo e desempenho.
Suporte: direct; fontes: C-S002
Limite: A expressão de custo é uma simplificação editorial; dependências e custos condicionais precisam ser medidos.

Nota de pesquisa:
Contratos, testes e critérios são propostas editoriais; as fontes sustentam os mecanismos indicados.

## T135:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 formalizou custo esperado e propagação da primeira resposta. A camada nova usa cascatas por evidência e orçamento de erro, com transferência seletiva de artefatos entre estágios.

Portões heterogêneos
Não use um único escore de confiança em todos os estágios. Extração pode ser verificada por schema e localização; cálculo por execução; resposta documental por cobertura das fontes. A cascata só escala quando o verificador identifica uma lacuna específica que o estágio seguinte tem chance de resolver.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, C-S002.

Escalonar evidência, não persuasão
Prepare um pacote com entrada original, fatos confirmados, falhas do verificador e trechos necessários. A resposta anterior entra como candidato explicitamente falível. Em tarefas suscetíveis a ancoragem, execute a rota forte primeiro sem o candidato e compare depois; esse custo adicional precisa entrar na avaliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, C-S002.

Interrupção com resultado parcial
Reserve uma etapa de encerramento antes de consumir todo o orçamento. Ela identifica o que foi confirmado, o que ficou pendente e o motivo de parada. Um último modelo mais forte não deve ser iniciado quando o prazo restante não permite executar também sua verificação obrigatória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S011, V2A-S012.

USO AVANÇADO — Extração documental com resolução localizada
Cenário: Documentos contêm campos simples e poucas cláusulas ambíguas.
Estratégia: O modelo econômico extrai campos com referências; regras validam formato e consistência. Reenvie apenas cláusulas inconclusivas junto de contexto suficiente. Se a ambiguidade for documental, preserve-a em vez de continuar pagando por modelos maiores.
Papel do modelo pequeno: 3–7B executa extração fechada; 15–30B examina exceções com fontes.
Aceite proposto: Proposta: comparar custo total, campos corrigidos e erros introduzidos na escalada, sem esconder documentos abandonados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S002, V4C-S014.

USO AVANÇADO — Cascata de reparadores de CI
Cenário: Falhas de build incluem ajustes mecânicos e problemas semânticos.
Estratégia: Aplique reparadores determinísticos reconhecidos; encaminhe os demais a um modelo com escopo de arquivos restrito. Rode CI novamente e finalize após limite sem progresso. Nunca permita alterar código de produção apenas para contornar um teste válido.
Papel do modelo pequeno: 8–14B propõe reparos locais; 15–30B analisa dependências entre falhas.
Aceite proposto: Proposta: medir correções aceitas, regressões e alterações fora do escopo em falhas reais retidas da calibração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: primeiro estágio para respostas curtas verificáveis e seleção de regras mecânicas.
8–14B: Proposta: resolver exceções locais depois de receber diagnósticos concretos, sem revisar tudo novamente.
15–30B: Proposta: último estágio local para integração de evidências, com possibilidade explícita de encaminhar além da banda.
Requisitos de treino/runtime: O verificador precisa detectar erro relevante melhor que mera autoconfiança; contabilizar todos os estágios.
Não aplicar quando: Não usar quando quase toda tarefa exige a rota forte ou quando o verificador aprova sistematicamente respostas erradas.

## T135:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean mostra cascata de reparadores, não prova uma cascata universal de tamanhos de LLM. Bedrock routing é recurso distinto de cascata pós-resposta.
Consultas registradas: V4C-Q008, V4C-Q009, V4C-Q006.

## T135:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T135 → T200 [complements]
Como combinar: O portão precisa de evidência separada para decidir se continua.
Interface: Resultado por critério, falha localizada e artefato avaliado.
Condição: A independência exigida é funcional; erro correlacionado deve ser medido.
Aceite proposto: Testar candidatos plausíveis mas incorretos e observar escalonamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S002, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T135 → T220 [complements]
Como combinar: Falhas reconhecidas alimentam reparo de chamada antes de trocar de modelo.
Interface: Erro tipado, argumentos originais e schema vigente.
Condição: Não existe efeito remoto ainda desconhecido.
Aceite proposto: Confirmar que reparar formato não cria nova intenção de negócio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009, V3C-S038. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Impedir que cada estágio reinicie o orçamento da tarefa.
- Separar rejeição por falta de evidência de rejeição por indisponibilidade operacional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare cascata com fronteira fixa na mesma carga e com todas as tarefas contabilizadas. Economia média pode esconder latência pior e erros concentrados em casos difíceis.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T133, T136, T190

## Fontes primárias associadas

### C-S002 — FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

[https://arxiv.org/abs/2305.05176](https://arxiv.org/abs/2305.05176)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cascatas de modelos e decisões de encaminhamento podem ser otimizadas sob orçamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S001 — RouteLLM — repository and threshold calibration

[https://github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Calibração de limiares depende da distribuição de consultas e da fração pretendida de chamadas ao modelo forte.

Limite: README em branch mutável; exemplos numéricos não são limiares recomendados para LAI.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S011 — Understanding intelligent prompt routing in Amazon Bedrock

[https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso de roteamento entre dois modelos de uma família, critérios de qualidade e fallback; não prova uso por cliente específico.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S038 — LangChain — Prebuilt middleware

[https://docs.langchain.com/oss/python/langchain/middleware/built-in](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Middleware de erro de ferramenta é distinto de retry; ordem de composição determina tratamento de exceções e limites.

Limite: Documentação dinâmica com requisitos de versão; não se pressupõe disponibilidade de classes no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
