# Pesquisas, projetos e tecnologias de referência

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

# R001 — MemGPT

**Nome canônico:** MemGPT: Towards LLMs as Operating Systems  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R001  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Memory-GPT; gerenciamento virtual de contexto

## R001:C01 — conceito

Pesquisa que trata a janela limitada de uma LLM como memória de trabalho e gerencia informação entre níveis internos e externos. A analogia com sistemas operacionais orienta movimentação de dados e controle de fluxo; não cria uma janela física infinita nem faz todos os registros participarem simultaneamente da atenção.

Como funciona:
- Manter um estado compacto no contexto disponível ao modelo.
- Consultar e atualizar memórias externas por operações explícitas.
- Usar controle de fluxo para encadear recuperação, processamento e interação.

## R001:C02 — aplicacao

Quando usar:
- Estudar agentes que precisam retomar conversas entre sessões.
- Projetar consulta a documentos maiores que a janela ativa.

Quando não usar:
- Quando o requisito é acesso instantâneo e integral a cada detalhe sem custo de recuperação.

Implementação proposta:
- Proposta: definir os campos que precisam permanecer no contexto e os que podem ser recuperados.
- Implementar operações de leitura/escrita com IDs estáveis antes de adicionar decisões automáticas de paginação.
- Avaliar o agente com informações antigas relevantes e restrições recentes contraditórias.

Aplicação LAI proposta:
Proposta LAI: usar o trabalho como referência para o controlador de contexto da Helena, mantendo a persistência e os critérios de aceite sob controle do executor.

## R001:C03 — riscos_validacao

Armadilhas:
- O controlador pode não perceber que uma informação ausente é necessária.
- Mover um resumo para a memória não garante preservação das condições omitidas.

Métricas sugeridas:
- Recall de fatos críticos após várias sessões.
- Chamadas adicionais e tokens por resposta correta.

Testes propostos:
- Proposta: retirar do contexto um fato indispensável e exigir sua recuperação com origem.
- Reiniciar o processo e verificar que o estado confirmado continua acessível.

## R001:C04 — perguntas_proveniencia

Pergunta: MemGPT aumenta os parâmetros do modelo?
Resposta: O gerenciamento virtual de contexto é uma arquitetura de sistema; consultar memória externa não adiciona automaticamente conhecimento aos pesos.

Pergunta: Ter memória externa garante lembrar o fato certo?
Resposta: Não. É necessário testar descoberta, recuperação, validade temporal e uso correto do que foi recuperado.

Pergunta: O resumo da fila contém todo o conhecimento antigo?
Resposta: Não. Ele é uma representação reduzida. O histórico completo fica no armazenamento externo e precisa de operações de recuperação para detalhes omitidos.

Pergunta: Continuação automática elimina necessidade de limites?
Resposta: Não. Defina orçamento e condição de progresso. Um agente pode continuar chamando memória sem obter evidência adicional ou resolver a tarefa.

Escopo das fontes:
A-S009 sustenta a arquitetura de memória em níveis e o controle de fluxo. O desenho operacional e os testes acima são propostas; não reproduzem os experimentos do artigo.

## R001:C05 — mecanismo_avancado

No desenho original, o contexto principal separa instruções estáticas, bloco de trabalho editável por funções e fila FIFO de mensagens. O gerenciador registra entradas e saídas em recall storage; itens expulsos podem ser recuperados e reinseridos. A continuidade do processamento também é explícita: uma chamada pode solicitar nova inferência após seu resultado ou devolver o controle até surgir outro evento. Memória e agenda de execução são partes relacionadas, mas distintas.

Condição de contorno:
O agente precisa usar corretamente as funções e perceber necessidades de busca; manter um histórico externo não garante que informações antigas entrem na decisão apropriada.

Contrato proposto:
- Entradas: Eventos, contexto ativo, armazenamento externo e schemas das funções de memória.
- Saídas: Atualizações de memória, resultados de busca paginados e decisão de continuar ou ceder controle.
- Estado: Fila, resumo recursivo, bloco de trabalho, histórico externo e chamadas em andamento.
- Invariante: Um conteúdo expulso permanece fora da atenção até ser explicitamente recuperado e incluído no contexto principal.

Compromissos de projeto:
- Autogerência permite adaptar o conteúdo ativo e aumenta o número de inferências de controle.
- Resumo da fila mantém continuidade e pode perder detalhe que só a recuperação do original restaura.

## R001:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir resultado maior que a capacidade ativa e exigir várias páginas. O controlador deve paginar, conservar a necessidade de continuação e evitar tanto overflow quanto loop sem avanço.

Plano de avaliação proposto:
Avaliação proposta: comparar janela FIFO, resumo isolado e arquitetura com funções de memória usando eventos equivalentes. Medir recuperação necessária, chamadas de controle, coerência após expulsões e qualidade das decisões; separar limites do modelo e do gerenciador.

Comparações:
- T063 (specializes): MemGPT é uma implementação de pesquisa concreta do padrão de gerência virtual de contexto.
- R013 (distinct_from): MemFS projeta memória em checkout Git; não é simplesmente o nome atual de cada mecanismo do artigo original.

Afirmação rastreável:
O artigo MemGPT descreve fila, working context, recall storage, paginação e encadeamento de funções para controle de fluxo.
Suporte: direct; fontes: A-S009
Limite: Configurações ilustrativas do artigo não são limites universais; o projeto atual Letta possui contratos próprios que precisam ser consultados.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R001:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu a arquitetura original MemGPT. Aqui a proposta mede competência de controle de memória antes de delegar esse controle a um modelo pequeno.

Projeto e decomposição
Separe lembrar informação e escolher quando escrevê-la ou buscá-la. Um modelo pode responder corretamente com evidência fornecida e ainda falhar ao decidir operações de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V4A-S026.

Controle adaptativo
Comece com controlador externo e ações limitadas, como consultar referência e propor atualização. Amplie autonomia somente após medir perdas, buscas inúteis e escrita de hipóteses como fatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V4A-S026.

Validação contrafactual
Compare memória controlada por código, pelo modelo e política híbrida. Meça recuperação de fatos antigos, qualidade das escritas e custo de chamadas; sucesso em conversa curta não valida gestão de contexto virtual. Unidade de avaliação: política de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V4A-S026.

USO AVANÇADO — Assistente local persistente
Cenário: Modelo 3–7B tem janela limitada.
Estratégia: Manter perfil explícito e arquivo consultável; modelo solicita campos faltantes enquanto controlador decide persistência e limites.
Papel do modelo pequeno: 3–7B lê e propõe operações.
Aceite proposto: Não perder correção explícita nem gravar inferência como declaração do usuário.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V4A-S026.

USO AVANÇADO — Análise de documentos grandes
Cenário: A informação excede a janela.
Estratégia: Criar índice de evidências e permitir cargas paginadas com objetivo definido; registrar progresso para evitar ciclos.
Papel do modelo pequeno: 8–14B pesquisa; 15–30B integra.
Aceite proposto: Cada resposta deve citar páginas efetivamente abertas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, V4A-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor com ferramentas de memória restritas e política externa.
8–14B: Gerente de memória em domínio limitado, após testes de escrita e busca.
15–30B: Controlador mais autônomo quando avaliação demonstrar operações consistentes.
Requisitos de treino/runtime: Ferramentas compatíveis, armazenamento externo e avaliação de controle; MemGPT é padrão de pesquisa, Letta é framework distinto.
Não aplicar quando: Modelo não usa ferramentas com confiabilidade ou aplicações exigem memória ilimitada sem custo de acesso.

## R001:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C026 — UC Berkeley; autores MemGPT / MemGPT original
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa avalia gestão de contexto virtual em documentos e conversas.
Mecanismo documentado: Ferramentas movimentam informação entre janela e armazenamento externo.
Correspondência com esta base: Identidade do artigo original.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar política curta de consultar, carregar e verificar para 3–14B antes de delegar controle livre.
Limite: Não comprova produção bigtech nem memória ilimitada; experimentos não são garantias do runtime. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R001:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R001 → T063 [complements]
Como combinar: Implementar movimentação explícita entre níveis.
Interface: Bloco, referência, residência e orçamento.
Condição: Controlador não confundir arquivo e contexto ativo.
Aceite proposto: Testar tarefa com várias trocas de blocos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, V4A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R001 → T071 [requires]
Como combinar: Validar propostas de escrita antes de promover.
Interface: Conteúdo, origem e tipo de memória.
Condição: Proposta não adquirir autoridade por ter sido gerada.
Aceite proposto: Inserir hipótese plausível e impedir promoção indevida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, V4A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não atribuir ao MemGPT todas as capacidades atuais do Letta.
- Não contar sistema de pesquisa como implantação bigtech.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar política de memória com leitor fixo; distinguir melhora de acesso e melhora de capacidade do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T062, T063, T067, R002

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R002 — Letta

**Nome canônico:** Letta — plataforma de agentes com estado  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R002  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Letta platform; plataforma Letta; Letta MemFS; context repository; filesystem de memória; Letta / Letta MemFS

## R002:C01 — conceito

Letta é uma plataforma e um runtime para agentes com identidade persistente, configuração de modelo, ferramentas, conversas e memória. A ficha representa o projeto completo. MemFS é seu mecanismo documentado de memória em arquivos, detalhado separadamente em R013; persistir informações não implica aprender novos pesos nem garantir decisões corretas.

Como funciona:
- O agente reúne identidade, configuração e histórico; conversas diferentes podem compartilhar sua memória de longo prazo.
- Ferramentas consultam e modificam recursos externos; a janela ativa continua limitada e contém somente o contexto selecionado.

Nota de nomenclatura: Atualiza R002: a antiga ficha combinava Letta e MemFS. O detalhamento de MemFS passa a R013 e seu nome relacionado a R014.

## R002:C02 — aplicacao

Quando usar:
- Assistentes que retomam projetos em várias sessões e precisam de memória inspecionável.
- Aplicações que desejam incorporar um agente por SDK ou runtime administrado.

Quando não usar:
- Como garantia automática de transações corretas, memória factual ou recuperação de qualquer falha externa.

Implementação proposta:
- Proposta: registrar versão, backend, modelo, identificador do agente e política de armazenamento antes de integrar.
- Separar agentes com identidades independentes de conversas paralelas do mesmo agente; definir escopo de memória por cliente.
- Conectar uma ferramenta de leitura e uma operação idempotente; registrar entradas, resultados e alterações de memória com proveniência.

Aplicação LAI proposta:
Proposta LAI: avaliar Letta como candidato para agentes persistentes da Helena, comparando integração e retomada com o runtime existente em tarefas equivalentes.

## R002:C03 — riscos_validacao

Armadilhas:
- Conversas do mesmo agente compartilham memória; separar apenas threads pode não fornecer o isolamento pretendido.
- Agentes locais sem conta exigem atenção a backups; memória compartilhada também pode perpetuar informação errada.

Métricas sugeridas:
- Acerto de retomada, isolamento entre agentes, custo por tarefa e recuperação de memória relevante.

Testes propostos:
- Proposta: gravar uma preferência de teste, iniciar outra conversa e conferir a recuperação pelo mesmo agente.
- Repetir com outro agente e simular perda do processo, distinguindo armazenamento confirmado de conteúdo apenas transitório.

## R002:C04 — perguntas_proveniencia

Pergunta: Letta é um modelo de linguagem?
Resposta: Não. Ele organiza a execução e o estado de agentes que utilizam modelos configurados.

Pergunta: Uma nova conversa cria memória independente?
Resposta: Não necessariamente. Na documentação atual, conversas do mesmo agente compartilham sua memória; outro agente pode fornecer identidade separada.

Pergunta: Um agente local tem automaticamente backup remoto?
Resposta: Não. A documentação distingue agentes locais sem conta e agentes com backup na nuvem; o contrato deve registrar qual modalidade foi usada.

Pergunta: Stateful significa aprendizado nos pesos?
Resposta: Não. Neste contexto significa identidade e estado persistentes. Mudanças de arquivos, histórico ou configuração não são automaticamente treinamento paramétrico.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R002:C05 — mecanismo_avancado

A identidade do agente e a identidade da conversa não são equivalentes na documentação atual da Letta. Várias conversas podem compartilhar a memória do mesmo agente, enquanto agentes diferentes mantêm identidades e MemFS próprios. Para colaboração entre agentes, existe repositório compartilhado com propriedade organizacional. Essa separação importa na avaliação: observar uma lembrança em outra conversa pode ser comportamento esperado, e não isolamento quebrado entre usuários.

Condição de contorno:
A separação de conversas não deve ser usada como fronteira de memória quando o produto documenta compartilhamento no nível do agente.

Contrato proposto:
- Entradas: Identidade do agente, conversa, configuração e recursos de memória explicitamente associados.
- Saídas: Continuidade de interação com contexto selecionado e alterações persistidas no escopo correto.
- Estado: MemFS, histórico de conversas, configuração de ferramentas e repositórios compartilhados anexados.
- Invariante: Nenhuma suposição de isolamento é baseada apenas na existência de threads diferentes; o escopo real precisa ser declarado.

Compromissos de projeto:
- Compartilhar memória entre conversas melhora continuidade e aumenta a necessidade de resolver escritas concorrentes.
- Separar agentes reduz interferência e pode exigir mecanismo explícito para compartilhar conhecimento comum.

## R002:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar uma preferência em duas conversas do mesmo agente e consultar uma terceira. Verifique a política de resolução e diferencie esse caso de agentes distintos sem memória compartilhada.

Plano de avaliação proposto:
Avaliação proposta: avaliar matriz de mesmo agente ou diferente agente e mesma conversa ou diferente conversa. Medir continuidade, interferência, conflitos e recuperação após troca de computador; documentar armazenamento local ou hospedado usado no ensaio.

Comparações:
- R013 (complements): MemFS é o mecanismo de memória em arquivos dentro do escopo mais amplo da plataforma.
- T064 (complements): Estado persistente descreve uma responsabilidade necessária à continuidade, mas não especifica todo o produto Letta.

Afirmação rastreável:
Letta documenta memória compartilhada entre conversas de um agente e distingue MemFS individual de repositórios compartilhados da organização.
Suporte: direct; fontes: V2B-S002, V3A-S046
Limite: A disponibilidade de componentes depende da modalidade e versão; persistência não garante qualidade factual ou coordenação sem conflitos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R002:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou identidade de agente e conversa. Aqui Letta é tratado como infraestrutura substituível cujo contrato precisa ser testado com cada consumidor.

Projeto e decomposição
Defina perfil de compatibilidade por modelo: formato de ferramentas, leitura de blocos, qualidade de atualizações e retomada. Framework stateful não torna automaticamente qualquer 3–30B competente em memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V4A-S026, V3A-S046.

Controle adaptativo
Separe fatos persistidos pelo servidor de instruções visíveis no turno. Migração de modelo deve reconstruir contexto e testar se o consumidor interpreta corretamente o estado existente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V4A-S026, V3A-S046.

Validação contrafactual
Compare mesmo agente com dois leitores e mesmos dados. Meça operações válidas, memórias recuperadas e alterações indevidas; uso de armazenamento compartilhado não implica compreensão compartilhada. Unidade de avaliação: agente persistente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V4A-S026, V3A-S046.

USO AVANÇADO — Mudança para modelo local
Cenário: Projeto quer reduzir dependência de provedor.
Estratégia: Exportar inventário de estado, validar interfaces e retomar tarefas reversíveis em amostra antes da migração ampla.
Papel do modelo pequeno: 8–14B candidato a leitor local.
Aceite proposto: Memórias e pendências devem permanecer interpretáveis sem mudar seu significado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V4A-S026, V3A-S046.

USO AVANÇADO — Agentes com memória comum
Cenário: Especialistas usam decisões do projeto.
Estratégia: Compartilhar apenas objetos com escopo apropriado e separar hipóteses privadas; validar conflitos quando dois agentes propõem correção.
Papel do modelo pequeno: 15–30B integra; 3–7B extrai.
Aceite proposto: Uma atualização não pode sobrescrever decisão confirmada sem controle de versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V4A-S026, V3A-S046.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de domínio estreito com memória explícita e poucas ferramentas.
8–14B: Agente stateful de tarefas moderadas após teste do protocolo.
15–30B: Especialista integrador com acesso seletivo a memória compartilhada.
Requisitos de treino/runtime: Servidor e versão de API identificados, storage durável e modelo compatível; não há execução do Letta neste pacote.
Não aplicar quando: A decisão de adotar se baseia somente em README ou promete persistência sem testar backend real.

## R002:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C027 — Letta / Framework de agentes stateful
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Fornecedor distingue framework Letta do padrão MemGPT e oferece serviços stateful.
Mecanismo documentado: Persistência do agente e ferramentas de memória externas ao modelo.
Correspondência com esta base: Fornecedor e framework identificados.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher modelo compatível por testes de protocolo e separar identidade de agente e conversa.
Limite: Letta não é bigtech; implantação facilitada não comprova cliente ou escala. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S026, V2B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R002:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R002 → T064 [requires]
Como combinar: Validar persistência independente do processo.
Interface: agent_id, estado, versão e referências.
Condição: Backend sobreviver ao reinício.
Aceite proposto: Restaurar em processo novo e verificar mesmas pendências.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2B-S002, V4A-S026, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R002 → T075 [complements]
Como combinar: Reconciliar propostas de múltiplos agentes.
Interface: Objeto, revisão-base, proposta e origem.
Condição: Escritas compartilhadas terem controle de concorrência.
Aceite proposto: Simular duas correções incompatíveis e preservar conflito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2B-S002, V4A-S026, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não equiparar conversa nova a agente novo sem conferir escopo.
- Não chamar produto disponível de implantação comprovada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade e uso de ferramentas com o mesmo runtime; trocar leitor pode alterar qualidade mesmo preservando estado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R001, R013, R014, T047, T064, T072

## Fontes primárias associadas

### V2B-S001 — Letta Documentation

