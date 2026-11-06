# T083 — Advanced Prefix Caching

**Nome canônico:** Advanced Prefix Caching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Correção terminológica do inventário original  
**ID canônico:** T082  
**Data da curadoria:** 2026-11-05

## T083:C01 — conceito

Rótulo descritivo para variantes sofisticadas de prefix caching, não uma técnica única padronizada. Pode reunir identificação de blocos, compartilhamento entre requisições, isolamento por domínio, políticas de retenção e roteamento. Deve ser decomposto em funcionalidades verificáveis para evitar contar a mesma capacidade várias vezes.

Como funciona:
- Associar cada bloco ao prefixo precedente, tokens e metadados que afetam os estados.
- Compartilhar somente blocos compatíveis dentro do escopo autorizado.
- Gerenciar referências e remoção sem invalidar sequências ainda em uso.

Nota de nomenclatura: Mantido o nome do inventário; classificado como extensão editorial de Prefix Caching.

## T083:C02 — aplicacao

Quando usar:
- Múltiplas sessões usam grandes prefixos repetidos.
- A taxa de acerto local depende de placement e retenção.

Quando não usar:
- Usar o adjetivo avançado como requisito sem especificar comportamento, isolamento e métrica.

Implementação proposta:
- Documentar uma matriz: chave, granularidade, validade, política de despejo e recuperação.
- Incluir modelo, LoRA e modalidade na identidade quando alterarem o cálculo.
- Comparar cada extensão isoladamente contra o prefix caching básico.

Aplicação LAI proposta:
Proposta LAI: usar este registro como checklist de extensões de T082, sem lançar uma segunda infraestrutura com nome diferente.

## T083:C03 — riscos_validacao

Armadilhas:
- Mesmo hash não é prova universal de identidade; serialização e colisões exigem tratamento.
- Compartilhamento entre usuários pode introduzir canais de inferência por tempo, mesmo sem retornar conteúdo alheio.

Métricas sugeridas:
- Economia de prefill por unidade de memória retida.
- Erros de identidade, acertos úteis e custo de manutenção do índice.

Testes propostos:
- Trocar adaptador mantendo o texto e garantir ausência de reaproveitamento incompatível.
- Executar namespaces distintos com prefixo igual e verificar a política explícita de isolamento.

## T083:C04 — perguntas_proveniencia

Pergunta: Existe um algoritmo único chamado Advanced Prefix Caching?
Resposta: Não foi identificado como denominação única; o registro organiza extensões operacionais do cache de prefixos.

Pergunta: Salt resolve autorização inteira?
Resposta: Não. Restringe reutilização no cache compatível; autenticação e autorização continuam necessárias no serviço.

Pergunta: Hash forte elimina todos os erros?
Resposta: Não. Omissão de campos da identidade e referências expiradas são defeitos lógicos independentes de colisões criptográficas.

Pergunta: Uma colisão simulada deve ser ignorada?
Resposta: Não. Ela testa a política de conflito ou a validação secundária, explicitando o comportamento seguro previsto pelo contrato.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T083:C05 — mecanismo_avancado

O índice precisa identificar o contexto que produziu cada bloco, incluindo ancestralidade, adaptadores e entradas multimodais relevantes. Dois prompts com o mesmo token marcador de imagem podem conter imagens diferentes; comparar apenas IDs de tokens produz um falso hit. Como proposta de implementação, referências de blocos devem ser adquiridas antes de sua possível expulsão, com geração de identificador que detecte reutilização de slots.

Condição de contorno:
A designação advanced prefix caching não especifica um protocolo universal; consistência e isolamento devem ser definidos por implementação.

Contrato proposto:
- Entradas: Tokens, hashes de conteúdo multimodal, identidade do adaptador e domínio de cache.
- Saídas: Referências válidas a blocos e explicação verificável dos hits.
- Estado: Índice, contadores de referência e versões de alocação.
- Invariante: Igualdade de chave implica compatibilidade de todo estado que afeta as projeções.

Compromissos de projeto:
- Chaves mais completas exigem computação e metadados adicionais.
- Verificação defensiva reduz falsos hits, porém pode converter possíveis reutilizações em misses.

## T083:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter marcadores iguais e trocar a imagem ou adaptador; também simular referência expirada. Esperar miss ou rejeição explícita, nunca uso silencioso do bloco incompatível.

Plano de avaliação proposto:
Plano proposto: comparar índice simples e identidade completa com entradas multimodais e trocas de adaptador. Medir falsos hits, misses, bytes de metadados e TTFT; exigir ausência de mistura de estados no conjunto controlado.

Comparações:
- T082 (specializes): Acrescenta identidade e ciclo de vida ao reúso básico de prefixos.

