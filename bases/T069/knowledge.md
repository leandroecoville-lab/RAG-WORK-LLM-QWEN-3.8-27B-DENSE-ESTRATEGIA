# T069 — Consolidação por resumos — anteriormente chamada de “Context Distillation”

**Nome canônico:** Consolidação por resumos  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T069  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Context Distillation como memória resumida; correção de context distillation; destilação não é resumo; memória resumida externa; consolidação textual sem treino

## T069:C01 — conceito

Consolidação por resumos transforma histórico extenso em memória textual menor, persistida fora dos pesos do modelo. O resumo é lido ou recuperado em chamadas futuras e continua sendo uma representação sujeita a perdas. O nome anterior “Context Distillation” é mantido para corrigir a terminologia; T069 tem identidade própria e não redireciona para T179.

Como funciona:
- Selecionar um intervalo de eventos e separar fatos, decisões vigentes, hipóteses e pendências.
- Produzir síntese com referências às evidências originais, preservando datas, responsáveis, negações e condições.
- Publicar nova versão do resumo e manter acesso ao histórico para verificar ou expandir afirmações.

Nota de nomenclatura: T069 não redireciona para T179.

## T069:C02 — aplicacao

Quando usar:
- Continuidade de sessões extensas, memória de projeto e redução de entrada repetida quando o histórico integral permanece consultável.

Quando não usar:
- Como prova literal de contrato, substituto de evidência original ou alegação de que o modelo aprendeu permanentemente.

Implementação proposta:
- Proposta: definir esquema de resumo com objetivo, estado atual, decisões, restrições e trabalho pendente; registrar event_range, source_ids, versão e data de consolidação.
- Gerar a atualização a partir de novas evidências e do resumo anterior, verificando itens alterados contra os originais; evitar cadeias ilimitadas de resumo de resumo.
- Preservar conflitos sem resolvê-los por omissão. Quando uma decisão mudar, registrar substituição e intervalo de vigência.
- Regerar a síntese a partir do histórico em marcos definidos, comparando perdas com um conjunto de fatos críticos conhecido.

Aplicação LAI proposta:
Proposta LAI: manter uma memória de projeto resumida, versionada e recuperável, com links aos eventos e confirmação explícita de que não houve treino de pesos.

## T069:C03 — riscos_validacao

Armadilhas:
- Uma síntese pode converter hipótese em fato, apagar exceções ou perpetuar um erro de versões anteriores.
- Reduzir tokens sem medir preservação factual pode piorar a continuidade apesar do arquivo ficar menor.

Métricas sugeridas:
- Retenção de decisões e restrições, afirmações sem fonte, compressão em tokens e custo para recuperar detalhes omitidos.

Testes propostos:
- Teste proposto: resumir um histórico com decisão revogada, negação e pendência; conferir cada item com seus eventos de origem.
- Perguntar por um detalhe omitido e exigir expansão da fonte, sem reconstrução inventada.

## T069:C04 — perguntas_proveniencia

Pergunta: Qual a diferença operacional entre T069 e T179?
Resposta: T069 escreve e relê memória externa. T179 destila comportamento de contexto para parâmetros por treinamento; os artefatos e a avaliação são diferentes.

Pergunta: O resumo pode substituir definitivamente o histórico?
Resposta: Não como regra geral. A proposta conserva evidência original para auditoria, correção e recuperação de detalhes que a síntese perdeu.

Pergunta: Posso desfazer uma consolidação?
Resposta: Se mantiver originais e versões, pode substituir a síntese e reindexar derivados. Isso não desfaz respostas ou efeitos externos já produzidos.

Pergunta: O resumo precisa ser incluído em toda chamada?
Resposta: Somente quando relevante. Armazená-lo não altera o modelo; sua influência depende de leitura, recuperação ou outro caminho explícito de condicionamento.

Escopo das fontes:
Fontes distinguem sumarização externa e treino paramétrico; implementação e testes são propostos.

## T069:C05 — mecanismo_avancado

A consolidação por resumos mantém o conhecimento em um artefato externo que precisa entrar novamente no contexto para influenciar o modelo. Seu custo reaparece em leitura e atualização. Já a destilação paramétrica usa treinamento para internalizar comportamento condicionado a contexto. Essa distinção muda reversibilidade: editar ou trocar um resumo é uma operação de dados; corrigir comportamento internalizado exige outro processo e não oferece citação automática da origem.

Condição de contorno:
Uma sequência de resumos pode conservar coerência narrativa e perder detalhes raros; a qualidade percebida do texto não mede completude factual.

Contrato proposto:
- Entradas: Histórico delimitado, resumo anterior opcional, alterações recentes e fontes recuperáveis.
- Saídas: Síntese externa versionada com cobertura, fatos candidatos, decisões vigentes e lacunas.
- Estado: Origem dos fatos resumidos, revisões, substituições e critério de reconstrução a partir dos originais.
- Invariante: T069 permanece memória externa; nenhum resumo salvo é apresentado como mudança nos parâmetros do modelo.

Compromissos de projeto:
- Atualizar resumo incrementalmente economiza leitura do histórico e acumula dependência de decisões anteriores de seleção.
- Reconstruir do original reduz essa dependência e custa mais tokens e processamento.

