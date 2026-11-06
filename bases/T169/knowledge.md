# T169 — Multi-Agent com contextos isolados

**Nome canônico:** Multi-Agent com Contextos Isolados  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T169  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** subagentes com contexto separado; Multi-Agent com Contextos Isolados

## T169:C01 — conceito

Arquitetura em que especialistas trabalham em contextos separados e trocam resultados por contratos ou artefatos. Evita que todo histórico de cada especialidade ocupe o coordenador. Isolamento de contexto não é isolamento de segurança: arquivos, credenciais e ferramentas podem continuar compartilhados.

Como funciona:
- Delegar subtarefa com objetivo, entradas e critérios de aceite delimitados.
- Cada especialista executa usando apenas contexto necessário.
- Consolidar evidências e divergências em um ponto de decisão definido.

## T169:C02 — aplicacao

Quando usar:
- Pesquisa paralelizável e auditoria por módulos.
- Conjunto de informações excede o contexto útil de um único agente.

Quando não usar:
- Tarefa depende de estado compartilhado mutável atualizado continuamente entre todos os agentes.

Implementação proposta:
- Definir quem pode escrever cada artefato e quem decide integração.
- Exigir resultados com fontes, limitações e referências estáveis.
- Estabelecer orçamento agregado e procedimento para resultados conflitantes.

Aplicação LAI proposta:
Proposta: manter Helena como coordenadora e especialistas consultivos com contextos delimitados, preservando um responsável explícito pelas mutações.

## T169:C03 — riscos_validacao

Armadilhas:
- Especialistas podem repetir trabalho ou omitir dependências.
- Resumo do coordenador pode distorcer detalhes; preservar artefato original evita parte da perda.

Métricas sugeridas:
- Cobertura, duplicação e custo total por missão.
- Erros de integração e divergências resolvidas com evidência.

Testes propostos:
- Dar fatos contraditórios a especialistas e exigir que a consolidação preserve o conflito.
- Matar um agente e verificar que o coordenador detecta lacuna de cobertura.

## T169:C04 — perguntas_proveniencia

Pergunta: Contextos isolados tornam agentes independentes de verdade?
Resposta: Não. Podem compartilhar modelo, fontes e erros correlacionados.

Pergunta: Mais agentes sempre ajudam?
Resposta: Não. Coordenação e consumo podem superar o ganho em tarefas pouco separáveis.

Pergunta: Dois agentes com contextos separados podem sobrescrever o mesmo arquivo?
Resposta: Sim, se compartilham a árvore de trabalho; é necessário separar responsabilidade ou controlar versões.

Pergunta: Como avaliar se delegar economizou?
Resposta: Contabilizar coordenação, resumos, merge e correções no custo total do objetivo, além do trabalho de cada agente.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T169:C05 — mecanismo_avancado

Isolar contexto muda a distribuição de informação entre agentes, mas cria custo de integração. Um resumo final pode perder exceções descobertas pelo especialista; por isso, o retorno proposto inclui artefatos, evidências, versões de entrada e pendências. Se agentes compartilham diretório, escritas concorrentes continuam possíveis. Contexto separado e exclusão de escrita são propriedades independentes, assim como custo faturado por cada agente.

Condição de contorno:
A delegação pode piorar tarefas curtas ou fortemente acopladas quando a comunicação custa mais que o trabalho paralelo aproveitável.

Contrato proposto:
- Entradas: Submissões delimitadas, versões comuns, recursos atribuídos e critério de entrega.
- Saídas: Resultado por agente, artefatos, fontes e conflitos identificados.
- Estado: Responsáveis por arquivos, bases de edição e estados dos ramos.
- Invariante: O coordenador não confunde resumo do especialista com evidência completa de alteração ou teste.

Compromissos de projeto:
- Especialização concentra informação relevante e pode ocultar premissas necessárias à integração.
- Isolamento de escrita reduz conflito e exige etapa explícita de merge.

## T169:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois agentes recebem a mesma base e produzem mudanças incompatíveis no mesmo contrato; exigir detecção da divergência antes de consolidar ambos.

Plano de avaliação proposto:
Comparar agente único e divisão por responsabilidades com orçamento total equivalente. Medir qualidade integrada, retrabalho, tokens de comunicação e tempo final. A decisão deve considerar resultado do conjunto, não apenas rapidez individual de cada agente.

Comparações:
- T237 (complements): Offloading define a unidade delegada; isolamento de contexto define parte da fronteira de execução.
- T239 (complements): Worktrees podem separar árvores de edição, sem substituir contratos de integração.

Afirmação rastreável:
Claude Code documenta subagentes com contexto próprio e consumo de solicitações associado ao mesmo conjunto de limites.
Suporte: direct; fontes: V2A-S018
Limite: Inicialização, ferramentas e permissões variam por tipo e versão; não se presume isolamento de sistema operacional.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T169:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separava isolamento de contexto e exclusão de escrita. A camada nova define fronteiras de conhecimento, contratos de retorno e seleção de trabalhadores pequenos conforme a verificabilidade de cada subtarefa.

Pacote mínimo suficiente
O trabalhador recebe objetivo local, entradas necessárias, critérios de aceite e limites da conclusão. Não envie toda a conversa apenas para parecer completo. Inclua exceções capazes de mudar a decisão: uma tarefa de remoção de código precisa saber quais comportamentos preservar. Isolamento útil reduz distração sem amputar dependências informacionais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4C-S014.

