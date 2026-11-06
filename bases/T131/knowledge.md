# T131 — Suffix Decoding

**Nome canônico:** SuffixDecoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T131  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** SuffixDecoding; decodificação por sufixos

## T131:C01 — conceito

SuffixDecoding propõe continuações a partir de padrões encontrados em árvores de sufixos de tokens do prompt e de gerações anteriores. É especulação sem pesos auxiliares. Não equivale a cache de respostas: o modelo alvo continua verificando o trecho candidato antes de aceitá-lo.

Como funciona:
- Manter estrutura de sufixos com sequências de tokens observadas.
- Buscar padrões que correspondam ao final da geração atual e selecionar continuações.
- Verificar no alvo, atualizar o histórico permitido e controlar retenção da estrutura.

## T131:C02 — aplicacao

Quando usar:
- Workflows iterativos repetem trechos de código, instruções ou tentativas.
- Há implementação compatível e custo de lookup pequeno para a carga.

Quando não usar:
- A estrutura cresce sem limite ou a carga não oferece repetição suficiente.

Implementação proposta:
- Definir limites de tokens armazenados e isolamento por domínio antes de habilitar pool compartilhado.
- Comparar com n-gramas simples e geração convencional no mesmo workload.
- Medir custo no host e na verificação sob diferentes níveis de concorrência.

Aplicação LAI proposta:
Proposta LAI: avaliar em ciclos de edição e verificação da Helena; manter a árvore como acelerador descartável, sem promovê-la a memória factual.

## T131:C03 — riscos_validacao

Armadilhas:
- Uma árvore grande pode consumir CPU e memória e anular o ganho da GPU.
- Histórico de outro domínio pode elevar candidatos ruins; compartilhamento exige política explícita.

Métricas sugeridas:
- Comprimento médio aceito, tempo de busca e atualização.
- Memória da árvore, throughput e p95 com concorrência crescente.

Testes propostos:
- Executar ciclos repetitivos e carga inédita; aceitar a técnica apenas onde houver benefício líquido.
- Evictar históricos e verificar continuidade correta, sem depender da estrutura para verdade ou persistência da missão.

## T131:C04 — perguntas_proveniencia

Pergunta: SuffixDecoding é memória episódica?
Resposta: Não. Armazena padrões úteis para propor tokens, sem avaliar se uma experiência foi correta.

Pergunta: Precisa treinar um modelo auxiliar?
Resposta: O método descrito é model-free na proposta; ainda depende de implementação e verificação no alvo.

Pergunta: O índice torna a resposta uma cópia obrigatória?
Resposta: Não. Ele fornece candidatos; o alvo deve rejeitar continuações incompatíveis com seu contexto atual.

Pergunta: Sem pesos adicionais significa custo zero?
Resposta: Não. Estruturas, contagens, consultas, sincronização e atualização consomem memória e tempo de CPU.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T131:C05 — mecanismo_avancado

Uma árvore de sufixos pode organizar continuações de múltiplas sequências, mas busca rápida não torna atualização gratuita. A implementação descrita pela Snowflake mantém informações de frequência para selecionar filhos, expondo uma troca entre tempo de consulta, atualização e memória. Sob alta concorrência, o proponente na CPU pode limitar o sistema mesmo quando a GPU verifica candidatos eficientemente.

Condição de contorno:
Históricos pouco repetitivos ou manutenção pesada da estrutura reduzem o benefício, independentemente da ausência de pesos adicionais.

Contrato proposto:
- Entradas: Tokens confirmados, histórico autorizado ao índice, limite de retenção e orçamento de proposta.
- Saídas: Continuação candidata com origem e comprimento explícitos.
- Estado: Árvores locais/compartilhadas, contagens e política de remoção de sequências.
- Invariante: Atualizações e remoções preservam contagens e não deixam referências a sequências ausentes.

Compromissos de projeto:
- Reter mais sequências amplia cobertura e custo de memória.
- Pré-organizar filhos acelera escolha e acrescenta manutenção quando contagens mudam.

## T131:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover uma sequência muito frequente enquanto outras usam seus padrões e inserir continuações novas. Esperar consistência de referências e contagens, com verificação normal dos candidatos restantes.

Plano de avaliação proposto:
Plano proposto: comparar N-Gram e sufixos na mesma mistura repetitiva e não repetitiva. Medir tempo CPU de atualização/consulta, memória, verificação e latência total por concorrência; aceitar benefício sem esconder custo do proponente.

Comparações:
- T103 (distinct_from): Uma trie de prefixos indexa ancestralidade KV; a estrutura de sufixos encontra padrões para propor novos tokens.

Afirmação rastreável:
O relato técnico da Snowflake descreve árvores de sufixos e estruturas auxiliares para reduzir custo de selecionar continuações.
Suporte: direct; fontes: B-S040
Limite: Os ganhos relatados pertencem às cargas avaliadas; não garantem superioridade em toda tarefa.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T131:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou atualização de árvores e gargalo de CPU. A nova camada considera envelhecimento de padrões, compartilhamento controlado e avaliação da adaptação a mudanças de domínio.

