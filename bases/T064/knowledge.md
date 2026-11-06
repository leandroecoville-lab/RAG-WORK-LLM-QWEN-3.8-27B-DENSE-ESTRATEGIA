# T064 — Persistent Agent State

**Nome canônico:** Persistent Agent State  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T064  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** estado persistente de agente

## T064:C01 — conceito

Estado de execução do agente que sobrevive a chamadas, sessões e reinícios: missão, etapa, valores intermediários, ações pendentes e referências. É distinto de conhecimento geral do agente. Persistir texto de conversa sem controle de execução pode ser insuficiente para retomar corretamente.

Como funciona:
- Modelar os campos necessários à próxima transição.
- Gravar mudanças confirmadas com identidade e versão.
- Recarregar e reconciliar o estado antes de continuar.

## T064:C02 — aplicacao

Quando usar:
- Missões duráveis e workflows com ferramentas.
- Retomada após crash, pausa ou troca de modelo.

Quando não usar:
- Não guardar segredos ou objetos de conexão diretamente em snapshots se bastam referências seguras.

Implementação proposta:
- Proposta: persistir campos serializáveis e migráveis.
- Separar sessão do usuário, missão e tentativa de execução.
- Registrar estado de cada efeito externo para não confundir planejado, iniciado e confirmado.

Aplicação LAI proposta:
Proposta LAI: a Helena deve reabrir o estado da missão antes de agir; prompts novos não devem recriar o progresso a partir de suposições.

## T064:C03 — riscos_validacao

Armadilhas:
- Estado persistido pode apontar a artefatos temporários já desaparecidos.
- Atualizações parciais podem combinar etapas incompatíveis.

Métricas sugeridas:
- Taxa de retomada sem perda ou duplicação.
- Falhas de migração e referências inválidas.

Testes propostos:
- Reiniciar processo em cada transição de um workflow e conferir continuidade.
- Mudar schema de estado e testar migração de um snapshot antigo.

## T064:C04 — perguntas_proveniencia

Pergunta: Estado persistente significa memória de longo prazo?
Resposta: É uma forma de persistência operacional. Memória de conhecimento tem finalidade e política de recuperação diferentes.

Pergunta: Salvar após a resposta final basta?
Resposta: Não para missões longas. Falhas podem ocorrer antes; pontos críticos precisam de confirmação durante a execução.

Pergunta: O estado deve guardar credenciais diretamente?
Resposta: Prefira referências a mecanismos apropriados de resolução. A persistência precisa permitir renovar acesso sem transformar um segredo expirado em dependência irrecuperável.

Pergunta: Posso identificar execução apenas pelo usuário?
Resposta: Não quando há missões ou tentativas simultâneas. Identifique proprietário, missão, thread e tentativa conforme as unidades reais de concorrência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T064:C05 — mecanismo_avancado

Persistir estado exige distinguir valores reconstruíveis de recursos efêmeros: um caminho, socket ou objeto cliente não equivale ao recurso que representa. O estado também precisa identificar código e schema capazes de interpretá-lo após atualização. Uma retomada pode restaurar dados perfeitamente e ainda executar uma transição diferente porque o programa mudou. Migrações e verificação de dependências pertencem ao contrato de persistência, além da serialização.

Condição de contorno:
O estado deixa de ser retomável quando contém referências sem duração compatível, segredos expirados ou versões que o novo runtime não sabe interpretar.

Contrato proposto:
- Entradas: Campos serializáveis, referências duráveis, identidade de execução e versão de schema ou workflow.
- Saídas: Estado confirmado e carregável com dependências verificadas ou bloqueios de migração explícitos.
- Estado: Histórico de revisões, migrações aplicadas, agenda e operações externas pendentes.
- Invariante: Carregar bytes válidos não é declarado como retomada bem-sucedida antes de verificar compatibilidade e dependências.

Compromissos de projeto:
- Persistir informação mínima reduz custo e pode aumentar reconstrução após falha.
- Persistir intermediários acelera retomada e torna migração mais difícil quando mudam tipos e contratos de ferramentas.

## T064:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: reiniciar com nova versão do workflow e remover um artefato referenciado. O carregamento deve detectar ambos os problemas e não marcar a missão como pronta apenas porque o JSON foi lido.

Plano de avaliação proposto:
Avaliação proposta: comparar retomada na mesma versão e após migração com falhas de dependência. Medir estados recuperáveis, tempo de reconstrução, transições inválidas e perdas de artefatos; testar também separação entre threads de um mesmo usuário.

Comparações:
- T047 (distinct_from): Memória longa conserva conhecimento reutilizável; estado persistente determina continuidade de uma execução identificada.
- T060 (complements): Checkpoint publica um ponto específico do estado com semântica de retomada.

Afirmação rastreável:
LangGraph separa estado de thread preservado por checkpointers de dados compartilháveis mantidos em stores.
Suporte: direct; fontes: V3A-S031, V3A-S032
Limite: Essa separação não fornece automaticamente migração de qualquer schema customizado ou durabilidade de arquivos externos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T064:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu serialização e migração. Aqui estado persistente inclui fronteiras de portabilidade e prova de restauração em ambiente novo.

Projeto e decomposição
Separe estado lógico da tarefa e conexões ao ambiente. Tokens de sessão, descritores de arquivo e clientes de API devem ser reconstruídos, não tratados como objetos duráveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

Controle adaptativo
Manifesto de restauração declara recursos necessários e quais podem ser substituídos. Trocar modelo ou ferramenta pode exigir revalidação do plano, mesmo quando dados persistidos continuam legíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

