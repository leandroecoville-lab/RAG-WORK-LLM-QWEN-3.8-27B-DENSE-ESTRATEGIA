# T009 — RAG — Retrieval-Augmented Generation; incluindo RAG temporal

**Nome canônico:** RAG com filtragem temporal explícita  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T009  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** RAG — Retrieval-Augmented Generation; Retrieval-Augmented Generation; geração aumentada por recuperação; RAG temporal; temporal retrieval-augmented generation

## T009:C01 — conceito

RAG recupera informação externa e a fornece à geração para fundamentar respostas. RAG temporal acrescenta uma interpretação explícita de quando a evidência vale e, quando necessário, de quando passou a ser conhecida pelo sistema. Não constitui um algoritmo único: combina recuperação com modelagem temporal, versionamento e critérios de citação. Nem recuperação nem recência garantem verdade.

Como funciona:
- Transformar a pergunta em consulta, escopo de acesso e referência temporal; distinguir “válido em junho” de “o que sabíamos em junho”.
- Filtrar versões elegíveis por intervalos de validade e de registro antes da seleção final de evidências.
- Combinar busca lexical ou vetorial, reranking e geração com documento, versão, trecho e datas verificáveis.

## T009:C02 — aplicacao

Quando usar:
- Políticas que mudam, contratos com vigência, histórico de projetos e decisões que precisam ser reconstruídas como eram em determinada data.

Quando não usar:
- Para substituir consultas transacionais exatas ou inferir uma data ausente apenas porque o documento foi indexado recentemente.

Implementação proposta:
- Proposta: armazenar valid_from/valid_to e recorded_from/recorded_to, além de origem, identidade e controle de acesso; adotar convenção explícita para limites dos intervalos.
- Preservar correções tardias como novas versões. Indexação recente de um documento antigo não muda a data de validade do fato.
- Ao faltar data ou existir conflito, retornar a limitação e evidências concorrentes; não escolher silenciosamente a versão com maior similaridade.

Aplicação LAI proposta:
Proposta LAI: exigir data de referência em consultas de evolução do projeto e manter citações que permitam reconstruir o estado consultado.

## T009:C03 — riscos_validacao

Armadilhas:
- Recency boosting sozinho favorece documentos novos, mas não responde consultas históricas.
- Filtrar depois de top-k pequeno pode deixar de fora toda evidência temporalmente correta.

Métricas sugeridas:
- Recall de evidências elegíveis, acurácia das respostas históricas, vazamento de versões futuras e suporte das citações.

Testes propostos:
- Teste proposto: cadastrar uma regra de janeiro e substituição de março; perguntas sobre fevereiro e abril devem selecionar versões diferentes.
- Inserir em maio uma correção retroativa e testar separadamente validade histórica e conhecimento disponível antes da correção.

## T009:C04 — perguntas_proveniencia

Pergunta: Ordenar documentos por data de publicação já produz RAG temporal?
Resposta: É apenas uma heurística de recência. Consultas temporais exigem interpretar a pergunta e verificar quais versões eram válidas no intervalo solicitado.

Pergunta: Uma correção recebida hoje deve alterar toda resposta sobre o passado?
Resposta: Depende da pergunta: pode corrigir o fato historicamente válido, mas não o que o sistema sabia antes de recebê-la.

Pergunta: Uma citação correta garante resposta correta?
Resposta: Não. O trecho pode existir e ainda ser mal interpretado, estar fora do corte temporal ou não sustentar a conclusão apresentada.

Pergunta: Quando não recuperar é aceitável?
Resposta: Quando o contrato da tarefa dispensa evidência externa e a decisão é justificada. Uma pergunta factual atual ou histórica pode exigir busca mesmo que pareça simples.

Escopo das fontes:
O artigo RAG fundamenta recuperação mais geração; XTDB fundamenta validade e tempo de sistema. A combinação e o contrato temporal LAI são propostas de arquitetura.

## T009:C05 — mecanismo_avancado

A qualidade final resulta de etapas separáveis: existir evidência elegível, recuperá-la, preservar seu sentido no contexto e usá-la corretamente. RAG temporal acrescenta filtros de validade e conhecimento: uma correção publicada hoje pode mudar a resposta sobre ontem sem mudar o que o sistema sabia ontem. Avaliar só similaridade do trecho mistura erros de indexação, tempo e leitura.

