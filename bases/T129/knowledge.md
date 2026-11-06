# T129 — MTP — Multi-Token Prediction

**Nome canônico:** MTP — Multi-Token Prediction  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T129  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multi-token prediction; predição de múltiplos tokens

## T129:C01 — conceito

Objetivo ou arquitetura que treina o modelo para predizer vários tokens futuros, em vez de apenas o próximo. Algumas implementações usam cabeças auxiliares sobre um tronco compartilhado e podem apoiar especulação na inferência. O treinamento MTP e o algoritmo de aceitação de tokens são componentes distintos.

Como funciona:
- Definir alvos em múltiplas posições futuras durante o treino.
- Otimizar cabeças ou módulos que compartilham parte da representação.
- Na inferência compatível, usar previsões adicionais como candidatos e aplicar verificação apropriada.

## T129:C02 — aplicacao

Quando usar:
- Checkpoint já fornece módulos MTP e runtime suporta sua utilização.
- Pesquisa de treinamento quer comparar eficiência de aprendizagem e geração.

Quando não usar:
- Esperar criar cabeças úteis apenas ligando uma flag em modelo que não as possui.

Implementação proposta:
- Inspecionar configuração e pesos auxiliares disponibilizados com o modelo.
- Comparar modo normal e modo MTP com mesma tarefa e amostragem.
- Registrar política de verificação e limites de número de tokens futuros.

Aplicação LAI proposta:
Proposta LAI: verificar suporte concreto do checkpoint antes de planejar ganho MTP; considerar como atributo na escolha de modelos e runtimes.

## T129:C03 — riscos_validacao

Armadilhas:
- Predizer vários tokens não garante que todos serão aceitos ou produzidos numa única passagem útil.
- Módulos ausentes ou incompatíveis não podem ser substituídos por mera configuração.

Métricas sugeridas:
- Aceitação de cada posição futura e custo incremental do módulo.
- Qualidade de tarefa, latência final e memória adicional.

Testes propostos:
- Desabilitar módulos auxiliares e obter uma referência de geração convencional.
- Forçar baixa concordância e verificar que a implementação não aceita previsões sem o controle exigido.

## T129:C04 — perguntas_proveniencia

Pergunta: MTP e speculative decoding são sinônimos?
Resposta: Não. MTP produz previsões; especulação define como candidatos são usados e verificados.

Pergunta: MTP pode melhorar treinamento?
Resposta: É uma hipótese investigada com resultados em modelos específicos; não garante ganho para todo checkpoint.

Pergunta: MTP exige usar todas as cabeças no serviço?
Resposta: Não necessariamente; o objetivo auxiliar e o uso acelerado na inferência são decisões distintas.

Pergunta: Previsão futura já conhece o token intermediário amostrado?
Resposta: Não por definição. Examine o condicionamento da arquitetura antes de tratá-la como uma cadeia autoregressiva comum.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T129:C05 — mecanismo_avancado

Prever posições futuras com cabeças auxiliares modifica o objetivo de treinamento. Cabeças que partem de uma representação compartilhada não produzem automaticamente a mesma fatoração autoregressiva de gerar um token e condicionar o próximo nele. Usá-las como propostas exige um procedimento de verificação apropriado. Também é possível usar o objetivo apenas como supervisão auxiliar e manter um caminho convencional na implantação.

Condição de contorno:
Um checkpoint treinado somente para próximo token não ganha cabeças úteis apenas por habilitar uma opção de execução.

Contrato proposto:
- Entradas: Arquitetura com cabeças compatíveis, alvos deslocados e política de uso na inferência.
- Saídas: Perdas auxiliares no treino ou propostas verificáveis durante geração.
- Estado: Pesos das cabeças, alinhamento dos alvos e estados compartilhados.
- Invariante: Cada cabeça é supervisionada pela posição futura correta, sem acesso indevido ao alvo.

Compromissos de projeto:
- Supervisão adicional pode mudar representações e exige controlar comparações de treinamento.
- Mais candidatos por passo elevam potencial de amortização e trabalho de verificação.

## T129:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deslocar em uma posição os rótulos de uma cabeça e comparar com a indexação correta. Esperar perda e aceitação anormais; verificar também fronteiras e padding de exemplos.

