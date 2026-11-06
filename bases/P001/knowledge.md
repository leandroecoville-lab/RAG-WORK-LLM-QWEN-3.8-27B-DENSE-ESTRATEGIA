# P001 — Context Engine

**Nome canônico:** Context Engine  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P001  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** motor proposto de preparação de contexto

## P001:C01 — conceito

Context Engine é um nome editorial proposto para a cadeia que transforma uma solicitação, seu estado e evidências recuperadas na entrada efetiva do modelo. Sua entrega seria um pacote de contexto acompanhado de manifesto: fontes, versões, trechos, prioridades e tokens. As fontes fundamentam engenharia de contexto e recuperação; não demonstram um componente LAI implementado com esse nome.

Como funciona:
- Receber objetivo atual, contrato de resposta, modelo escolhido e orçamento fornecido pelo gestor de contexto.
- Consultar fontes autorizadas, normalizar resultados e eliminar redundância sem apagar divergências relevantes.
- Ordenar instruções e evidências, reservando espaço para a resposta e preservando referências aos documentos originais.

## P001:C02 — aplicacao

Quando usar:
- Tarefas que combinam histórico, arquivos e ferramentas, exigindo uma entrada reconstruível e mensurável.

Quando não usar:
- Como substituto da persistência de memória, do roteamento de modelos ou da validação da resposta produzida.

Implementação proposta:
- Proposta: definir uma função build_context que recebe versões explícitas e devolve mensagens, manifesto e estado de completude.
- Dividir a preparação em recuperação, seleção, extração e empacotamento; atribuir orçamento de tokens a cada etapa.
- Quando uma evidência necessária não couber, buscar um trecho menor ou declarar contexto insuficiente; manter rastreável o descarte.

Aplicação LAI proposta:
Proposta LAI: usar P001 como pipeline de montagem, P002 para orçamento e P007 para busca, devolvendo ao executor um manifesto verificável antes da inferência.

## P001:C03 — riscos_validacao

Armadilhas:
- Uma apresentação organizada pode ocultar evidência incompleta; o manifesto deve indicar lacunas e conflitos.
- Reutilizar contexto montado para outro modelo pode ultrapassar seu limite ou alterar a contagem de tokens.

Métricas sugeridas:
- Tempo de preparação, tokens por fonte, cobertura das evidências necessárias e incidência de referências não resolvidas.

Testes propostos:
- Aceite proposto: reconstruir o mesmo pacote a partir das mesmas entradas versionadas, com ordem determinística quando aplicável.
- Testar fontes contraditórias e uma evidência que exceda a cota; conferir preservação do conflito e explicação da insuficiência.

## P001:C04 — perguntas_proveniencia

Pergunta: Qual artefato permitiria explicar o que o modelo recebeu?
Resposta: O manifesto do contexto, vinculado às mensagens efetivas e contendo IDs, versões, recortes e decisões de inclusão.

Pergunta: O Context Engine decidiria sozinho qual memória é verdadeira?
Resposta: Não. Ele deve carregar evidências e conflitos; reconciliação de memória e verificação possuem contratos próprios.

Pergunta: Como localizar um erro do motor?
Resposta: Compare candidatos recuperados, seleção e contexto final; uma fonte encontrada pode ter sido excluída na montagem.

Pergunta: O que aceitar como saída válida?
Resposta: Contexto dentro do orçamento com requisitos preservados, referências resolvíveis e decisões de exclusão observáveis.

Escopo das fontes:
Fontes apoiam montagem seletiva e recuperação; nome, interfaces e critérios de aceite são propostas editoriais.

## P001:C05 — mecanismo_avancado

Propõe-se que Context Engine produza um artefato de contexto, com versão e proveniência, antes da chamada ao modelo. A composição deve contabilizar instruções, schemas de ferramentas, histórico, evidências e reserva de saída. A seleção precisa tratar dependências: incluir uma conclusão sem sua condição ou uma alteração sem a versão de origem pode reduzir tokens e destruir o significado. O motor deve expor motivos de inclusão e exclusão, permitindo investigar falhas de recuperação e montagem separadamente.

Condição de contorno:
O orçamento calculado depende do tokenizer e do protocolo realmente usados pelo servidor. Uma estimativa local não substitui a contagem do provedor quando existe diferença de serialização.

Contrato proposto:
- Entradas: Tarefa, identidade autorizada, snapshot de memória, candidatos recuperados, ferramentas elegíveis e orçamento do modelo.
- Saídas: Contexto serializado, manifesto de evidências, contagem ou estimativa de tokens e justificativas de seleção.
- Estado: Versão da política de montagem, tokenizer, snapshot dos insumos e relações entre evidências e referências.
- Invariante: Nenhum trecho deve perder sua identidade de fonte; exclusões não podem remover silenciosamente requisitos obrigatórios da tarefa.

Compromissos de projeto:
- Montagem determinística facilita auditoria, enquanto seleção adaptativa pode melhorar relevância e introduzir variação.
- Preservar dependências consome mais tokens por evidência, mas evita trechos isolados que induzem interpretação errada.