Validação contrafactual
Compare reinício no mesmo processo, processo novo e ambiente novo. Meça recursos ausentes, decisões indevidamente preservadas e retomada correta; gravar JSON não prova portabilidade. Unidade de avaliação: estado restaurável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

USO AVANÇADO — Migração de executor
Cenário: Tarefa sai de uma máquina para outra.
Estratégia: Restaurar dados e artefatos, reabrir conexões e verificar versões antes de liberar próxima etapa.
Papel do modelo pequeno: 3–7B interpreta estado; código valida recursos.
Aceite proposto: Nenhuma referência efêmera deve ser aceita como recurso disponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

USO AVANÇADO — Troca de modelo
Cenário: Modelo local substitui provedor remoto.
Estratégia: Manter fatos e progresso, reconstruir contexto no template do novo modelo e validar comportamento em etapa reversível.
Papel do modelo pequeno: 8–14B retoma contrato explícito.
Aceite proposto: Não assumir compatibilidade de prompt, tokenizer ou ferramenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2B-S002, V3A-S032, V4A-S026.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de tarefa estreita a partir de estado estruturado completo.
8–14B: Leitor de estado restaurado que identifica lacunas e incompatibilidades.
15–30B: Replanejador quando recursos ou capacidade do consumidor mudarem.
Requisitos de treino/runtime: Schema versionado, referências duráveis e verificação de dependências; persistência externa não modifica pesos.
Não aplicar quando: O estado depende de recursos que desapareceram e não há procedimento de reconstrução.

## T064:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C005 — Google / Megastore em serviços interativos
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Autores relatam serviços Google em produção sobre Megastore.
Mecanismo documentado: Partições recebem semântica ACID serializável e replicação síncrona.
Correspondência com esta base: Estado durável de serviços, não estado completo de um agente LLM.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher agregado transacional por sessão/projeto e manter decisões do LLM como propostas.
Limite: A atomicidade não atravessa automaticamente partições e APIs externas; relato de 2011. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S004.

V4A-C011 — Google / MillWheel: detector contínuo de anomalias
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Artigo relata detector em uso e adoção do framework no Google.
Mecanismo documentado: Grafo de computação sobre registros, estado persistente e tempo lógico.
Correspondência com esta base: Estado de processamento é durável; não define serialização de um agente.
Transferência proposta para modelo pequeno: Proposta de engenharia: Manter agregações em código; usar 3–7B apenas para categorizar observações recebidas.
Limite: Não confundir fluxo de eventos com Event Sourcing de domínio, nem inferir efeitos externos exatamente uma vez. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S012.

V4A-C027 — Letta / Framework de agentes stateful
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Fornecedor distingue framework Letta do padrão MemGPT e oferece serviços stateful.
Mecanismo documentado: Persistência do agente e ferramentas de memória externas ao modelo.
Correspondência com esta base: Estado persistente de agentes é recurso explícito.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher modelo compatível por testes de protocolo e separar identidade de agente e conversa.
Limite: Letta não é bigtech; implantação facilitada não comprova cliente ou escala. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S026, V2B-S002.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q005, V4A-Q008, V4A-Q023.

## T064:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T064 → T060 [complements]
Como combinar: Vincular estado à fronteira executável de retomada.
Interface: Estado, etapa, revisão e operações pendentes.
Condição: Checkpoint preservar contexto de continuidade.
Aceite proposto: Restaurar estado sem cursor e exigir diagnóstico de incompletude.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2B-S002, V3A-S032, V4A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T064 → T066 [requires]
Como combinar: Resolver recursos após restauração.
Interface: Referências, versões e status de disponibilidade.
Condição: Resolver respeitar ambiente e escopo atuais.
Aceite proposto: Testar recurso removido e impedir uso presumido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2B-S002, V3A-S032, V4A-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não persistir segredo efêmero como memória reutilizável.
- Não confundir estado legível com plano ainda válido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar retomada entre ambientes; capacidade do modelo não substitui recursos e contratos ausentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T040, T053, T059, T060, T065

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S031 — LangGraph Checkpointers

[https://docs.langchain.com/oss/python/langgraph/checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints por super-step, StateSnapshot e pending writes de tarefas concluídas; estado de execução e retomada.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V3A-S032 — LangGraph Stores

[https://docs.langchain.com/oss/python/langgraph/stores](https://docs.langchain.com/oss/python/langgraph/stores)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memórias entre threads, namespaces, listagem paginada e ordenação dependente do backend.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V2B-S002 — Stateful agents

[https://docs.letta.com/concepts/stateful-agents](https://docs.letta.com/concepts/stateful-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade persistente, memória compartilhada entre conversas do mesmo agente e distinção entre agentes locais e com backup em nuvem.

Limite: Documentação atual consultada; não comprova isolamento ou durabilidade de uma implantação específica.

### V4A-S026 — MemGPT Is Now Part of Letta

[https://www.letta.com/blog/memgpt-and-letta/](https://www.letta.com/blog/memgpt-and-letta/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue padrão de memória MemGPT e framework Letta; persistência de agentes como serviço.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S004 — Megastore: Providing Scalable, Highly Available Storage for Interactive Services

[https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/](https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transações serializáveis em partições e experiência com serviços Google em produção.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S012 — MillWheel: Fault-Tolerant Stream Processing at Internet Scale

[https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxos com estado persistente e tempo lógico, incluindo detector de anomalias em uso.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