[https://docs.letta.com/](https://docs.letta.com/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Plataforma de agentes com estado, harness aberto, Agent SDK e opções de execução administrada ou própria.

Limite: Página oficial consultada; recursos disponíveis dependem da versão e implantação. Não houve instalação nem ensaio no ambiente LAI.

### V2B-S002 — Stateful agents

[https://docs.letta.com/concepts/stateful-agents](https://docs.letta.com/concepts/stateful-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade persistente, memória compartilhada entre conversas do mesmo agente e distinção entre agentes locais e com backup em nuvem.

Limite: Documentação atual consultada; não comprova isolamento ou durabilidade de uma implantação específica.

### V3A-S046 — Letta Shared memory

[https://docs.letta.com/concepts/shared-memory](https://docs.letta.com/concepts/shared-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MemFS pertence a um agente; repositório compartilhado pertence à organização e requer commit, push e pull para sincronização entre checkouts.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R003 — LongMem

**Nome canônico:** LongMem — Augmenting Language Models with Long-Term Memory  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R003  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Long-Term Memory augmented language model; memória neural de longo prazo

## R003:C01 — conceito

Arquitetura de pesquisa que usa a LLM base congelada como codificador de memória e uma rede lateral adaptável como recuperador e leitor. Seu mecanismo aprende a utilizar representações de contextos passados. É diferente de simplesmente conectar uma API de chat a arquivos ou a um índice textual.

Como funciona:
- Codificar contextos anteriores com o backbone congelado.
- Armazenar representações recuperáveis em um banco de memória.
- Treinar a adaptação para que a rede lateral recupere e utilize essa informação.

## R003:C02 — aplicacao

Quando usar:
- Pesquisa em arquiteturas de memória com acesso ao modelo e ao treinamento.
- Comparação controlada entre memória neural e recuperação textual em tarefas longas.

Quando não usar:
- Como configuração imediata de um servidor arbitrário que só expõe chat/completions.

Implementação proposta:
- Proposta: identificar implementação e checkpoint compatíveis antes de escolher o experimento.
- Reproduzir um caso pequeno com e sem acesso à memória mantendo dados e orçamento comparáveis.
- Medir armazenamento, latência e ganho na tarefa; incluir episódios antigos e dados fora do domínio.

Aplicação LAI proposta:
Proposta LAI: tratar LongMem como linha de pesquisa; para integração inicial da Helena com APIs, avaliar primeiro recuperação textual e estado persistente.

## R003:C03 — riscos_validacao

Armadilhas:
- Trocar o codificador pode invalidar a compatibilidade das representações armazenadas.
- A capacidade do banco de memória não significa atenção exata a todo o histórico em cada passo.

Métricas sugeridas:
- Qualidade na tarefa com memória versus sem memória.
- Custo de codificação, leitura e manutenção por quantidade de contexto armazenado.

Testes propostos:
- Proposta: alterar uma informação histórica relevante e observar se a recuperação responde à alteração.
- Remover a memória e exigir queda específica nas tarefas dependentes dela, evitando atribuir ganhos a outros fatores.

## R003:C04 — perguntas_proveniencia

Pergunta: LongMem é apenas RAG textual?
Resposta: Não. O trabalho inclui arquitetura neural, representações armazenadas e treinamento de adaptação.

Pergunta: Posso assumir compatibilidade com meu Qwen?
Resposta: Não. Ela depende de implementação, arquitetura, checkpoint e treinamento, que precisam ser examinados.

Pergunta: A palavra staleness significa informação factual vencida?
Resposta: No argumento arquitetural, refere-se à compatibilidade de representações quando redes mudam. Validade temporal dos fatos exige controle adicional.

Pergunta: É uma biblioteca intercambiável com RAG textual?
Resposta: Não diretamente. Ela depende de componentes internos e treinamento; a documentação do repositório apresenta uma implementação específica baseada em fairseq.

Escopo das fontes:
A-S013 sustenta o backbone congelado e a rede lateral treinável. Não foi reproduzido o sistema nem extrapolado o resultado do artigo ao ambiente LAI.

## R003:C05 — mecanismo_avancado

O código de LongMem armazena chaves e valores por cabeça de atenção. Para buscar, indexa uma média das chaves de cada chunk e recupera os estados dos chunks selecionados, separando unidade de busca da unidade lida. O backbone congelado mantém estável a representação codificada enquanto a rede lateral aprende a utilizá-la. Essa estabilidade reduz incompatibilidade por deriva do codificador; não torna fatos antigos automaticamente atuais.

Condição de contorno:
A memória continua limitada por capacidade, custo de busca e interface neural; transportar esse banco para outro backbone pode invalidar seu significado mesmo com dimensões iguais.

Contrato proposto:
- Entradas: Contextos anteriores, backbone e tokenizer compatíveis, configuração de banco e rede lateral adaptada.
- Saídas: Estados recuperados e geração condicionada pela arquitetura de leitura de memória.
- Estado: Chaves e valores, índice por cabeça, configuração de chunks e versões dos pesos.
- Invariante: Memórias codificadas sob uma versão não são reutilizadas com outro consumidor apenas por passarem na validação de forma.

Compromissos de projeto:
- Buscar representantes de chunks reduz a unidade de indexação e pode diluir um detalhe importante dentro da média.
- Congelar o codificador facilita reutilização do banco e restringe liberdade de atualizar o backbone sem reconstrução.

## R003:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar o backbone mantendo o banco anterior e comparar com recodificação completa. A experiência deve detectar deriva de compatibilidade, sem atribuir qualquer queda apenas ao tamanho da memória.

Plano de avaliação proposto:
Avaliação proposta: comparar backbone sem memória, arquitetura com banco e banco recodificado após mudança controlada. Medir uso de contexto passado, latência de busca, memória computacional e preservação de detalhes; contabilizar adaptação e construção do índice.

Comparações:
- T052 (specializes): LongMem usa uma interface neural específica para contexto passado, dentro da família ampla de representações latentes.
- R001 (distinct_from): MemGPT controla texto e funções externamente; LongMem modifica a arquitetura de leitura e requer adaptação treinada.

Afirmação rastreável:
A implementação oficial indexa médias das chaves por chunk e retorna chaves e valores dos grupos recuperados.
Suporte: direct; fontes: V3A-S047
Limite: Código consultado sem execução; detalhes são desta implementação de pesquisa e não demonstram prontidão para o servidor da LAI.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R003:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhou memória KV e encoder congelado. Aqui LongMem é analisado como projeto de ciclo de vida de representações, incluindo atualização do consumidor.

Projeto e decomposição
Versione encoder, representação armazenada e módulo que a lê como conjunto. Alterar qualquer parte exige teste de compatibilidade; dimensão igual não preserva geometria nem significado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

Controle adaptativo
Separe renovação factual do texto e renovação representacional. Reindexar com encoder antigo pode atualizar fatos; trocar encoder exige reconstruir memória mesmo quando documentos não mudaram.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

Validação contrafactual
Compare memória atualizada, obsoleta e reconstruída após mudança de modelo. Meça recuperação e resposta separadamente, além do custo de treino e armazenamento; não atribuir falha neural a falta de documento. Unidade de avaliação: memória neural por revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

USO AVANÇADO — Experimento de memória longa
Cenário: Equipe tem pesos e infraestrutura de treino.
Estratégia: Reproduzir interface em escala controlada, avaliar vantagem sobre RAG textual e ampliar somente se o ganho cobrir manutenção.
Papel do modelo pequeno: 15–30B consumidor experimental.
Aceite proposto: Exigir benefício além do mesmo modelo com evidência textual equivalente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

USO AVANÇADO — Corpus que muda
Cenário: Fatos antigos precisam ser substituídos.
Estratégia: Manter mapa texto-representação e reconstruir regiões afetadas; verificar que estados antigos não continuam acessíveis como atuais.
Papel do modelo pequeno: 8–14B pode servir como baseline textual.
Aceite proposto: Consulta deve acompanhar atualização factual sem misturar revisões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Baseline de leitura textual, sem presumir que LongMem se encaixa diretamente.
8–14B: Consumidor experimental apenas se arquitetura e treino forem adaptados e avaliados.
15–30B: Alvo de pesquisa com acesso a camadas, memória externa e recursos de treinamento.
Requisitos de treino/runtime: Código e arquitetura compatíveis, dados de treino e instrumentação de estados; não é ferramenta plug-and-play para modelo fechado.
Não aplicar quando: Não há acesso ao modelo ou custo de reconstruir representações domina benefício de contexto.

## R003:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C029 — Autores LongMem; Microsoft Research e colaboradores / LongMem
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo e código estudam memória neural recuperável para contexto extenso.
Mecanismo documentado: Representações em memória e módulo adaptado de leitura são componentes treinados.
Correspondência com esta base: Projeto e código específicos.
Transferência proposta para modelo pequeno: Proposta de engenharia: Somente considerar 15–30B se houver acesso a treino e alinhamento de estados; iniciar com RAG textual controlado.
Limite: Não é plug-in universal nem uso bigtech demonstrado; portar requer treino e compatibilidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S013, V3A-S047.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q018, V4A-Q023.

## R003:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R003 → T052 [requires]
Como combinar: Declarar formato e versão da memória neural.
Interface: Camada, tensor, máscaras, encoder e consumidor.
Condição: Representações serem semanticamente compatíveis.
Aceite proposto: Trocar encoder sem reconstruir e medir degradação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S045, V3A-S047. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R003 → T009 [alternative]
Como combinar: Usar RAG textual como comparação operacional.
Interface: Mesmas fontes, consulta e orçamento de recursos.
Condição: Baseline receber evidência equivalente.
Aceite proposto: Separar ganho de memória neural de ganho de recuperação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S045, V3A-S047. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar encoder congelado como garantia de fatos atuais.
- Não transportar métricas do artigo para outro porte sem experimento.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar contexto longo em tarefa definida; resultados do LongMem não demonstram superioridade geral a modelos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T052, T068, T062

## Fontes primárias associadas

### A-S013 — Augmenting Language Models with Long-Term Memory

[https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: LongMem: backbone congelado como codificador e rede lateral treinada para recuperação e leitura.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S045 — LongMem official implementation

[https://github.com/Victorwz/LongMem](https://github.com/Victorwz/LongMem)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Organização de SideNetwork, banco de memória e atenção para fusão; dependências de implementação de pesquisa em fairseq.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V3A-S047 — LongMem External_Memory implementation

[https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py](https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco de chaves e valores por cabeça, indexação da média das chaves em chunks e recuperação dos estados dos chunks selecionados.

Limite: Leitura do código na branch main, sem execução. Detalhes representam esta implementação de pesquisa e não garantem compatibilidade com qualquer modelo ou ambiente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R004 — Generative Agents

**Nome canônico:** Generative Agents: Interactive Simulacra of Human Behavior  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R004  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** agentes generativos; memory stream; reflexão episódica

## R004:C01 — conceito

Pesquisa sobre agentes que simulam comportamentos humanos em um ambiente interativo. A arquitetura registra experiências em linguagem natural, produz reflexões de nível mais alto e recupera memórias para planejamento. Sua avaliação de comportamento plausível não demonstra que um agente empresarial tomará decisões corretas ou seguras.

Como funciona:
- Registrar observações e experiências do agente em um fluxo de memória.
- Sintetizar reflexões que relacionam experiências anteriores.
- Recuperar conteúdo relevante para planejar e ajustar ações no ambiente.

## R004:C02 — aplicacao

Quando usar:
- Estudo de memória episódica e planejamento em simulações.
- Prototipação de exercícios de interação com personagens e cenários controlados.

Quando não usar:
- Como evidência de leitura real de intenção humana ou validação científica de um cliente específico.

Implementação proposta:
- Proposta: começar com simulação pequena e registrar todas as observações com sua origem.
- Separar observação literal de reflexão inferida para não transformar uma interpretação em fato.
- Comparar memória completa, memória sem reflexão e memória sem recuperação mantendo os cenários iguais.

Aplicação LAI proposta:
Proposta LAI: usar a separação entre experiência, reflexão e plano para treinos simulados de vendas; validar resultados reais por evidências externas à simulação.

## R004:C03 — riscos_validacao

Armadilhas:
- Um comportamento convincente pode encobrir uma decisão factual incorreta.
- Reflexões geradas pelo próprio modelo podem retroalimentar uma interpretação falsa.

Métricas sugeridas:
- Consistência com observações e objetivos declarados do cenário.
- Frequência de inferências indevidas promovidas a fatos e custo por episódio.

Testes propostos:
- Proposta: inserir uma observação ambígua e confirmar que a inferência permanece identificada.
- Corrigir uma informação do personagem e medir se o planejamento usa a atualização.

## R004:C04 — perguntas_proveniencia

Pergunta: Comportamento plausível prova competência comercial?
Resposta: Não. Plausibilidade em uma simulação e resultado comercial real são critérios diferentes.

Pergunta: Reflexão deve virar memória comprovada?
Resposta: Somente após critérios de validação adequados. Inicialmente, é uma interpretação do agente.

Pergunta: A importância usada no artigo é confiança factual?
Resposta: Não. Ela destaca a relevância percebida do evento para o agente simulado. Um item importante ainda pode conter interpretação equivocada.

Pergunta: Refletir sobre reflexões aumenta evidência disponível?
Resposta: Aumenta organização e abstração, não o número de observações independentes. A cadeia deve continuar apontando às origens que realmente sustentam a conclusão.

Escopo das fontes:
A-S008 sustenta os componentes de observação, reflexão, planejamento e recuperação na simulação. Os controles de evidência e critérios comerciais acima são propostas editoriais.

## R004:C05 — mecanismo_avancado

Generative Agents calcula recuperação combinando recência de acesso, importância atribuída e relevância à situação. Reflexões entram novamente no mesmo fluxo e podem sustentar reflexões posteriores por referências. Isso cria uma estrutura de derivação útil à coerência, mas também um caminho de autorreforço: uma interpretação incorreta pode reaparecer com aparência de conhecimento consolidado se não for distinguida da observação original.

Condição de contorno:
Plausibilidade de comportamento numa simulação não mede a verdade de afirmações, capacidade causal ou confiabilidade de decisões num ambiente empresarial.

Contrato proposto:
- Entradas: Observações da simulação, situação atual, memórias anteriores e regras de planejamento.
- Saídas: Ações planejadas, reflexões derivadas e memórias selecionadas para a próxima inferência.
- Estado: Fluxo de memória, tempos de criação e acesso, escores e referências das reflexões.
- Invariante: Reflexão mantém status de inferência e não é confundida com nova observação independente do ambiente.

Compromissos de projeto:
- Reflexões permitem abstrair padrões e podem amplificar interpretações erradas.
- Recência por acesso mantém continuidade e pode privilegiar lembranças já usadas, reduzindo exposição a evidência esquecida.

## R004:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir uma observação ambígua que gere inferência incorreta e depois apresentar correção direta. O sistema deve revisar derivados relevantes, sem contar reflexões repetidas como várias confirmações.

Plano de avaliação proposto:
Avaliação proposta: comparar arquitetura completa com remoção de reflexão ou variação do recuperador. Medir coerência, fidelidade às observações, propagação de correções e custo; mantenha plausibilidade e precisão factual como dimensões separadas.

Comparações:
- T049 (complements): O fluxo registra experiências situadas que podem ser recuperadas para orientar comportamento.
- T058 (complements): Reflexões sintetizam memórias em abstrações, exigindo rastreabilidade das derivações.

Afirmação rastreável:
O artigo combina relevância, recência e importância na recuperação e armazena reflexões com referências às memórias utilizadas.
Suporte: direct; fontes: A-S008
Limite: Pesos e limiares ilustrados pertencem à simulação estudada; não são recomendações universais para memória operacional.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R004:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu plausibilidade e verdade. Aqui Generative Agents é usado para estudar crenças divergentes e transferência de memória em simulação controlada.

Projeto e decomposição
Separe estado verdadeiro do ambiente e crenças de cada agente. Reflexões podem ser coerentes com observações incompletas e ainda estar erradas; isso deve ser mensurável no experimento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

Controle adaptativo
Controle quais eventos cada agente presencia e quais recebe por relato. A memória precisa preservar origem para distinguir experiência direta, rumor e inferência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

Validação contrafactual
Compare agentes com reflexão, somente episódios e memória fornecida por controlador. Meça fidelidade ao que foi observado, propagação de rumores e ações compatíveis com crenças, sem confundir realismo narrativo com acerto. Unidade de avaliação: agente em simulação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

USO AVANÇADO — Simulação de colaboração
Cenário: Agentes precisam coordenar tarefas com informação parcial.
Estratégia: Distribuir observações diferentes, registrar mensagens e verificar como crenças convergem após evidência nova.
Papel do modelo pequeno: 3–7B atua em papéis estreitos.
Aceite proposto: Agente não pode usar informação que nunca recebeu.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

USO AVANÇADO — Treino de recuperação episódica
Cenário: É preciso testar memória sob ruído.
Estratégia: Criar ambiente sintético próprio com eventos identificados e mudanças de preferência; comparar recência, relevância e importância.
Papel do modelo pequeno: 8–14B recupera; 15–30B planeja.
Aceite proposto: Correção explícita deve alterar comportamento sem apagar histórico de crença.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Agente simulado com vocabulário e ações limitadas.
8–14B: Agente com memória episódica e reflexão em ambiente controlado.
15–30B: Planejador social experimental, sem extrapolar para comportamento humano real.
Requisitos de treino/runtime: Simulador com estado conhecido, logs e controle de observações; não usar comportamento plausível como único avaliador.
Não aplicar quando: A intenção é prever pessoas reais ou validar causalidade social sem desenho empírico apropriado.

## R004:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C030 — Autores Generative Agents / Generative Agents / Smallville
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo constrói agentes simulados que registram experiências e refletem.
Mecanismo documentado: Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.
Correspondência com esta base: Trabalho identificado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.
Limite: Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R004:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R004 → T049 [requires]
Como combinar: Registrar experiências com origem e observador.
Interface: Evento, agente, percepção e tempo.
Condição: Store distinguir observação de relato.
Aceite proposto: Introduzir rumor e rastrear sua propagação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R004 → T051 [complements]
Como combinar: Separar perspectivas e crenças no grafo.
Interface: Relação, agente que acredita e evidência.
Condição: Crença não ser promovida a fato do ambiente.
Aceite proposto: Consultar perspectiva individual e comparar com estado verdadeiro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar simulação de prova de produção empresarial.
- Não inferir personalidade humana real a partir de agente textual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar memória e coordenação dentro do simulador; realismo de personagens não demonstra inteligência social geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T054, T058, T071

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R005 — LLMLingua

**Nome canônico:** LLMLingua — compressão de prompts em múltiplas etapas  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R005  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** LLM Lingua; compressor de prompt; prompt compression LLMLingua

## R005:C01 — conceito

Método de compressão de prompts que combina controle de orçamento e seleção iterativa de conteúdo. O texto comprimido continua sendo fornecido ao modelo alvo. A ficha usa o artigo original como referência e distingue LongLLMLingua, uma extensão voltada a cenários de contexto longo.

Como funciona:
- Definir quanto contexto pode ser preservado no orçamento.
- Avaliar conteúdo e aplicar compressão em etapas para reduzir redundância.
- Executar o modelo alvo com o resultado comprimido e comparar a tarefa final.

Nota de nomenclatura: LLMLingua pode designar uma família de ferramentas. As variantes têm mecanismos e requisitos próprios; esta ficha não trata todas como um único algoritmo.

## R005:C02 — aplicacao

Quando usar:
- Prompts extensos e repetitivos cujo custo de processamento domina o fluxo.
- Tarefas com conjunto de avaliação que permita detectar perda de informação relevante.

Quando não usar:
- Quando cada caractere de um contrato, código ou registro precisa ser preservado literalmente sem perda.

Implementação proposta:
- Proposta: fixar versão do compressor, tokenizer e modelo alvo.
- Experimentar razões de compressão conservadoras antes de elevar a redução.
- Comparar qualidade, latência total e custo, incluindo o compressor e a recuperação das fontes originais.

Aplicação LAI proposta:
Proposta LAI: experimentar em históricos repetitivos e documentos recuperados; manter instruções obrigatórias e campos exatos fora de uma compressão destrutiva.

## R005:C03 — riscos_validacao

Armadilhas:
- Uma pequena exclusão pode remover negação, unidade, condição ou nome decisivo.
- A redução de tokens não garante menor latência se o compressor custar mais que o prefill economizado.

Métricas sugeridas:
- Razão entre tokens antes e depois, medida pelo tokenizer do destino.
- Variação de acurácia e tempo completo da chamada, incluindo compressão.

Testes propostos:
- Proposta: incluir pares que diferem apenas por uma negação e verificar que a resposta mantém a distinção.
- Comparar prompts originais e comprimidos em dados reservados, sem aceitar economia acompanhada de erro crítico.

## R005:C04 — perguntas_proveniencia

Pergunta: LLMLingua é Context Distillation?
Resposta: Não são equivalentes. Aqui a redução é aplicada ao texto enviado; a destilação paramétrica treina comportamento nos pesos ou adaptadores.

Pergunta: Posso adotar a maior razão publicada?
Resposta: Não automaticamente. O limite aceitável depende de tarefa, idioma, modelo e custo dos erros.

Pergunta: O gerador precisa ler texto perfeitamente gramatical?
Resposta: Nem sempre, mas a tarefa precisa conservar sentido suficiente. Aparência estranha não prova perda, e texto fluente não prova fidelidade.

Pergunta: A taxa configurada é a economia final da aplicação?
Resposta: Não. Some compressor, reprocessamento, overhead e possíveis releituras. O custo líquido depende do uso real e da qualidade preservada.

Escopo das fontes:
A-S015 sustenta os componentes do método original; A-S018 identifica LongLLMLingua. Não foram reproduzidos seus benchmarks nem afirmados ganhos específicos para o Qwen.

## R005:C05 — mecanismo_avancado

O LLMLingua original combina controle de orçamento, compressão iterativa de tokens e alinhamento de distribuição entre modelos. O repositório atual reúne variantes com mecanismos diferentes: LongLLMLingua condiciona a tarefa de contexto longo, enquanto LLMLingua-2 usa classificação aprendida de tokens. Reproduzir um resultado exige registrar variante, checkpoint e configuração; citar apenas o nome do pacote não identifica o método executado.

Condição de contorno:
A redução de tokens pode deixar de compensar quando o custo do compressor domina ou quando detalhes removidos provocam novas buscas e geração adicional.

Contrato proposto:
- Entradas: Prompt estruturado, orçamento, variante escolhida e trechos que não podem ser comprimidos.
- Saídas: Texto reduzido, métricas de tamanho e referências ao original para validar conteúdo preservado.
- Estado: Checkpoint do compressor, tokenizer, parâmetros e versões do gerador consumidor.
- Invariante: Preservar uma palavra ou símbolo não é tratado como garantia de preservar a relação lógica da frase.

Compromissos de projeto:
- Compressão extrativa conserva partes do original e pode quebrar relações entre elas.
- Seções protegidas reduzem risco de perder contratos e limitam a compressão máxima alcançável.

## R005:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: proteger os tokens de uma condição, mas permitir remoção da ligação entre condição e consequência. A verificação deve detectar a mudança semântica apesar de todas as palavras protegidas continuarem presentes.

Plano de avaliação proposto:
Avaliação proposta: comparar prompt integral, seleção por passagem e variante específica do LLMLingua com mesmo gerador. Medir sustentação, preservação de exceções, custo do compressor e latência total; incluir taxas de compressão graduais, sem presumir um ganho fixo.

Comparações:
- T037 (complements): Condicionamento à pergunta é relevante em variantes apropriadas, mas não define todos os métodos do pacote.
- R006 (distinct_from): LLMLingua entrega contexto reduzido ao gerador; PRISM transfere comportamento para adaptadores treinados.

Afirmação rastreável:
O artigo original descreve compressão coarse-to-fine; o repositório distingue variantes e documenta preservação de tokens e seções.
Suporte: direct; fontes: A-S015, V3A-S044
Limite: Opções de uma variante não devem ser atribuídas automaticamente às demais; a pesquisa não executou o pacote.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R005:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciou variantes LLMLingua. Aqui a seleção de variante depende do consumidor e do perfil de carga, com teste de robustez de leitura.

Projeto e decomposição
Escolha entre compressão orientada à consulta e independente da tarefa conforme reutilização prevista. Um corpus consultado de muitas formas pode não amortizar recompressão específica por pergunta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

Controle adaptativo
Avalie legibilidade funcional para cada leitor 3–30B. O fato de um modelo grande interpretar tokens selecionados não prova que um modelo menor preserve relações, negações e referências.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

Validação contrafactual
Compare variantes com taxa efetiva e custo completo, incluindo compressor, leitura e expansão de recuperação. Meça qualidade por tipo de informação, não apenas compressão média. Unidade de avaliação: pipeline compressor-leitor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

USO AVANÇADO — RAG local de baixa latência
Cenário: Documentos retornados são redundantes.
Estratégia: Usar compressor leve após recuperação, proteger campos decisivos e encaminhar original quando teste de suporte falhar.
Papel do modelo pequeno: 3–7B lê pacote conservador.
Aceite proposto: Não reduzir latência sacrificando unidade, negação ou fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

USO AVANÇADO — Análise recorrente de dossiê
Cenário: Várias perguntas usam o mesmo material.
Estratégia: Comparar representação geral reutilizada com compressão por pergunta; manter original e medir custo acumulado por sessão.
Papel do modelo pequeno: 8–14B integra; 15–30B audita casos difíceis.
Aceite proposto: Escolher variante por custo por resposta aceita, não por taxa anunciada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028, V3A-S001.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de compressão moderada com relações explícitas e recuperação de fallback.
8–14B: Leitor de texto mais denso após validação de fidelidade contextual.
15–30B: Professor ou auditor de preservação, sem presumir comportamento igual entre modelos.
Requisitos de treino/runtime: Versão exata da biblioteca e compressor, tokenizer do leitor e dados próprios de avaliação; integração Prompt flow é disponibilidade.
Não aplicar quando: Compressão custa mais que leitura ou produz texto que o consumidor não interpreta com confiabilidade.

## R005:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação expõe ferramenta de compressão utilizável em fluxo.
Mecanismo documentado: Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.
Correspondência com esta base: Integração do projeto identificado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.
Limite: Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S027.

V4A-C031 — Microsoft Research / LLMLingua-2
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa formula compressão como classificação de tokens treinada com dados destilados.
Mecanismo documentado: Compressor especializado seleciona texto para um leitor posterior.
Correspondência com esta base: Variante da família, distinta do original.
Transferência proposta para modelo pequeno: Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.
Limite: Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V3A-S001, V4A-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## R005:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R005 → T037 [complements]
Como combinar: Condicionar seleção à pergunta quando variante suportar.
Interface: Pergunta, trechos e taxa efetiva.
Condição: Objetivo permanecer estável durante reuso.
Aceite proposto: Trocar pergunta e testar perda de evidência relevante.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028, V3A-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R005 → T042 [requires]
Como combinar: Contar contexto final e reserva do consumidor.
Interface: Tokens após compressão, metadados e saída prevista.
Condição: Contagem usar protocolo do leitor.
Aceite proposto: Comparar taxa solicitada e redução efetiva em tokens.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028, V3A-S001. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar integração em biblioteca de produção comprovada.
- Não transportar ganhos publicados para todo modelo pequeno.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar pipeline completo com leitura integral; compressor eficiente pode piorar um consumidor menos robusto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T020, T037, T018

## Fontes primárias associadas

### A-S015 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models

[https://aclanthology.org/2023.emnlp-main.825/](https://aclanthology.org/2023.emnlp-main.825/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão textual com orçamento e seleção iterativa de tokens.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S018 — LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression

[https://arxiv.org/abs/2310.06839](https://arxiv.org/abs/2310.06839)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão voltada à informação relevante em contextos longos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S044 — LLMLingua official implementation

[https://github.com/microsoft/LLMLingua](https://github.com/microsoft/LLMLingua)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenciação das variantes LLMLingua, LongLLMLingua e LLMLingua-2; opções de preservação e compressão estruturada documentadas no README.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V4A-S027 — LLMLingua Prompt Compression — Prompt flow

[https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html](https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração documentada de compressor e contrato de entrada/saída; não comprova carga real.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R006 — PRISM

**Nome canônico:** PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** PRISM prompt compression; internalização seletiva em LoRA

## R006:C01 — conceito

Trabalho que identifica qual componente do prompt mais contribui para uma tarefa e procura internalizar esse comportamento em adaptadores LoRA. Distingue tarefas dominadas por padrões de exemplos daquelas dominadas por instruções procedimentais. O diagnóstico orienta o alvo da compressão paramétrica.

Como funciona:
- Comparar desempenho com instruções isoladas e com exemplos isolados.
- Gerar dados de supervisão a partir das saídas com o prompt completo.
- Treinar adaptadores para reproduzir o componente selecionado com menos contexto explícito.

Nota de nomenclatura: Nome desambiguado pelo título completo e pela fonte A-S011; não confundir com outros projetos PRISM.

## R006:C02 — aplicacao

Quando usar:
- Tarefas repetidas com prompts estáveis e conjunto de avaliação reservado.
- Estudo de troca entre custo de treinamento e custo recorrente de inferência.

Quando não usar:
- Para memorizar fatos voláteis que precisam de atualização exata e imediata.

Implementação proposta:
- Proposta: medir a linha de base e os dois componentes do prompt sem alterar o restante da tarefa.
- Filtrar exemplos gerados pelo professor e registrar suas falhas antes do treinamento.
- Comparar adaptador e prompt completo em tarefas novas, incluindo alterações posteriores de instrução.

Aplicação LAI proposta:
Proposta LAI: considerar para schemas e procedimentos estáveis do Qwen somente depois de medir a alternativa com prompt curto e recuperação de exemplos.

## R006:C03 — riscos_validacao

Armadilhas:
- Uma saída errada gerada com o prompt completo pode virar supervisão persistente.
- Um benefício medido em um conjunto não garante transferência a outro domínio ou checkpoint.

Métricas sugeridas:
- Desempenho sem o componente removido e quantidade de tokens efetivamente eliminada.
- Custo total de treinamento, inferência e atualização do comportamento.

Testes propostos:
- Proposta: reservar exemplos fora do processo de geração e seleção de dados.
- Mudar uma regra de execução e medir se o adaptador respeita a nova instrução ou retém o comportamento antigo.

## R006:C04 — perguntas_proveniencia

Pergunta: PRISM dispensa treinamento?
Resposta: Não. A proposta identificada usa autodestilação e treinamento de adaptadores LoRA.

Pergunta: PRISM significa qualquer projeto com esse nome?
Resposta: Não. Aqui a referência é o título completo registrado na ACL Anthology; há homônimos.

Pergunta: O diagnóstico garante que treinar compensa?
Resposta: Não. É um sinal sobre a contribuição do prompt. Custo, reutilização, generalização e preservação de exceções ainda precisam ser medidos.

Pergunta: Posso remover toda instrução após o treinamento?
Resposta: Somente se o desenho e a avaliação sustentarem isso. Regras variáveis e condições novas podem continuar exigindo contexto explícito.

Escopo das fontes:
A-S011 sustenta diagnóstico de componentes e internalização em LoRA. Percentuais do artigo não foram reproduzidos ou prometidos para a LAI.

## R006:C05 — mecanismo_avancado

O diagnóstico de PRISM compara comportamento com instruções e com exemplos para escolher o componente a internalizar. Essa ablação é informativa, mas interação entre componentes pode impedir interpretação puramente aditiva: exemplos podem ensinar formato somente quando uma instrução explica a exceção. A supervisão silver vem do modelo com prompt completo; portanto, erros sistemáticos desse professor podem ser transferidos ao adaptador, mesmo que a compressão preserve seu comportamento.

Condição de contorno:
O ganho diminui quando a tarefa muda frequentemente, há pouca reutilização para amortizar treinamento ou os exemplos não representam as exceções operacionais importantes.

Contrato proposto:
- Entradas: Tarefa, prompt decomposto, modelo base, entradas de treinamento e dados independentes de avaliação.
- Saídas: Adaptador identificado e prompt residual, acompanhados do diagnóstico de componentes e resultados verificáveis.
- Estado: Versão do backbone, prompt professor, dados silver, configuração de treinamento e escopo da tarefa.
- Invariante: Um adaptador não é apresentado como equivalente ao prompt completo fora das condições em que essa equivalência foi avaliada.

Compromissos de projeto:
- Internalização reduz contexto repetido e torna correções dependentes de um ciclo de treinamento e validação.
- Dados silver reduzem anotação humana e herdam limitações do professor e da distribuição de entradas.

## R006:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir exceções dependentes da interação entre instrução e exemplo, depois comprimir o componente selecionado. A avaliação deve detectar perda das exceções, ainda que a média das tarefas comuns pareça boa.

Plano de avaliação proposto:
Avaliação proposta: comparar prompt completo, componentes isolados, prompt reduzido sem adaptador e PRISM na mesma divisão independente. Medir qualidade por caso, obediência a novas instruções, tokens e custo amortizado de treinamento; não escolher o diagnóstico usando o teste final.

Comparações:
- R007 (distinct_from): PRISM seleciona comportamento de componentes do prompt; SADA enfatiza interface interna e alinhamento de estados para adaptadores.
- T069 (distinct_from): Resumo externo continua sendo lido como dados; PRISM modifica comportamento por pesos adicionais treinados.

Afirmação rastreável:
PRISM usa diagnóstico entre instruções e exemplos e autodestilação de saídas do prompt completo para treinar adaptadores LoRA.
Suporte: direct; fontes: A-S011
Limite: A sigla é ambígua fora deste catálogo; esta ficha corresponde exclusivamente ao trabalho de Jha, Wang, Barbu e Aggarwal na EMNLP 2026.

Nota de pesquisa:
Identificação reconferida em 2026-11-05: PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights, Eshita Jha, Mingxian Wang, Andrei Barbu e Chetan Aggarwal, https://aclanthology.org/2026.emnlp-main.2431/. Escopo coincide com a v2; não foram associados trabalhos homônimos. Contratos e testes são propostas editoriais, sem treinamento ou reprodução de resultados.

## R006:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 verificou PRISM e suas ablações. Aqui o foco é governar atualização de adapters quando o componente internalizado do prompt muda.

Projeto e decomposição
Mantenha identidade exata: Prompt Representation Internalization via Selective Compression into LoRA Weights. A proposta distingue o que foi internalizado e o que continua explícito no prompt.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

Controle adaptativo
Uma mudança de procedimento ou padrão exige avaliar se adapter antigo permanece válido. Remover instrução do contexto e depois esquecê-la no treinamento cria divergência difícil de observar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

Validação contrafactual
Compare mesmo modelo com prompt completo, adapter e prompt residual. Meça aderência a mudanças, custo de retreino e interferência em tarefas não alvo; rótulos do professor podem propagar erro. Unidade de avaliação: adapter por versão de instrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

USO AVANÇADO — Rotina repetitiva estável
Cenário: Instruções extensas se repetem em muitos pedidos.
Estratégia: Identificar componente dominante, gerar dados de treino autorizados e validar substituição seletiva antes de retirar texto do prompt.
Papel do modelo pequeno: 3–7B aluno em tarefa estreita.
Aceite proposto: Adapter deve manter exceções e formato em casos novos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

USO AVANÇADO — Política com revisões
Cenário: Uma regra internalizada precisa mudar.
Estratégia: Versionar instrução e adapter juntos, testar regra antiga versus nova e manter prompt explícito durante transição.
Papel do modelo pequeno: 8–14B aluno; 15–30B professor possível.
Aceite proposto: Nenhuma resposta pode seguir regra revogada sem detecção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S011, V4A-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Aluno especializado em padrão fechado, com controle de regressões.
8–14B: Aluno para procedimento mais variado e prompt residual explícito.
15–30B: Professor ou aluno complexo quando treinamento e benefício forem demonstrados.
Requisitos de treino/runtime: Treino LoRA, dados de professor, versão da instrução e avaliação independente; nenhuma implantação PRISM foi executada.
Não aplicar quando: Regras mudam rápido, exigem auditoria literal a cada chamada ou diagnóstico não identifica componente estável.

## R006:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C032 — Eshita Jha, Mingxian Wang, Andrei Barbu, Chetan Aggarwal / PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda internalização seletiva de componente de prompt.
Mecanismo documentado: Diagnóstico distingue padrões e procedimentos; dados derivados do professor treinam LoRA.
Correspondência com esta base: Título e autores preservam identidade da sigla.
Transferência proposta para modelo pequeno: Proposta de engenharia: Comparar adapter 3–30B ao mesmo modelo com instrução completa e medir custo de atualização.
Limite: Não encontrada implantação bigtech exata nesta pesquisa; resultados não legitimam trocar de PRISM homônimo. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Consulta encontrou pesquisa e integração relacionada de compressão, não implantação bigtech exata do PRISM identificado. Sigla não foi associada a trabalhos homônimos.
Consultas registradas: V4A-Q017, V4A-Q024.

## R006:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R006 → T179 [complements]
Como combinar: Tratar internalização como atualização paramétrica.
Interface: Prompt de origem, dados e adapter versionado.
Condição: Pesos realmente serem treinados e avaliados.
Aceite proposto: Comparar aluno antes e depois, mantendo tarefa e fontes constantes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S011, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R006 → T072 [requires]
Como combinar: Vincular adapter à versão de instrução.
Interface: adapter_id, instrução, base model e dados.
Condição: Roteamento impedir uso de versão incompatível.
Aceite proposto: Enviar pedido sob regra nova ao adapter antigo e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S011, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir PRISM com trabalhos homônimos.
- Não apresentar LoRA treinada como cache de contexto sem custo de manutenção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar substituição de instrução numa tarefa definida; não inferir paridade geral com o professor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T179, T180, T182, R007

## Fontes primárias associadas

### A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

[https://aclanthology.org/2026.emnlp-main.2431/](https://aclanthology.org/2026.emnlp-main.2431/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diagnóstico de componentes do prompt e autodestilação seletiva em adaptadores LoRA.

Limite: Identificação pelo título completo; há projetos homônimos. Resultados publicados não foram reproduzidos nesta entrega.

### V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs

[https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo 8B disponível e adaptadores experimentais por subtarefa RAG; separar disponibilidade e experimento.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R007 — SADA

**Nome canônico:** SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R007  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** State-Aligned Distillation Adapters; adaptadores com alinhamento de estados

## R007:C01 — conceito

Pesquisa sobre conversão de contexto em adaptadores que procura preservar estados internos relevantes do modelo com contexto completo. O trabalho identifica divergência de estados entre o modelo com adaptador e o modelo de referência e propõe alinhamento para reduzir essa diferença.

Como funciona:
- Escolher representações internas adequadas para informar o mapeamento contexto-parâmetros.
- Usar a saída do bloco de atenção como interface de representação.
- Treinar com sinal de alinhamento entre os estados do modelo com adaptador e os do modelo com contexto completo.

Nota de nomenclatura: SADA está desambiguado pelo título completo da publicação; o nome sozinho não define compatibilidade com outros modelos.

## R007:C02 — aplicacao

Quando usar:
- Pesquisa que disponha de acesso às ativações e ao treinamento do modelo.
- Comparações controladas de retenção de contexto explícito versus compressão em parâmetros.

Quando não usar:
- Como recurso ativável apenas por prompt em uma API fechada sem acesso aos estados internos.

Implementação proposta:
- Proposta: verificar implementação, checkpoints e tarefas usadas no trabalho antes de portar a arquitetura.
- Reproduzir um caso pequeno medindo estados internos e desempenho final simultaneamente.
- Comparar com contexto completo e adaptação sem alinhamento, incluindo casos em que manter o texto é necessário.

Aplicação LAI proposta:
Proposta LAI: tratar como experimento de pesquisa posterior à memória externa e à destilação convencional, com critérios próprios de compatibilidade e ganho.

## R007:C03 — riscos_validacao

Armadilhas:
- Estados mais próximos não garantem resposta correta em toda tarefa.
- Mudar arquitetura ou tokenizer pode invalidar o mapeamento e exigir novo treinamento.

Métricas sugeridas:
- Qualidade da tarefa e divergência de representações por camada.
- Custo de produzir adaptadores, memória usada e latência total por contexto.

Testes propostos:
- Proposta: fazer ablação do alinhamento mantendo dados e orçamento constantes.
- Incluir perguntas que dependem de detalhes exatos para medir perdas ocultas pela média de desempenho.

## R007:C04 — perguntas_proveniencia

Pergunta: SADA é um banco de memória textual?
Resposta: Não. A referência identificada trata mapeamento de contexto em adaptadores e alinhamento de representações.

Pergunta: Alinhar estados torna a compressão sem perda?
Resposta: Não há garantia geral. É necessário medir tarefas e casos em que detalhes do contexto precisam permanecer explícitos.

Pergunta: Por que comparar estados e respostas separadamente?
Resposta: Divergência interna ajuda diagnosticar o mecanismo, mas a utilidade final depende da tarefa. Uma melhora em uma medida não substitui a outra.

Pergunta: O método equivale a resumir texto num arquivo?
Resposta: Não. Ele produz parâmetros de adaptação por uma interface neural treinada. Persistir um resumo externo opera em outro nível do sistema.

Escopo das fontes:
A-S012 sustenta a proposta de interface de estados e alinhamento. Não houve auditoria do código nem reprodução dos experimentos.

## R007:C05 — mecanismo_avancado

SADA aborda a diferença entre reproduzir uma resposta final e preservar estados internos próximos aos obtidos com contexto completo. Atribui divergência em camadas profundas à seleção de entrada inadequada e à supervisão insuficiente. Usa a saída do bloco de atenção como interface e alinhamento de estados na destilação. Isso exige acesso aos componentes internos; uma comparação apenas textual não reproduz o mecanismo proposto.

Condição de contorno:
Estados internos semelhantes não garantem por si só resposta correta, e a interface aprendida pode perder validade quando mudam backbone, camadas ou distribuição do contexto.

Contrato proposto:
- Entradas: Modelo compatível, contexto professor, representações internas selecionadas e mecanismo de geração de adaptadores.
- Saídas: Pesos temporários e avaliação da geração junto de medidas de divergência interna.
- Estado: Versões de camadas, treinamento, interface de features e configuração de leitura do adaptador.
- Invariante: Um adaptador é vinculado ao modelo e contexto de origem; não é tratado como memória universal intercambiável.

Compromissos de projeto:
- Comprimir contexto em parâmetros pode reduzir custo de inferência e exige computação para produzir e aplicar adaptadores.
- Alinhar estados oferece sinal de treinamento adicional e aumenta acesso necessário à arquitetura e custo de adaptação.

## R007:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar o backbone ou a interface de camada mantendo o mapeamento treinado. Verifique divergência interna e qualidade da saída, sem aceitar compatibilidade apenas porque os tensores têm dimensões iguais.

Plano de avaliação proposto:
Avaliação proposta: comparar contexto explícito, adaptação sem alinhamento e SADA com backbone fixo. Medir saída sustentada, distância de estados por camada, memória e latência incluindo geração do adaptador; incluir situações em que reter texto explícito é preferível.

Comparações:
- R006 (distinct_from): PRISM diagnostica componentes dominantes; SADA trata seleção de interface e supervisão de estados na parametrização do contexto.
- T052 (complements): O método depende de representações internas compatíveis, dentro da família ampla de contexto latente.

Afirmação rastreável:
SADA propõe attention-block output como interface e state-alignment distillation para reduzir divergência de estados frente ao modelo com contexto completo.
Suporte: direct; fontes: A-S012
Limite: Esta ficha refere-se ao artigo de Gao e coautores na ACL 2026; nenhuma garantia é transferida a trabalhos homônimos ou modelos arbitrários.

Nota de pesquisa:
Identificação reconferida em 2026-11-05: SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters, Wenhao Gao, Tianlong Wang, Wei Jia, Linhao Zhang, Aiwei Liu, Miao Fan e Zhou Xiao, https://aclanthology.org/2026.acl-long.1046/. Escopo coincide com a v2. Link de código consta na publicação, mas não houve instalação nem execução; contratos e avaliações são propostas.

## R007:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 identificou SADA e interface de estados. Aqui adapters derivados de contexto recebem isolamento, expiração e avaliação funcional por sessão.

Projeto e decomposição
Preserve identidade: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters. A proposta exige relacionar adapter ao contexto que o produziu, ao modelo-base e à interface de estados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

Controle adaptativo
Se o contexto muda ou pertence a outro escopo, o adapter anterior não pode ser reutilizado por semelhança. Cache de adapter precisa de identidade exata e condições de validade, não apenas nome da tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

Validação contrafactual
Compare erro de alinhamento interno e qualidade final separadamente. Teste contexto correto, trocado e revogado; estados próximos podem produzir resposta errada ou conservar informação que já deveria ser desconsiderada. Unidade de avaliação: adapter e contexto de origem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

USO AVANÇADO — Contexto recorrente especializado
Cenário: Muitas chamadas usam o mesmo material estável.
Estratégia: Avaliar custo de criar adapter e reutilizá-lo, mantendo caminho de leitura textual para mudanças e auditoria.
Papel do modelo pequeno: 15–30B modelo aberto experimental.
Aceite proposto: Amortização deve incluir geração, troca e invalidação do adapter.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

USO AVANÇADO — Sessões isoladas
Cenário: Cada tarefa contém informações próprias.
Estratégia: Associar adapter a sessão e contexto, impedir carga cruzada e verificar limpeza ao trocar tarefa.
Papel do modelo pequeno: 8–14B somente se arquitetura adaptada.
Aceite proposto: Nenhuma saída pode usar conteúdo de contexto de outra sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S012, V3A-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Baseline textual ou aluno experimental restrito, sem compatibilidade presumida.
8–14B: Consumidor adaptado apenas com acesso a estados e treinamento validado.
15–30B: Alvo de pesquisa com instrumentação de camadas e análise de custo.
Requisitos de treino/runtime: Modelo aberto compatível, acesso aos estados, treino e versionamento; a pesquisa não é API universal para modelos fechados.
Não aplicar quando: Não há controle da interface neural ou o contexto muda antes de amortizar adaptação.

## R007:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C033 — Wenhao Gao, Tianlong Wang, Wei Jia, Linhao Zhang, Aiwei Liu, Miao Fan, Zhou Xiao / SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda adaptação de contexto por alinhamento de estados.
Mecanismo documentado: Distilação aproxima estados em interface de blocos de atenção usando adapters.
Correspondência com esta base: Título e autores fixam escopo da sigla.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar modelo aberto em faixa permitida com instrumentação de estados e teste funcional separado.
Limite: Nenhuma produção bigtech exata estabelecida; alinhamento interno não garante resposta correta. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S012.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Não foi estabelecida implantação bigtech exata do SADA identificado. A transferência a 3–30B permanece proposta dependente de arquitetura, treino e avaliação.
Consultas registradas: V4A-Q017, V4A-Q024.

## R007:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R007 → T052 [requires]
Como combinar: Fixar significado da representação alinhada.
Interface: Camada, tensor, máscara e versão do modelo.
Condição: Interface coincidir com o treinamento.
Aceite proposto: Trocar camada de leitura e medir falha funcional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S012, V3A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R007 → T031 [complements]
Como combinar: Invalidar adapter quando contexto ou escopo mudar.
Interface: Context_digest, session_id e validade.
Condição: Relação com contexto de origem ser verificável.
Aceite proposto: Revogar contexto e impedir carregamento do adapter antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S012, V3A-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir SADA com siglas homônimas.
- Não usar alinhamento de estados como prova suficiente de correção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefa e modelo-base fixos com contexto textual; não prometer equivalência geral ao professor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T052, T179, T182, R006

## Fontes primárias associadas

### A-S012 — SADA: Bridging In-Context Learning and Fine-Tuning via State-Aligned Distillation Adapters

[https://aclanthology.org/2026.acl-long.1046/](https://aclanthology.org/2026.acl-long.1046/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapeamento contexto-parâmetros e alinhamento de estados para adaptadores.

Limite: Leitura do resumo e metadados; código não auditado e resultados não reproduzidos.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R008 — LangGraph

**Nome canônico:** LangGraph  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** LangGraph runtime

## R008:C01 — conceito

Runtime e framework de orquestração para agentes com estado e fluxos em grafo. Permite combinar nós determinísticos e chamadas de modelos, controlar transições e integrar persistência. Não é uma LLM, um RAG pronto nem um planejador universal; essas partes precisam ser projetadas pela aplicação.

Como funciona:
- Definir estado, nós e arestas do workflow.
- Executar transições segundo condições e resultados.
- Usar checkpointers e stores apropriados quando continuidade e memória forem necessárias.

## R008:C02 — aplicacao

Quando usar:
- Aplicação precisa de controle explícito de estado e fluxo.
- Missões exigem interrupção, retomada e observabilidade.

Quando não usar:
- Adotar framework apenas para uma única chamada simples sem necessidade de estado.

Implementação proposta:
- Fixar versão e consultar documentação correspondente antes de integrar.
- Construir prova pequena com modelo local ou remoto por adaptador.
- Escolher persistência durável e política de migração do estado para uso real.

Aplicação LAI proposta:
Proposta: avaliar LangGraph como componente possível da Helena somente após comparar requisitos e capacidades já existentes.

## R008:C03 — riscos_validacao

Armadilhas:
- Exemplo com backend em memória não demonstra retomada após reinício.
- Misturar side effects no replay pode duplicar ações se o fluxo não foi projetado para isso.

Métricas sugeridas:
- Conclusão correta de workflow e retomada após falha.
- Custo operacional e complexidade comparados ao runtime existente.

Testes propostos:
- Interromper o processo e retomar usando armazenamento persistente.
- Atualizar schema de estado e testar compatibilidade com missões já iniciadas.

## R008:C04 — perguntas_proveniencia

Pergunta: Precisa usar LangChain para usar LangGraph?
Resposta: A documentação consultada informa que não, embora exemplos frequentemente usem suas integrações.

Pergunta: Instalar LangGraph dá memória factual correta?
Resposta: Não. É preciso definir conteúdo, proveniência e recuperação.

Pergunta: O redutor padrão concatena mensagens concorrentes?
Resposta: Não. É necessário escolher uma regra adequada ao canal e testar conflitos e repetição.

Pergunta: O store substitui o checkpointer da conversa?
Resposta: Não. O store compartilha dados entre threads; a retomada do estado da thread exige persistência apropriada.

Escopo das fontes:
Documentação oficial consultada descreve grafo, persistência e ausência de arquitetura de agente prescrita. O roteiro de integração e avaliação é proposta editorial.

## R008:C05 — mecanismo_avancado

No LangGraph, nós devolvem atualizações parciais e cada canal de estado define como combiná-las. O redutor padrão substitui o valor; acumulação precisa de regra explícita. Isso torna o merge parte da semântica, especialmente quando vários nós executam no mesmo superpasso. Separar schemas de entrada, saída e estado interno organiza a interface, mas não filtra automaticamente o streaming. Assim, um canal omitido da resposta de invoke ainda pode aparecer em eventos transmitidos se a aplicação não selecionar a projeção adequada. Checkpointer por thread e store entre threads também representam escopos diferentes.

Condição de contorno:
Persistir estado não torna o redutor correto nem converte um canal privado em fronteira de acesso. Compatibilidade depende das versões do grafo e do backend.

Contrato proposto:
- Entradas: Atualizações tipadas, identificação da thread, versão do grafo e projeção permitida para streaming.
- Saídas: Estado consolidado e eventos filtrados para cada consumidor.
- Estado: Canais, redutores, checkpoints e namespace do store explicitamente separados.
- Invariante: Cada atualização preserva a identidade dos fatos; nenhuma saída pública inclui canais excluídos pelo contrato.

Compromissos de projeto:
- Redutor acumulativo conserva contribuições, mas pode duplicar mensagens sem identidade estável.
- Streaming melhora acompanhamento, porém amplia as superfícies que precisam de projeção e validação.

## R008:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois nós escrevem no mesmo canal e um inclui dado interno. Variar ordem de conclusão, inspecionar invoke e stream; exigir merge previsto e ausência do dado no consumidor público.

Plano de avaliação proposto:
Comparar execução serial com paralela, fixando entradas e resultados dos nós. Medir equivalência do estado, duplicações, eventos indevidos e latência; adotar concorrência somente preservando as invariantes definidas.

Comparações:
- R017 (distinct_from): LangChain compõe agentes em nível mais alto; LangGraph expõe diretamente estado, transições e fusão de atualizações.
- T142 (distinct_from): Framework com planejamento é uma família; configurar LangGraph não acrescenta um planejador automaticamente.

Afirmação rastreável:
Schemas de entrada e saída restringem invoke, mas não ocultam canais do streaming por padrão.
Suporte: direct; fontes: V3C-S006
Limite: Comportamento documentado da Graph API consultada; mecanismos concretos devem corresponder à versão integrada.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R008:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o merge e a persistência anteriores com evolução de grafos em execução, testes algébricos de junção e isolamento de resultados que chegam depois da mudança de intenção.

Evolução com conversas abertas
Proposta: versionar grafo, schema e política junto do checkpoint. Classificar migrações em leitura compatível, transformação explícita ou encerramento controlado. Manter o executor antigo enquanto houver estados incompatíveis evita reinterpretar um nó pendente com significado novo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

Junção sob reentrega
Testar redutores com permutações, duplicatas e resultados tardios. Associatividade ou idempotência só devem ser exigidas quando o domínio permite; uma sequência de decisões pode exigir ordem. Registrar revisão da intenção em cada ramo permite rejeitar uma resposta correta para uma pergunta já cancelada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

Estado público por projeção
Construir uma projeção de saída a partir do estado validado, separada do estado de trabalho. O fluxo de eventos recebe a mesma revisão e política de exposição. A proposta trata vazamento de eventos e resposta final como superfícies distintas, com testes próprios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

USO AVANÇADO — Atendimento com mudança de solicitação
Cenário: Cliente altera o pedido enquanto duas consultas executam.
Estratégia: Incrementar revisão da intenção, preservar resultados auditáveis e impedir que ramos antigos atualizem a resposta atual.
Papel do modelo pequeno: Classificar a alteração e extrair campos; a decisão de validade pertence ao controlador.
Aceite proposto: Reproduzir chegada fora de ordem e confirmar ausência de resposta ou efeito da revisão cancelada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

USO AVANÇADO — Migração de workflow vivo
Cenário: Novo contrato de ferramenta precisa coexistir com sessões antigas.
Estratégia: Roteá-las pela versão persistida e migrar somente estados com transformação testada.
Papel do modelo pequeno: Produzir estado tipado sem escolher silenciosamente a versão de execução.
Aceite proposto: Retomar amostras históricas e conferir transições, efeitos e projeção final por versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S006, V3D-S016, V4C-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: nós de extração ou classificação com estados pequenos e ramos explícitos.
8–14B: 8–14B: decisões locais com poucas ferramentas, limitadas por critérios externos.
15–30B: 15–30B: síntese de ramos quando a avaliação mostrar ganho sobre agregação determinística.
Requisitos de treino/runtime: Persistência, versões e redutores pertencem à aplicação; não exigem treino da LLM.
Não aplicar quando: Não adotar grafo complexo quando uma função determinística e uma chamada resolvem a tarefa.

## R008:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C027 — Klarna / relato LangChain / AI Assistant com LangGraph
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: Relato de fornecedor identifica tarefas de suporte com roteamento e instruções adaptadas.
Mecanismo documentado: LangGraph coordena tarefas; LangSmith apoia observação, avaliação e evolução de prompts.
Correspondência com esta base: Fonte nomeia LangGraph na arquitetura.
Transferência proposta para modelo pequeno: Proposta: usar estados curtos e prompts por tarefa em modelos pequenos, avaliando erros de roteamento e resolução.
Limite: Classificação conservadora: nesta pesquisa detalhes técnicos vêm do fornecedor, sem abertura de relato técnico do operador. Não conta para dez casos de produção.
Fontes: V4C-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Klarna é relato de cliente pelo fornecedor e permanece produto/uso documentado com limites. A busca LinkedIn não confirmou LangGraph; sem atribuição por semelhança arquitetural.
Consultas registradas: V4C-Q021, V4C-Q026.

## R008:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R008 → T060 [complements]
Como combinar: Vincular retomada à versão do grafo e à revisão da intenção.
Interface: Checkpoint, graph_version, intent_revision e próximo nó.
Condição: Sessões atravessam deploys ou falhas.
Aceite proposto: Um checkpoint incompatível é recusado ou migrado por regra registrada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006, V3D-S016, V4C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R008 → T148 [complements]
Como combinar: Resolver elegibilidade do ramo antes de publicar seu resultado.
Interface: Predicado tipado e revisão do estado de origem.
Condição: Existem ramos paralelos ou decisões atrasadas.
Aceite proposto: Resultado de ramo obsoleto não altera o estado vigente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S006, V3D-S016, V4C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não inferir independência apenas porque nós executam em paralelo.
- Não usar memória entre threads sem namespace e política de visibilidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar o mesmo grafo e ferramentas com modelos diferentes; depois ablar a estrutura. Contabilizar ramos descartados e efeitos incorretos, não apenas respostas finais.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T142, T154, T159, T160

## Fontes primárias associadas

### C-S009 — LangGraph overview

[https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime de grafos com estado, controle de fluxo e integração de operações determinísticas e de LLM.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S019 — Persistence — LangGraph

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers mantêm estado de threads; stores preservam informação definida pela aplicação entre threads.

Limite: A URL durable-execution redirecionou para persistence na consulta; exemplos InMemory não demonstram durabilidade após queda de processo.

### C-S023 — Temporal Workflow Execution overview

[https://docs.temporal.io/workflow-execution](https://docs.temporal.io/workflow-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução durável recupera estado por histórico de eventos e replay sujeito a determinismo.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S006 — LangGraph — Graph API overview

[https://docs.langchain.com/oss/python/langgraph/graph-api](https://docs.langchain.com/oss/python/langgraph/graph-api)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supersteps, reducers de estado, Send, Command, migrações e reexecução de nós.

Limite: Documentação dinâmica consultada em 2026-11-05; compatibilidade exige fixar a versão efetivamente instalada.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

### V4C-S028 — How Klarna's AI assistant redefined customer support at scale

[https://www.langchain.com/blog/customers-klarna](https://www.langchain.com/blog/customers-klarna)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fornecedor relata assistência de Klarna com LangGraph, roteamento de tarefas, prompts adaptados e avaliações LangSmith.

Limite: Abertura confirmou relato do fornecedor e citação de executivo; detalhes do runtime não foram confirmados em publicação técnica do operador nesta busca. Registro conservador como recurso/caso documentado sem entrar na meta estrita de produção.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R009 — vLLM

**Nome canônico:** vLLM  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R009  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** vllm runtime

## R009:C01 — conceito

Projeto de inferência e serving de modelos, com gerenciamento KV, escalonamento e kernels especializados. É um runtime, não um modelo nem uma memória de agente. A documentação consultada lista batching contínuo, cache de prefixos, quantização e APIs de serving; suporte efetivo depende de arquitetura, versão e backend.

Como funciona:
- Carregar checkpoint e tokenizer com configuração de execução compatível.
- Administrar filas, estados e chamadas a kernels durante prefill e decode.
- Expor resultados, streaming e métricas ao cliente de aplicação.

## R009:C02 — aplicacao

Quando usar:
- Servir modelos abertos para múltiplas requisições com observabilidade.
- Comparar ajustes de throughput e latência sem reescrever o modelo.

Quando não usar:
- Presumir que um recurso listado funciona em toda combinação de quantização, arquitetura e GPU.

Implementação proposta:
- Fixar versão do runtime e revisão dos pesos numa configuração reproduzível.
- Validar chat template, parser de ferramentas e formato de saída antes de otimizar.
- Medir carga mista com limites de memória, tokens e requisições explícitos.

Aplicação LAI proposta:
Proposta LAI: usar como candidato de runtime configurável; este pacote não inspecionou nem alterou a instalação local do usuário.

## R009:C03 — riscos_validacao

Armadilhas:
- API compatível não significa semântica idêntica de todas as opções de outro provedor.
- Uma configuração que passa em chamada curta pode falhar sob contexto longo ou concorrência.

Métricas sugeridas:
- TTFT, ITL, goodput, erros e ocupação KV.
- Acerto de ferramentas e estabilidade em carga representativa.

Testes propostos:
- Reproduzir tarefas com e sem otimizações mantendo o checkpoint fixo e comparar correção e custo.
- Cancelar, reiniciar e sobrecarregar em ambiente de teste para verificar contratos operacionais.

## R009:C04 — perguntas_proveniencia

Pergunta: vLLM ensina o modelo a usar ferramentas?
Resposta: Não. Oferece serving e parsers; competência depende do checkpoint, template e avaliação.

Pergunta: As opções latest valem para minha versão instalada?
Resposta: Não necessariamente. A configuração deve ser conferida na documentação da versão real.

Pergunta: cache_salt resolve sozinho o isolamento entre clientes?
Resposta: Não. Ele participa da separação do cache; a própria documentação exige considerar outras superfícies compartilhadas.

Pergunta: Qual ganho medir primeiro?
Resposta: Separe prefill e decode; avalie TTFT sob carga antes de atribuir melhora global ao cache.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## R009:C05 — mecanismo_avancado

Em vLLM, o reúso de prefixos se apoia na identidade de blocos e de seus antecessores. Tokens iguais isoladamente não bastam quando adaptadores, conteúdo multimodal ou outros fatores alteram o cálculo. A documentação inclui identificadores adicionais e cache_salt na chave. A documentação de segurança também esclarece que compartilhar o processo servidor não oferece isolamento completo entre locatários. O gateway precisa definir o domínio de confiança antes de otimizar o cache.

Condição de contorno:
A presença de uma opção na documentação atual não comprova suporte no binário instalado; versão, arquitetura do checkpoint e configuração precisam ser registrados juntos.

Contrato proposto:
- Entradas: Revisão do modelo, tokenizer, adaptador, mensagens serializadas, identidade autorizada e política de cache por domínio.
- Saídas: Tokens gerados, motivo de término, uso reportado e métricas de prefill, decode, fila e reutilização.
- Estado: Mapa de blocos KV, referências ativas, filas de requisições e configuração efetiva do processo servidor.
- Invariante: Nenhuma solicitação deve selecionar diretamente o namespace de cache de outro domínio; identidades incompatíveis exigem separação ou miss.

Compromissos de projeto:
- Prefixos frequentes podem reduzir trabalho de prefill, mas dados mantidos ocupam memória que serviria à concorrência.
- Separar processos aumenta custo operacional; compartilhar requer avaliar explicitamente os limites reais de isolamento.

## R009:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: enviar prompts idênticos com adaptadores distintos e identidades separadas; verificar que não ocorre reúso incompatível e que um cancelamento libera recursos da requisição.

Plano de avaliação proposto:
Comparar cache desligado e ligado com distribuição fixa de comprimentos, concorrência e proporção de prefixos repetidos. Medir TTFT, latência entre tokens, throughput, memória e qualidade. Não extrapolar ganho de prefill para geração longa.

Comparações:
- T082 (complements): O servidor materializa cache de prefixos e outros mecanismos.
- T093 (complements): A gestão paginada de KV participa do uso eficiente de memória.

Afirmação rastreável:
A chave do cache de prefixos inclui contexto anterior e identidades adicionais; o processo compartilhado não é uma fronteira geral de isolamento.
Suporte: direct; fontes: V3D-S004, V3D-S005
Limite: Documentação atual consultada; nenhuma instalação ou configuração do usuário foi inspecionada.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R009:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 priorizou identidade do cache e isolamento. Esta camada transforma vLLM em uma opção de serviço a qualificar por workload, observabilidade e contrato do cliente, usando casos reais sem transferir suas configurações.

Escolha por workload
Prefill longo, decode longo e alta concorrência pressionam partes diferentes do runtime. Comece com uma configuração simples e meça fila, TTFT, intervalo entre tokens e respostas completas. Ativar todas as otimizações juntas impede identificar a causa de uma melhora ou regressão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

Recursos com maturidade distinta
A documentação atual inclui métricas experimentais de aceitação especulativa com restrições próprias. Trate disponibilidade e estabilidade por recurso e versão, não pelo nome vLLM. API de uso, motivo de término e métricas precisam ser validadas no cliente, inclusive em streaming e cancelamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

Casos que orientam hipóteses
LinkedIn descreve vLLM em Hiring Assistant e busca de vagas; Amazon relata Rufus com integração Neuron e execução multinó. Esses exemplos demonstram adoção em ambientes específicos. Não fixam hardware, versão, modelo ou melhor política para uma implantação 3–30B local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

USO AVANÇADO — Servidor especializado compartilhado
Cenário: Vários clientes usam modelos ou adapters relacionados.
Estratégia: Defina domínios de confiança, limites e identidade completa antes de otimizar prefixos. Teste batching e cache com carga representativa, monitorando justiça e cancelamento.
Papel do modelo pequeno: Um 8–14B pode atender tarefas de domínio com capacidade ajustada ao contexto real.
Aceite proposto: Qualidade-base preservada e prazos atendidos por cliente, sem mistura de estado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

USO AVANÇADO — Avaliar especulação
Cenário: Respostas longas apresentam padrões repetitivos.
Estratégia: Escolha proponente compatível, confira métricas por pedido quando disponíveis e compare com alvo sozinho. Registre CPU, memória e capacidade, além da aceitação.
Papel do modelo pequeno: Um 15–30B pode ser alvo; 3–7B também é possível se o custo adicional compensar.
Aceite proposto: Ganho líquido no serviço e correção do algoritmo sob configurações reais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S004, V3D-S005, V4B-S010, V4B-S008, V4B-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma réplica simples pode bastar; complexidade de orquestração deve responder a carga medida.
8–14B: Explore cache e batching antes de distribuir o modelo sem necessidade.
15–30B: Reserve KV e temporários, verificando topologia quando houver paralelismo.
Requisitos de treino/runtime: Runtime precisa suportar arquitetura, dtype, quantização e recursos escolhidos na versão fixada.
Não aplicar quando: Não presumir que endpoint semelhante a outra API oferece semântica idêntica ou isolamento completo entre locatários.

## R009:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 3. Lacuna: 7. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 3. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C008 — Amazon / Rufus
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Amazon relata lançamento de modelo maior para clientes Rufus e atendimento ao tráfego de Prime Day usando a solução multinó descrita.
Mecanismo documentado: Líder vLLM agenda lotes contínuos; Neuron executa cálculo distribuído, com TP/CP conforme fase e comunicação EFA/RDMA.
Correspondência com esta base: vLLM é parte explícita do runtime lançado.
Transferência proposta para modelo pequeno: Proposta: para 15–30B, dimensionar comunicação e memória antes de distribuir; para 3–14B, comparar uma réplica local bem utilizada antes de adotar multinó.
Limite: Hardware é Trainium, não GPU local. Pipeline parallelism não é explicitado e não é mapeado. Escala publicada não demonstra ganho equivalente para modelos menores.
Fontes: V4B-S008.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: vLLM é identificado como runtime do serviço.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

V4B-C005 — LinkedIn (Microsoft) / AI-Powered Job Search
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O pipeline de ranking usa professores especializados e um aluno compacto; o serviço de entendimento de consultas do mesmo produto é descrito com vLLM e batching.
Mecanismo documentado: Sinais de relevância, engajamento e representações alimentam treinamento do aluno; cache de sinais reduz trabalho repetido entre experimentos.
Correspondência com esta base: vLLM serve o componente de interpretação de consultas.
Transferência proposta para modelo pequeno: Proposta: treinar um aluno 3–14B para uma tarefa bem delimitada, versionando sinais e avaliando dados futuros; o caso mostra especialização, não necessidade de copiar sua escala.
Limite: O aluno de ranking citado é 0,6B, fora da faixa solicitada. Ranking e query understanding são componentes diferentes do produto; não se afirma que o aluno de ranking é o modelo servido pelo vLLM descrito.
Fontes: V4B-S005, V4B-S010.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: O scorer offline implementado utiliza servidores vLLM.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4B-C023 — Snowflake / Suffix Decoding
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: pesquisa sobre LLM.
Uso observado: A publicação apresenta método e avaliações de geração especulativa a partir de sufixos. O registro não transforma resultados experimentais em comprovação de implantação operacional.
Mecanismo documentado: Estruturas de sufixos usam histórico de tokens para propor continuações que precisam ser verificadas pelo alvo.
Correspondência com esta base: Integração com runtime não comprova toda configuração de vLLM.
Transferência proposta para modelo pequeno: Proposta: avaliar em saídas com forte repetição, incluindo custo de atualizar e consultar o índice em CPU.
Limite: Sem caso específico de bigtech implantada confirmado nesta fonte; ganho depende de repetição, alvo, concorrência e custo do proponente.
Fontes: B-S040.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q018.

## R009:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R009 → T082 [complements]
Como combinar: O Hiring Assistant usa prefix caching no serving descrito pelo LinkedIn.
Interface: Prefixo compatível e configuração de serviço.
Condição: Escopo do caso documentado.
Aceite proposto: Medir tokens realmente reutilizados e latência.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

2. R009 → T088 [complements]
Como combinar: O mesmo caso descreve continuous batching junto ao serving vLLM.
Interface: Sequências ativas e política de lote.
Condição: Configuração e modelo compatíveis.
Aceite proposto: Avaliar carga aberta e prazos por requisição.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S010. Casos: V4B-C001.

CONTROLES DE FALHA
- Fixar versões de modelo, tokenizer, runtime e parâmetros no manifest.
- Não promover resposta truncada a sucesso só porque o HTTP terminou normalmente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
vLLM é infraestrutura, não fonte de capacidade cognitiva. Compare o serviço completo de um modelo pequeno com fronteira em qualidade, custo e prazo sob condições explícitas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T088, T093, T094, T102

## Fontes primárias associadas

### B-S044 — vLLM — Welcome

[https://docs.vllm.ai/en/latest/](https://docs.vllm.ai/en/latest/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de inferência e serving com API, batching, gerenciamento KV e kernels especializados.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S004 — Automatic Prefix Caching — vLLM design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos, hash do prefixo anterior, tokens e fatores adicionais como adaptador, multimodalidade e cache_salt.

Limite: Documentação latest; não comprova configuração instalada nem ganho local.

### V3D-S005 — Security — vLLM

[https://github.com/vllm-project/vllm/blob/main/docs/usage/security.md](https://github.com/vllm-project/vllm/blob/main/docs/usage/security.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites de isolamento em processos compartilhados e papel limitado de cache_salt.

Limite: Arquivo main consultado; namespace de cache não constitui isolamento geral entre locatários.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

### B-S040 — SuffixDecoding at Production Scale with Arctic Inference and vLLM

[https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/](https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvores de sufixos sobre tokens anteriores produzem candidatos especulativos sem modelo auxiliar.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S005 — The training infrastructure behind AI-Powered Job Search: 8X faster multi-teacher distillation

[https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation](https://www.linkedin.com/blog/engineering/infrastructure/the-training-infrastructure-behind-ai-powered-job-search-eight-x-faster-multi-teacher-distillation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline real de ranking com múltiplos professores e aluno 0,6B; cache e streaming de sinais de treino.

Limite: Aluno publicado está abaixo de 3B; transferência à faixa solicitada é proposta, não reprodução da implantação.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R010 — Hugging Face TGI

**Nome canônico:** Hugging Face TGI  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R010  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Text Generation Inference; TGI

## R010:C01 — conceito

Text Generation Inference é um toolkit de serving de LLMs com recursos como streaming, batching e observabilidade. Na consulta de 2026-11-05, a documentação oficial informa maintenance mode e orienta novos desenvolvimentos para outros engines. Isso é um estado datado do projeto, não prova de falha de uma implantação existente.

Como funciona:
- Disponibilizar um modelo suportado por um serviço de geração.
- Administrar execução e devolver tokens ou resposta completa pela API.
- Expor métricas e controles conforme a versão e o backend adotados.

Nota de nomenclatura: Estado do projeto verificado em documentação oficial em 2026-11-05; revisar antes de decisão futura.

## R010:C02 — aplicacao

Quando usar:
- Manter uma implantação existente que já esteja validada e tenha suporte adequado ao caso.
- Comparar contratos ao planejar migração de um serving legado.

Quando não usar:
- Selecionar TGI para projeto novo presumindo evolução ativa sem considerar o aviso oficial atual.

Implementação proposta:
- Inventariar versão, modelo, backend e recursos realmente utilizados.
- Criar testes de contrato para prompts, streaming, ferramentas e cancelamento antes da migração.
- Comparar um runtime alternativo com as mesmas tarefas e guardar um caminho de rollback.

Aplicação LAI proposta:
Proposta LAI: manter TGI como referência histórica e opção de compatibilidade; para nova implantação, reavaliar alternativas mantidas com evidências atuais.

## R010:C03 — riscos_validacao

Armadilhas:
- Migração por API semelhante pode mudar templates, razões de parada e comportamento de streaming.
- Aviso de manutenção não estabelece automaticamente prazo de suporte ou inexistência de correções.

Métricas sugeridas:
- Compatibilidade de respostas e eventos do cliente.
- Latência, erros, memória e custo operacional antes/depois da migração.

Testes propostos:
- Reexecutar casos de integração existentes nos dois runtimes e registrar diferenças materiais.
- Verificar que timeout e cancelamento liberam recursos no substituto antes de mover tráfego.

## R010:C04 — perguntas_proveniencia

Pergunta: TGI foi verificado como descontinuado definitivamente?
Resposta: Não. A evidência consultada diz maintenance mode; esse é o estado exato registrado.

Pergunta: Preciso migrar imediatamente se já uso?
Resposta: Não se conclui isso sem avaliar suporte, riscos e custo da instalação concreta.

Pergunta: Manutenção significa que o serviço parou?
Resposta: Não. É uma mudança no escopo de evolução do projeto; operação depende da instalação.

Pergunta: Basta trocar a URL por outro servidor?
Resposta: Não. Compare template, streaming, erros, término e qualidade nas tarefas reais antes da troca.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## R010:C05 — mecanismo_avancado

A documentação oficial de TGI consultada em 2026-11-05 informa manutenção limitada a correções menores, documentação e tarefas leves. Isso altera a decisão de adoção, mas não invalida automaticamente uma instalação existente. Uma migração deve comparar a semântica do endpoint: serialização de chat, tokens especiais, campos de uso, término, streaming, limites e erros. Compatibilidade aparente da rota HTTP não garante comportamento equivalente em casos extremos.

Condição de contorno:
O status do projeto não informa sozinho se um modelo específico funciona na versão local; suporte de kernels e variantes de hardware precisa ser verificado no ambiente alvo.

Contrato proposto:
- Entradas: Imagem ou versão fixada, checkpoint, tokenizer, configuração de batching e conjunto representativo de chamadas do aplicativo.
- Saídas: Respostas completas e em fluxo, erros classificados, métricas de serviço e relatório de diferenças entre servidores.
- Estado: Configuração de implantação, filas, shards e registro de versões usado durante toda a comparação.
- Invariante: Uma substituição de servidor só é considerada compatível quando preserva os contratos que o consumidor efetivamente utiliza.

Compromissos de projeto:
- Manter uma implantação estável evita migração imediata, mas exige acompanhar suporte e necessidades futuras.
- Migrar pode ampliar opções de execução, porém templates e parâmetros diferentes podem mudar a resposta mesmo com pesos iguais.

## R010:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: interromper um stream, testar sequência de parada, entrada longa e parâmetro inválido em ambos os servidores; registrar diferenças de término e liberação de recursos.

Plano de avaliação proposto:
Executar comparação controlada com o mesmo conjunto de tarefas, hardware e orçamento. Medir erros, latência p50/p95, custo por resposta aceita e equivalência funcional. Definir rollback antes de qualquer mudança real de tráfego.

Comparações:
- R009 (alternative): Outro servidor pode atender ao mesmo contrato após validação.
- P009 (complements): O componente proposto deve encapsular diferenças de provedor.

Afirmação rastreável:
TGI encontra-se em modo de manutenção segundo a documentação oficial consultada em 2026-11-05.
Suporte: direct; fontes: V3D-S006
Limite: Estado documental datado; não representa desativação imediata de instalações existentes.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R010:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 registrou maintenance mode e equivalência de endpoints. A nova camada organiza a decisão entre manter e migrar, com inventário de dependências e experimentos de transição que preservam a interpretação dos resultados.

Manutenção datada
A documentação consultada em 05/11/2026 informa manutenção limitada do TGI. Isso pesa em novos desenvolvimentos e compatibilidade futura, mas não demonstra que um serviço existente está defeituoso. Liste necessidades reais, como novos modelos e recursos, antes de definir migração apenas pelo estado do projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010.

Dependências do consumidor
Inventarie templates, parâmetros, erros, streaming, métricas, limites e comportamento de cancelamento usados pela aplicação. Uma troca de engine pode alterar defaults e tokenização sem mudar a rota HTTP. Compare requisições serializadas e estados terminais, não somente textos de exemplos felizes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010.

Migração observável
Faça replay autorizado em ambiente de teste e compare semântica antes de desempenho. Depois, teste carga com as mesmas chegadas e contextos. Mantenha rollback e evidências da versão antiga. A adoção histórica no HuggingChat em 2023 não deve ser descrita como confirmação da configuração atual do produto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010.

USO AVANÇADO — Serviço TGI existente
Cenário: A aplicação funciona, mas precisa de recurso novo.
Estratégia: Avalie se a versão atual atende o contrato e se o novo requisito justifica mudança. Crie testes de compatibilidade e compare candidatos, sem pressupor vencedor.
Papel do modelo pequeno: Um 8–14B pode continuar útil no serviço existente enquanto a migração é qualificada.
Aceite proposto: Nenhuma regressão de formato, término, erro ou qualidade no caminho consumido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010.

USO AVANÇADO — Novo serviço pequeno
Cenário: Não há dependência histórica de TGI.
Estratégia: Compare engines com suporte atual ao checkpoint, incluindo Transformers continuous batching e outros runtimes. Use um caso mínimo representativo e meça operação completa.
Papel do modelo pequeno: Um 3–7B permite iniciar simples; o runtime escolhido deve corresponder ao workload.
Aceite proposto: Escolher pela compatibilidade e manutenção requeridas, sem copiar benchmarks de outra pilha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Evite montar complexidade de shards se uma réplica atende o objetivo.
8–14B: Serviços existentes merecem análise de custo de migração e contrato, não descarte automático.
15–30B: Modelos 15–30B exigem qualificar paralelismo, quantização e memória no engine escolhido.
Requisitos de treino/runtime: TGI é runtime de serving; versão, container e suporte do checkpoint precisam ser fixados.
Não aplicar quando: Não afirmar que maintenance mode interrompe automaticamente produção nem que HuggingChat continua usando a mesma pilha de 2023.

## R010:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C010 — Hugging Face / HuggingChat — relato de 2023
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: O operador informou em 2023 que TGI alimentava HuggingChat e integrava seus serviços de inferência.
Mecanismo documentado: Servidor dedicado de geração com streaming e otimizações disponíveis na pilha; o relato identifica o runtime efetivamente usado.
Correspondência com esta base: A fonte do operador afirma TGI como backend de HuggingChat naquele período.
Transferência proposta para modelo pequeno: Proposta: usar o caso como referência de migração e compatibilidade; novos serviços 3–30B devem considerar estado atual de manutenção e testar alternativas.
Limite: Não demonstra stack atual do HuggingChat. O maintenance mode documentado em 2026 é preservado, e disponibilidade histórica não é recomendação automática de nova adoção.
Fontes: V4B-S019, V3D-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q015.

## R010:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R010 → R009 [alternative]
Como combinar: vLLM pode ser candidato de migração quando atende o contrato e o modelo.
Interface: Requisições, eventos e métricas equivalentes.
Condição: Suporte verificado no ambiente.
Aceite proposto: Comparar casos de erro e carga, além de geração normal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R010 → R023 [alternative]
Como combinar: Transformers documenta recursos atuais de batching contínuo que devem ser avaliados conforme o uso.
Interface: Configuração de geração e scheduling.
Condição: API e arquitetura compatíveis na versão fixada.
Aceite proposto: Verificar operação e manutenção antes de adotar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S006, V4B-S019, V4B-S014, V4B-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não levar defaults de um engine para outro sem inspeção.
- Separar evidência histórica de implantação de disponibilidade atual de recursos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A escolha do servidor modifica custo e operação. Para comparar com fronteira, mantenha o modelo e o contrato claros; uma migração de TGI não melhora automaticamente a qualidade das respostas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R009, R011, T088, T141

## Fontes primárias associadas

### B-S042 — Text Generation Inference

[https://huggingface.co/docs/text-generation-inference/en/index](https://huggingface.co/docs/text-generation-inference/en/index)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Toolkit de serving; aviso de maintenance mode observado em 2026-11-05.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S006 — Text Generation Inference — maintenance status

[https://huggingface.co/docs/text-generation-inference/en/index](https://huggingface.co/docs/text-generation-inference/en/index)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estado de manutenção do TGI com correções menores, documentação e tarefas leves.

Limite: Estado documental verificado em 2026-11-05; não demonstra interrupção de serviço existente.

### V4B-S019 — Open-Source Text Generation & LLM Ecosystem at Hugging Face

[https://huggingface.co/blog/os-llms](https://huggingface.co/blog/os-llms)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Relato histórico do operador de TGI servindo HuggingChat e integração nos serviços de inferência.

Limite: Fonte histórica; não prova stack atual do HuggingChat nem cancela estado atual de manutenção do TGI.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R011 — NVIDIA TensorRT-LLM

**Nome canônico:** NVIDIA TensorRT-LLM  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R011  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** TensorRT LLM; TRT-LLM

## R011:C01 — conceito

Biblioteca e runtime da NVIDIA para inferência de modelos, com APIs e otimizações para GPUs compatíveis. A página oficial consultada em 2026-11-05 descreve arquitetura PyTorch nativa. Portanto, não se deve pressupor que toda versão atual exige o antigo fluxo de compilação de engines TensorRT.

Como funciona:
- Carregar um modelo por um caminho suportado na versão escolhida.
- Executar kernels, gerenciamento KV e escalonamento adequados ao hardware.
- Atender chamadas locais ou por serviço, com opções de paralelismo e geração.

Nota de nomenclatura: Evitar aplicar descrição de versões antigas à documentação atual; snapshot factual consultado em 2026-11-05.

## R011:C02 — aplicacao

Quando usar:
- Implantação em hardware NVIDIA com necessidade concreta de otimização e modelos suportados.
- Comparação de runtime com perfil de carga bem definido.

Quando não usar:
- Escolher pelo nome ou por benchmark de outra GPU sem validar modelo, kernel e versão.

Implementação proposta:
- Consultar matriz de hardware e modelos da versão fixada.
- Adaptar integração à API e ao fluxo atual, evitando tutoriais de backend removido.
- Comparar com runtime de referência usando o mesmo checkpoint, precisão e metas de latência.

Aplicação LAI proposta:
Proposta LAI: avaliar somente após confirmar suporte ao checkpoint e hardware reais; o nome TensorRT-LLM não comprova compatibilidade com qualquer quantização Qwen.

## R011:C03 — riscos_validacao

Armadilhas:
- Recursos disponíveis para uma arquitetura de GPU não são automaticamente disponíveis para toda a linha.
- Resultados de alto throughput podem depender de batch, precisão e paralelismo diferentes do uso interativo.

Métricas sugeridas:
- Goodput com prazo fixo, latência de cauda e memória.
- Correção de tool calling, saída estruturada e estabilidade do serviço.

Testes propostos:
- Executar uma matriz pequena de comprimento e concorrência com igualdade de condições.
- Verificar caminhos não suportados e guardar logs que comprovem o backend real em uso.

## R011:C04 — perguntas_proveniencia

Pergunta: TensorRT-LLM sempre exige construir engine previamente?
Resposta: Não como afirmação universal. A documentação atual consultada descreve arquitetura PyTorch nativa; versões e caminhos devem ser identificados.

Pergunta: É concorrente de Qwen?
Resposta: Não. Qwen é família de modelos; TensorRT-LLM é infraestrutura para executar modelos compatíveis.

Pergunta: Ainda devo executar um tutorial antigo de build de engine?
Resposta: Primeiro identifique a versão; o caminho legado descrito pode ter sido removido.

Pergunta: O nome TensorRT-LLM basta para prever velocidade?
Resposta: Não. Hardware, checkpoint, kernels, quantização, comprimento e concorrência determinam o caso medido.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## R011:C05 — mecanismo_avancado

A página atual de arquitetura do TensorRT-LLM apresenta PyTorch como único backend de execução e informa a remoção do antigo backend de engines TensorRT. Guias antigos de conversão e build não devem ser aplicados automaticamente à edição atual. A arquitetura descrita separa execução do modelo, decodificação, agendamento e gerenciamento de recursos. A integração deve registrar versão exata, hardware e caminho de carregamento, evitando tratar o nome do produto como uma arquitetura imutável.

Condição de contorno:
Documentação em latest pode divergir de uma versão instalada anteriormente; migração exige consultar o guia correspondente e testar o checkpoint específico.

Contrato proposto:
- Entradas: Checkpoint, configuração do modelo, precisão, paralelismo, limites de contexto e versão fixada do toolkit.
- Saídas: Sequência gerada, motivo de parada, uso de memória e métricas separadas por fila, prefill e decode.
- Estado: Recursos de KV, requisições ativas, microbatches e configuração dos executores e decodificadores.
- Invariante: A configuração carregada deve coincidir com o manifesto avaliado; mudança de backend ou precisão invalida a equivalência presumida.

Compromissos de projeto:
- Integrações especializadas podem ampliar eficiência, mas aumentam a dependência entre hardware, kernels e versões.
- Aumentar lotes melhora amortização de trabalho, porém pode elevar espera e memória para atender caudas longas.

## R011:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: carregar deliberadamente configuração de um guia antigo e confirmar diagnóstico claro; cancelar solicitações durante geração e verificar liberação de recursos sem corromper vizinhas.

Plano de avaliação proposto:
Comparar configurações somente após garantir paridade funcional. Fixar distribuição de prompts, comprimentos de saída e carga; medir throughput sob SLO de latência, memória máxima e precisão na tarefa. Nenhum resultado GPU está incluído como medição deste pacote.

Comparações:
- R009 (alternative): São opções de serving a comparar no hardware alvo.
- T121 (complements): O scheduler materializa decisões de ocupação e prioridade.

Afirmação rastreável:
A documentação latest consultada informa PyTorch como único backend e remoção do backend legado de engines TensorRT.
Suporte: direct; fontes: V3D-S007
Limite: A afirmação refere-se à documentação atual, não a todas as versões históricas.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R011:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 corrigiu a suposição de backend legado obrigatório. A nova camada estrutura a qualificação por recurso, precisão e arquitetura, separando disponibilidade anunciada de benefício medido.

Arquitetura atual e versão
A documentação consultada apresenta execução PyTorch nativa. Guias de engines legados podem ser relevantes apenas para versões históricas específicas. Registre versão e caminho usado, evitando combinar instruções de épocas diferentes numa receita que parece válida mas não corresponde ao produto instalado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S007, V4B-S011, B-S034.

Matriz de capacidades
Quantização, speculative decoding, batching e paralelismo possuem requisitos próprios. Verifique a combinação concreta, pois suporte isolado a dois recursos não prova sua composição. Comece pelo checkpoint em caminho simples e acrescente uma otimização por vez, preservando testes de qualidade e conclusão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S007, V4B-S011, B-S034.

Hardware e custo
Kernels e precisões especializadas dependem de geração de hardware e configuração. Uma página de produto não confirma compatibilidade da GPU local nem ganho de uma determinada quantização. Inclua tempo de inicialização, memória, aquecimento e operação sob carga na decisão, sem transportar números promocionais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S007, V4B-S011, B-S034.

USO AVANÇADO — Qualificar modelo especializado
Cenário: Um 15–30B precisa servir respostas com prazo definido.
Estratégia: Fixe checkpoint, precisão e paralelismo, valide carregamento e resultados, depois teste otimizações elegíveis. Meça prefill e decode separadamente para orientar escolhas.
Papel do modelo pequeno: O modelo mantém competência própria; o runtime procura executá-lo eficientemente.
Aceite proposto: Atender prazo e orçamento sem regressão de qualidade ou falhas de término.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S007, V4B-S011, B-S034.

USO AVANÇADO — Explorar baixa precisão
Cenário: Há suporte potencial a FP8 ou quatro bits.
Estratégia: Compare artefatos compatíveis, verifique kernels selecionados e identifique componentes que permanecem em precisão maior. Avalie erro por domínio antes de aumentar concorrência.
Papel do modelo pequeno: Um 8–14B pode liberar memória para sessões se a quantização funcionar no ambiente.
Aceite proposto: Economia física e ganho de serviço medidos com configuração completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S007, V4B-S011, B-S034.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma pilha especializada pode não ser necessária para um 3–7B de baixa carga.
8–14B: Explore recursos somente quando o perfil identifica um gargalo relevante.
15–30B: Modelos maiores exigem contabilizar KV, buffers e comunicação, além dos pesos.
Requisitos de treino/runtime: Runtime NVIDIA e hardware suportado na versão concreta; treinamento adicional depende do recurso, como módulos auxiliares treinados.
Não aplicar quando: Não assumir antigo fluxo de build obrigatório nem compatibilidade universal por ser uma GPU NVIDIA.

## R011:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C011 — NVIDIA / TensorRT-LLM
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.
Mecanismo documentado: Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.
Correspondência com esta base: Produto e arquitetura do runtime são descritos diretamente.
Transferência proposta para modelo pequeno: Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.
Limite: É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.
Fontes: V4B-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de produto e eventual adoção consultada. O caso registrado é recurso operacional documentado; não foi confirmado um cliente específico de produção para cada otimização neste recorte.
Consultas registradas: V4B-Q025.

## R011:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R011 → T123 [complements]
Como combinar: FP8 é um recurso documentado, sujeito a formato e suporte do caminho.
Interface: Pesos, escalas e precisão de acumulação.
Condição: Combinação disponível na versão e hardware escolhidos.
Aceite proposto: Comparar qualidade e perfil com referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S007, V4B-S011, B-S034. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R011 → T128 [complements]
Como combinar: EAGLE é uma opção documentada que exige módulo compatível com o alvo.
Interface: Par alvo/proponente e configuração de verificação.
Condição: Artefatos e recurso suportados conjuntamente.
Aceite proposto: Medir aceitação e ganho líquido, sem confundir as métricas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S007, V4B-S011, B-S034. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar misturar documentação latest com configuração de uma versão antiga.
- Registrar fallback e precisão efetivamente usada, não apenas a solicitada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
TensorRT-LLM pode melhorar operação de um modelo especializado. A comparação com fronteira deve medir a aplicação completa, sem atribuir capacidade cognitiva ao runtime ou à marca do hardware.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R009, R010, T088, T102, T118, T123

## Fontes primárias associadas

### B-S043 — TensorRT LLM — Overview

[https://nvidia.github.io/TensorRT-LLM/overview.html](https://nvidia.github.io/TensorRT-LLM/overview.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime atual descrito como PyTorch nativo, com API de inferência e recursos distribuídos; não pressupõe fluxo legado de engines.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S007 — TensorRT-LLM — Architecture Overview

[https://nvidia.github.io/TensorRT-LLM/latest/torch/arch_overview.html](https://nvidia.github.io/TensorRT-LLM/latest/torch/arch_overview.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: PyTorch como único backend atual, remoção do caminho legado e organização dos componentes de execução.

Limite: Página latest; versões históricas podem manter outra arquitetura. Não houve benchmark GPU.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

### B-S034 — Using FP8 and FP4 with Transformer Engine

[https://nvidia.github.io/TransformerEngine/examples/fp8_primer.html](https://nvidia.github.io/TransformerEngine/examples/fp8_primer.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações FP8 E4M3/E5M2 e escalas para controlar faixa dinâmica.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R012 — Tinker — Prompt Distillation

**Nome canônico:** Tinker Prompt Distillation  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R012  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Tinker prompt-distillation recipe; Tinker Prompt Distillation

## R012:C01 — conceito

Receita do Tinker Cookbook para gerar exemplos com um professor condicionado por instruções e treinar um aluno para a tarefa com prompt reduzido. A documentação consultada demonstra classificação de linguagem. É uma referência de implementação de treinamento, não uma memória externa nem garantia de suporte a todo checkpoint local.

Como funciona:
- Gerar dataset de exemplos usando o professor e o prompt da tarefa.
- Aplicar treinamento do aluno com os exemplos selecionados.
- Amostrar e avaliar o checkpoint para conferir retenção do comportamento.

## R012:C02 — aplicacao

Quando usar:
- Experimentação de destilação de um prompt estável.
- Equipe dispõe de dados representativos e acesso à infraestrutura de treinamento necessária.

Quando não usar:
- Presumir que uma receita demonstra resultados em português, ferramentas ou modelos não avaliados.

Implementação proposta:
- Conferir requisitos atuais e compatibilidade do modelo antes de iniciar.
- Substituir exemplos demonstrativos por dataset com curadoria e divisão correta.
- Registrar prompt, dados, configuração e checkpoint em cada experimento.

Aplicação LAI proposta:
Proposta: usar a receita como referência para experimento controlado da Helena; priorizar medição antes de ampliar treino ou inferir economia.

## R012:C03 — riscos_validacao

Armadilhas:
- Executar receita de classificação não comprova transferência a agentes completos.
- Custos e modelos disponíveis podem mudar; esta base não fixa preço nem disponibilidade.

Métricas sugeridas:
- Qualidade em teste reservado com prompt reduzido.
- Tokens economizados e custo total do experimento.

Testes propostos:
- Comparar aluno base, aluno treinado e professor com prompt completo.
- Testar exceções e linguagem não vistas na geração dos dados.

## R012:C04 — perguntas_proveniencia

Pergunta: O pacote RAG executou esse treinamento?
Resposta: Não. Ele documenta a técnica e os critérios de avaliação.

Pergunta: A receita serve como banco de fatos atualizados?
Resposta: Não. É um fluxo de aprendizagem paramétrica de comportamento.

Pergunta: Distilar este inventário substitui RAG com fontes?
Resposta: Não automaticamente. Treinar comportamento e recuperar evidência verificável resolvem necessidades diferentes.

Pergunta: Quando o investimento compensa?
Resposta: Quando a economia por chamada e a qualidade sustentada superam custo de dados, treino, atualização e avaliação.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## R012:C05 — mecanismo_avancado

A receita de prompt distillation do Tinker descreve um professor que recebe instrução p e consulta q, produzindo resposta r. O estudante aprende a prever r a partir de q sem receber p. O efeito desejado é incorporar comportamento recorrente nos parâmetros. Para preparar uma experiência útil, a curadoria precisa separar exemplos de treino e avaliação por famílias de entrada; repetir as mesmas perguntas com pequenas alterações pode criar uma impressão enganosa de generalização.

Condição de contorno:
Um comportamento treinado pode envelhecer quando a política muda. Dados factuais voláteis e evidências que precisam de citação continuam exigindo mecanismos de atualização e recuperação.

Contrato proposto:
- Entradas: Prompt professor versionado, consultas representativas, respostas verificadas, checkpoint estudante e orçamento de treino.
- Saídas: Checkpoint ou adaptador, manifesto dos dados e relatório de tarefas com e sem a instrução original.
- Estado: Proveniência de exemplos, partições imutáveis, hiperparâmetros e associação entre versão do prompt e pesos.
- Invariante: A avaliação reservada não participa da seleção de exemplos, ajuste do prompt professor ou escolha de checkpoint.

Compromissos de projeto:
- Remover instruções repetidas pode reduzir tokens de entrada, mas transfere custo para coleta, treino e validação.
- Um estudante pode reproduzir regularidades e também erros do professor; aceitação depende de avaliação independente.

## R012:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: alterar uma regra após o treinamento e confrontar casos antigos e novos; verificar se a versão do comportamento fica identificável e se o fallback preserva a política vigente.

Plano de avaliação proposto:
Comparar modelo base com prompt, base sem prompt e estudante sem prompt em partição reservada. Medir acerto, violações de regra, tokens e custo total amortizado. Definir o volume de chamadas necessário para compensar o treinamento.

Comparações:
- T180 (specializes): A receita é uma implementação do objetivo de destilar instruções.
- T069 (distinct_from): Um resumo externo não altera os parâmetros do estudante.

Afirmação rastreável:
A receita treina o estudante sem o prompt usado pelo professor para produzir os exemplos.
Suporte: direct; fontes: V3D-S008
Limite: O tutorial demonstra um procedimento; não garante desempenho em novos domínios ou checkpoints.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R012:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu a receita professor com prompt e aluno sem prompt. A nova camada define critérios para escolher a receita, acompanhar disponibilidade dos modelos e comparar transferência on-policy e dados estáticos.

Receita como ponto de partida
O exemplo do cookbook demonstra uma tarefa, não uma configuração universal. Antes de adaptar, declare quais instruções são estáveis e quais entradas continuam variáveis. Preserve um prompt mínimo quando necessário para selecionar comportamento; retirar tudo pode tornar casos diferentes indistinguíveis para o aluno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

Disponibilidade temporal
Modelos e exemplos do serviço mudam. A documentação atual de distillation usa opções diferentes de exemplos históricos que foram retirados. Registre identificadores disponíveis no momento do experimento e não prometa treinamento de um checkpoint local arbitrário só porque o nome da família aparece numa receita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

Sinal na distribuição do aluno
As receitas e o estudo de on-policy distillation motivam avaliar o professor nos estados gerados pelo aluno. Compare com dados estáticos do professor e rótulos corretos quando disponíveis. Isso muda custo e cobertura; um sinal de imitação continua sujeito a erros do professor e limitações de capacidade do estudante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

USO AVANÇADO — Destilar classificação de domínio
Cenário: Um prompt extenso define categorias estáveis.
Estratégia: Gere consultas representativas, obtenha respostas verificadas e ajuste o aluno com entradas reduzidas. Teste fronteiras entre classes e exemplos fora do padrão.
Papel do modelo pequeno: Um 3–7B ou outro porte efetivamente suportado pode executar classificação estreita.
Aceite proposto: Acurácia por classe e custo completo após retirar instruções, em dados inéditos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

USO AVANÇADO — Melhorar trajetórias do aluno
Cenário: O aluno falha em estados que o professor raramente visita.
Estratégia: Colete estados em ambiente controlado e obtenha supervisão apropriada. Compare políticas sem contaminar avaliação e mantenha filtros de qualidade.
Papel do modelo pequeno: Um 8–14B pode ser estudado se disponível e adequado; faixa não implica suporte atual de todo modelo.
Aceite proposto: Sucesso de tarefa e estabilidade após a transferência, além da loss de treino.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S008, V4B-S012, V4B-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize comportamento delimitado e verificador confiável; suporte do serviço é requisito separado.
8–14B: Receitas atuais precisam ser lidas com identificadores e APIs da versão utilizada.
15–30B: Compare custo de destilar 15–30B com adaptar diretamente um checkpoint disponível, sem presumir oferta do serviço.
Requisitos de treino/runtime: É referência de treinamento; requer dados, estudante suportado e avaliação. Não é cache nem memória externa.
Não aplicar quando: Não afirmar que recipe reproduzida em documentação foi executada neste pacote ou que transfere toda capacidade do professor.

## R012:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C012 — Thinking Machines Lab / Tinker Cookbook — destilação
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: pesquisa sobre LLM.
Uso observado: A equipe publica receitas reproduzíveis e experiências de transferência de comportamento, incluindo aluno em suas próprias trajetórias e redução do contexto de instruções.
Mecanismo documentado: LoRA e perdas de destilação treinam o aluno; prompt distillation condiciona o professor com informação ausente da entrada reduzida do aluno.
Correspondência com esta base: É a referência Tinker para prompt distillation.
Transferência proposta para modelo pequeno: Proposta: começar com uma tarefa 3–14B e teste temporal independente, mantendo acesso a exemplos do professor e custos de geração/treino separados.
Limite: Receita/benchmark não prova deployment do aluno. Modelos históricos do artigo foram substituídos na oferta; não se assume disponibilidade nem suporte do checkpoint local.
Fontes: V4B-S012, V4B-S013, V3D-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q009.

## R012:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R012 → T180 [feeds]
Como combinar: A receita concretiza transferência de instruções estáveis para comportamento do aluno.
Interface: Prompt professor, consultas e respostas revisadas.
Condição: Parâmetros variáveis preservados na entrada.
Aceite proposto: Testar com e sem instrução original em famílias novas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R012 → T178 [complements]
Como combinar: On-policy e off-policy são escolhas de distribuição do sinal de destilação.
Interface: Trajetórias, logits ou textos disponíveis.
Condição: Objetivo e acesso ao professor explícitos.
Aceite proposto: Comparar cobertura e qualidade sob orçamento total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S008, V4B-S012, V4B-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Versionar professor, estudante, receita e dados; não copiar nomes de exemplos retirados.
- Manter casos reservados fora da geração e seleção de exemplos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a rotina aprendida com professor e fronteira na mesma tarefa. Tinker oferece meios para experimentar transferência; a receita não estabelece paridade geral nem economia garantida.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T179, T180, T182

## Fontes primárias associadas

### C-S034 — Prompt Distillation — Tinker Documentation

[https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/prompt-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Receita gera dados com professor e treina aluno para tarefa de classificação com prompt reduzido.

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

### V4B-S013 — On-Policy Distillation

[https://thinkingmachines.ai/blog/on-policy-distillation/](https://thinkingmachines.ai/blog/on-policy-distillation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Supervisão em trajetórias do aluno, KL reversa, experiências de raciocínio e assistente interno; atualização datada de modelos retirados.

Limite: Casos experimentais; números e modelos do artigo não descrevem hardware nem checkpoint do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R013 — Letta MemFS

**Nome canônico:** Letta MemFS — memória versionada em arquivos  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** MemFS; Letta / Letta MemFS

## R013:C01 — conceito

MemFS projeta a memória de longo prazo de um agente Letta em um checkout Git, manipulável com ferramentas comuns de arquivos. A documentação também o chama de context repository. O mecanismo combina persistência, organização hierárquica e carregamento seletivo; não transforma todos os arquivos em contexto simultaneamente nem valida a veracidade das memórias.

Como funciona:
- Arquivos de memória possuem caminhos e descrições; índices MEMORY.md ajudam o agente a localizar conteúdo aprofundado.
- Na documentação atual, arquivos na raiz permanecem no prompt; diretórios indexados são consultados sob demanda.
- Edições locais precisam ser confirmadas e sincronizadas para compor a memória compartilhada em outros computadores.

Nota de nomenclatura: O nome combinado da edição anterior é preservado como alias histórico. Não houve instalação nem teste de sincronização real.

## R013:C02 — aplicacao

Quando usar:
- Procedimentos, decisões e preferências textuais que precisam de histórico e inspeção.
- Conhecimento de projeto maior que o orçamento disponível no prompt.

Quando não usar:
- Eventos concorrentes de alto volume que exigem transações ou grandes arquivos sem valor contextual.

Implementação proposta:
- Proposta: definir poucos arquivos essenciais, diretórios por assunto e índices que descrevam quando consultar cada conteúdo.
- Registrar fonte, data e responsável por memória importante; separar fatos comprovados de hipóteses e instruções.
- Estabelecer fluxo de revisão, commit, sincronização e resolução de conflitos antes de permitir escritores concorrentes.

Aplicação LAI proposta:
Proposta LAI: experimentar MemFS para manuais e decisões de engenharia, mantendo eventos operacionais volumosos no armazenamento definido para sua carga.

## R013:C03 — riscos_validacao

Armadilhas:
- Commit local e sincronização remota são etapas distintas; não declarar propagação antes de confirmá-la.
- O blog original descreve system/; a documentação atual reserva essa organização a agentes antigos.

Métricas sugeridas:
- Tokens fixos de memória, recuperação por consulta, conflitos de edição e atraso de sincronização.

Testes propostos:
- Proposta: editar sem push, abrir outra sessão e conferir a diferença entre estado local e compartilhado.
- Alterar o mesmo fato em dois escritores e verificar preservação da proveniência e resolução explícita da divergência.

## R013:C04 — perguntas_proveniencia

Pergunta: MemFS exige carregar todo o repositório no prompt?
Resposta: Não. Sua hierarquia distingue conteúdo sempre carregado de referências lidas conforme a necessidade.

Pergunta: Um commit prova que a memória é verdadeira?
Resposta: Não. Ele registra uma versão; a confirmação factual depende das evidências e da revisão do conteúdo.

Pergunta: MemFS inclui automaticamente embeddings?
Resposta: Não. A documentação distingue busca comum de arquivos e modos semânticos ou híbridos opcionais, com componentes adicionais e indexação.

Pergunta: Busca de conversa e busca de memória são a mesma operação?
Resposta: Não. Conversas possuem histórico próprio; arquivos MemFS representam memória organizada. Encontrar um item num desses acervos não comprova cobertura do outro.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R013:C05 — mecanismo_avancado

No MemFS atual, arquivos de memória na raiz são carregados a cada turno; agentes antigos podem usar a pasta system. Diretórios com índice MEMORY.md permanecem fora da janela até consulta. Essa organização transforma nomes e descrições em sinais de descoberta. O mecanismo não inclui índice semântico por padrão: busca por arquivos, memória vetorial opcional e busca no histórico conversacional são capacidades separadas com requisitos próprios.

Condição de contorno:
Um arquivo persistido num diretório profundo pode continuar invisível na prática se o índice não orientar sua descoberta ou se o agente não abrir a referência necessária.

Contrato proposto:
- Entradas: Checkout do agente, arquivos com metadados, índices de diretórios e configuração de busca efetivamente instalada.
- Saídas: Contexto essencial carregado, referências descobríveis e conteúdo aprofundado lido sob demanda.
- Estado: Commits, alterações locais, sincronização e índices opcionais com revisões correspondentes.
- Invariante: Alegar que uma memória foi usada exige leitura ou carregamento efetivo; presença no repositório não basta.

Compromissos de projeto:
- Arquivos essenciais na raiz simplificam acesso recorrente e consomem orçamento em toda chamada.
- Hierarquia reduz contexto ativo e depende de bons índices; busca semântica opcional acrescenta instalação, indexação e manutenção.

## R013:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar memória profunda sem atualizar seu índice e depois mover o arquivo. A avaliação deve detectar perda de descoberta e referências quebradas, mesmo que o conteúdo continue versionado no Git.

Plano de avaliação proposto:
Avaliação proposta: comparar organização plana e hierárquica com tarefas que exigem referências antigas. Medir memória encontrada, arquivos abertos, tokens fixos e sincronização entre computadores; avaliar busca lexical e semântica como configurações distintas.

Comparações:
- R014 (complements): R014 é um alias desta mesma referência, preservado para discutir colaboração; não representa outro mecanismo independente.
- T014 (specializes): MemFS concretiza carregamento progressivo por organização de arquivos e índices.

Afirmação rastreável:
A documentação MemFS descreve raiz ativa, diretórios sob demanda, ausência de índice vetorial padrão e sincronização via commits e push.
Suporte: direct; fontes: A-S010
Limite: Documentação dinâmica consultada em 2026-11-05; instalações antigas e modalidades locais podem ter organização e disponibilidade distintas.

Nota de pesquisa:
MemFS reaberto em 2026-11-05. Mantida a equivalência nominal oficial com context repository e a identidade canônica R013. Aprofundamento baseado na documentação atual, sem afirmar instalação de mods, índice semântico ou sincronização no ambiente do usuário. Contratos e testes são propostas.

## R013:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou residência e carregamento do MemFS. Aqui a proposta organiza arquivos por estabilidade, custo de leitura e frequência de mudança.

Projeto e decomposição
Separe identidade e convenções estáveis de notas voláteis de tarefa. Arquivo sempre carregado deve ser pequeno e discriminativo; detalhes grandes ficam em caminhos descobríveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Controle adaptativo
Projete índice para distinguir arquivos parecidos e declarar quando abri-los. Nome de arquivo sozinho pode não informar escopo; descritores devem apontar finalidade e limites.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Validação contrafactual
Compare memória plana e organização por estabilidade. Meça arquivos abertos sem uso, leituras repetidas e instruções antigas aplicadas; contar tokens iniciais não capta custo de expansão. Unidade de avaliação: repositório de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Agente de projeto longo
Cenário: Memória reúne decisões e notas temporárias.
Estratégia: Manter visão inicial de objetivos e índices, carregar módulo ativo e arquivar detalhes concluídos com referência. Não promover nota temporária para convenção.
Papel do modelo pequeno: 3–7B lê índice; 8–14B trabalha por módulo.
Aceite proposto: Retomada deve carregar decisões vigentes sem trazer hipóteses encerradas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Conhecimento compartilhado
Cenário: Vários agentes precisam dos mesmos procedimentos.
Estratégia: Separar conteúdo comum de notas individuais, versionar correções e testar se cada leitor abre procedimento completo quando necessário.
Papel do modelo pequeno: 15–30B integra conflitos.
Aceite proposto: Mudança compartilhada deve ser visível na revisão declarada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de índice curto e arquivos com estrutura explícita.
8–14B: Agente que carrega e atualiza módulos limitados.
15–30B: Integrador de memórias compartilhadas com conflitos entre fontes.
Requisitos de treino/runtime: MemFS e versão do produto identificados, arquivos acessíveis e política de edição; não presumir indexação semântica automática.
Não aplicar quando: Arquivos crescem sem catálogo ou usuários confundem conteúdo no disco com conteúdo recebido pelo modelo.

## R013:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C028 — Letta / MemFS e Context Repositories
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve memória em arquivos e repositórios de contexto.
Mecanismo documentado: Conteúdo seletivamente residente, edição de arquivos e versionamento Git.
Correspondência com esta base: MemFS é referência principal.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.
Limite: Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S010, V2B-S003, V3A-S046.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R013:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R013 → T014 [complements]
Como combinar: Usar descritores para selecionar arquivos antes da carga.
Interface: Caminho, escopo, versão e finalidade.
Condição: Descrição distinguir recursos próximos.
Aceite proposto: Testar arquivo raro necessário à tarefa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R013 → T076 [requires]
Como combinar: Preservar revisão das alterações de memória.
Interface: Commit, arquivo, diff e origem.
Condição: Merge semântico revisado quando necessário.
Aceite proposto: Detectar duas decisões incompatíveis em arquivos separados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir busca de conversa com índice semântico dos arquivos.
- Não contar R014 como implantação adicional deste mesmo sistema.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade de retomada e custo de leitura; estrutura de arquivos não compensa instruções ambíguas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R002, R014, R027, T014, T053, T072, T076

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2B-S003 — Introducing Context Repositories: Git-based Memory for Coding Agents

[https://www.letta.com/blog/context-repositories/](https://www.letta.com/blog/context-repositories/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Origem do nome Context Repositories, memória em Git, divulgação progressiva e trabalho de subagentes em worktrees.

Limite: Anúncio histórico de fevereiro de 2026; descreve system/ e ativação antigos. Regras atuais de MemFS prevalecem. Não houve reprodução dos fluxos descritos.

### V3A-S046 — Letta Shared memory

[https://docs.letta.com/concepts/shared-memory](https://docs.letta.com/concepts/shared-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MemFS pertence a um agente; repositório compartilhado pertence à organização e requer commit, push e pull para sincronização entre checkouts.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R014 — Letta Context Repositories

**Nome canônico:** Letta MemFS — Context Repositories  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Letta context repository; Context Repositories da Letta

## R014:C01 — conceito

Context Repositories é o nome apresentado pela Letta para memória do agente organizada em repositório Git e arquivos locais. A documentação de MemFS declara explicitamente a equivalência de nomes. Esta entrada preserva a referência solicitada no inventário e destaca colaboração e versionamento; não representa um produto independente adicional ao MemFS.

Como funciona:
- O repositório permite inspecionar mudanças de memória por diff e manter histórico de revisões.
- O anúncio descreve subagentes em worktrees separados, com alterações posteriormente integradas ao repositório compartilhado.
- Hierarquia, descrições e índices orientam a seleção de contexto, enquanto o conteúdo aprofundado permanece disponível para consulta.

Nota de nomenclatura: Alias relacionado explicitamente ao canonical_id R013. O blog é histórico; regras operacionais atuais devem ser verificadas na documentação de MemFS.

## R014:C02 — aplicacao

Quando usar:
- Comparação de padrões de memória colaborativa e rastreamento de decisões textuais.
- Projetos com vários agentes contribuindo para conhecimento persistente sobre o mesmo código.

Quando não usar:
- Para contabilizar duas soluções distintas quando MemFS e Context Repositories aparecem na mesma lista.

Implementação proposta:
- Proposta: mapear este nome para R013 no catálogo e conservar a origem do anúncio como referência histórica.
- Distribuir assuntos por escritor, criar worktrees e exigir fonte e justificativa em cada mudança de memória.
- Revisar conflitos semânticos após o merge: dois arquivos podem discordar mesmo quando o Git não apresenta conflito textual.

Aplicação LAI proposta:
Proposta LAI: usar esta ficha para esclarecer nomenclatura e avaliar escrita paralela de memória, com integração condicionada à validação das evidências.

## R014:C03 — riscos_validacao

Armadilhas:
- O anúncio descreve uma organização antiga com system/; implementar a estrutura da documentação correspondente à versão instalada.
- Merge sem conflito não comprova coerência, atualidade ou isolamento entre clientes; duplicar aliases pode inflar a recuperação.

Métricas sugeridas:
- Duplicação de fichas canônicas, divergências de fatos, tempo de integração e precisão da memória recuperada.

Testes propostos:
- Proposta: pesquisar ambos os nomes e confirmar a resolução ao mesmo conceito, preservando as duas referências.
- Criar conclusões incompatíveis em worktrees separados e testar se a revisão detecta a contradição após integrar os arquivos.

## R014:C04 — perguntas_proveniencia

Pergunta: Context Repositories é um produto autônomo?
Resposta: A fonte atual o apresenta como outro nome de MemFS; esta base não cria um terceiro produto.

Pergunta: Worktrees resolvem contradições de memória?
Resposta: Eles isolam alterações. Resolver contradições exige comparar significado, evidência e validade temporal, além de integrar o Git.

Pergunta: Por que manter duas fichas se são aliases?
Resposta: Para preservar o inventário solicitado e permitir busca pelos dois nomes. A identidade canônica impede contabilizar duas tecnologias onde há uma equivalência nominal.

Pergunta: Merge sem conflito significa memória correta?
Resposta: Não. Git verifica compatibilidade textual de mudanças. Regras contraditórias, escopo errado ou fontes frágeis precisam de validação do conteúdo.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R014:C05 — mecanismo_avancado

Esta entrada é um alias de R013, não um segundo produto. Seu foco complementar é a colaboração: worktrees podem isolar alterações de memória, mas integrar texto não valida conclusões. Também é necessário distinguir o context repository individual do agente de um shared memory repository organizacional. Ambos usam Git, porém propriedade, leitores e sincronização são contratos diferentes; compartilhar o mesmo formato não torna o escopo automaticamente comum.

Condição de contorno:
Colaboração perde coerência quando agentes leem commits diferentes sem registrar a revisão, ou quando uma integração textual limpa combina conclusões incompatíveis.

Contrato proposto:
- Entradas: Repositório e proprietário, commits de base, mudanças de agentes e política de integração.
- Saídas: Revisão integrada com conflitos resolvidos explicitamente e registro de publicação aos consumidores.
- Estado: Worktrees, branches, commits lidos, revisões pendentes e associação de agentes aos repositórios.
- Invariante: Alias R014 resolve para R013; colaboração não aumenta a contagem de mecanismos independentes de memória.

Compromissos de projeto:
- Worktrees permitem pesquisa paralela e tornam necessárias integração e revisão de dependências.
- Repositórios compartilhados reduzem duplicação de conhecimento e ampliam o impacto de uma memória incorreta publicada.

## R014:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dois agentes alteram regras em arquivos distintos, produzindo incompatibilidade sem conflito de linhas. A revisão deve detectar o problema antes de publicar uma versão recomendada aos demais agentes.

Plano de avaliação proposto:
Avaliação proposta: comparar manutenção por um agente e trabalho paralelo com integração em tarefas equivalentes. Medir conflitos semânticos, tempo até convergência, revisões efetivamente lidas e correções propagadas; controlar a quantidade total de trabalho para não confundir paralelismo com qualidade.

Comparações:
- R013 (complements): É a mesma referência canônica; esta ficha acrescenta o recorte de colaboração e publicação.
- T076 (specializes): O uso de Git para memória concretiza versionamento e sincronização, mantendo necessidade de revisão factual.

Afirmação rastreável:
MemFS é chamado context repository; Letta distingue memória individual e repositórios compartilhados e documenta commit, push e pull entre checkouts.
Suporte: direct; fontes: A-S010, V3A-S046
Limite: A equivalência de nomes não torna repositórios individuais e organizacionais idênticos em propriedade ou acesso.

Nota de pesquisa:
Alias preservado: R014 → R013 conforme declaração explícita de MemFS na documentação Letta. O anúncio Context Repositories foi reaberto e a página atual Shared memory foi consultada para separar colaboração em memória individual de repositórios organizacionais. Nenhum produto independente foi inventado; contratos e testes são propostas.

## R014:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 registrou R014 como alias de R013. Aqui a novidade é controlar esse alias no catálogo e evitar duplicação de memória, métricas e casos.

Projeto e decomposição
Mantenha uma identidade canônica para MemFS/Context Repositories no escopo editorial adotado. Consultas pelos dois nomes devem chegar à mesma implementação e às mesmas versões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Controle adaptativo
Apresente diferenças de terminologia como metadados, sem criar um segundo pipeline de memória. Duplicar catálogos pelo alias pode gerar duas cópias divergentes da mesma regra.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Validação contrafactual
Compare resolução com e sem normalização de alias. Meça resultados duplicados, referências inconsistentes e contagem inflada de casos; nomes distintos não demonstram implantações independentes. Unidade de avaliação: alias de componente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Migração de documentação
Cenário: Equipe usa nomes diferentes para a mesma família.
Estratégia: Resolver nomes antigos para identidade canônica, preservar histórico e exibir fonte que fixa escopo. Não alterar conteúdo só para adequar rótulo.
Papel do modelo pequeno: 3–7B normaliza termos.
Aceite proposto: Consulta por qualquer alias deve retornar mesma revisão elegível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Grafo de combinações
Cenário: Catálogo precisa mostrar relações entre técnicas.
Estratégia: Colapsar alias antes de calcular cobertura e impedir aresta que sugira composição entre cópias do mesmo componente.
Papel do modelo pequeno: 8–14B explica equivalência editorial.
Aceite proposto: Não contar R013 e R014 como dois casos ou duas camadas técnicas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Resolvedor de nomes para IDs canônicos em vocabulário fechado.
8–14B: Leitor que explica diferenças de nomenclatura sem inventar capacidades.
15–30B: Revisor de migrações de catálogo com versões históricas e escopos diferentes.
Requisitos de treino/runtime: Tabela de aliases e escopo editorial explícito; revisar se documentação futura passar a distinguir produtos materialmente.
Não aplicar quando: Fonte nova indicar produtos diferentes e o catálogo insistir em colapsá-los sem revisão.

## R014:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C028 — Letta / MemFS e Context Repositories
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve memória em arquivos e repositórios de contexto.
Mecanismo documentado: Conteúdo seletivamente residente, edição de arquivos e versionamento Git.
Correspondência com esta base: Alias editorial da mesma família; não segundo caso.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.
Limite: Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S010, V2B-S003, V3A-S046.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R014:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R014 → R013 [alternative]
Como combinar: Resolver este nome para a ficha canônica, sem etapa adicional.
Interface: canonical_id=R013, alias e revisão do catálogo.
Condição: Escopo continuar equivalente ao adotado na base.
Aceite proposto: Consultar ambos os nomes e comparar identidade e fontes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R014 → T066 [requires]
Como combinar: Normalizar nome antes de abrir memória correspondente.
Interface: Alias, identidade canônica e versão.
Condição: Resolver preservar histórico de renomeação.
Aceite proposto: Detectar alias apontando para objeto diferente sem evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar dois rótulos para inflar meta de produção.
- Não atribuir a nome editorial capacidades ausentes das fontes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar consistência de resolução e clareza do catálogo; alias não altera capacidade de modelo nem qualidade de memória.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R002, R013, R027, T075, T076, T237, T239

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2B-S003 — Introducing Context Repositories: Git-based Memory for Coding Agents

[https://www.letta.com/blog/context-repositories/](https://www.letta.com/blog/context-repositories/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Origem do nome Context Repositories, memória em Git, divulgação progressiva e trabalho de subagentes em worktrees.

Limite: Anúncio histórico de fevereiro de 2026; descreve system/ e ativação antigos. Regras atuais de MemFS prevalecem. Não houve reprodução dos fluxos descritos.

### V3A-S046 — Letta Shared memory

[https://docs.letta.com/concepts/shared-memory](https://docs.letta.com/concepts/shared-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MemFS pertence a um agente; repositório compartilhado pertence à organização e requer commit, push e pull para sincronização entre checkouts.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R015 — Learning by Distilling Context

**Nome canônico:** Learning by Distilling Context  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R015  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Snell, Klein e Zhong 2022; context distillation por treinamento

## R015:C01 — conceito

Learning by Distilling Context investiga transferir para os parâmetros de um modelo benefícios antes dependentes de instruções, exemplos ou rascunhos no contexto. O trabalho de Snell, Klein e Zhong usa autotreinamento com respostas produzidas sob contexto mais informativo. É aprendizagem paramétrica; não equivale a resumir uma conversa em arquivo para reutilização posterior.

Como funciona:
- Para entradas da tarefa, o modelo condicionado em instruções pode produzir rascunho e resposta final.
- O treinamento usa a resposta final como alvo, condicionada somente na entrada, sem exigir aquelas instruções ou o rascunho.
- O professor e o aluno podem partir do mesmo modelo; a vantagem supervisionada vem do contexto adicional.

Nota de nomenclatura: Distinguir esta referência de consolidação por resumos, registrada em T069. Não transportar resultados publicados para Qwen ou português sem avaliação.

## R015:C02 — aplicacao

Quando usar:
- Tarefas repetidas com instruções estáveis e dados representativos para um experimento de treinamento.

Quando não usar:
- Fatos mutáveis que precisam de atualização imediata ou situações sem avaliação confiável das respostas geradas.

Implementação proposta:
- Proposta: escolher uma tarefa estreita, congelar instruções e gerar entradas sintéticas sem misturar exemplos de teste.
- Produzir alvos com contexto completo, filtrar erros verificáveis e manter vínculo entre entrada, prompt e resposta.
- Treinar um aluno em cópia controlada do checkpoint e comparar com o modelo base e o professor contextualizado.

Aplicação LAI proposta:
Proposta LAI: avaliar destilação de uma rotina estável de classificação ou extração; continuar recuperando documentos para conhecimento atualizado e auditável.

## R015:C03 — riscos_validacao

Armadilhas:
- Erros do professor podem virar supervisão; respostas fluentes não bastam para selecionar bons exemplos.
- Reduzir tokens de instrução pode sacrificar flexibilidade; mudanças de política exigem nova avaliação ou adaptação.

Métricas sugeridas:
- Acerto em teste reservado, aderência a novas instruções, tokens por inferência e custo total de treinamento.

Testes propostos:
- Proposta: avaliar todos os sistemas nas mesmas entradas, mantendo separados dados de geração, treino e teste.
- Incluir exceções, mudanças de regra e tarefas fora da distribuição para medir perdas ocultadas pela média.

## R015:C04 — perguntas_proveniencia

Pergunta: Esse método cria memória externa?
Resposta: Não. Ele ajusta parâmetros para internalizar comportamento que se beneficiava de contexto adicional.

Pergunta: O professor precisa ser maior que o aluno?
Resposta: Não neste desenho. O mesmo modelo recebe contexto privilegiado para produzir os alvos usados no treinamento.

Pergunta: Destilar exige um professor maior?
Resposta: Não necessariamente. O professor pode ser o mesmo modelo com contexto ou processo de geração mais informativo.

Pergunta: O aluno passa a fornecer a fonte de cada resposta?
Resposta: Não automaticamente. Treinamento paramétrico não cria proveniência por afirmação; quando citações são necessárias, mantenha um mecanismo explícito de recuperação e verificação.

Escopo das fontes:
Resumo e metadados do paper original foram consultados novamente em 2026-11-05. O mecanismo descrito está no resumo. O protocolo LAI é proposta editorial, sem reprodução experimental nem treinamento executado.

## R015:C05 — mecanismo_avancado

O ganho do professor em Learning by Distilling Context vem de uma assimetria informacional: ele recebe contexto instrutivo e pode produzir um rascunho antes da resposta; o treinamento pede ao aluno a resposta final sem aqueles apoios. Professor e aluno podem partir do mesmo modelo. A supervisão transfere comportamento observado, não garante copiar todo o processo que o produziu nem preservar informações ausentes das entradas de treinamento.

Condição de contorno:
A destilação pode falhar quando respostas do professor contêm erros, entradas sintéticas não cobrem o domínio ou a informação omitida varia de modo imprevisível em cada chamada.

Contrato proposto:
- Entradas: Modelo, instruções enriquecidas, entradas da tarefa e respostas finais produzidas com o contexto professor.
- Saídas: Modelo ajustado e avaliação de desempenho sem o contexto removido.
- Estado: Dados de autotreinamento, versões dos pesos, processo de filtragem e escopo de avaliação.
- Invariante: Remover contexto na inferência só é considerado adequado após verificar o comportamento em entradas independentes.

Compromissos de projeto:
- Internalizar instruções pode reduzir custo recorrente e acrescenta treinamento e manutenção.
- Saídas sintéticas ampliam supervisão e podem reproduzir vieses ou erros do próprio modelo professor.

## R015:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir dados em que o professor usa uma instrução válida somente para parte das entradas e depois avaliar uma exceção nova. O aluno deve ser testado quanto a generalização indevida, mesmo que imite bem os dados sintéticos.

Plano de avaliação proposto:
Avaliação proposta: comparar modelo base com e sem contexto, professor enriquecido e aluno ajustado em divisões independentes. Medir qualidade por condição, regressões, obediência a instruções novas e custo amortizado; manter exemplos de avaliação fora da geração de treinamento.

Comparações:
- T179 (specializes): O trabalho é uma referência concreta para destilação paramétrica de benefícios do contexto.
- T069 (distinct_from): Consolidação por resumos preserva informação em texto externo; aqui o aprendizado altera os parâmetros do modelo.

Afirmação rastreável:
Snell, Klein e Zhong treinam o modelo a prever respostas finais sem instruções ou scratchpad presentes na geração dos alvos.
Suporte: direct; fontes: A-S040
Limite: O artigo não demonstra que qualquer conhecimento possa ser internalizado sem perda nem elimina necessidade de evidência atualizada em tarefas mutáveis.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R015:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou professor contextual e aluno. Aqui distilação de contexto é avaliada pela capacidade de atualizar, esquecer e detectar conhecimento não internalizado.

Projeto e decomposição
Defina qual conhecimento ou comportamento deve ser internalizado e qual continuará recuperável externamente. Um aluno pode reproduzir respostas frequentes sem aprender condições que as tornam válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

Controle adaptativo
Atualização de contexto exige dados novos e análise de interferência. Manter evidência externa facilita corrigir fatos sem depender apenas de retreino, especialmente quando domínio muda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

Validação contrafactual
Compare aluno antes/depois, professor com contexto e aluno com RAG. Meça generalização, atualização de fatos e regressões fora da tarefa; não assumir que todo raciocínio do professor foi transferido. Unidade de avaliação: ciclo de distilação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

USO AVANÇADO — Procedimento estável de alta frequência
Cenário: Instruções repetidas dominam custo.
Estratégia: Gerar exemplos com variações e exceções, treinar aluno e manter teste de aderência à versão vigente. Retirar prompt somente após validar.
Papel do modelo pequeno: 3–7B aluno especializado.
Aceite proposto: Casos novos devem obedecer condições, não só reproduzir formatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

USO AVANÇADO — Conhecimento técnico mutável
Cenário: Fatos mudam após treinamento.
Estratégia: Internalizar vocabulário e habilidades estáveis, mantendo dados recentes em RAG; testar se aluno aceita correção explícita das fontes.
Papel do modelo pequeno: 8–14B leitor híbrido.
Aceite proposto: Não insistir em fato antigo quando evidência atual contradiz pesos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S040, A-S011.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Aluno de tarefa fechada com dados de alta qualidade e cobertura de exceções.
8–14B: Aluno híbrido que combina habilidade internalizada e conhecimento externo.
15–30B: Professor ou aluno de integração complexa quando custo de treino justificar.
Requisitos de treino/runtime: Acesso a treino, dados autorizados, versão de contexto e avaliação por origem; compressão externa T069 não é o mesmo processo.
Não aplicar quando: Conhecimento muda rápido, dados são insuficientes ou aluno não demonstra generalização além de respostas vistas.

## R015:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q017, V4A-Q024.

## R015:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R015 → T179 [complements]
Como combinar: Formalizar transferência como atualização de parâmetros.
Interface: Professor, contexto, exemplos e checkpoint do aluno.
Condição: Treino e mudança de pesos serem verificáveis.
Aceite proposto: Comparar comportamento em exemplos inéditos e exceções.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S040, A-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R015 → T009 [complements]
Como combinar: Manter fatos voláteis em recuperação externa.
Interface: Consulta, evidência vigente e versão.
Condição: Aluno respeitar contexto quando contradiz memória paramétrica.
Aceite proposto: Atualizar fato no corpus e medir resposta sem retreinar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S040, A-S011. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar resumo salvo de destilação paramétrica.
- Não usar resultado do professor como verdade sem verificar dados de treino.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefa delimitada e custo amortizado; aprender com professor contextual não transfere toda sua capacidade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R012, T069, T177, T178, T179, T180, P017

## Fontes primárias associadas

### A-S040 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fine-tuning para internalizar benefícios de instruções e exemplos antes fornecidos no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

[https://aclanthology.org/2026.emnlp-main.2431/](https://aclanthology.org/2026.emnlp-main.2431/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diagnóstico de componentes do prompt e autodestilação seletiva em adaptadores LoRA.

Limite: Identificação pelo título completo; há projetos homônimos. Resultados publicados não foram reproduzidos nesta entrega.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R016 — Lost in the Middle

**Nome canônico:** Lost in the Middle: How Language Models Use Long Contexts  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R016  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** efeito de posição em contexto longo; lost-in-the-middle effect

## R016:C01 — conceito

Lost in the Middle avalia como a posição da evidência afeta modelos de linguagem em perguntas sobre múltiplos documentos e recuperação de pares chave-valor. Nos experimentos publicados, a informação no início ou fim frequentemente foi mais bem utilizada que no meio. O resultado é um alerta experimental sobre uso efetivo de contexto, não uma lei universal para todo modelo atual.

Como funciona:
- Mover a mesma evidência pelo contexto permite separar disponibilidade de informação e capacidade de utilizá-la.
- Aumentar distratores pode elevar o comprimento sem acrescentar informação útil; a janela aceita não mede compreensão.

Nota de nomenclatura: Primeira submissão em 2023; não é benchmark atual do checkpoint ou servidor do usuário.

## R016:C02 — aplicacao

Quando usar:
- Desenho de avaliações de RAG, montagem de contexto e comparação de modelos com janelas extensas.

Quando não usar:
- Para concluir, sem teste, que determinado modelo falha sempre no meio ou que evidências finais são universalmente melhores.

Implementação proposta:
- Proposta: construir perguntas com resposta verificável e evidência identificada, mantendo fixos pergunta e conteúdo relevante.
- Variar sistematicamente posição, comprimento e quantidade de distratores; controlar truncamento e orçamento de saída.
- Comparar contexto completo, recuperação seletiva e diferentes ordenações usando o mesmo checkpoint e configuração de geração.

Aplicação LAI proposta:
Proposta LAI: usar uma bateria de posições como critério para escolher o orçamento e a ordenação do contexto no RAG da Helena.

## R016:C03 — riscos_validacao

Armadilhas:
- Mover documentos pode mudar relações entre trechos; controlar essa variável antes de atribuir tudo à posição.
- Uma resposta correta por conhecimento prévio pode esconder que o modelo ignorou a evidência fornecida.

Métricas sugeridas:
- Acerto por posição relativa, suporte das citações, degradação com distratores e tokens consumidos por resposta correta.

Testes propostos:
- Proposta: incluir fatos sintéticos ou versões contraditórias controladas para exigir uso do material apresentado.
- Testar também ausência de evidência e múltiplas evidências necessárias; registrar variância entre execuções e falhas de truncamento.

## R016:C04 — perguntas_proveniencia

Pergunta: Uma janela maior garante recuperação melhor?
Resposta: Não. O estudo mostra que aceitar mais tokens e utilizar a evidência corretamente são propriedades diferentes.

Pergunta: Basta colocar tudo importante no final?
Resposta: Isso é uma hipótese de ordenação a testar. Evidência distribuída, dependências e o modelo escolhido podem alterar o resultado.

Pergunta: Devo colocar toda evidência importante no começo e no fim?
Resposta: Não existe regra universal. Isso pode duplicar tokens e não resolver relações complexas. Teste a montagem no modelo e tarefa efetivamente usados.

Pergunta: Uma janela maior elimina a necessidade de recuperação?
Resposta: Não necessariamente. Recuperação pode selecionar conteúdo útil mesmo quando tudo caberia; compare qualidade e custo sob condições controladas.

Escopo das fontes:
Resumo e metadados da versão arXiv foram consultados novamente em 2026-11-05. As observações pertencem aos modelos e tarefas estudados; a bateria proposta não foi executada no ambiente LAI.

## R016:C05 — mecanismo_avancado

O valor metodológico de Lost in the Middle está no controle de posição: manter a evidência e mudar sua localização permite testar utilização, em vez de apenas disponibilidade. Para uma avaliação atual, posição absoluta e relativa precisam ser separadas do comprimento total e da quantidade de distratores. Reordenar trechos também pode alterar relações entre eles, portanto a intervenção deve preservar o conteúdo e a estrutura necessária à pergunta.

Condição de contorno:
A tendência observada não é lei universal de toda arquitetura ou modelo atual; tarefas de agregação e múltiplas evidências podem apresentar padrões diferentes de recuperação pontual.

Contrato proposto:
- Entradas: Contextos controlados, evidência identificada, posições alternativas e configuração fixa do modelo.
- Saídas: Desempenho por posição e comprimento, com registro de evidência realmente utilizada na resposta.
- Estado: Versão do modelo, ordem dos trechos, geração de distratores e divisão independente de avaliação.
- Invariante: Aceitar o tamanho da entrada não é interpretado como capacidade uniforme de utilizar toda a informação contida nela.

Compromissos de projeto:
- Mover evidência ajuda diagnosticar atenção efetiva e pode introduzir mudanças de vizinhança que precisam controle.
- Encurtar contexto reduz distratores e também pode remover apoio necessário a tarefas de combinação.

## R016:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deslocar a mesma evidência entre início, meio e fim, mantendo demais elementos equivalentes. Se o acerto variar, a avaliação deve reportar dependência posicional, sem explicar a diferença por ausência da informação.

Plano de avaliação proposto:
Avaliação proposta: comparar posições em vários comprimentos e tarefas, com amostras novas e configurações iguais. Medir resposta sustentada, variabilidade e custo; separar localização de uma evidência de combinação de várias, sem usar perguntas do benchmark como conteúdo do RAG.

Comparações:
- T013 (complements): Capacidade efetiva de contexto exige medir uso da informação, além do limite nominal do modelo.
- T028 (complements): Reranking e montagem podem alterar posição da evidência, mas precisam ser avaliados sem ocultar condições relevantes.

Afirmação rastreável:
O artigo observa degradação quando evidência relevante fica no meio de contextos longos nos modelos e tarefas estudados.
Suporte: direct; fontes: A-S019
Limite: Os resultados pertencem ao estudo publicado; RULER também evidencia a necessidade de avaliar capacidades distintas, sem estabelecer posição ótima universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R016:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu posição da evidência. Aqui a avaliação distingue efeito de posição, competição entre evidências e organização estrutural do contexto.

Projeto e decomposição
Mover evidência sem alterar conteúdo permite investigar posição; adicionar distrações investiga competição. Misturar as duas intervenções impede saber por que a resposta mudou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

Controle adaptativo
Compare agrupamento por fonte e por afirmação mantendo citações e condições. Evidência no começo pode parecer forte apenas porque recebe rótulo mais claro ou é repetida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

Validação contrafactual
Construa avaliações próprias por modelo e quantização, sem importar perguntas de benchmark. Meça acerto por posição absoluta, posição relativa e comprimento, além de sensibilidade a múltiplas evidências necessárias. Unidade de avaliação: pacote de contexto controlado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

USO AVANÇADO — Montagem de contexto RAG
Cenário: Informação decisiva pode ficar enterrada.
Estratégia: Ordenar por requisitos e inserir índice curto, mantendo detalhes originais; comparar com ordem aleatória sem duplicar evidência.
Papel do modelo pequeno: 3–7B lê pacotes curtos.
Aceite proposto: Ganho deve persistir quando posição e quantidade de tokens são controladas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

USO AVANÇADO — Tarefa de múltiplos saltos
Cenário: Resposta depende de dois trechos distantes.
Estratégia: Agrupar trechos relacionados por ID de requisito e testar se leitor combina ambos; não assumir que colocar um no fim resolve integração.
Papel do modelo pequeno: 8–14B integra; 15–30B compara baseline.
Aceite proposto: Nenhuma conclusão pode depender de apenas um dos elos necessários.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor com evidência compacta e organização explícita por campo.
8–14B: Leitor de pacotes moderados testado em diferentes posições.
15–30B: Leitor de contexto amplo após medir robustez a distração e relações distantes.
Requisitos de treino/runtime: Controle experimental de posição, comprimento e repetição; resultados dependem de modelo, tarefa e configuração.
Não aplicar quando: O sistema toma Lost in the Middle como lei universal ou presume que todos os modelos atuais reproduzem o mesmo perfil.

## R016:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q018, V4A-Q024.

## R016:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R016 → T024 [complements]
Como combinar: Empacotar evidências por requisito com ordem testável.
Interface: Afirmação, trechos, posição e referências.
Condição: Builder registrar ordem efetivamente enviada.
Aceite proposto: Reordenar sem mudar conteúdo e medir decisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S019, V3A-S015, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R016 → T013 [requires]
Como combinar: Avaliar janela efetiva no consumidor concreto.
Interface: Modelo, tokenizer, comprimento e distribuição de evidências.
Condição: Teste cobrir carga relevante do produto.
Aceite proposto: Comparar posições sob o mesmo orçamento total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S019, V3A-S015, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não repetir a evidência para fabricar ganho de posição.
- Não extrapolar um resultado histórico para todos os modelos 3–30B.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar robustez a posição com dados idênticos; vantagem numa configuração não prova capacidade geral de longo contexto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T013, T018, T028, T037, T039, T222

## Fontes primárias associadas

### A-S019 — Lost in the Middle: How Language Models Use Long Contexts

[https://arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Avaliação de efeitos da posição da evidência em perguntas e recuperação de pares chave-valor.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S015 — RULER: What's the Real Context Size of Your Long-Context Language Models?

[https://arxiv.org/abs/2404.06654](https://arxiv.org/abs/2404.06654)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Capacidade de contexto medida em tarefas distintas, incluindo rastreamento e agregação, além de recuperação literal.

Limite: Foram consultados resumo e descrição geral das capacidades, sem perguntas ou gabaritos. Resultados de modelos históricos não qualificam modelos atuais automaticamente.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# R018 — Temporal

**Nome canônico:** Temporal  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R018  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Temporal durable execution; Temporal Workflows

## R018:C01 — conceito

Temporal é uma plataforma de execução durável de workflows. Ela registra histórico de eventos e reconstrói o estado por replay do código de orquestração. Operações externas ficam em Activities executadas por workers. O mecanismo ajuda a retomar processos após falhas; não conserva automaticamente a memória arbitrária de um processo nem garante efeitos externos exatamente uma vez.

Como funciona:
- O workflow deve tomar decisões compatíveis com o histórico registrado; valores não determinísticos exigem tratamento apropriado.
- Chamadas de LLM, rede e banco ficam em Activities, cujos resultados confirmados são reutilizados durante o replay.
- Uma Activity pode executar mais de uma vez por retries, inclusive depois de realizar parcialmente seu efeito.

Nota de nomenclatura: A garantia sobre o histórico não deve ser apresentada como exactly-once de qualquer serviço externo.

## R018:C02 — aplicacao

Quando usar:
- Missões longas com espera, múltiplas dependências e necessidade de recuperação operacional.

Quando não usar:
- Como substituto de memória semântica, cache KV ou validador da resposta produzida pela LLM.

Implementação proposta:
- Proposta: modelar etapas e condições de término; separar decisões determinísticas de integrações com efeitos externos.
- Definir timeouts, política de retry e chave de idempotência estável para cada operação de negócio.
- Guardar referências de artefatos grandes, registrar resultados de Activities e testar compatibilidade do replay ao evoluir o código.

Aplicação LAI proposta:
Proposta LAI: avaliar Temporal para coordenar tarefas extensas de programação e integrações da Helena, mantendo verificadores de conteúdo e evidências em etapas explícitas.

## R018:C03 — riscos_validacao

Armadilhas:
- Reexecutar uma escrita sem chave idempotente pode duplicar o efeito quando a confirmação anterior se perde.
- Persistência do workflow não confirma que uma ferramenta cumpriu o objetivo; sucesso operacional e qualidade são verificações distintas.

Métricas sugeridas:
- Workflows concluídos, tempo de retomada, retries por Activity, backlog de trabalho e efeitos duplicados.

Testes propostos:
- Proposta: interromper um worker depois do efeito externo e antes da confirmação; exigir reconciliação sem duplicação.
- Reproduzir históricos guardados com a nova definição do workflow e detectar incompatibilidades antes de substituir workers.

## R018:C04 — perguntas_proveniencia

Pergunta: Replay chama novamente toda LLM anterior?
Resposta: Resultados de Activities já confirmadas são reutilizados pelo histórico; atividades sem conclusão confirmada podem precisar de nova execução.

Pergunta: Temporal elimina a necessidade de idempotência?
Resposta: Não. Activities podem executar mais de uma vez, portanto os efeitos externos precisam tolerar repetição ou ser reconciliados.

Pergunta: Schedule-to-Start resolve uma fila sem workers com retry?
Resposta: Esse timeout é não repetível por desenho; reenfileirar na mesma fila não resolveria a ausência de capacidade.

Pergunta: Heartbeat local garante progresso recuperável?
Resposta: Não necessariamente. É preciso considerar throttling e o último detalhe efetivamente recebido pelo serviço.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R018:C05 — mecanismo_avancado

Os timeouts do Temporal delimitam fases diferentes. Schedule-to-Start mede espera de uma tarefa na fila; Start-to-Close limita uma tentativa; Schedule-to-Close delimita a execução lógica inteira, incluindo tentativas e esperas. Heartbeat informa atividade e progresso, mas o SDK pode agrupar transmissões: progresso registrado localmente antes da queda pode não ter chegado ao serviço. O workflow precisa reproduzir comandos compatíveis com o histórico; chamadas de modelo e integrações ficam em Activities, cujos efeitos precisam suportar repetição. Essa separação permite diagnosticar fila saturada sem confundi-la com worker travado.

Condição de contorno:
Timeout não confirma que um serviço externo parou de trabalhar. Uma tentativa anterior pode continuar e produzir efeito após o início de outra.

Contrato proposto:
- Entradas: Workflow ID, Activity ID, limites por fase, política de retry e chave da operação externa.
- Saídas: Resultado confirmado ou falha classificada por fase, com referência ao efeito observado.
- Estado: Histórico de comandos, tentativas, último heartbeat transmitido e versão do código.
- Invariante: Repetições conservam identidade lógica; resultado tardio é reconciliado antes de criar outro efeito.

Compromissos de projeto:
- Timeout curto acelera detecção, mas aumenta tentativas concorrentes quando o serviço apenas está lento.
- Heartbeat frequente melhora observabilidade, porém transmissão e persistência têm custo e atraso.

## R018:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover workers da fila e, separadamente, travar um worker após começar. Exigir diagnósticos distintos; interromper após efeito externo e confirmar reconciliação pela mesma chave.

Plano de avaliação proposto:
Comparar políticas com cargas e falhas idênticas. Medir espera de fila, tempo por tentativa, duração total, efeitos duplicados e atraso de recuperação; escolher limites a partir da distribuição operacional.

Comparações:
- T159 (specializes): Temporal oferece implementação concreta de execução durável, com regras próprias de histórico e workers.
- T162 (complements): Idempotência protege efeitos de Activities que podem repetir, fora da reconstrução determinística do workflow.

Afirmação rastreável:
Start-to-Close limita uma tentativa, enquanto Schedule-to-Close limita a execução da Activity ao longo das tentativas.
Suporte: direct; fontes: V2A-S010
Limite: Esses limites não equivalem a interromper atomicamente uma transação em serviço externo.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R018:C07 — estrategia_3_30b

NOVA CAMADA v4 — Avança dos timeouts para controle do crescimento do histórico, continuidade de identidade entre unidades de execução e tratamento de respostas externas tardias.

Histórico com orçamento
Proposta: medir crescimento do histórico por etapa, especialmente em polling e loops de agente. Guardar grandes documentos em armazenamento versionado e conservar referências verificáveis no estado. Planejar fronteiras de renovação ou subdivisão sem apagar a identidade lógica da tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

Resultado tardio
Tratar deadline local e estado remoto separadamente. Uma Activity interrompida pode deixar trabalho externo ativo. O resultado posterior deve ser associado à operação original e conciliado com a decisão vigente, sem iniciar outra operação por interpretar silêncio como falha definitiva.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

Upgrade com replay controlado
Usar históricos representativos para verificar compatibilidade antes de trocar workers. Chamadas a modelos permanecem fora da lógica determinística de workflow. A migração precisa preservar decisões já tomadas; reexecutar a LLM para preencher um resultado antigo muda o processo histórico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

USO AVANÇADO — Pesquisa longa em documentos versionados
Cenário: A tarefa atravessa falhas de worker e várias consultas.
Estratégia: Persistir decisões pequenas e referências imutáveis; dividir etapas por resultado verificável.
Papel do modelo pequeno: Extrair evidências e redigir sínteses dentro de Activities com prazo e resultado registrado.
Aceite proposto: Retomar após falha entre etapas sem consultar novamente fontes já congeladas por necessidade de replay.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

USO AVANÇADO — Operação externa com resposta ambígua
Cenário: Fornecedor responde depois do timeout da Activity.
Estratégia: Conservar operation_id e consultar status antes de repetir; registrar compensação somente quando definida pelo domínio.
Papel do modelo pequeno: Classificar evidência textual, sem decidir sozinho se um efeito remoto ocorreu.
Aceite proposto: Injetar resposta tardia e comprovar ausência de duplicação ou reconciliação explicitamente pendente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: ações semânticas pequenas; o workflow assume duração e persistência.
8–14B: 8–14B: microplanos com saídas tipadas e limites por Activity.
15–30B: 15–30B: reservar a interpretação mais difícil; tamanho não muda a semântica durável.
Requisitos de treino/runtime: Runtime, backend e políticas duráveis precisam de implantação própria; persistência não é aprendida pelo modelo.
Não aplicar quando: Não usar workflow determinístico como lugar para chamadas de rede ou amostragem de LLM.

## R018:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Foram pesquisados casos Temporal em Stripe/Coinbase e Cadence em Uber. Relato Cadence não foi convertido em adoção Temporal; resultados não confirmados não entram como produção exata.
Consultas registradas: V4C-Q002, V4C-Q022, V4C-Q025, V4C-Q029.

## R018:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R018 → T241 [complements]
Como combinar: Reproduzir transições registradas sem recriar efeitos externos.
Interface: Histórico, versão de worker e decisões persistidas.
Condição: Recuperação ou upgrade exige replay.
Aceite proposto: Histórico suportado reproduz comandos compatíveis e não repete chamada sem necessidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R018 → T243 [complements]
Como combinar: Encaminhar estados remotos incertos ao reconciliador.
Interface: Operation_id, tentativa, prazo e observações do destino.
Condição: Timeout não resolve o resultado de negócio.
Aceite proposto: Cada ambiguidade recebe estado verificável antes de retry de efeito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S018, V3C-S023, V3C-S024, V3C-S040. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir Cadence com Temporal apenas pela história compartilhada.
- Não confundir heartbeat recente com confirmação de efeito remoto.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sistemas completos sob quedas e atraso de rede, incluindo tempo de recuperação e duplicações. O ganho de durabilidade não deve ser atribuído a mais parâmetros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T060, T159, T160, T162, T241, T243

## Fontes primárias associadas

### V2B-S005 — Temporal Workflow

[https://docs.temporal.io/workflows](https://docs.temporal.io/workflows)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico de eventos, replay determinístico e reutilização de resultados de Activities já confirmadas.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S006 — Activity Definition

[https://docs.temporal.io/activity-definition](https://docs.temporal.io/activity-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Activities para ações externas, possibilidade de múltiplas execuções e necessidade de idempotência.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2A-S010 — Detecting Activity failures

[https://docs.temporal.io/encyclopedia/detecting-activity-failures](https://docs.temporal.io/encyclopedia/detecting-activity-failures)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Timeouts de atividades, heartbeats, detalhes de progresso e tentativas posteriores.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

### V3C-S023 — Temporal — Retry Policies

[https://docs.temporal.io/encyclopedia/retry-policies](https://docs.temporal.io/encyclopedia/retry-policies)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferenças entre retries de Activities, Workflow Executions e Workflow Tasks; limites de tentativas e prazo total.

Limite: Defaults e APIs são específicos do runtime; não foram presumidos como configurações LAI.

### V3C-S024 — Temporal — Activity Execution

[https://docs.temporal.io/activity-execution](https://docs.temporal.io/activity-execution)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de vida durável de Activities, despacho a workers e registro de resultados em workflows.

Limite: Retomar a execução não garante por si efeito externo exatamente uma vez.

### V3C-S040 — Temporal — Long-Running Activity pattern

[https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Heartbeats transportam detalhes de progresso e ajudam retomada e entrega de cancelamento em atividades longas.

Limite: Persistência depende de entrega ao serviço; heartbeat emitido localmente pode não sobreviver a crash antes do envio.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R019 — Aider

**Nome canônico:** Aider — programação assistida no terminal  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R019  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** aider.chat; AI pair programming com Aider

## R019:C01 — conceito

Aider é uma ferramenta de programação assistida que combina conversa com uma LLM, contexto do repositório e edição de arquivos. Seu repo map apresenta símbolos relevantes sem enviar necessariamente todo o código. Formatos de edição diferentes permitem substituir arquivos completos ou aplicar mudanças localizadas, conforme o modelo e a configuração.

Como funciona:
- O mapa sintetiza arquivos, classes, funções e assinaturas para orientar dependências e localização de código.
- O formato chamado diff pelo Aider usa blocos SEARCH/REPLACE; o formato udiff é baseado em unified diff, com adaptações.
- Comandos de teste podem devolver erros ao ciclo de correção; o código de saída informa falha operacional do comando.

Nota de nomenclatura: Nenhuma chamada ao Aider ou modelo foi executada. Formatos e recursos devem corresponder à versão instalada.

## R019:C02 — aplicacao

Quando usar:
- Mudanças localizadas em projetos Git, refatorações e correções com testes e critérios verificáveis.

Quando não usar:
- Quando faltam especificação e ambiente de validação, mas se pretende tratar uma edição aplicada como solução comprovada.

Implementação proposta:
- Proposta: trabalhar em branch ou worktree isolado e registrar a revisão inicial do repositório.
- Selecionar arquivos editáveis e referências relevantes; conferir o formato de edição aceito pelo modelo escolhido.
- Configurar comando de teste confiável e limite de tentativas; revisar o diff resultante contra a tarefa e os testes existentes.

Aplicação LAI proposta:
Proposta LAI: usar Aider como referência para repo map e edição incremental; comparar essas escolhas com o executor existente em pequenos reparos controlados.

## R019:C03 — riscos_validacao

Armadilhas:
- Repo map é uma seleção, não uma descrição completa de toda semântica ou de dependências dinâmicas.
- Trechos de busca repetidos ou arquivos alterados em paralelo podem provocar falha ou aplicação indevida de edições.

Métricas sugeridas:
- Aplicação correta do patch, testes relevantes aprovados, regressões, tokens e tentativas por alteração aceita.

Testes propostos:
- Proposta: usar um defeito conhecido, reproduzi-lo antes da edição e confirmar que o teste passa depois.
- Inserir trecho repetido e mudança concorrente para conferir se o executor identifica ambiguidade em vez de aceitar silenciosamente o resultado.

## R019:C04 — perguntas_proveniencia

Pergunta: O diff do Aider é sempre um unified diff?
Resposta: Não. O formato denominado diff usa busca e substituição; udiff é outro formato documentado.

Pergunta: Um patch aplicado e sem erro encerra a tarefa?
Resposta: Não. Ainda é necessário verificar comportamento, requisitos e possíveis regressões no código afetado.

Pergunta: Editor correto no formato significa plano implementado?
Resposta: Não. Compare as diferenças com requisitos e testes comportamentais específicos.

Pergunta: Por que um formatador pode confundir a correção automática?
Resposta: Se retornar código não zero por ter formatado código, o executor pode interpretar sucesso de formatação como falha de lint.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R019:C05 — mecanismo_avancado

O modo architect do Aider separa duas tarefas: formular a alteração e traduzi-la em instruções de edição. Os papéis podem usar modelos diferentes ou o mesmo modelo em duas chamadas. Isso separa erro de raciocínio de erro de formatação, mas uma tradução sintaticamente válida ainda pode contrariar o plano. O editor usa um formato próprio: diff significa SEARCH/REPLACE; udiff pertence a outra convenção. O repo map orienta localização, enquanto o conteúdo atual do arquivo determina a alteração aplicável. Na integração de lint, o código de saída precisa distinguir erro real de um formatador que apenas modificou arquivos.

Condição de contorno:
Dois estágios não garantem maior qualidade. Um plano incompleto, mapa desatualizado ou comando de validação mal configurado pode aumentar ciclos de correção.

Contrato proposto:
- Entradas: Revisão base, arquivos editáveis, proposta do architect, formato do editor e comandos de validação.
- Saídas: Alterações aplicadas, diagnóstico do parser e resultados associados à revisão modificada.
- Estado: Plano original, resposta do editor, diferenças resultantes e tentativas de reparo.
- Invariante: A edição preserva o escopo aprovado e é validada no conteúdo efetivamente produzido.

Compromissos de projeto:
- Separar papéis facilita localizar a causa da falha, mas acrescenta latência e consumo de contexto.
- SEARCH/REPLACE economiza saída, porém depende de trechos identificáveis no arquivo atual.

## R019:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer plano correto e fazer o editor emitir formato incompatível. Exigir rejeição explícita; configurar formatador com saída não zero e conferir que não produz falso ciclo de reparação.

Plano de avaliação proposto:
Comparar code e architect nas mesmas tarefas, revisões e orçamento total. Medir acerto funcional, aplicação de edições, divergência do plano e custo incluindo reparos; selecionar pela taxa de alterações aceitas.

Comparações:
- T229 (complements): Aider pode concretizar edição por patches, mas também oferece formatos de arquivo completo; o contrato depende da configuração.
- R027 (complements): Git fixa a base e permite comparar o resultado entre as etapas de planejamento e edição.

Afirmação rastreável:
Architect e editor são etapas separadas e podem utilizar o mesmo modelo em duas solicitações.
Suporte: direct; fontes: V3C-S042
Limite: A documentação não demonstra que a separação supera todo modelo e tarefa de programação.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R019:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda architect/editor com contrato semântico de tradução, classificação de erros e política de encaminhamento baseada no tipo de edição.

Plano testável para editor menor
Proposta: o planejador entrega arquivos elegíveis, comportamento esperado e condições que devem permanecer verdadeiras. O editor traduz essas condições para uma alteração limitada. Um plano em prosa sem critérios deixa a segunda etapa reconstruir a intenção, anulando a separação de responsabilidades.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

Diagnóstico de falha
Distinguir localização incorreta, formato inválido, conflito de base e regressão semântica. Repetir a mesma chamada com mais tokens não é tratamento universal. Uma falha de formato pode voltar ao editor; uma mudança de requisito precisa voltar ao planejador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

Roteamento por superfície
Separar edições mecânicas, mudanças locais e refatorações atravessando módulos. Modelos menores podem ser úteis nos dois primeiros grupos se houver ferramentas e testes adequados. O roteador deve aprender com resultados aceitos por classe, incluindo tentativas que não produziram patch.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

USO AVANÇADO — Atualização mecânica em muitos arquivos
Cenário: Mudança repetitiva tem regra e exceções identificáveis.
Estratégia: Produzir candidatos por AST/busca, deixar o editor resolver somente ambiguidades delimitadas e validar o conjunto.
Papel do modelo pequeno: 3–7B pode traduzir planos pequenos; transformação determinística executa casos inequívocos.
Aceite proposto: Comparar cobertura e falsos positivos com script simples, contabilizando revisão humana.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

USO AVANÇADO — Correção localizada
Cenário: Bug tem reprodução e poucos arquivos candidatos.
Estratégia: Congelar teste e base, produzir patch numa cópia isolada e devolver evidência ao planejador.
Papel do modelo pequeno: 8–14B edita; modelo maior só entra se falha semântica justificar.
Aceite proposto: Patch aplica na base declarada, resolve reprodução e não quebra testes relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: edição estreita com arquivo atual e invariantes explícitos, quando o backend e modelo forem compatíveis.
8–14B: 8–14B: correções locais com teste executável e contexto seletivo.
15–30B: 15–30B: planejamento multiarquivo sujeito a orçamento e comparação com decomposição menor.
Requisitos de treino/runtime: Validar suporte do provedor, formato de edição e comandos locais na versão utilizada.
Não aplicar quando: Não escolher dois modelos por prestígio; a tradução adicional pode elevar erro e custo.

## R019:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: Recurso nativo documentado do Aider.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Documentação do próprio Aider sustenta recursos disponíveis. Não foram confirmadas dez implantações Big Tech do produto; arquiteturas parecidas não foram renomeadas Aider.
Consultas registradas: V4C-Q023.

## R019:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R019 → T208 [complements]
Como combinar: Entregar ao executor uma intenção verificável em vez de apenas prosa livre.
Interface: Arquivos elegíveis, condição inicial, mudança e invariantes.
Condição: Há benefício medido em separar planejamento e edição.
Aceite proposto: O executor não precisa adivinhar requisito ausente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S042, V2B-S009, V2B-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R019 → T233 [feeds]
Como combinar: Submeter patch e base ao validador antes de integrar.
Interface: Patch, hash-base e comandos de verificação.
Condição: Toda alteração produz artefato revisável.
Aceite proposto: Conflito ou teste falho bloqueia a promoção do patch.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S042, V2B-S009, V2B-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar a opção diff como sinônimo universal de unified diff.
- Não avaliar apenas patches que aplicaram; tentativas inválidas também custam.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar arquiteturas de uma e duas chamadas no mesmo conjunto de bugs, com custo por correção aceita. Reportar editor pequeno e planejador maior como sistema híbrido, não capacidade isolada do editor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T216, T217, T229, T230, T231, T236, T239, R027

## Fontes primárias associadas

### V2B-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa conciso de arquivos e símbolos para contexto do código.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferença entre whole, diff com SEARCH/REPLACE e udiff adaptado.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S009 — Linting and testing

[https://aider.chat/docs/usage/lint-test.html](https://aider.chat/docs/usage/lint-test.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução de testes, interpretação de código de saída e configuração de testes após edições.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R020 — Claude Code

**Nome canônico:** Claude Code — agente de programação da Anthropic  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R020  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Claude Code CLI; claude -p

## R020:C01 — conceito

Claude Code é um agente de programação da Anthropic que inspeciona código, edita arquivos e executa ferramentas no ambiente disponível. Sua CLI também permite execução não interativa. A continuidade combina histórico de sessão, instruções de projeto e memória; esses mecanismos não equivalem a executar indefinidamente nem a comprovar que uma tarefa foi concluída.

Como funciona:
- O ciclo de trabalho usa ferramentas para ler, alterar e verificar o projeto, alimentando o modelo com os resultados.
- Arquivos de instruções e auto memory carregam contexto entre sessões; a documentação distingue contexto de configuração efetivamente imposta.
- A execução por claude -p oferece saídas consumíveis por scripts e opções explícitas de ferramentas e continuidade.

Nota de nomenclatura: Não houve instalação, autenticação ou execução real do Claude Code. A ficha não fixa modelo, plano ou compatibilidade local.

## R020:C02 — aplicacao

Quando usar:
- Implementação, investigação de defeitos e revisão em repositórios com comandos de validação conhecidos.
- Automação limitada por tarefa quando um controlador acompanha resultado, custo e término.

Quando não usar:
- Como substituto de um workflow durável ou de verificação independente de mudanças e efeitos externos.

Implementação proposta:
- Proposta: registrar versão, modelo, diretório de trabalho e política de ferramentas antes de uma missão.
- Manter instruções curtas sobre arquitetura e testes; passar evidências e escopo da mudança de forma explícita.
- Em automação, capturar saída estruturada, status de término e artefatos; validar o diff e os testes antes da próxima etapa.

Aplicação LAI proposta:
Proposta LAI: usar Claude Code como referência de executor de programação, mantendo o controlador de continuidade e os verificadores da Helena separados do histórico conversacional.

## R020:C03 — riscos_validacao

Armadilhas:
- Instruções em Markdown orientam o modelo, mas não impõem uma barreira operacional; controles precisam existir na execução.
- Retomar a conversa não garante que arquivos, dependências e serviços continuam iguais aos vistos anteriormente.

Métricas sugeridas:
- Tarefas aceitas, regressões, chamadas de ferramenta, custo por correção e progresso verificável por tentativa.

Testes propostos:
- Proposta: resolver um defeito reproduzível em checkout de teste e comparar o patch com critérios de aceite.
- Interromper e retomar a tarefa após mudar um arquivo; conferir releitura do estado e ausência de operações repetidas indevidamente.

## R020:C04 — perguntas_proveniencia

Pergunta: Memória de projeto garante cumprimento de regras?
Resposta: Não. Ela fornece contexto; restrições obrigatórias precisam ser verificadas por controles e ferramentas apropriados.

Pergunta: Modo headless garante recuperação após queda?
Resposta: Não por si só. O controlador precisa registrar execução, artefatos e estado confirmado para decidir como retomar.

Pergunta: Restaurar a conversa restaura o código?
Resposta: A ação permite conservar o código; os dois estados devem ser selecionados e verificados separadamente.

Pergunta: Um checkpoint listado garante arquivos recuperáveis?
Resposta: Não. Snapshots podem ter sido removidos; é necessário conferir disponibilidade e resultado da restauração.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R020:C05 — mecanismo_avancado

O checkpoint de Claude Code tem escopo de sessão e distingue restauração de código, conversa ou ambos. Resumir a conversa não altera arquivos. Há uma diferença operacional no rastreamento: após a ferramenta de edição tocar um arquivo, mudanças posteriores por Bash nesse arquivo podem ser desfeitas; um arquivo modificado somente por Bash permanece fora desse rastreamento. Edições de subagentes têm regras específicas de execução e de arquivos já acompanhados, portanto não cabem na suposição de restauração integral. O controlador deve registrar o conjunto coberto antes de usar rewind como recuperação.

Condição de contorno:
Snapshots sujeitos à retenção podem desaparecer. Caminhos simbólicos ou hard links são ignorados pela restauração documentada; efeitos em bancos não pertencem ao checkpoint.

Contrato proposto:
- Entradas: ID da sessão, checkpoint escolhido, escopo de restauração e inventário de arquivos e efeitos.
- Saídas: Código e/ou conversa restaurados, com lista de caminhos preservados ou ignorados.
- Estado: Snapshots disponíveis, arquivos rastreados e revisão Git anterior à tentativa.
- Invariante: A recuperação só declara concluído o escopo cuja restauração foi conferida por conteúdo.

Compromissos de projeto:
- Rewind facilita experimentar alternativas, mas sua cobertura depende de como cada alteração ocorreu.
- Restaurar só a conversa conserva trabalho útil, porém pode deixar o modelo sem explicação das mudanças atuais.

## R020:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: editar um arquivo pela ferramenta e outro apenas por Bash; executar mudança externa. Restaurar código e conferir hashes: exigir cobertura documentada e reconciliação separada do efeito externo.

Plano de avaliação proposto:
Comparar rewind e reconstrução por revisão Git em cenários equivalentes. Medir arquivos recuperados, alterações remanescentes e tempo de retomada; escolher o mecanismo conforme o escopo exigido.

Comparações:
- T240 (distinct_from): Snapshot genérico precisa definir cobertura; o checkpoint do produto cobre apenas o estado documentado da sessão.
- R027 (complements): Git mantém histórico versionado de código independente da retenção dos checkpoints da conversa.

Afirmação rastreável:
Arquivo alterado somente por Bash não é rastreado; alterações por Bash em arquivo previamente editado pela ferramenta podem ser restauradas.
Suporte: direct; fontes: V3C-S030
Limite: Regras consultadas nesta data; não afirmar que todos os subagentes ou tipos de arquivo têm cobertura idêntica.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R020:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o uso de Claude Code como referência de engenharia: medir contaminação da memória de projeto, perda de obrigações na compactação e qualidade dos limites de delegação.

Memória por evidência
Proposta para harness próprio: cada orientação persistida distingue fato do repositório, preferência e hipótese. Vincular instruções derivadas de código à revisão observada e revalidá-las quando arquivos relevantes mudarem. A memória deixa de ser um depósito de conclusões que se perpetuam sem teste.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

Compactação com obrigações
Antes de compactar, extrair condições de aceite, decisões pendentes, efeitos confirmados e artefatos por hash. Depois, executar uma recuperação de obrigações numa tarefa de controle. Texto menor só é melhoria se preservar os compromissos que governam a próxima ação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

Delegação e retorno mínimo
Definir tarefa, arquivos permitidos, budget e formato de evidência antes de criar um trabalhador. O retorno inclui achado, fonte e incerteza; não concatena toda a sessão. O integrador precisa verificar conflitos de base e qualidade do resultado, mesmo quando o subagente afirma ter concluído.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

USO AVANÇADO — Diagnóstico assistido de incidente
Cenário: Logs extensos e muitas hipóteses competem por contexto.
Estratégia: Separar coleta, teste de hipótese e alteração; manter trace e comando que sustenta cada achado.
Papel do modelo pequeno: Um trabalhador pequeno pode extrair padrões; autorização e execução permanecem no controlador.
Aceite proposto: Hipótese só vira fato depois de evidência reproduzível; medir falsas conclusões e tempo até diagnóstico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

USO AVANÇADO — Sessão longa de manutenção
Cenário: Múltiplas subtarefas atravessam compactações.
Estratégia: Persistir obrigações e estado por módulo; retomar lendo artefatos atuais antes de editar.
Papel do modelo pequeno: No harness próprio, leitor 8–14B recompõe contexto local sob schema.
Aceite proposto: Após compactação, recuperar todos os aceites ainda abertos sem restaurar histórico irrelevante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: aplicar padrões de localização e extração em harness compatível; não se afirma suporte do Claude Code a qualquer modelo pequeno.
8–14B: 8–14B: reproduzir contratos de memória/retomada no próprio sistema, com validação externa.
15–30B: 15–30B: avaliar integração de subtarefas; não presumir reprodução da qualidade dos modelos Claude.
Requisitos de treino/runtime: Separar aprendizado arquitetural de disponibilidade comercial e de backends documentados do produto.
Não aplicar quando: Não usar rewind como rollback universal de banco, rede ou arquivos não cobertos.

## R020:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: O operador descreve uso de Claude Code.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Medições incluem sessões Claude Code, sem demonstrar todos os recursos do produto.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Casos de uso interno Anthropic e medições Uber foram identificados. Uma equipe, um recurso e uma fonte adicional do mesmo produto não foram multiplicados como implantações independentes.
Consultas registradas: V4C-Q024.

## R020:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R020 → T234 [complements]
Como combinar: Versionar instruções persistidas junto de sua evidência e escopo.
Interface: Regra, módulo, revisão de origem e condição de revalidação.
Condição: Conhecimento de projeto é reutilizado entre sessões.
Aceite proposto: Regra obsoleta é detectada antes de orientar uma alteração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R020 → T212 [complements]
Como combinar: Compactar somente com registro explícito de obrigações e artefatos.
Interface: Pacote de retomada com pendências e hashes.
Condição: A sessão atinge orçamento de contexto.
Aceite proposto: A retomada conserva os aceites ativos e não inventa conclusão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar uso interno de Claude Code como evidência de modelos 3–30B.
- Não promover automaticamente anotações de subagente a instruções permanentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar o padrão de harness no modelo pequeno com execução de referência na mesma tarefa, distinguindo diferenças de ferramentas, permissões e infraestrutura.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T217, T218, T234, T235, T237, T239, R027

## Fontes primárias associadas

### V2B-S010 — Claude Code overview

[https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Agente de programação com leitura, edição, comandos, integração Git e opções de automação.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S011 — How Claude remembers your project

[https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instruções de projeto e auto memory; distinção entre conteúdo contextual e controles impostos na execução.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S012 — Run Claude Code programmatically

[https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução não interativa com claude -p, opções de saída e continuidade, códigos de término e diferenças entre modos.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V3C-S030 — Claude Code — Checkpointing

[https://code.claude.com/docs/en/checkpointing](https://code.claude.com/docs/en/checkpointing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointing distingue restauração de código, conversa e sumarização; escopo de arquivos e retenção são limitados.

Limite: Documentação consultada em 2026-11-05; não extrapolar cobertura para estado externo, todas as ferramentas ou outras versões.

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R021 — OpenAI Codex

**Nome canônico:** OpenAI Codex — agente e CLI de programação  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R021  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Codex CLI; codex exec

## R021:C01 — conceito

OpenAI Codex oferece um agente de programação capaz de inspecionar arquivos, editar código e executar comandos no ambiente autorizado. Esta ficha enfatiza a CLI e sua automação documentada. Codex é o produto e seu ciclo de ferramentas; o modelo configurado, a sessão e o estado do repositório são elementos diferentes que precisam ser registrados.

Como funciona:
- A CLI compõe contexto do projeto e ferramentas com chamadas de modelo; arquivos AGENTS.md fornecem instruções descobertas por escopo.
- codex exec executa uma tarefa sem interface interativa; a opção --json produz eventos JSONL, incluindo conclusão e falha de turno.
- Uma sessão pode ser retomada por identificador explícito, preservando vínculo com a execução anterior sem substituir a verificação do código atual.

Nota de nomenclatura: A documentação consultada informa que --full-auto deixou de ser suportado; não reutilizar flags antigas sem conferir a CLI. Não fixa modelo, plano ou versão instalada.

## R021:C02 — aplicacao

Quando usar:
- Investigação, implementação e revisão de mudanças em repositórios com requisitos e testes claros.
- Pipelines que precisam consumir eventos e artefatos de uma tarefa de programação delimitada.

Quando não usar:
- Para considerar uma mensagem final ou um turno concluído como prova suficiente de aceitação do software.

Implementação proposta:
- Proposta: conferir a CLI instalada, instruções aplicáveis, modelo, diretório e permissões necessárias à missão.
- Usar execução não interativa com registro de eventos, ID de sessão, revisão Git inicial e artefatos produzidos.
- Definir critérios de aceite externos; retomar pelo ID correto, reler mudanças concorrentes e limitar tentativas sem progresso.

Aplicação LAI proposta:
Proposta LAI: integrar Codex como executor de missões de programação com eventos estruturados, mantendo aceitação e continuidade sob controle verificável da aplicação.

## R021:C03 — riscos_validacao

Armadilhas:
- Usar a sessão mais recente em trabalhadores paralelos pode retomar a missão errada; preferir identificação explícita.
- Instruções de projeto não substituem controles de execução; configurações e flags mudam entre versões.

Métricas sugeridas:
- Tarefas aceitas, regressões, custo por alteração, tentativas, falhas de ferramentas e rastreabilidade entre sessão e commit.

Testes propostos:
- Proposta: executar um reparo reproduzível em checkout isolado e verificar testes e diff independentemente da mensagem final.
- Simular duas sessões concorrentes e interrupção; confirmar que a retomada utiliza a missão, o diretório e o estado esperados.

## R021:C04 — perguntas_proveniencia

Pergunta: codex exec cria um serviço durável de workflow?
Resposta: Não por si só. Ele executa a tarefa; persistência operacional, reconciliação e política de retomada precisam de desenho próprio.

Pergunta: Qual evidência comprova a correção?
Resposta: Resultados de verificações relevantes e o estado dos artefatos, vinculados à revisão analisada; a declaração do agente sozinha não basta.

Pergunta: Um evento item.completed encerra necessariamente a tarefa?
Resposta: Não. Concluir um item não substitui o status do turno e a verificação externa dos artefatos.

Pergunta: Por que evitar a sessão implicitamente mais recente?
Resposta: Execuções paralelas podem tornar a escolha ambígua; registre e retome o identificador da missão.

Escopo das fontes:
A inspeção do workspace não localizou CLI ou código local do Codex. Foram lidas páginas oficiais da OpenAI, incluindo redirecionamentos para ChatGPT Learn. Os passos de integração e testes são propostas; nenhuma execução Codex foi realizada.

## R021:C05 — mecanismo_avancado

Na automação do Codex, eventos e resposta final têm contratos distintos. --json produz eventos JSONL; --output-schema define o schema da resposta final, não a validação de todos os eventos. O consumidor distingue itens intermediários, conclusão e falha de turno, preservando eventos desconhecidos para diagnóstico em mudanças de versão. Retomar por ID identifica a conversa; o controlador ainda precisa associá-la ao diretório e à revisão de trabalho. A descoberta de AGENTS.md segue escopos e limites documentados: existir um arquivo no repositório não prova que entrou no contexto daquela execução.

Condição de contorno:
Interromper o processo pode deixar artefatos sem resposta final. Texto válido em stdout não demonstra que o turno ou a tarefa foram aceitos.

Contrato proposto:
- Entradas: Versão da CLI, sessão explícita, diretório, revisão Git, schema final e política de ferramentas.
- Saídas: Log de eventos, resposta final quando disponível e manifesto dos arquivos produzidos.
- Estado: Último evento persistido, status terminal, instruções carregadas e revisão verificada.
- Invariante: Artefatos e evidências ficam vinculados à sessão e ao conteúdo analisado; eventos intermediários não definem sucesso.

Compromissos de projeto:
- JSONL permite acompanhamento incremental, mas exige parser tolerante a evolução e interrupções.
- Schema final facilita integração, porém não comprova correção das mudanças ou completude dos testes.

## R021:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: encerrar uma execução após alteração de arquivo e antes do evento terminal. Exigir estado incompleto; retomar por ID e revalidar a revisão antes de aceitar o resultado.

Plano de avaliação proposto:
Comparar parser incremental com leitura da resposta final em traços controlados de sucesso, falha e truncamento. Medir classificações incorretas, perda de eventos e rastreabilidade; exigir identificação inequívoca do término.

Comparações:
- T235 (complements): O controlador headless transforma eventos e artefatos do executor em estado persistente da missão.
- R027 (complements): A revisão Git identifica o conteúdo; a sessão identifica a conversa e não substitui esse vínculo.

Afirmação rastreável:
--output-schema especifica o formato da resposta final; --json disponibiliza eventos separados em JSONL.
Suporte: direct; fontes: V3C-S039
Limite: A CLI não foi localizada no PATH nesta pesquisa; a análise documental não valida flags em instalação local.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R021:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda os contratos de automação com isolamento reproduzível por tarefa, verificação do artefato final e observabilidade que permite localizar onde o agente perdeu o requisito.

Ambiente identificável
Proposta: associar cada execução a revisão de código, configuração de ferramentas e conjunto de testes. Isolar diretório e recursos por tarefa evita que um resultado aprovado em um ambiente seja atribuído ao código de outro trabalhador. Isso exige controle além da conversa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

Evidência para o agente
Instrumentar comandos e testes com resultados concisos e referências ao trace completo. Dar ao modelo acesso sob demanda à falha relevante reduz a necessidade de despejar logs. A evidência precisa dizer o que foi executado, sobre qual artefato e qual condição falhou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

Conclusão composta
Tratar finalização do turno, término do processo, criação do patch e aceite como estados diferentes. A resposta final é uma declaração do agente; o controlador decide conclusão usando artefato e verificações. Se o processo termina antes do relatório, o resultado permanece desconhecido até reconciliação local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

USO AVANÇADO — Fila de correções independentes
Cenário: Vários bugs podem ser trabalhados em paralelo.
Estratégia: Criar ambiente por tarefa, limitar ferramentas e integrar somente a revisão que passou pelos testes registrados.
Papel do modelo pequeno: No harness próprio, modelo pequeno resolve alteração local; integração continua externa.
Aceite proposto: Nenhum worker modifica base de outro; a árvore integrada é verificada novamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

USO AVANÇADO — Falha de teste com log enorme
Cenário: O agente precisa interpretar uma regressão localizada.
Estratégia: Extrair sumário determinístico e permitir leitura da seção relevante por referência.
Papel do modelo pequeno: 3–14B classifica causa provável e propõe próximo experimento curto.
Aceite proposto: O teste confirmatório diferencia a hipótese de causas alternativas antes de alterar código.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: transferir contratos de ferramenta e evidência ao próprio harness; não equiparar o modelo ao produto Codex.
8–14B: 8–14B: tarefas locais com ambiente reproduzível e execução real de testes.
15–30B: 15–30B: mudanças maiores somente quando orçamento, ferramentas e resultados justificarem.
Requisitos de treino/runtime: Suporte a modelo/backend é propriedade da versão instalada; a ficha não garante compatibilidade de qualquer 3–30B.
Não aplicar quando: Não concluir sucesso apenas porque houve evento final ou JSON válido.

## R021:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Uso interno de Codex confirmado pelo operador.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Relatos OpenAI de uso interno e harness foram consolidados num caso. São referência de sistema real, sem demonstração de paridade de uma LLM pequena.
Consultas registradas: V4C-Q027.

## R021:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R021 → T239 [complements]
Como combinar: Associar cada tarefa a área de trabalho e base verificáveis.
Interface: Task_id, worktree, commit-base e recursos isolados.
Condição: Trabalhadores podem editar simultaneamente.
Aceite proposto: Os testes e o patch referem-se à mesma base e ao mesmo trabalhador.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R021 → T195 [feeds]
Como combinar: Produzir artefato verificável e solicitar execução real do critério.
Interface: Patch, comandos, ambiente e resultados observados.
Condição: Há critério executável para a mudança.
Aceite proposto: Aceite é derivado do resultado registrado, não da narrativa do agente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contabilizar testes descritos como se tivessem sido executados.
- Não afirmar que ambiente isolado elimina dependências externas compartilhadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sistemas na mesma revisão e infraestrutura, registrando tentativas e intervenção humana. O padrão de harness pode ser transferível sem reproduzir capacidades do modelo de referência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T217, T218, T234, T235, T236, T239, R027

## Fontes primárias associadas

### V2B-S013 — Codex CLI

[https://learn.chatgpt.com/docs/codex/cli](https://learn.chatgpt.com/docs/codex/cli)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Inspeção, edição e execução de código no terminal; configuração e composição com scripts.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V2B-S014 — Non-interactive mode

[https://learn.chatgpt.com/docs/non-interactive-mode](https://learn.chatgpt.com/docs/non-interactive-mode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: codex exec, eventos JSONL, identificação e retomada de sessão, configuração explícita e remoção de --full-auto.

Limite: Página oficial consultada após redirecionamento de developers.openai.com. CLI e código Codex não estavam disponíveis no workspace; comandos não foram executados.

### V2B-S015 — Custom instructions with AGENTS.md

[https://learn.chatgpt.com/docs/agent-configuration/agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta e precedência de instruções globais e de projeto no início da execução.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V2A-S005 — Non-interactive mode

[https://developers.openai.com/codex/noninteractive/](https://developers.openai.com/codex/noninteractive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução programática do Codex, retomada de sessão e resultados consumíveis por automações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S017 — Custom instructions with AGENTS.md

[https://developers.openai.com/codex/guides/agents-md/](https://developers.openai.com/codex/guides/agents-md/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta hierárquica de instruções de projeto pelo Codex e limites de carregamento.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R022 — Qwen

**Nome canônico:** Qwen — família de modelos  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R022  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Tongyi Qianwen; família Qwen

## R022:C01 — conceito

Qwen designa uma família de modelos do Qwen Team, Alibaba, com diferentes gerações, tamanhos, modalidades e variantes. O nome sozinho não identifica um checkpoint nem suas capacidades. A documentação diferencia modelos densos, variantes MoE e modos de uso; decisões de implantação precisam partir do identificador e da revisão exatos do modelo escolhido.

Como funciona:
- Pesos e arquitetura determinam o modelo; tokenizer, template de conversa e configuração de geração definem como a aplicação o utiliza.
- Variantes base, instruct e thinking têm objetivos e formatos distintos; controles válidos em uma não são automaticamente válidos em outra.
- Em MoE, parâmetros ativados por token e parâmetros totais são medidas diferentes, relevantes para computação e armazenamento.

Nota de nomenclatura: As páginas consultadas incluem exemplos Qwen3; eles não são declarados como geração mais recente nem como modelo instalado. Nenhum checkpoint do usuário foi inspecionado.

## R022:C02 — aplicacao

Quando usar:
- Avaliação de modelos para geração, programação ou outras modalidades suportadas pelo checkpoint específico.

Quando não usar:
- Para deduzir memória necessária, limite de contexto ou qualidade apenas pela palavra Qwen ou pelo tamanho ativo de um MoE.

Implementação proposta:
- Proposta: registrar model_id, revisão, licença, arquitetura, tokenizer, precisão e quantização do artefato candidato.
- Ler a model card e os requisitos atuais do backend; conferir template, tokens de parada e formato de ferramentas.
- Medir memória para pesos, KV e buffers sob o contexto e a concorrência pretendidos, antes de escolher a configuração.

Aplicação LAI proposta:
Proposta LAI: inventariar primeiro o checkpoint realmente instalado e então escolher as técnicas de inferência aplicáveis; esta ficha não verifica o modelo atual do usuário.

## R022:C03 — riscos_validacao

Armadilhas:
- A mesma família inclui comportamentos diferentes; aplicar um parser de raciocínio ou flag de outra variante pode quebrar a saída.
- Uma receita oficial demonstra uma combinação específica; não comprova compatibilidade com qualquer GPU, versão ou checkpoint local.

Métricas sugeridas:
- Qualidade por tarefa, memória máxima, tempo até primeiro token, latência por token e validade de chamadas estruturadas.

Testes propostos:
- Proposta: testar português, ferramentas, contexto longo e casos sem resposta com a revisão exata selecionada.
- Comparar backend e quantização contra uma referência documentada, mantendo prompts e critérios de avaliação equivalentes.

## R022:C04 — perguntas_proveniencia

Pergunta: Todo Qwen usa o mesmo template e modo de raciocínio?
Resposta: Não. Esses detalhes variam entre gerações e variantes e devem ser conferidos na documentação do checkpoint.

Pergunta: Esta ficha confirma que o modelo cabe na GPU local?
Resposta: Não. Isso exige identificar pesos, formato, backend, contexto, concorrência e memória efetivamente disponível.

Pergunta: Um modelo com poucos parâmetros ativos cabe como um denso desse tamanho?
Resposta: Não necessariamente. Os pesos totais, KV e buffers também ocupam memória.

Pergunta: Que informação falta para escolher a execução?
Resposta: Checkpoint e revisão exatos, hardware, contexto, concorrência e tarefa; o nome da família é insuficiente.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R022:C05 — mecanismo_avancado

Qwen identifica uma família de modelos, não uma configuração única de memória, contexto ou execução. A documentação de conceitos explica nomes que distinguem parâmetros totais e ativos por token em modelos MoE. O número ativo ajuda a interpretar computação, mas não equivale à memória total necessária para hospedar os pesos. Antes de integrar um checkpoint, leia configuração, tokenizer, template e capacidades declaradas para aquela revisão específica.

Condição de contorno:
Não se pode inferir qual modelo está instalado no ambiente do usuário nem concluir que o modelo exemplificado numa página é o mais recente de toda a família.

Contrato proposto:
- Entradas: Identificador e revisão do checkpoint, configuração, tokenizer, template de chat, dtype e limites efetivos do servidor.
- Saídas: Tokens e respostas com template correto, motivo de término, capacidade observada e manifesto de compatibilidade.
- Estado: Arquivos e hashes carregados, parâmetros de geração e adaptações aplicadas pelo servidor.
- Invariante: Toda medição deve permitir reconstruir qual revisão e qual serialização produziram a resposta; nome abreviado sozinho é insuficiente.

Compromissos de projeto:
- MoE pode reduzir computação ativa relativa ao total de parâmetros, mas os pesos e a comunicação continuam relevantes.
- Quantização e offload podem permitir hospedagem menor, com efeitos específicos sobre qualidade e latência a medir.

## R022:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: executar mensagens com papéis e chamadas de ferramenta usando template correto e template incompatível; comparar tokens especiais e validade do resultado, sem atribuir a diferença apenas ao modelo.

Plano de avaliação proposto:
Avaliar o checkpoint candidato no mesmo conjunto de tarefas e orçamento do baseline. Medir memória residente, throughput, cauda de latência e respostas aceitas. Registrar variantes de template e modo de raciocínio quando suportados pelo checkpoint.

Comparações:
- T184 (complements): Alguns checkpoints empregam MoE; a família não é sinônimo dessa arquitetura.
- R023 (complements): Transformers pode carregar checkpoints compatíveis e seus templates.

Afirmação rastreável:
A documentação Qwen diferencia parâmetros totais e ativos na nomenclatura de modelos MoE.
Suporte: direct; fontes: V3D-S009
Limite: Convenção documental; não identifica o modelo local nem garante suporte por todo servidor.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R022:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu identidade exata do checkpoint. Esta camada orienta seleção dentro da família, leitura de parâmetros totais/ativos e validação de modos de geração sem presumir o modelo existente no servidor.

Família e escolha concreta
O lançamento Qwen3 de 2025 fornece exemplos densos e MoE com configurações distintas. Use-o como referência datada, não como catálogo completo ou mais recente de toda a família. Antes de decidir, identifique modalidade, revisão, tamanho total, licença, template e capacidades declaradas do candidato específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

Modos e contrato
Modos de geração e separação de campos internos ou finais podem mudar tokenização, comprimento e tratamento pelo cliente. Valide o template oficial da revisão e a forma de consumir a resposta. Uma aplicação que espera apenas JSON precisa tratar corretamente qualquer região adicional e término, sem assumir que todos os Qwen usam a mesma convenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

Dimensionamento honesto
Qwen3-30B-A3B ilustra a diferença entre total e ativo: computação por token não equivale a memória de pesos. Qwen3-32B denso está fora de uma faixa estrita de até 30B, embora seja próximo numericamente. Não alargue o intervalo solicitado sem declarar essa decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

USO AVANÇADO — Escolher aluno especializado
Cenário: A tarefa tem dados e critérios claros.
Estratégia: Compare candidatos dentro da faixa total desejada com o mesmo acesso a ferramentas e documentos. Avalie base, adaptação e quantização como versões distintas.
Papel do modelo pequeno: Modelos densos 3–7B podem ser candidatos a tarefas estreitas; suporte depende do checkpoint concreto.
Aceite proposto: Medir qualidade por categoria, custo de contexto e comportamento fora do domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

USO AVANÇADO — Escolher MoE para serving
Cenário: A computação ativa parece atraente.
Estratégia: Inspecione pesos totais, roteamento e runtime, depois teste memória e comunicação. Compare com dense que cabe no mesmo orçamento físico.
Papel do modelo pequeno: Um MoE total 15–30B pode ser alternativa, sem ser tratado como dense de poucos bilhões.
Aceite proposto: Atender memória e prazos com qualidade observada, não estimada pelo nome.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Exemplos como Qwen3-4B ilustram a faixa; não confirmam qual versão é adequada ou instalada.
8–14B: Exemplos 8B e 14B permitem estudar especialização, respeitando revisão e template próprios.
15–30B: 30B-A3B exige orçamento de pesos totais; 32B não deve ser contado dentro do limite estrito.
Requisitos de treino/runtime: Modelo e runtime precisam suportar arquitetura, precisão e modo usados. Nenhum checkpoint local foi inspecionado nesta ficha.
Não aplicar quando: Não afirmar compatibilidade com uma GPU ou engine apenas pelo nome Qwen.

## R022:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Fonte oficial identifica a família e seus checkpoints.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q016.

## R022:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R022 → T184 [complements]
Como combinar: Variantes MoE exigem leitura separada de total, ativo e comunicação.
Interface: Configuração do checkpoint e mapas de experts.
Condição: Variante realmente é MoE.
Aceite proposto: Conferir memória física e custo por token.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S009, V4B-S020, V3D-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R022 → R023 [complements]
Como combinar: Transformers fornece classes e templates para checkpoints suportados.
Interface: Revisão, tokenizer e mensagens.
Condição: Versão da biblioteca reconhece o modelo.
Aceite proposto: Comparar tokens serializados e término da geração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S009, V4B-S020, V3D-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar usar nome abreviado como identidade de artefato.
- Não transferir contexto, licença ou formato de uma geração Qwen para outra.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare o checkpoint escolhido em tarefas reais de domínio com fronteira. A família contém modelos distintos; nenhum resultado de um membro prova capacidade de todos os demais.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R009, R011, R023, R024, T085, T086, T133, T184

## Fontes primárias associadas

### V2B-S016 — Key Concepts — Qwen

[https://qwen.readthedocs.io/en/latest/getting_started/concepts.html](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Qwen como família de modelos, variantes, tokenização e distinção entre parâmetros totais e ativos de MoE.

Limite: Página oficial contém exemplos de gerações específicas; não estabelece qual modelo está instalado nem deve ser usada para declarar a geração mais recente.

### V2B-S017 — Quickstart — Qwen

[https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Exemplos de uso com Transformers e serving; templates e modos de raciocínio variam entre variantes Qwen3.

Limite: Receitas de modelos específicos, sem validação no hardware do usuário. Versões e parâmetros dos exemplos não são requisitos universais da família.

### V3D-S009 — Qwen — Key Concepts

[https://qwen.readthedocs.io/en/latest/getting_started/concepts.html](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Nomenclatura de parâmetros totais e ativos em modelos MoE, identidade do checkpoint e formatos de uso.

Limite: Não identifica modelo local nem estabelece qual é o lançamento mais recente de toda a família.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

### V3D-S010 — Transformers — Chat templates

[https://huggingface.co/docs/transformers/main/chat_templating](https://huggingface.co/docs/transformers/main/chat_templating)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Serialização de mensagens, tokens especiais e cuidados para não duplicá-los após aplicar template.

Limite: Página main; confirmar API e template na revisão concreta do modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R023 — Hugging Face Transformers

**Nome canônico:** Hugging Face Transformers — biblioteca de modelos  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R023  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Transformers library; transformers Python

## R023:C01 — conceito

Hugging Face Transformers fornece definições de modelos, tokenizers, preprocessadores e interfaces para inferência e treinamento. A biblioteca permite carregar checkpoints e executar geração, entre outras tarefas. Ela não torna todos os modelos equivalentes: arquitetura, classe carregada, template e revisão dos artefatos continuam determinando o comportamento observado.

Como funciona:
- As classes de modelo executam a arquitetura correspondente ao checkpoint; o tokenizer ou processador converte entradas para os tensores esperados.
- Na conversa, apply_chat_template transforma papéis e mensagens em uma sequência com os marcadores adequados ao modelo.
- A geração combina configuração de amostragem, critérios de parada e cache; cada opção exige suporte da combinação utilizada.

Nota de nomenclatura: Não fixa a versão mais recente como requisito. O uso de outras bibliotecas ou backends precisa ser testado com a mesma revisão de modelo.

## R023:C02 — aplicacao

Quando usar:
- Prototipagem, avaliação controlada de checkpoints e integração direta com modelos.
- Construção de uma referência funcional antes de comparar motores de serving especializados.

Quando não usar:
- Para presumir suporte a uma arquitetura nova apenas porque seus pesos estão disponíveis em um repositório.

Implementação proposta:
- Proposta: fixar versões da biblioteca e revisão de modelo e tokenizer; selecionar a classe compatível com a tarefa.
- Inspecionar os tokens produzidos pelo template e evitar duplicar marcadores especiais na tokenização posterior.
- Definir limites de entrada e saída, dtype, dispositivo e parâmetros de geração; registrar configurações junto aos resultados.

Aplicação LAI proposta:
Proposta LAI: usar Transformers como referência para validar tokenização e comportamento do modelo antes de atribuir diferenças ao vLLM, llama.cpp ou à quantização.

## R023:C03 — riscos_validacao

Armadilhas:
- Duplicar BOS/EOS ou usar template de outro modelo pode degradar a conversa sem gerar erro explícito.
- Documentação de main pode descrever recursos ausentes na versão instalada; um carregamento bem-sucedido não comprova qualidade nem capacidade de servir a carga.

Métricas sugeridas:
- Fidelidade da tokenização, acerto por tarefa, latência, memória máxima e término correto da geração.

Testes propostos:
- Proposta: testar conversa curta, múltiplos turnos, entrada próxima do limite e saída interrompida pelo orçamento.
- Conferir que a avaliação separa texto de entrada e continuação gerada, e que o template coincide com a referência do checkpoint.

## R023:C04 — perguntas_proveniencia

Pergunta: Um template serve para todos os modelos de chat?
Resposta: Não. Os marcadores e a organização esperada pertencem ao treinamento e à configuração de cada modelo.

Pergunta: A documentação main corresponde ao pacote instalado?
Resposta: Não necessariamente. É preciso comparar a versão consultada com a versão e os recursos efetivamente presentes no ambiente.

Pergunta: Por que a mesma lista de mensagens pode gerar outro resultado?
Resposta: Template, tokens especiais e parâmetros podem alterar a sequência efetivamente enviada.

Pergunta: Qual estratégia de cache é sempre melhor?
Resposta: Nenhuma. Escolha conforme memória, compilação, arquitetura, comprimento e custo de transferência medidos.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R023:C05 — mecanismo_avancado

Transformers converte conversas estruturadas em sequências que o modelo realmente consome. Templates diferentes produzem delimitadores e tokens de controle distintos. Formatar uma conversa e depois acrescentar novamente tokens especiais pode introduzir duplicações. A biblioteca também documenta estratégias de KV com diferentes compromissos: crescimento dinâmico, reserva estática, quantização e offload. Compatibilidade depende da classe de modelo e da versão, portanto template e cache devem ser validados como partes separadas da integração.

Condição de contorno:
Documentação main descreve desenvolvimento corrente; não comprova a presença de uma API na versão instalada. Um modelo customizado pode restringir caminhos disponíveis.

Contrato proposto:
- Entradas: Mensagens, tokenizer e template da revisão escolhida, estratégia de cache, parâmetros de geração e orçamento de memória.
- Saídas: IDs de tokens serializados, sequência gerada, consumo de memória e metadados de término.
- Estado: Configuração e objetos de cache pertencentes à sequência, pesos carregados e versão da biblioteca.
- Invariante: Tokens especiais devem aparecer conforme o template, sem duplicação involuntária; cache não pode misturar posições ou sequências incompatíveis.

Compromissos de projeto:
- Cache estático pode facilitar compilação em casos suportados, mas reserva capacidade que talvez não seja usada.
- Offload e quantização reduzem pressão de memória em certos cenários, podendo introduzir transferência ou erro numérico.

## R023:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: comparar os IDs produzidos por serialização única e por caminho que duplica tokens especiais; testar também retomada de cache com posição errada e exigir detecção ou rejeição.

Plano de avaliação proposto:
Fixar versão, pesos e mensagens. Medir qualidade, latência fria e aquecida e memória para estratégias de cache compatíveis. Testar entrada curta, longa e concorrente; não generalizar resultados de uma classe para todas as arquiteturas.

Comparações:
- T081 (complements): A biblioteca oferece mecanismos para armazenar e reutilizar estado KV.
- T140 (complements): Chamadas de ferramenta dependem de uma representação adequada ao modelo.

Afirmação rastreável:
Templates de chat definem a serialização; as estratégias de cache têm compatibilidades e custos distintos.
Suporte: direct; fontes: V3D-S010, V3D-S011
Limite: Documentação consultada na linha main; opções precisam ser confirmadas na versão instalada.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R023:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou templates e estratégias KV. Esta camada incorpora continuous batching documentado atualmente, separação entre geração e agendamento e transição de protótipo para serviço observável.

Biblioteca também evolui no serving
A documentação atual apresenta generate_batch e ContinuousBatchingManager, com configuração de geração e de scheduling separadas. Portanto, a afirmação de que Transformers não oferece batching contínuo seria incorreta. Disponibilidade da API não garante suporte de todas as arquiteturas nem substitui qualificação operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S010, V3D-S011, V4B-S014, V4B-S006.

Configurações com funções distintas
Temperatura e limite de tokens controlam geração; orçamento de tokens, cache e admissão controlam execução. Mantenha essas escolhas em manifests separados e registre valores efetivos. Um ajuste de scheduling não deve alterar silenciosamente a intenção de amostragem ou o limite contratado pelo cliente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S010, V3D-S011, V4B-S014, V4B-S006.

Protótipo para operação
Um exemplo de notebook que gera corretamente não cobre concorrência, cancelamento, pressão de memória e erros. A plataforma Uber usa componentes Transformers em treinamento e serviços associados, mas isso não comprova qualquer combinação de inferência. Construa testes de integração da classe e do modelo realmente usados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S010, V3D-S011, V4B-S014, V4B-S006.

USO AVANÇADO — Protótipo especializado
Cenário: A equipe precisa comparar modelos e ajustes rapidamente.
Estratégia: Use carregamento e tokenização explícitos, inspecione templates e valide respostas. Só depois acrescente batching ou cache adequado, medindo cada mudança.
Papel do modelo pequeno: Um 3–7B permite ciclos de experimento curtos sem dispensar validação final.
Aceite proposto: Reproduzir entrada tokenizada e resultado de tarefa com versões fixadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S010, V3D-S011, V4B-S014, V4B-S006.

USO AVANÇADO — Serviço com concorrência moderada
Cenário: Há interesse em usar recursos atuais da própria biblioteca.
Estratégia: Qualifique ContinuousBatchingManager na arquitetura escolhida, teste cancelamento e limites e compare com outro engine sob carga equivalente.
Papel do modelo pequeno: Um 8–14B pode ser servido se o caminho atende recursos e prazos necessários.
Aceite proposto: Medir fila, conclusão e memória, além da geração de um único pedido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S010, V3D-S011, V4B-S014, V4B-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: A simplicidade de integração pode ser vantagem quando carga e modelo são modestos.
8–14B: Separar configuração de geração e scheduling ajuda a diagnosticar regressões.
15–30B: Modelos 15–30B exigem verificar quantização, distribuição e buffers na classe concreta.
Requisitos de treino/runtime: Biblioteca de modelos, treino e inferência com recursos atuais de serving; suporte é por versão e arquitetura.
Não aplicar quando: Não descrever toda geração via Transformers como serial nem assumir que a API substitui gestão completa de produção.

## R023:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: Transformers integra explicitamente a pilha de treino.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: O recurso faz parte da biblioteca Transformers documentada.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q007, V4B-Q014.

## R023:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R023 → T088 [complements]
Como combinar: A documentação de continuous batching oferece gerenciamento de pedidos ativos.
Interface: Requisições e configuração de agendamento.
Condição: Modelo e backend suportados.
Aceite proposto: Testar entrada, saída e cancelamento de sequências.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S014. Casos: V4B-C013.

2. R023 → T082 [complements]
Como combinar: O caminho documentado inclui cache de prefixos onde suportado.
Interface: Identidade de tokens e configuração de cache.
Condição: Compatibilidade e isolamento confirmados.
Aceite proposto: Medir reúso consumido e evitar mistura de estado.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S014. Casos: V4B-C013.

CONTROLES DE FALHA
- Não duplicar tokens especiais depois de aplicar template.
- Registrar classe carregada e avisos de fallback, não só versão do pacote.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Transformers facilita implementar e comparar modelos. A vantagem frente a fronteira depende da aplicação e do checkpoint; a biblioteca não torna arquiteturas e capacidades equivalentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R022, R009, R024, T081, T085, T089, T177

## Fontes primárias associadas

### V2B-S018 — Transformers

[https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Definições de modelos e interfaces para inferência e treinamento de diferentes modalidades.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V2B-S019 — Chat templates

[https://huggingface.co/docs/transformers/main/chat_templating](https://huggingface.co/docs/transformers/main/chat_templating)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatação de mensagens, apply_chat_template, marcadores de geração e risco de duplicar tokens especiais.

Limite: Página da branch main; conferir a documentação correspondente à versão instalada. Sem avaliação com checkpoint local.

### B-S009 — Generation — GenerationConfig

[https://huggingface.co/docs/transformers/main_classes/text_generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Critérios de parada, limite de novos tokens e semântica específica de early_stopping em beam search.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S010 — Transformers — Chat templates

[https://huggingface.co/docs/transformers/main/chat_templating](https://huggingface.co/docs/transformers/main/chat_templating)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Serialização de mensagens, tokens especiais e cuidados para não duplicá-los após aplicar template.

Limite: Página main; confirmar API e template na revisão concreta do modelo.

### V3D-S011 — Transformers — KV cache strategies

[https://huggingface.co/docs/transformers/main/kv_cache](https://huggingface.co/docs/transformers/main/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estratégias dinâmica, estática, quantizada e offload têm custos e compatibilidades distintos.

Limite: Tabela depende de classes e versões; não é garantia universal de suporte.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R024 — llama.cpp

**Nome canônico:** llama.cpp — inferência em C/C++  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R024  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** llama-server; llama CLI; ggml-org/llama.cpp

## R024:C01 — conceito

llama.cpp é um projeto de inferência em C/C++ para modelos suportados, com execução em CPU e diferentes backends de GPU. Seu ecossistema usa arquivos GGUF e oferece interface de linha de comando e servidor HTTP. Formato de arquivo, método de quantização e motor de execução são escolhas relacionadas, mas representam funções distintas.

Como funciona:
- O runtime carrega pesos e metadados do modelo e executa kernels disponíveis no backend compilado.
- Configurações de precisão, camadas em GPU, contexto e batching afetam memória, latência e capacidade.
- O servidor documenta rotas compatíveis com APIs conhecidas, incluindo geração; isso exige validar o contrato utilizado pela aplicação.

Nota de nomenclatura: Documentação do repositório oficial consultada, sem compilação ou benchmark local. Não afirma compatibilidade do Qwen ou da GPU instalada do usuário.

## R024:C02 — aplicacao

Quando usar:
- Inferência local com modelos compatíveis e necessidade de explorar CPU, GPU ou combinação das duas.
- Comparação de artefatos GGUF quantizados sob restrições reais de memória e carga.

Quando não usar:
- Quando a arquitetura, modalidade ou função necessária não está implementada na revisão escolhida.

Implementação proposta:
- Proposta: fixar revisão do projeto, opções de compilação e backend; registrar identidade e hash dos arquivos do modelo.
- Confirmar arquitetura, tokenizer, template e precisão dos tensores; distinguir conversão de formato de quantização.
- Executar uma configuração mínima e aumentar contexto e concorrência gradualmente, acompanhando memória e qualidade antes de servir a carga.

Aplicação LAI proposta:
Proposta LAI: avaliar llama.cpp como candidato de inferência local para artefatos compatíveis, comparando custo e qualidade com o motor já utilizado.

## R024:C03 — riscos_validacao

Armadilhas:
- Um arquivo GGUF não garante que todo backend suporta sua arquitetura e todas as operações necessárias.
- Offload parcial pode reduzir pressão de VRAM com custo de transferência; throughput e latência precisam ser medidos na carga real.

Métricas sugeridas:
- Memória RAM e VRAM, tempo de prefill, geração por token, qualidade e latência sob concorrência.

Testes propostos:
- Proposta: comparar respostas de avaliação com uma referência do mesmo checkpoint e registrar perdas por quantização.
- Testar no cliente os campos usados, streaming, parada e erro de contexto; conferir que o modelo servido é o solicitado.

## R024:C04 — perguntas_proveniencia

Pergunta: GGUF significa automaticamente modelo de quatro bits?
Resposta: Não. GGUF é um formato que pode armazenar diferentes tipos de tensores; a quantização precisa ser identificada separadamente.

Pergunta: API compatível dispensa teste de integração?
Resposta: Não. Recursos, campos e detalhes de execução variam; o contrato efetivamente usado pela aplicação deve ser verificado.

Pergunta: GGUF identifica a qualidade de uma quantização?
Resposta: Não. É preciso conhecer esquema, modelo de origem e avaliação da variante concreta.

Pergunta: Devo medir apenas tokens por segundo?
Resposta: Não. Inclua prefill, latência de cauda, memória e proporção de respostas aceitas no uso real.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R024:C05 — mecanismo_avancado

llama.cpp inclui um servidor que pode executar modelos compatíveis em CPU e GPU, com diferentes precisões e caminhos de offload. O arquivo GGUF transporta tensores e metadados, porém o formato por si só não assegura que uma arquitetura ou template seja suportado pelo build utilizado. Uma execução reproduzível precisa identificar commit ou versão, hash do modelo, quantização, contexto, distribuição CPU/GPU e parâmetros de concorrência.

Condição de contorno:
Resultados de uma máquina com offload parcial não podem ser extrapolados para outra com pesos inteiramente na GPU; largura de banda, memória e comprimento alteram o gargalo.

Contrato proposto:
- Entradas: Build fixado, GGUF identificado por hash, template de chat, limites de contexto, configuração de offload e requisição.
- Saídas: Texto ou stream, motivo de parada, estatísticas do servidor e uso observado de CPU, GPU e memória.
- Estado: Slots de geração, KV por sequência, modelo carregado e configuração efetiva de batching.
- Invariante: Um slot reutilizado deve preservar apenas estado compatível e autorizado; trocar modelo ou template invalida suposições de equivalência.

Compromissos de projeto:
- Execução local amplia opções de hardware, mas throughput depende fortemente da combinação de pesos e memória.
- Mais paralelismo pode amortizar trabalho ou ampliar disputa por KV; o efeito deve ser medido sob carga.

## R024:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: cancelar uma geração, reutilizar capacidade para outra sessão e verificar ausência de mistura de saída. Repetir com arquivo GGUF ou template incompatível e exigir falha identificável.

Plano de avaliação proposto:
Comparar configurações no mesmo build e checkpoint. Medir prefill, decode, memória, consumo e qualidade em tarefas fixas, mantendo número de tokens comparável. Registrar se medições incluem carregamento inicial e aquecimento.

Comparações:
- T127 (complements): GGUF é um formato usado pelo ecossistema, não uma técnica única.
- R009 (alternative): O papel de servidor pode ser atendido por runtimes com características diferentes.

Afirmação rastreável:
O servidor llama.cpp documenta execução CPU/GPU, geração paralela e batching contínuo.
Suporte: direct; fontes: V3D-S012
Limite: Suporte depende do build, backend e arquitetura; a documentação não equivale a benchmark local.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R024:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu manifesto de build e slots. Esta camada trata distribuição CPU/GPU, concorrência local e seleção de quantização como decisões conjuntas, sem transformar portabilidade em desempenho presumido.

Execução híbrida real
Offload de camadas ou operações muda onde pesos e temporários residem e pode introduzir transferências. Meça CPU, GPU e memória de sistema, incluindo prefill e decode. Um arquivo que cabe em RAM não garante prazo aceitável, e maior uso da GPU não implica automaticamente melhor tempo completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

Slots e concorrência
Slots representam recursos de geração e estado; aumentar quantidade pode elevar throughput ou dividir recursos demais. Teste mistura de contextos e cancelamentos, garantindo limpeza de estado entre pedidos incompatíveis. A configuração deve preservar limites por usuário e não apenas maximizar ocupação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

Build como artefato
Backends e otimizações dependem do build e do dispositivo. Guarde commit, flags relevantes, bibliotecas e hash do GGUF. Ao atualizar, compare tokenização, templates e resultados antes de medir velocidade, porque uma mudança funcional pode parecer melhoria de desempenho por gerar saídas diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

USO AVANÇADO — Aplicação local offline
Cenário: O domínio permite um modelo pequeno com dados locais.
Estratégia: Escolha GGUF suportado, valide template e configure recursos segundo o dispositivo. Use ferramentas determinísticas para operações críticas e mantenha limites de contexto claros.
Papel do modelo pequeno: Um 3–7B pode atender extração ou reescrita estreita sem pressupor conexão externa.
Aceite proposto: Qualidade e tempo medidos no dispositivo, com memória e energia quando relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

USO AVANÇADO — Servidor de equipe pequena
Cenário: Poucos usuários compartilham um host.
Estratégia: Teste slots, batching e offload com chegadas realistas. Inclua pedidos longos que pressionam KV e observe justiça, não apenas throughput médio.
Papel do modelo pequeno: Um 8–14B pode ser adequado se a memória física e o prazo forem suficientes.
Aceite proposto: Respostas completas sem vazamento de estado ou falhas sob concorrência prevista.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Portabilidade e implantação simples podem ser úteis, mas qualidade do checkpoint continua central.
8–14B: Compare quantizações e offload mantendo template e geração fixos.
15–30B: 15–30B pode exigir memória de sistema e transferências que dominam latência; medir antes de escolher.
Requisitos de treino/runtime: Runtime C/C++ com modelos e backends suportados. GGUF não garante arquitetura reconhecida pelo build.
Não aplicar quando: Não apresentar README como prova de uso em bigtech nem compatibilidade de todo modelo ou GPU.

## R024:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C024 — Projeto llama.cpp / llama.cpp server
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: O repositório documenta servidor utilizável e carregamento de modelos GGUF, com recursos de geração e configuração de execução.
Mecanismo documentado: Runtime lê metadados e tensores GGUF e expõe geração por servidor; suporte depende da arquitetura, quantização e build.
Correspondência com esta base: Referência ao runtime llama.cpp.
Transferência proposta para modelo pequeno: Proposta: começar por um modelo 3–7B conhecido, validar template e respostas, depois medir uso de CPU/GPU e memória sob carga.
Limite: README comprova recurso, não cliente de produção. Não confirma compatibilidade do checkpoint ou hardware local; GGUF não designa um único algoritmo de quantização.
Fontes: V3D-S012, B-S037.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q026.

## R024:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R024 → T127 [requires]
Como combinar: GGUF fornece tensores e metadados usados pelo runtime.
Interface: Arquivo identificado e capacidades do leitor.
Condição: Arquitetura e tipos de tensor suportados.
Aceite proposto: Inspecionar metadados e comparar tokenização.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S012, V2B-S020, B-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R024 → T087 [complements]
Como combinar: Batching e slots devem ser avaliados como política de concorrência do servidor.
Interface: Pedidos ativos e orçamento de contexto.
Condição: Configuração suporta a carga pretendida.
Aceite proposto: Medir fila, memória e cancelamento efetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S012, V2B-S020, B-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar se a atualização mudou defaults ou template.
- Não confundir tamanho do arquivo com consumo total durante geração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a solução local com fronteira em tarefas delimitadas e incluindo custo operacional. llama.cpp amplia opções de execução; não assegura paridade cognitiva ou latência por si só.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T086, T088, T121, T127, R009, R022, R023

## Fontes primárias associadas

### V2B-S020 — llama.cpp — LLM inference in C/C++

[https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Motor C/C++, backends CPU/GPU, inferência híbrida e opções de quantização.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V2B-S021 — LLaMA.cpp HTTP Server

[https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Servidor HTTP, batching, rotas compatíveis, opções de modelo e configuração de contexto.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### B-S037 — GGUF specification

[https://github.com/ggml-org/ggml/blob/master/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formato binário de modelos, tensores e metadados; não é por si só um algoritmo de quantização.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S012 — llama.cpp HTTP server — README

[https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Servidor com caminhos CPU/GPU, geração paralela e batching contínuo.

Limite: Arquivo master; recursos dependem do build, backend e arquitetura do modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R025 — XGrammar

**Nome canônico:** XGrammar — motor de geração estruturada  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R025  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** xgrammar; XGrammar constrained decoding

## R025:C01 — conceito

XGrammar implementa geração estruturada por restrições durante a decodificação. A biblioteca compila descrições como JSON Schema ou gramáticas e calcula quais tokens podem continuar a saída. Ela atua no processo de amostragem, não apenas na validação do texto pronto. A estrutura admitida continua diferente da correção factual e das regras de negócio.

Como funciona:
- A gramática compilada depende da configuração de tokenização e pode ser compartilhada entre solicitações compatíveis.
- Cada solicitação mantém seu próprio GrammarMatcher; uma máscara remove tokens inválidos dos logits antes da amostragem.
- Após aceitar o token escolhido, o matcher avança; a condição de término precisa respeitar o estado da geração estruturada.

Nota de nomenclatura: Não promete suporte a toda construção de schema ou a qualquer checkpoint. Nenhum backend foi configurado ou testado nesta entrega.

## R025:C02 — aplicacao

Quando usar:
- Extração, contratos de ferramentas e respostas estruturadas quando o runtime oferece integração compatível.

Quando não usar:
- Para comprovar verdade, autorização ou relações semânticas que não estão expressas e verificadas no contrato.

Implementação proposta:
- Proposta: escolher um schema pequeno e registrar sua versão junto ao tokenizer e ao modelo.
- Usar a integração do backend ou conectar compilação, máscara e atualização de estado a cada passo de geração.
- Manter estado separado por solicitação, rejeitar gramáticas incompatíveis e validar o objeto completo com um validador independente.

Aplicação LAI proposta:
Proposta LAI: avaliar XGrammar para contratos estruturados do executor e extrações do RAG; verificar conteúdo, identificadores e evidências após a geração.

## R025:C03 — riscos_validacao

Armadilhas:
- Compartilhar um matcher mutável entre usuários pode contaminar o estado; compartilhar somente a gramática compilada apropriada.
- Interromper pelo limite de tokens pode deixar um prefixo válido e uma saída incompleta; não tratá-la como objeto final aceito.

Métricas sugeridas:
- Validade sintática, conformidade ao schema, conclusão íntegra, latência de compilação e impacto no tempo por token.

Testes propostos:
- Proposta: testar objetos aninhados, Unicode, campos obrigatórios, restrições impossíveis e orçamento insuficiente de saída.
- Misturar solicitações com schemas diferentes no mesmo lote e verificar isolamento, término e rejeição de tokens inadmissíveis.

## R025:C04 — perguntas_proveniencia

Pergunta: JSON válido significa resposta correta?
Resposta: Não. O objeto pode cumprir a estrutura e ainda conter valores falsos ou incompatíveis com a evidência.

Pergunta: Basta escrever uma gramática no prompt?
Resposta: Não. A restrição precisa ser implementada pelo backend durante a decodificação; o prompt também deve explicar o conteúdo esperado.

Pergunta: Posso compartilhar o mesmo matcher entre pedidos?
Resposta: Não como estado mutável único: cada sequência precisa de seu próprio progresso gramatical.

Pergunta: JSON válido prova resposta correta?
Resposta: Não. Sintaxe, regras de domínio e correspondência com evidência precisam de verificações distintas.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R025:C05 — mecanismo_avancado

Na integração do XGrammar, informação do tokenizer, compilador e gramática compilada podem ser preparados para reúso apropriado. O estado do matcher acompanha a sequência de cada requisição: gerar máscara, aplicá-la aos logits antes de amostrar e aceitar o token escolhido são etapas distintas. Em lotes, a linha da máscara precisa corresponder à requisição correta. Rollback especulativo exige manter estado gramatical e sequência de tokens coerentes.

Condição de contorno:
Restringir tokens à linguagem aceita não verifica fatos, autorização ou regras de negócio externas. Uma saída interrompida por orçamento pode continuar incompleta mesmo com prefixo gramatical válido.

Contrato proposto:
- Entradas: Tokenizer compatível, gramática ou schema suportado, logits da etapa e estado de cada sequência ativa.
- Saídas: Máscara de tokens permitidos, decisão amostrada e estado atualizado ou término reconhecido.
- Estado: Artefato compilado reutilizável e matcher específico por sequência, com associação estável à posição do lote.
- Invariante: Cada token confirmado deve avançar exatamente o matcher correspondente; token descartado por rollback não pode permanecer aceito.

Compromissos de projeto:
- Compilação reutilizável amortiza custo, mas requer chave que identifique gramática e tokenizer.
- Restrições reduzem saídas malformadas, enquanto schemas complexos ou incompatíveis ampliam custo e risco de integração.

## R025:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: permutar requisições no lote e rejeitar um ramo especulativo; verificar que máscaras e histórico do matcher acompanham a sequência correta, sem contaminar a vizinha.

Plano de avaliação proposto:
Comparar geração livre com validação posterior e geração restrita, mantendo modelo e tarefas. Medir validade completa, acerto semântico, latência de compilação, latência por token e interrupções. Separar primeira compilação de uso aquecido.

Comparações:
- T196 (specializes): Implementa restrição gramatical durante a decodificação.
- T197 (complements): Validação posterior continua verificando o objeto completo e regras adicionais.

Afirmação rastreável:
A integração usa máscara antes da amostragem e estado de matcher associado à sequência.
Suporte: direct; fontes: V3D-S013
Limite: A documentação de integração não garante suporte irrestrito a todo schema ou backend.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R025:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou matcher por sequência e rollback. A nova camada usa structural tags e modos de chamada de ferramenta para desenhar contratos mistos, com testes de fronteiras e custos de compilação.

Programa de saída
Structural tags permitem especificar regiões livres e estruturadas no fluxo. Modele transições entre explicação e objeto de ferramenta, em vez de aplicar uma restrição genérica a toda a resposta. Delimitadores precisam corresponder ao template do modelo e às regras do consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

Modos de ferramenta
A documentação distingue escolhas como automático, obrigatório, ferramenta forçada e ausência de chamada, conforme integração. O contrato deve refletir o modo realmente solicitado. Forçar uma ferramenta não demonstra que ela é apropriada para a intenção; seleção semântica e autorização continuam externas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

Compilação e reúso
Gramáticas compiladas podem ser reutilizadas quando tokenizer e contrato são compatíveis, mas matcher continua pertencendo à sequência. Meça compilação e cache em schemas dinâmicos. Um catálogo com muitas variações pode consumir memória e introduzir latência inicial que não aparece em benchmark com gramática já pronta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

USO AVANÇADO — API de domínio
Cenário: O agente deve escolher uma ferramenta e preencher argumentos.
Estratégia: Use modo e tags compatíveis, compile schemas conhecidos e valide objeto completo antes de executar. Teste quando a resposta correta é não chamar ferramenta.
Papel do modelo pequeno: Um 3–7B pode preencher contratos estreitos com menos erros de sintaxe.
Aceite proposto: Medir escolha correta, argumentos corretos e validade estrutural separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

USO AVANÇADO — Texto com trecho estruturado
Cenário: A aplicação precisa exibir explicação e consumir um objeto.
Estratégia: Defina fronteiras inequívocas e teste tokens que incluem vários caracteres estruturais. Confirme conclusão e parser antes de liberar o objeto ao consumidor.
Papel do modelo pequeno: Um 8–14B pode produzir resposta mista mantendo o controle do fluxo.
Aceite proposto: Nenhum fragmento livre interpretado como ação e nenhuma estrutura parcial aceita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Schemas simples tornam a restrição útil sem sobrecarregar contexto ou compilação.
8–14B: Teste tags e modos próprios do checkpoint; o mesmo desenho textual pode tokenizar diferente.
15–30B: Modelos maiores não eliminam necessidade de matcher correto em lotes e especulação.
Requisitos de treino/runtime: Biblioteca integrada ao loop de amostragem; exige suporte do engine e do tokenizer, sem treino obrigatório.
Não aplicar quando: Não supor suporte integral a todo JSON Schema nem equivalência de templates entre famílias.

## R025:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: É a implementação XGrammar documentada.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013.

## R025:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R025 → T196 [feeds]
Como combinar: XGrammar implementa máscaras e estados para geração restringida.
Interface: Gramática compilada, matcher e logits.
Condição: Integração respeita sequência e rollback.
Aceite proposto: Testar prefixos, conclusão e tokens proibidos.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S015, V4B-S016. Casos: V4B-C014.

2. R025 → T197 [complements]
Como combinar: Validação final cobre contrato completo e diferenças de recursos suportados.
Interface: Objeto e schema versionado.
Condição: Dialeto e limites conhecidos.
Aceite proposto: Rejeitar saída truncada e campos semanticamente inválidos em camada própria.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S013, V4B-S015, V4B-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não compartilhar matcher mutável entre sequências concorrentes.
- Invalidar cache de gramática quando tokenizer ou contrato muda.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
XGrammar pode melhorar confiabilidade de interface de um modelo pequeno. Compare campos corretos e decisões de ferramenta; estrutura garantida não equivale a competência geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T141, T196, T197, R009, R011, R023, R026

## Fontes primárias associadas

### V2B-S022 — XGrammar — Quick Start

[https://xgrammar.mlc.ai/docs/latest/start/quick_start.html](https://xgrammar.mlc.ai/docs/latest/start/quick_start.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compilação de gramáticas, JSON Schema, tokenizer e integração de geração restrita.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V2B-S023 — XGrammar — Integration with LLM Engine

[https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html](https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramática compartilhável, matcher por solicitação, máscaras de tokens, aceitação e término.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V3D-S013 — XGrammar — Engine integration

[https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html](https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos de tokenizer, compilação, matcher por sequência e máscara antes da amostragem.

Limite: Integração exige sincronização com a sequência; restrição sintática não comprova correção semântica.

### V4B-S015 — Structural Tag Usage — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de formatos, tags, regiões livres/estruturadas e delimitadores de tokens.

Limite: Restrições formais não validam autorização, conteúdo factual nem sucesso de ferramenta.

### V4B-S016 — Tool Calling and Reasoning — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas específicas de formato de modelo e escolhas auto/required/forced/none para chamadas de ferramenta.

Limite: Lista de estilos não verifica checkpoint do usuário; interoperabilidade precisa ensaio por tokenizer e backend.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R026 — Guidance

**Nome canônico:** Guidance — programação controlada de geração  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R026  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** guidance Python; Guidance library

## R026:C01 — conceito

Guidance é uma biblioteca para combinar texto de prompt, geração e controle de fluxo em programas Python. Ela permite construir saídas por partes e impor restrições conforme o backend, incluindo seleção entre alternativas e geração JSON. O suporte efetivo depende do provedor e da integração; a biblioteca não transforma qualquer endpoint em um decodificador plenamente controlável.

Como funciona:
- Um objeto de modelo acumula contexto e campos gerados que o programa pode consultar por nome.
- select restringe a escolha a alternativas; gen produz segmentos conforme opções disponíveis; o código Python decide as próximas operações.
- guidance.json aceita schema ou modelos compatíveis, mas sua documentação informa suporte parcial a construções de JSON Schema.

Nota de nomenclatura: Limitações de JSON Schema são atribuídas à API documentada, não à impossibilidade teórica de representar toda restrição em qualquer sistema.

## R026:C02 — aplicacao

Quando usar:
- Classificação com rótulos fechados, extração estruturada e fluxos pequenos que combinam geração com lógica determinística.

Quando não usar:
- Quando as restrições necessárias não são suportadas pelo backend ou quando um parser determinístico já resolve a tarefa.

Implementação proposta:
- Proposta: selecionar o backend e verificar suas capacidades antes de definir a gramática ou formato esperado.
- Começar por uma seleção pequena, incluindo opção para evidência insuficiente; capturar campos gerados sem depender de posições textuais frágeis.
- Adicionar schema e validação semântica externa; registrar prompt, modelo, programa e parâmetros para reproduzir os testes.

Aplicação LAI proposta:
Proposta LAI: comparar Guidance com geração estruturada nativa em uma rotina de classificação ou extração da Helena, mantendo critérios de negócio fora do texto gerado.

## R026:C03 — riscos_validacao

Armadilhas:
- Um exemplo funcional com modelo local não demonstra os mesmos recursos em uma API remota.
- Um campo bem formatado ainda pode representar decisão errada; suporte parcial de schema exige verificar cada restrição usada.

Métricas sugeridas:
- Acurácia dos rótulos, conformidade estrutural, rejeições semânticas, latência e tokens usados por decisão aceita.

Testes propostos:
- Proposta: testar alternativas parecidas, ausência de evidência e entradas que tentam induzir rótulos fora do conjunto.
- Validar strings com escapes, objetos aninhados, limites de saída e regras numéricas no validador externo, identificando falhas de conteúdo separadamente.

## R026:C04 — perguntas_proveniencia

Pergunta: Guidance tem as mesmas capacidades em todos os modelos?
Resposta: Não. A documentação distingue o suporte por backend; cada combinação precisa ser verificada.

Pergunta: Uma escolha forçada entre rótulos garante classificação correta?
Resposta: Não. Ela garante um formato admissível quando suportada, mas ainda exige avaliar se o rótulo corresponde à entrada.

Pergunta: Se o programa aceitou o schema, todas as regras foram garantidas?
Resposta: Não presuma isso; confira suporte documentado e valide o objeto final com o contrato da aplicação.

Pergunta: Como tratar uma captura interrompida?
Resposta: Preserve o estado de incompletude, descarte uso operacional e decida entre retry limitado ou erro explícito.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R026:C05 — mecanismo_avancado

Guidance combina fluxo de programa e geração controlada, com capacidades que variam conforme o backend. A documentação de JSON explicita limitações de suporte a recursos do schema; não se deve presumir equivalência integral entre uma restrição declarada e a validação completa do objeto. O contrato da aplicação precisa verificar a saída terminada, inclusive regras que o mecanismo de geração não consegue impor naquele provedor.

Condição de contorno:
Um programa que funciona com controle local de logits pode não ter as mesmas capacidades numa API remota. Compatibilidade deve ser testada no backend realmente selecionado.

Contrato proposto:
- Entradas: Programa Guidance, backend, modelo, schema ou escolhas permitidas e limite de geração.
- Saídas: Capturas nomeadas, texto produzido, estado final e resultado de validação posterior do objeto completo.
- Estado: Modelo e configuração de execução, progresso das capturas e artefatos necessários ao programa.
- Invariante: Uma captura parcial ou uma restrição não suportada não pode ser promovida silenciosamente a resultado validado.

Compromissos de projeto:
- Controle programático torna o formato mais previsível, mas adiciona acoplamento às capacidades do provedor.
- Validar novamente custa trabalho, porém detecta lacunas de schema e regras de negócio que a geração não cobre.

## R026:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: exigir uma restrição de schema fora do subconjunto suportado e interromper outra geração no limite; confirmar que ambos os casos recebem diagnóstico explícito antes de qualquer consumo transacional.

Plano de avaliação proposto:
Fixar modelo, backend e tarefas. Comparar geração livre, Guidance e restrição nativa do servidor quanto a validade completa, semântica, tempo e custo. Incluir casos numéricos, objetos aninhados e truncamento, sem considerar apenas exemplos que terminam corretamente.

Comparações:
- T196 (complements): Pode utilizar restrições de geração conforme o backend.
- R025 (alternative): São ferramentas distintas; comparar capacidade concreta, não apenas o objetivo de estruturação.

Afirmação rastreável:
A documentação Guidance informa diferenças entre backends e limitações de suporte a JSON Schema.
Suporte: direct; fontes: V3D-S014, V3D-S015
Limite: As limitações são dependentes da versão; valide o subconjunto necessário ao aplicativo.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R026:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou diferenças de backend e captura parcial. A nova camada explica token healing, composição de trechos e validação de programas que intercalam texto fixo com geração.

Fronteira de tokens
Token healing recua na fronteira de tokenização para permitir continuações compatíveis com o prefixo textual. Isso trata um efeito de segmentação, não autoriza alterar significado do texto fornecido. O mecanismo depende de controle do backend; não presuma que qualquer endpoint remoto permite a mesma operação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

Fluxo programático
Um programa Guidance mistura texto fixo, escolhas e capturas. Defina quais partes são dados e quais controlam o fluxo, mantendo valores externos sem reinterpretá-los como instruções do programa. A execução deve registrar capturas concluídas e interrupções para que um consumidor não use um objeto incompleto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

Portabilidade por capacidade
Backends locais e remotos oferecem graus diferentes de controle. Crie uma matriz das operações realmente suportadas, incluindo restrições JSON e geração por partes. Se um recurso não existe, escolha uma alternativa explícita e reavalie o contrato; não simule sucesso com prompting que apenas pede o formato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

USO AVANÇADO — Formulário com campos controlados
Cenário: A aplicação alterna valores fixos e texto gerado.
Estratégia: Use capturas nomeadas, escolhas fechadas quando adequadas e validação final. Teste fronteiras de tokens e encerramento por orçamento, preservando campos já determinados.
Papel do modelo pequeno: Um 3–7B pode completar estruturas estreitas com controle programático.
Aceite proposto: Objeto completo, campos corretos e ausência de alterações indevidas em texto fixo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

USO AVANÇADO — Prototipar geração composta
Cenário: Há dúvida entre programa segmentado e resposta única.
Estratégia: Implemente ambas as alternativas no mesmo backend e compare custo, qualidade e clareza do contrato. Inclua o custo de chamadas adicionais e de prefixos repetidos.
Papel do modelo pequeno: Um 8–14B pode resolver tarefas compostas, se a segmentação não remover dependências necessárias.
Aceite proposto: Medir sucesso da tarefa e manutenção do programa, não só JSON válido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Programas curtos e escolhas explícitas podem reduzir exigência de geração livre.
8–14B: Segmentação ajuda controle, mas deve preservar contexto relevante entre partes.
15–30B: Em 15–30B, chamadas adicionais podem dominar custo; compare com geração única restrita.
Requisitos de treino/runtime: Biblioteca de controle em Python; capacidades dependem do backend e da versão, sem promessa universal de token healing remoto.
Não aplicar quando: Não confundir controle de fluxo com verificação de fatos ou com atualização dos pesos.

## R026:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C015 — Guidance / Guidance — geração programática
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.
Mecanismo documentado: Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.
Correspondência com esta base: É o comportamento documentado da biblioteca Guidance.
Transferência proposta para modelo pequeno: Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.
Limite: Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.
Fontes: V4B-S030, V3D-S015, V3D-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q021.

## R026:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R026 → T196 [complements]
Como combinar: Restrições de geração podem ser usadas onde o backend oferece controle suficiente.
Interface: Prefixo, captura e restrição suportada.
Condição: Contrato não depende de recurso indisponível.
Aceite proposto: Testar saídas impossíveis, término e fronteiras de tokens.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S014, V3D-S015, V4B-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R026 → T197 [requires]
Como combinar: Objeto gerado precisa de validação completa após a captura.
Interface: JSON concluído e schema do consumidor.
Condição: Dialeto e recursos conhecidos.
Aceite proposto: Distinguir erro de estrutura, regra de negócio e falta de conclusão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S014, V3D-S015, V4B-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não promover uma captura parcial a resultado válido.
- Verificar que texto fixo permanece exatamente conforme o contrato após token healing.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Guidance pode organizar uma aplicação pequena e reduzir erros de interface. A comparação com fronteira deve avaliar a tarefa e o custo do programa completo, sem inferir inteligência do grau de controle.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T134, T140, T141, T196, T197, R023, R024, R025

## Fontes primárias associadas

### V2B-S024 — Introduction to guidance

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de contexto, select, captura de variáveis e controle Python; suporte de restrições depende do backend.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V2B-S025 — guidance.json

[https://guidance.readthedocs.io/en/latest/generated/guidance.json.html](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração JSON com schema ou modelos tipados e limites declarados de cobertura de JSON Schema.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V3D-S014 — Guidance — guidance.json

[https://guidance.readthedocs.io/en/latest/generated/guidance.json.html](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contrato da geração JSON e limitações de suporte a recursos de JSON Schema.

Limite: Suporte depende da versão; saída final e regras de domínio precisam de validação própria.

### V3D-S015 — Guidance — Introduction

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo programático e diferenças de capacidade entre backends locais e remotos.

Limite: Compartilhamento interno de recursos não implica fronteira de segurança ou equivalência de provedores.

### V4B-S030 — Token healing — Guidance

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de fronteiras de tokenização por recuo e prefixo restrito; integração documentada com LlamaCpp/Transformers.

Limite: Exemplos não comprovam qualidade de domínio nem implementação eficiente em todo provedor remoto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# R027 — Git

**Nome canônico:** Git — controle distribuído de versões  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R027  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Git version control; controle de versões com Git

## R027:C01 — conceito

Git organiza versões de arquivos em objetos e commits que registram snapshots, pais e metadados. O histórico permite comparar mudanças, relacionar decisões à revisão de código e reconstruir arquivos versionados. Em agentes de programação, isso fornece uma base verificável para checkpoints de código, sem capturar automaticamente bancos, serviços externos ou estado de execução.

Como funciona:
- Blobs representam conteúdo; árvores organizam caminhos; commits apontam para uma árvore e para seus ancestrais.
- Branches identificam linhas de trabalho; diffs mostram alterações entre versões ou entre o estado de trabalho e uma referência.
- Worktrees permitem diretórios de trabalho separados vinculados ao mesmo repositório, úteis para missões paralelas.

Nota de nomenclatura: Referência ao Git, sem confundir com um serviço específico de hospedagem. Nenhum commit, branch ou worktree do usuário foi criado ou alterado.

## R027:C02 — aplicacao

Quando usar:
- Rastreamento de código, instruções, memória textual e artefatos pequenos que precisam de comparação por versão.

Quando não usar:
- Como único mecanismo de recuperação de processos, confirmação de operações externas ou preservação de arquivos não incluídos no commit.

Implementação proposta:
- Proposta: registrar a revisão inicial e as alterações existentes antes de iniciar uma missão.
- Usar branch e worktree por mudança independente; revisar o diff e adicionar explicitamente os arquivos que compõem cada etapa.
- Criar commits coerentes com evidências de verificação; guardar referências externas de testes e confirmar sincronização quando recuperação remota for necessária.

Aplicação LAI proposta:
Proposta LAI: vincular missões, patches e resultados de validação a revisões Git; usar esse vínculo para retomar trabalho e comparar mudanças sem depender somente do histórico conversacional.

## R027:C03 — riscos_validacao

Armadilhas:
- Um commit pode conter código incorreto; hash e histórico identificam conteúdo, não comprovam comportamento.
- Integrar sem conflito textual não garante compatibilidade semântica; recursos externos usados por worktrees podem continuar compartilhados.

Métricas sugeridas:
- Rastreabilidade entre tarefa e commit, alterações indevidas, conflitos de integração e sucesso da reconstrução de uma revisão.

Testes propostos:
- Proposta: reconstruir o projeto pela revisão registrada em diretório separado e executar verificações relevantes.
- Integrar mudanças paralelas com interação funcional conhecida e conferir testes; testar recuperação incluindo os artefatos externos necessários.

## R027:C04 — perguntas_proveniencia

Pergunta: Commit é um snapshot completo do agente?
Resposta: Não. Ele representa arquivos versionados e metadados; conversa, memória volátil e efeitos externos exigem mecanismos próprios.

Pergunta: Worktrees impedem todos os conflitos entre agentes?
Resposta: Não. Isolam diretórios de trabalho, mas alterações ainda precisam ser integradas e serviços ou recursos externos podem continuar compartilhados.

Pergunta: Mesmo conteúdo implica mesmo commit?
Resposta: Não. Pais e metadados também compõem o commit; compare árvores quando a questão for conteúdo.

Pergunta: Testar o working tree valida um commit parcialmente staged?
Resposta: Somente se os conteúdos coincidirem. Verifique a árvore candidata ou teste um checkout construído a partir dela.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R027:C05 — mecanismo_avancado

Git separa objetos imutáveis de referências mutáveis. Uma árvore identifica conteúdo e caminhos; um commit acrescenta pais e metadados, então commits diferentes podem apontar à mesma árvore. Publicar uma etapa envolve mover uma referência para o commit validado, operação diferente de construir objetos. git update-ref aceita o valor anterior esperado, permitindo rejeitar publicação quando outro processo moveu a referência. Transações com várias referências validam e bloqueiam atualizações, mas leitores concorrentes podem observar um subconjunto das mudanças. Essa propriedade não deve ser ampliada para um snapshot global de leitura.

Condição de contorno:
O commit normalmente usa o índice; com staging parcial, o conteúdo commitado pode diferir do diretório testado. Nenhum hash demonstra correção funcional.

Contrato proposto:
- Entradas: Árvore validada, commit candidato, referência de destino e identificador anterior esperado.
- Saídas: Nova referência confirmada ou conflito explícito sem sobrescrever trabalho concorrente.
- Estado: Índice, working tree, objetos e referências registrados separadamente.
- Invariante: A revisão publicada corresponde ao conteúdo validado; atualização concorrente força reconciliação.

Compromissos de projeto:
- Publicação condicional evita perda silenciosa, mas requer resolver conflitos de evolução legítimos.
- Commits pequenos melhoram rastreabilidade, porém testes precisam acompanhar a composição final das etapas.

## R027:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: validar um commit e mover a referência por outro processo antes da publicação. Exigir falha da atualização condicional; repetir com staging parcial e detectar divergência entre árvore testada e publicada.

Plano de avaliação proposto:
Comparar publicação direta com condicional sob concorrência controlada. Medir sobrescritas, conflitos corretamente detectados e divergências de conteúdo; aceitar somente estratégia que preserve histórico e vínculo de validação.

Comparações:
- T236 (complements): Commit por etapa precisa garantir que o índice representa a etapa testada, além de registrar mensagem.
- T239 (complements): Worktrees separam índices e diretórios, mas compartilham objetos e várias referências do repositório.

Afirmação rastreável:
git update-ref pode exigir correspondência com o objeto anterior; atualizar várias referências não garante visão conjunta atômica para todo leitor concorrente.
Suporte: direct; fontes: V3C-S037
Limite: A atomicidade descrita não cobre arquivos externos, serviços ou validação semântica do commit.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R027:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a identidade de commits com atestação da árvore efetivamente testada, integração concorrente e vínculo entre código, modelo e medições.

Teste ligado à árvore
Proposta: registrar hash da árvore, dependências relevantes e configuração de teste no resultado. Se qualquer entrada muda após o teste, a evidência deixa de autorizar promoção. O commit preserva uma versão; não prova que essa versão é exatamente a que foi exercitada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

Integração concorrente
Validar cada candidato em isolamento e depois validar a composição. Dois patches corretos na mesma base podem interagir ao serem unidos. A atualização final de referência usa revisão esperada e o controlador trata rejeição concorrente como necessidade de reintegração, não como retry cego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

Experimento versionado
Vincular revisão de código, checksum de pesos/adaptador, política de prompt e dataset ao relatório de desempenho. Grandes artefatos podem permanecer fora do repositório, identificados por manifestos. Reverter código sem reverter configuração do modelo pode não restaurar o comportamento observado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

USO AVANÇADO — Integração de agentes de código
Cenário: Dois trabalhadores mudam módulos relacionados.
Estratégia: Criar candidatos isolados, verificar contratos locais e executar testes de interação sobre a árvore combinada.
Papel do modelo pequeno: Modelos pequenos produzem mudanças estreitas; Git e CI preservam identidade e promoção.
Aceite proposto: Uma mudança concorrente de base invalida o aceite antigo e exige nova verificação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

USO AVANÇADO — Comparação de sistemas 3–30B
Cenário: Experimento mistura alterações de prompt, quantização e retrieval.
Estratégia: Congelar manifestos por condição e separar ablações em revisões identificáveis.
Papel do modelo pequeno: O modelo é objeto do experimento; não decide qual revisão foi executada.
Aceite proposto: Reproduzir o relatório a partir dos manifestos ou registrar precisamente a dependência indisponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: editar unidades pequenas com diffs legíveis; versionamento não compensa raciocínio insuficiente.
8–14B: 8–14B: refatorações locais com integração validada por árvore.
15–30B: 15–30B: alterações maiores continuam exigindo controles de concorrência e evidência.
Requisitos de treino/runtime: Git atua sobre artefatos; não requer treino nem conhece semântica da tarefa.
Não aplicar quando: Não armazenar volumes ilimitados de traces ou pesos no Git apenas porque o repositório aceita arquivos.

## R027:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: O operador confirma migração e uso de Git.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Git e worktrees sustentam o ambiente.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: Fonte descreve um sistema de versionamento relacionado e diferenças para Git, não adoção interna integral de Git.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Sistema substituiu Git naquele ambiente; não comprova comportamento Git atual.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Clonagem, commits e pull requests compõem o fluxo documentado.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Windows/Git, GitHub e Codex fornecem evidências delimitadas. Sapling e Scion mantêm mapeamentos de família/analogia quando o mecanismo Git não está comprovado.
Consultas registradas: V4C-Q015, V4C-Q016, V4C-Q011.

## R027:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R027 → T239 [complements]
Como combinar: Isolar candidatos e conservar a identidade de suas bases.
Interface: Worktree, tarefa e commit-base.
Condição: Há edição concorrente.
Aceite proposto: Nenhum índice ou diretório de um trabalhador contamina o candidato de outro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R027 → T233 [complements]
Como combinar: Invalidar a aprovação quando a árvore do candidato muda.
Interface: Tree_hash, ambiente de teste e revisão esperada da referência.
Condição: Uma alteração será integrada.
Aceite proposto: Só a árvore verificada é promovida, com nova validação após composição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir Sapling/Piper com Git por oferecerem operações semelhantes.
- Não interpretar hash ou assinatura como prova de correção funcional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar taxa de mudanças aceitas e custo de integração, incluindo conflitos. Controle de versão é infraestrutura comum aos modelos comparados, não uma vantagem paramétrica.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T061, T072, T076, T229, T233, T236, T239, R013

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2B-S026 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho ligadas ao mesmo repositório e organização de branches em diretórios separados.

Limite: Manual oficial consultado; não descreve isolamento de serviços externos nem garante correção de merges. Nenhum worktree do usuário foi alterado.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S036 — Git — git-commit

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Commit usual registra o índice; opções com paths e seleção parcial mudam quais alterações são incluídas.

Limite: Commit não captura por si arquivos ignorados, banco de dados, processos ou efeitos externos.

### V2A-S019 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho associadas a um mesmo repositório.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
