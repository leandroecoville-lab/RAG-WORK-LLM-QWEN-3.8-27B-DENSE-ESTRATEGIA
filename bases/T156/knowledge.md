# T156 — Temperature Tuning

**Nome canônico:** Temperature Tuning  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T156  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ajuste de temperatura

## T156:C01 — conceito

Ajuste da temperatura de amostragem para controlar quão concentrada fica a distribuição usada na escolha de tokens. Temperaturas menores tendem a concentrar escolhas; maiores favorecem diversidade. Isso não corresponde a um controle direto de factualidade, criatividade útil ou inteligência.

Como funciona:
- Aplicar escala aos logits antes da amostragem, conforme o backend.
- Combinar temperatura com outros parâmetros, como top-p, de forma explícita.
- Avaliar o resultado da tarefa e a diversidade, não apenas variação textual.

## T156:C02 — aplicacao

Quando usar:
- Geração de candidatos para seleção posterior.
- Extração ou classificação que requer estabilidade de formato e decisão.

Quando não usar:
- Tentar corrigir conhecimento incorreto exclusivamente reduzindo temperatura.

Implementação proposta:
- Testar poucos valores compatíveis com o endpoint e manter demais parâmetros fixos.
- Registrar versão de modelo e seed quando suportada.
- Escolher configuração por tarefa com critério de qualidade, não por preferência abstrata.

Aplicação LAI proposta:
Proposta: perfis de amostragem da Helena serem definidos por avaliação de extração, planejamento e geração de alternativas.

## T156:C03 — riscos_validacao

Armadilhas:
- Temperatura zero não garante reprodução exata em toda infraestrutura.
- Misturar alterações de temperatura, top-p e prompt impede atribuir causa ao ganho.

Métricas sugeridas:
- Acerto médio e variância em repetições.
- Diversidade de soluções válidas e custo por candidato aceito.

Testes propostos:
- Repetir mesmas entradas com configurações controladas e comparar resultados.
- Confirmar que valor não suportado gera erro explícito em vez de ajuste silencioso.

## T156:C04 — perguntas_proveniencia

Pergunta: Temperatura baixa elimina alucinação?
Resposta: Não. Pode repetir com maior estabilidade uma resposta errada.

Pergunta: Temperatura de calibração é a mesma coisa?
Resposta: Não. Calibração ajusta probabilidades de confiança; amostragem escolhe tokens.

Pergunta: Temperatura zero produz verdade?
Resposta: Não. Ela tende a escolher o candidato dominante; se a distribuição favorece um erro, esse erro pode se repetir.

Pergunta: Por que variar também top-p atrapalha o teste?
Resposta: Porque muda o conjunto de tokens elegíveis, impedindo atribuir o efeito observado somente à temperatura.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T156:C05 — mecanismo_avancado

Para logits zᵢ e temperatura T positiva, a amostragem pode usar pᵢ(T)=exp(zᵢ/T)/Σⱼexp(zⱼ/T), antes ou em composição com outros filtros. Diminuir T amplia diferenças relativas, mas não corrige a ordenação de candidatos que o modelo já calculou incorretamente. O limite T→0 concentra massa nos maiores logits; um backend pode oferecer modo guloso em vez de aceitar divisão numérica por zero.

Condição de contorno:
Quando filtros, penalidades ou implementação mudam, o mesmo valor de temperatura não descreve sozinho a distribuição final.

Contrato proposto:
- Entradas: Logits, temperatura, demais filtros e configuração de amostragem.
- Saídas: Token amostrado ou escolha gulosa, com configuração identificada.
- Estado: Seed quando suportada, sequência anterior e versão do backend.
- Invariante: Comparações de temperatura mantêm iguais os demais fatores de geração.

Compromissos de projeto:
- Concentração reduz diversidade e pode repetir consistentemente um erro dominante.
- Diversidade amplia exploração e aumenta o trabalho para selecionar respostas corretas.

## T156:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar um caso em que a alternativa mais provável é errada; comparar múltiplas amostras sem assumir que temperatura baixa melhora factualidade.

Plano de avaliação proposto:
Comparar temperaturas com várias repetições, controlando modelo, prompt, top-p e limite de saída. Medir correção, diversidade útil e custo do verificador. Escolher por tarefa, reportando variabilidade; uma seed isolada não sustenta conclusão geral.

Comparações:
- T146 (complements): Diversidade de amostragem pode compor a largura da busca sob orçamento.
- T198 (distinct_from): Concentração dos logits não equivale à calibração de confiança factual.

Afirmação rastreável:
Transformers documenta TemperatureLogitsWarper e sua combinação com filtros top-k e top-p.
Suporte: direct; fontes: V3C-S017
Limite: O contrato exato de temperatura zero e determinismo depende da biblioteca e do modo de geração.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T156:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicava temperatura e diversidade. A expansão trata políticas de amostragem por fase, repetição útil e seleção verificável, evitando usar aleatoriedade para mascarar um problema de contrato.

Exploração e emissão separadas
Use diversidade onde alternativas podem ser avaliadas: hipóteses de causa, estratégias de consulta ou candidatos de patch. Na emissão de argumentos de ferramenta, privilegie o contrato validável. Não altere a temperatura de uma conversa inteira só porque uma das fases exige criatividade; registre a política em cada chamada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018, V3C-S017.

