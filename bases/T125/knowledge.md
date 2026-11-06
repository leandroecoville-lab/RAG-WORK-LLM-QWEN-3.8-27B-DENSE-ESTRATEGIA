# T125 — GPTQ

**Nome canônico:** GPTQ  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T125  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** post-training weight quantization GPTQ

## T125:C01 — conceito

Método de quantização de pesos após treinamento que usa informação aproximada de segunda ordem para controlar o erro introduzido na conversão. É um algoritmo, distinto de bibliotecas e formatos que o implementam. Exige considerar calibração e compatibilidade do artefato com o kernel de inferência.

Como funciona:
- Observar entradas representativas das camadas para estimar sensibilidade.
- Quantizar grupos de pesos com compensação do erro no procedimento escolhido.
- Salvar os pesos empacotados e metadados requeridos pelo runtime.

## T125:C02 — aplicacao

Quando usar:
- Há modelo de referência e necessidade de reduzir armazenamento de pesos.
- Existe implementação GPTQ mantida e compatível com o modelo/hardware.

Quando não usar:
- Utilizar apenas o nome GPTQ como garantia de qualidade ou de compatibilidade entre ferramentas.

Implementação proposta:
- Separar conjunto de calibração e avaliação, mantendo textos e tarefas representativos.
- Registrar bits, group size, ordenação e demais parâmetros da implementação.
- Comparar com outro método sob memória, runtime e conjunto de tarefas equivalentes.

Aplicação LAI proposta:
Proposta LAI: comparar GPTQ e a receita já usada no modelo local com dados reais de tarefa e custo de fallback; não escolher pela sigla.

## T125:C03 — riscos_validacao

Armadilhas:
- Calibração estreita pode favorecer um domínio e degradar outro.
- Diferenças de layout e versão podem impedir carregamento mesmo com o mesmo número de bits.

Métricas sugeridas:
- Erro de tarefa, tamanho dos pesos e memória máxima.
- Tempo por token e custo de quantização, registrados separadamente.

Testes propostos:
- Validar o checkpoint quantizado no runtime de destino e comparar saídas em casos de ferramenta e extração.
- Avaliar dados fora da calibração para detectar deterioração que uma avaliação sobre os mesmos textos esconderia.

## T125:C04 — perguntas_proveniencia

Pergunta: GPTQ é um modelo?
Resposta: Não. É um método para reduzir precisão dos pesos de um modelo já treinado.

Pergunta: O resultado mantém todas as habilidades?
Resposta: Não há garantia universal; depende do checkpoint, calibração, configuração e avaliação do domínio.

Pergunta: Por que magnitude do peso não basta?
Resposta: O efeito do erro depende de quais entradas o multiplicam e de suas correlações.

Pergunta: PTQ significa nenhum dado?
Resposta: Não. O método pode dispensar treino por gradientes do modelo completo e ainda exigir ativações representativas para calibração.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T125:C05 — mecanismo_avancado

O objetivo de reconstrução por camada pondera erro de pesos pelas entradas observadas: minimizar uma expressão como ||WX−WqX||² difere de minimizar apenas ||W−Wq||². A aproximação de curvatura depende de XXᵀ, portanto correlações da calibração influenciam compensações. O procedimento atualiza pesos ainda não quantizados para absorver parte do erro introduzido, exigindo estabilidade numérica na representação da informação de segunda ordem.

Condição de contorno:
Calibração estreita pode preservar bem suas ativações e representar mal entradas com correlações diferentes.

Contrato proposto:
- Entradas: Pesos da camada, ativações de calibração, agrupamento e estabilização numérica.
- Saídas: Pesos quantizados com metadados e erro de reconstrução registrado.
- Estado: Informação aproximada de curvatura, ordem de processamento e compensações pendentes.
- Invariante: A compensação usa estatísticas correspondentes à camada e às entradas realmente calibradas.

Compromissos de projeto:
- Calibração mais diversa custa coleta e pode melhorar cobertura.
- Aproximação de segunda ordem adiciona trabalho offline e não remove erro de quantização.

## T125:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: calibrar em entradas quase colineares e avaliar um domínio com outras correlações. Verificar estabilidade da fatoração, erro de reconstrução e degradação fora da amostra.

Plano de avaliação proposto:
Plano proposto: comparar arredondamento simples e GPTQ com mesmo orçamento de bits, grupos e dados. Separar erro local, qualidade final e custo de conversão; aceitar pelo conjunto de validação independente e pelo kernel de destino.

Comparações:
- T126 (alternative): AWQ orienta reescala por ativações; GPTQ usa compensações ligadas à reconstrução de camada.

