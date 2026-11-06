# T091 — FlashAttention-2

**Nome canônico:** FlashAttention-2  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T091  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Flash Attention 2

## T091:C01 — conceito

Evolução da implementação de atenção exata com melhor divisão de trabalho entre blocos e warps da GPU. Reduz operações e comunicação que limitavam a utilização do hardware. É um algoritmo/kernel, não um novo modelo de linguagem nem uma expansão automática de contexto.

Como funciona:
- Reorganizar operações para reduzir trabalho fora das multiplicações matriciais.
- Distribuir uma cabeça de atenção por mais blocos quando isso melhora ocupação.
- Particionar o trabalho entre warps para reduzir comunicação interna desnecessária.

## T091:C02 — aplicacao

Quando usar:
- Modelo e GPU possuem backend FA2 suportado e a atenção é um gargalo.
- Comparação de kernels em prefill e treino de sequências extensas.

Quando não usar:
- Ativar FA2 só pelo número da versão quando outro backend otimizado já é superior na carga.

Implementação proposta:
- Fixar versão do pacote, CUDA e dimensões de cabeça no experimento.
- Registrar o kernel efetivo e comparar contra o backend padrão do mesmo runtime.
- Ensaiar vários comprimentos e tamanhos de lote para identificar regiões de ganho.

Aplicação LAI proposta:
Proposta LAI: conservar o backend já validado como baseline e testar FA2 apenas em uma cópia controlada da configuração de inferência.

## T091:C03 — riscos_validacao

Armadilhas:
- Um benchmark de kernel isolado não equivale ao ganho de ponta a ponta.
- Mudança silenciosa de dtype, máscara ou padding invalida a comparação.

Métricas sugeridas:
- Ocupação, tempo por chamada e proporção de operações não matriciais.
- TTFT, throughput e memória com o mesmo workload.

Testes propostos:
- Comparar logits e saída da atenção com referência em tolerância definida por dtype.
- Testar casos curtos e longos para garantir que a escolha automática não cria regressões materiais.

## T091:C04 — perguntas_proveniencia

Pergunta: FA2 altera os pesos?
Resposta: Não. A otimização implementa o cálculo de atenção sem exigir ensinar uma nova habilidade ao modelo.

Pergunta: É sempre melhor que FA1?
Resposta: O projeto melhora paralelismo, mas desempenho real ainda depende de formas e hardware.

Pergunta: O maior tile é o melhor?
Resposta: Não. Registradores e memória compartilhada limitam quantos blocos podem executar simultaneamente e podem causar spill.

Pergunta: Backward tem exatamente a mesma vantagem?
Resposta: Não. As dependências entre gradientes exigem coordenação adicional; meça o caminho de treinamento separadamente.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T091:C05 — mecanismo_avancado

No particionamento descrito para o forward, dividir consultas entre warps permite que cada grupo produza sua própria fatia de saída. Dividir chaves entre warps pode exigir somar resultados parciais com comunicação adicional. A seleção de tiles também envolve registradores: aumentar o bloco reduz certas transferências, porém pode provocar spilling ou impedir que blocos suficientes permaneçam simultaneamente ativos no dispositivo.

Condição de contorno:
Formas pequenas podem não oferecer paralelismo suficiente; a configuração eficiente varia com dimensão da cabeça e recursos disponíveis.

Contrato proposto:
- Entradas: Tensores, máscara e configuração de tiles compatível com o dispositivo.
- Saídas: Resultado da atenção e informações sobre o kernel realmente selecionado.
- Estado: Registradores, memória compartilhada e distribuição de linhas de consulta.
- Invariante: Cada linha recebe contribuições de todas as chaves permitidas exatamente uma vez.

Compromissos de projeto:
- Tiles maiores podem reduzir tráfego e diminuir ocupação ao mesmo tempo.
- Menos operações escalares ajuda quando essas operações limitam o kernel.

## T091:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: variar dimensões próximas aos limites de especialização e registrar spilling ou fallback. Comparar numericamente com referência e exigir que configurações não suportadas falhem de modo explícito.

Plano de avaliação proposto:
Plano proposto: comparar implementações sob mesmas formas e precisão, separando prefill e decode. Medir tempo, ocupação e tráfego compartilhado quando disponíveis; escolher pelo tempo total, sem usar utilização teórica isolada como critério de sucesso.

Comparações:
- T090 (specializes): Mantém a atenção e melhora sua distribuição de trabalho entre recursos da GPU.

Afirmação rastreável:
O artigo descreve dividir Q entre warps para reduzir comunicação que surgia no esquema com K repartido.
Suporte: direct; fontes: V3B-S006
Limite: O detalhamento refere-se ao algoritmo publicado; kernels posteriores podem escolher outras decomposições.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T091:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou divisão de trabalho e registradores. Aqui o foco é escolher FA2 dentro de um conjunto de backends, lidar com comprimentos variáveis e distinguir ganhos da atenção de efeitos introduzidos por empacotamento ou compilação.

