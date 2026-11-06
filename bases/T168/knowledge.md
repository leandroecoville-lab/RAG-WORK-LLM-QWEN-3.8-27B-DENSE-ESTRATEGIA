# T168 — Soft Limit / Hard Limit de tokens

**Nome canônico:** Soft Limit / Hard Limit de Tokens  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T168  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limites suave e rígido de tokens; Soft Limit / Hard Limit de Tokens

## T168:C01 — conceito

Dois níveis de orçamento: limite suave aciona redução de contexto ou checkpoint; limite rígido impede exceder uma fronteira. Podem ser definidos por chamada ou missão. É necessário distinguir orçamento escolhido pela aplicação do máximo técnico aceito pelo modelo e pelo servidor.

Como funciona:
- Contabilizar consumo acumulado e estimar próximo passo.
- Ao atingir limite suave, resumir estado ou reduzir material opcional.
- Ao atingir limite rígido, encerrar ou recusar nova etapa com status explícito.

## T168:C02 — aplicacao

Quando usar:
- Missões longas com expansão imprevisível do histórico.
- Contratos de custo ou latência que exigem teto verificável.

Quando não usar:
- Interromper no meio de uma mutação sem mecanismo para verificar seu resultado.

Implementação proposta:
- Reservar espaço para mensagem final e persistência do estado.
- Definir limites de entrada, saída e total de missão separadamente.
- Considerar chamadas de especialistas, retries e ferramentas no orçamento total.

Aplicação LAI proposta:
Proposta: a Helena salvar estado antes de esgotar contexto, permitindo retomar com referências e orçamento novo autorizado pela política da missão.

## T168:C03 — riscos_validacao

Armadilhas:
- Aviso suave ignorado deixa o agente sem espaço para concluir.
- Corte rígido pode produzir JSON incompleto e não desfaz ações já realizadas.

Métricas sugeridas:
- Missões que atingem cada limite e taxa de retomada.
- Overflow técnico e custo excedido por erro de contagem.

Testes propostos:
- Forçar limite suave e verificar checkpoint contendo próximos passos e evidências.
- Atingir limite rígido e exigir saída incompleta explícita sem falsa conclusão.

## T168:C04 — perguntas_proveniencia

Pergunta: Soft limit é uma capacidade do modelo?
Resposta: É uma política da aplicação, salvo recurso específico do backend.

Pergunta: Hard limit garante resposta completa?
Resposta: Não. Precisa de reserva e tratamento de truncamento.

Pergunta: Por que não compactar somente ao atingir o máximo?
Resposta: Porque a própria operação ou resultados ainda em voo podem precisar de espaço que já não existe.

Pergunta: Limite suave deve ser um percentual fixo?
Resposta: Não necessariamente. O tamanho da próxima etapa e o custo de recuperação podem ser mais informativos que uma fração constante.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T168:C05 — mecanismo_avancado

Um limite suave precisa deixar margem para a ação corretiva que aciona. Compactar, gerar um handoff ou receber uma ferramenta em andamento também consome contexto; disparar a recuperação no último token disponível pode torná-la impossível. A margem pode considerar distribuição de crescimento por etapa e diferença entre contagem estimada e observada. O limite rígido continua sendo uma fronteira de rejeição, não uma rotina de recuperação.

Condição de contorno:
Se a próxima unidade obrigatória já excede a capacidade restante, apenas elevar o limiar suave não torna a chamada viável.

Contrato proposto:
- Entradas: Ocupação estimada, crescimento pendente, capacidade e custo da recuperação.
- Saídas: Continuar, compactar, dividir ou interromper com estado preservado.
- Estado: Margem reservada, picos observados e gatilhos já acionados.
- Invariante: A ação de recuperação deve caber antes do limite rígido ou usar procedimento externo compatível.

Compromissos de projeto:
- Margem ampla reduz emergências e diminui espaço útil para evidência.
- Gatilhos adaptativos acompanham variabilidade e podem oscilar sem histerese ou controle de reentrada.

## T168:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: entregar resultado grande enquanto uma compactação é planejada; verificar que a reserva inclui o material pendente e evita repetidas compactações sem ganho.

Plano de avaliação proposto:
Comparar limiares fixos e margens baseadas em tamanhos observados. Controlar ferramentas e modelos. Medir estouros, recuperação concluída, informação preservada e compactações redundantes. Definir fronteiras por carga e custo de continuidade.

Comparações:
- T152 (complements): A alocação distribui cotas; os limites determinam quando mudar de estratégia.
- T212 (complements): Auto-compact é uma resposta possível ao gatilho suave, não sua definição completa.

