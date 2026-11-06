# T106 — Otimização de KV com MQA/GQA

**Nome canônico:** Otimização do armazenamento KV em modelos MQA/GQA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T106  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** GQA/MQA KV Optimization; KV cache com cabeças compartilhadas; MQA/GQA KV optimization

## T106:C01 — conceito

Otimização de KV com MQA/GQA significa preservar no serving o compartilhamento de cabeças definido pelo modelo. MQA usa uma cabeça KV compartilhada; GQA usa grupos com menos cabeças KV que cabeças de consulta. Isso reduz o volume lógico do cache comparado a MHA, mantendo as demais dimensões. Não é uma terceira arquitetura nem um botão que converte qualquer checkpoint sem consequências.

Como funciona:
- Ler no checkpoint os números de cabeças de consulta e KV, dimensão por cabeça, camadas e dtype do cache.
- Armazenar cabeças KV compartilhadas sem duplicação persistente desnecessária e mapear consultas aos grupos corretos.
- Usar kernels e layouts compatíveis para evitar que uma expansão materializada elimine a economia de memória.

## T106:C02 — aplicacao

Quando usar:
- Servir checkpoints MQA/GQA sob restrição de memória ou largura de banda, especialmente com contextos longos e múltiplas sequências.

Quando não usar:
- Para inferir o consumo total da GPU apenas pelo número de cabeças ou alterar a arquitetura declarada de um modelo arbitrariamente.

Implementação proposta:
- Proposta: estimar KV como 2 × camadas × sequências × tokens × cabeças_KV × dimensão_cabeça × bytes, quando K e V têm a mesma dimensão.
- Tratar a fórmula como estimativa lógica: adicionar páginas, fragmentação, reservas, replicação entre dispositivos e outros buffers.
- Comparar buffers físicos e shapes com o desenho esperado; verificar suporte de backend, dtype e distribuição de cabeças no paralelismo escolhido.
- Validar logits ou respostas contra uma execução de referência; conversão de MHA para MQA/GQA é outro procedimento, podendo exigir treinamento.

Aplicação LAI proposta:
Proposta LAI: dimensionar concorrência usando as cabeças KV reais do modelo e medições do executor, mantendo separado o orçamento dos pesos.

## T106:C03 — riscos_validacao

Armadilhas:
- Confundir redução do cache com redução proporcional da memória dos pesos.
- Replicar cabeças para compatibilidade de um kernel pode reduzir ou anular a economia prática.

Métricas sugeridas:
- Bytes de KV por token e sequência, pico de memória, largura de banda e latência de decode.

Testes propostos:
- Teste proposto: dobrar o comprimento e conferir crescimento esperado do cache, separando memória reservada de efetivamente usada.
- Comparar múltiplos grupos e sequências para detectar mistura de cabeças ou contaminação entre requisições.

## T106:C04 — perguntas_proveniencia

Pergunta: MQA e GQA são técnicas de compressão textual?
Resposta: Não. Alteram o compartilhamento de chaves e valores na atenção; o texto da entrada pode continuar idêntico.

Pergunta: Por que T106 não usa apenas T100 como canônico?
Resposta: Este registro trata a operação de serving aplicável a MQA e GQA; T099 e T100 descrevem as arquiteturas específicas.

Pergunta: Como considerar camadas locais e globais?
Resposta: Use comprimentos retidos por camada, em vez de multiplicar todas por um único comprimento total.

Pergunta: Menos bytes por token garante mais usuários?
Resposta: Apenas se KV for o limitante relevante e outros recursos, prazos e reservas também suportarem a concorrência adicional.

Escopo das fontes:
Papers MQA/GQA e documentação de atenção fundamentam o mecanismo; dimensionamento operacional e testes são propostas.

## T106:C05 — mecanismo_avancado

O orçamento KV deve ser calculado por camada e dispositivo, pois arquiteturas híbridas podem ter números de cabeças ou comprimentos retidos diferentes. Uma soma útil é Σcamadas 2·B·Tcamada·Hkv_camada·dcamada·scamada bytes, antes de padding e réplicas. MQA/GQA reduzem Hkv lógico; o runtime precisa manter essa economia no layout físico, evitando materializar cópias persistentes para cada cabeça de consulta.

Condição de contorno:
Replicação por paralelismo, kernels incompatíveis ou camadas de atenção global podem tornar a economia menor que a previsão simplificada.

Contrato proposto:
- Entradas: Configuração por camada, comprimentos retidos, dtype e plano de particionamento.
- Saídas: Estimativa detalhada e medição de bytes KV por dispositivo.
- Estado: Grupos lógicos, réplicas físicas, reservas e buffers temporários.
- Invariante: Toda economia declarada distingue valores úteis de memória realmente alocada.

Compromissos de projeto:
- Mais grupos preservam diversidade com maior custo por token.
- Repartir grupos exige comunicação ou replicação conforme o plano distribuído.

## T106:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: instrumentar alocações ao alternar entre um kernel com broadcast e outro que materializa expansão. Esperar mesma saída, mas detectar explicitamente a diferença de bytes físicos.