## T069:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um detalhe raro, omiti-lo numa primeira síntese e depois formular uma tarefa que dependa dele. O sistema deve reabrir a origem ou declarar a lacuna, sem inventar o detalhe perdido.

Plano de avaliação proposto:
Avaliação proposta: comparar resumo incremental, recomputação integral e recuperação de trechos com orçamento semelhante. Medir fatos raros, correções, suporte e custo ao longo de ciclos; usar casos novos independentes dos exemplos usados para ajustar o resumidor.

Comparações:
- T179 (distinct_from): Destilação paramétrica altera pesos; este registro continua síntese textual externa lida em chamadas futuras.
- T058 (specializes): Resumir é uma forma de consolidação, enquanto consolidação também pode produzir relações ou procedimentos.

Afirmação rastreável:
Recursively Summarizing Enables Long-Term Dialogue Memory propõe atualizar memória por resumos; Learning by Distilling Context usa fine-tuning para internalizar ganhos do contexto.
Suporte: direct; fontes: V3A-S005, A-S040
Limite: Os trabalhos tratam mecanismos diferentes; o uso informal da palavra distillation não elimina essa diferença.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T069:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 corrigiu o nome para consolidação externa por resumos. Aqui o resumo é uma vista de consulta por finalidade, mantendo separação de T179.

Projeto e decomposição
Produza vistas diferentes para localizar informação, retomar tarefa e explicar decisão. Um único resumo universal tende a misturar detalhes irrelevantes e omitir condições úteis a um consumidor específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

Controle adaptativo
Considere o resumo como projeção reconstruível. Quando a finalidade mudar, gerar nova vista a partir das fontes; não empilhar resumos de finalidades diferentes até perder a ligação com origem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

Validação contrafactual
Compare resumo único e vistas por finalidade. Meça decisões sustentadas, custo de reconstrução e dependência do texto original; nenhum desses processos atualiza pesos do modelo. Unidade de avaliação: vista resumida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

USO AVANÇADO — Retomada de projeto
Cenário: Equipe precisa estado operacional curto.
Estratégia: Gerar vista de pendências e decisões confirmadas, com referências para justificativas. Não incluir hipótese descartada como regra ativa.
Papel do modelo pequeno: 3–7B lê vista operacional.
Aceite proposto: Próxima ação deve respeitar decisão vigente e evidência necessária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

USO AVANÇADO — Consulta histórica
Cenário: Usuário quer entender mudança de posição.
Estratégia: Criar vista cronológica a partir de versões originais, preservando o que era desconhecido em cada etapa.
Papel do modelo pequeno: 15–30B explica evolução.
Aceite proposto: Não reescrever passado usando conclusão atual como se sempre fosse conhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, A-S040, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de resumos estruturados por tarefa e campos.
8–14B: Autor de síntese local com fontes por afirmação.
15–30B: Integrador de vistas históricas ou contraditórias.
Requisitos de treino/runtime: Origens preservadas, finalidade e versão da vista; distilação paramétrica é outro processo, identificado por T179.
Não aplicar quando: Resumo vira única cópia do conhecimento ou é reutilizado para finalidade que exige detalhes omitidos.

## T069:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.
Mecanismo documentado: Aplicação específica de um modelo local para condensar transcrições.
Correspondência com esta base: Resumo de gravação é analogia de artefato externo, sem prova de consolidação de memória de agente.
Transferência proposta para modelo pequeno: Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.
Limite: Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.
Fontes: V4D-S005.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q013, V4A-Q023.

## T069:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T069 → T179 [alternative]
Como combinar: Escolher internalização em pesos somente como projeto distinto.
Interface: Corpus, objetivo e critério de atualização.
Condição: Houver dados e treino apropriados, não mera escrita de resumo.
Aceite proposto: Verificar mudança de pesos antes de chamar processo de destilação paramétrica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, A-S040, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T069 → T072 [requires]
Como combinar: Versionar vista e finalidade junto da origem.
Interface: Resumo, purpose_id, fontes e revisão.
Condição: Dependências permitirem reconstrução.
Aceite proposto: Mudar finalidade e detectar vista incompatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, A-S040, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não afirmar aprendizado paramétrico por ter salvo resumo.
- Não converter hipótese sintetizada em fato confirmado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar utilidade da vista para tarefa específica; resumir externamente melhora acesso, não aumenta por si só conhecimento dos pesos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T043, T058, T072, T179, P004

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S040 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fine-tuning para internalizar benefícios de instruções e exemplos antes fornecidos no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S005 — Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

[https://arxiv.org/abs/2308.15022](https://arxiv.org/abs/2308.15022)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização recursiva de memória a partir do resumo anterior e novos diálogos, sem equivaler a mudança dos pesos.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4D-S005 — Pixel December 2023 feature drop

[https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Lançamento de Gemini Nano em Pixel 8 Pro e resumo offline no Recorder.

Limite: Não identifica o checkpoint nem sua contagem de parâmetros. Smart Reply no Gboard era developer preview; não confundir resumo com cadeia hierárquica ou destilação.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