Diversidade efetiva
Múltiplas amostras que diferem apenas em nomes de variáveis não representam explorações independentes. Agrupe candidatos por alteração semântica ou hipótese e contabilize famílias distintas. Quando todos seguem a mesma interpretação errada, forneça evidência nova ou mude a decomposição; aumentar o número de amostras pode apenas multiplicar custo correlacionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S017, V4C-S029.

Configuração completa
Temperatura participa de uma política que também contém top-p, penalidades, limites e modo de raciocínio. A documentação Nemotron diferencia regimes de geração; essa configuração não é um padrão universal. Na migração de backend, valide o comportamento efetivo e confirme se algum parâmetro foi ignorado pelo servidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S018.

USO AVANÇADO — Busca de reparos pequenos
Cenário: Há teste reproduzível que distingue alterações corretas de incorretas.
Estratégia: Gere candidatos diversos em cópias isoladas, deduplique patches equivalentes e rode primeiro o teste que reproduz o defeito. Se todos falharem da mesma forma, interrompa a rodada e solicite observação adicional antes de aumentar diversidade.
Papel do modelo pequeno: 3–7B produz alternativas locais; verificador executável escolhe elegíveis.
Aceite proposto: Proposta: medir taxa de solução por família de candidatos e custo até o primeiro patch aceito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V3C-S017.

USO AVANÇADO — Extração com ambiguidades
Cenário: Documento permite duas interpretações de um campo.
Estratégia: Faça uma primeira extração com política estável. Quando validação de domínio detectar ambiguidade, peça candidatos estruturados apoiados em trechos, em vez de reamostrar silenciosamente até surgir valor conveniente. Preserve a possibilidade de não resolver o campo.
Papel do modelo pequeno: 8–14B gera interpretações; 15–30B confronta evidência conflitante.
Aceite proposto: Proposta: erro factual, abstenção apropriada e estabilidade entre repetições.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Amostras curtas em domínio estreito, com parser e teste externos.
8–14B: Explorar estratégias de consulta e pequenas interpretações alternativas sem substituir evidência.
15–30B: Comparar candidatos de maior alcance mantendo orçamento e verificador independente.
Requisitos de treino/runtime: Registrar política inteira, versão de pesos, runtime e seed quando suportada; usar várias repetições.
Não aplicar quando: Não usar diversidade como substituto de dado ausente nem voto de modelos como prova de verdade.

## T156:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C019 — NVIDIA / Nemotron Nano 9B v2 e integração RAG
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A NVIDIA publica modelo 9B e documentação de integração com controles de reasoning e ferramentas.
Mecanismo documentado: O orçamento de thinking tem semântica própria de término e pode ultrapassar o limiar antes do corte; template e parser fazem parte do contrato de serving.
Correspondência com esta base: A model card distingue configurações de amostragem por modo.
Transferência proposta para modelo pequeno: Proposta: avaliar uma matriz de tarefas e orçamentos no checkpoint e servidor exatos; reservar saída final e checar ferramentas antes de adotar modo com menos esforço.
Limite: Operational_product: recurso publicado, não caso de cliente em produção. 9B não demonstra limites universais das bandas; não foram usados os comandos nem reproduzidos benchmarks.
Fontes: V4C-S018, V4C-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Nemotron documenta parâmetros por regime; OpenAI relata seleção entre candidatos. Não foi encontrado ensaio operacional que determine temperatura universal por faixa de parâmetros.
Consultas registradas: V4C-Q014, V4C-Q027.

## T156:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T156 → T146 [complements]
Como combinar: Dedicar largura de busca a famílias diferentes de hipótese, usando amostragem como uma das fontes de variedade.
Interface: Identidade do candidato, política e grupo semântico.
Condição: Existe avaliador capaz de comparar resultados.
Aceite proposto: Ganho por candidato útil, incluindo custo dos descartados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T156 → T200 [complements]
Como combinar: Enviar candidatos ao verificador antes de selecionar uma resposta definitiva.
Interface: Artefato imutável, resultado de teste e motivo da rejeição.
Condição: Critério independente da preferência textual do gerador.
Aceite proposto: Rejeitar candidato eloquente que falha o requisito objetivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Baixa temperatura pode reproduzir deterministicamente o erro dominante.
- Votar entre amostras correlacionadas não gera confiança calibrada; reportar desacordo e origem das alternativas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare custo por solução validada, controlando quantas amostras o modelo de fronteira recebe. Um pequeno modelo com muitas tentativas não deve ser comparado a uma única tentativa sem explicitar orçamento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T188, T198

## Fontes primárias associadas

### C-S021 — sampling_params — vLLM

[https://docs.vllm.ai/en/latest/api/vllm/sampling_params/](https://docs.vllm.ai/en/latest/api/vllm/sampling_params/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Parâmetros de amostragem incluem temperatura e limites de saída; compatibilidade deve ser conferida na versão instalada.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S017 — Transformers — Utilities for generation

[https://huggingface.co/docs/transformers/internal/generation_utils](https://huggingface.co/docs/transformers/internal/generation_utils)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TemperatureLogitsWarper e filtros top-k/top-p transformam logits e distribuição de amostragem.

Limite: Parâmetros e ordem de aplicação variam por backend; não garantem factualidade ou determinismo entre ambientes.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S019 — Enable Reasoning for NVIDIA RAG Blueprint

[https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html](https://docs.nvidia.com/rag/latest/enable-nemotron-thinking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controles de reasoning diferentes por família e integração de limites de esforço no blueprint.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
