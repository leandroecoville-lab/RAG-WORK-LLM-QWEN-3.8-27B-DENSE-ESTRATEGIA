# T157 — Prefix Hashing

**Nome canônico:** Prefix Hashing  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T157  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** hash de prefixos

## T157:C01 — conceito

Identificação de prefixos ou blocos de contexto por hash para localizar estados computacionais reutilizáveis. A identidade deve refletir os tokens e as condições relevantes da execução, não apenas texto visualmente semelhante. O hash serve para indexação; não prova que um conteúdo é verdadeiro.

Como funciona:
- Tokenizar com configuração compatível com o modelo servido.
- Combinar conteúdo, histórico ancestral e metadados necessários em uma chave.
- Reutilizar estado somente quando a identidade de cache corresponde.

## T157:C02 — aplicacao

Quando usar:
- Runtime com reutilização de KV cache para prefixos idênticos.
- Muitas chamadas compartilham instruções ou documentos estáveis.

Quando não usar:
- Reutilizar cache entre checkpoints, adaptadores ou tenants sem identidade compatível.

Implementação proposta:
- Incluir versão de modelo e configuração relevante no namespace do cache.
- Adotar hash apropriado e política de isolamento entre clientes.
- Testar invalidadores como troca de adaptador, template e conteúdo multimodal.

Aplicação LAI proposta:
Proposta: conferir a implementação real do servidor antes de organizar prompts da Helena para reaproveitamento de prefixo.

## T157:C03 — riscos_validacao

Armadilhas:
- Pequena mudança no começo do prompt invalida reutilização posterior.
- Hash de texto ignora diferenças introduzidas por template ou tokenização.

Métricas sugeridas:
- Taxa de acerto por blocos e tokens de prefill evitados.
- Número de reutilizações inválidas detectadas em testes de isolamento.

Testes propostos:
- Alterar um token do prefixo e verificar que blocos dependentes não são tratados como iguais.
- Trocar adaptador ou identidade de cliente e conferir segregação do cache.

## T157:C04 — perguntas_proveniencia

Pergunta: Hash semelhante indica prefixo parecido?
Resposta: Não em hash criptográfico comum; ele identifica igualdade do conteúdo representado.

Pergunta: Prefix hashing é semantic caching?
Resposta: Não. Reutilização exata de estado difere de aproximar perguntas pelo significado.

Pergunta: Texto igual garante KV igual?
Resposta: Não. Modelo, tokenização, adaptador e entradas multimodais podem alterar o cálculo apesar da aparência textual.

Pergunta: Por que incluir a identidade do bloco anterior?
Resposta: Porque a representação de um token depende do prefixo causal; igualar somente o bloco local ignora esse contexto.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T157:C05 — mecanismo_avancado

No desenho de prefix caching do vLLM, a identidade de um bloco depende do hash do bloco anterior, dos tokens do bloco e de extras relevantes. Encadear o pai impede tratar o mesmo fragmento como equivalente após históricos diferentes. Conteúdo multimodal merece atenção: placeholders textuais iguais podem corresponder a imagens distintas, exigindo identidade adicional. Adaptadores e grupos de compartilhamento também podem afetar a chave.

Condição de contorno:
Uma chave incompleta permite reutilização indevida; uma chave excessivamente específica destrói acertos sem necessidade.

Contrato proposto:
- Entradas: Tokens efetivos, ancestralidade do bloco, modelo e metadados de execução relevantes.
- Saídas: Chave de bloco e resolução para KV compatível ou cache miss.
- Estado: Mapa de blocos, contagens de referência e política de expiração.
- Invariante: Só blocos semanticamente equivalentes para o cálculo de atenção compartilham identidade.

Compromissos de projeto:
- Isolar grupos de cache reduz compartilhamento e evita mistura de domínios que devem permanecer separados.
- Blocos maiores reduzem metadados e podem perder reaproveitamento de prefixos parcialmente iguais.

## T157:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter tokens de placeholder e trocar a imagem ou o adaptador; exigir cache miss quando a representação computada mudar.

Plano de avaliação proposto:
Comparar reutilização com cache desabilitado, controlando modelo, tokenizer e entradas. Medir acerto de blocos, tempo de prefill, memória e igualdade esperada dos resultados numéricos. Considerar também mudanças de prefixo e cache frio.

Comparações:
- T171 (complements): Orquestração usa identidade de prefixo para estimar onde existe trabalho reutilizável.
- T150 (distinct_from): Singleflight compartilha uma execução em curso; hashing endereça estado computacional armazenado.

Afirmação rastreável:
O design vLLM inclui hash do pai, tokens e extras como LoRA, hashes multimodais e salt.
Suporte: direct; fontes: V3C-S015
Limite: A documentação descreve aquela implementação; não se deve presumir a mesma composição em outros backends.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T157:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhava hash encadeado de blocos. Esta camada considera migração de versões, isolamento entre domínios e investigação de falsos acertos, com decisões que preservam equivalência computacional.

Namespace de execução
Construa a identidade de cache a partir da configuração efetivamente servida, não do alias comercial do modelo. Troca de quantização, adaptador ou template deve ser avaliada como mudança de execução. Um namespace explícito reduz o risco de um alias mutável apontar para pesos novos enquanto blocos antigos continuam elegíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

Invalidar com alcance definido
Organize quais mudanças invalidam todos os blocos e quais afetam apenas uma ramificação do prefixo. Uma alteração no núcleo inicial invalida seus descendentes; mudar somente o último documento não precisa destruir prefixos anteriores compatíveis. Esse desenho permite publicar prompts novos com convivência controlada entre gerações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, V4C-S014.

