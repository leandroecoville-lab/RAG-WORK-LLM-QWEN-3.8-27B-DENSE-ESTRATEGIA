# T099 — Multi-Query Attention — MQA

**Nome canônico:** Multi-Query Attention — MQA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T099  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multi-query attention; atenção multi-query

## T099:C01 — conceito

Arquitetura em que várias cabeças de consulta compartilham uma única cabeça de chaves e valores. Isso reduz armazenamento e leitura de KV em comparação com MHA equivalente. O compartilhamento faz parte dos pesos e do treinamento; não é simplesmente uma flag de compressão aplicável a todo checkpoint.

Como funciona:
- Projetar consultas em múltiplas cabeças.
- Produzir um conjunto compartilhado de chaves e valores por posição.
- Cada cabeça de consulta calcula seus scores contra o KV compartilhado.

## T099:C02 — aplicacao

Quando usar:
- Escolha de checkpoint prioriza eficiência de decode e memória.
- Projeto de modelo permite avaliar o compromisso entre compartilhamento e qualidade.

Quando não usar:
- Substituir cabeças de um modelo MHA por uma só sem conversão e treinamento apropriados.

Implementação proposta:
- Ler número de cabeças Q e KV na configuração do modelo.
- Confirmar que o kernel não materializa cópias desnecessárias do KV compartilhado.
- Comparar modelos ou variantes controlando capacidade e qualidade, não só VRAM.

Aplicação LAI proposta:
Proposta LAI: usar MQA como atributo na seleção de modelos; a decisão de runtime deve respeitar a arquitetura existente do Qwen escolhido.

## T099:C03 — riscos_validacao

Armadilhas:
- Menor número de cabeças KV não garante desempenho superior em toda tarefa.
- Uma implementação ingênua pode expandir KV e perder parte do benefício de armazenamento.

Métricas sugeridas:
- Bytes KV por token e banda de memória durante decode.
- Acerto do checkpoint em tarefas relevantes e latência por usuário.

Testes propostos:
- Verificar shapes reais dos tensores e compartilhamento sem cópia persistente indevida.
- Avaliar ferramentas e contexto longo antes de selecionar o modelo apenas por eficiência.

## T099:C04 — perguntas_proveniencia

Pergunta: Posso converter MHA em MQA apenas configurando num_kv_heads=1?
Resposta: Não. Isso muda a arquitetura e a interpretação dos pesos; uma conversão válida requer método e avaliação.

Pergunta: MQA é memória externa?
Resposta: Não. É organização interna das projeções da atenção.

Pergunta: A dimensão das consultas também cai?
Resposta: Não necessariamente. Múltiplas cabeças Q podem permanecer, enquanto o conjunto de K e V é compartilhado.

Pergunta: A fórmula representa toda a memória do servidor?
Resposta: Não. Pesos, temporários, reservas, tabelas e cópias distribuídas são parcelas adicionais que precisam ser medidas.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T099:C05 — mecanismo_avancado

O compartilhamento de K e V preserva múltiplas consultas, mas reduz a diversidade dos espaços de chave e valor. Para camadas homogêneas, o cache idealizado ocupa 2·L·B·T·Hkv·d·s bytes, com camadas L, sequências B, tokens T, cabeças KV Hkv, dimensão d e bytes por valor s. Em MQA, Hkv é um, antes de replicações, padding e metadados.

Condição de contorno:
Essa redução é arquitetural; um checkpoint MHA não se converte de forma equivalente simplesmente descartando suas cabeças KV.

Contrato proposto:
- Entradas: Pesos compatíveis com MQA, consultas múltiplas e KV compartilhado.
- Saídas: Saídas por cabeça de consulta usando o mesmo conjunto KV.
- Estado: Cache com uma cabeça KV lógica por camada e sequência.
- Invariante: Compartilhamento não modifica a correspondência entre posições e estados do histórico.

Compromissos de projeto:
- Menor tráfego KV pode favorecer decode com contexto extenso.
- Capacidade representacional diferente pode exigir treinamento ou adaptação para preservar qualidade.

## T099:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comparar kernel compartilhado com referência que expande virtualmente K e V para todas as consultas. Injetar mapeamento posicional errado e esperar divergência detectável.

Plano de avaliação proposto:
Plano proposto: validar equivalência entre implementações do mesmo modelo antes de comparar arquiteturas treinadas. Medir bytes reais, replicações, latência por comprimento e qualidade; não atribuir diferenças de checkpoint somente ao número de cabeças.

Comparações:
- T100 (alternative): GQA mantém mais de um grupo KV e oferece outra troca entre compartilhamento e capacidade.

