# T085 — Quantization

**Nome canônico:** Quantization  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T085  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** quantização

## T085:C01 — conceito

Família de representações numéricas que usa menos bits para pesos, ativações ou cache. Reduz armazenamento e pode reduzir tráfego de memória, mas ganho de velocidade depende de kernels compatíveis. Precisão do peso, precisão do cálculo e precisão do KV são decisões distintas.

Como funciona:
- Escolher tensores e grupos que receberão representação de menor precisão.
- Definir escalas, arredondamento e eventual ponto zero ou formato flutuante.
- Executar kernels que interpretem o formato, mantendo algumas operações em precisão maior quando necessário.

## T085:C02 — aplicacao

Quando usar:
- Modelo ou concorrência limitados por memória.
- Hardware com execução eficiente para o esquema escolhido.

Quando não usar:
- Escolher a menor quantidade de bits sem avaliar erro de tarefa e suporte real do runtime.

Implementação proposta:
- Criar baseline em precisão de referência e um conjunto de tarefas representativas.
- Quantizar com dados de calibração quando o método exigir e registrar sua procedência.
- Comparar arquivos, memória real, throughput e acerto no mesmo ambiente.

Aplicação LAI proposta:
Proposta LAI: escolher a quantização pelo custo de uma missão correta, incluindo retries e fallback, e não apenas por tokens por segundo.

## T085:C03 — riscos_validacao

Armadilhas:
- Arquivo pequeno não garante pequena memória total: KV, buffers e desquantização continuam existindo.
- Perplexidade semelhante pode esconder piora em ferramentas, números ou respostas estruturadas.

Métricas sugeridas:
- Memória de pico, tamanho do artefato e tempo por token.
- Taxa de acerto por tarefa e erros críticos frente ao baseline.

Testes propostos:
- Executar casos de extração exata e chamadas de ferramenta; exigir limite de regressão previamente definido.
- Testar maior contexto e concorrência pretendidos, incluindo aquecimento e operações temporárias.

## T085:C04 — perguntas_proveniencia

Pergunta: INT4 sempre é quatro vezes mais rápido que FP16?
Resposta: Não. A relação de bits dos pesos não determina a velocidade de todo o sistema.

Pergunta: Quantizar é treinar novas habilidades?
Resposta: Não. Em geral é reduzir a precisão de uma habilidade já aprendida, com possível perda.

Pergunta: Menos bits significam menos latência?
Resposta: Somente quando o caminho de execução explora a representação e a economia supera conversões e outros gargalos.

Pergunta: Uma escala serve para todos os contextos?
Resposta: Pode servir ao contrato escolhido, mas sua adequação deve ser testada também em distribuições diferentes da calibração.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T085:C05 — mecanismo_avancado

O orçamento de armazenamento depende de dados e metadados. Para N valores, b bits por valor, grupos de g valores e m bytes de escala ou zero por grupo, uma estimativa é N·b/8 + ceil(N/g)·m, antes de alinhamento e tensores mantidos em precisão maior. O dtype de armazenamento também não determina sozinho o dtype da multiplicação ou a velocidade do kernel.

Condição de contorno:
Reduzir bits pode apenas liberar capacidade quando descompactação, conversões ou operadores não quantizados dominam o tempo total.

Contrato proposto:
- Entradas: Pesos, dados de calibração quando exigidos, granularidade e kernel pretendido.
- Saídas: Artefato quantizado e relatório de erro, tamanho e operadores efetivamente usados.
- Estado: Escalas, zeros, layout, versão do artefato e tensores preservados.
- Invariante: A avaliação identifica precisamente quais valores foram quantizados e onde ocorre arredondamento.

Compromissos de projeto:
- Grupos menores adaptam melhor escalas, mas aumentam metadados.
- Calibração representativa custa trabalho e pode não cobrir mudanças de domínio.

## T085:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir ativações com outliers ausentes da calibração e verificar saturação, erro de logits e tarefa final. O simples carregamento do modelo não deve aprovar a conversão.

Plano de avaliação proposto:
Plano proposto: comparar com o mesmo checkpoint em maior precisão, controlando amostragem e backend. Separar memória de pesos, cache e temporários; medir qualidade, prefill e decode. Aceitar pela fronteira observada entre custo e perda tolerável.

Comparações:
- T086 (distinct_from): Quantizar pesos e quantizar cache modificam tensores e erros diferentes.

Afirmação rastreável:
SmoothQuant usa uma transformação equivalente para deslocar dificuldade de quantização das ativações para os pesos.
Suporte: direct; fontes: V3B-S003
Limite: A equivalência antecede a quantização; o arredondamento posterior continua sendo aproximado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T085:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 contabilizou metadados e distinguiu armazenamento de cálculo. Agora a decisão usa orçamento de erro por componente, mudança de domínio e qualidade pós-integração, tratando compressão como uma sequência de experimentos reversíveis e não como escolha isolada de bits.

