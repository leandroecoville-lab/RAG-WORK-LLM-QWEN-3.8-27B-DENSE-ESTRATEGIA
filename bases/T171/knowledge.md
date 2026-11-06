# T171 — Cache-Aware Orchestration

**Nome canônico:** Cache-Aware Orchestration  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T171  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** orquestração orientada a cache

## T171:C01 — conceito

Orquestração que considera possibilidade de reutilizar contexto ou resultados ao ordenar chamadas e escolher destinos. É uma política de sistema: um backend com prefixo reutilizável pode economizar prefill, mas esperar por ele pode aumentar a latência. A decisão deve avaliar o custo total.

Como funciona:
- Identificar partes estáveis e identidade de cache aplicável.
- Estimar benefício de reutilização junto com fila e carga do destino.
- Organizar chamadas sem violar dependências, atualidade ou isolamento.

## T171:C02 — aplicacao

Quando usar:
- Muitas tarefas usam instruções e documentos iguais.
- Múltiplas réplicas têm estados de cache diferentes.

Quando não usar:
- Maximizar acerto de cache sacrificando qualidade, permissão ou prazo da tarefa.

Implementação proposta:
- Manter prefixo estável quando o contrato permitir.
- Incluir versões e contexto de autorização nas chaves necessárias.
- Comparar política orientada a cache com balanceamento simples sob carga realista.

Aplicação LAI proposta:
Proposta: alinhar montagem de contexto da Helena com o cache do runtime somente depois de medir comportamento do servidor usado.

## T171:C03 — riscos_validacao

Armadilhas:
- Agrupar pedidos pode aumentar espera mais que economiza computação.
- Alterações pequenas no prefixo invalidam benefício estimado.

Métricas sugeridas:
- Tokens de prefill evitados e latência de cauda.
- Custo total incluindo fila, recomputação e invalidação.

Testes propostos:
- Variar tamanho de prefixo compartilhado e carga para medir ponto de benefício.
- Atualizar documento ou política e exigir invalidação correta.

## T171:C04 — perguntas_proveniencia

Pergunta: Prefixo estável sempre é melhor?
Resposta: Não se ele inclui conteúdo desnecessário ou desatualizado.

Pergunta: Cache-aware routing é a mesma coisa que semantic routing?
Resposta: Não. Um usa estado de reutilização; o outro usa significado da solicitação.

Pergunta: Mais cache hit significa menor latência sempre?
Resposta: Não. Uma fila longa ou custo de transferência pode superar a economia de prefill.

Pergunta: Cache miss após o roteamento deve mudar a resposta?
Resposta: Não por si. O backend deve recomputar o prefixo compatível; cache afeta custo e tempo, não a intenção da tarefa.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T171:C05 — mecanismo_avancado

A afinidade de cache deve competir com o custo de fila. Uma rota com prefixo reutilizável pode ser mais lenta que outra fria se estiver congestionada. Uma estimativa proposta soma espera, prefill não reutilizado, transferência e decode esperado. A informação de residência também envelhece: um bloco anunciado pode ser removido antes da admissão. O plano precisa tolerar cache miss sem alterar correção da resposta.

Condição de contorno:
Quando decode ou ferramenta externa domina o tempo, economizar prefill pode ter efeito pequeno sobre a latência final.

Contrato proposto:
- Entradas: Prefixos identificados, residência estimada, carga dos destinos e requisitos do modelo.
- Saídas: Rota elegível e expectativa separada de economia e espera.
- Estado: Hashes, versões, acertos observados e idade da telemetria.
- Invariante: Uma decisão por cache nunca troca modelo ou contexto incompatível apenas para aumentar acertos.

Compromissos de projeto:
- Afinidade aumenta reutilização e pode concentrar tráfego em poucos workers.
- Balancear carga distribui filas e pode duplicar prefixos na memória de vários destinos.

## T171:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: tornar o worker com cache quente lento e remover blocos após anunciar residência; exigir execução correta e registro de cache miss, sem insistência ilimitada no destino.

Plano de avaliação proposto:
Comparar balanceamento sem afinidade e política combinada sob diferentes tamanhos de prefixo e ocupação. Medir latência completa, prefill poupado, memória e desequilíbrio de filas. Decidir pela métrica de serviço, não só pela taxa de cache hit.

Comparações:
- T157 (complements): Identidade de prefixo permite verificar qual estado pode ser reutilizado.
- T120 (complements): Roteamento de KV é uma aplicação específica dessa consideração de residência e custo.

Afirmação rastreável:
O design de cache do vLLM identifica blocos reutilizáveis pelo contexto encadeado e metadados relevantes.
Suporte: related; fontes: V3C-S015
Limite: A fórmula de decisão entre fila e cache é uma proposta de orquestração, não garantia fornecida pelo hashing.

Nota de pesquisa:
Síntese técnica com contratos e testes propostos; não há alegação de implantação ou medição LAI.