Plano de avaliação proposto:
Plano proposto: comparar previsão por camada com medições em vários comprimentos e concorrências. Separar pesos, KV e temporários; investigar divergências antes de estimar capacidade máxima e validar limites sob crescimento real de saídas.

Comparações:
- T100 (complements): A arquitetura define grupos; o planejamento operacional verifica sua representação física.

Afirmação rastreável:
GQA usa um número de cabeças KV intermediário entre MQA e MHA convencional.
Suporte: direct; fontes: B-S019
Limite: A contagem arquitetural não inclui automaticamente réplicas, alinhamento ou reservas do servidor.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T106:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou KV por camada e dispositivo. A nova camada liga esse orçamento ao limite de concorrência, à arquitetura efetiva do checkpoint e ao caminho de execução que pode desperdiçar a economia lógica.

Do checkpoint à reserva
Extraia número de cabeças KV, dimensões, tipos de camada e limites de retenção do checkpoint real. Converta a estimativa em reserva por sequência usando comprimento de entrada e crescimento permitido da saída. Dividir VRAM apenas pelo tamanho dos pesos ignora justamente o benefício e o custo que MQA/GQA pretendem controlar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

Representação versus expansão
Algumas interfaces aceitam grupos de consultas mas expandem K/V temporariamente para atender um kernel. Isso pode preservar resultados e ainda aumentar pico de memória ou tráfego. Examine o caminho selecionado, incluindo fallback, para saber se a redução arquitetural chega ao armazenamento e às leituras relevantes durante decode.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

Comparação de modelos
Dois checkpoints com igual quantidade de parâmetros podem ter largura, profundidade e grupos KV distintos. A comparação operacional deve incluir bytes por token e custo de atenção, além de pesos. Qwen3 publica configurações diferentes; sua família não autoriza presumir a configuração ou o backend do modelo existente no servidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

USO AVANÇADO — Dimensionamento de sessões
Cenário: Um serviço precisa suportar conversas de tamanhos variados.
Estratégia: Construa classes de reserva por contexto e libere margem ao terminar cada pedido. Use configuração real e medição física para calibrar o estimador.
Papel do modelo pequeno: Um 8–14B pode ser escolhido por equilíbrio entre qualidade especializada e custo por sessão.
Aceite proposto: Estimativas devem prever pico por dispositivo sem subestimar réplicas ou buffers.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

USO AVANÇADO — Seleção de checkpoint
Cenário: Há candidatos 3–30B com respostas semelhantes no domínio.
Estratégia: Compare qualidade, memória dos pesos, KV por token e latência sob a mesma distribuição de contexto. Evite converter um MHA existente apenas para obter uma linha melhor na planilha.
Papel do modelo pequeno: O modelo menor assume tarefas cujo conhecimento vem de evidência recuperada.
Aceite proposto: Selecionar pelo serviço dentro do orçamento, com testes de dependência longa preservados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S019, B-S018, V4B-S020, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma redução de KV pode ampliar concorrência mesmo quando pesos já cabem; confirme que o trabalho é limitado por cache.
8–14B: Com grupos KV suficientes, particionamento pode ser conveniente, mas divisibilidade deve ser verificada.
15–30B: Em 15–30B, atenção, pesos e comunicação competem; reduzir KV não elimina o restante do consumo.
Requisitos de treino/runtime: Arquitetura requer pesos compatíveis. Otimização de layout e kernels é de runtime, mantendo a estrutura treinada.
Não aplicar quando: Não trocar número de cabeças KV em configuração e esperar preservação automática da função.

## T106:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Configuração permite dimensionar KV, mas economia física depende do executor.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q016, V4B-Q005.

## T106:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T106 → T100 [requires]
Como combinar: A economia GQA depende da razão entre cabeças de consulta e KV do checkpoint.
Interface: Configuração por camada e layout físico.
Condição: Carregamento confirma grupos e projeções corretos.
Aceite proposto: Comparar logits e bytes com implementação de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, B-S018, V4B-S020, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T106 → T087 [feeds]
Como combinar: O orçamento de cache informa admissão de sequências no lote contínuo.
Interface: Reserva por sequência e capacidade livre real.
Condição: Crescimento futuro incluído na admissão.
Aceite proposto: Submeter mistura de contextos e observar falta de memória e espera.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S019, B-S018, V4B-S020, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar parâmetros ativos de MoE como tamanho dos pesos residentes.
- Relatar separadamente memória útil, alocada e pico de temporários.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Um modelo pequeno com GQA pode servir mais contexto simultâneo que outro candidato, mas isso não demonstra raciocínio superior. Compare tarefas cuja evidência cabe na janela e que tenham resposta verificável.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T099, T100, T081, P009

## Fontes primárias associadas

### B-S018 — Fast Transformer Decoding: One Write-Head is All You Need

[https://arxiv.org/abs/1911.02150](https://arxiv.org/abs/1911.02150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MQA compartilha chaves e valores entre cabeças de consulta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S019 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

[https://arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Grupos de consultas compartilham cabeças KV; conversão proposta envolve treinamento.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S017 — torch.nn.functional.scaled_dot_product_attention

[https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de implementações de atenção, máscaras e suporte dependente de backend.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