Afirmação rastreável:
A contagem antecipada pode considerar mensagens e ferramentas estruturadas para orientar tamanho de entrada.
Suporte: related; fontes: V3C-S022
Limite: As fronteiras suave/rígida e a reserva de recuperação são desenho editorial, não comportamento universal do endpoint.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T168:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 enfatizava margem para recuperação. Esta camada diferencia limite de raciocínio, resposta, contexto e consumo acumulado, com uma política de degradação que termina em artefato útil e verificável.

Quatro fronteiras distintas
Mantenha contadores para entrada total, saída visível, raciocínio quando exposto pelo backend e orçamento da missão. Um teto de saída não impede o histórico de crescer; uma janela disponível não autoriza gastar indefinidamente. Expresse qual limite é imposto pelo servidor e qual é apenas gatilho do controlador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V3C-S022.

Limite suave condicionado
O ponto de ação deve depender do próximo passo. Receber um log grande exige margem diferente de emitir JSON curto. Antes de chamar ferramenta com saída imprevisível, negocie paginação ou projeção; se não existir limite de payload, o controlador precisa tratar o resultado fora da janela antes de apresentá-lo ao modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V4C-S018.

Finalização reservada
Reserve capacidade para registrar estado, evidências e pendências. A resposta final parcial deve distinguir o que foi verificado do que ficou sem executar. Cortar no meio de uma chamada de ferramenta ou de um JSON pode deixar artefato inutilizável; trate truncamento como falha de contrato e preserve o último resultado confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S022, V4C-S018.

USO AVANÇADO — Modelo de raciocínio local
Cenário: Um 9B pode consumir orçamento em raciocínio antes de responder.
Estratégia: Teste limites com o backend real e observe a diferença entre pedido de interrupção e término efetivo. A documentação Nemotron mostra controle específico de thinking; não suponha que o parâmetro seja uma barreira rígida idêntica em todos os servidores. Defina reserva para a saída validável.
Papel do modelo pequeno: 8–14B executa raciocínio delimitado; um controlador externo contabiliza a conclusão.
Aceite proposto: Proposta: taxa de respostas completas, consumo acima do alvo e qualidade por faixa de orçamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V4C-S019.

USO AVANÇADO — Análise de repositório extensa
Cenário: O agente se aproxima do limite antes de terminar o patch.
Estratégia: Interrompa expansão de arquivos, salve a revisão e um plano de continuação, e valide o que já foi editado. Uma nova sessão recebe apenas objetivos pendentes e referências. Não declare concluído porque o limite rígido encerrou a geração.
Papel do modelo pequeno: 3–7B atua em trechos; 15–30B integra lotes com reservas explícitas.
Aceite proposto: Proposta: retomada sem perder alterações confirmadas e sem aceitar JSON ou patch truncado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Saídas curtas e schemas simples reduzem risco de consumir a reserva de finalização.
8–14B: Raciocínio condicionado ao orçamento, medido no backend que realmente servirá o modelo.
15–30B: Dividir análises longas em estágios com checkpoint e critérios de integração.
Requisitos de treino/runtime: Contador por tokenizer, telemetria do provedor e tratamento de finish reason; margem baseada em payload observado.
Não aplicar quando: Não tratar orçamento de thinking como limite universal nem compactar quando já não cabe a própria compactação.

## T168:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: Limiar de thinking e limite final de geração têm semânticas diferentes.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Nemotron oferece evidência direta de modelo dentro da faixa pedida e controles documentados; implantação específica e ganhos locais não foram demonstrados.
Consultas registradas: V4C-Q014, V4C-Q027.

## T168:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T168 → T222 [feeds]
Como combinar: Publicar consumo e margem para disparar ação antes do limite rígido.
Interface: Contadores por categoria e estimativa do próximo payload.
Condição: Medidas distinguem uso observado de previsão.
Aceite proposto: Gatilho ocorre com espaço para a ação corretiva escolhida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T168 → T211 [complements]
Como combinar: Ao atingir limite suave, gerar passagem de estado antes de perder a capacidade de registrar pendências.
Interface: Objetivos, revisão, artefatos e próximo passo.
Condição: Handoff precisa ser validado e persistido antes do encerramento.
Aceite proposto: Nova sessão retoma sem inventar conclusão das etapas ausentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Timeout, limite de tokens e término normal precisam de estados diferentes.
- Uma saída válida sintaticamente ainda pode ter omitido requisito para caber no teto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare curvas de qualidade por orçamento em vez de uma única configuração. O 9B documentado é recurso concreto, mas sua existência não demonstra equivalência geral a modelos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T043, T060, T152, T176

## Fontes primárias associadas

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
