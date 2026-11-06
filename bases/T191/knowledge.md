# T191 — Chain-of-Verification

**Nome canônico:** Chain-of-Verification  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T191  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** CoVe; cadeia de verificação

## T191:C01 — conceito

Método de checagem que parte de uma resposta inicial, formula perguntas de verificação, responde a essas perguntas de forma separada e revisa o texto final. A separação busca reduzir influência do rascunho sobre a checagem. Não garante factualidade quando a verificação depende do mesmo conhecimento incorreto.

Como funciona:
- Produzir rascunho e identificar afirmações que precisam ser verificadas.
- Formular checagens e respondê-las com contexto separado quando apropriado.
- Revisar a resposta de acordo com os resultados e manter lacunas explícitas.

## T191:C02 — aplicacao

Quando usar:
- Respostas factuais compostas por várias alegações.
- Listas e textos em que um erro pontual compromete o conjunto.

Quando não usar:
- Trocar verificação de fonte por uma simples pergunta ao mesmo modelo se ele tem certeza.

Implementação proposta:
- Decompor alegações em itens verificáveis e não apenas frases inteiras.
- Usar fontes externas quando a tarefa depende de fatos atuais.
- Vincular cada correção à pergunta de checagem e à evidência correspondente.

Aplicação LAI proposta:
Proposta: a Helena usar checagens por alegação nos relatórios técnicos e comerciais, preservando fontes e separando inferência de fato.

## T191:C03 — riscos_validacao

Armadilhas:
- Checagens podem confirmar apenas partes fáceis e ignorar a alegação central.
- Rascunho completo nas perguntas pode induzir respostas ancoradas.

Métricas sugeridas:
- Alegações corretas antes e depois da revisão.
- Cobertura de checagem e número de falsos fatos introduzidos na revisão.

Testes propostos:
- Inserir fato falso entre fatos verdadeiros e testar sua identificação.
- Remover fonte essencial e exigir que a conclusão seja rebaixada para inconclusiva.

## T191:C04 — perguntas_proveniencia

Pergunta: CoVe prova uma afirmação só porque fez perguntas?
Resposta: Não. A qualidade depende das respostas de verificação e suas evidências.

Pergunta: Exige outro modelo?
Resposta: Não na formulação básica, embora verificadores distintos possam ser avaliados.

Pergunta: Perguntas neutras garantem verdade?
Resposta: Não. Elas reduzem indução, mas o respondente ainda pode desconhecer o fato ou consultar fonte errada.

Pergunta: Pode retornar só o texto final?
Resposta: Pode, mas preservar internamente o mapa de cobertura permite auditar quais afirmações receberam evidência e quais continuam incertas.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T191:C05 — mecanismo_avancado

Uma pergunta de checagem pode carregar a própria conclusão que deveria verificar. Formular “por que X aconteceu em 2020?” já pressupõe evento e data. Como proposta, transforme afirmações em questões neutras sobre entidades, relações e tempo, preserve um mapa entre alegações e verificações e marque o que não foi coberto. Responder em contextos separados reduz cópia do rascunho, mas não elimina conhecimento compartilhado incorreto.

Condição de contorno:
Alegações omitidas pelo planejador permanecem sem verificação mesmo quando todas as perguntas produzidas foram respondidas.

Contrato proposto:
- Entradas: Rascunho, inventário de alegações, perguntas neutras e fontes quando disponíveis.
- Saídas: Texto revisado e mapa de cada correção ou incerteza.
- Estado: Relações alegação-pergunta-resposta, contextos separados e proveniência.
- Invariante: Nenhuma alegação é declarada verificada apenas por estar perto de outra que foi checada.

Compromissos de projeto:
- Fatorar perguntas reduz interferência e aumenta número de chamadas.
- Adicionar busca amplia evidência e exige avaliar qualidade e atualidade das fontes.

## T191:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir data falsa na formulação de uma pergunta e deixar outra alegação sem pergunta correspondente. Esperar detecção de pressuposição e indicação de cobertura incompleta.

Plano de avaliação proposto:
Plano proposto: comparar checagem conjunta e fatorada com o mesmo rascunho. Medir cobertura, correções válidas, erros introduzidos e custo; avaliar factualidade por referências externas, sem considerar respostas do próprio modelo como certificado suficiente.

