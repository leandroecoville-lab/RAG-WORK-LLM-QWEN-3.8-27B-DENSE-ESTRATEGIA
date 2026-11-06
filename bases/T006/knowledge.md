# T006 — Context Compression

**Nome canônico:** Context Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão de contexto

## T006:C01 — conceito

Família de métodos que reduz a representação entregue ao modelo: selecionar trechos, remover redundância, resumir ou usar representações aprendidas. É necessário declarar o tipo de compressão: texto legível, seleção extrativa e estados latentes têm requisitos e perdas diferentes.

Como funciona:
- Identificar informação obrigatória e redundância permitida.
- Escolher transformação compatível com a tarefa e o modelo.
- Preservar ligações para a informação original e avaliar o resultado.

## T006:C02 — aplicacao

Quando usar:
- Excesso de documentos ou histórico dentro do orçamento de entrada.
- Repetição extensa de instruções e resultados de ferramentas.

Quando não usar:
- Não comprimir cegamente código, números, negações ou evidências que exigem reprodução exata.

Implementação proposta:
- Proposta: definir orçamento por seção e lista de campos protegidos.
- Comparar uma linha de base sem compressão com versões em diferentes razões.
- Medir tempo do compressor junto da inferência e restaurar originais quando faltar evidência.

Aplicação LAI proposta:
Proposta LAI: aplicar primeiro seleção e deduplicação auditáveis; experimentar métodos aprendidos apenas quando a economia compensar a infraestrutura adicional.

## T006:C03 — riscos_validacao

Armadilhas:
- Texto menor pode exigir mais chamadas de recuperação.
- A compressão pode produzir uma síntese plausível que remove justamente a exceção relevante.

Métricas sugeridas:
- Razão entre tokens originais e enviados.
- Qualidade final, fidelidade factual e latência total.

Testes propostos:
- Inserir condições de exceção em posições variadas e conferir sua retenção.
- Usar perguntas com números próximos e rejeitar compressões que alterem valores.

## T006:C04 — perguntas_proveniencia

Pergunta: Comprimir contexto equivale a treinar o modelo?
Resposta: Não. Muitos métodos alteram apenas a entrada; alguns métodos latentes ou paramétricos exigem treinamento.

Pergunta: Menos tokens significa menor custo total?
Resposta: Só se a economia superar o custo da compressão, de buscas extras e de eventuais reexecuções.

Pergunta: Texto extraído garante fidelidade?
Resposta: Garante que os trechos selecionados vieram da entrada quando o processo é realmente extrativo. Não garante que o conjunto preservou o sentido e as condições do original.

Pergunta: Como interpretar uma compressão vazia?
Resposta: Como decisão de não acrescentar evidência, não como prova de que não existe resposta. O gerador precisa respeitar as regras de evidência da tarefa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T006:C05 — mecanismo_avancado

A função objetivo deve incluir custo do compressor, custo de leitura do resultado e perda na tarefa final. Uma representação curta que exige releituras frequentes pode custar mais que o original. Também importa definir suficiência: compressão para extração numérica exige preservar valores e condições, enquanto síntese temática pode tolerar detalhes ausentes. Não existe uma taxa que expresse todas essas perdas.

Condição de contorno:
O ganho desaparece quando compressão e reconstrução superam o trabalho economizado, ou quando o consumidor não entende a representação produzida.

Contrato proposto:
- Entradas: Conteúdo original, classe de tarefa, orçamento e consumidor identificado.
- Saídas: Representação reduzida com tipo declarado e vínculo à fonte.
- Estado: Versões do compressor, política de preservação e artefatos originais.
- Invariante: Uma saída latente não é tratada como texto intercambiável entre modelos incompatíveis.

Compromissos de projeto:
- Extração conserva palavras selecionadas, mas ainda pode remover relações e negações.
- Abstração integra informações dispersas, porém acrescenta risco de afirmações geradas sem suporte.