Condição de contorno:
Se o acervo não contém evidência suficiente ou as datas representam publicação sem validade de domínio, recuperação não pode fabricar uma resposta temporal bem definida.

Contrato proposto:
- Entradas: Pergunta, escopo, instante de validade e eventual instante de conhecimento.
- Saídas: Resposta com evidências elegíveis, versões e lacunas explicitadas.
- Estado: Índices por revisão, metadados temporais e registro dos candidatos utilizados.
- Invariante: Nenhuma evidência posterior ao corte de conhecimento é apresentada como já conhecida naquele corte.

Compromissos de projeto:
- Filtros temporais rígidos aumentam precisão histórica, mas exigem metadados confiáveis.
- Mais candidatos ampliam cobertura e também ruído, custo e oportunidades de contradição.

## T009:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um fato válido no passado e uma correção registrada depois. Perguntas sobre o passado segundo conhecimento atual e segundo conhecimento antigo devem produzir resultados compatíveis com seus cortes diferentes.

Plano de avaliação proposto:
Avaliação proposta: isolar recuperação e leitura usando candidatos conhecidos e depois o pipeline completo. Medir evidência elegível recuperada, atribuição, atualização e abstenção; comparar com busca sem filtro temporal sobre o mesmo corpus.

Comparações:
- T056 (complements): Bitemporalidade explicita os dois cortes necessários a consultas históricas mais rigorosas.
- T025 (complements): Adaptive RAG decide estratégias adicionais de recuperação conforme a necessidade observada.

Afirmação rastreável:
LongMemEval distingue atualização de conhecimento, raciocínio temporal e abstenção como capacidades de memória.
Suporte: related; fontes: V3A-S002
Limite: A avaliação de memória apoia a separação de capacidades; o contrato temporal proposto não é uma API do benchmark.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T009:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou recuperação temporal e leitura. Aqui o desenho novo é orçamento de evidência orientado por tipo de afirmação e custo do erro.

Projeto e decomposição
Classifique a resposta em afirmações verificáveis antes de preencher contexto. Uma data exige fonte exata; uma comparação exige evidências simétricas; um panorama exige diversidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

Controle adaptativo
Monte pacotes por afirmação com apoio, contradição e lacuna. O leitor pequeno deve decidir somente dentro do pacote, sem completar campos ausentes com lembrança paramétrica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

Validação contrafactual
Compare recuperação única e pacotes de evidência mantendo o mesmo corpus. Conte respostas parcialmente corretas e citações que não sustentam a frase. Unidade de avaliação: pergunta com evidências. Use casos em que o documento recuperado é correto, mas o trecho não sustenta o atributo pedido. O sistema deve marcar essa célula como insuficiente, em vez de premiar a presença de uma citação. Para comparações, medir cobertura por alternativa impede que a opção mais documentada pareça melhor apenas por receber mais contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

USO AVANÇADO — Comparação de produtos técnicos
Cenário: Atributos vêm de documentos diferentes.
Estratégia: Recuperar cada atributo por item, normalizar unidades em código e gerar tabela com células ausentes explícitas.
Papel do modelo pequeno: 3–7B extrai; 8–14B redige comparação.
Aceite proposto: Cada célula preenchida precisa de suporte elegível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

USO AVANÇADO — Investigação de divergência
Cenário: Duas fontes discordam sobre uma decisão.
Estratégia: Recuperar versões e contexto de autoria, separar conflito factual de diferença de escopo e evitar votação por quantidade.
Papel do modelo pequeno: 15–30B integra versões incompatíveis.
Aceite proposto: Resposta deve preservar conflito ainda não resolvido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor extrativo de pacotes pequenos com abstenção por campo.
8–14B: Leitor especializado em citações e comparação de poucas fontes.
15–30B: Integrador multietapas quando cada elo possuir evidência recuperável.
Requisitos de treino/runtime: Esquema por afirmação, filtros e referências estáveis; especialização contextual é opcional, não garantia.
Não aplicar quando: As fontes necessárias não existem ou o objetivo exige descoberta que o corpus não sustenta.

