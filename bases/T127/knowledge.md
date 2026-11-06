# T127 — GGUF — formato de modelos, não método único de quantização

**Nome canônico:** GGUF — contêiner binário de modelos  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** format  
**Estado da evidência:** Correção terminológica do inventário original  
**ID canônico:** T127  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** GGUF / formatos de quantização; GGUF; formato GGUF; GGUF não é algoritmo de quantização

## T127:C01 — conceito

GGUF é um formato binário para armazenar modelos destinados à inferência em executores compatíveis com GGML. Reúne tensores e metadados e pode conter diferentes tipos numéricos, inclusive representações não quantizadas. A extensão do arquivo identifica o contêiner; não identifica sozinha um único método de quantização, sua qualidade ou a velocidade de execução.

Como funciona:
- Converter arquitetura, nomes e formas dos tensores e metadados necessários para o formato aceito pelo executor.
- Registrar tipos de tensor e informações como tokenizer e configuração do modelo.
- Carregar os dados com suporte aos tipos numéricos e à arquitetura presentes no arquivo.

## T127:C02 — aplicacao

Quando usar:
- Distribuição e execução local em ambientes compatíveis, especialmente quando carregamento, metadados e opções de representação precisam acompanhar o artefato.

Quando não usar:
- Como garantia de que qualquer modelo será aceito ou que todos os tensores usam a mesma precisão.

Implementação proposta:
- Proposta: registrar checkpoint de origem, revisão, conversor, versão do executor e hash do GGUF produzido.
- Inspecionar tipos por tensor e metadados; distinguir tamanho do arquivo, memória residente e memória de contexto durante geração.
- Comparar uma versão de referência e uma quantizada no mesmo conjunto de tarefas, com tokenizer e chat template corretos.
- Verificar suporte da combinação arquitetura/tipo/backend antes de decidir a distribuição; manter o artefato de referência para reproduzir diferenças.

Aplicação LAI proposta:
Proposta LAI: tratar cada GGUF como artefato versionado de modelo, com rastreabilidade e avaliação próprias, sem declarar que a mera conversão produziu compressão ou melhoria.

## T127:C03 — riscos_validacao

Armadilhas:
- Usar o nome comercial de uma quantização como se descrevesse integralmente todos os tensores.
- Atribuir erros de template ou tokenizer à quantização, sem isolar a causa.

Métricas sugeridas:
- Tamanho em disco, tempo de carga, memória de execução, throughput e diferença de qualidade frente à referência.

Testes propostos:
- Teste proposto: conferir magic/header e metadados com ferramenta compatível; carregar no executor de destino e gerar com entradas conhecidas.
- Testar texto multilíngue, tokens especiais e contexto longo, separando incompatibilidade de arquivo de degradação numérica.

## T127:C04 — perguntas_proveniencia

Pergunta: Todo arquivo GGUF é quantizado em quatro bits?
Resposta: Não. GGUF admite múltiplas representações e pode armazenar tensores sem quantização de quatro bits.

Pergunta: Dois GGUF do mesmo modelo têm desempenho equivalente?
Resposta: Não necessariamente. Tipos de tensor, conversão, template, revisão e kernels do executor podem mudar memória, velocidade e qualidade.

Pergunta: Extensão .gguf prova que foi quantizado?
Resposta: Não. É necessário inspecionar os tipos dos tensores e o histórico de conversão.

Pergunta: Um hash correto prova conversão correta?
Resposta: Prova integridade do arquivo identificado, não que pesos, tokenizer e metadados correspondam semanticamente ao modelo pretendido.

Escopo das fontes:
A especificação oficial sustenta formato e metadados. O protocolo de comparação e a aplicação são propostas editoriais.

## T127:C05 — mecanismo_avancado

O contêiner precisa preservar mais que valores numéricos: nomes, dimensões, tipos, offsets e metadados da arquitetura determinam como os bytes viram operações. Na especificação GGUF, offsets de tensores são relativos à região de dados e obedecem ao alinhamento declarado. Interpretar o offset como relativo ao começo do arquivo é um erro de leitura, mesmo quando o cabeçalho parece válido.

Condição de contorno:
Um arquivo estruturalmente válido pode representar arquitetura, tokenizer ou tipo de tensor que o executor não suporta.

Contrato proposto:
- Entradas: Arquivo, versão de estrutura reconhecida, descritores de tensor e capacidades do leitor.
- Saídas: Inventário validado e modelo carregado com interpretação explícita dos metadados.
- Estado: Mapa de regiões, alinhamento, tokenizer e tipos por tensor.
- Invariante: Nenhuma dimensão, offset ou tamanho leva a leitura fora da região válida.

Compromissos de projeto:
- Metadados autocontidos facilitam transporte e exigem compatibilidade semântica do leitor.
- Tipos mistos podem melhorar qualidade e tornam inadequada uma única estimativa de bits por parâmetro.

## T127:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar alinhamento, truncar dados e deslocar um offset mantendo o cabeçalho legível. Esperar rejeição estrutural antes da inferência; testar tokenizer incompatível em etapa separada.

Plano de avaliação proposto:
Plano proposto: validar integridade e formas, depois comparar tokenização e logits com o artefato de origem sob transformação documentada. Medir tamanho por tipo de tensor e desempenho no executor real; distinguir erro de conversão de erro de quantização.

Comparações:
- T124 (distinct_from): W4A16 descreve uma escolha numérica; GGUF organiza dados e metadados de diversas representações.

