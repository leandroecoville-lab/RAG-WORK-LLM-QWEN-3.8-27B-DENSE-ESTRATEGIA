# T223 — Constitutional Self-Check

**Nome canônico:** Constitutional Self-Check  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T223  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** principle based self check; checagem por princípios

## T223:C01 — conceito

Checagem de uma proposta contra princípios explícitos antes de concluir uma ação ou resposta. Neste catálogo, é uma adaptação de revisão por princípios durante a inferência. Constitutional AI descreve um método de treinamento mais amplo; executar uma autocrítica com regras não equivale a treinar ou reproduzir esse método.

Como funciona:
- Uma lista curta de princípios é traduzida em perguntas observáveis sobre a proposta.
- O revisor associa cada conclusão a trechos, resultados ou condições verificáveis.
- Uma revisão pode gerar correção, solicitação de evidência ou indicação de conflito ainda não resolvido.

Nota de nomenclatura: Adaptação editorial durante inferência; manter distinção explícita de Constitutional AI como método de treinamento.

## T223:C02 — aplicacao

Quando usar:
- Verificar aderência a especificações, qualidade de citações, requisitos de formato e limites operacionais de uma missão.

Quando não usar:
- Como único controle de permissão ou como certificação automática de segurança e correção do sistema.

Implementação proposta:
- Proposta: selecionar princípios relevantes ao tipo de alteração e definir o que comprova cada um.
- Submeter a proposta e suas evidências ao revisor, mantendo o texto das regras separado dos documentos analisados.
- Exigir resultado estruturado com critério, evidência, falha encontrada e correção sugerida.
- Executar validações determinísticas quando existir uma propriedade verificável por código ou contrato.
- Preservar críticas não resolvidas no encerramento; não repetir a revisão até obter artificialmente uma aprovação.

Aplicação LAI proposta:
Proposta LAI: aplicar revisão por princípios aos entregáveis de cada missão, com critérios pequenos e rastreáveis e validação automática das propriedades que permitirem isso.

## T223:C03 — riscos_validacao

Armadilhas:
- O mesmo modelo pode reproduzir o erro da proposta original.
- Regras vagas incentivam aprovação superficial.
- Uma crítica eloquente pode inventar problemas ou evidências inexistentes.

Métricas sugeridas:
- Falhas reais identificadas; falsos positivos; critérios com evidência; correções confirmadas; custo da revisão.

Testes propostos:
- Apresentar uma proposta que viola um critério explícito e verificar a localização exata do problema.
- Incluir um resultado de teste ausente e exigir reconhecimento da falta de evidência.
- Comparar aprovação do revisor com verificações determinísticas disponíveis.

## T223:C04 — perguntas_proveniencia

Pergunta: Isso é Constitutional AI completo?
Resposta: Não. O uso aqui é uma checagem em execução inspirada em revisão por princípios. A referência original inclui processos de treinamento que não são executados nesta base.

Pergunta: Uma aprovação do modelo autoriza uma operação?
Resposta: Não. Autorizações pertencem ao controle de acesso e às instruções válidas. Uma autochecagem fornece avaliação, não concessão de permissão.

Pergunta: Não encontrar uma violação prova conformidade?
Resposta: Não. Pode refletir cobertura limitada ou critério mal interpretado; o relatório deve explicitar escopo e evidência.

Pergunta: Preciso verificar novamente após uma correção?
Resposta: Sim, nas dimensões afetadas: o artefato mudou e a evidência anterior pode não valer para a nova versão.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T223:C05 — mecanismo_avancado

Uma autochecagem por princípios precisa testar aplicabilidade, evidência e conflito entre regras. Pedir apenas uma nota geral incentiva aprovação superficial. A proposta vincula cada princípio relevante a uma parte concreta do candidato e registra satisfeito, violado ou não determinado. Critério não aplicável não equivale a critério cumprido. Se a revisão altera o artefato, verificações afetadas precisam ser refeitas sobre a nova versão.

Condição de contorno:
Autocrítica pelo mesmo modelo pode reproduzir o erro inicial; concordância interna não substitui uma evidência externa disponível.

Contrato proposto:
- Entradas: Candidato versionado, princípios vigentes e evidências necessárias.
- Saídas: Diagnóstico por princípio, correções propostas e pontos inconclusivos.
- Estado: Versão das regras, aplicabilidade e artefato revisado.
- Invariante: Uma revisão não declara aprovação em dimensões para as quais não possui evidência.

Compromissos de projeto:
- Regras detalhadas tornam revisão mais rastreável e podem conflitar ou ocupar muito contexto.
- Checagem interna é barata relativamente a revisão externa e compartilha vieses do produtor.

## T223:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir dois princípios que exigem interpretação conflitante e um fato impossível de verificar; exigir identificação do conflito e inconclusão factual, sem nota única de aprovação.

Plano de avaliação proposto:
Comparar autochecagem, checklist determinístico e revisão independente em candidatos com violações conhecidas. Medir falsa aprovação, correções que introduzem defeitos e custo. Separar avaliação da proposta da avaliação do artefato já corrigido.

