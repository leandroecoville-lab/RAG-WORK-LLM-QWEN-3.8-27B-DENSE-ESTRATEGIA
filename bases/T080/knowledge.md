# T080 — Adaptive Speculative Decoding

**Nome canônico:** Adaptive Speculative Decoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T080  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** dynamic speculation lookahead; especulação adaptativa

## T080:C01 — conceito

Ajusta durante a geração quanto trabalho especulativo realizar. Em vez de propor sempre o mesmo número de tokens, um controlador usa confiança do assistente, aceitação recente ou custo observado. É uma família de políticas sobre a especulação, e não uma garantia adicional de exatidão.

Como funciona:
- Observar sinais de facilidade do trecho e resultados das últimas propostas.
- Encerrar ou ampliar o rascunho dentro de limites definidos.
- Submeter todo candidato à mesma verificação exigida pelo método base.

## T080:C02 — aplicacao

Quando usar:
- Tarefas que alternam texto previsível e decisões difíceis.
- Pares assistente/alvo cuja concordância varia muito entre prompts.

Quando não usar:
- Controlador sem telemetria ou com custo superior ao trabalho economizado.

Implementação proposta:
- Começar com comprimento fixo como baseline e registrar tempo do assistente e do alvo.
- Adicionar limite mínimo/máximo e uma regra de ajuste gradual por janela.
- Separar calibração do controlador e avaliação em tarefas novas.

Aplicação LAI proposta:
Proposta LAI: comparar controlador adaptativo e rascunho fixo em tarefas de código, extração e conversa antes de adotar uma política comum.

## T080:C03 — riscos_validacao

Armadilhas:
- Confiança alta do assistente não demonstra que o alvo aceitará o token.
- Reagir a uma única rejeição pode produzir oscilação e piorar a latência de cauda.

Métricas sugeridas:
- Comprimento proposto versus aceito por trecho.
- Tempo líquido economizado e frequência de recuo ao modo convencional.

Testes propostos:
- Alternar entradas repetitivas e imprevisíveis; exigir melhoria média sem ultrapassar o orçamento de cauda.
- Injetar queda de concordância e verificar que o controlador limita rapidamente o desperdício.

## T080:C04 — perguntas_proveniencia

Pergunta: Confiança do assistente pode dispensar o alvo?
Resposta: Não em especulação exata. Ela orienta o tamanho do rascunho, não autoriza aceitar seu conteúdo.

Pergunta: Qual comprimento é ideal?
Resposta: É específico da carga, par de modelos e hardware; deve ser ajustado por ganho líquido medido.

Pergunta: É necessário treinar o assistente novamente?
Resposta: Não para adaptar o horizonte; atualizar pesos online seria uma intervenção distinta, com outros custos e controles.

Pergunta: Qual unidade orienta a decisão?
Resposta: Milissegundos por token confirmado, condicionados à carga, são mais úteis que a fração aceita observada isoladamente.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T080:C05 — mecanismo_avancado

O tamanho do rascunho deve minimizar tempo por token confirmado, e não maximizar isoladamente sua taxa de aceitação. Um controlador pode observar duração das propostas, verificação e quantidade aceita, mantendo limites e suavização para evitar oscilações. Confiança do assistente é apenas um sinal para decidir quanto especular; um assistente confiante também pode discordar sistematicamente do alvo.

Condição de contorno:
Quando a carga muda mais rapidamente que a adaptação, estatísticas antigas podem produzir decisões piores que uma política fixa.

Contrato proposto:
- Entradas: Sinais por iteração, orçamento de latência e limites permitidos para propostas.
- Saídas: Próximo tamanho do rascunho e motivo observável da decisão.
- Estado: Estatísticas móveis por classe de carga e configuração do par de modelos.
- Invariante: A adaptação altera quantidade proposta, mantendo a mesma regra correta de verificação.

Compromissos de projeto:
- Horizontes longos amortizam verificações, mas elevam desperdício após rejeição.
- Controladores muito sensíveis podem reagir ao ruído do escalonador.

## T080:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alternar trechos fáceis e divergentes, injetando atrasos no assistente. Esperar redução do horizonte quando o custo aumenta, sem aceitar tokens pela confiança sozinha.

Plano de avaliação proposto:
Plano proposto: comparar horizonte constante, regra heurística e adaptação, com mesmos modelos e chegadas. Medir latência por token confirmado, variância, custo adicional e tempo de recuperação após mudanças; escolher pela distribuição real de serviço.

Comparações:
- T079 (complements): A política escolhe esforço; o algoritmo de aceitação continua responsável pela exatidão.

Afirmação rastreável:
A implementação documentada pela Hugging Face pode interromper propostas usando a confiança do assistente.
Suporte: direct; fontes: B-S002
Limite: O limiar é uma heurística de execução; não equivale a calibração de correção factual ou concordância garantida.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T080:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou horizonte variável e estabilidade do controlador. Aqui a adaptação considera censura por encerramento, prazo restante e mudança de carga, permitindo aprender uma política sem confundir facilidade do texto com capacidade disponível do servidor.

