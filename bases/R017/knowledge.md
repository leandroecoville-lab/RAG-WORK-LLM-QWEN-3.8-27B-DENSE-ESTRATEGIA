# R017 — LangChain

**Nome canônico:** LangChain  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R017  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** LangChain agents; langchain.agents.create_agent

## R017:C01 — conceito

LangChain oferece componentes e uma interface de alto nível para construir agentes a partir de modelo, ferramentas, prompt e middleware. A documentação atual destaca create_agent como ponto de composição. LangGraph fornece a camada de orquestração associada; nenhuma dessas abstrações dispensa definir dados, contratos, persistência e critérios de qualidade da aplicação.

Como funciona:
- O ciclo alterna chamadas de modelo e execução de ferramentas, mantendo mensagens e estado da interação.
- Middleware pode ajustar comportamento e contexto em pontos do ciclo; integrações conectam provedores e recursos.
- Memória por conversa depende do estado e de um checkpointer configurado; duração do armazenamento varia conforme o backend.

Nota de nomenclatura: A ficha usa a documentação atual de create_agent; exemplos de APIs antigas precisam ser conferidos antes de migração.

## R017:C02 — aplicacao

Quando usar:
- Aplicações que precisam integrar modelos e ferramentas com interfaces comuns.
- Prototipagem de agentes de recuperação ou extração com controle explícito do ciclo.

Quando não usar:
- Quando uma função determinística simples resolve a tarefa sem benefício demonstrado de um agente.

Implementação proposta:
- Proposta: fixar versões do framework e das integrações; selecionar um modelo que suporte as operações necessárias.
- Implementar uma ferramenta de busca que devolva texto, identificadores e fontes, preservando erros e ausência de resultado.
- Adicionar persistência apenas com escopo definido por conversa e usuário; limitar passos e validar saídas fora do modelo.

Aplicação LAI proposta:
Proposta LAI: comparar um agente LangChain com a implementação RAG direta em consultas equivalentes, medindo manutenção e qualidade antes de acrescentar camadas.

## R017:C03 — riscos_validacao

Armadilhas:
- A interface comum não torna iguais capacidades, parâmetros e formatos de ferramentas de todos os provedores.
- Um checkpointer em memória não comprova recuperação após reinício; abstrações podem ocultar chamadas extras e retries.

Métricas sugeridas:
- Acerto por tarefa, chamadas por resposta, falhas de ferramenta, latência e precisão das evidências recuperadas.

Testes propostos:
- Proposta: testar ferramenta com sucesso, vazio e erro; verificar que o agente não inventa resultados.
- Reiniciar com o armazenamento escolhido e testar isolamento entre threads, limites do loop e recuperação do estado correto.

## R017:C04 — perguntas_proveniencia

Pergunta: LangChain e LangGraph são sinônimos?
Resposta: Não. LangChain oferece composição de agentes e integrações; LangGraph é uma camada de orquestração para controle mais detalhado.

Pergunta: Instalar LangChain cria um RAG completo?
Resposta: Não. Fontes, ingestão, recuperação, montagem de contexto, validação e avaliação precisam ser definidos na aplicação.

Pergunta: Mensagem de erro ao modelo prova que houve retry?
Resposta: Não. O traço precisa registrar tentativas efetivas; feedback e repetição são mecanismos diferentes.

Pergunta: Por que medir chamadas fora do contador de turnos?
Resposta: Uma chamada lógica pode envolver retries ou fallback, aumentando custo e efeitos sem acrescentar turno visível.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R017:C05 — mecanismo_avancado

A composição de middleware no LangChain precisa ser avaliada pela ordem efetiva dos envoltórios. Transformar uma exceção de ferramenta em mensagem para o modelo pode impedir que uma camada externa de retry veja a falha. A documentação distingue ToolErrorMiddleware, que oferece feedback, de ToolRetryMiddleware, que repete a operação. Na composição descrita, o retry fica internamente e deve propagar o erro final quando outra camada o tratará. Limites de chamadas, fallback e resumo também alteram o caminho observado; contar somente turnos do agente oculta tentativas adicionais do provedor ou da ferramenta.

Condição de contorno:
Uma interface comum não uniformiza erros, cancelamento ou capacidades dos provedores. Ordem válida para um conjunto de middlewares não é regra universal para qualquer extensão.

Contrato proposto:
- Entradas: Versões das integrações, ordem dos middlewares, taxonomia de erros e orçamento por operação.
- Saídas: Resultado tipado, erro terminal ou feedback ao modelo, com tentativas identificadas.
- Estado: Contadores por chamada lógica e tentativa, contexto aplicado e provedor efetivamente utilizado.
- Invariante: Nenhuma exceção absorvida é simultaneamente registrada como sucesso da ferramenta; retries permanecem contabilizados.

Compromissos de projeto:
- Feedback permite recuperação contextual, mas pode induzir o modelo a repetir uma operação já parcialmente executada.
- Retry automático reduz falhas transitórias, mas a ordem errada altera limites e diagnóstico.

## R017:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ferramenta falha transitoriamente duas vezes. Inverter os envoltórios e observar quais exceções chegam ao retry; exigir número de tentativas e resultado coerentes com a configuração declarada.

Plano de avaliação proposto:
Comparar composição mínima e completa com respostas de ferramenta controladas. Medir chamadas reais, custo, latência e recuperação correta; justificar cada middleware pelo efeito observado, sem assumir benefício cumulativo.

