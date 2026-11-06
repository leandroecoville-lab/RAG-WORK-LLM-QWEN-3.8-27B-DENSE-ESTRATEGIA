# R024 — llama.cpp

**Nome canônico:** llama.cpp — inferência em C/C++  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R024  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** llama-server; llama CLI; ggml-org/llama.cpp

## R024:C01 — conceito

llama.cpp é um projeto de inferência em C/C++ para modelos suportados, com execução em CPU e diferentes backends de GPU. Seu ecossistema usa arquivos GGUF e oferece interface de linha de comando e servidor HTTP. Formato de arquivo, método de quantização e motor de execução são escolhas relacionadas, mas representam funções distintas.

Como funciona:
- O runtime carrega pesos e metadados do modelo e executa kernels disponíveis no backend compilado.
- Configurações de precisão, camadas em GPU, contexto e batching afetam memória, latência e capacidade.
- O servidor documenta rotas compatíveis com APIs conhecidas, incluindo geração; isso exige validar o contrato utilizado pela aplicação.

Nota de nomenclatura: Documentação do repositório oficial consultada, sem compilação ou benchmark local. Não afirma compatibilidade do Qwen ou da GPU instalada do usuário.

## R024:C02 — aplicacao

Quando usar:
- Inferência local com modelos compatíveis e necessidade de explorar CPU, GPU ou combinação das duas.
- Comparação de artefatos GGUF quantizados sob restrições reais de memória e carga.

Quando não usar:
- Quando a arquitetura, modalidade ou função necessária não está implementada na revisão escolhida.

Implementação proposta:
- Proposta: fixar revisão do projeto, opções de compilação e backend; registrar identidade e hash dos arquivos do modelo.
- Confirmar arquitetura, tokenizer, template e precisão dos tensores; distinguir conversão de formato de quantização.
- Executar uma configuração mínima e aumentar contexto e concorrência gradualmente, acompanhando memória e qualidade antes de servir a carga.

Aplicação LAI proposta:
Proposta LAI: avaliar llama.cpp como candidato de inferência local para artefatos compatíveis, comparando custo e qualidade com o motor já utilizado.

## R024:C03 — riscos_validacao

Armadilhas:
- Um arquivo GGUF não garante que todo backend suporta sua arquitetura e todas as operações necessárias.
- Offload parcial pode reduzir pressão de VRAM com custo de transferência; throughput e latência precisam ser medidos na carga real.

Métricas sugeridas:
- Memória RAM e VRAM, tempo de prefill, geração por token, qualidade e latência sob concorrência.

Testes propostos:
- Proposta: comparar respostas de avaliação com uma referência do mesmo checkpoint e registrar perdas por quantização.
- Testar no cliente os campos usados, streaming, parada e erro de contexto; conferir que o modelo servido é o solicitado.

## R024:C04 — perguntas_proveniencia

Pergunta: GGUF significa automaticamente modelo de quatro bits?
Resposta: Não. GGUF é um formato que pode armazenar diferentes tipos de tensores; a quantização precisa ser identificada separadamente.

Pergunta: API compatível dispensa teste de integração?
Resposta: Não. Recursos, campos e detalhes de execução variam; o contrato efetivamente usado pela aplicação deve ser verificado.

Pergunta: GGUF identifica a qualidade de uma quantização?
Resposta: Não. É preciso conhecer esquema, modelo de origem e avaliação da variante concreta.

Pergunta: Devo medir apenas tokens por segundo?
Resposta: Não. Inclua prefill, latência de cauda, memória e proporção de respostas aceitas no uso real.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R024:C05 — mecanismo_avancado

llama.cpp inclui um servidor que pode executar modelos compatíveis em CPU e GPU, com diferentes precisões e caminhos de offload. O arquivo GGUF transporta tensores e metadados, porém o formato por si só não assegura que uma arquitetura ou template seja suportado pelo build utilizado. Uma execução reproduzível precisa identificar commit ou versão, hash do modelo, quantização, contexto, distribuição CPU/GPU e parâmetros de concorrência.

Condição de contorno:
Resultados de uma máquina com offload parcial não podem ser extrapolados para outra com pesos inteiramente na GPU; largura de banda, memória e comprimento alteram o gargalo.

Contrato proposto:
- Entradas: Build fixado, GGUF identificado por hash, template de chat, limites de contexto, configuração de offload e requisição.
- Saídas: Texto ou stream, motivo de parada, estatísticas do servidor e uso observado de CPU, GPU e memória.
- Estado: Slots de geração, KV por sequência, modelo carregado e configuração efetiva de batching.
- Invariante: Um slot reutilizado deve preservar apenas estado compatível e autorizado; trocar modelo ou template invalida suposições de equivalência.

Compromissos de projeto:
- Execução local amplia opções de hardware, mas throughput depende fortemente da combinação de pesos e memória.
- Mais paralelismo pode amortizar trabalho ou ampliar disputa por KV; o efeito deve ser medido sob carga.

## R024:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: cancelar uma geração, reutilizar capacidade para outra sessão e verificar ausência de mistura de saída. Repetir com arquivo GGUF ou template incompatível e exigir falha identificável.

Plano de avaliação proposto:
Comparar configurações no mesmo build e checkpoint. Medir prefill, decode, memória, consumo e qualidade em tarefas fixas, mantendo número de tokens comparável. Registrar se medições incluem carregamento inicial e aquecimento.

