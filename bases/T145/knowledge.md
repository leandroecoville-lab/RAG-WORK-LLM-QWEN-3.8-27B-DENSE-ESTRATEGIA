# T145 — Adaptive Depth

**Nome canônico:** Adaptive Depth  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T145  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** profundidade adaptativa

## T145:C01 — conceito

Rótulo amplo para variar a profundidade de processamento conforme a tarefa. Neste inventário significa variar rodadas, etapas ou verificações do agente; não significa saltar camadas de qualquer transformer existente. Profundidade adicional só vale quando melhora o resultado de forma mensurável.

Como funciona:
- Estimar dificuldade ou detectar falha após uma primeira tentativa.
- Escolher entre encerrar, verificar ou expandir outra etapa.
- Parar por critério de qualidade, ganho marginal ou limite de orçamento.

## T145:C02 — aplicacao

Quando usar:
- Tarefas com dificuldade muito desigual.
- Possibilidade de testar se uma rodada adicional corrigiu algo concreto.

Quando não usar:
- Usar número fixo de reflexões apenas para aparentar análise profunda.

Implementação proposta:
- Definir níveis curtos, médios e extensos de execução.
- Avaliar política de passagem entre níveis em dados separados.
- Registrar contribuição de cada rodada e detectar repetição sem progresso.

Aplicação LAI proposta:
Proposta: a Helena expandir investigação apenas quando faltarem evidências ou um teste falhar, preservando respostas já aceitas.

## T145:C03 — riscos_validacao

Armadilhas:
- Indicador de dificuldade pode confundir texto longo com tarefa difícil.
- Rodadas extras podem degradar uma resposta inicialmente correta.

Métricas sugeridas:
- Qualidade versus número de etapas.
- Custo marginal de cada correção realmente obtida.

Testes propostos:
- Comparar profundidade fixa e adaptativa no mesmo teto de custo.
- Dar tarefa já resolvida e verificar encerramento sem revisões desnecessárias.

## T145:C04 — perguntas_proveniencia

Pergunta: Adaptive Depth reduz camadas do Qwen?
Resposta: Não nesta proposta; atua no workflow do agente.

Pergunta: Qual profundidade é ideal?
Resposta: Depende de tarefa e verificador e deve ser estimada por avaliação.

Pergunta: Uma resposta mais longa demonstra maior profundidade útil?
Resposta: Não. O ganho deve aparecer em evidências, hipóteses resolvidas ou resultados verificados, não em extensão textual.

Pergunta: Quando a política deve registrar inconclusão?
Resposta: Quando o objetivo permanece pendente e não há orçamento ou ação elegível que sustente nova etapa.

Escopo das fontes:
s1 sustenta o tema de orçamento em inferência; a política de profundidade de agente é uma proposta distinta, não o algoritmo do artigo.

## T145:C05 — mecanismo_avancado

Profundidade adaptativa pode usar o ganho observado entre etapas como sinal de continuidade: um novo teste elimina uma hipótese, uma busca resolve uma lacuna ou uma revisão corrige um defeito. Contar palavras de deliberação não mede esse ganho. Uma política proposta combina orçamento residual e evidência de progresso, reservando uma saída explícita quando a próxima rodada não tem uma operação verificável capaz de alterar a conclusão.

Condição de contorno:
Um sinal de progresso mal definido pode premiar reformulações repetidas e interromper cedo tarefas difíceis cujo benefício aparece apenas depois.

Contrato proposto:
- Entradas: Estado atual, critérios pendentes, custo da próxima etapa e limite global.
- Saídas: Continuar, concluir ou interromper com pendências identificadas.
- Estado: Profundidade percorrida, mudanças verificadas e recursos restantes.
- Invariante: Maior profundidade não substitui evidência de satisfação do requisito.

Compromissos de projeto:
- Parar cedo reduz desperdício e pode perder soluções de descoberta tardia.
- Manter exploração mínima melhora cobertura e aumenta custo em casos já resolvidos.

## T145:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: oferecer uma tarefa resolvida na primeira rodada e outra que exige buscar um dado ausente; verificar se a política diferencia conclusão de simples confiança declarada.

Plano de avaliação proposto:
Comparar número fixo de rodadas e política adaptativa sob o mesmo orçamento máximo. Estratificar por dificuldade medida independentemente. Avaliar sucesso, custo e interrupções prematuras; decidir pela fronteira entre qualidade e trabalho adicional, sem limiar universal.

Comparações:
- T146 (specializes): Profundidade controla número de etapas; adaptive compute também distribui largura, modelos e verificadores.
- T219 (complements): O limite global de passos encerra a execução; profundidade adaptativa decide como distribuir esforço dentro desse limite.

