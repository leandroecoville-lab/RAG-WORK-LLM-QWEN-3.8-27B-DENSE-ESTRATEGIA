# T053 — Scratchpad em arquivo

**Nome canônico:** Scratchpad em Arquivo  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T053  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** scratchpad persistente; notas operacionais externas; Scratchpad em Arquivo

## T053:C01 — conceito

Externaliza estado operacional explícito da missão em arquivos: objetivo, plano, decisões, hipóteses, resultados e referências. A próxima chamada carrega somente o necessário. Não equivale a extrair integralmente o raciocínio interno oculto da LLM; registra informações úteis e verificáveis para continuidade.

Como funciona:
- Escrever estado e notas após etapas relevantes.
- Persistir com versão e indicação de conclusão da gravação.
- Reler estado compacto e abrir detalhes por referência.

## T053:C02 — aplicacao

Quando usar:
- Missões longas, auditorias e desenvolvimento com interrupções.
- Agentes que precisam separar contexto ativo de acervo operacional.

Quando não usar:
- Não usar um único arquivo editável como prova exclusiva de que uma ação ocorreu.

Implementação proposta:
- Proposta: separar estado atual, decisões, hipóteses e evidências.
- Gravar arquivo temporário e promover por operação atômica quando suportada.
- Usar controle de versão ou compare-and-swap para evitar sobrescritas concorrentes.

Aplicação LAI proposta:
Proposta LAI: tornar o estado da Helena explícito e recuperável, mantendo logs e resultados de ferramentas como evidência independente das notas.

## T053:C03 — riscos_validacao

Armadilhas:
- O agente pode dizer que salvou sem a gravação ter sido confirmada.
- Dois processos podem sobrescrever o mesmo estado.

Métricas sugeridas:
- Taxa de retomada fiel e perda de estado.
- Quantidade de leituras necessárias por etapa.

Testes propostos:
- Interromper após gravação e reconstruir próxima ação em novo processo.
- Simular dois escritores e exigir detecção de conflito.

## T053:C04 — perguntas_proveniencia

Pergunta: O arquivo deve conter todo o raciocínio do modelo?
Resposta: Não. Deve guardar decisões, justificativas concisas, evidências e estado operacional necessário.

Pergunta: Guardar uma referência economiza contexto sempre?
Resposta: Somente se a recuperação seletiva custar menos que reenviar o material e mantiver a qualidade necessária.

Pergunta: O arquivo precisa conter raciocínio interno completo?
Resposta: Não. Registre decisões, motivos verificáveis, resultados, pendências e referências necessários à continuidade, sem alegar extrair estados internos ocultos.

Pergunta: Como saber qual nota prevalece?
Resposta: Use revisão publicada e regras de autoridade. Data de modificação do filesystem pode refletir cópia ou sincronização, e não a ordem lógica das decisões.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T053:C05 — mecanismo_avancado

Um scratchpad em arquivo funciona como protocolo entre execuções: alguém escreve um estado explícito e outro processo o interpreta posteriormente. O contrato precisa distinguir alteração no buffer, gravação no disco, revisão publicada e cópia sincronizada. Um arquivo legível pode estar incompleto ou ser de uma execução antiga. Por isso, identidade da missão, revisão e marcador de conclusão têm utilidade operacional além do formato Markdown.

Condição de contorno:
Arquivos deixam de ser uma solução simples quando muitos escritores precisam alterar simultaneamente o mesmo estado sem coordenação ou quando não existe armazenamento persistente.

Contrato proposto:
- Entradas: Estado explícito da tarefa, referências verificáveis e revisão que o escritor pretende substituir.
- Saídas: Arquivo completo publicado com identidade, versão e confirmação de gravação observada.
- Estado: Revisão anterior, alterações pendentes, posição de sincronização e conflitos não resolvidos.
- Invariante: Um leitor usa apenas revisões completas e não interpreta nota de intenção como confirmação de execução.

Compromissos de projeto:
- Arquivos são inspecionáveis e interoperáveis, mas não oferecem transações entre recursos por padrão.
- Versionamento facilita revisão e recuperação; sincronização remota adiciona estados intermediários e conflitos.