Afirmação rastreável:
O artigo de MQA compartilha chaves e valores entre cabeças para reduzir tráfego no decode incremental.
Suporte: direct; fontes: B-S018
Limite: A redução de tráfego é motivação arquitetural, não uma previsão universal de tempo end-to-end.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T099:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 quantificou a cabeça KV única. Agora a estratégia compara MQA como escolha de checkpoint e examina replicações físicas, conversão arquitetural e inferência em diferentes regimes, sem atribuir ao compartilhamento ganhos que vieram de outro modelo.

Seleção de modelo com controle
Comparar dois checkpoints diferentes mistura dados, treinamento, tokenizer e arquitetura. Use esse ensaio para escolher produto, mas não como prova causal de MQA. Se a pergunta for arquitetural, é preciso controlar o restante ou declarar a limitação. Memória menor é verificável pelo layout, enquanto qualidade depende do conjunto completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

Replicação distribuída
Uma cabeça KV lógica pode ser replicada em vários ranks para alimentar consultas particionadas. Some bytes em todos os dispositivos e observe comunicação necessária. A conta de uma única cópia não descreve automaticamente o sistema distribuído; aumentar TP pode reduzir pesos por rank sem reduzir KV na mesma proporção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

Ponto de equilíbrio da leitura
Meça quanto do decode vem de ler KV, de ler pesos e de executar outros operadores. MQA beneficia o primeiro componente, mas sua contribuição varia com contexto e batch. Para prompts curtos, a diferença pode ser pequena; em sessões extensas, o benefício potencial precisa ser confrontado com qualidade de dependências remotas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

USO AVANÇADO — Escolha para atendimento longo
Cenário: Há muitos turnos e poucas respostas simultâneas.
Estratégia: Compare modelos treinados com MQA e alternativas adequadas à tarefa, medindo memória e qualidade por comprimento. Preserve fatos distantes no teste e não escolha apenas pelo maior contexto que cabe. Inclua custo de recuperação quando ela for necessária.
Papel do modelo pequeno: Um 3–14B com MQA pode ser eficiente para uma tarefa estreita se mantiver qualidade suficiente.
Aceite proposto: Aprovar por respostas corretas dentro do orçamento e bytes reais por sessão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

USO AVANÇADO — Distribuição de modelo maior
Cenário: Um alvo não cabe confortavelmente em um dispositivo.
Estratégia: Inspecione como o backend distribui a cabeça KV e escolha TP considerando replicação. Compare com uma instância quantizada ou outra arquitetura suportada. Não reescreva pesos MHA descartando cabeças para simular MQA.
Papel do modelo pequeno: Um 15–30B pode precisar de distribuição, mas ganhos de memória devem ser medidos por rank.
Aceite proposto: Exigir contabilidade de memória total e latência de comunicação no caminho crítico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S018, V4B-S017, V4B-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, avaliar se um checkpoint MQA já treinado atende o domínio antes de planejar conversão.
8–14B: Em 8–14B, comparar tamanho efetivo de cache e qualidade de atenção em conversas prolongadas.
15–30B: Em 15–30B, verificar replicação KV em TP e orçamento de cada dispositivo.
Requisitos de treino/runtime: MQA é arquitetura treinada; qualquer conversão de MHA exige método de adaptação e validação próprios.
Não aplicar quando: Não prometer a mesma qualidade ao trocar número de cabeças KV nem inferir economia física apenas da configuração lógica.

## T099:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005, V4B-Q016.

## T099:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T099 → T100 [alternative]
Como combinar: Comparar checkpoint GQA quando uma cabeça compartilhada comprometer qualidade ou distribuição.
Interface: Número de grupos, qualidade por tarefa e bytes medidos.
Condição: Modelos são avaliados como produtos, com diferenças declaradas.
Aceite proposto: Escolher pela fronteira qualidade/custo sem alegar causalidade isolada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S018, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T099 → T118 [complements]
Como combinar: Planejar replicação da cabeça compartilhada junto do particionamento de consultas.
Interface: Mapeamento de heads por rank e buffers de comunicação.
Condição: Backend suporta o layout corretamente.
Aceite proposto: Somar memória por rank e testar paridade com execução de referência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S018, V4B-S017, V4B-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Contar réplicas físicas e não somente cabeças lógicas.
- Registrar diferenças de treino ao comparar checkpoints com arquiteturas distintas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar atendimento longo com uma fronteira no mesmo domínio. MQA reduz custo de estado em modelos compatíveis; não oferece garantia de raciocínio, factualidade ou recuperação de contexto equivalentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T100, T106, T108

## Fontes primárias associadas

### B-S018 — Fast Transformer Decoding: One Write-Head is All You Need

[https://arxiv.org/abs/1911.02150](https://arxiv.org/abs/1911.02150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MQA compartilha chaves e valores entre cabeças de consulta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