## P001:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: fornecer duas versões contraditórias de um requisito e um limite insuficiente; exigir explicitação da versão escolhida ou insuficiência, sem combinar silenciosamente afirmações incompatíveis.

Plano de avaliação proposto:
Comparar montagem por ordem de chegada e composição com orçamento no mesmo conjunto de tarefas. Medir cobertura dos requisitos, fidelidade das citações, tokens e respostas aceitas. Avaliar exclusões manualmente em uma amostra reservada.

Comparações:
- T024 (complements): Context Broker e Builder podem realizar aquisição e composição.
- T152 (complements): A alocação de tokens fornece o limite de montagem.

Afirmação rastreável:
Engenharia de contexto abrange a seleção de informações disponíveis durante a inferência.
Suporte: related; fontes: V3D-S021
Limite: A fonte sustenta o problema; Context Engine e este contrato são uma proposta editorial própria.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P001:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu montagem e manifesto. Aqui Context Engine é proposto como compilador de necessidades de evidência em pacotes próprios para cada consumidor.

Projeto e decomposição
Receber tarefa e decompor saída em afirmações ou ações com requisitos. Cada requisito recebe tipo de suporte, prioridade e condição de insuficiência; o contexto deixa de ser simples concatenação de documentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

Controle adaptativo
Montar uma representação conforme o leitor: campos explícitos para extrator pequeno, pares de evidência para comparador e panorama com referências para integrador. A transformação deve preservar identidade dos fatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

Validação contrafactual
Comparar pacote único e compilação por papel com mesmas fontes. Medir suporte por afirmação, tokens inúteis e diferenças introduzidas pela representação; organização não autoriza adicionar conhecimento. Unidade de avaliação: pacote de contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

USO AVANÇADO — Pipeline local de análise
Cenário: Extração e síntese usam modelos diferentes.
Estratégia: Compilar campos para 3–7B, consolidar resultados em código e fornecer ao integrador somente evidências e conflitos. Reabrir fonte quando campo não tiver suporte.
Papel do modelo pequeno: 3–7B extrai; 15–30B integra.
Aceite proposto: Nenhuma afirmação final pode perder vínculo com evidência original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

USO AVANÇADO — Resposta sob prazo
Cenário: Nem todas as fontes chegam a tempo.
Estratégia: Priorizar requisitos essenciais, produzir pacote parcial explícito e bloquear conclusões que dependam de fonte pendente.
Papel do modelo pequeno: 8–14B responde escopo coberto.
Aceite proposto: Completude declarada deve coincidir com requisitos efetivamente sustentados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de pacotes tipados por campo, com pouca ambiguidade.
8–14B: Leitor de pacotes comparativos e exceções locais.
15–30B: Integrador de afirmações interdependentes com expansão dirigida.
Requisitos de treino/runtime: Modelo de requisitos, manifesto de transformações e perfis de consumidor; componente LAI é proposta editorial, não software verificado.
Não aplicar quando: A tarefa não pode ser decomposta sem perder significado e o pacote omite dependências essenciais.

## P001:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4A-C002 — Anthropic / Research multi-agent system
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A equipe descreve passagem do protótipo à produção do recurso Research.
Mecanismo documentado: Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.
Correspondência com esta base: Inspira montagem de contexto; não comprova Context Engine LAI.
Transferência proposta para modelo pequeno: Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.
Limite: Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q020.

## P001:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P001 → P007 [requires]
Como combinar: Solicitar evidência por requisito e escopo.
Interface: requirement_id, consulta, filtros e tipo de suporte.
Condição: Retriever devolver proveniência e lacunas.
Aceite proposto: Recuperar documento correto que não sustenta o requisito e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P001 → P002 [requires]
Como combinar: Negociar limite de contexto antes de compilar.
Interface: Perfil do modelo, reserva e cotas por requisito.
Condição: Conjunto obrigatório caber ou gerar insuficiência.
Aceite proposto: Trocar para modelo menor e recalcular pacote.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

3. P001 → T200 [feeds]
Como combinar: Entregar manifesto à verificação da resposta.
Interface: Afirmações, fontes e transformações aplicadas.
Condição: Verificador acessar originais quando necessário.
Aceite proposto: Detectar citação que aponta fonte verdadeira mas não suporta a frase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir contexto bem organizado com evidência completa.
- Não promover texto recuperado a instrução da aplicação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar leitor pequeno com pacote compilado e fronteira com fontes equivalentes; não prometer paridade geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T024, T009, T032, P002, P007, P009

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S003 — ParentDocumentRetriever — source code

[https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores parent_splitter e child_splitter, indexação dos filhos e retorno dos pais por IDs.

Limite: Código de referência consultado em branch móvel. A página da API anterior retornou content-type não suportado; o código oficial foi aberto e inspecionado. Não atesta implantação local.

### V3D-S021 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Curadoria iterativa de contexto, seleção de informações e restrições da janela.

Limite: Artigo de engenharia, não prova experimental dos componentes arquiteturais propostos neste pacote.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