Auditar equivalência
Acompanhe acertos por classe de chave e compare amostras com recomputação sem cache. Um resultado incorreto pode vir de colisão lógica por metadado ausente, mesmo sem colisão criptográfica. Testes devem trocar imagem, adaptador, tenant e template separadamente para localizar a dimensão que a chave deixou de representar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

USO AVANÇADO — Assistentes por organização
Cenário: Vários clientes usam instruções parecidas e documentos diferentes.
Estratégia: Compartilhe somente o prefixo cuja reutilização seja permitida e computacionalmente compatível; introduza identidade de domínio onde necessário. Documentos privados não se tornam compartilháveis apenas porque o texto inicial coincide. Compare isolamento estrito e compartilhamento aprovado sob carga.
Papel do modelo pequeno: 3–7B atende tarefas curtas; o runtime determina identidade, sem delegá-la ao modelo.
Aceite proposto: Proposta: nenhum reaproveitamento entre domínios proibidos e redução de prefill nos casos elegíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

USO AVANÇADO — Atualização de instruções
Cenário: O mesmo agente recebe uma revisão do núcleo operacional.
Estratégia: Publique nova geração do prompt, mantenha a anterior para execuções já iniciadas e contabilize aquecimento. Não misture tokens de um template com estado calculado por outro. Expire versões antigas quando suas execuções e requisitos de retenção terminarem.
Papel do modelo pequeno: 8–14B e 15–30B mantêm papéis; a compatibilidade depende da configuração, não do porte.
Aceite proposto: Proposta: resposta equivalente à recomputação e custo de aquecimento explicitado na migração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Beneficiar-se de prefixos curtos muito repetidos, sem esperar ganho quando decode domina.
8–14B: Usar templates estáveis de extração e registrar variações por tarefa.
15–30B: Reaproveitar instruções longas e repositórios comuns, medindo pressão de KV e concorrência.
Requisitos de treino/runtime: Backend com identidade documentada, política de expulsão e telemetria por versão; não reimplementar hash ad hoc.
Não aplicar quando: Não compartilhar estado entre modelos ou representações multimodais apenas porque textos visíveis são iguais.

## T157:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C008 — Moonshot AI / Kimi / Mooncake serving
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores identificam Mooncake como plataforma operacional do Kimi. O artigo histórico descreve a arquitetura; suas avaliações usam replay de traces e um modelo substituto.
Mecanismo documentado: Pool de KV e scheduler centrado em cache combinados com separação prefill/decode e controle de admissibilidade por SLO.
Correspondência com esta base: Seção 5.1/Algoritmo 1: chave de bloco combina tokens locais e hash do bloco anterior. Escopo histórico v1; sem transferir automaticamente métricas para 3–30B.
Transferência proposta para modelo pequeno: Proposta: testar decisão de transferir KV contra recomputar prefill, usando bytes, fila, reutilização e latência prevista; rejeitar cedo pedidos incapazes de cumprir SLO, preservando métricas de rejeição.
Limite: O artigo v1 descreve a plataforma Kimi, mas seus experimentos usam replay de traces e modelo substituto com arquitetura LLaMA2-70B. Métricas não são medições de um aluno 3–30B. A biblioteca atual e seus backends não são automaticamente a configuração histórica.
Fontes: V4D-S016, V4D-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes de vLLM e políticas Uber apoiam implementação e afinidade. Request collapsing de CDN não é prefix KV cache e não foi contado como o mesmo mecanismo.
Consultas registradas: V4C-Q009, V4C-Q017.

## T157:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T157 → T171 [feeds]
Como combinar: Fornecer identidade e idade de residência para decisão de afinidade, mantendo possibilidade de recomputar.
Interface: Chave de prefixo, namespace e timestamp de telemetria.
Condição: Estimativa de economia compete com espera na fila.
Aceite proposto: Rota correta mesmo após expulsão de bloco.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T157 → T155 [complements]
Como combinar: Avaliar edição do prompt também pelo quanto invalida prefixos frequentes.
Interface: Versões de módulos e distribuição de reutilização.
Condição: Qualidade é aprovada antes da economia de cache.
Aceite proposto: Comparar custo total após troca e não apenas tokens removidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Hash forte não corrige a ausência de uma dimensão semântica da chave.
- Telemetria de hit não comprova equivalência; manter teste de recomputação em mudanças de runtime.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare pequeno e fronteira com cache frio e quente separados. Vantagem por prefixo repetido é propriedade da carga e infraestrutura, não equivalência geral de raciocínio.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T103, T171

## Fontes primárias associadas

### C-S022 — Automatic Prefix Caching — vLLM

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos inclui hash ancestral, tokens e informações como adaptador e salt de isolamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4D-S016 — Mooncake — serving platform for Kimi

[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Operador identifica Mooncake como plataforma do Kimi; arquitetura com pool KV e prefill/decode separados, scheduler condicionado a SLO.

Limite: Separar resultados simulados e tráfego real. Não transferir ganhos publicados ou integrações adicionadas em 2026 a qualquer modelo/hardware/revisão histórica.

### V4D-S020 — Mooncake: Kimi’s KVCache-centric Architecture for LLM Serving

[https://arxiv.org/html/2407.00079v1](https://arxiv.org/html/2407.00079v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura Kimi descrita em v1: reuso/prefixos, prefill em blocos, batching contínuo, Messenger RDMA, hashes encadeados e roteamento por fila, cache e SLO (seções 3–5).

Limite: Conservar versão v1; experimentos incluem modelo substituto e replay de traces. Não atribuir recursos posteriores da biblioteca à implantação histórica.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
