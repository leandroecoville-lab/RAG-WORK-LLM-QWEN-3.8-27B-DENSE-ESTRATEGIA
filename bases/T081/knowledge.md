# T081 — KV Cache Reuse

**Nome canônico:** KV Cache Reuse  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T081  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reuso de cache de chaves e valores

## T081:C01 — conceito

Reutiliza tensores de chaves e valores já calculados para tokens anteriores, evitando repetir parte do processamento autorregressivo. Há reuso dentro da própria geração e reuso de prefixos entre chamadas. Esses estados computacionais não são memória semântica, histórico textual nem uma resposta pronta.

Como funciona:
- No prefill, calcular estados KV das posições válidas.
- Em cada passo de decode, acrescentar os novos estados sem recalcular todo o prefixo.
- Ao reutilizar entre chamadas, conferir identidade do modelo, sequência e condições de execução.

## T081:C02 — aplicacao

Quando usar:
- Geração de vários tokens com arquitetura que oferece cache.
- Continuação de um prefixo realmente idêntico.

Quando não usar:
- Reusar estados após alterar pesos, adaptador, tokens anteriores ou configuração posicional incompatível.

Implementação proposta:
- Inventariar quais camadas possuem KV e quais usam outros estados recorrentes.
- Estimar memória por sequência e concorrência, incluindo overhead de alocação.
- Registrar revisão do modelo e invalidação do cache no ciclo de deploy.

Aplicação LAI proposta:
Proposta LAI: tratar KV como aceleração descartável do runtime; manter estado de missão e documentos em memória persistente separada.

## T081:C03 — riscos_validacao

Armadilhas:
- Textos visualmente semelhantes podem tokenizar de maneira diferente.
- Duplicar ou anexar incorretamente o último token ao retomar altera posições e saída.

Métricas sugeridas:
- Memória KV por sequência e tokens efetivamente reaproveitados.
- Tempo por token com cache ligado e desligado em entrada igual.

Testes propostos:
- Retomar uma sequência com cache e comparar logits com recomputação completa dentro da tolerância numérica.
- Mudar um token antigo e exigir invalidação do trecho afetado e de seus sucessores.

## T081:C04 — perguntas_proveniencia

Pergunta: KV guarda o conhecimento da empresa?
Resposta: Não. Guarda representações dependentes de uma execução específica do modelo.

Pergunta: Posso reutilizar em outro modelo?
Resposta: Não de forma geral; formato e significado dos estados dependem dos pesos e da arquitetura.

Pergunta: Cache elimina todo custo quadrático?
Resposta: Evita refazer o prefixo a cada passo; o prefill denso ainda possui interações quadráticas entre tokens.

Pergunta: Texto idêntico basta para reutilizar?
Resposta: Não. Tokenização, posições, máscara e estado do modelo precisam corresponder, inclusive quando o template de conversa muda.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T081:C05 — mecanismo_avancado

O cache evita recalcular projeções de tokens anteriores, mas a consulta nova ainda interage com as chaves preservadas. Portanto, atenção densa no decode mantém custo dependente do contexto. Em um loop incremental, devem entrar somente tokens ainda não processados, enquanto a máscara representa a extensão anterior mais a nova. Posições, pesos e adaptadores fazem parte da identidade lógica desse estado.

Condição de contorno:
Prefixos editados, máscaras diferentes ou mudança de modelo invalidam estados mesmo quando parte do texto visível permanece igual.

Contrato proposto:
- Entradas: Tokens incrementais, posições, máscara completa e identidade do modelo.
- Saídas: Logits atuais e cache estendido com comprimento lógico explícito.
- Estado: Chaves e valores por camada, posições válidas e revisão do prefixo.
- Invariante: O cache representa exatamente o mesmo prefixo usado para calcular os logits.

Compromissos de projeto:
- Menos recomputação exige memória crescente em atenção global.
- Pré-alocação facilita estabilidade de formas, mas pode reservar capacidade ociosa.