Afirmação rastreável:
O GPTQ utiliza informação aproximada de segunda ordem e atualiza pesos restantes durante a quantização.
Suporte: direct; fontes: V3B-S013
Limite: A qualidade de reconstrução em uma camada não garante desempenho de toda tarefa ou de domínios não vistos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T125:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou reconstrução ponderada por ativações. Esta camada trata curadoria de calibração, composição dos erros entre camadas e rastreabilidade de escolhas numéricas.

Calibração por comportamento
Selecione exemplos que representem tarefas, formatos e comprimentos reais, sem contaminar avaliação. Uma coleção genérica pode deixar módulos pouco exercitados no domínio. Registre tokens processados e distribuição por categoria; quantidade de exemplos não informa sozinha a cobertura de ativações relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

Erro que se propaga
Baixo erro local de reconstrução não garante baixo erro na saída final. Camadas quantizadas alteram entradas das seguintes, e avaliação autoregressiva acumula diferenças nas continuações. Compare reconstrução por camada, logits e tarefas completas; nenhuma dessas medidas substitui as outras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

Estabilidade e escolhas
Agrupamento, ordem de processamento e estabilização influenciam o artefato. Preserve parâmetros e logs, incluindo falhas de fatoração ou fallback. Ajustar esses valores para melhorar um conjunto pequeno de testes pode gerar sobreajuste do processo de quantização; reserve uma validação independente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

USO AVANÇADO — Modelo de domínio numérico
Cenário: Pequenos erros afetam respostas estruturadas ou cálculo.
Estratégia: Calibre com dados de formato semelhante e use ferramentas externas para verificar resultados. Examine categorias sensíveis antes de decidir se certas camadas ficam em precisão maior.
Papel do modelo pequeno: Um 8–14B pode continuar útil quando cálculo e validação são delegados a ferramentas.
Aceite proposto: Comparar taxa de erro por categoria com referência de maior precisão e com o mesmo verificador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

USO AVANÇADO — Pipeline reproduzível de distribuição
Cenário: Várias versões do modelo serão quantizadas.
Estratégia: Versione base, calibração, parâmetros, código e formato de saída. Automatize inspeção de metadados e teste de carregamento; aprove cada versão com uma avaliação separada.
Papel do modelo pequeno: Modelos 3–7B permitem ciclos de validação rápidos, sem dispensar cobertura de casos críticos.
Aceite proposto: Reproduzir artefatos ou explicar diferenças com manifests completos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S013, V4D-S009, B-S035.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: A economia pode facilitar implantação local; avalie se o processo de calibração compensa o objetivo.
8–14B: Mantenha variedade de tarefas e comprimentos; um único domínio textual estreito pode esconder perdas.
15–30B: Quantização de 15–30B exige recursos para calibração e buffers, não somente para o arquivo final.
Requisitos de treino/runtime: Método pós-treino com dados de calibração e runtime compatível. A menção no Phi Silica não fixa uma receita aplicável a outro modelo.
Não aplicar quando: Não usar métricas de reconstrução como prova de correção factual ou de compatibilidade de kernel.

## T125:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Implementação publicada usa GPTQ em pesos rotacionados; não afirmar que todo backend atual é idêntico. Escopo: configuração técnica publicada em 2024-12-06, não confirmação de todos os detalhes da API atual.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q006.

## T125:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T125 → T124 [feeds]
Como combinar: GPTQ pode gerar uma representação de pesos de quatro bits com metadados próprios.
Interface: Códigos, escalas, grupos e layout.
Condição: Consumidor implementa a representação específica.
Aceite proposto: Conferir saída de camadas após exportação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S013, V4D-S009, B-S035. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T125 → T198 [complements]
Como combinar: Perdas de quantização podem alterar calibração de confiança e precisam de nova medição.
Interface: Predições e resultados rotulados por versão.
Condição: Conjunto independente do usado para calibrar pesos.
Aceite proposto: Comparar confiabilidade por faixa sem presumir preservação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S013, V4D-S009, B-S035. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter conjunto de avaliação fora da calibração e da escolha de hiperparâmetros.
- Registrar exceções de precisão e fallback para não rotular artefatos diferentes como idênticos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação correta primeiro mede a diferença causada por GPTQ e depois a adequação à tarefa frente a fronteira. Um bom erro de reconstrução não estabelece equivalência de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T124, T126

## Fontes primárias associadas

### B-S035 — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers

[https://arxiv.org/abs/2210.17323](https://arxiv.org/abs/2210.17323)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Quantização de pesos pós-treino usando aproximação de informação de segunda ordem.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S013 — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers — full text

[https://arxiv.org/html/2210.17323v2](https://arxiv.org/html/2210.17323v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetivo quadrático de reconstrução por camada, Hessiana aproximada, compensação de erro e estabilidade.

Limite: Seções metodológicas consultadas; calibração e resultados publicados não validam checkpoints locais.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