Afirmação rastreável:
A especificação GGUF define alinhamento global e offsets relativos ao início da região de dados dos tensores.
Suporte: direct; fontes: B-S037
Limite: O formato não certifica qualidade, compatibilidade universal ou um método único de quantização.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T127:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou estrutura e offsets do contêiner. A nova camada aborda proveniência do artefato, paridade de tokenização e controle de mudanças entre conversão, quantização e carregamento.

Manifesto de origem
Um arquivo válido pode conter pesos de origem diferente da esperada. Associe hash, checkpoint base, licença aplicável, ferramenta de conversão e política de quantização. A inspeção do cabeçalho verifica estrutura; não prova autoria, qualidade nem correspondência com uma versão anunciada pelo nome do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

Template como parte do comportamento
Tokenizer, tokens especiais e template de chat afetam a entrada efetivamente vista pelo modelo. Compare sequências de token IDs produzidas no caminho original e no consumidor GGUF. Uma migração pode parecer perda de quantização quando o erro real é duplicação de marcadores, papel de mensagens ou encerramento incorreto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

Compatibilidade evolutiva
Uma versão do contêiner e um tipo de tensor reconhecidos não garantem suporte à arquitetura inteira. Verifique tipos de camada, posições e recursos exigidos pelo checkpoint. O carregador deve rejeitar uma interpretação desconhecida em vez de assumir defaults que produzem respostas plausíveis e incorretas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

USO AVANÇADO — Pacote local reproduzível
Cenário: Um modelo será distribuído para execução offline.
Estratégia: Entregue manifesto, configuração de chat, exemplos mínimos e verificações de integridade. Valide o carregamento no build escolhido e meça memória com contexto real.
Papel do modelo pequeno: Um 3–7B pode oferecer extração ou classificação local com contratos explícitos.
Aceite proposto: Reproduzir tokenização e respostas de controle sem depender do nome comercial do arquivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

USO AVANÇADO — Comparação de quantizações
Cenário: Vários arquivos GGUF representam o mesmo checkpoint.
Estratégia: Inspecione tipos por tensor e metadados antes de comparar. Fixe runtime, template e geração; diferencie ganho do método de ganho do backend.
Papel do modelo pequeno: Um 8–14B pode ser selecionado conforme orçamento de RAM/VRAM e qualidade medida.
Aceite proposto: Relatar tamanho, memória em execução e erros por categoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S037, V3D-S012.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Boa faixa para prototipação local, sujeita ao suporte da arquitetura e ao contexto desejado.
8–14B: CPU/GPU offload e precisão mista precisam de medição no dispositivo real.
15–30B: Arquivos de 15–30B podem caber em armazenamento sem caber no orçamento de execução; incluir KV e buffers.
Requisitos de treino/runtime: GGUF é contêiner, não método único. Conversão de formato e quantização são operações distintas.
Não aplicar quando: Não interpretar extensão .gguf como prova de compatibilidade, segurança ou ausência de perda numérica.

## T127:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C024 — Projeto llama.cpp / llama.cpp server
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: O repositório documenta servidor utilizável e carregamento de modelos GGUF, com recursos de geração e configuração de execução.
Mecanismo documentado: Runtime lê metadados e tensores GGUF e expõe geração por servidor; suporte depende da arquitetura, quantização e build.
Correspondência com esta base: GGUF é o contêiner consumido.
Transferência proposta para modelo pequeno: Proposta: começar por um modelo 3–7B conhecido, validar template e respostas, depois medir uso de CPU/GPU e memória sob carga.
Limite: README comprova recurso, não cliente de produção. Não confirma compatibilidade do checkpoint ou hardware local; GGUF não designa um único algoritmo de quantização.
Fontes: V3D-S012, B-S037.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de uso de llama.cpp/GGUF consultada. A documentação comprova recursos; não foi confirmado nesta pesquisa um caso específico novo de implantação de bigtech para cada método de quantização.
Consultas registradas: V4B-Q026.

## T127:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T127 → R024 [requires]
Como combinar: llama.cpp é um consumidor relevante de GGUF, com suporte específico por build.
Interface: Arquivo, arquitetura e parâmetros de carregamento.
Condição: Leitor reconhece todos os componentes usados.
Aceite proposto: Executar validação de carregamento e tokenização.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S037, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T127 → T124 [complements]
Como combinar: Alguns tensores podem usar quatro bits, mas o formato permite várias políticas.
Interface: Tipos por tensor e metadados de quantização.
Condição: Comparação identifica a receita concreta.
Aceite proposto: Medir qualidade e memória, sem chamar todo GGUF de W4A16.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S037, V3D-S012. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar hashes antes de carregar artefatos transferidos.
- Não ocultar perda de tokenizer ou template sob uma comparação genérica de modelos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a solução local completa com fronteira numa tarefa delimitada. Um formato portátil facilita entrega; não demonstra competência nem torna quantizações diferentes equivalentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T124, T125, P009

## Fontes primárias associadas

### B-S037 — GGUF specification

[https://github.com/ggml-org/ggml/blob/master/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formato binário de modelos, tensores e metadados; não é por si só um algoritmo de quantização.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3D-S012 — llama.cpp HTTP server — README

[https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Servidor com caminhos CPU/GPU, geração paralela e batching contínuo.

Limite: Arquivo master; recursos dependem do build, backend e arquitetura do modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
