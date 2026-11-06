# T055 — Procedural Memory

**Nome canônico:** Procedural Memory  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T055  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** memória procedural; memória de procedimentos

## T055:C01 — conceito

Armazena como executar atividades: sequências, condições, ferramentas, critérios de conclusão e estratégias. Pode ser representada por workflows ou skills recuperáveis. Não é apenas uma descrição conceitual; precisa de passos aplicáveis e condições nas quais o procedimento foi validado.

Como funciona:
- Identificar um procedimento a partir de especificação ou experiências.
- Definir pré-condições, ações e verificações.
- Recuperar a versão adequada e avaliar o resultado de sua aplicação.

## T055:C02 — aplicacao

Quando usar:
- Tarefas recorrentes de diagnóstico, extração ou validação.
- Padronização do trabalho entre agentes e modelos.

Quando não usar:
- Não promover uma sequência que funcionou uma vez a procedimento universal.

Implementação proposta:
- Proposta: associar skill a versão de ferramenta e ambiente.
- Incluir tratamento de falha, efeitos e critérios de parada.
- Manter exemplos de uso correto e situações em que o procedimento não se aplica.

Aplicação LAI proposta:
Proposta LAI: transformar correções comprovadas da Helena em skills com contrato e avaliação; conhecimento textual sozinho não prova execução competente.

## T055:C03 — riscos_validacao

Armadilhas:
- Procedimento pode envelhecer quando uma API muda.
- Um agente pode seguir etapas mecanicamente apesar de pré-condições falsas.

Métricas sugeridas:
- Conclusão correta por procedimento e versão.
- Falhas de pré-condição detectadas antes da execução.

Testes propostos:
- Executar em cenário compatível e em cenário incompatível conhecido.
- Alterar schema da ferramenta e exigir bloqueio ou migração do procedimento.

## T055:C04 — perguntas_proveniencia

Pergunta: Uma skill é aprendizado nos pesos?
Resposta: Não necessariamente. Ela pode ser memória procedural externa carregada sob demanda.

Pergunta: Procedimentos precisam explicar por quê?
Resposta: Uma justificativa curta e limites de aplicação ajudam a reconhecer quando adaptar ou interromper os passos.

Pergunta: Um procedimento deve incluir rollback?
Resposta: Quando aplicável, descreva compensação e limites. Nem todo efeito pode ser revertido, e executar uma compensação também exige verificar o estado externo.

Pergunta: Como aprender com um único sucesso?
Resposta: Registre uma receita candidata com escopo estreito. Amplie sua recomendação somente depois de testar variações e situações em que não deve ser usada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T055:C05 — mecanismo_avancado

Memória procedural pode armazenar receita, política de decisão ou código executável; essas representações exigem controles diferentes. Uma sequência textual ensina o agente a escolher ações, enquanto um workflow implementado restringe transições. Promover uma experiência a procedimento exige identificar quais pré-condições causaram seu sucesso e quais passos foram apenas circunstanciais. Compatibilidade deve ser verificada no momento de uso, não apenas na data de publicação.

Condição de contorno:
Um procedimento perde aplicabilidade quando depende de permissão, versão ou estado externo diferente daquele em que foi validado, mesmo que seu objetivo permaneça igual.

Contrato proposto:
- Entradas: Objetivo, pré-condições, ferramentas compatíveis, passos e evidências de validação do procedimento.
- Saídas: Versão selecionada com critérios de sucesso, pontos de decisão e tratamento de falhas.
- Estado: Histórico de revisão, dependências e registros de execução sob condições conhecidas.
- Invariante: Selecionar uma receita não autoriza efeitos externos nem prova que suas pré-condições estão satisfeitas.

Compromissos de projeto:
- Receitas flexíveis transferem conhecimento e deixam decisões ao modelo.
- Workflows explícitos facilitam validação e exigem manutenção quando mudam ferramentas, contratos ou condições de operação.

