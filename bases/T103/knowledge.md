# T103 — Prefix Tree / Trie de prefixos

**Nome canônico:** Prefix Tree / Trie de Prefixos  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T103  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** prefix trie; árvore de prefixos; Prefix Tree / Trie de Prefixos

## T103:C01 — conceito

Estrutura de dados que organiza sequências pelo início compartilhado. Em um índice de cache, cada caminho pode apontar para estados associados ao prefixo. Uma radix tree comprime caminhos de filho único em arestas mais longas; a estrutura sozinha não executa atenção.

Como funciona:
- Percorrer tokens em ordem para localizar o maior prefixo comum.
- Criar ou dividir caminhos quando novas sequências divergem.
- Associar referências de estado aos trechos e atualizar o índice após remoções.

## T103:C02 — aplicacao

Quando usar:
- Muitas sequências compartilham segmentos iniciais extensos.
- É útil localizar o maior prefixo disponível em vez de somente um hash de prompt inteiro.

Quando não usar:
- Usar similaridade semântica como se significasse identidade de tokens para cache KV exato.

Implementação proposta:
- Definir chaves com tokens e escopo de modelo, adaptador e tenant.
- Separar nós do índice de alocações físicas para permitir remoção segura.
- Documentar operações atômicas de inserir, consultar, dividir e invalidar.

Aplicação LAI proposta:
Proposta LAI: estudar a estrutura para entender o runtime e o roteamento; evitar construir uma trie paralela na Helena sem necessidade operacional.

## T103:C03 — riscos_validacao

Armadilhas:
- Índice stale pode apontar para memória já liberada.
- Textos com o mesmo início visível podem ter tokens diferentes devido ao template ou espaços.

Métricas sugeridas:
- Tamanho do índice, custo de busca e comprimento do prefixo encontrado.
- Taxa de referências inválidas e memória liberada após remoções.

Testes propostos:
- Inserir sequências com prefixos comuns em ordens diferentes e exigir resultados equivalentes de busca.
- Remover uma folha sem afetar irmãos e remover o último uso sem deixar referências pendentes.

## T103:C04 — perguntas_proveniencia

Pergunta: Trie é igual a árvore de resumos?
Resposta: Não. Organiza prefixos de sequências exatas, não níveis de abstração semântica.

Pergunta: Radix tree é outra família de cache?
Resposta: É uma variação compactada da estrutura de prefixos, usada por algumas implementações de cache.

Pergunta: Pode indexar pelo texto decodificado?
Resposta: Somente com um contrato que preserve identidade de tokenização; textos aparentes iguais não garantem os mesmos IDs.

Pergunta: Dividir uma aresta exige copiar todo o KV?
Resposta: Não necessariamente. A divisão lógica pode alterar referências para segmentos existentes quando o armazenamento permite compartilhamento.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T103:C05 — mecanismo_avancado

A árvore representa ancestralidade exata: compartilhar um sufixo textual não torna dois caminhos equivalentes se seus prefixos anteriores diferem. Numa radix tree, uma aresta pode carregar vários tokens; uma divergência no meio dessa aresta exige divisão sem perder a correspondência entre posições e referências KV. A complexidade de busca depende dos tokens comparados e da representação das arestas, não somente do número de nós.

Condição de contorno:
Uma árvore de strings normalizadas pode produzir identidade diferente da tokenização realmente usada pelo modelo.

Contrato proposto:
- Entradas: Sequências de token IDs, domínio de identidade e referências dos estados disponíveis.
- Saídas: Maior prefixo compatível e ponto exato para inserir ou dividir caminhos.
- Estado: Rótulos de arestas, ligações, comprimentos e referências de cache.
- Invariante: O caminho completo desde a raiz identifica o contexto; um nó isolado não basta.

Compromissos de projeto:
- Arestas comprimidas reduzem nós e complicam divisões parciais.
- Índice maior melhora cobertura potencial e aumenta manutenção e memória de CPU.

## T103:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir sequências que divergem dentro da mesma aresta e outras com sufixos iguais. Esperar divisão correta e nenhum hit baseado apenas na igualdade dos últimos tokens.

Plano de avaliação proposto:
Plano proposto: comparar trie simples e radix tree com as mesmas sequências. Medir tokens comparados, nós, memória e tempo de atualização; exigir que todas as buscas concordem com uma referência linear de maior prefixo.

Comparações:
- T104 (complements): RadixAttention usa a estrutura para organizar estados; a árvore sozinha não executa atenção.

Afirmação rastreável:
O SGLang descreve radix tree com arestas que podem representar sequências de tokens de comprimentos variados.
Suporte: direct; fontes: V3B-S011
Limite: A estrutura de dados não determina política de escalonamento, memória física ou validade dos pesos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T103:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou ancestralidade e divisão de arestas. Esta camada trata o trie como catálogo de disponibilidade distribuída: possuir um caminho lógico não significa que seus tensores estejam prontos para consumo.

