# T242 — Recuperação híbrida por Snapshot + Event Sourcing

**Nome canônico:** Recuperação híbrida por Snapshot + Event Sourcing  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T242  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** snapshot plus event sourcing; snapshot e replay incremental

## T242:C01 — conceito

Recuperação que carrega um snapshot válido e aplica apenas os eventos posteriores à sua fronteira. O padrão reduz trabalho de reconstrução sem transformar o snapshot na única fonte de verdade. Sua correção depende de alinhamento entre estado capturado, sequência confirmada e versão do processador de eventos.

Como funciona:
- O snapshot representa todos os eventos até uma sequência declarada.
- O recuperador inicia nesse estado e aplica o sufixo do log após a fronteira.
- Se o snapshot não puder ser validado, usa outro ponto consistente ou reconstrução integral compatível.

## T242:C02 — aplicacao

Quando usar:
- Históricos extensos, projeções custosas e tarefas duráveis cuja recuperação integral seria lenta.

Quando não usar:
- Combinar uma cópia parcial com um log de cobertura desconhecida ou apagar eventos necessários sem política de retenção e reconstrução definida.

Implementação proposta:
- Proposta: persistir snapshot com schema_version, processor_version, sequência e digest dos dados.
- Garantir que a fronteira não avance além dos eventos efetivamente incorporados ao estado.
- Carregar o snapshot validado, buscar eventos estritamente posteriores e aplicar a mesma lógica de reconstrução.
- Tratar duplicatas e gaps conforme a ordenação do log; um gap não deve ser silenciosamente ignorado.
- Comparar periodicamente a recuperação híbrida com replay integral em uma amostra e reconciliar efeitos externos à parte.

Aplicação LAI proposta:
Proposta LAI: acelerar retomadas de missões preservando um log verificável, snapshots versionados e uma política explícita de compatibilidade e retenção.

## T242:C03 — riscos_validacao

Armadilhas:
- Erro de uma unidade na fronteira duplica ou omite um evento.
- Mudanças no redutor podem tornar snapshots antigos incompatíveis.
- Um log incompleto impede a reconstrução mesmo quando o snapshot parece íntegro.

Métricas sugeridas:
- Tempo de recuperação; tamanho do sufixo; idade do snapshot; gaps; divergência contra replay integral; falhas de compatibilidade.

Testes propostos:
- Criar snapshot na sequência N e verificar aplicação a partir de N+1.
- Corromper o snapshot e confirmar fallback controlado.
- Remover um evento do sufixo e exigir diagnóstico de cobertura incompleta.
- Restaurar diferentes snapshots do mesmo histórico e comparar o estado final esperado.

## T242:C04 — perguntas_proveniencia

Pergunta: Snapshot torna Event Sourcing desnecessário?
Resposta: Não neste padrão. O snapshot é um atalho materializado; os eventos posteriores e a identidade da fronteira continuam necessários à recuperação.

Pergunta: Isso garante exatamente uma execução de efeitos externos?
Resposta: Não. O padrão reconstrói estado local. Garantias de efeitos dependem do protocolo com o sistema externo, da idempotência e da reconciliação de incertezas.

Pergunta: O snapshot permite apagar imediatamente todo o histórico?
Resposta: Não sem mudar o contrato de recuperação e auditoria; erros de snapshot ou novas projeções podem precisar dos eventos antigos.

Pergunta: Como verificar a fronteira do cursor?
Resposta: Comparar a recuperação híbrida com uma projeção de referência e incluir eventos imediatamente antes e depois da posição declarada.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T242:C05 — mecanismo_avancado

O snapshot precisa declarar se seu cursor representa último evento incluído ou próximo evento a aplicar. Se incorpora até 100, o sufixo começa em 101; essa convenção evita dupla aplicação ou lacuna. Versão do reducer, schema e identidade do stream também precisam ser compatíveis. Um snapshot corrompido deve permitir recorrer a uma versão anterior ou ao replay integral, desde que o histórico necessário ainda exista.

Condição de contorno:
Apagar eventos antigos após snapshot elimina a recuperação integral e torna disponibilidade e compatibilidade desse snapshot mais críticas.

Contrato proposto:
- Entradas: Snapshot, cursor com semântica explícita, stream e processador compatível.
- Saídas: Estado restaurado, sufixo aplicado e evidência de continuidade.
- Estado: Versões, integridade do snapshot e intervalo disponível de eventos.
- Invariante: Nenhum evento lógico é omitido ou aplicado duas vezes na fronteira da recuperação.

Compromissos de projeto:
- Snapshots frequentes encurtam replay e consomem escrita e armazenamento.
- Retenção curta reduz volume e diminui opções de reconstrução após corrupção ou mudança de código.

## T242:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deslocar o cursor em uma unidade e corromper o snapshot mais recente; exigir detecção da inconsistência e fallback para base recuperável sem repetir efeitos externos.

Plano de avaliação proposto:
Comparar replay integral e recuperação híbrida em históricos de tamanhos variados. Verificar igualdade do estado esperado, duração e custo de snapshots. Escolher frequência pela relação entre taxa de eventos, custo de projeção e objetivo de recuperação.

Comparações:
- T240 (requires): O mecanismo híbrido pressupõe uma base de snapshot válida ou retorna ao replay integral.
- T241 (requires): Aplicar os eventos posteriores é parte constitutiva da recuperação híbrida.