## T009:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Recuperação antecede geração e inclui múltiplas fontes.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Documentação oferece índice semântico para Chat e cloud agent.
Mecanismo documentado: Busca de seções de código por significado e atualização do índice.
Correspondência com esta base: Contexto recuperado do repositório orienta respostas.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.
Limite: Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S023.

V4A-C020 — Google / NotebookLM com fontes multimodais
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Produto oferece análise de documentos, áudio e vídeo com citações.
Mecanismo documentado: Conteúdo de fontes e transcrições fundamenta respostas referenciadas.
Correspondência com esta base: Fundamentação em fontes é relacionada, sem pipeline interno publicado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.
Limite: Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S025.

V4A-C021 — Google DeepMind / DataGemma RIG/RAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto publica variantes para fundamentar geração em Data Commons.
Mecanismo documentado: RIG troca números por dados; RAG usa modelo Gemma para preparar contexto de Gemini 1.5 Pro.
Correspondência com esta base: Recuperação contextual é objetivo explícito.
Transferência proposta para modelo pequeno: Proposta de engenharia: Testar roteador pequeno para consulta estatística, mantendo unidade, período e população.
Limite: RAG citado não é pipeline integral 3–30B; não há implantação de usuário comprovada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S014.

V4A-C022 — Salesforce / SFR-RAG 9B
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa apresenta modelo de nove bilhões especializado em fidelidade contextual.
Mecanismo documentado: Pós-treino privilegia leitura de evidência, citações e reconhecimento de insuficiência.
Correspondência com esta base: Leitor especializado para RAG.
Transferência proposta para modelo pequeno: Proposta de engenharia: Considerar leitor 8–14B especializado e comparar com modelo geral do mesmo porte.
Limite: Resultados experimentais publicados não garantem produção nem superioridade universal; nenhuma pergunta de benchmark foi incorporada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S019.

V4B-C025 — Google DeepMind / RETRO
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: O trabalho avalia um modelo treinado para consumir trechos recuperados por uma arquitetura específica de atenção.
Mecanismo documentado: Codificação de vizinhos recuperados e cross-attention por trechos fazem parte da função treinada.
Correspondência com esta base: A família usa conhecimento recuperado, mas não equivale a anexar trechos a um prompt comum.
Transferência proposta para modelo pequeno: Proposta: estudar custo e benefício de arquitetura treinada versus RAG externo antes de escolher uma intervenção em 3–30B.
Limite: Pesquisa não comprova produto implantado. Alterar um checkpoint convencional para reproduzir RETRO requer treinamento e compatibilidade; não é uma opção intercambiável de serving.
Fontes: B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q010, V4A-Q016, V4A-Q020.

## T009:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T009 → T028 [complements]
Como combinar: Ordenar candidatos por necessidade de evidência.
Interface: claim_id, candidato e tipo de suporte.
Condição: Reranker não excluir contradições obrigatórias.
Aceite proposto: Avaliar cobertura por afirmação, além do ranking global.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S019, V4A-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T009 → T200 [requires]
Como combinar: Verificar suporte após geração.
Interface: Frase, citação e trecho utilizado.
Condição: Verificador acessar a origem exata.
Aceite proposto: Detectar citação verdadeira mas irrelevante para a frase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S019, V4A-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não converter ausência de documento em prova de inexistência.
- Separar dados recuperados de instruções de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar fidelidade contextual e abstenção; capacidade geral do modelo permanece fora da conclusão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T027, T056, T072, P007

## Fontes primárias associadas

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

### V3A-S009 — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

[https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação e crítica adaptativas aprendidas com tokens de reflexão; distingue arquitetura treinada de simples instrução de autocrítica.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S014 — DataGemma

[https://deepmind.google/models/gemma/datagemma/](https://deepmind.google/models/gemma/datagemma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RIG substitui números por dados; variante RAG prepara contexto consumido por Gemini 1.5 Pro.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### B-S026 — Improving language models by retrieving from trillions of tokens

[https://arxiv.org/abs/2112.04426](https://arxiv.org/abs/2112.04426)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RETRO combina recuperação, codificador e cross-attention por trechos.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews

[https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto fundamentado em fontes com citações e transcrições; recursos disponíveis.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