## T055:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar o schema de uma ferramenta mantendo o nome. A seleção deve detectar a dependência incompatível e exigir adaptação validada, sem continuar reproduzindo argumentos antigos.

Plano de avaliação proposto:
Avaliação proposta: comparar orientação livre, procedimento textual e workflow em tarefas equivalentes. Medir cumprimento das pré-condições, conclusão verificável, falhas recuperadas e custo de adaptação; separar sucesso por execução correta de sucesso por acaso.

Comparações:
- T046 (complements): Demonstrações mostram casos; procedimentos explicitam condições e sequência reutilizável que os casos podem ilustrar.
- T071 (complements): Promoção decide quando um aprendizado candidato pode tornar-se procedimento recomendado.

Afirmação rastreável:
A especificação Agent Skills organiza instruções e recursos que podem ser carregados progressivamente para tarefas especializadas.
Suporte: related; fontes: V3A-S018
Limite: Esse formato fornece embalagem e descoberta; não garante execução correta, autorização ou validade permanente do procedimento.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T055:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu receita e workflow. Aqui procedimentos são recuperados por pré-condição e adaptados somente em pontos explicitamente variáveis.

Projeto e decomposição
Divida procedimento em invariantes e parâmetros. Caminhos, versões e limites podem variar; uma verificação obrigatória não deve desaparecer durante adaptação para outro projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

Controle adaptativo
Antes de executar, comparar ambiente observado com pré-condições. Quando incompatível, registrar necessidade de adaptação e testar em contexto limitado, evitando improvisar uma nova receita sob o mesmo nome.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

Validação contrafactual
Compare seleção por título e por pré-condições. Meça procedimento inadequado escolhido, adaptações indevidas e conclusão verificada; instrução lida não equivale a execução bem-sucedida. Unidade de avaliação: procedimento em contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

USO AVANÇADO — Rotina de manutenção
Cenário: Mesma tarefa ocorre em versões distintas.
Estratégia: Recuperar procedimento compatível, preencher parâmetros com dados observados e testar passo reversível antes de continuar.
Papel do modelo pequeno: 3–7B preenche parâmetros; 8–14B verifica.
Aceite proposto: Nenhuma etapa pode usar parâmetro inventado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

USO AVANÇADO — Aprendizado de nova rotina
Cenário: Um incidente gerou solução candidata.
Estratégia: Extrair pré-condições e falhas conhecidas, repetir em caso controlado e promover somente após evidência de transferência.
Papel do modelo pequeno: 15–30B analisa adaptação.
Aceite proposto: Não generalizar solução de um caso para todos os ambientes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V2A-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de procedimento curto com parâmetros e verificações explícitas.
8–14B: Avaliador de compatibilidade do ambiente e exceções locais.
15–30B: Adaptador de rotina com mudanças justificadas e validação independente.
Requisitos de treino/runtime: Procedimento versionado, precondições verificáveis e registro do que foi executado; ajuste de pesos é opcional.
Não aplicar quando: Ambiente não satisfaz pré-condições ou faltam ferramentas necessárias ao teste de aceite.

## T055:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T055:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T055 → T045 [requires]
Como combinar: Carregar ferramentas compatíveis com a rotina.
Interface: Capacidades, schemas e versões exigidas.
Condição: Ferramentas disponíveis no ambiente atual.
Aceite proposto: Substituir ferramenta por versão incompatível e exigir bloqueio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V2A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T055 → T195 [complements]
Como combinar: Verificar resultado por execução observável.
Interface: Passo, saída esperada e resultado real.
Condição: Teste medir propriedade relevante.
Aceite proposto: Detectar rotina que termina sem produzir artefato correto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V2A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir memória de procedimento com autorização para efeitos.
- Não ocultar adaptação sob identidade da versão original.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar execução fiel em ambientes novos; decorar passos não demonstra capacidade de adaptação geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T071, T204

## Fontes primárias associadas

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V2A-S016 — How Claude remembers your project

[https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instruções persistentes em arquivos e memória automática; escopo e carregamento dependem da configuração.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