Orçamento de erro composto
Separe os efeitos de quantizar pesos, ativações e KV. Teste cada alteração individualmente antes de combinar, pois pequenas perdas podem interagir em respostas longas ou raras. Defina quais erros são toleráveis por tarefa: falha de sintaxe, troca de entidade, omissão de exceção e erro numérico não têm o mesmo custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

Calibração como amostragem do uso
Construa um conjunto de calibração que represente comprimentos, idiomas e padrões de ferramentas. Reserve domínios e períodos posteriores para validação. Uma conversão excelente em texto geral pode distorcer canais importantes para código, números ou terminologia especializada; nenhum pequeno conjunto comprova robustez universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

Escolha pelo sistema final
Meça peso carregado, buffers temporários, cache e tempo de desquantização no runtime de destino. Uma representação mais compacta pode perder para outra com kernel melhor. Avalie também tempo de carregamento e capacidade de manter réplicas, porque o benefício operacional pode vir de maior concorrência, mesmo sem acelerar uma requisição isolada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

USO AVANÇADO — Especialista local de extração
Cenário: O modelo precisa caber em um dispositivo com orçamento fixo.
Estratégia: Compare uma base menor em maior precisão e uma base maior quantizada. Preserve o mesmo conjunto de documentos e verificador de campos. Escolha por resultados válidos dentro de prazo, incluindo entradas longas e categorias raras.
Papel do modelo pequeno: A faixa 3–7B pode vencer pela simplicidade; 8–14B só merece compressão se acrescentar qualidade mensurável.
Aceite proposto: Aceitar perda dentro do limite pré-definido por classe, sem ocultar regressões na média.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

USO AVANÇADO — Serviço de múltiplos especialistas
Cenário: Vários modelos ou adaptadores disputam memória de GPU.
Estratégia: Quantize primeiro componentes que liberam capacidade suficiente para aumentar réplicas ou reduzir preempção. Depois verifique comportamento combinado com cache e batching. Mantenha artefato de referência para reverter conversões problemáticas.
Papel do modelo pequeno: Um 15–30B pode tornar-se viável, mas memória total continua incluindo estados e temporários.
Aceite proposto: Comparar custo por tarefa aceita e SLO sob carga, não apenas tamanho do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S006, V3B-S003, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, preservar qualidade em tarefas estreitas pode importar mais que obter a menor representação possível.
8–14B: Em 8–14B, comparar técnicas com calibração do domínio e kernels realmente disponíveis no executor escolhido.
15–30B: Em 15–30B, quantização pode decidir viabilidade de memória; incluir margem para contexto e concorrência.
Requisitos de treino/runtime: PTQ usa calibração quando o método exige; QAT demanda treinamento; formatos e kernels devem ser compatíveis.
Não aplicar quando: Não reduzir bits de todos os tensores por padrão nem anunciar economia de memória como ganho equivalente de velocidade.

## T085:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Pilha Phi Silica publicada descreve quantização de pesos, com ressalva de revisão. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: A descrição técnica especifica quantização do modelo local.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q006.

## T085:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T085 → T198 [complements]
Como combinar: Recalibrar o critério de confiança após a conversão, pois probabilidades podem mudar.
Interface: Predições, rótulos independentes e revisão do artefato quantizado.
Condição: Há dados de validação fora da calibração numérica.
Aceite proposto: Comparar risco seletivo e taxa de abstenção antes/depois.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S006, V3B-S003, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T085 → T107 [complements]
Como combinar: Verificar se a redução de tráfego desloca o gargalo para cálculo ou conversão.
Interface: Bytes movimentados, kernels e latência por fase.
Condição: Profiler mede a execução real do formato escolhido.
Aceite proposto: Explicar a diferença entre ganho de capacidade e ganho de tempo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S006, V3B-S003, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Guardar base, receita de conversão e hashes do conjunto de calibração.
- Testar combinações de precisão, inclusive respostas longas e valores extremos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas especializadas contra a fronteira com o mesmo critério de correção. Compressão pode reduzir custo mantendo qualidade suficiente naquele recorte; não demonstra equivalência geral nem imunidade a erros raros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T086, T123, T124, T125, T126, T127

## Fontes primárias associadas

### B-S006 — Quantization — Overview

[https://huggingface.co/docs/transformers/main/en/quantization/overview](https://huggingface.co/docs/transformers/main/en/quantization/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Redução de bits para pesos e eventualmente ativações; necessidade de escolher formato e método compatíveis.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S003 — SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models

[https://arxiv.org/abs/2211.10438](https://arxiv.org/abs/2211.10438)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reescala equivalente antes da quantização e migração de dificuldade das ativações para pesos.

Limite: Resumo consultado; equivalência da reparametrização não elimina erro de arredondamento posterior.

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

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

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
