# T078 — Semantic Page Fault

**Nome canônico:** Semantic Page Fault  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T078  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** falta semântica de página; lacuna de contexto

## T078:C01 — conceito

Analogia de engenharia para o momento em que uma ação precisa de informação que não está no contexto ativo. Diferentemente de uma falta de página convencional, a ausência semântica pode não ser detectável de forma exata: o modelo pode desconhecer o que está faltando. Não é um padrão universal estabelecido.

Como funciona:
- Detectar uma dependência, referência ou campo necessário ausente.
- Solicitar recuperação da informação externa correspondente.
- Revalidar suficiência do contexto antes de continuar a ação.

Nota de nomenclatura: Analogia arquitetural relacionada à memória virtual do MemGPT; não se afirma que o paper padroniza esse rótulo ou garante detecção de toda lacuna.

## T078:C02 — aplicacao

Quando usar:
- Agentes com memória hierárquica e referências externas.
- Diagnóstico de falhas causadas por informação não carregada.

Quando não usar:
- Não interpretar confiança do modelo como prova de que nenhuma informação necessária está ausente.

Implementação proposta:
- Proposta: criar pré-condições verificáveis para ações críticas.
- Manter campos unknown e missing_reference explícitos no estado.
- Limitar tentativas de recuperação e retornar bloqueio ou incerteza quando a lacuna não puder ser resolvida.

Aplicação LAI proposta:
Proposta LAI: usar o conceito como evento de observabilidade da Helena, por exemplo falta de versão do schema, sem apresentá-lo como capacidade automática do Qwen.

## T078:C03 — riscos_validacao

Armadilhas:
- O sistema pode não reconhecer que há uma dependência omitida.
- Uma busca irrelevante pode ser tratada como resolução da lacuna.

Métricas sugeridas:
- Lacunas relevantes detectadas antes da execução.
- Taxa de recuperação suficiente e falsos sinais de resolução.

Testes propostos:
- Remover uma referência obrigatória de contrato e impedir a ação dependente.
- Fornecer resultado de busca sem a informação pedida e manter a lacuna aberta.

## T078:C04 — perguntas_proveniencia

Pergunta: Semantic page fault é um recurso nativo da LLM?
Resposta: Não como propriedade universal. É uma analogia que precisa de detecção e recuperação implementadas no sistema.

Pergunta: Por que a analogia com sistema operacional é limitada?
Resposta: O endereço de uma página faltante é explícito; a informação semântica necessária pode depender de interpretação e ser desconhecida do agente.

Pergunta: A falta pode ser resolvida por um resumo?
Resposta: Sim, se o resumo contém suporte suficiente e verificável para a dependência. Quando exige detalhe exato, é necessário abrir a fonte correspondente.

Pergunta: O que fazer quando nenhuma busca resolve?
Resposta: Preserve o estado desconhecido, registre tentativas e encerre a etapa conforme sua política. Não transforme esgotamento de orçamento em evidência de ausência.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T078:C05 — mecanismo_avancado

Semantic Page Fault é uma analogia útil para distinguir dependência identificável e lacuna semântica. A primeira pode ser verificada por contrato: falta uma versão, um resultado ou uma evidência obrigatória. A segunda depende de perceber que algo relevante está ausente, tarefa sujeita a falsos negativos. O controlador deve registrar a razão da busca e a condição observável que permitirá declarar a lacuna resolvida.

Condição de contorno:
Não existe detector universal que saiba tudo que o modelo deixou de considerar; ausência de alarme não comprova suficiência do contexto.

Contrato proposto:
- Entradas: Ação pretendida, pré-condições, contexto ativo e referências potencialmente necessárias.
- Saídas: Pedido de recuperação com critério de resolução, ou bloqueio explícito por dependência não satisfeita.
- Estado: Lacunas abertas, tentativas, evidências obtidas e orçamento de expansão.
- Invariante: Encontrar qualquer resultado parecido não basta para marcar como satisfeita a dependência originalmente ausente.

Compromissos de projeto:
- Regras determinísticas cobrem dependências conhecidas e não detectam todos os pressupostos implícitos.
- Sinais do modelo ampliam cobertura e podem gerar alarmes falsos ou buscas sem progresso.

## T078:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: retornar um documento semanticamente próximo que não contém a versão exigida pela ação. O controlador deve manter a falta aberta e impedir que o agente trate similaridade como resolução.

