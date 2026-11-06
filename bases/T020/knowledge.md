# T020 — Learned Prompt Compression

**Nome canônico:** Learned Prompt Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T020  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão aprendida de prompts

## T020:C01 — conceito

Família de compressão em que um modelo treinado decide o que preservar ou produz uma representação compacta. Inclui compressão textual e representações latentes como gist tokens. Essas saídas não são intercambiáveis: algumas exigem um modelo consumidor especificamente treinado.

Como funciona:
- Definir a representação de saída: texto, tokens especiais ou estados.
- Treinar ou selecionar compressor compatível com o consumidor.
- Avaliar perda de informação e custo do compressor na tarefa alvo.

## T020:C02 — aplicacao

Quando usar:
- Prompts longos recorrentes com economia potencial significativa.
- Cenários em que regras simples removem conteúdo importante.

Quando não usar:
- Não enviar vetores arbitrários a uma API textual esperando que ela compreenda a representação.

Implementação proposta:
- Proposta: versionar compressor, tokenizer e modelo consumidor conjuntamente.
- Separar tarefas de treino e avaliação por documentos e cenários.
- Preservar entrada original para comparação e fallback quando a fidelidade cair.

Aplicação LAI proposta:
Proposta LAI: testar após estabelecer uma linha de base de recuperação e seleção; a compatibilidade com o checkpoint local precisa ser comprovada.

## T020:C03 — riscos_validacao

Armadilhas:
- Compressão treinada em outro domínio pode apagar detalhes essenciais.
- Mudança do consumidor pode tornar a representação latente incompatível.

Métricas sugeridas:
- Qualidade por razão de compressão.
- Latência total, memória adicional e custo de treinamento amortizado.

Testes propostos:
- Avaliar casos fora do domínio e instruções com exceções.
- Comparar texto integral, compressão simples e compressor aprendido com orçamento idêntico.

## T020:C04 — perguntas_proveniencia

Pergunta: LLMLingua e gist tokens são a mesma coisa?
Resposta: Não. Um pode produzir texto reduzido; gist tokens dependem de uma representação aprendida e de suporte do consumidor.

Pergunta: É compressão sem perda?
Resposta: Em geral não. É uma aproximação cuja utilidade precisa ser medida na resposta final.

Pergunta: Compressor treinado dispensa validação de fidelidade?
Resposta: Não. O objetivo pode aproximar utilidade média sem preservar todos os detalhes críticos de uma aplicação específica.

Pergunta: Como versionar uma representação latente persistida?
Resposta: Vincule-a ao encoder, consumidor, tokenizer e configuração necessários. Se houver incompatibilidade, regenere a partir do original em vez de reinterpretar bytes silenciosamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T020:C05 — mecanismo_avancado

Aprender um compressor pode significar treinar seleção textual ou aprender um canal latente específico. No primeiro caso, a saída ainda pode circular entre consumidores de texto; no segundo, representação, máscara de atenção e modelo consumidor precisam ser compatíveis. O custo de treinamento e preparação deve ser amortizado pela quantidade de contextos ou chamadas em que o compressor será reutilizado.

Condição de contorno:
Mudanças de domínio, idioma, tokenizer ou consumidor podem invalidar a qualidade medida, mesmo quando o formato da saída continua aceito.

Contrato proposto:
- Entradas: Dados de treino separados da avaliação, objetivo de compressão e consumidor alvo.
- Saídas: Compressor versionado e representação com tipo e formato documentados.
- Estado: Pesos, tokenizer, configuração e relação entre entrada original e saída.
- Invariante: A avaliação mede a tarefa final em dados não usados para treinar ou escolher o compressor.

Compromissos de projeto:
- Seleção textual facilita inspeção, mas tem limites de compressão e pode quebrar relações.
- Slots latentes compactam mais agressivamente, porém diminuem portabilidade e auditabilidade direta.

## T020:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aplicar o compressor a exemplos de outro domínio contendo unidades e identificadores raros. Verificar preservação dos elementos necessários e reconhecer degradação em vez de extrapolar a validação original.

Plano de avaliação proposto:
Avaliação proposta: comparar método aprendido, seleção simples e texto integral, incluindo treinamento amortizado e custo por chamada. Controlar consumidor e orçamento; medir qualidade final, fidelidade e desempenho fora de distribuição.

Comparações:
- T052 (complements): Latent Context especifica uma possível representação, não a totalidade dos métodos aprendidos.
- T179 (distinct_from): Treinar um compressor não equivale necessariamente a internalizar a tarefa no modelo que responde.

Afirmação rastreável:
LLMLingua-2 formula compressão como classificação de tokens; ICAE aprende slots de memória consumidos por uma LLM compatível.
Suporte: direct; fontes: V3A-S001, V3A-S004
Limite: Resultados dependem dos modelos e objetivos de treinamento utilizados nas respectivas pesquisas.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T020:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu compatibilidade e amortização. Aqui o desenho novo adapta compressor ao consumidor e acompanha mudanças de domínio.

