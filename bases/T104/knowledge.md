# T104 — Radix Attention

**Nome canônico:** RadixAttention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T104  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** RadixAttention

## T104:C01 — conceito

RadixAttention é o mecanismo apresentado pelo SGLang para reutilização sistemática de cache KV por meio de uma radix tree. Relaciona prefixos de tokens a estados disponíveis. Seu nome pode sugerir uma nova fórmula de atenção, mas o foco é reuso e gerenciamento dos estados.

Como funciona:
- Encontrar o maior prefixo compatível na árvore de estados.
- Reaproveitar o trecho disponível e calcular a continuação ausente.
- Atualizar referências e política de remoção conforme novas requisições usam o cache.

Nota de nomenclatura: Normalização do nome original do inventário; preservado como técnica específica do SGLang.

## T104:C02 — aplicacao

Quando usar:
- Workflows repetem exemplos, instruções ou prefixos de conversação.
- Existe runtime que implementa o mecanismo com telemetria adequada.

Quando não usar:
- Esperar benefício quando prompts quase não compartilham início ou quando retenção reduz capacidade útil do batch.

Implementação proposta:
- Construir uma amostra com padrões reais de repetição, não somente prompts sintéticos idênticos.
- Comparar execução fria e aquecida e medir impacto em admissão de novas sequências.
- Avaliar justiça entre requisições com muito e pouco prefixo reutilizável.

Aplicação LAI proposta:
Proposta LAI: avaliar RadixAttention ao comparar runtimes em missões com prefixos reutilizados, mantendo igual modelo e conjunto de tarefas.

## T104:C03 — riscos_validacao

Armadilhas:
- Priorizar somente afinidade de cache pode aumentar espera de entradas novas.
- Cache aquecido em um worker não garante hit após roteamento para outro.

Métricas sugeridas:
- Proporção de tokens reaproveitados e tempo de prefill evitado.
- Tempo de espera por grupo e custo de manter a árvore.

Testes propostos:
- Repetir prefixos com continuações distintas e verificar saídas corretas e estados compartilhados válidos.
- Misturar tráfego sem repetição e exigir que a política não o prive de serviço.

## T104:C04 — perguntas_proveniencia

Pergunta: RadixAttention substitui o Transformer?
Resposta: Não. É uma técnica de runtime para aproveitar estados já calculados.

Pergunta: É sinônimo de todo prefix caching?
Resposta: Não. É uma implementação específica; cache de prefixos também pode usar outras estruturas.

Pergunta: Pode usar hits como único objetivo?
Resposta: Não. Eles ignoram quem está esperando e o custo de memória imposto às sequências ativas.

Pergunta: RadixAttention altera os pesos de atenção?
Resposta: Seu mecanismo de reúso organiza estados já calculados; uma implementação correta preserva a operação do modelo.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T104:C05 — mecanismo_avancado

O escalonamento orientado por afinidade de prefixo busca amortizar a construção do estado ao atender pedidos relacionados próximos no tempo. Isso cria uma tensão com justiça: pedidos sem prefixos populares podem esperar enquanto novas consultas compatíveis continuam chegando. Como proposta de integração, idade e prazo devem limitar essa preferência. O cache compartilhado também compete por memória com sequências ativas e seus tokens futuros.

Condição de contorno:
Uma boa taxa de hits pode coexistir com starvation ou piora da latência de classes pouco frequentes.

Contrato proposto:
- Entradas: Pedidos, afinidade de prefixo, idade, prioridades e capacidade KV disponível.
- Saídas: Ordem de execução com justificativa de afinidade e limites de espera.
- Estado: Árvore de estados, referências ativas e fila com tempos originais.
- Invariante: A política de reúso não altera conteúdo do pedido nem perde sua identidade.

Compromissos de projeto:
- Ordenar por afinidade reduz prefill repetido e pode prejudicar equidade.
- Reter históricos libera trabalho futuro e ocupa capacidade que poderia admitir novas sequências.

## T104:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alimentar continuamente um prefixo popular enquanto um pedido sem hit aguarda. Esperar execução dentro da regra de envelhecimento proposta, sem exigir que o pedido mude seu prompt.

Plano de avaliação proposto:
Plano proposto: comparar ordem de chegada e afinidade limitada por prazo com a mesma carga. Medir tokens recalculados, TTFT por classe, pior espera e throughput útil; aceitar economia de trabalho somente com equidade previamente definida.

Comparações:
- T103 (complements): A radix tree fornece correspondências; a política decide quando usar essa afinidade.

Afirmação rastreável:
O artigo do SGLang discute escalonamento por maior prefixo compartilhado e reconhece risco de starvation.
Suporte: direct; fontes: V3B-S011
Limite: A propriedade de reúso descrita para lotes não vira garantia geral de justiça em tráfego online.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T104:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu afinidade e justiça. O aprofundamento acrescenta seleção entre recuperar, transferir e recomputar, considerando que o prefixo pode estar disponível em diferentes níveis de memória.