Comparações:
- R008 (complements): LangGraph fornece mecanismos de execução e estado; o middleware modifica pontos específicos do ciclo do agente.
- T136 (complements): Fallback seleciona alternativa, enquanto middleware define como falhas e limites atravessam o ciclo.

Afirmação rastreável:
ToolErrorMiddleware converte erros em feedback para o agente e não repete automaticamente a ferramenta.
Suporte: direct; fontes: V3C-S038
Limite: A interação exata com retry depende da ordem, política de falha e versão dos middlewares.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R017:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a ordem dos middlewares com contabilidade de tentativas aninhadas, contratos de adaptadores e diagnóstico da camada responsável por falhas.

Tentativa lógica e física
Proposta: atribuir um ID à operação lógica e outro a cada tentativa de provedor ou ferramenta. Consolidar duração, tokens e efeitos numa árvore de tentativas. Um middleware que oculta a exceção não deve apagar o custo nem transformar tentativa interrompida em sucesso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S038, V2B-S004, V4C-S012.

Adaptador sob teste
Construir testes de contrato por provedor para ferramenta inexistente, argumentos inválidos, saída truncada, cancelamento e erro transitório. A mesma interface Python não assegura a mesma semântica. Registrar quais capacidades foram verificadas na combinação exata de modelo e adaptador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S038, V2B-S004, V4C-S012.

Deadline único
Propagar tempo restante e teto de tentativas através da composição. Cada camada decide usando orçamento residual, não seu timeout original. Registrar a justificativa de fallback permite separar indisponibilidade, recusa por contrato e insuficiência de qualidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S038, V2B-S004, V4C-S012.

USO AVANÇADO — Gateway de dois modelos pequenos
Cenário: Uma tarefa estruturada pode usar duas famílias de modelos.
Estratégia: Normalizar apenas campos comprovadamente equivalentes e recusar rotas que não preservem o contrato.
Papel do modelo pequeno: Produzir conteúdo do domínio; o adaptador trata diferenças de protocolo.
Aceite proposto: Testar cancelamento e truncamento em ambos, medindo resultados aceitos e custo agregado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S038, V2B-S004, V4C-S012.

USO AVANÇADO — Ferramenta com erro recuperável
Cenário: Falha de argumento precisa voltar ao agente sem duplicar efeitos.
Estratégia: Reparar o argumento em etapa separada; retry de transporte conserva a identidade lógica.
Papel do modelo pequeno: Corrigir o campo rejeitado, com limite de tentativas e schema atual.
Aceite proposto: Injetar falha após confirmação remota e garantir consulta/reconciliação antes de nova mutação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S038, V2B-S004, V4C-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: contratos estreitos e mensagens de erro curtas, sem exceções brutas extensas.
8–14B: 8–14B: reparo limitado de argumentos e seleção entre ferramentas verificadas.
15–30B: 15–30B: usar somente se a ambiguidade da tarefa justificar custo adicional medido.
Requisitos de treino/runtime: Compatibilidade depende das versões de bibliotecas, adaptadores e recursos do provedor.
Não aplicar quando: Não assumir que trocar o nome do modelo mantém ferramentas, streaming e limites idênticos.

## R017:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: As buscas verificaram relatos e frameworks relacionados. Uso de agentes, LangGraph ou interface comum não comprova automaticamente adoção de toda a biblioteca LangChain.
Consultas registradas: V4C-Q010, V4C-Q021, V4C-Q026.

## R017:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R017 → T170 [complements]
Como combinar: Executar contrato da ferramenta na versão que o middleware realmente envia.
Interface: Versão, schema normalizado e capacidades verificadas.
Condição: Há migração de provedor ou de ferramenta.
Aceite proposto: Payload incompatível falha antes de uma mutação externa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S038, V2B-S004, V4C-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R017 → T136 [complements]
Como combinar: Fazer fallback consumir o orçamento lógico compartilhado.
Interface: Tentativas consumidas, deadline e motivo de falha.
Condição: Mais de um backend é elegível.
Aceite proposto: Falhas aninhadas respeitam o teto global e preservam o requisito de saída.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S038, V2B-S004, V4C-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar somente a última chamada no custo da tarefa.
- Não converter toda exceção em instrução para tentar novamente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar modelos com a mesma composição e incluir todas as tentativas. Uma melhoria causada por retry extra deve aparecer separada da qualidade do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R008, T009, T024, T027, T060, T140, T154, T219

## Fontes primárias associadas

### V2B-S004 — LangChain overview

[https://docs.langchain.com/oss/python/langchain/overview](https://docs.langchain.com/oss/python/langchain/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: create_agent, composição de modelo, ferramentas, prompt e middleware; distinção entre LangChain, LangGraph e Deep Agents.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S038 — LangChain — Prebuilt middleware

[https://docs.langchain.com/oss/python/langchain/middleware/built-in](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Middleware de erro de ferramenta é distinto de retry; ordem de composição determina tratamento de exceções e limites.

Limite: Documentação dinâmica com requisitos de versão; não se pressupõe disponibilidade de classes no ambiente do usuário.

### V4C-S012 — Navigating the LLM Landscape: Uber’s Innovation with GenAI Gateway

[https://www.uber.com/us/en/blog/genai-gateway/](https://www.uber.com/us/en/blog/genai-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gateway interno com adaptadores de modelos, interface unificada, controle de acesso e atribuição de consumo.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
