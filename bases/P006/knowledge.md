# P006 — Progressive Loader

**Nome canônico:** Progressive Loader  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** carregador progressivo proposto

## P006:C01 — conceito

Progressive Loader é um componente editorial proposto para expor primeiro metadados baratos e carregar conteúdo completo somente quando necessário. A ideia pode ser aplicada a skills, ferramentas, documentos e memória. Sua existência na LAI não foi verificada; as fontes descrevem divulgação progressiva e recuperação de definições, sem estabelecer este nome como padrão técnico universal.

Como funciona:
- Manter um catálogo de identificadores, descrições, versões e tamanhos, separado do conteúdo integral.
- Selecionar candidatos relevantes à tarefa, abrir o recurso principal e expandir dependências apenas quando necessárias.
- Reutilizar conteúdo carregado na mesma versão, respeitando orçamento total e limite de profundidade.

## P006:C02 — aplicacao

Quando usar:
- Acervos extensos de procedimentos e ferramentas em que enviar todas as definições consumiria a maior parte do contexto.

Quando não usar:
- Quando uma regra obrigatória para interpretar a tarefa seria omitida pelo catálogo ou quando a descoberta é insuficientemente confiável.

Implementação proposta:
- Proposta: definir estados descoberto, selecionado, carregado e invalidado, com manifesto por chamada.
- Preservar identificadores retornados pelo catálogo; validar acesso e versão ao resolver referências, sem fabricar caminhos por similaridade de nome.
- Carregar instruções específicas antes da ação que dependa delas; se faltar um recurso necessário, registrar dependência não satisfeita.

Aplicação LAI proposta:
Proposta LAI: oferecer descoberta leve a P001 e P003, carregar procedimentos sob demanda e registrar quais versões efetivamente orientaram cada ação.

## P006:C03 — riscos_validacao

Armadilhas:
- Uma descrição inadequada pode impedir que o recurso certo seja escolhido, apesar de existir.
- Referências circulares geram expansão infinita sem detecção de recursos já visitados.
- Catálogo e conteúdo podem mudar em momentos distintos; a mesma descrição não garante o mesmo procedimento.

Métricas sugeridas:
- Tokens iniciais e expandidos, acerto de seleção, latência de abertura e dependências ausentes.

Testes propostos:
- Aceite proposto: usar duas ferramentas com nomes próximos e verificar seleção e carregamento da definição correta.
- Testar recurso removido, atualização de versão e ciclo de referências; exigir parada finita e diagnóstico da dependência.

## P006:C04 — perguntas_proveniencia

Pergunta: Carregar metadados basta para executar uma ferramenta?
Resposta: Somente se o contrato completo necessário já estiver disponível; caso contrário, a definição deve ser carregada antes da execução.

Pergunta: Como evitar expansão recursiva sem fim?
Resposta: Registrar IDs e versões visitados, limitar profundidade e orçamento e interromper ciclos com uma dependência explícita.

Pergunta: Qual é o custo escondido do carregamento progressivo?
Resposta: Seleção errada, ida adicional ao armazenamento e expansão que consome o orçamento economizado.

Pergunta: Quando o recurso pode ser reutilizado?
Resposta: Quando versão, autorização e finalidade permanecem compatíveis com a requisição atual.

Escopo das fontes:
Fontes sustentam divulgação progressiva; estados, manifesto e limites são critérios de projeto propostos.

## P006:C05 — mecanismo_avancado

Progressive Loader propõe carregar primeiro descrições suficientes para selecionar um recurso e depois seu conteúdo específico. Metadados devem incluir versão e referência estável, permitindo verificar que o corpo carregado corresponde ao item escolhido. O loader precisa contabilizar o custo adicional de schemas e instruções após a seleção. Conteúdo recuperado de um arquivo ou ferramenta permanece dado de sua origem; o carregamento não lhe concede autoridade para alterar políticas da aplicação.

Condição de contorno:
Uma descrição ruim pode esconder o recurso correto. Se a seleção falhar, carregar menos conteúdo aumenta economia e também reduz capacidade de concluir a tarefa.

Contrato proposto:
- Entradas: Catálogo autorizado, consulta, descrições resumidas, referências versionadas e orçamento disponível para expansão.
- Saídas: Conteúdo necessário, identidade verificada, custo de carga e indicação de recurso ausente ou incompatível.
- Estado: Cache de descrições e corpos por versão, recursos ativos e histórico mínimo de decisões de seleção.
- Invariante: O corpo carregado deve corresponder à identidade selecionada; conteúdo novo não pode exceder silenciosamente o orçamento restante.

