# T093 — PagedAttention

**Nome canônico:** PagedAttention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T093  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção paginada

## T093:C01 — conceito

Gerencia o cache KV em blocos físicos que não precisam estar contíguos e usa uma tabela para traduzir posições lógicas. Reduz desperdício por reserva e fragmentação no serving. A paginação reorganiza armazenamento; por si só não remove tokens nem substitui atenção densa por esparsa.

Como funciona:
- Dividir o KV de cada sequência em blocos lógicos.
- Mapeá-los para blocos físicos disponíveis conforme a sequência cresce.
- Permitir compartilhamento compatível e liberar blocos quando nenhuma sequência precisar deles.

## T093:C02 — aplicacao

Quando usar:
- Muitas requisições concorrentes com comprimentos imprevisíveis.
- Geração com ramificações que compartilham prefixos.

Quando não usar:
- Esperar que paginação sozinha resolva falta de memória dos pesos ou aumente qualidade do modelo.

Implementação proposta:
- Usar o gerenciador do runtime, evitando implementar tabelas KV independentes na aplicação.
- Observar capacidade alocada, ocupada e desperdiçada em cargas variadas.
- Verificar limpeza após cancelamento, erro e encerramento de sequência.

Aplicação LAI proposta:
Proposta LAI: considerar paginação como recurso interno do servidor de inferência; a Helena deve observar capacidade e pressão, não manipular blocos diretamente.

## T093:C03 — riscos_validacao

Armadilhas:
- Blocos menores reduzem desperdício interno, mas podem elevar overhead de metadados e acesso.
- Compartilhar blocos mutáveis sem controle pode corromper ramificações de geração.

Métricas sugeridas:
- Fragmentação interna, blocos livres e sequências simultâneas.
- Throughput com prazo de latência fixo e eventos de preempção.

Testes propostos:
- Criar sequências de diferentes tamanhos, cancelar parte delas e confirmar recuperação da memória.
- Bifurcar um prefixo e verificar que escrever em uma continuação não altera a outra.

## T093:C04 — perguntas_proveniencia

Pergunta: PagedAttention comprime o conteúdo?
Resposta: Não. Organiza o armazenamento dos estados; quantização e poda são decisões distintas.

Pergunta: É igual ao paging do sistema operacional?
Resposta: Usa inspiração semelhante, mas gerencia estruturas específicas do cache KV do modelo.

Pergunta: Paginação comprime os valores?
Resposta: Não. Ela reorganiza alocação e compartilhamento; quantização é uma transformação separada da representação.

Pergunta: Pode liberar ao terminar uma resposta?
Resposta: Somente depois de remover sua referência e confirmar que nenhum outro consumidor utiliza aquele bloco físico.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T093:C05 — mecanismo_avancado

Compartilhar blocos físicos requer separar referência lógica de propriedade da escrita. Quando duas continuações compartilham um bloco parcialmente preenchido, a próxima escrita pode exigir cópia antes de modificar o conteúdo. A fragmentação restante depende da granularidade: para uma sequência com T tokens e blocos de B tokens, a capacidade alocada é ceil(T/B)·B, salvo compartilhamento e reservas adicionais.

Condição de contorno:
A paginação reduz desperdício de alocação; não reduz por si só a quantidade matemática de estados necessários à atenção.

Contrato proposto:
- Entradas: Comprimento lógico, tabela de blocos, referências compartilhadas e solicitação de crescimento.
- Saídas: Mapeamento atualizado e blocos privados quando houver escrita divergente.
- Estado: Contadores de referência, ocupação parcial e lista de blocos livres.
- Invariante: Nenhuma sequência observa uma escrita privada realizada por outra continuação.

Compromissos de projeto:
- Blocos menores reduzem sobra final e aumentam metadados e indireções.
- Compartilhamento economiza memória, mas requer contagem e cópia consistentes.

## T093:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: bifurcar duas gerações no meio de um bloco, escrever tokens diferentes e cancelar uma delas. Esperar preservação da outra saída e liberação somente quando não restarem referências.

Plano de avaliação proposto:
Plano proposto: comparar alocação contígua e paginada em comprimentos e ramificações controlados. Medir bytes úteis, reservados, cópias, falhas de alocação e throughput; decidir pela capacidade entregue e latência, incluindo custo de gestão.

Comparações:
- T082 (complements): Compartilhamento físico pode sustentar reúso de prefixos, mas identidade do conteúdo continua necessária.

Afirmação rastreável:
O projeto de PagedAttention usa contagem de referências e cópia na escrita para blocos compartilhados que divergem.
Suporte: direct; fontes: V3B-S009
Limite: A evidência descreve o desenho original; tamanho de bloco e políticas atuais dependem do runtime.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T093:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou fragmentação e cópia na escrita. O aprofundamento concentra-se na escolha do tamanho de bloco, isolamento de falhas e admissão por crescimento futuro, conectando o alocador de KV ao comportamento real do serviço.

Granularidade como compromisso
Blocos menores reduzem sobra no fim de sequências, mas ampliam tabelas, metadados e trabalho de tradução. Blocos maiores simplificam gestão e podem favorecer acesso, ao custo de desperdício. Escolha pelo perfil de comprimentos e ramificações, incluindo overhead do kernel; não maximize eficiência de bytes ignorando o tempo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

