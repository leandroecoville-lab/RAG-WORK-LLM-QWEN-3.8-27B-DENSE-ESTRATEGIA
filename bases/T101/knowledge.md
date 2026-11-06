# T101 — Ring Attention

**Nome canônico:** Ring Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T101  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção em anel

## T101:C01 — conceito

Método para distribuir atenção de sequências extensas entre dispositivos. Mantém partes da sequência em GPUs diferentes e circula blocos KV em um anel, sobrepondo comunicação e cálculo quando possível. Não torna contexto ilimitado nem elimina a necessidade de conectividade e suporte do modelo.

Como funciona:
- Particionar consultas e estados por trechos da sequência.
- Enviar blocos KV entre dispositivos vizinhos no anel.
- Acumular atenção à medida que os blocos necessários passam por cada dispositivo.

## T101:C02 — aplicacao

Quando usar:
- Uma sequência excede memória operacional de um dispositivo.
- Existe infraestrutura multi-GPU com comunicação adequada e workload longo.

Quando não usar:
- Máquina de uma GPU ou contexto curto cujo custo de comunicação supera qualquer benefício.

Implementação proposta:
- Mapear topologia, banda e latência de comunicação antes da implementação.
- Preservar posições globais e máscara causal através das partições.
- Comparar atenção distribuída e referência local em sequências que cabem nas duas configurações.

Aplicação LAI proposta:
Proposta LAI: considerar somente em laboratório distribuído com necessidade demonstrada de uma sequência muito longa; não é otimização imediata para uma única 5090.

## T101:C03 — riscos_validacao

Armadilhas:
- Carga desigual por partição pode deixar dispositivos ociosos.
- Atrasos na comunicação podem impedir a sobreposição esperada e dominar o tempo total.

Métricas sugeridas:
- Memória por GPU, tempo de comunicação e tempo sobreposto.
- Eficiência ao aumentar número de dispositivos para uma sequência fixa.

Testes propostos:
- Comparar logits contra referência preservando dtype e tolerância numérica.
- Testar sequência irregular e falha de um participante; exigir erro controlado em vez de saída incompleta.

## T101:C04 — perguntas_proveniencia

Pergunta: Ring Attention aumenta a capacidade aprendida de contexto?
Resposta: Não por si só. Distribui o cálculo; posições e comportamento do checkpoint continuam limitando a utilidade.

Pergunta: Elimina o tráfego de rede?
Resposta: Não. Organiza a circulação de KV e tenta sobrepor o tráfego ao cálculo.

Pergunta: O anel reduz o número de pares atendidos?
Resposta: Não necessariamente. Pode preservar a atenção densa e apenas distribuir onde suas interações são calculadas.

Pergunta: Por que posições globais importam?
Resposta: A causalidade deve acompanhar a sequência original; índices locais de cada shard não determinam quais tokens estão no futuro.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T101:C05 — mecanismo_avancado

Sobrepor comunicação e computação não elimina bytes transmitidos: oculta parte do tempo quando existe trabalho suficiente enquanto o próximo bloco chega. Um limite simplificado por rodada é o maior entre duração de cálculo e transferência, acrescido de sincronização não ocultada. O primeiro carregamento e a drenagem final continuam relevantes. Blocos menores aumentam frequência de mensagens; maiores exigem mais memória temporária.

Condição de contorno:
Sequências curtas ou interconexão lenta podem tornar a comunicação dominante, frustrando a sobreposição assumida pelo projeto.

Contrato proposto:
- Entradas: Partições de consultas, blocos KV, topologia e máscara com posições globais.
- Saídas: Saídas locais normalizadas sobre todos os blocos globalmente permitidos.
- Estado: Buffers de envio/recepção, identificadores de rodada e acumuladores estáveis.
- Invariante: Cada bloco necessário contribui uma vez, independentemente da ordem de chegada.

Compromissos de projeto:
- Distribuir contexto reduz memória por dispositivo e adiciona comunicação.
- Mais dispositivos podem aumentar capacidade sem diminuir latência de uma requisição.

## T101:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atrasar um elo e permutar a ordem de recebimento preservando os identificadores. Esperar espera controlada e resultado equivalente; duplicar um bloco deve ser detectado.

Plano de avaliação proposto:
Plano proposto: comparar implementação local e distribuída para casos que caibam em ambas. Controlar sequência, precisão e máscara; medir bytes transferidos, tempo exposto de comunicação e duração total, separando ganho de capacidade de ganho de velocidade.

Comparações:
- T117 (specializes): É uma organização específica da comunicação para distribuir o contexto entre dispositivos.

Afirmação rastreável:
Ring Attention propõe sobrepor comunicação de blocos KV com cálculo de atenção em blocos.
Suporte: direct; fontes: B-S020
Limite: O grau efetivo de sobreposição depende da relação entre cálculo, tamanho dos blocos e banda disponível.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T101:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu sobreposição e buffers do anel. O aprofundamento passa a planejar topologia, tolerância a falhas e limites econômicos, distinguindo processamento distribuído do contexto de simples aumento nominal da janela de entrada.