Hit com custo
Na hierarquia HiCache, localizar um prefixo não encerra a decisão: restaurá-lo consome banda e pode disputar recursos com decodes ativos. Proponha comparar tempo estimado de restauração com prefill restante. Um prefixo maior em armazenamento pode ser menos vantajoso que um prefixo menor já residente; registre qual alternativa foi escolhida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Afinidade sob mudança de carga
Preferência por uma família de prompts precisa reagir à taxa de chegada. Popularidade passada pode manter estados sem utilidade e concentrar fila num worker. Use janelas de observação e idade do pedido, mas evite recalcular prioridades a cada token: essa oscilação pode tornar a política mais cara que a economia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Estado adicional
Modelos híbridos e mecanismos especulativos podem demandar estados além de KV convencional. Não restaure apenas a parcela que o índice conhece. A interface de cache deve enumerar componentes necessários, suas versões e o ponto até o qual representam o mesmo prefixo; caso contrário, trate o reúso como incompleto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Sessões com retomada
Cenário: Um usuário retorna a uma conversa longa depois de minutos.
Estratégia: Conserve metadados leves, coloque tensores em camada mais barata e restaure sob prazo. Se a previsão de transferência falhar, recalcule a partir de tokens confirmados sem misturar duas histórias.
Papel do modelo pequeno: Modelos 8–14B podem sustentar diálogos especializados com sessões intermitentes.
Aceite proposto: Medir tempo de retomada e consistência após expiração, sem contar restore como hit instantâneo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Lote com prefixos heterogêneos
Cenário: Consultas analíticas compartilham documentos diferentes.
Estratégia: Agrupe por afinidade apenas até o limite de espera e intercale famílias pouco populares. Limite quanto cada família pode manter residente.
Papel do modelo pequeno: Um 15–30B recebe contexto específico sem exigir que todos os documentos permaneçam na GPU.
Aceite proposto: Avaliar espera por família e total de trabalho concluído dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em prompts curtos, compare contra recomputação simples antes de adicionar armazenamento remoto.
8–14B: Busque equilíbrio entre sessões ativas e prefixos adormecidos; ambos competem pela mesma capacidade.
15–30B: Considere custo de restaurar várias camadas ou partições, e não apenas tamanho agregado.
Requisitos de treino/runtime: Runtime e formato de estado devem suportar o modelo escolhido; HiCache documentado não prova qualquer arquitetura.
Não aplicar quando: Não aplicar afinidade rígida quando uma família mantém fila permanentemente congestionada.

## T104:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: HiCache estende explicitamente RadixAttention.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T104:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T104 → T083 [complements]
Como combinar: A política consulta a hierarquia para escolher o melhor prefixo realmente materializável.
Interface: Residência, previsão de transferência e orçamento de banda.
Condição: Estimativas atualizadas e limite para restauração.
Aceite proposto: Induzir saturação da camada inferior e observar mudança para recomputação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T104 → T121 [requires]
Como combinar: O agendamento deve considerar custo e justiça além do tamanho do prefixo.
Interface: Idade original, deadline e afinidade.
Condição: Prioridade não reiniciada após reencaminhamento.
Aceite proposto: Verificar ausência de starvation em mistura de prompts.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar taxa de localização lógica da taxa de reutilização efetivamente consumida.
- Restaurar metadados e tensores como uma unidade consistente ou invalidar o candidato.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com um serviço de fronteira deve usar retomadas e concorrência equivalentes. Radix Attention otimiza execução; não compensa uma janela treinada insuficiente nem assegura compreensão de documentos extensos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T103, T105, T171

## Fontes primárias associadas

### B-S022 — SGLang: Efficient Execution of Structured Language Model Programs

[https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention reutiliza KV com estrutura de prefixos.

Limite: Resumo e versão HTML abertos; foco no mecanismo de reuso. Resultados publicados não reproduzidos.

### V3B-S011 — SGLang: Efficient Execution of Structured Language Model Programs — full text

[https://arxiv.org/html/2312.07104v2](https://arxiv.org/html/2312.07104v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RadixAttention, busca de prefixos e ciclo de vida/remoção de cache em árvore.

Limite: Texto do projeto consultado; não representa garantia de compatibilidade de implantação ou reprodução de resultados.

### V4B-S031 — HiCache in SGLang: hybrid-model caching with up to 15.5× input throughput

[https://www.sglang.io/blog/hicache](https://www.sglang.io/blog/hicache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hierarquia GPU/CPU/armazenamento, HiRadixTree, políticas de restauração e requisitos adicionais de estado híbrido/draft.

Limite: Resultados são benchmarks do projeto, não implantação específica de cliente; ganho publicado não transferido.

### V4D-S017 — Mooncake x SGLang HiCache System Design

[https://kvcache-ai.github.io/Mooncake/design/hicache-design.html](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Co-uso documentado de RadixAttention/HiRadixTree e cache de KV em GPU, host e armazenamento distribuído.

Limite: Documento de integração disponível, sem prova de adoção de toda essa configuração pelo serviço Kimi. Hierarquia de cache tensorial não é memória semântica de agente.

### V4D-S018 — Mooncake Architecture

[https://kvcache-ai.github.io/Mooncake/design/architecture.html](https://kvcache-ai.github.io/Mooncake/design/architecture.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contratos de plano de controle/dados, buffers, leases, armazenamento compartilhado e roteamento por prefixo.

Limite: Capacidades de componentes atuais não são evidência de que todo cliente utilize todos eles; suporte depende do backend e da configuração.

### V4D-S019 — Mooncake Transfer Engine

[https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html](https://kvcache-ai.github.io/Mooncake/design/transfer-engine/index.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segment/BatchTransfer, buffers registrados, transporte RDMA e escolha de caminho segundo topologia, com recuperação de falhas.

Limite: Documentação de biblioteca; submissão validada não torna transferência posterior atômica. Suporte amplo de transporte não comprova o caminho usado numa implantação específica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