## T006:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comprimir um conjunto com exceção rara indispensável à decisão. O consumidor deve preservá-la ou reconhecer insuficiência; uma resposta confiante baseada apenas na regra geral constitui falha.

Plano de avaliação proposto:
Avaliação proposta: comparar entrada integral, seleção simples e compressor candidato com o mesmo modelo final. Medir custo total, suporte factual, respostas incorretas e releituras; escolher pela fronteira de custo e qualidade da tarefa.

Comparações:
- T020 (complements): Compressão aprendida é uma família particular que exige treinamento ou modelo especializado.
- T037 (complements): Condicionar à pergunta muda quais perdas são aceitáveis para a resposta atual.

Afirmação rastreável:
RECOMP oferece compressores extrativo e abstrativo e permite saída vazia quando a recuperação não acrescenta informação.
Suporte: direct; fontes: V3A-S003
Limite: O mecanismo publicado não estabelece que qualquer resumo curto melhora qualquer consumidor.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T006:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou custos de compressão. Aqui a estratégia escolhe representações diferentes por tipo de informação e consumidor.

Projeto e decomposição
Transforme tabelas em registros tipados e narrativa em trechos extraídos. Números, relações e ressalvas exigem representações diferentes; aplicar a mesma taxa a tudo desperdiça capacidade do leitor pequeno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

Controle adaptativo
Reserve passagem sem compressão para campos de alta sensibilidade e compacte redundâncias de apresentação. O compressor deve emitir mapa de cobertura por requisito, permitindo ampliar somente a parte insuficiente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

Validação contrafactual
Compare compressão uniforme, por tipo e ausência de compressão. Meça respostas sensíveis a unidade, exceção e atribuição de fonte, além de tokens. Unidade de avaliação: documento com consulta. Na validação, uma tabela deve conter o mesmo número em colunas com unidades diferentes e uma nota que altera apenas uma linha. A representação comprimida precisa conservar essas relações. Compare resposta com objeto estruturado, texto linearizado e resumo abstrativo; esse contraste localiza se o erro foi criado pelo parser, pelo compressor ou pela leitura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

USO AVANÇADO — Manual com especificações
Cenário: Texto mistura requisitos e explicações.
Estratégia: Extrair requisitos literalmente, resumir justificativas e manter tabelas estruturadas; reabrir se um requisito não puder ser ligado à seção.
Papel do modelo pequeno: 3–7B lê campos; 8–14B integra exceções.
Aceite proposto: Não perder valor, unidade ou condição obrigatória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

USO AVANÇADO — Dossiê repetitivo
Cenário: Vários documentos repetem o mesmo fato.
Estratégia: Agrupar duplicações por origem, preservar divergências e enviar exemplos representativos acompanhados da contagem de fontes independentes.
Papel do modelo pequeno: 15–30B sintetiza controvérsias.
Aceite proposto: Conservar posição minoritária documentada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de representação estruturada curta, sem reconstruir texto telegráfico complexo.
8–14B: Leitor misto de registros e trechos, apto a pedir expansão específica.
15–30B: Integrador de múltiplas representações com verificador de consistência.
Requisitos de treino/runtime: Parser de tipos, mapa de cobertura e tokenizer do consumidor; treinamento opcional para leitura comprimida.
Não aplicar quando: O compressor altera relação entre condições ou custa mais que a leitura integral.

## T006:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.
Mecanismo documentado: Aplicação específica de um modelo local para condensar transcrições.
Correspondência com esta base: Resumo é redução de conteúdo, mas não comprova algoritmo específico de compressão contextual.
Transferência proposta para modelo pequeno: Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.
Limite: Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.
Fontes: V4D-S005.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Compressão de prompt é recurso do runtime NPU; a fonte não prova sua ativação em toda ação Click to Do.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação expõe ferramenta de compressão utilizável em fluxo.
Mecanismo documentado: Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.
Correspondência com esta base: Compressão textual explícita.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.
Limite: Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S027.

