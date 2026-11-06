# T092 — FlashAttention-3

**Nome canônico:** FlashAttention-3  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T092  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Flash Attention 3

## T092:C01 — conceito

Versão de atenção otimizada cujo trabalho original explora recursos de GPUs Hopper, incluindo assincronia, sobreposição entre movimentação e cálculo e caminhos de baixa precisão. O nome não garante disponibilidade nem vantagem em qualquer GPU NVIDIA. Cada backend e formato precisam ser identificados.

Como funciona:
- Sobrepor transferência de blocos e operações dos Tensor Cores.
- Intercalar multiplicações e normalização para reduzir espera.
- Aplicar estratégia específica de baixa precisão quando o caminho escolhido a suporta.

## T092:C02 — aplicacao

Quando usar:
- Hardware e runtime oferecem implementação compatível com as características exploradas.
- Atenção limita desempenho e há oportunidade de melhorar sobreposição de operações.

Quando não usar:
- Tratar resultados publicados em H100 como previsão direta para uma RTX 5090 ou outro acelerador.

Implementação proposta:
- Consultar a matriz de suporte da versão efetivamente instalada.
- Separar ensaios em FP16/BF16 e FP8 para não atribuir todo ganho ao mesmo fator.
- Guardar configuração e profiler que comprovem o caminho executado.

Aplicação LAI proposta:
Proposta LAI: manter compatibilidade com o hardware real como condição de entrada; o pacote RAG não afirma FA3 funcionando no servidor do usuário.

## T092:C03 — riscos_validacao

Armadilhas:
- Nome de GPU mais recente não significa suporte automático a todas as instruções e kernels de outro projeto.
- FP8 pode exigir escalas e avaliação numérica distintas da variante de maior precisão.

Métricas sugeridas:
- Sobreposição de cópia/cálculo, tempo de kernel e utilização computacional.
- Erro da atenção, acerto de tarefa e latência final por precisão.

Testes propostos:
- Comparar referência e kernel em entradas extremas e máscaras usadas pelo modelo.
- Confirmar que formato não suportado produz erro explícito, sem presumir ganho por uma flag aceita.

## T092:C04 — perguntas_proveniencia

Pergunta: FA3 serve automaticamente na 5090?
Resposta: Não se pode concluir pelo nome; é necessário verificar backend, versão, build e formatos suportados.

Pergunta: FP8 e FA3 são a mesma técnica?
Resposta: Não. Um é formato/estratégia numérica; o outro é uma implementação de atenção que pode explorá-lo.

Pergunta: Ter suporte a FP8 basta para usar o kernel?
Resposta: Não. O caminho pode depender de instruções, layouts e software adicionais.

Pergunta: Pipeline mais ocupado prova menor latência?
Resposta: Não. Coordenação e pressão de recursos podem compensar a sobreposição; compare duração real do trabalho completo.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T092:C05 — mecanismo_avancado

A execução assíncrona exige distinguir transferência iniciada de dados já disponíveis para consumo. Sobrepor movimento, multiplicação e normalização cria mais trabalho em andamento, mas também introduz dependências de buffers e barreiras. A variante de baixa precisão adiciona outro eixo: formato, escalas e tratamento de outliers precisam ser avaliados separadamente da vantagem do pipeline, evitando atribuir toda diferença a uma única mudança.

Condição de contorno:
As técnicas do artigo exploram recursos de Hopper; o nome da família não certifica suporte em qualquer GPU posterior ou doméstica.

Contrato proposto:
- Entradas: Forma, dtype, recursos suportados e política de quantização quando usada.
- Saídas: Atenção calculada e identificação do caminho assíncrono ou fallback.
- Estado: Buffers alternados, eventos de disponibilidade e escalas por bloco.
- Invariante: Um buffer não é sobrescrito enquanto algum consumidor ainda depende dele.

Compromissos de projeto:
- Mais sobreposição pode aumentar pressão sobre registradores e memória compartilhada.
- Baixa precisão reduz tráfego, mas acrescenta erro e trabalho de escalonamento numérico.

## T092:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar comprimentos irregulares e repetidas alternâncias de buffers, comparando com referência. Uma sincronização removida deve ser detectada por divergência ou ferramenta de verificação, não aceita como ganho.

Plano de avaliação proposto:
Plano proposto: avaliar primeiro caminhos de mesma precisão e depois variar precisão isoladamente. Controlar formas e backend; medir latência, erro de saída e uso de recursos. Aprovar somente configurações suportadas com qualidade dentro do requisito definido.