Plano de avaliação proposto:
Plano proposto: separar experimento de qualidade do treinamento e experimento de velocidade na inferência. Controlar dados, orçamento e arquitetura; medir métricas de tarefa, custo das cabeças e tokens confirmados, evitando atribuir todo ganho ao paralelismo de saída.

Comparações:
- T079 (complements): Cabeças futuras podem fornecer candidatos, mas a regra especulativa determina sua confirmação exata.

Afirmação rastreável:
O trabalho de multi-token prediction treina cabeças independentes sobre um tronco compartilhado para prever vários tokens futuros.
Suporte: direct; fontes: B-S039
Limite: O resultado não implica que previsões simultâneas possam ser publicadas sem verificação preservando a distribuição original.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T129:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou supervisão auxiliar e proposta especulativa. O aprofundamento analisa transferência entre treino e serving, qualidade por distância futura e custo de manter cabeças que podem não ser usadas.

Objetivo e implantação
Um modelo pode ter sido treinado com alvos futuros sem disponibilizar todas as cabeças na exportação. Inspecione artefato e runtime antes de planejar MTP na inferência. Uma descrição do treinamento não comprova que a implantação usa geração de múltiplos tokens por passo ou que o checkpoint público inclui os componentes necessários.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

Distância da previsão
Quanto mais distante o token previsto, maior pode ser a incerteza sem observar as escolhas intermediárias. Meça acerto e aceitação por horizonte, categoria e configuração de amostragem. Uma média agregada pode esconder uma primeira cabeça útil e demais posições que só acrescentam custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

Compartilhamento de computação
Cabeças auxiliares podem reaproveitar representações, mas ainda exigem operações e estado. Quantifique memória e tempo adicionais e confirme se o backend executa de modo eficiente. A alternativa de draft externo possui outro custo e outra flexibilidade; a comparação depende da implementação concreta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

USO AVANÇADO — Escolha de checkpoint
Cenário: Dois modelos semelhantes diferem em suporte MTP.
Estratégia: Compare qualidade do caminho convencional, disponibilidade das cabeças e benefício da verificação. Não escolha só pelo número de tokens que o material promocional diz prever.
Papel do modelo pequeno: Um 15–30B pode ser candidato quando respostas longas tornam a economia relevante.
Aceite proposto: Aceitar pela latência completa, memória e qualidade no mesmo domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

USO AVANÇADO — Pesquisa de treinamento
Cenário: Há controle sobre um modelo especializado.
Estratégia: Adicione objetivos futuros com alinhamento rigoroso e avalie se melhoram representação ou serving. Separe efeito do treinamento do efeito de executar as cabeças na geração.
Papel do modelo pequeno: Um 3–7B pode servir como escala de experimento antes de investimento maior.
Aceite proposto: Ablacionar objetivo auxiliar e modo de inferência em comparações distintas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S039, V4B-S011, V4D-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: O benefício pode estar no treinamento, mesmo sem aceleração em serving; não misturar as conclusões.
8–14B: Use horizonte curto inicialmente e registre retornos decrescentes por posição.
15–30B: Inclua estados auxiliares no orçamento e na transferência entre workers, quando presentes.
Requisitos de treino/runtime: Requer arquitetura e pesos compatíveis, além de verificação apropriada na inferência. Não é um flag que cria cabeças treinadas.
Não aplicar quando: Não emitir previsões independentes como se fossem a mesma fatoração autoregressiva do alvo.

## T129:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C007 — DeepSeek-AI / DeepSeek-V3/R1 — infraestrutura de inferência online
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Autores descrevem a implantação do serviço e publicam perfis associados a configurações de prefill e decode.
Mecanismo documentado: Separação das fases, paralelismo tensorial/especialistas e sobreposição de comunicação com computação.
Correspondência com esta base: MTP faz parte da pesquisa/treino do modelo; a fonte não comprova que a especulação MTP esteja ativa em toda implantação online.
Transferência proposta para modelo pequeno: Proposta: medir sobreposição de comunicação e decisão de particionamento só quando o modelo/carga exigir múltiplos dispositivos; alunos que cabem em uma GPU devem ter esse caminho simples como baseline.
Limite: 671B totais, fora da faixa solicitada. Configurações do artigo e do perfil não são idênticas. Trace simula balanceamento perfeito e não demonstra ganho em 3–30B.
Fontes: V4D-S014, V4D-S015.