Resultado com evidência recuperável
Peça artefato e referências precisas, não apenas um parágrafo de confiança. O integrador deve conseguir reabrir a evidência e descobrir o que foi inferido, testado ou deixado pendente. Se um resultado depende de uma versão antiga, essa incompatibilidade precisa aparecer antes da síntese, mesmo que o texto final pareça coerente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

Diversidade de papéis e falhas
Especializar por objeto ou propriedade reduz mistura de responsabilidades, mas agentes do mesmo modelo ainda compartilham vieses. Faça verificação por mecanismos diferentes quando possível: parser, compilador e teste de execução. Revisores independentes de contexto podem detectar problemas distintos sem se tornarem provas independentes de verdade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, C-S030.

USO AVANÇADO — Revisão por propriedade
Cenário: Um patch deve preservar comportamento e não introduzir mudanças fora de escopo.
Estratégia: Dê a cada revisor uma propriedade e acesso ao diff e às evidências pertinentes. Agregue resultados identificando exatamente qual propriedade falhou; não use maioria para anular uma violação obrigatória. Reabra evidência quando houver conflito entre revisores.
Papel do modelo pequeno: 3–7B faz checklist estreito; 8–14B examina relações locais; 15–30B integra conflitos.
Aceite proposto: Proposta: detectar violações inseridas e medir falsos bloqueios por propriedade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

USO AVANÇADO — Pesquisa especializada
Cenário: Fontes técnicas pertencem a ecossistemas distintos.
Estratégia: Divida por pergunta verificável, distribua orçamento e exija fonte primária com data. O integrador verifica se dois trabalhadores citaram a mesma evidência antes de tratá-los como confirmação independente. Encaminhe lacunas específicas, sem repetir a missão inteira para cada agente.
Papel do modelo pequeno: 8–14B extrai por documento; integrador maior resolve contradições e limites.
Aceite proposto: Proposta: cobertura por questão, duplicação de coleta e custo total de coordenação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Subtarefas estreitas, com entradas curtas e saída verificável por contrato.
8–14B: Especialistas com poucos documentos e critérios claros de abstenção.
15–30B: Integração de dependências e conflitos; não delegar mais contexto do que o próximo passo exige.
Requisitos de treino/runtime: Registro de versões, artefatos compartilhados com dono e política de concorrência; contabilização por agente.
Não aplicar quando: Não dividir uma decisão cuja evidência precisa ser comparada conjuntamente sem preservar ponte de integração.

## T169:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C007 — Anthropic / Claude Research — sistema multiagente
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A Anthropic relata a passagem de seu sistema Research a produção, com líder, subagentes paralelos, ferramentas e checkpoints.
Mecanismo documentado: O líder decompõe perguntas, delega objetivos e formatos, agrega resultados e preserva estado; ferramentas podem executar em paralelo e falhas são tratadas com adaptação e proteções determinísticas.
Correspondência com esta base: Subagentes possuem contextos próprios no sistema relatado.
Transferência proposta para modelo pequeno: Proposta: reservar agentes 3–30B a buscas delimitadas e extração com fontes, escalando síntese difícil conforme verificação. Medir custo total e cobertura, pois paralelismo aumenta consumo.
Limite: A implantação usa modelos Claude citados pelo operador; não demonstra que 3–30B reproduzam seus resultados. Ganhos do estudo interno não são transferidos; execução assíncrona plena aparece como direção futura.
Fontes: C-S030.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Subagentes delimitados usam modelo padrão mais econômico que o principal.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.
Mecanismo documentado: LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.
Correspondência com esta base: Arquitetura multiagente é mencionada sem especificação de isolamento.
Transferência proposta para modelo pequeno: Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.
Limite: Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.
Fontes: V4C-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Claude Research e harnesses Uber fornecem casos operacionais. O papel por faixa de parâmetros é proposta: as fontes não informam que os trabalhadores usados sejam 3–30B.
Consultas registradas: V4C-Q009, V4C-Q010.

## T169:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T169 → T237 [complements]
Como combinar: Claude Research distribui tarefas a subagentes e recebe resultados com referências para integração.
Interface: Objetivo local, orçamento e artefato retornado.
Condição: Tarefas distinguíveis e mecanismo de reunião.
Aceite proposto: Verificar suficiência do retorno antes de declarar cobertura.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: C-S030. Casos: V4C-C007.

2. T169 → T171 [complements]
Como combinar: Harness Uber diferencia perfis de cache entre interação e subagentes, articulando contexto e custo.
Interface: Perfil de sessão, prefixo estável e política de retenção.
Condição: Compatibilidade do provedor e configuração atual.
Aceite proposto: Medir economia sem misturar estados incompatíveis.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

CONTROLES DE FALHA
- Contexto separado não impede dois agentes de escreverem no mesmo arquivo.
- Confirmações que derivam da mesma fonte ou do mesmo erro não contam como evidências independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare uma equipe pequena com um agente de fronteira sob orçamento total equivalente. Ganhos em tarefas paralelizáveis não significam superioridade em raciocínio indivisível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T139, T147, T186, T200

## Fontes primárias associadas

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

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

### V4C-S028 — How Klarna's AI assistant redefined customer support at scale

[https://www.langchain.com/blog/customers-klarna](https://www.langchain.com/blog/customers-klarna)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fornecedor relata assistência de Klarna com LangGraph, roteamento de tarefas, prompts adaptados e avaliações LangSmith.

Limite: Abertura confirmou relato do fornecedor e citação de executivo; detalhes do runtime não foram confirmados em publicação técnica do operador nesta busca. Registro conservador como recurso/caso documentado sem entrar na meta estrita de produção.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