Comparações:
- T200 (complements): Independência de contexto ajuda a reduzir contaminação, mas verificação externa acrescenta outra dimensão de independência.

Afirmação rastreável:
Na variante fatorada de CoVe, perguntas são respondidas separadamente sem o rascunho original no contexto de resposta.
Suporte: direct; fontes: C-S044
Limite: O trabalho publicado estudou uso do próprio LLM; integrar fontes externas é uma extensão proposta.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T191:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 propôs perguntas neutras por alegação. A nova camada trata cobertura, evidência contraditória e atualização do texto, distinguindo autoquestionamento de verificação apoiada em fontes externas.

Inventário verificável
Extraia alegações atômicas com entidade, relação, tempo e escopo. Uma frase pode conter várias afirmações e qualificações; checar só o nome principal deixa datas e causalidade sem cobertura. Mantenha ligação entre cada alegação e a versão do rascunho para atualizar o mapa depois de revisões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

Busca que pode refutar
Formule consultas que permitam encontrar contradição e priorize fontes primárias adequadas ao tipo de fato. Preserve resultados conflitantes e data de validade. Pedir ao mesmo modelo que confirme sua frase sem nova evidência pode reduzir alguns erros, mas não constitui independência nem garantia factual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

Revisão com rastreabilidade
Quando uma checagem muda uma alegação, revise trechos dependentes dela, inclusive conclusões. Não substitua uma afirmação precisa por linguagem vaga apenas para escapar do teste. Marque o que continua não verificado e remova conclusões cuja base foi invalidada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

USO AVANÇADO — Relatório factual
Cenário: O modelo produz texto com datas, produtos e capacidades.
Estratégia: Extraia alegações, consulte fontes e reescreva somente depois de consolidar evidência. Priorize fatos que sustentam decisões, sem fingir cobertura integral quando o orçamento é limitado.
Papel do modelo pequeno: Um 3–7B pode estruturar alegações; recuperação e revisão externas sustentam a validade.
Aceite proposto: Medir cobertura de alegações relevantes e taxa de correções válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

USO AVANÇADO — Resposta sobre política formal
Cenário: Há regras documentadas e exceções.
Estratégia: Use perguntas de verificação para localizar fatos e um verificador formal para relações cobertas pela política. Separe erro de tradução, regra ausente e inconsistência.
Papel do modelo pequeno: Um 8–14B pode redigir a explicação, mantendo o alcance da prova explícito.
Aceite proposto: Nenhuma afirmação de verdade além do escopo das fontes ou da política.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S044, V4B-S027, V3B-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Decomposição curta e fontes explícitas reduzem carga de memória; o modelo não deve inventar respostas de checagem.
8–14B: Pode organizar verificações mais complexas, desde que entidades e datas sejam resolvidas.
15–30B: Maior porte não elimina necessidade de fontes atualizadas nem problemas de premissas falsas.
Requisitos de treino/runtime: Workflow em runtime; pesquisa externa e verificadores são complementos distintos do CoVe original.
Não aplicar quando: Não contar perguntas respondidas como fatos verificados sem avaliar evidência e cobertura.

## T191:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q019.

## T191:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T191 → T200 [complements]
Como combinar: Checagem independente reduz dependência do rascunho como fonte.
Interface: Alegações neutras e evidências originais.
Condição: Verificador não recebe conclusão esperada como prova.
Aceite proposto: Testar alegações plausíveis, mas falsas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S044, V4B-S027, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T191 → T197 [complements]
Como combinar: Um schema pode organizar o mapa de alegações e estados de verificação.
Interface: IDs, fonte, status e trecho afetado.
Condição: Validade estrutural não substitui validade da evidência.
Aceite proposto: Detectar alegações sem fonte ou com checagem pendente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S044, V4B-S027, V3B-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar perguntas que pressupõem o fato contestado.
- Rever conclusões dependentes quando uma premissa é corrigida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare fidelidade factual e cobertura com um baseline de fronteira sob acesso equivalente a fontes. O número de etapas de verificação não é uma medida de correção.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T190, T200, T206

## Fontes primárias associadas

### C-S044 — Chain-of-Verification Reduces Hallucination in Large Language Models

[https://arxiv.org/abs/2309.11495](https://arxiv.org/abs/2309.11495)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rascunho, perguntas de checagem, respostas independentes e revisão final compõem CoVe.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