Forma de entrada como distribuição
Colete distribuição de batch, comprimento e dimensão de cabeça. Um único tensor grande pode favorecer a configuração escolhida e esconder degradações nas formas pequenas predominantes em produção. Construa uma grade baseada no uso e pese resultados por frequência, mantendo casos raros críticos separados da média.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

Remoção de padding com fronteiras
Quando usar representação de comprimento variável, preserve os offsets cumulativos e a máscara de cada sequência. Remover padding altera layout, não autoriza atenção entre documentos. Valide exemplos com tamanhos extremos e lotes reordenados; uma saída plausível pode esconder mistura de contexto difícil de perceber visualmente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

Ciclo de vida do backend
Fixe pacote, compilador e dispositivo do ensaio e registre o fallback disponível. Não selecione FA2 apenas pelo nome conhecido nem descarte uma implementação nova sem teste. Após atualização, reavalie formas efetivamente utilizadas, porque mudanças no despacho ou em máscaras podem ter mais impacto que o microbenchmark principal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Lote de documentos desiguais
Cenário: Um classificador recebe textos curtos e longos juntos.
Estratégia: Compare padding convencional com caminho varlen suportado, mantendo exemplos idênticos e mapeamento de IDs. Só então compare FA2 com outros backends. Isso evita atribuir à versão do kernel uma economia causada pela remoção de padding.
Papel do modelo pequeno: Um especialista 3–14B pode se beneficiar de menos trabalho inútil nos prefills.
Aceite proposto: Aprovar com independência entre exemplos e redução de tempo ponderada pelo tráfego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

USO AVANÇADO — Migração de runtime
Cenário: Um modelo já funciona em um executor de referência.
Estratégia: Monte testes diferenciais de máscara, posições e sampling, aqueça todas as formas relevantes e faça rollout gradual. Se houver backend ausente, falhe com diagnóstico ou use fallback conhecido; não ignore silenciosamente o padrão da arquitetura.
Papel do modelo pequeno: Um 15–30B precisa preservar compatibilidade junto de TP, GQA e dtype selecionados.
Aceite proposto: Exigir qualidade equivalente e picos de memória dentro do orçamento do serviço.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S011, V3B-S006, V4B-S017, V4B-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, medir formatos curtos e overhead de despacho para não escolher pelo cenário mais favorável ao kernel.
8–14B: Em 8–14B, avaliar varlen e empacotamento com testes de isolamento dos exemplos.
15–30B: Em 15–30B, incluir formas resultantes do particionamento por dispositivo, não apenas tensores do modelo inteiro.
Requisitos de treino/runtime: Runtime deve suportar a arquitetura, dtype e máscara; versão FA2 não é configuração universal de todo checkpoint.
Não aplicar quando: Não forçar FA2 quando o backend perde um recurso do modelo ou realiza conversões caras não medidas.

## T091:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T091:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T091 → T087 [complements]
Como combinar: Avaliar lote e layout juntamente, mantendo compatibilidade e identidade por sequência.
Interface: Comprimentos, offsets cumulativos e IDs dos exemplos.
Condição: Kernel varlen é suportado e não mistura sequências.
Aceite proposto: Comparar resultados com processamento independente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S011, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T091 → T098 [alternative]
Como combinar: Selecionar outro kernel eficiente quando oferecer melhor cobertura das formas reais.
Interface: Contrato de atenção e matriz de compatibilidade.
Condição: Ambas implementações preservam a mesma semântica.
Aceite proposto: Escolher por distribuição de latência e memória, não por nome de versão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S011, V3B-S006, V4B-S017, V4B-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar lotes reordenados e comprimentos unitários.
- Separar melhoria por unpadding, compilação e troca de kernel no relatório.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar uma aplicação de modelo pequeno com fronteira usando custo e prazo do serviço. FA2 pode melhorar eficiência; qualquer diferença de qualidade decorre do modelo ou da execução e deve ser investigada separadamente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T090, T092, T098, T113

## Fontes primárias associadas

### B-S011 — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning

[https://arxiv.org/abs/2307.08691](https://arxiv.org/abs/2307.08691)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Melhor particionamento de trabalho e paralelismo na atenção exata.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S006 — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning — full text

[https://arxiv.org/html/2307.08691v1](https://arxiv.org/html/2307.08691v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento entre blocos e warps, custo de operações não matriciais.

Limite: Texto técnico consultado; velocidade depende de formas, dtype e arquitetura do dispositivo.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S018 — FlexAttention + FlashAttention-4: Fast and Flexible

[https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend FlashAttention-4 de FlexAttention em Hopper/Blackwell e geração de modificadores de score/máscara.

Limite: Demonstração de backend; não transforma FA2/FA3 em versões equivalentes nem garante ganho em qualquer forma de tensor.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