Afirmação rastreável:
O desenho do vLLM inclui hashes extras para adaptadores, multimodalidade e salt de cache.
Suporte: direct; fontes: B-S005
Limite: Essa lista documenta uma implementação; não demonstra isolamento completo de qualquer implantação.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T083:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu identidade completa e aquisição segura de referências. Esta ficha transforma o rótulo amplo em uma política multinível de admissão, retenção e observabilidade, para que advanced corresponda a capacidades demonstráveis e não a duplicação de nomes.

Camadas com custo explícito
Separe blocos ativos na GPU, prefixos ociosos retidos e eventual armazenamento secundário. Cada promoção precisa declarar bytes movidos, tempo e compatibilidade. Não presuma que copiar KV da CPU sempre vence recomputar; a comparação depende do comprimento, interconexão, disponibilidade do worker e urgência da requisição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

Admissão resistente à poluição
Um cliente pode enviar muitos prefixos únicos e deslocar conteúdo útil. Adote cotas por domínio, frequência mínima ou retenção limitada para entradas de uma só utilização. A política deve proteger sequências ativas e manter estatísticas por origem, sem transformar um prefixo compartilhado em canal de acesso a conteúdo de outro domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

Métricas por etapa do cache
Exponha busca de identidade, hit lógico, disponibilidade física e tempo de aquisição separadamente. Um índice pode anunciar um bloco que já foi removido ou que ainda está sendo transferido. Registre miss por incompatibilidade, expiração e capacidade; isso permite corrigir a política certa sem atribuir todo fracasso à taxa de hit.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

USO AVANÇADO — Serviço com vários adaptadores
Cenário: Clientes usam a mesma base com comportamentos especializados.
Estratégia: Inclua adaptador e revisão na chave, reserve orçamento por grupo e compartilhe somente estados cuja equivalência esteja comprovada. Evite usar o ID do modelo base como chave universal. Teste promoção e invalidação enquanto pedidos antigos ainda executam.
Papel do modelo pequeno: Modelos 3–30B podem compartilhar infraestrutura, mantendo seus estados computacionais separados.
Aceite proposto: Exigir zero falso hit nos testes e custo menor que caches totalmente isolados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

USO AVANÇADO — Retenção entre reinícios
Cenário: Prompts institucionais são caros de reconstruir e muito recorrentes.
Estratégia: Avalie armazenamento secundário para um conjunto pequeno de prefixos validados. Carregue sob demanda, confirme manifesto e descarte artefatos de revisão incompatível. Use TTL como política econômica, não como prova de validade.
Papel do modelo pequeno: Um alvo 15–30B pode economizar prefill se transferência for efetivamente mais barata.
Aceite proposto: Medir retomada fria, bytes transferidos e impacto nas requisições sem reuso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S005, V3D-S004, V4B-S004.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, começar com cache local simples; múltiplas camadas podem adicionar mais coordenação que economia.
8–14B: Em 8–14B, quotas por adaptador e observabilidade de misses tendem a ser prioridades antes de tiering.
15–30B: Em 15–30B, investigar armazenamento secundário somente após medir a pressão KV e a frequência de revisitas.
Requisitos de treino/runtime: Requer recursos concretos do runtime; nome advanced não implica transferência, isolamento ou persistência já implementados.
Não aplicar quando: Não usar índice de similaridade textual para reutilizar tensores exatos nem prometer todas as funções sob um único nome.

## T083:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Hierarquia e prefetch ampliam a política de reutilização de prefixos descrita.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002.

## T083:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T083 → T105 [complements]
Como combinar: Aplicar remoção por valor e referência ativa em cada camada de armazenamento.
Interface: Uso recente, custo de reconstrução, bytes e contagem de referências.
Condição: A remoção não toca estado necessário a um decode em andamento.
Aceite proposto: Injetar pressão e verificar que sequências ativas permanecem corretas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S005, V3D-S004, V4B-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T083 → T157 [requires]
Como combinar: Identificar prefixos e versões antes de consultar níveis de cache.
Interface: Hash encadeado, metadados multimodais e domínio de isolamento.
Condição: A serialização da identidade é determinística.
Aceite proposto: Alterar um componente por vez e exigir miss apropriado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S005, V3D-S004, V4B-S004. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Distinguir hit de índice de estado realmente pronto para consumo.
- Limitar promoção de prefixos únicos e testar concorrência na invalidação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo e SLO de workloads recorrentes com uma API de fronteira que ofereça cache documentado. O resultado caracteriza eficiência operacional, sem inferir equivalência de capacidades cognitivas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T103, T104, T105, T120

## Fontes primárias associadas

### B-S005 — Automatic Prefix Caching — design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos por prefixo, tokens e metadados; isolamento de reutilização por salt.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S004 — Automatic Prefix Caching — vLLM design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos, hash do prefixo anterior, tokens e fatores adicionais como adaptador, multimodalidade e cache_salt.

Limite: Documentação latest; não comprova configuração instalada nem ganho local.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

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
