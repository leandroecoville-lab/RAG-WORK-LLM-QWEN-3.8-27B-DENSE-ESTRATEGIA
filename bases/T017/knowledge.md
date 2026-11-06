# T017 — Context Folding

**Nome canônico:** Context Folding  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T017  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** dobramento de contexto

## T017:C01 — conceito

Fecha trabalho intermediário em representações menores e retorna ao contexto principal. Há trabalhos específicos chamados Context-Folding; um deles usa subtrajetórias branch/return e treinamento FoldGRPO. No runtime, uma versão arquitetural pode preservar somente resultado, evidências e pendências de cada subatividade.

Como funciona:
- Abrir uma subtarefa com contexto focado e limite claro.
- Executar ações locais mantendo o histórico completo fora do contexto principal.
- Retornar síntese contratada e referências, removendo detalhes intermediários da chamada principal.

## T017:C02 — aplicacao

Quando usar:
- Pesquisa ou desenvolvimento com muitas subtarefas delimitáveis.
- Histórico de tentativa e erro que não precisa permanecer ativo após conclusão.

Quando não usar:
- Não dobrar uma subtarefa ainda aberta quando seus detalhes são necessários para resolver dependências.

Implementação proposta:
- Proposta: definir retorno com estado, resultado, evidência e dúvidas.
- Versionar o registro fechado para poder reabri-lo.
- Comparar orquestração simples com modelo treinado para folding sem presumir equivalência entre ambos.

Aplicação LAI proposta:
Proposta LAI: especialistas retornam achados compactos ao decisor; a proposta de runtime não implica que o Qwen já recebeu treinamento FoldGRPO.

## T017:C03 — riscos_validacao

Armadilhas:
- Uma síntese pode ocultar falha ou incerteza da subtarefa.
- Branches isolados podem tomar decisões incompatíveis.

Métricas sugeridas:
- Tamanho do contexto ativo e frequência de reabertura.
- Sucesso em tarefas longas incluindo conflitos entre subtarefas.

Testes propostos:
- Introduzir uma dependência cruzada e verificar se é reportada ao principal.
- Reabrir uma subtarefa após interrupção e recuperar evidências originais.

## T017:C04 — perguntas_proveniencia

Pergunta: Context folding é apenas resumir tudo?
Resposta: Não necessariamente. A divisão e retomada de subtrajetórias também organiza o controle da execução.

Pergunta: Posso reproduzir o paper só adicionando um prompt?
Resposta: Não. Um padrão parecido em software não reproduz automaticamente o treinamento e os resultados publicados.

Pergunta: Uma dobra precisa guardar raciocínio interno completo?
Resposta: Não. O contrato deve preservar estado operacional e evidências úteis, sem presumir acesso ou necessidade de registrar processos internos ocultos do modelo.

Pergunta: Como saber se a decomposição foi boa?
Resposta: Observe integração, reaberturas e dependências que atravessam retornos. Uma redução aparente de contexto pode esconder repetição de trabalho nas subtarefas.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T017:C05 — mecanismo_avancado

O retorno de uma subtrajetória precisa preservar aquilo que o contexto pai ainda deve usar: resultado, premissas, evidências e pendências. Fechar a trajetória não desfaz seus efeitos. Uma dobra útil distingue uma conclusão comprovada de uma tentativa interrompida, e mantém forma de reabrir artefatos quando o resumo não responde a uma dúvida posterior.

Condição de contorno:
O ganho diminui quando subtarefas compartilham dependências extensas ou quando o retorno omite detalhes necessários à integração, causando reabertura frequente.

Contrato proposto:
- Entradas: Objetivo da subtrajetória, contexto mínimo e contrato de retorno.
- Saídas: Resultado compacto com referências e estado de conclusão explícito.
- Estado: Pilha de tarefas, artefatos produzidos e efeitos confirmados ou incertos.
- Invariante: Dobrar contexto não muda o estado real de operações nem converte pendência em conclusão.

Compromissos de projeto:
- Contexto ativo menor reduz leitura repetida, mas transfere responsabilidade para o contrato de retorno.
- Subtrajetórias mais independentes são fáceis de dobrar; decomposição inadequada multiplica coordenação.

## T017:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: encerrar uma subtrajetória após enviar uma operação cuja resposta se perdeu. O retorno deve preservar a incerteza e impedir que o pai repita a operação como se nunca tivesse ocorrido.