Topologia observada
Meça bandas e latências entre os dispositivos realmente usados, incluindo saltos entre hosts e contenção de outros jobs. Um anel lógico pode atravessar enlaces muito diferentes. Ordene ranks considerando a topologia e compare comunicação efetiva com trabalho por bloco, sem usar banda de catálogo como se fosse atingível na aplicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

Falha como unidade coletiva
Uma rodada incompleta não pode produzir um resultado silenciosamente parcial. Defina timeout e cancelamento coordenado para todos os participantes, preservando o pedido para recomputação. Registre qual bloco e rank faltaram; retornar atenção sobre um subconjunto muda a função e não é um fallback exato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

Custo de reservar o grupo
Mesmo que um prompt longo execute mais rápido, vários dispositivos ficam comprometidos com uma única entrada. Compare a redução de latência com a quantidade de outras tarefas que poderiam ser atendidas. Para tráfego misto, reserve paralelismo de contexto a pedidos que ultrapassem um limiar de custo observado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

USO AVANÇADO — Leitura excepcionalmente longa
Cenário: Algumas entradas não cabem ou excedem o prazo em um dispositivo.
Estratégia: Selecione somente essas entradas para o grupo distribuído e mantenha o restante em réplicas locais. Teste acesso a evidências distantes e valide máscara global. Se não houver benefício líquido, reduza contexto via recuperação em vez de distribuir automaticamente.
Papel do modelo pequeno: Um 15–30B pode precisar de CP por contexto, mesmo quando seus pesos cabem localmente.
Aceite proposto: Aceitar por qualidade, prazo e custo de ocupação do grupo inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

USO AVANÇADO — Experimento arquitetural
Cenário: Um estudo precisa validar atenção completa com sequência extensa.
Estratégia: Compare anel e referência em tamanhos menores, depois aumente comprimento e número de ranks. Teste falhas de comunicação e desbalanceamento. Preserve logs de posições e normalizadores para localizar perda ou duplicação de blocos.
Papel do modelo pequeno: Modelos 3–14B podem servir como protótipos controlados antes de ampliar recursos.
Aceite proposto: Exigir equivalência numérica e ausência de saída parcial quando um rank falha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S020, V4B-S003.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, múltiplos dispositivos raramente se justificam sem contexto extremo ou objetivo experimental explícito.
8–14B: Em 8–14B, medir se CP resolve memória de sequência melhor que outra estratégia de contexto.
15–30B: Em 15–30B, considerar ocupação do grupo e interação com TP antes de combinar paralelismos.
Requisitos de treino/runtime: Requer runtime distribuído, topologia adequada e modelo que suporte o contexto; não amplia treinamento posicional por si só.
Não aplicar quando: Não usar anel quando transferência domina ou quando a tarefa pode recuperar poucos trechos suficientes.

## T101:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C003 — Meta / Infraestrutura de inferência Meta AI
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Meta relata técnicas implementadas para sistemas de inferência que sustentam aplicações como Meta AI, com metas distintas de prefill e geração.
Mecanismo documentado: Algoritmos de comunicação para TP e variantes Pass-KV/Pass-Q para contexto; resultados de escala são apresentados separadamente das direções futuras.
Correspondência com esta base: Pass-KV/Pass-Q são descritos como variantes frequentemente chamadas ring attention, sem identificar toda implementação com o paper específico.
Transferência proposta para modelo pequeno: Proposta: usar topologia e formas reais para decidir CP/TP em 3–30B, preservando uma execução local como comparação quando possível.
Limite: Modelos e clusters citados excedem muitos ambientes 3–30B. Disaggregated inference aparece como direção futura nesse texto e não é contado como implantação exata a partir dele.
Fontes: V4B-S003.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q003.

## T101:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T101 → T117 [complements]
Como combinar: Implementar uma estratégia de comunicação para contexto particionado.
Interface: Blocos, posições globais e estado de normalização.
Condição: Todos os ranks compartilham a mesma semântica de atenção.
Aceite proposto: Comparar Pass-KV/alternativas com referência e medir custo coletivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S020, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T101 → T122 [complements]
Como combinar: Transportar blocos usando caminho de baixa intervenção CPU quando suportado.
Interface: Buffers registrados, eventos de conclusão e ordem de rodadas.
Condição: Hardware e biblioteca garantem visibilidade correta dos dados.
Aceite proposto: Injetar atrasos e verificar que consumo espera a transferência completa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S020, V4B-S003. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Nunca publicar resultado de uma rodada incompleta.
- Relatar custo total de dispositivos e comunicação, além da latência isolada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar perguntas de contexto extenso com fronteira incluindo custo de todos os dispositivos. Ring Attention viabiliza cálculo distribuído; não prova entendimento confiável de toda a informação acessível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T117, T118, T122

## Fontes primárias associadas

### B-S020 — Ring Attention with Blockwise Transformers for Near-Infinite Context

[https://arxiv.org/abs/2310.01889](https://arxiv.org/abs/2310.01889)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sequência distribuída e circulação de blocos KV com computação sobreposta.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S003 — Scaling LLM Inference: Innovations in Tensor Parallelism, Context Parallelism, and Expert Parallelism

[https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Técnicas implementadas para inferência de aplicações Meta AI; separação de métricas de prefill e decode e paralelismos.

Limite: Escala e interconexão da Meta não representam servidor do usuário; não confirma cada técnica em todo modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