V4B-C011 — NVIDIA / TensorRT-LLM
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: A documentação de produto descreve API de serving e runtime Python/PyTorch, com opções de quantização e especulação.
Mecanismo documentado: Integra atenção paginada, in-flight batching, formatos de baixa precisão e proponentes como EAGLE/MTP, conforme suporte de modelo e hardware.
Correspondência com esta base: MTP é recurso documentado para modelos compatíveis.
Transferência proposta para modelo pequeno: Proposta: criar uma matriz de recursos por checkpoint 3–30B, fixar build e testar a combinação mínima antes de habilitar otimizações adicionais.
Limite: É evidência de disponibilidade de produto, não deployment de cliente. Não comprova compatibilidade do servidor do usuário nem exige universalmente o antigo fluxo de engines compiladas.
Fontes: V4B-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T129:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T129 → T079 [feeds]
Como combinar: Cabeças MTP podem produzir candidatos para verificação especulativa.
Interface: Propostas e informações exigidas pelo algoritmo.
Condição: Runtime suporta o checkpoint e a regra de confirmação.
Aceite proposto: Comparar distribuição e medir tokens confirmados por rodada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S039, V4B-S011, V4D-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T129 → T102 [complements]
Como combinar: Separar fases pode exigir transferir estados auxiliares junto ao KV.
Interface: Manifesto de estados por sequência.
Condição: Destino conhece todos os componentes necessários.
Aceite proposto: Testar retomada sem perda ou mistura de cabeças e posições.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S039, V4B-S011, V4D-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar se as cabeças existem no artefato entregue, não somente no paper.
- Separar disponibilidade do recurso em TensorRT-LLM de adoção por um produto específico.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
MTP não permite inferir qualidade geral a partir de quantos tokens são propostos. Compare a resposta do modelo e o custo de produzi-la; melhoria de treinamento e aceleração são hipóteses diferentes.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T128, T132

## Fontes primárias associadas

### B-S039 — Better & Faster Large Language Models via Multi-token Prediction

[https://arxiv.org/abs/2404.19737](https://arxiv.org/abs/2404.19737)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetivo de treino prevê múltiplos tokens com cabeças auxiliares sobre tronco compartilhado.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S011 — NVIDIA TensorRT LLM

[https://developer.nvidia.com/tensorrt-llm](https://developer.nvidia.com/tensorrt-llm)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Runtime Python/PyTorch, cache paginado, batching, quantização e especulação documentados.

Limite: Página de produto demonstra recursos disponíveis, não adoção comprovada por cliente nem compatibilidade do hardware local.

### V4D-S008 — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

[https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesquisa sobre RL de raciocínio e transferência de capacidades a modelos menores.

Limite: Pesquisa e benchmarks, não evidência de implantação de cada variante. Registro atual é v2, revisado em 2026-01-04; comparação histórica não define fronteira de novembro de 2026.

### V4D-S014 — Profiling Data in DeepSeek Infra

[https://github.com/deepseek-ai/profile-data/blob/main/README.md](https://github.com/deepseek-ai/profile-data/blob/main/README.md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descrição de sobreposição computação/comunicação, RDMA e configurações ligadas ao deployment online V3/R1.

Limite: Os traces publicados simulam roteamento MoE perfeitamente balanceado; não são reprodução integral de tráfego real. EP32/EP128 deste perfil e EP32/EP320 do relatório são contextos/revisões diferentes.

### V4D-S015 — DeepSeek-V3 Technical Report — v2

[https://arxiv.org/html/2412.19437v2](https://arxiv.org/html/2412.19437v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seção 3.4 descreve deployment de inferência com prefill/decode separados, TP/EP e redundância de especialistas guiada por carga.

Limite: Modelo de 671B totais, fora de 3–30B. Custos publicados de treino não incluem toda a pesquisa. MTP especulativo avaliado não prova ativação em todo serviço online.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