Afirmação rastreável:
Event sourcing usa histórico ordenado para reidratar estado, e snapshots podem reduzir o trabalho de reconstrução.
Suporte: direct; fontes: A-S027
Limite: A fonte apoia o padrão; convenção do cursor e fallback precisam ser definidos e verificados pela aplicação.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T242:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 fixava cursor e fallback para snapshot anterior. A expansão otimiza recuperação com verificação de compatibilidade, política de retenção e ensaios que distinguem dados perdidos de mero tempo de reconstrução.

Escolher base elegível
O snapshot mais recente nem sempre é utilizável: pode ter schema incompatível, artefato ausente ou versão de reducer indisponível. Selecione a base mais recente que satisfaça integridade e semântica, e declare o custo do sufixo restante. Não converter silenciosamente campos sem origem apenas para conseguir usar o checkpoint novo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V3C-S028.

Retenção como contrato
Decida por quanto tempo conservar eventos anteriores e snapshots compatíveis. Apagar o prefixo reduz armazenamento e elimina caminhos de recuperação; o snapshot passa a ser parte crítica do estado durável. Teste corrupção e perda antes de adotar essa política, incluindo referências a arquivos que não estão dentro do log.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V4C-S025.

Metas de recuperação
Meça tempo até serviço apto e até missão efetivamente reconciliada. Carregar um snapshot rapidamente não significa que efeitos externos e eventos atrasados foram resolvidos. Defina quais dados podem ser perdidos, se algum, e quais operações devem permanecer desconhecidas até consulta; não esconder incerteza atrás de uma métrica de startup.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S001, C-S026.

USO AVANÇADO — Missões com histórico extenso
Cenário: Reproduzir tudo a cada retomada fica caro.
Estratégia: Crie snapshots em fronteiras consistentes e aplique o sufixo em ambiente controlado. Compare o resultado com replay integral numa amostra de históricos que incluam falhas. Se a comparação divergir, preserve log e investigue antes de reduzir retenção.
Papel do modelo pequeno: 3–30B opera nas atividades; recuperação do estado fica em código verificável.
Aceite proposto: Proposta: estado equivalente à referência com tempo de recuperação menor e sem lacunas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V4C-S001.

USO AVANÇADO — Migração do formato de estado
Cenário: Um novo esquema muda como tarefas e evidências são representadas.
Estratégia: Mantenha processador antigo disponível ou gere snapshot migrado com manifesto de transformação. Verifique invariantes e referências antes de marcá-lo elegível. Se um campo não pode ser reconstruído, represente a lacuna ou refaça a etapa com nova intenção, sem atribuir dado inventado ao passado.
Papel do modelo pequeno: 8–14B auxilia mapeamento; 15–30B revisa casos ambíguos; código executa migração.
Aceite proposto: Proposta: migração auditável e fallback para base anterior enquanto houver compatibilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S041, V3C-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Unidades de atividade pequenas reduzem o estado que precisa ser recuperado por vez.
8–14B: Checagem de tarefas e referências após replay, sem modificar automaticamente o histórico.
15–30B: Análise de migração e reconciliação de exceções, mantendo lógica de recuperação determinística.
Requisitos de treino/runtime: Cursor inequívoco, identidade do stream, versão do reducer e política explícita de retenção.
Não aplicar quando: Não eliminar eventos antigos antes de demonstrar restauração e compatibilidade dos snapshots remanescentes.

## T242:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes de event sourcing e continuidade sustentam princípios. Não foi encontrado caso operacional que prove exatamente toda a composição editorial para agentes proposta aqui.
Consultas registradas: V4C-Q002, V4C-Q020.

## T242:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T242 → T240 [complements]
Como combinar: Capturar base consistente com manifesto e cursor para iniciar a recuperação.
Interface: Estado, cursor e referências de artefatos.
Condição: Base passou por teste de restauração.
Aceite proposto: Snapshot não incorpora cursor posterior ao estado gravado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T242 → T241 [complements]
Como combinar: Reproduzir sufixo com processador compatível e sem repetir efeitos externos.
Interface: Eventos posteriores e versão de redução.
Condição: Convenção de último incluído ou próximo a aplicar é explícita.
Aceite proposto: Nenhum evento perdido ou aplicado duas vezes na fronteira.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S041. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Checkpoint de transporte por partição não prova corte global entre streams.
- Snapshot corrompido com prefixo apagado pode impedir recuperação; registrar esse limite antes de reduzir retenção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare recuperação completa, incluindo reconciliação, em vez de carregar bytes. A estratégia aumenta continuidade de sistemas com modelos pequenos, mas não cria memória cognitiva nem resolve ausência de eventos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T240, T241, T243

## Fontes primárias associadas

### A-S027 — Event Sourcing pattern

[https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico append-only como origem de projeções e reconstrução do estado.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S041 — Marten — Events Versioning

[https://martendb.io/events/versioning.html](https://martendb.io/events/versioning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Evolução de schemas e upcasting permitem interpretar eventos históricos sem tratar mudança de representação como novo fato.

Limite: Mecanismos específicos do framework; conversão deve preservar semântica e não inventar informação histórica ausente.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S025 — Brooklin Architecture

[https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture](https://github.com/linkedin/brooklin/wiki/Brooklin-Architecture)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenador, partições, atribuição de tarefas e offsets/checkpoints em ZooKeeper.

Limite: Fonte primária consultada, sem reprodução. Documentação de recurso não identifica automaticamente um deployment de cliente.

### V4C-S001 — Announcing Cadence 1.0: The Powerful Workflow Platform Built for Scale and Reliability

[https://www.uber.com/us/en/blog/announcing-cadence/](https://www.uber.com/us/en/blog/announcing-cadence/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Cadence, persistência e retomada de workflows, isolamento de tráfego e validação de evolução de código.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