Compromissos de projeto:
- Descrições curtas reduzem tokens iniciais, mas precisam preservar sinais que distinguem recursos parecidos.
- Cache local reduz leituras repetidas, porém exige invalidação quando a versão ou autorização muda.

## P006:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: alterar um recurso entre seleção e leitura e incluir instruções maliciosas no corpo; exigir detecção de versão divergente e manutenção da hierarquia de instruções.

Plano de avaliação proposto:
Comparar catálogo integral e carregamento progressivo com tarefas que exigem ferramentas frequentes e raras. Medir seleção correta, tokens totais incluindo expansão, leituras extras e conclusão comprovada, não apenas redução do prompt inicial.

Comparações:
- T014 (specializes): Materializa divulgação progressiva de informação.
- T151 (complements): Pode carregar schemas de ferramentas somente quando necessários.

Afirmação rastreável:
Documentação de Agent Skills descreve divulgação progressiva de instruções e recursos.
Suporte: related; fontes: C-S052
Limite: O componente, suas verificações de versão e seu contrato são recomendações editoriais.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P006:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou seleção e identidade. Aqui Progressive Loader é proposto com carregamento de dependências, cancelamento e verificação de utilidade.

Projeto e decomposição
Mantenha grafo de dependências declaradas por recurso. Carregar procedimento pode exigir schema e definição; a carga deve retornar conjunto completo ou lista de faltas, não sucesso parcial oculto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

Controle adaptativo
Prefetch só ocorre para dependência provável e dentro de cota. Se objetivo mudar, cancelar cargas pendentes e impedir que resultado tardio seja anexado à tarefa errada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

Validação contrafactual
Compare catálogo integral, carga simples e carga por dependências. Meça escolhas incorretas, conteúdo nunca usado e faltas detectadas antes da execução; bytes lidos não equivalem a informação útil. Unidade de avaliação: carga de recurso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

USO AVANÇADO — Ferramentas numerosas
Cenário: A ação exige schema raro.
Estratégia: Selecionar capacidade por metadados, abrir schema e dependências, validar versão e somente então permitir argumentos.
Papel do modelo pequeno: 3–7B seleciona; 8–14B constrói chamada.
Aceite proposto: Nenhuma execução pode usar contrato apenas resumido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

USO AVANÇADO — Memória modular
Cenário: Uma tarefa referencia vários arquivos.
Estratégia: Abrir índice, resolver conjunto mínimo de módulos e registrar versões; interromper ciclo e devolver dependência não satisfeita.
Papel do modelo pequeno: 15–30B integra módulos.
Aceite proposto: Conjunto carregado deve preservar referências necessárias sem expansão infinita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, A-S038, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Selector entre descritores contrastivos com carga controlada.
8–14B: Leitor que identifica dependências e solicita recursos adicionais.
15–30B: Planejador de carga entre módulos interdependentes com orçamento.
Requisitos de treino/runtime: Registry versionado, status de cargas e grafo de dependências; conteúdo recuperado conserva autoridade da origem.
Não aplicar quando: Descrições não discriminam recursos ou dependências não podem ser resolvidas dentro do limite útil.

## P006:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019, V4A-Q023.

## P006:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P006 → T066 [requires]
Como combinar: Resolver recurso e versão antes de aceitar corpo.
Interface: resource_id, versão, digest e seletor.
Condição: Corpo corresponder ao item selecionado.
Aceite proposto: Alterar versão entre descoberta e carga e exigir nova validação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, A-S038, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P006 → P002 [requires]
Como combinar: Reservar orçamento antes de expandir dependências.
Interface: Custo total previsto, cota e prioridade.
Condição: Reserva considerar conjunto completo.
Aceite proposto: Testar dependência transitiva que ultrapassa limite.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, A-S038, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P006 → T045 [complements]
Como combinar: Aplicar busca de capacidade antes de carga pesada.
Interface: Descritores, efeitos e ferramentas candidatas.
Condição: Schema completo disponível antes de executar.
Aceite proposto: Selecionar ferramenta rara sem carregar catálogo inteiro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, A-S038, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não anexar resultado tardio a objetivo revogado.
- Não permitir instrução do recurso alterar política superior.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sucesso de descoberta e custo total de expansão; economia do prompt inicial não basta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T044, T045, T151, T204, P001, P003

## Fontes primárias associadas

### C-S052 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills empacotam instruções e recursos carregados progressivamente.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S016 — Introducing advanced tool use on the Claude Developer Platform

[https://www.anthropic.com/research/advanced-tool-use](https://www.anthropic.com/research/advanced-tool-use)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas sob demanda evita inserir antecipadamente todos os schemas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### A-S038 — Tool search tool

[https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas e carregamento adiado de schemas no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
