# T004 — Summarization em cadeia

**Nome canônico:** Summarization em Cadeia  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T004  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** rolling summary; resumo acumulado; Summarization em Cadeia

## T004:C01 — conceito

Mantém um resumo acumulado atualizado por novos blocos de conteúdo. Cada passo usa o resumo anterior e o próximo trecho para produzir a nova versão. É econômico em contexto, mas uma perda ou distorção inicial pode propagar-se nas versões seguintes.

Como funciona:
- Ordenar os blocos e manter os originais acessíveis.
- Atualizar resumo com decisões, fatos e pendências do próximo bloco.
- Associar cada afirmação importante à evidência que a originou.

## T004:C02 — aplicacao

Quando usar:
- Históricos cronológicos de atendimento ou execução.
- Fluxos que recebem novos eventos continuamente.

Quando não usar:
- Evitar como único registro quando são necessárias citações literais ou reconstrução completa.

Implementação proposta:
- Proposta: usar campos estáveis para fatos, decisões, dúvidas e referências.
- Versionar cada resumo e guardar quais blocos foram incorporados.
- Em intervalos definidos, reconstruir a síntese dos originais para medir deriva acumulada.

Aplicação LAI proposta:
Proposta LAI: produzir notas compactas de missão para Helena mantendo decisões e fontes separadas; a síntese serve à navegação, não à autoridade factual.

## T004:C03 — riscos_validacao

Armadilhas:
- Uma hipótese pode virar fato ao ser reescrita repetidamente.
- Eventos recentes podem dominar a síntese e apagar obrigações persistentes.

Métricas sugeridas:
- Retenção de fatos críticos em cada atualização.
- Número de afirmações do resumo sem evidência recuperável.

Testes propostos:
- Injetar uma correção tardia e exigir preservação do histórico da mudança.
- Comparar a décima versão com uma síntese independente dos mesmos originais.

## T004:C04 — perguntas_proveniencia

Pergunta: O resumo anterior é suficiente para auditar?
Resposta: Não. Uma cadeia de resumos pode perder informação; os eventos e documentos originais precisam permanecer disponíveis.

Pergunta: Como evitar que uma correção desapareça?
Resposta: Registrar validade, versão e relação de substituição em campos próprios, além do texto resumido.

Pergunta: Como detectar deriva sem reler tudo?
Resposta: Amostre fatos críticos, verifique referências e compare campos protegidos com sua fonte. Essa auditoria reduz risco, mas não prova ausência de perdas não amostradas.

Pergunta: Um resumo antigo pode ser a única fonte?
Resposta: Pode ser a única representação disponível, mas deve ser marcado como evidência derivada. Sem o original, não é possível confirmar detalhes que ele omitiu.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T004:C05 — mecanismo_avancado

A atualização recorrente s_t=f(s_(t-1),bloco_t) cria dependência de caminho: um fato ausente de s_(t-1) não reaparece sem consulta ao original. Por isso, uma cadeia deve separar resumo narrativo de campos verificáveis, como identificadores e decisões vigentes. Aumentar a fluência da síntese pode esconder degradação factual acumulada em ciclos longos.

Condição de contorno:
Quando a tarefa exige detalhes arbitrários do passado, um resumo de tamanho fixo não oferece garantia de recuperação completa, independentemente da qualidade aparente da prosa.

Contrato proposto:
- Entradas: Resumo anterior versionado, novo bloco e política de preservação.
- Saídas: Nova síntese e referências às evidências incorporadas ou substituídas.
- Estado: Originais recuperáveis, versão do sumarizador e decisões protegidas.
- Invariante: Correções explícitas permanecem distinguíveis das afirmações anteriores que corrigem.

Compromissos de projeto:
- Atualização incremental reduz leitura repetida, mas transmite erros entre ciclos.
- Campos estruturados preservam precisão, porém exigem esquema e manutenção além do texto livre.

## T004:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir um valor, corrigi-lo após vários blocos e continuar resumindo. A memória final deve indicar o valor vigente e permitir verificar a correção sem reconstruí-la por adivinhação.

Plano de avaliação proposto:
Avaliação proposta: comparar resumo recorrente com resumo regenerado dos originais sob orçamento equivalente. Variar número de ciclos e frequência de correções; medir omissões, inversões de negação, atribuição e custo acumulado.

Comparações:
- T008 (alternative): A hierarquia preserva caminhos locais para revisar perdas sem reprocessar toda a cadeia.
- T069 (complements): O resultado textual pode alimentar consolidação persistente sem alterar parâmetros do modelo.