Plano de avaliação proposto:
Avaliação proposta: comparar histórico integral, resumos periódicos e branch/return com mesmas tarefas e orçamento. Medir contexto ativo, custo agregado, reaberturas e integração correta; avaliar separadamente política treinada e orquestração manual.

Comparações:
- T237 (complements): Subagentes podem materializar subtarefas, mas folding não exige equivalência entre agente e trajetória.
- T043 (distinct_from): Compactação geral reduz histórico; folding usa fronteiras explícitas de subtarefa e retorno.

Afirmação rastreável:
O trabalho Context Folding combina branch/return com FoldGRPO para aprender gerenciamento de contexto.
Suporte: direct; fontes: V3A-S020
Limite: Aplicar uma dobra manual não reproduz o treinamento nem os resultados experimentais do trabalho.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T017:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu retorno do folding. Aqui a novidade é decidir quais subtarefas merecem contexto isolado e medir a suficiência do retorno.

Projeto e decomposição
Escolha folding quando exploração produz muito material descartável e poucos resultados estáveis. Dependências densas entre subtarefas podem tornar o custo de comunicar estado maior que a economia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

Controle adaptativo
Retorne resultado, evidências e perguntas ainda abertas em canais separados. O chamador pode pedir expansão pontual sem reiniciar toda a exploração nem aceitar conclusão sem base.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

Validação contrafactual
Compare execução monolítica e subcontextos com mesmo limite total de chamadas. Meça trabalho duplicado, suficiência do retorno e necessidade de reabrir exploração. Unidade de avaliação: subtarefa delegada. Inclua subtarefa cujo resultado é correto localmente, mas incompatível com uma restrição do chamador. O contrato deve carregar essa restrição desde a delegação e devolver conflito, não uma solução aparentemente completa. Medir retrabalho por retorno insuficiente ajuda a decidir quando isolamento de contexto compensa a comunicação adicional entre trabalhadores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

USO AVANÇADO — Investigação de componente
Cenário: Um erro pode estar em três módulos.
Estratégia: Abrir subcontexto por hipótese, exigir evidência discriminante e retornar também hipóteses descartadas com motivo.
Papel do modelo pequeno: 3–7B localiza; 8–14B investiga módulo.
Aceite proposto: Líder deve distinguir ausência de evidência de hipótese refutada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

USO AVANÇADO — Pesquisa de alternativas
Cenário: Cada opção tem documentação extensa.
Estratégia: Delegar coleta em esquema comum e comparar somente atributos respaldados; reabrir opção quando critério novo surgir.
Papel do modelo pequeno: 15–30B integra comparações.
Aceite proposto: Nenhuma diferença deve resultar apenas de cobertura desigual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Subtarefa estreita de localização ou extração com retorno fechado.
8–14B: Investigador local capaz de pedir uma expansão adicional.
15–30B: Coordenador de retornos heterogêneos e lacunas entre hipóteses.
Requisitos de treino/runtime: Contrato de retorno, referências duráveis e orçamento por subcontexto; folding aprendido exige treino próprio.
Não aplicar quando: Todos os trabalhadores precisam continuamente do mesmo estado mutável.

## T017:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T017:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T017 → T169 [complements]
Como combinar: Isolar exploração por hipótese e devolver contrato comum.
Interface: Objetivo, limites, resultado e evidências.
Condição: Não houver escrita concorrente irrestrita.
Aceite proposto: Medir duplicação e efeitos de informação omitida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S020, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T017 → T015 [feeds]
Como combinar: Retornar referências para detalhes reabríveis.
Interface: Resultado, artifact_id e seletores.
Condição: Artefato sobreviver ao encerramento do subcontexto.
Aceite proposto: Reabrir suporte após encerrar o trabalhador.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S020, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir isolamento de contexto com isolamento de efeitos.
- Conservar incertezas no retorno condensado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas decomponíveis; dobrar agentes não garante compensar um leitor insuficiente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T004, T043, T169

## Fontes primárias associadas

### A-S037 — Scaling Long-Horizon LLM Agent via Context-Folding

[https://context-folding.github.io/](https://context-folding.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subtrajetórias branch/return e treinamento FoldGRPO para gestão do contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S020 — Scaling Long-Horizon Agent via Context Folding

[https://proceedings.mlr.press/v306/sun26x.html](https://proceedings.mlr.press/v306/sun26x.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Branch de subtrajetória, retorno resumido e treinamento FoldGRPO; não equivalente a simples resumo externo.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