Plano de avaliação proposto:
Avaliação proposta: comparar gatilho apenas verbal, pré-condições explícitas e combinação dos dois. Medir dependências ausentes detectadas, alarmes falsos, custo de busca e ações indevidas; incluir casos de confiança alta sem evidência suficiente.

Comparações:
- T063 (complements): Gerência virtual fornece operações para trazer conteúdo; a analogia trata a decisão de perceber e resolver sua ausência.
- T044 (complements): Expansão progressiva pode executar a busca motivada por uma lacuna identificada.

Afirmação rastreável:
MemGPT usa níveis externos e operações explícitas de recuperação para trabalhar com conteúdo além da janela ativa.
Suporte: related; fontes: A-S009
Limite: A fonte sustenta a inspiração arquitetural, não estabelece Semantic Page Fault como padrão formal nem garante detecção de faltas semânticas.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T078:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu Semantic Page Fault como analogia. Aqui o evento recebe critérios de detecção e resolução específicos por contrato de tarefa.

Projeto e decomposição
Detecte falta por requisito explícito: referência não aberta, campo obrigatório ausente ou conflito não resolvido. Não existe detector universal que saiba toda informação que o modelo deveria ter.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Controle adaptativo
Uma carga resolve a falta apenas se satisfizer o requisito registrado. Conteúdo parecido pode aumentar tokens sem remover o bloqueio; manter estado aberto evita falso progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

Validação contrafactual
Compare detecção por autoconfiança e por contrato. Meça faltas reais detectadas, alarmes indevidos e conclusões emitidas antes da resolução; incluir perguntas sem fonte disponível. Unidade de avaliação: lacuna semântica registrada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Resposta com citação
Cenário: Modelo possui título mas não conteúdo.
Estratégia: Gerar falta de evidência, resolver referência e ler trecho antes de redigir afirmação factual. Se indisponível, declarar lacuna.
Papel do modelo pequeno: 3–7B verifica campos.
Aceite proposto: Nenhuma citação pode ser validada só pelo nome do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

USO AVANÇADO — Execução de procedimento
Cenário: Falta pré-condição para próxima ação.
Estratégia: Suspender etapa, buscar dado específico e testar condição; se fonte retornar algo inconclusivo, manter bloqueio.
Papel do modelo pequeno: 8–14B identifica necessidade.
Aceite proposto: Ação só avança quando a pré-condição observável estiver satisfeita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S009, A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Detector de campos obrigatórios ausentes em schema fechado.
8–14B: Detector de contradição ou referência insuficiente em pacote curto.
15–30B: Planejador de como resolver lacunas interdependentes, com orçamento e parada.
Requisitos de treino/runtime: Contrato de tarefa, estados aberto/resolvido/indisponível e ferramenta de resolução; nomenclatura é editorial.
Não aplicar quando: A aplicação trata confiança subjetiva como prova de completude ou não possui fonte capaz de resolver a falta.

## T078:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C026 — UC Berkeley; autores MemGPT / MemGPT original
Evidência: pesquisa; não comprova produção; analogia; não é adoção deste componente. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa avalia gestão de contexto virtual em documentos e conversas.
Mecanismo documentado: Ferramentas movimentam informação entre janela e armazenamento externo.
Correspondência com esta base: Semantic Page Fault é rótulo editorial inspirado em necessidade de informação.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar política curta de consultar, carregar e verificar para 3–14B antes de delegar controle livre.
Limite: Não comprova produção bigtech nem memória ilimitada; experimentos não são garantias do runtime. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q023.

## T078:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T078 → T066 [requires]
Como combinar: Resolver identidade e abrir conteúdo faltante.
Interface: Requisito, referência, versão e seletor.
Condição: Abertura verificar o conteúdo esperado.
Aceite proposto: Retornar recurso homônimo e manter falta aberta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T078 → T044 [feeds]
Como combinar: Expandir contexto com objetivo de resolver lacuna.
Interface: Lacuna, candidatos e orçamento restante.
Condição: Expansão vinculada à decisão bloqueada.
Aceite proposto: Carregar trecho irrelevante e impedir marcação como resolvido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S009, A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar analogia como padrão universal de memória virtual.
- Não chamar toda baixa confiança de page fault.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar completude verificável por contrato; esse mecanismo organiza necessidades, não descobre automaticamente todos os desconhecidos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T044, T062, T063, T067

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