Comparações:
- T123 (complements): FP8 pode participar da implementação, mas precisão e assincronia são decisões independentes.

Afirmação rastreável:
FlashAttention-3 explora assincronia, especialização de warps e intercalamento de multiplicações com softmax em GPUs Hopper.
Suporte: direct; fontes: B-S012
Limite: A fonte apresenta uma arquitetura específica; não verifica a placa, o driver ou o servidor do usuário.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T092:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou pipeline assíncrono e baixa precisão. Esta ficha acrescenta gestão de compatibilidade de hardware, controle de regressão por forma e decisão de upgrade, sem transformar uma versão otimizada para uma arquitetura em recomendação universal.

Matriz de elegibilidade
Antes de habilitar um caminho FA3, registre arquitetura do dispositivo, dtype, dimensão de cabeça e recursos exigidos pelo pacote. Separe suporte declarado de execução verificada. Uma GPU da mesma marca ou uma versão recente do driver não prova que o caminho assíncrono original esteja disponível ou seja selecionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

Dupla linha de base
Compare primeiro o caminho de mesma precisão com o backend atual; depois avalie caminhos de precisão reduzida. Mantenha a máscara e os dados constantes. Essa separação permite localizar se um ganho veio da organização do cálculo ou de mudança numérica, e se uma regressão pertence ao kernel ou à quantização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

Política de atualização
Versione o artefato de compilação e mantenha rollback. A existência de backends mais novos, como a integração documentada de FA4 em FlexAttention, reforça a necessidade de medir, não de atualizar automaticamente. O backend escolhido deve vencer no conjunto de formas do serviço e passar o mesmo contrato de exatidão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

USO AVANÇADO — Pool com hardware heterogêneo
Cenário: Workers de diferentes gerações servem o mesmo checkpoint.
Estratégia: Defina perfil de backend por classe de dispositivo. Compare resultados por precisão e evite encaminhar um artefato compilado para destino incompatível. Exponha o perfil usado em cada requisição para diagnosticar divergências e caudas.
Papel do modelo pequeno: Um 8–30B pode manter pesos comuns com execução específica por dispositivo.
Aceite proposto: Exigir fallback previsível e ausência de erro silencioso em workers não elegíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

USO AVANÇADO — Prefill de alta intensidade
Cenário: Sequências longas consomem parcela relevante do tempo GPU.
Estratégia: Teste FA3 no intervalo de shapes de produção e meça aquecimento, sincronização e pico de memória. Avalie low precision como experimento adicional, com corpus de valores extremos e consultas sensíveis a pequenas mudanças.
Papel do modelo pequeno: Um 3–14B só justifica a troca se atenção realmente dominar o perfil.
Aceite proposto: Aceitar por tempo total, tolerância numérica e qualidade por segmento, sem portar speedups publicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S012, V4B-S018, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, o overhead restante pode limitar benefício; priorizar medição do caminho completo.
8–14B: Em 8–14B, variar contexto e batch para identificar onde o caminho otimizado realmente compensa.
15–30B: Em 15–30B, testar compatibilidade com sharding, GQA e formatos quantizados do restante da rede.
Requisitos de treino/runtime: Exige runtime e hardware adequados; não é atualização de pesos nem aumento de contexto treinado.
Não aplicar quando: Não alegar compatibilidade com uma GPU específica do usuário sem identificar e testar dispositivo, build e backend.

## T092:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T092:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T092 → T123 [complements]
Como combinar: Avaliar o caminho FP8 separadamente da reorganização assíncrona.
Interface: Escalas, dtype e erros por camada ou saída.
Condição: Implementação oferece o caminho numérico no hardware selecionado.
Aceite proposto: Comparar primeiro mesma precisão e depois baixa precisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S012, V4B-S018, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T092 → T107 [requires]
Como combinar: Localizar se espera de memória, cálculo ou sincronização domina cada forma.
Interface: Perfil de kernels e tempo no serviço.
Condição: Instrumentação não altera materialmente o regime observado.
Aceite proposto: Repetir com aquecimento e relatar variância e custos externos à atenção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S012, V4B-S018, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar a implementação realmente selecionada em cada worker.
- Manter fallback e testes numéricos após recompilação ou upgrade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve usar tarefa, qualidade e custo observados. Uma otimização específica de hardware pode melhorar latência local, sem sustentar alegação de inteligência equivalente ou superior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T091, T123, T086

## Fontes primárias associadas

### B-S012 — FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision

[https://arxiv.org/abs/2407.08608](https://arxiv.org/abs/2407.08608)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto centrado em Hopper, assincronia e variantes de baixa precisão.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