Projeto e decomposição
Treine ou selecione compressor conforme o leitor final. Tokens que um modelo grande reconstrói podem ser ambíguos para 3–7B; a função de perda precisa refletir tarefa do consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

Controle adaptativo
Use perfil de compressão por domínio e detectar mudança de distribuição com amostras de reconstrução funcional. A detecção não exige restaurar todo o texto, mas preservar respostas a requisitos definidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

Validação contrafactual
Compare compressor universal, especializado e extração determinística. Inclua treino, manutenção e falhas de transferência no custo amortizado. Unidade de avaliação: par compressor-consumidor. Após quantizar ou trocar o consumidor, repetir teste de preservação é obrigatório: o compressor não mudou, mas sua linguagem pode ter ficado menos interpretável. Compare erros em números, relações e exceções, além de acerto global. Se o ganho desaparecer, usar texto menos comprimido pode ser melhor que retreinar toda a cadeia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

USO AVANÇADO — Leitor local de manuais
Cenário: Modelo pequeno recebe contexto de servidor.
Estratégia: Aprender seleção de trechos que preservam campos necessários; enviar conteúdo original quando detector indicar domínio desconhecido.
Papel do modelo pequeno: 3–7B lê formato treinado.
Aceite proposto: Qualidade deve atingir mínimo no domínio e degradar de forma detectável fora dele.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

USO AVANÇADO — Fluxo com várias tarefas
Cenário: Mesmo corpus atende perguntas distintas.
Estratégia: Usar compressor geral para descoberta e compressão específica após selecionar objetivo; manter ambos vinculados à origem.
Papel do modelo pequeno: 8–14B decide campos necessários.
Aceite proposto: Não reutilizar representação específica para objetivo incompatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor treinado em representação simples e explícita.
8–14B: Compressor ou leitor especializado em poucas famílias de tarefa.
15–30B: Professor ou avaliador de preservação funcional, sem garantir decodificação universal.
Requisitos de treino/runtime: Dados de treino separados por origem, leitor fixado por versão e avaliação após quantização.
Não aplicar quando: Modelo é fechado sem interface compatível para memória latente ou domínio muda rápido demais.

## T020:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C031 — Microsoft Research / LLMLingua-2
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa formula compressão como classificação de tokens treinada com dados destilados.
Mecanismo documentado: Compressor especializado seleciona texto para um leitor posterior.
Correspondência com esta base: Compressão aprendida explícita.
Transferência proposta para modelo pequeno: Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.
Limite: Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V3A-S001, V4A-S028.

V4A-C023 — IBM / Granite RAG LoRAs experimentais
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Anúncio distingue modelos disponíveis de adaptadores publicados no Granite Experiments.
Mecanismo documentado: Adaptadores para subtarefas como reescrita de consultas e detecção de alucinação.
Correspondência com esta base: Especialização aprendida é relacionada, mas não comprova compressor de prompts.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir especialização de 8B por papel sem ativar o mesmo adaptador em tarefas incompatíveis.
Limite: Experimentos não são implantação; não transferir compatibilidade KV de aLoRA a qualquer LoRA. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q017, V4A-Q024.

## T020:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T020 → T177 [complements]
Como combinar: Adaptar leitura ao formato comprimido.
Interface: Pares original/comprimido e tarefa rotulada.
Condição: Treino autorizado e dados separados.
Aceite proposto: Medir benefício além de simples exposição ao domínio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S001, V3A-S004, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T020 → T037 [complements]
Como combinar: Aplicar compressão condicionada à pergunta quando necessário.
Interface: Consulta, representação e versão do compressor.
Condição: Objetivo da consulta permanecer estável.
Aceite proposto: Trocar pergunta e detectar necessidade de recompressão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S001, V3A-S004, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transportar estados latentes entre arquiteturas apenas pela dimensão.
- Conservar caminho de leitura sem compressão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar pares completos compressor-leitor; ganho isolado do compressor não demonstra qualidade do sistema.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T022, T052, R005

## Fontes primárias associadas

### A-S015 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models

[https://aclanthology.org/2023.emnlp-main.825/](https://aclanthology.org/2023.emnlp-main.825/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão textual com orçamento e seleção iterativa de tokens.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S033 — Learning to Compress Prompts with Gist Tokens

[https://arxiv.org/abs/2304.08467](https://arxiv.org/abs/2304.08467)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações compactas de prompt treinadas com alterações de máscara de atenção.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs

[https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo 8B disponível e adaptadores experimentais por subtarefa RAG; separar disponibilidade e experimento.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