## T081:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar continuação com padding e depois alterar um token inicial sem invalidar o cache. Comparar logits com recomputação integral; a reutilização incompatível deve falhar na validação.

Plano de avaliação proposto:
Plano proposto: controlar pesos, dtype, máscara e sequência; comparar execução incremental com recomputação completa. Registrar erro numérico tolerado pelo backend, bytes por camada e latência por comprimento; avaliar separadamente prefill e decode.

Comparações:
- T116 (alternative): Recomputação recupera estados ausentes ao custo de trabalho adicional de inferência.

Afirmação rastreável:
A documentação de cache exige máscara cobrindo tokens passados e atuais no loop incremental.
Suporte: direct; fontes: V3B-S005
Limite: O contrato concreto depende da arquitetura; atenção bidirecional não herda automaticamente a propriedade causal.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T081:C07 — estrategia_3_30b

NOVA CAMADA v4 — Além da identidade dos estados explicada na v3, esta ficha trata KV como artefato de execução com ciclo de vida: aquisição, validação, empréstimo, migração e reconstrução. A prioridade é evitar que otimização torne recuperação operacional frágil.

Manifesto de estado
Associe ao cache um manifesto com revisão de pesos, adaptador, tokenizer, posições, formato numérico e comprimento confirmado. O manifesto deve ser verificável antes de anexar novos tokens. Um blob legível pode estar semanticamente incompatível; checksum prova integridade de bytes, não equivalência da configuração que os produziu.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

Empréstimo e propriedade
Distingua uma referência compartilhada somente para leitura de uma continuação que pode escrever. Ao criar ramificações, use referências contadas ou cópia controlada para as regiões mutáveis. Uma requisição cancelada não pode liberar blocos ainda consumidos por outra; a contabilidade deve acompanhar o ciclo completo do consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

Recuperação desacoplada
Projete o serviço para reconstruir KV a partir dos tokens confirmados quando a afinidade se perder. Persistir todos os tensores pode ser mais caro que recalcular um prefixo curto. A decisão de persistência deve considerar tempo de retomada, bytes transferidos, taxa de falha e frequência real de revisita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

USO AVANÇADO — Continuação após mudança de worker
Cenário: Um agente retorna à conversa depois de expiração ou reinício.
Estratégia: Negocie compatibilidade do manifesto; se for exata, transfira o estado suportado. Caso contrário, reproduza os tokens confirmados no destino. Diferencie retomar a computação de repetir ações externas já realizadas.
Papel do modelo pequeno: Modelos 3–30B podem reconstruir contexto local sem depender de memória KV durável.
Aceite proposto: Aceitar com mesmo histórico lógico e sem duplicação de efeitos; medir custo de reconstrução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

USO AVANÇADO — Comparação de alternativas
Cenário: Um planejador abre duas continuações do mesmo prefixo.
Estratégia: Compartilhe o prefixo imutável, mantenha sufixos independentes e descarte o ramo perdedor após seleção. Não misture tokens de ramos diferentes ao consolidar a conversa, mesmo que os prompts tenham o mesmo texto inicial.
Papel do modelo pequeno: Um modelo pequeno pode explorar alternativas dentro de um orçamento explícito de memória.
Aceite proposto: Verificar independência dos ramos e bytes adicionais realmente alocados por continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, B-S003, V4B-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, reconstrução pode ser simples o bastante para dispensar transferência persistente de grandes blobs.
8–14B: Em 8–14B, comparar retenção local de sessões ativas com recomputação de sessões raras.
15–30B: Em 15–30B, projetar migração conforme volume KV e capacidade de cada worker, evitando reservar memória inutilizada.
Requisitos de treino/runtime: Reuso é runtime; mudanças de adaptador, posição ou representação exigem invalidação ou conversão formalmente suportada.
Não aplicar quando: Não usar KV como histórico auditável nem recuperar conversa a partir de estado sem tokens e configuração de origem.

## T081:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: A arquitetura reutiliza KV como recurso compartilhado do serving.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