Identidade versus residência
Separe a chave lógica, formada pelo prefixo tokenizado e sua configuração, do descritor de residência. Um nó pode apontar para GPU, RAM, armazenamento ou reconstrução pendente. A consulta deve retornar comprimento reutilizável e custo estimado de materialização; considerar todo nó encontrado um hit rápido mascara transferências e pode piorar a primeira resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Publicação de caminhos
Insira referências inicialmente privadas e publique apenas estados completos. Se o produtor for cancelado durante prefill, o caminho não pode anunciar um bloco parcialmente escrito. Um protocolo proposto marca geração, quantidade válida e confirmação; consumidores leem uma visão consistente enquanto divisões de arestas e remoções avançam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

Granularidade de persistência
Uma árvore pode comprimir arestas em tokens, enquanto o armazenamento transfere páginas maiores. Mantenha o deslocamento entre ambas as unidades e contabilize bytes úteis versus transportados. Prefixos ligeiramente divergentes podem multiplicar páginas mesmo quando a representação lógica permanece compacta; a cardinalidade dos nós não estima sozinha o consumo físico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Biblioteca de ferramentas estável
Cenário: Agentes compartilham descrições extensas de ferramentas.
Estratégia: Ordene componentes por estabilidade, versione o template e mantenha dados voláteis após a região compartilhada. Consulte a árvore antes de reservar a cópia física, preservando isolamento entre locatários.
Papel do modelo pequeno: Um 3–7B consome um contrato de ferramentas consistente sem depender de memória paramétrica adicional.
Aceite proposto: Comparar tokens reutilizados e bytes transferidos, além de testar revogação de ferramentas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

USO AVANÇADO — Auditoria de divergência
Cenário: Duas versões do serviço perdem reutilização inesperadamente.
Estratégia: Instrumente o primeiro token divergente, a versão do tokenizer e o template. Produza um diagnóstico agregado sem registrar segredos presentes nos prompts.
Papel do modelo pequeno: Um modelo pequeno pode explicar relatórios já sanitizados; o cálculo da divergência é determinístico.
Aceite proposto: Localizar mudanças introduzidas deliberadamente e não confundir divergência legítima com erro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S011, V4B-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Priorize poucos prefixos de alta repetição; uma árvore ampla pode custar mais que recomputar prompts curtos.
8–14B: Teste várias famílias de prompts e limite a retenção por família, evitando que um fluxo domine o catálogo.
15–30B: Modele residência por dispositivo: encontrar um prefixo de um 30B pode exigir transferência incompatível com o prazo.
Requisitos de treino/runtime: Recurso de runtime; tokenizer, pesos, adapters e posições participam da identidade.
Não aplicar quando: Não reutilizar caminhos entre configurações incompatíveis ou usar semântica textual aproximada como igualdade KV.

## T103:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C009 — Mooncake / SGLang community / SGLang HiCache com backend Mooncake
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Documentação da integração descreve o fluxo de busca local, prefetch remoto e write-back de KV.
Mecanismo documentado: HiRadixTree relaciona prefixos a camadas GPU/host/distribuída; Transfer Engine move dados e componentes de controle resolvem localização.
Correspondência com esta base: HiRadixTree organiza spans de tokens e seus locais de armazenamento.
Transferência proposta para modelo pequeno: Proposta: para 8–30B com prefixos longos repetidos, testar promoção por custo evitado e usar offload somente quando acesso remoto for melhor que recomputação; validar identidade de modelo, adaptador e tokens antes de reutilizar.
Limite: Integração disponível, não prova de implantação própria de Big Tech nem de todas as opções em Kimi. Roteamento atual e revisão do runtime precisam ser fixados. Modelo pequeno e tráfego baixo podem perder desempenho com a complexidade adicional.
Fontes: V4D-S017, V4D-S018, V4D-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q022.

## T103:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T103 → T104 [feeds]
Como combinar: A árvore fornece candidatos de prefixo para a política de Radix Attention.
Interface: Comprimento compatível, referências, residência e custo.
Condição: O escalonador interpreta somente estados confirmados.
Aceite proposto: Cancelar produtores e verificar que consumidores não leem estados incompletos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T103 → T105 [complements]
Como combinar: Expulsão física atualiza disponibilidade sem apagar necessariamente a descrição lógica.
Interface: Estado de presença e plano de reconstrução.
Condição: Não existir consumidor ativo sem referência protegida.
Aceite proposto: Comparar resultado após restore com execução fria.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S011, V4B-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não exportar tokens de prompts privados em métricas de divergência.
- Testar split, merge e remoção concorrentes com prefixos que terminam dentro de uma página.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare o serviço completo em uma coleção fixa de consultas repetidas. O trie pode reduzir recomputação; não melhora a resposta de um modelo pequeno a uma pergunta que ele não consegue resolver.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T082, T104, T120

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