Memória de padrões
Frequências antigas podem favorecer continuações que deixaram de ser comuns. Uma política proposta limita retenção por idade ou quantidade de tokens e compara seu efeito com índice só da requisição. O objetivo é evitar que histórico volumoso aumente custo e reduza relevância sem melhorar aceitação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

Compartilhamento e isolamento
Árvores locais e compartilhadas têm propriedades diferentes. Um índice compartilhado pode aproveitar repetição entre pedidos, mas exige separar domínios de acesso e versões de tokenização. O verificador do alvo não substitui a política de quais dados podem participar da proposta; metadados de origem precisam acompanhar o índice.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

Medição da contribuição
Compare contra n-gram simples e contra nenhum proponente. Separe custo de construção, atualização, consulta e verificação, incluindo aquecimento do índice. Se a avaliação começa com um índice preenchido por exemplos do teste, o resultado não representa uma implantação sem esse conhecimento prévio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

USO AVANÇADO — Geração de código repetitiva
Cenário: Muitos pedidos seguem APIs e padrões semelhantes.
Estratégia: Use histórico autorizado e versionado, limite retenção e avalie mudanças de biblioteca. O alvo verifica propostas, e compilação ou testes avaliam a tarefa depois.
Papel do modelo pequeno: Um 8–14B pode produzir alterações locais com repertório repetitivo.
Aceite proposto: Medir latência e correção executável, incluindo APIs raras e mudanças de versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

USO AVANÇADO — Lotes com documentos padronizados
Cenário: Saídas compartilham trechos e estruturas.
Estratégia: Construa um índice a partir de dados permitidos, mantenha um controle frio e teste deriva no padrão. Evite transformar o índice em repositório invisível de informações sensíveis.
Papel do modelo pequeno: Um 15–30B pode aproveitar repetição quando o custo de verificação justifica a estrutura.
Aceite proposto: Comparar ganho líquido depois de incluir manutenção de CPU e memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S040, V3B-S001, V4B-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Uma árvore sofisticada pode ser desnecessária para poucos pedidos e alvos baratos.
8–14B: Repetição entre tarefas pode justificar estudo, com limites claros de retenção.
15–30B: Em alta concorrência, CPU e sincronização podem limitar o sistema antes da GPU.
Requisitos de treino/runtime: Runtime e algoritmo de confirmação corretos; não exige atualização dos pesos do alvo.
Não aplicar quando: Não tratar benchmark de Suffix Decoding como prova de implantação nem assumir que frequência equivale a correção.

## T131:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C023 — Snowflake / Suffix Decoding
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: pesquisa sobre LLM.
Uso observado: A publicação apresenta método e avaliações de geração especulativa a partir de sufixos. O registro não transforma resultados experimentais em comprovação de implantação operacional.
Mecanismo documentado: Estruturas de sufixos usam histórico de tokens para propor continuações que precisam ser verificadas pelo alvo.
Correspondência com esta base: O mecanismo é suffix decoding.
Transferência proposta para modelo pequeno: Proposta: avaliar em saídas com forte repetição, incluindo custo de atualizar e consultar o índice em CPU.
Limite: Sem caso específico de bigtech implantada confirmado nesta fonte; ganho depende de repetição, alvo, concorrência e custo do proponente.
Fontes: B-S040.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fonte primária de Suffix Decoding e métricas de runtime consultadas. O caso selecionado é pesquisa; implantação específica de bigtech não foi confirmada neste recorte.
Consultas registradas: V4B-Q001, V4B-Q018.

## T131:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T131 → T130 [alternative]
Como combinar: N-gram simples é um baseline que ajuda a justificar a árvore de sufixos.
Interface: Mesmo histórico permitido e política de verificação.
Condição: Orçamentos de memória e CPU comparáveis.
Aceite proposto: Comparar ganho líquido e sensibilidade à mudança de domínio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S040, V3B-S001, V4B-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T131 → T080 [complements]
Como combinar: O horizonte pode reagir à aceitação e ao custo de consulta.
Interface: Propostas por posição e duração da rodada.
Condição: Ajuste não usa dados futuros nem altera a distribuição-alvo.
Aceite proposto: Medir adaptação após mudança controlada na repetição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S040, V3B-S001, V4B-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Eliminar referências a sequências removidas e corrigir contagens relacionadas.
- Separar aquecimento legítimo de vazamento do conjunto de avaliação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve avaliar o gerador completo na tarefa. A árvore melhora proposta de continuações; não adiciona compreensão geral nem transforma cópia provável em verdade.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T130, T103

## Fontes primárias associadas

### B-S040 — SuffixDecoding at Production Scale with Arctic Inference and vLLM

[https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/](https://www.snowflake.com/en/blog/engineering/suffixdecoding-arctic-inference-vllm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvores de sufixos sobre tokens anteriores produzem candidatos especulativos sem modelo auxiliar.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Algoritmo de aceitação, distribuição residual e análise idealizada de custo.

Limite: Texto do algoritmo e análise consultados; resultados experimentais não reproduzidos; pressupostos de paralelismo não certificam servidor local.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