Sinais que não enviesam a decisão
Uma sequência encerrada por EOS não fornece a mesma observação que um rascunho rejeitado. Marque passos censurados por término, cancelamento ou limite. Mantenha histogramas por posição proposta e classe de tarefa, pois a média global pode esconder aceitação alta no primeiro token e quase nula no restante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

Controle em dois tempos
Use uma política rápida para escolher o próximo horizonte a partir do prefixo recente e uma política lenta para ajustar limites conforme fila e memória. A rápida não deve aumentar candidatos quando a lenta identifica saturação. Registre ambas as decisões para distinguir mudança de texto de mudança de capacidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

Aprendizado com exploração limitada
Reserve uma parcela controlada de tráfego elegível para comparar horizontes alternativos. Sem exploração, a política só observa os regimes que ela própria escolheu e pode ficar presa em uma configuração ruim. A exploração deve respeitar prazo, orçamento KV e disponibilidade do caminho convencional, com desligamento imediato se o SLO piorar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

USO AVANÇADO — Saída heterogênea
Cenário: Uma mesma resposta alterna enumerações previsíveis e explicações abertas.
Estratégia: Use segmentos observáveis do formato como sinais auxiliares, sem presumir que JSON sempre é fácil. Reduza o horizonte após divergências consecutivas e recupere lentamente quando tokens confirmados por custo voltarem a crescer.
Papel do modelo pequeno: Alvos pequenos podem beneficiar-se principalmente nos segmentos repetitivos.
Aceite proposto: Aprovar por tempo total e cauda; exigir que adaptação não altere critérios de aceitação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

USO AVANÇADO — Tráfego com rajadas
Cenário: O servidor atende agentes durante picos de requisições.
Estratégia: Imponha limite global de trabalho especulativo. Ao crescer a fila, compare horizonte menor e desligamento temporário; reative com histerese quando a pressão cair. Não use um limiar único de confiança para todos os modelos.
Papel do modelo pequeno: Um 8–30B pode compartilhar GPU com outros trabalhos; a política preserva capacidade útil.
Aceite proposto: Medir tempo de recuperação após rajada, preempções e latência dos pedidos que não especulam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S002, V3B-S001, V4B-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, exigir evidência de que a própria instrumentação e decisão custam menos que a economia obtida.
8–14B: Em 8–14B, perfilar transições entre formatos e idiomas para evitar uma política dominada pelo tráfego mais frequente.
15–30B: Em 15–30B, controlar horizonte conjuntamente com reserva KV e trabalho de verificação concorrente.
Requisitos de treino/runtime: A adaptação é runtime; confiança do proponente precisa ser acessível e qualquer aprendizado de política exige dados separados.
Não aplicar quando: Não aplicar política treinada em baixa carga diretamente à saturação, nem interpretar EOS como rejeição.

## T080:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T080:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T080 → T079 [requires]
Como combinar: Adaptar apenas a quantidade proposta, preservando o algoritmo de verificação do mecanismo base.
Interface: Horizonte escolhido, candidatos e máscara de posições válidas.
Condição: A proposta variável é suportada pelo backend.
Aceite proposto: Testar todos os horizontes contra o mesmo alvo convencional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S002, V3B-S001, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T080 → T121 [complements]
Como combinar: Combinar orçamento especulativo com admissão por GPU para proteger requisições já ativas.
Interface: Fila, prazo restante, bytes KV e custo por passo.
Condição: O scheduler informa pressão em tempo útil.
Aceite proposto: Reproduzir rajadas e verificar ausência de oscilação persistente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S002, V3B-S001, V4B-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Versionar política e manter histórico das decisões para detectar drift.
- Separar observações censuradas e impor um horizonte máximo verificável.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O experimento com fronteira deve comparar custo por resposta correta em diferentes níveis de carga. Adaptar horizonte melhora utilização quando funciona; não transforma um modelo menor em especialista mais competente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T145, T146

## Fontes primárias associadas

### B-S002 — Faster Assisted Generation with Dynamic Speculation

[https://huggingface.co/blog/dynamic_speculation_lookahead](https://huggingface.co/blog/dynamic_speculation_lookahead)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comprimento adaptativo do rascunho e interrupção por confiança do modelo assistente.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S001 — Fast Inference from Transformers via Speculative Decoding

[https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Algoritmo de aceitação, distribuição residual e análise idealizada de custo.

Limite: Texto do algoritmo e análise consultados; resultados experimentais não reproduzidos; pressupostos de paralelismo não certificam servidor local.

### V4B-S014 — Continuous batching — Transformers

[https://huggingface.co/docs/transformers/en/continuous_batching](https://huggingface.co/docs/transformers/en/continuous_batching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: ContinuousBatchingManager, generate_batch, configuração separada de geração e scheduling, cache paginado e recursos de serving.

Limite: Documentação dinâmica; exemplos não são implantação de cliente. Verificar versão instalada e suporte arquitetural.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