Comparações:
- T127 (complements): GGUF é um formato usado pelo ecossistema, não uma técnica única.
- R009 (alternative): O papel de servidor pode ser atendido por runtimes com características diferentes.

Afirmação rastreável:
O servidor llama.cpp documenta execução CPU/GPU, geração paralela e batching contínuo.
Suporte: direct; fontes: V3D-S012
Limite: Suporte depende do build, backend e arquitetura; a documentação não equivale a benchmark local.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R024:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu manifesto de build e slots. Esta camada trata distribuição CPU/GPU, concorrência local e seleção de quantização como decisões conjuntas, sem transformar portabilidade em desempenho presumido.

Execução híbrida real
Offload de camadas ou operações muda onde pesos e temporários residem e pode introduzir transferências. Meça CPU, GPU e memória de sistema, incluindo prefill e decode. Um arquivo que cabe em RAM não garante prazo aceitável, e maior uso da GPU não implica automaticamente melhor tempo completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

Slots e concorrência
Slots representam recursos de geração e estado; aumentar quantidade pode elevar throughput ou dividir recursos demais. Teste mistura de contextos e cancelamentos, garantindo limpeza de estado entre pedidos incompatíveis. A configuração deve preservar limites por usuário e não apenas maximizar ocupação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

Build como artefato
Backends e otimizações dependem do build e do dispositivo. Guarde commit, flags relevantes, bibliotecas e hash do GGUF. Ao atualizar, compare tokenização, templates e resultados antes de medir velocidade, porque uma mudança funcional pode parecer melhoria de desempenho por gerar saídas diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

USO AVANÇADO — Aplicação local offline
Cenário: O domínio permite um modelo pequeno com dados locais.
Estratégia: Escolha GGUF suportado, valide template e configure recursos segundo o dispositivo. Use ferramentas determinísticas para operações críticas e mantenha limites de contexto claros.
Papel do modelo pequeno: Um 3–7B pode atender extração ou reescrita estreita sem pressupor conexão externa.
Aceite proposto: Qualidade e tempo medidos no dispositivo, com memória e energia quando relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

USO AVANÇADO — Servidor de equipe pequena
Cenário: Poucos usuários compartilham um host.
Estratégia: Teste slots, batching e offload com chegadas realistas. Inclua pedidos longos que pressionam KV e observe justiça, não apenas throughput médio.
Papel do modelo pequeno: Um 8–14B pode ser adequado se a memória física e o prazo forem suficientes.
Aceite proposto: Respostas completas sem vazamento de estado ou falhas sob concorrência prevista.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S012, V2B-S020, B-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Portabilidade e implantação simples podem ser úteis, mas qualidade do checkpoint continua central.
8–14B: Compare quantizações e offload mantendo template e geração fixos.
15–30B: 15–30B pode exigir memória de sistema e transferências que dominam latência; medir antes de escolher.
Requisitos de treino/runtime: Runtime C/C++ com modelos e backends suportados. GGUF não garante arquitetura reconhecida pelo build.
Não aplicar quando: Não apresentar README como prova de uso em bigtech nem compatibilidade de todo modelo ou GPU.

## R024:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C024 — Projeto llama.cpp / llama.cpp server
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: O repositório documenta servidor utilizável e carregamento de modelos GGUF, com recursos de geração e configuração de execução.
Mecanismo documentado: Runtime lê metadados e tensores GGUF e expõe geração por servidor; suporte depende da arquitetura, quantização e build.
Correspondência com esta base: Referência ao runtime llama.cpp.
Transferência proposta para modelo pequeno: Proposta: começar por um modelo 3–7B conhecido, validar template e respostas, depois medir uso de CPU/GPU e memória sob carga.
Limite: README comprova recurso, não cliente de produção. Não confirma compatibilidade do checkpoint ou hardware local; GGUF não designa um único algoritmo de quantização.
Fontes: V3D-S012, B-S037.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q026.

## R024:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R024 → T127 [requires]
Como combinar: GGUF fornece tensores e metadados usados pelo runtime.
Interface: Arquivo identificado e capacidades do leitor.
Condição: Arquitetura e tipos de tensor suportados.
Aceite proposto: Inspecionar metadados e comparar tokenização.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S012, V2B-S020, B-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R024 → T087 [complements]
Como combinar: Batching e slots devem ser avaliados como política de concorrência do servidor.
Interface: Pedidos ativos e orçamento de contexto.
Condição: Configuração suporta a carga pretendida.
Aceite proposto: Medir fila, memória e cancelamento efetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S012, V2B-S020, B-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar se a atualização mudou defaults ou template.
- Não confundir tamanho do arquivo com consumo total durante geração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare a solução local com fronteira em tarefas delimitadas e incluindo custo operacional. llama.cpp amplia opções de execução; não assegura paridade cognitiva ou latência por si só.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T086, T088, T121, T127, R009, R022, R023

## Fontes primárias associadas

### V2B-S020 — llama.cpp — LLM inference in C/C++

[https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Motor C/C++, backends CPU/GPU, inferência híbrida e opções de quantização.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V2B-S021 — LLaMA.cpp HTTP Server

[https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Servidor HTTP, batching, rotas compatíveis, opções de modelo e configuração de contexto.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

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