V4D-C004 — Google / Chrome built-in AI / Summarizer API
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação lista a Summarizer API no Chrome estável desde a versão 138.
Mecanismo documentado: Interface local de geração com modelo gerenciado pelo navegador e requisitos de disponibilidade.
Correspondência com esta base: Sumarização acessível via API; não demonstra técnica particular de poda/compressão.
Transferência proposta para modelo pequeno: Proposta: detectar disponibilidade local e limitar a tarefa a texto fornecido; manter o contrato de saída igual quando um backend alternativo for necessário.
Limite: Disponibilidade não constitui prova de implantação em cliente, volume de tráfego ou porte exato do modelo. As etapas de preview e estável precisam ser verificadas por API.
Fontes: V4D-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## T006:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T006 → T033 [requires]
Como combinar: Identificar tipos antes de compactar.
Interface: Seções, tabelas, listas e seus identificadores.
Condição: Parser preservar unidades e fronteiras.
Aceite proposto: Verificar casos com tabela atravessando páginas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T006 → T044 [complements]
Como combinar: Expandir apenas o requisito insuficiente.
Interface: Lacuna, referência e orçamento restante.
Condição: Original permanecer acessível.
Aceite proposto: Medir releitura e recuperação da condição omitida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não declarar compressão sem perda sem prova.
- Preservar distinção entre citação literal e paráfrase.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar qualidade final por tipo de informação; compressão bem lida por fronteira pode falhar em 3–7B.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T018, T020, T021, T043, T052

## Fontes primárias associadas

### A-S015 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models

[https://aclanthology.org/2023.emnlp-main.825/](https://aclanthology.org/2023.emnlp-main.825/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão textual com orçamento e seleção iterativa de tokens.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S016 — Compressing Context to Enhance Inference Efficiency of Large Language Models

[https://aclanthology.org/2023.emnlp-main.391/](https://aclanthology.org/2023.emnlp-main.391/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Selective Context: remoção de redundância no contexto de entrada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S003 — RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation

[https://arxiv.org/abs/2310.04408](https://arxiv.org/abs/2310.04408)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressores extrativo e abstrativo orientados à tarefa; possibilidade de retornar contexto vazio quando não agrega informação.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

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

### V4D-S003 — Get started with Phi Silica in the Windows App SDK

[https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução local; diferenças NPU/GPU; especulação com modelo de rascunho na NPU; preparação do modelo e transição anunciada para Aion Instruct.

Limite: Página mutável consultada em 2026-11-05. Rollout retail/removação em janeiro de 2027 é plano futuro. Especulação e compressão NPU não estão disponíveis no caminho GPU descrito; não inferir equivalência entre revisões.

### V4D-S004 — Manage Click to Do

[https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ações locais de texto do Click to Do usam Phi Silica em Copilot+ PCs; resposta exibida progressivamente e controles de administração.

Limite: Não demonstra memória persistente aprendida. Ação e seleção da interface não provam qual técnica de compressão interna foi utilizada em cada chamada.

### V4D-S005 — Pixel December 2023 feature drop

[https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Lançamento de Gemini Nano em Pixel 8 Pro e resumo offline no Recorder.

Limite: Não identifica o checkpoint nem sua contagem de parâmetros. Smart Reply no Gboard era developer preview; não confundir resumo com cadeia hierárquica ou destilação.

### V4D-S007 — Built-in AI APIs

[https://developer.chrome.com/docs/ai/built-in-apis](https://developer.chrome.com/docs/ai/built-in-apis)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade e estágio das APIs locais do Chrome; Summarizer documentado como estável desde Chrome 138.

Limite: Tabela é mutável e partes textuais podem acompanhar versões em ritmos diferentes. API disponível não comprova uso por cliente; não identifica porte exato do checkpoint.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
