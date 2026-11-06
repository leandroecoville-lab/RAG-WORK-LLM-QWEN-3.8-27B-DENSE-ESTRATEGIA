# T063 — Virtual Context Management — memória virtual de contexto, estilo MemGPT

**Nome canônico:** Virtual Context Management — MemGPT  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T063  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gerenciamento de contexto virtual; Virtual Context Management — MemGPT

## T063:C01 — conceito

Estratégia proposta no MemGPT, inspirada em memória virtual de sistemas operacionais: informação se move entre contexto limitado e armazenamento externo, com controle explícito da execução. A analogia não implica acesso automático e perfeito a tudo que está armazenado.

Como funciona:
- Distinguir informação ativa de memória externa recuperável.
- Usar operações de memória para carregar e preservar conteúdo.
- Controlar a continuação da tarefa conforme necessidade de nova informação.

## T063:C02 — aplicacao

Quando usar:
- Conversas entre sessões e análise documental extensa.
- Pesquisa de agentes que gerenciam sua própria seleção de contexto.

Quando não usar:
- Não tratar a capacidade externa como atenção simultânea sobre todo o histórico.

Implementação proposta:
- Proposta: definir ferramentas de leitura e escrita com contratos curtos.
- Manter memória essencial fixada e orçamento para novos resultados.
- Medir quando o agente deixa de recuperar algo necessário e oferecer regras de recuperação obrigatória.

Aplicação LAI proposta:
Proposta LAI: adotar princípios de contexto virtual na Helena sem afirmar reprodução do MemGPT; a implantação precisa de avaliação própria.

## T063:C03 — riscos_validacao

Armadilhas:
- O modelo pode não perceber a ausência de uma informação.
- Operações frequentes de memória podem aumentar latência e custo.

Métricas sugeridas:
- Recall de informações fora do contexto ativo.
- Sucesso de tarefa e custo de movimentação entre níveis.

Testes propostos:
- Colocar um fato relevante apenas na memória externa e pedir tarefa que dependa dele.
- Simular indisponibilidade da memória e exigir resposta com lacuna explícita.

## T063:C04 — perguntas_proveniencia

Pergunta: MemGPT fornece contexto infinito?
Resposta: Não literalmente. Usa memória externa e movimentação de informação para trabalhar além do contexto ativo.

Pergunta: É a mesma coisa que simplesmente aumentar max_context?
Resposta: Não. A estratégia organiza recuperação e persistência, enquanto a configuração altera o limite de entrada suportado.

Pergunta: A janela física do modelo aumenta?
Resposta: Não por esse mecanismo. O sistema altera qual informação entra na janela e pode executar várias chamadas para trabalhar com um acervo maior.

Pergunta: É necessário modificar pesos para esse padrão?
Resposta: A ideia pode ser implementada com ferramentas e controle externo. O desempenho depende da capacidade do modelo de usar essas operações corretamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T063:C05 — mecanismo_avancado

A analogia com memória virtual funciona melhor para entender movimentação do que garantias. Sistemas operacionais identificam endereços ausentes de forma precisa; um agente pode não perceber que precisa de uma lembrança. Ferramentas de busca, escrita e controle de execução ampliam o contexto utilizável, mas a política de acionamento continua sujeita a falhas. Há custo tanto para localizar conteúdo quanto para decidir quando fazê-lo.

Condição de contorno:
Sem índices descobríveis, regras de recuperação ou sinais de dependência, o agente pode responder com a janela atual mesmo quando existe evidência decisiva armazenada fora dela.

Contrato proposto:
- Entradas: Estado essencial, contexto ativo, ferramentas de memória e limites de orçamento por chamada.
- Saídas: Movimentações de conteúdo, referências resolvidas e continuidade da execução com lacunas registradas.
- Estado: Memórias externas, histórico de buscas, regiões fixadas e limites de controle do agente.
- Invariante: A disponibilidade de informação externa não é apresentada como se todo esse conteúdo tivesse sido lido simultaneamente.

Compromissos de projeto:
- Mover dados sob demanda permite sessões maiores e adiciona turnos de ferramenta.
- Autogerência oferece flexibilidade e exige limites para evitar busca circular ou gravação de memórias incorretas.

## T063:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: armazenar uma restrição antiga fora da janela e criar uma ação que dependa dela. Compare acionamento espontâneo e regra explícita de consulta; falha de recuperação deve impedir alegação de cobertura completa.