Afirmação rastreável:
O método de memória recursiva combina memória anterior com diálogos subsequentes para produzir a próxima memória.
Suporte: direct; fontes: V3A-S005
Limite: Ganhos experimentais de consistência não equivalem a conservação integral do histórico.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T004:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou deriva acumulada. Aqui resumos são especializados por consumidor e acompanhados de um registro de mudanças de entendimento.

Projeto e decomposição
Produza resumo operacional e resumo explicativo distintos. O primeiro contém próximos passos e restrições; o segundo conserva justificativas. Um consumidor pequeno recebe apenas o primeiro e abre justificativas quando identifica conflito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

Controle adaptativo
Cada atualização declara fatos adicionados, corrigidos e ainda incertos. A cadeia pode assim detectar transformação de hipótese em certeza, mesmo quando o texto final continua fluente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

Validação contrafactual
Compare consumidores recebendo resumo único e duas visões especializadas. Meça decisões corretas e frequência de abertura do original, incluindo custo dessas leituras. Unidade de avaliação: histórico com revisões. Uma prova útil fornece resumo operacional com decisão vigente e resumo explicativo ainda defendendo a decisão anterior. O consumidor deve detectar a revisão incompatível antes de agir. Conte casos de retomada correta, justificativa incoerente e abertura necessária do original; isso avalia a interface entre vistas, não apenas a qualidade individual de cada resumo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

USO AVANÇADO — Passagem entre turnos de operação
Cenário: Equipes retomam trabalho incompleto.
Estratégia: Gerar quadro de pendências e histórico de decisões separadamente; exigir evidência da conclusão antes de retirar pendência.
Papel do modelo pequeno: 3–7B atualiza campos; 8–14B explica desvios.
Aceite proposto: Preservar responsável, prazo e condição de cada pendência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

USO AVANÇADO — Pesquisa com hipóteses concorrentes
Cenário: Novas fontes alteram conclusões.
Estratégia: Manter resumo por hipótese e um quadro de diferenças; somente consolidar após comparar evidências conflitantes.
Papel do modelo pequeno: 15–30B integra argumentos com citações.
Aceite proposto: Não converter falta de evidência em refutação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atualização de campos fechados a partir de observação curta.
8–14B: Produção de resumo operacional com rastreio de alterações.
15–30B: Síntese de justificativas concorrentes, com verificação por fonte.
Requisitos de treino/runtime: Esquema de diferenças e fontes estáveis; exemplos de correções ajudam ajuste supervisionado.
Não aplicar quando: Exatidão literal integral é obrigatória ou a sequência não possui evidências recuperáveis.

## T004:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.
Mecanismo documentado: Aplicação específica de um modelo local para condensar transcrições.
Correspondência com esta base: Há sumarização; não está documentada uma cadeia de resumos.
Transferência proposta para modelo pequeno: Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.
Limite: Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.
Fontes: V4D-S005.

V4D-C004 — Google / Chrome built-in AI / Summarizer API
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação lista a Summarizer API no Chrome estável desde a versão 138.
Mecanismo documentado: Interface local de geração com modelo gerenciado pelo navegador e requisitos de disponibilidade.
Correspondência com esta base: Não documenta cadeia de sumarização por trás da API.
Transferência proposta para modelo pequeno: Proposta: detectar disponibilidade local e limitar a tarefa a texto fornecido; manter o contrato de saída igual quando um backend alternativo for necessário.
Limite: Disponibilidade não constitui prova de implantação em cliente, volume de tráfego ou porte exato do modelo. As etapas de preview e estável precisam ser verificadas por API.
Fontes: V4D-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q022.

## T004:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T004 → T072 [requires]
Como combinar: Versionar cada visão e sua base comum.
Interface: revision_id, covered_until e lista de alterações.
Condição: Visões derivadas da mesma revisão.
Aceite proposto: Detectar mistura de resumo operacional novo e explicativo antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T004 → T015 [complements]
Como combinar: Ligar justificativas a originais sob demanda.
Interface: Afirmação, referência e intervalo de origem.
Condição: Referência resolver conteúdo específico.
Aceite proposto: Conferir leitura original quando uma hipótese muda.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar queda de certeza explicitamente.
- Não fundir opiniões de fontes distintas como consenso.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar decisões após sucessivas correções, sem usar concisão ou fluência como medida principal.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T043, T059, T072

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

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

### V4D-S007 — Built-in AI APIs

[https://developer.chrome.com/docs/ai/built-in-apis](https://developer.chrome.com/docs/ai/built-in-apis)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade e estágio das APIs locais do Chrome; Summarizer documentado como estável desde Chrome 138.

Limite: Tabela é mutável e partes textuais podem acompanhar versões em ritmos diferentes. API disponível não comprova uso por cliente; não identifica porte exato do checkpoint.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