Afirmação rastreável:
O estudo de computação em inferência mostra que a utilidade das estratégias varia com a dificuldade da consulta.
Suporte: related; fontes: V3C-S003
Limite: Os experimentos de raciocínio não validam diretamente este detector de progresso para workflows.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T145:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 usou progresso verificável como sinal de continuidade. O aprofundamento separa limite de raciocínio do modelo, número de ações e profundidade do workflow, com orçamento reservado para concluir e verificar.

Três profundidades distintas
Tokens internos de reasoning, rodadas de ferramenta e caminhos no grafo não são intercambiáveis. Um modelo pode raciocinar muito sem obter informação nova; outro pode realizar várias leituras úteis com pouca geração. A política deve definir qual dimensão está controlando e medir o efeito de cada uma separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V4C-S019.

Parada compatível com o servidor
Um limiar de thinking pode ser aproximado e depender de delimitadores ou mecanismos específicos. Reserve espaço para a resposta final e trate corte prematuro como resultado incompleto. Não suponha que um parâmetro com nome semelhante tenha o mesmo comportamento em outro modelo, template ou backend.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018.

Próxima etapa com valor esperado
Antes de ampliar esforço, identifique uma ação que possa mudar a decisão e seu custo provável. Se faltam fontes, mais reasoning sobre os mesmos dados não cria evidência. Se há candidatos verificáveis, uma rodada adicional pode valer mais que aumentar o tamanho da resposta final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S003.

USO AVANÇADO — Resposta técnica com recuperação
Cenário: Perguntas variam entre busca factual e integração de condições.
Estratégia: Use esforço curto para localizar fatos; amplie somente quando existirem conflitos ou etapas dedutivas verificáveis. Se a fonte não responder, finalize insuficiência. Execute o verificador antes de consumir a reserva da resposta final.
Papel do modelo pequeno: 3–7B extrai; 8–14B integra poucas condições; 15–30B analisa exceções delimitadas.
Aceite proposto: Proposta: comparar matriz de orçamentos em perguntas reservadas, incluindo cortes de saída e afirmações sem fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V4C-S019.

USO AVANÇADO — Reparo com tentativas progressivas
Cenário: Um patch falha em testes e o erro se mantém.
Estratégia: Diferencie erro de formato, falha conhecida e ausência de progresso. Permita nova tentativa somente com diagnóstico diferente ou mudança concreta de estratégia; a tentativa seguinte recebe o orçamento restante, não o orçamento inicial.
Papel do modelo pequeno: 8–30B prepara candidatos de reparo enquanto ferramentas verificam comportamento.
Aceite proposto: Proposta: medir reparos aceitos por rodada e encerrar quando a política definida antes do teste não justificar continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: poucas decisões locais com saída curta; profundidade adicional só após sinal externo de necessidade.
8–14B: Proposta: orçamento de reasoning específico do checkpoint e loops limitados por teste.
15–30B: Proposta: revisão de casos mais complexos mantendo reserva explícita de verificação e síntese.
Requisitos de treino/runtime: Confirmar suporte e semântica do parâmetro; a banda de tamanho não define o orçamento adequado.
Não aplicar quando: Não ampliar profundidade quando falta informação externa ou quando o modelo repete a mesma conclusão sem nova evidência.

## T145:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: O modelo controla orçamento de thinking interno; isso é relacionado, mas não comprova profundidade de rodadas ou etapas do agente.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Nemotron 9B documenta mecanismo de orçamento; a documentação não comprova dez implantações de profundidade adaptativa nem ganhos gerais.
Consultas registradas: V4C-Q014, V4C-Q009.

## T145:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T145 → T168 [complements]
Como combinar: O limite suave dispara encerramento planejado antes do teto que pode truncar o resultado.
Interface: Consumo atual, reserva de saída e semântica do servidor.
Condição: O orçamento é medido na unidade correta.
Aceite proposto: Forçar limite próximo e exigir estado de conclusão coerente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T145 → T218 [feeds]
Como combinar: A política recebe sinais de estagnação para decidir se outra etapa é útil.
Interface: Mudança de artefato, teste e hipótese entre rodadas.
Condição: A tarefa admite medir progresso observável.
Aceite proposto: Comparar parada por teto com parada por falta de progresso em falhas conhecidas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S032, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar resposta truncada como tentativa semanticamente avaliada.
- Registrar esforço solicitado e efetivamente observado, incluindo excesso permitido pelo backend.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare curvas qualidade–custo por tarefa com um modelo de fronteira. Um ponto favorável em orçamento controlado não demonstra que mais tokens eliminem a diferença de capacidade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T146, T190, T201

## Fontes primárias associadas

### C-S012 — s1: Simple test-time scaling

[https://arxiv.org/abs/2501.19393](https://arxiv.org/abs/2501.19393)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de orçamento de computação em inferência; não prova que qualquer modelo melhora ao gerar mais texto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S003 — Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

[https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Efetividade de estratégias de computação em inferência varia com dificuldade; alocação adaptativa pode superar orçamento uniforme no estudo.

Limite: Experimentos não validam política universal para agentes, ferramentas ou cargas LAI.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