## T171:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 comparava afinidade de cache e custo de fila. Esta camada organiza prompts, tarefas e duração de sessões para preservar reutilização sem concentrar carga nem confundir cache de conteúdo com estado cognitivo.

Reutilização por fase
Agrupe tarefas que compartilham instruções e evidências estáveis, mas mantenha dados específicos depois desse prefixo. A ordenação só vale quando preserva semântica e isolamento. Um agrupamento excessivo pode esperar por tarefas futuras e aumentar latência; defina limite de espera e permita envio frio quando o prazo exigir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, V4C-S014.

Retenção conforme retorno provável
Uma sessão interativa pode voltar várias vezes ao mesmo prefixo, enquanto um trabalhador curto pode nunca reutilizá-lo. Avalie política de retenção pela frequência e intervalo de retorno, incluindo custo e pressão de memória. O perfil operacional relatado pela Uber é evidência de diferenciação, não valor universal de TTL.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014.

Caminhos de falha
Se a rota quente falhar, o plano precisa funcionar com recomputação fria em destino compatível. Carregue referências suficientes para reconstruir entrada, não só uma indicação de que havia cache. Se a implementação distribui KV, verifique custo e compatibilidade de transferência antes de presumir ganho.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015, B-S032.

USO AVANÇADO — Extração de muitos registros
Cenário: Várias chamadas aplicam o mesmo manual a dados diferentes.
Estratégia: Mantenha manual e exemplos estáveis, distribua registros em lotes que caibam no contrato e registre configuração. Compare afinidade com balanceamento simples sob cache frio, quente e saturado. Não reduza o manual necessário somente para aumentar throughput aparente.
Papel do modelo pequeno: 3–7B extrai campos repetitivos; verificação externa detecta desvios.
Aceite proposto: Proposta: menor custo de prefill por registro aceito sem aumento da cauda de latência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S015.

USO AVANÇADO — Especialistas de uma campanha
Cenário: Subagentes compartilham convenções do repositório, mas trabalham em módulos diferentes.
Estratégia: Prepare núcleo comum curto e anexe contexto de módulo após ele. Escolha retenção para a duração esperada dos lotes; não mantenha todo o KV de trabalhadores encerrados se não houver reuso plausível. Durante retomada, recupere documentos por versão e aceite cache miss.
Papel do modelo pequeno: 8–14B executa módulos; 15–30B coordena integração sem exigir cache compartilhado de toda a conversa.
Aceite proposto: Proposta: medir memória por tarefa, reutilização e custo completo da campanha.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Cargas repetitivas curtas podem beneficiar-se mais de throughput que de prefixos enormes.
8–14B: Templates especializados e estáveis oferecem reutilização previsível entre chamadas.
15–30B: Contextos maiores exigem avaliar benefício de prefill contra pressão de KV e concorrência.
Requisitos de treino/runtime: Telemetria de hits, filas, expulsões e versões; controle de isolamento e possibilidade de recomputação.
Não aplicar quando: Não escolher modelo incompatível ou adiar indefinidamente uma tarefa somente para aproveitar cache.

## T171:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Política de cache distingue sessões interativas e subagentes de duração curta.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber fornece caso operacional de ajuste por perfil. vLLM fundamenta identidade de blocos; políticas propostas não foram executadas neste pacote.
Consultas registradas: V4C-Q009, V4C-Q017.

## T171:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T171 → T169 [complements]
Como combinar: Uber diferencia perfis de uso e cache entre sessões e subagentes do harness.
Interface: Tipo de sessão, duração prevista e prefixo compatível.
Condição: A política de cache acompanha o ciclo do trabalhador.
Aceite proposto: Medir economia em chamadas aceitas, não apenas hits.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

2. T171 → T157 [complements]
Como combinar: Usar identidade completa do prefixo para decidir o que pode ser reutilizado.
Interface: Hash, namespace e configuração de execução.
Condição: Tokens e metadados de computação são compatíveis.
Aceite proposto: Troca de adaptador provoca invalidação adequada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Cache de resultado textual, prefix KV e singleflight resolvem problemas distintos.
- Queda de hit após deploy pode ser aquecimento legítimo; analisar junto de latência e qualidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare pequeno e fronteira sob taxas de repetição declaradas. Uma vantagem em carga cacheável pode desaparecer em perguntas únicas e não transfere capacidade de generalização.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T002, T082, T157

## Fontes primárias associadas

### C-S022 — Automatic Prefix Caching — vLLM

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de blocos inclui hash ancestral, tokens e informações como adaptador e salt de isolamento.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S054 — SGLang: Efficient Execution of Structured Language Model Programs

[https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Coordenação entre programas de LLM e runtime permite otimizar compartilhamento de contexto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### B-S032 — KV-Aware Routing

[https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing](https://docs.nvidia.com/dynamo/knowledge-base/concepts/system-architecture/kv-aware-routing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Roteamento considera reutilização KV e carga ativa; seleção e transferência são responsabilidades distintas.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