## T053:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper uma escrita no meio e reiniciar o leitor em outro processo. Ele deve recuperar a última revisão válida ou detectar incompletude, sem usar a metade nova como estado definitivo.

Plano de avaliação proposto:
Avaliação proposta: comparar notas livres e protocolo com campos mínimos em retomadas interrompidas. Medir estado reconstruído, perdas de correções, conflitos de escritor e latência de publicação; incluir gravação local confirmada com sincronização remota falha.

Comparações:
- T064 (complements): O arquivo pode representar parte do estado persistente, desde que tenha identidade e semântica de retomada.
- T076 (complements): Git acrescenta histórico de versões; não transforma automaticamente cada arquivo em estado transacional do agente.

Afirmação rastreável:
MemFS distingue edições locais de memória comprometida e sincronizada por Git entre computadores.
Suporte: direct; fontes: A-S010
Limite: É um exemplo de implementação; um scratchpad comum não herda automaticamente commit, push ou resolução de conflitos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T053:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou estados de persistência. Aqui scratchpad vira um documento de trabalho com seções de autoridade e leitura econômica.

Projeto e decomposição
Separe fatos observados, hipóteses, decisões e tarefas em seções identificadas. Atualizações do modelo não devem transformar hipótese em decisão apenas por mover uma linha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

Controle adaptativo
Use índice curto no início e detalhes referenciados por seção. O consumidor pequeno lê primeiro estado e pendências, abrindo justificativas somente quando a ação depender delas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

Validação contrafactual
Compare arquivo narrativo e seções tipadas. Meça erros de retomada, repetição de trabalho e alterações concorrentes em seções diferentes; verificar também crescimento do arquivo. Unidade de avaliação: revisão de arquivo de trabalho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

USO AVANÇADO — Projeto longo de código
Cenário: Estado precisa sobreviver à sessão.
Estratégia: Registrar revisão do código, teste executado e próximo teste; manter resultado de execução distinto de intenção de executar.
Papel do modelo pequeno: 3–7B atualiza campos; 8–14B retoma.
Aceite proposto: Nenhum teste planejado pode aparecer como aprovado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

USO AVANÇADO — Pesquisa colaborativa
Cenário: Agentes acrescentam descobertas.
Estratégia: Cada agente escreve proposta com fonte e área de responsabilidade; integrador confirma decisões e resolve conflito entre seções.
Papel do modelo pequeno: 15–30B integra evidências.
Aceite proposto: Alteração deve preservar autoria e evidência de cada afirmação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atualizador de campos curtos com operações restritas por seção.
8–14B: Leitor de estado e justificativas locais para retomar tarefa.
15–30B: Integrador de contribuições com conflitos e dependências cruzadas.
Requisitos de treino/runtime: Formato de seções, revisão-base e escrita atômica; arquivo continua artefato externo, não treino de pesos.
Não aplicar quando: Scratchpad é a única cópia de evidências extensas ou cresce sem índice e política de manutenção.

## T053:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.
Mecanismo documentado: Redução da conversa e persistência de informação reutilizável fora da janela.
Correspondência com esta base: Notas externas são família relacionada; não demonstra todos os contratos desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.
Limite: Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S002, A-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019, V4A-Q026.

## T053:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T053 → T076 [complements]
Como combinar: Versionar alterações de seções e decisões.
Interface: Arquivo, diff, revisão-base e autoria.
Condição: Conflitos semânticos revisados após merge textual.
Aceite proposto: Introduzir duas decisões incompatíveis em seções distintas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T053 → T044 [complements]
Como combinar: Ler justificativas sob demanda.
Interface: Índice, section_id e requisito da tarefa.
Condição: Seção manter referência ao conteúdo completo.
Aceite proposto: Retomar com índice apenas e abrir suporte necessário.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não salvar segredos incidentais em notas reutilizáveis.
- Não confundir presença no arquivo com confirmação externa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar retomada em sessão limpa; modelos pequenos precisam de campos mais explícitos que narrativa livre.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T050, T060, T064

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