Comparações:
- T200 (complements): Verificação independente testa dimensões que a autochecagem pode interpretar incorretamente.
- T206 (complements): Verificação de processo acompanha se a sequência respeitou critérios definidos.

Afirmação rastreável:
Constitutional AI utiliza princípios em crítica e revisão como parte de um método de treinamento mais amplo.
Suporte: related; fontes: V2A-S020
Limite: A checagem de inferência desta ficha é adaptação editorial e não reproduz o treinamento descrito no paper.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T223:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculava princípios a evidências e estados de avaliação. A expansão trata a autochecagem como revisão limitada, define resposta a conflito e impede confundir crítica em inferência com treinamento constitucional.

Princípio operacionalizável
Traduza cada regra aplicável em uma pergunta verificável sobre o candidato. Exigir preservar a API pode gerar comparação de assinatura e testes; exigir clareza pode precisar de revisão humana ou critérios mais subjetivos. Não atribua a mesma força probatória aos dois tipos. Registre desconhecido quando falta evidência, em vez de aprovação por ausência de objeção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V2A-S020.

Conflito e precedência
Princípios podem entrar em tensão: brevidade versus cobertura, velocidade versus validação. Defina quais são restrições e quais são objetivos de otimização. O revisor não deve inventar precedência para aprovar a própria proposta; conflito material volta ao controlador com alternativas e consequências. Uma constituição longa e contraditória piora a verificabilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S020, V4C-S030.

Crítica muda a evidência
Se a autochecagem altera o artefato, verificações anteriores podem deixar de valer. Vincule o parecer à versão candidata e rerode critérios afetados. Separar gerador e crítico pode reduzir alguns vieses, mas modelos semelhantes ainda podem concordar no mesmo erro; use verificadores externos sempre que houver propriedade executável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S032.

USO AVANÇADO — Resposta técnica com fontes
Cenário: O agente precisa respeitar escopo, evidência e incerteza.
Estratégia: Revise alegações individuais: existe fonte, ela sustenta o detalhe e a limitação foi preservada? Marque inferência separadamente e remova certeza indevida. Não aceitar citação apenas porque o domínio parece confiável; conferir conteúdo quando a alegação importa.
Papel do modelo pequeno: 3–7B faz checklist estreito; 8–14B relaciona alegação e trecho; 15–30B examina conflitos.
Aceite proposto: Proposta: detectar alegações sem suporte e preservar lacunas sem bloquear conclusões sustentadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V3C-S032.

USO AVANÇADO — Patch com invariantes
Cenário: Uma mudança deve manter semântica e evitar adições fora do escopo.
Estratégia: Use revisões por propriedade e combine-as com compilação e testes. Uma violação obrigatória bloqueia o candidato mesmo que a maioria das avaliações seja positiva. Se a propriedade não puder ser provada pelo método, registrar limite e pedir verificação adequada.
Papel do modelo pequeno: 8–14B revisa propriedades locais; 15–30B analisa intenção e efeitos transversais.
Aceite proposto: Proposta: rejeitar violações inseridas e medir falsos negativos de cada critério.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Regras poucas, concretas e ligadas a trechos ou campos explícitos.
8–14B: Revisão de aderência com evidência recuperável e estado desconhecido permitido.
15–30B: Análise de conflitos e síntese de pareceres, mantendo validação externa independente.
Requisitos de treino/runtime: Versão das regras, versão do artefato e testes ligados a requisitos; critérios subjetivos precisam de calibração.
Não aplicar quando: Não tratar autoconcordância como prova formal nem chamar o procedimento de fine-tuning constitucional.

## T223:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: AutoClean documenta revisão por propriedades, não adoção do rótulo Constitucional Self-Check. O componente desta ficha é composição editorial em inferência. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q006, V4C-Q027, V4D-Q023.

## T223:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T223 → T200 [complements]
Como combinar: Encaminhar propriedades objetivas a verificador externo e conservar o parecer textual como evidência de natureza diferente.
Interface: Critério, artefato e resultado observável.
Condição: Verificador não depende apenas da opinião do gerador.
Aceite proposto: Candidato elogiado mas reprovado em requisito objetivo é rejeitado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T223 → T221 [complements]
Como combinar: Usar a versão vigente do objetivo para selecionar princípios aplicáveis à revisão.
Interface: Meta, restrições e critérios de aceite.
Condição: Mudança autorizada atualiza a base da checagem.
Aceite proposto: Não reprovar ou aprovar por regra obsoleta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S032. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Checklist preenchido não comprova que os itens foram verificados.
- Parecer sobre versão anterior não acompanha automaticamente a versão corrigida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare ganho incremental da autochecagem frente a verificação externa e frente a modelo de fronteira. O procedimento pode melhorar aderência, mas continua limitado por capacidade e vieses do crítico.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T185, T224, T217

## Fontes primárias associadas

### V2A-S020 — Constitutional AI: Harmlessness from AI Feedback

[https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Crítica e revisão guiadas por princípios, dentro de um método de treinamento mais amplo.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S022 — Function calling

[https://developers.openai.com/api/docs/guides/function-calling](https://developers.openai.com/api/docs/guides/function-calling)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chamadas de ferramentas com esquema de argumentos, modo estrito e resultados associados.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