Plano de avaliação proposto:
Avaliação proposta: comparar janela fixa, recuperação inicial e gerência durante a execução. Medir acertos de recuperação, leituras redundantes, custo de controle e retenção entre sessões; incluir lacunas que não produzem baixa confiança aparente.

Comparações:
- R001 (complements): MemGPT é a proposta concreta que introduz e demonstra esse desenho de gerência virtual de contexto.
- T078 (complements): Semantic Page Fault nomeia uma analogia para dependência ausente, cuja detecção não é garantida pelo modelo.

Afirmação rastreável:
MemGPT propõe virtual context management com diferentes níveis de memória e interrupções para controle de fluxo.
Suporte: direct; fontes: A-S009
Limite: O artigo demonstra tarefas específicas; a analogia não garante memória ilimitada efetiva nem detecção perfeita de informação ausente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T063:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou limites da analogia com sistema operacional. Aqui contexto virtual usa prefetch condicionado e detecção de thrashing semântico.

Projeto e decomposição
Antecipe carregamento de dependências explícitas do próximo passo, como schema ou definição citada. Prefetch especulativo amplo pode ocupar a janela antes de saber o que será útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Controle adaptativo
Detecte alternância repetida entre blocos que se expulsam mutuamente. A solução pode ser decompor a tarefa ou fixar conjunto mínimo, não apenas aumentar frequência de recuperação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Validação contrafactual
Compare carga sob demanda e prefetch limitado. Meça acertos de antecipação, conteúdo carregado sem uso e ciclos de recarga; falta semântica continua inferida, não falha de endereço exata. Unidade de avaliação: sequência de cargas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Execução de procedimento
Cenário: Próxima etapa tem dependências conhecidas.
Estratégia: Carregar schema e parâmetros antes da etapa, mantendo evidência da atual até confirmar conclusão. Liberar conjunto anterior pela transição.
Papel do modelo pequeno: 3–7B executa etapa delimitada.
Aceite proposto: Não expulsar condição necessária antes de concluir ação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Comparação de arquivos grandes
Cenário: Leitor alterna continuamente entre versões.
Estratégia: Construir quadro de diferenças com referências e carregar pares correspondentes, evitando reler arquivos completos.
Papel do modelo pequeno: 8–14B compara pares.
Aceite proposto: Reduzir recargas sem perder diferenças relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de blocos pequenos selecionados por controlador explícito.
8–14B: Gerente de comparação local com prefetch de dependências.
15–30B: Planejador que reorganiza tarefa quando conjunto de trabalho não cabe.
Requisitos de treino/runtime: Mapa de residência, referências versionadas e telemetria de cargas; nenhum aumento físico da janela é presumido.
Não aplicar quando: Conjunto indispensável excede orçamento e não pode ser dividido sem perder relações essenciais.

## T063:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C026 — UC Berkeley; autores MemGPT / MemGPT original
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa avalia gestão de contexto virtual em documentos e conversas.
Mecanismo documentado: Ferramentas movimentam informação entre janela e armazenamento externo.
Correspondência com esta base: Virtual context management é o mecanismo estudado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar política curta de consultar, carregar e verificar para 3–14B antes de delegar controle livre.
Limite: Não comprova produção bigtech nem memória ilimitada; experimentos não são garantias do runtime. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## T063:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T063 → T078 [requires]
Como combinar: Representar falta específica que precisa de carga.
Interface: Requisito ausente, referência e decisão bloqueada.
Condição: Falta ter critério de resolução verificável.
Aceite proposto: Carregar trecho parecido e manter falta aberta se não responder.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T063 → T218 [complements]
Como combinar: Detectar thrashing de blocos sem avanço.
Interface: Histórico de cargas, descarte e progresso.
Condição: Repetição ser medida por identidade e revisão.
Aceite proposto: Forçar alternância A/B e exigir replanejamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir paginação de texto com KV cache do modelo.
- Não prometer memória ilimitada disponível em uma chamada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas maiores que a janela com igual custo total; paginação útil depende da política de seleção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T062, T067, T078, R001

## Fontes primárias associadas

### A-S009 — MemGPT: Towards LLMs as Operating Systems

[https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gerência de contexto virtual entre níveis de memória e controle de fluxo.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