V4B-C002 — Perplexity / Engine de inferência com KV Messenger
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A equipe descreve sua implementação de serving com workers de prefill e decode separados e um KV Messenger que coordena o transporte de estados.
Mecanismo documentado: Transferência por camada e páginas via libfabric/RDMA, seguida de sinalização de conclusão antes de admitir decode; certos métodos exigem estado auxiliar.
Correspondência com esta base: O decode consome estado recebido, mas o caso não demonstra todo tipo de reuso entre requisições.
Transferência proposta para modelo pequeno: Proposta: considerar o desenho para 15–30B apenas quando interferência entre fases justificar rede e coordenação; comparar primeiro com chunked prefill agregado.
Limite: Fonte não fixa porte do modelo em cada deployment. Não autoriza prometer redução de TTFT: transporte pode aumentá-lo. Não é uma bigtech na classificação estrita.
Fontes: V4B-S002.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: Blocos KV podem ser reutilizados entre requisições elegíveis.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

V4B-C015 — Guidance / Guidance — geração programática
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.
Mecanismo documentado: Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.
Correspondência com esta base: Objetos de modelo podem compartilhar estado, sem comprovar todos os cenários de cache distribuído.
Transferência proposta para modelo pequeno: Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.
Limite: Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.
Fontes: V4B-S030, V3D-S015, V3D-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002, V4B-Q003.

## T081:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T081 → T116 [alternative]
Como combinar: Recalcular quando custo ou incompatibilidade tornam transferência inadequada.
Interface: Tokens confirmados, máscara e manifesto de execução.
Condição: O histórico original é reconstruível.
Aceite proposto: Comparar logits e saída sob tolerância definida do backend.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, B-S003, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T081 → T060 [complements]
Como combinar: Salvar progresso lógico independentemente do cache computacional.
Interface: Revisão da sessão, resultados aceitos e referências de artefatos.
Condição: Checkpoint distingue efeitos concluídos de geração parcial.
Aceite proposto: Reiniciar sem KV e verificar continuidade da missão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, B-S003, V4B-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Nunca aceitar comprimento confirmado maior que os tokens disponíveis.
- Testar liberação concorrente e cache perdido durante uma ramificação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar retomada de uma tarefa real contra um serviço de fronteira com o mesmo contexto. Menor tempo de prefill pode melhorar custo e experiência, mas não resolve lacunas de entendimento do modelo.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T084, T086, T105, T116

## Fontes primárias associadas

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S005 — How caching works

[https://huggingface.co/docs/transformers/main/en/cache_explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Semântica causal de reutilização KV, máscara cobrindo passado e presente, estado por camada.

Limite: Documentação dinâmica main consultada em 2026-11-05; contrato de sessão é inferência editorial, não API documentada.

### V4B-S002 — Disaggregated Prefill and Decode

[https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode](https://www.perplexity.ai/en-GB/hub/blog/disaggregated-prefill-and-decode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação própria de prefill/decode separados, KV Messenger, transferência por camada e RDMA com libfabric.

Limite: Descrição do operador sem garantir compatibilidade local ou benefício para modelos pequenos; TTFT inclui transferência.

### V3D-S014 — Guidance — guidance.json

[https://guidance.readthedocs.io/en/latest/generated/guidance.json.html](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contrato da geração JSON e limitações de suporte a recursos de JSON Schema.

Limite: Suporte depende da versão; saída final e regras de domínio precisam de validação própria.

### V3D-S015 — Guidance — Introduction

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo programático e diferenças de capacidade entre backends locais e remotos.

Limite: Compartilhamento interno de recursos não implica fronteira de segurança ou equivalência de provedores.

### V4B-S030 — Token healing — Guidance

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de fronteiras de tokenização por recuo e prefixo restrito; integração documentada com LlamaCpp/Transformers.

Limite: Exemplos não comprovam qualidade de domínio nem implementação eficiente em todo provedor remoto.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

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

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