Reserva para crescimento
Uma sequência admitida precisa continuar crescendo até seu limite autorizado. Defina margem ou política explícita de preempção antes de esgotar páginas. Contar apenas o prompt inicial pode admitir pedidos demais e gerar recomputação repetida, aumentando o atraso justamente quando a memória parece estar bem utilizada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

Diagnóstico por invariantes
Mantenha relação verificável entre blocos lógicos, páginas físicas e referências ativas. Uma página reciclada precisa de identificação que impeça referências antigas de ler novo conteúdo. Teste estados de limite, cancelamento e compartilhamento; falhas no alocador podem produzir texto plausível de outra sequência sem um crash evidente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

USO AVANÇADO — Muitas respostas curtas
Cenário: Um endpoint recebe grande quantidade de extrações pequenas.
Estratégia: Meça sobra por sequência e custo das tabelas para diferentes granularidades suportadas. Compare capacidade útil mantendo o mesmo limite de saída. Não aumente simultaneamente batch e contexto ao avaliar o tamanho do bloco.
Papel do modelo pequeno: Um 3–14B pode ganhar concorrência quando desperdício do cache domina a capacidade.
Aceite proposto: Exigir memória útil maior sem piora relevante no tempo de serviço.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

USO AVANÇADO — Exploração com ramos
Cenário: Um agente avalia continuações alternativas de um prefixo.
Estratégia: Compartilhe páginas imutáveis, aplique cópia controlada na parte mutável e libere ramos descartados. A contabilidade deve reconhecer compartilhamento e impedir dupla liberação. Teste o ramo sobrevivente após cancelar os demais.
Papel do modelo pequeno: Um 15–30B pode explorar alternativas sem replicar todo o prefixo.
Aceite proposto: Verificar equivalência com ramos independentes e custo incremental de cada continuação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S009, V4B-S014, V4B-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, grande número de sequências curtas pode tornar metadados e fragmentação mais relevantes que pesos.
8–14B: Em 8–14B, medir tamanho de bloco junto da distribuição de saída e taxa de cancelamento.
15–30B: Em 15–30B, reservar crescimento evita ciclos de preempção que anulam a capacidade obtida.
Requisitos de treino/runtime: Paginação é runtime e precisa de kernel/alocador compatíveis; não altera o padrão lógico de atenção.
Não aplicar quando: Não interpretar páginas como chunking semântico nem remover páginas ainda necessárias para manter uma falsa meta de ocupação.

## T093:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C013 — Hugging Face / Transformers ContinuousBatchingManager
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação atual expõe geração por lote contínuo e interface para submissão e recuperação de requisições.
Mecanismo documentado: Configuração de memória/scheduling separada da configuração de geração, com recursos de cache paginado e prefixos conforme backend.
Correspondência com esta base: A documentação inclui gerenciamento paginado do cache.
Transferência proposta para modelo pequeno: Proposta: experimentar serving de 3–30B com manifestos de versão e comparação contra outros runtimes, sem presumir que uma API de biblioteca substitui todos os controles operacionais.
Limite: Guia não comprova uso por uma organização cliente. Defaults e APIs podem mudar; instalação local não foi executada.
Fontes: V4B-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q004, V4B-Q014.

## T093:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T093 → T105 [complements]
Como combinar: Expulsar apenas blocos ociosos ou preemptar conforme política explícita de reconstrução.
Interface: Referências, prioridade e custo de recomputação.
Condição: A validade de páginas ativas é protegida.
Aceite proposto: Simular pressão e comprovar ausência de leitura após reciclagem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S009, V4B-S014, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T093 → T118 [complements]
Como combinar: Alinhar gestão de páginas com shards de KV e conclusão dos ranks.
Interface: Mapeamentos por rank, comprimentos e confirmação coletiva.
Condição: Todos os participantes reconhecem a mesma sequência lógica.
Aceite proposto: Cancelar um pedido durante comunicação e verificar liberação consistente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S009, V4B-S014, V4B-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar reutilização agressiva de páginas com conteúdo sentinela.
- Contar memória de tabelas e reservas, não apenas tensores preenchidos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar capacidade de atender tarefas corretas com uma fronteira sob carga equivalente. PagedAttention reduz desperdício de armazenamento; não aumenta o conhecimento ou o alcance lógico da atenção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T088, T105, T116, R009

## Fontes primárias associadas

### B-S013 — Efficient Memory Management for Large Language Model Serving with PagedAttention

[https://arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Blocos não contíguos de KV, menor fragmentação e compartilhamento no serving.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S009 — Efficient Memory Management for Large Language Model Serving with PagedAttention — full text

[https://arxiv.org/html/2309.06180v1](https://arxiv.org/html/2309.06180v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Blocos lógicos/físicos, compartilhamento, contagem de referências e cópia na escrita.

Limite: Texto do projeto original; medições publicadas não são resultados da implantação do usuário.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

### V4B-S008 — How Amazon scaled Rufus by building multi-node inference using AWS Trainium chips and vLLM

[https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/](https://aws.amazon.com/blogs/machine-learning/how-amazon-scaled-rufus-by-building-multi-node-inference-using-aws-trainium-chips-and-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus lançado com inferência multinó, Neuron, vLLM e continuous batching; relato de tráfego Prime Day.

Limite: Arquitetura específica Trainium; não transpor escala, latência nem suporte de GPU a outro ambiente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
