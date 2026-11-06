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
