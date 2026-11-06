# T214 — Tool Output Pruning

**Nome canônico:** Tool Output Pruning  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T214  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda de saída de ferramentas

## T214:C01 — conceito

Redução seletiva de saídas de ferramentas antes de incluí-las no contexto. A poda pode remover linhas repetidas, campos irrelevantes ou trechos já conhecidos, mantendo acesso ao resultado original. Seu objetivo é aumentar densidade de informação sem esconder dados necessários para interpretar sucesso, falha ou alcance da consulta.

Como funciona:
- Capturar a saída completa em artefato e produzir uma visão compacta específica para o tipo de ferramenta.
- Preservar metadados como código de saída, cobertura, truncamento e localização dos detalhes omitidos.
- Permitir expansão direcionada quando o agente necessita de evidência que ficou fora da visão inicial.

## T214:C02 — aplicacao

Quando usar:
- Logs volumosos, resultados de busca, respostas JSON extensas e listagens de repositórios.

Quando não usar:
- Quando a seleção não consegue identificar campos críticos ou a saída é curta e já relevante.

Implementação proposta:
- Proposta: criar adaptadores por ferramenta, com regras determinísticas para erros, avisos e linhas representativas.
- Mostrar contagem total e omitida, além de referência estável para o original.
- Em testes, destacar falhas e contexto de stack trace; em buscas, manter arquivos, linhas e limites da pesquisa.
- Ajustar a política por tarefa, sem converter ausência na amostra em ausência no conjunto completo.

Aplicação LAI proposta:
Proposta LAI: entregar ao agente uma visão de logs com erro, resultado e ponteiros, mantendo a evidência completa para inspeção.

## T214:C03 — riscos_validacao

Armadilhas:
- Guardar apenas as primeiras linhas pode esconder o erro final.
- Filtrar por palavras-chave pode remover a causa anterior da falha.
- Poda destrutiva impede auditoria posterior.

Métricas sugeridas:
- Tokens poupados; recuperação de detalhes; erros críticos omitidos; latência adicional do adaptador.

Testes propostos:
- Colocar um erro no meio e no fim de um log e verificar sua preservação.
- Produzir saída sem resultado por limite de busca e exigir aviso de cobertura.
- Comparar decisões com saída integral e podada em casos representativos.

## T214:C04 — perguntas_proveniencia

Pergunta: Poda precisa usar outro LLM?
Resposta: Não. Seleção de campos, deduplicação e limites por seção podem ser determinísticos; um resumo por LLM é outra opção.

Pergunta: Poda e Observation Masking são iguais?
Resposta: Não. Poda seleciona partes de uma saída; masking normalmente oculta observações antigas inteiras por uma política de histórico.

Pergunta: Posso guardar só a última linha do comando?
Resposta: Somente se ela representar o resultado necessário; muitos comandos produzem avisos ou falhas relevantes antes dela.

Pergunta: Como diferenciar ausência de erro e erro removido?
Resposta: Preservar metadados de completude e critérios de seleção, além de acesso à saída original.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T214:C05 — mecanismo_avancado

Podar uma saída exige preservar sinais que determinam sua interpretação: código de retorno, alcance da consulta, paginação, truncamento e contexto do erro. Selecionar apenas linhas com sucesso pode transformar falha parcial em aparente conclusão. Uma proposta mantém um cabeçalho de proveniência e uma referência ao original, separando fatos extraídos de texto omitido. A extração deve ocorrer por unidades semânticas, como registro ou traceback completo.

Condição de contorno:
Se a informação necessária não pode ser reconhecida por regras confiáveis, poda agressiva pode custar mais em releituras que o contexto economizado.

Contrato proposto:
- Entradas: Saída original, metadados de execução, objetivo da leitura e orçamento.
- Saídas: Trechos selecionados, indicadores de completude e referência ao original.
- Estado: Hash ou versão, regra de seleção e intervalos omitidos.
- Invariante: A poda não altera sucesso, falha ou alcance sem registrar essa mudança de representação.

Compromissos de projeto:
- Filtros determinísticos são baratos e podem perder exceções inesperadas.
- Síntese por modelo capta significado e introduz custo e risco de inferência indevida.

## T214:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar a única falha no meio de milhares de linhas de sucesso e ocultar a última página; exigir preservação da falha e indicação de incompletude.

Plano de avaliação proposto:
Comparar saída integral, filtros por campos e seleção semântica em logs rotulados. Medir tokens, falhas relevantes preservadas e releituras necessárias. Aprovar redução somente se mantiver os sinais exigidos pela decisão posterior.

Comparações:
- T215 (distinct_from): Masking substitui observações antigas; pruning pode selecionar dentro de uma observação atual.
- T238 (complements): Referências por faixa permitem recuperar detalhes omitidos quando necessário.

Afirmação rastreável:
O estudo de observation masking identifica saídas de ferramentas como parte importante do crescimento de contexto de agentes de software.
Suporte: related; fontes: V2A-S003
Limite: A fonte motiva reduzir observações; o contrato de poda seletiva e seus filtros são proposta editorial.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T214:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservava proveniência, erros e paginação na poda. A expansão projeta respostas de ferramenta antes da transferência, usa seleção em duas passagens e protege dados que terão função em verificações futuras.

Projeção junto à origem
Quando o serviço suporta seleção de campos, peça somente o que a próxima decisão exige. Isso reduz rede e parsing além de tokens. A seleção precisa incluir identificador, versão e estado de completude; omitir um campo de erro pode tornar uma resposta parcial indistinguível de sucesso. Projeção é contrato, não simples corte de caracteres.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

Índice seguido de detalhe
Para resultados desconhecidos, peça primeiro metadados ou índice e depois os itens relevantes. A segunda passagem custa latência e só compensa quando evita grande volume inútil. Mantenha uma reserva para buscar detalhes que surgirem como necessários; não avalie a política apenas pelos tokens do primeiro retorno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, V4C-S014.

Poda orientada ao teste
Marque campos exigidos pelo critério de aceite como protegidos. Se a etapa seguinte compara versões ou verifica integridade, esses metadados não podem sair porque parecem repetitivos. Ao compactar logs, mantenha unidade semântica completa do erro e referência para o original; a seleção deve ser reprodutível para investigar omissões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S031.

USO AVANÇADO — API retorna objetos extensos
Cenário: O agente precisa de três campos de um conjunto profundo.
Estratégia: Resolva o schema, derive projeção explícita e valide que os campos obrigatórios vieram. Se o servidor não suportar projeção, armazene a resposta integral e selecione num adaptador determinístico antes de inserir no contexto. Retorno vazio exige distinguir ausência de dados e projeção incorreta.
Papel do modelo pequeno: 3–7B consome objeto curto; 8–14B propõe projeção revisada pelo contrato.
Aceite proposto: Proposta: redução de bytes e tokens sem campos críticos ausentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013.

USO AVANÇADO — Diagnóstico de build
Cenário: Milhares de linhas contêm poucos erros causais.
Estratégia: Agrupe falhas por teste e preserve traceback completo do primeiro erro relevante, versão e comando executado. Deixe avisos secundários recuperáveis. Quando o reparo falhar, recupere linhas ao redor antes de inventar nova hipótese sobre log que foi ocultado.
Papel do modelo pequeno: 8–14B classifica diagnósticos; 15–30B analisa causas entre módulos.
Aceite proposto: Proposta: mesma taxa de diagnóstico correto com menos contexto e reconsultas contabilizadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir campos estritos e pequenos, preservando sinais de ausência e erro.
8–14B: Selecionar unidades relevantes com retorno de referências ao original.
15–30B: Projetar dados para decisões compostas e identificar dependências informacionais futuras.
Requisitos de treino/runtime: Schemas confiáveis, armazenamento integral quando necessário e métricas de reconsulta e omissão.
Não aplicar quando: Não podar evidência que sustenta um resultado ainda pendente de validação.

## T214:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 2.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Response Projection reduz respostas aos campos selecionados.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Code-mode mantém polling e dados intermediários fora do contexto da LLM.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Gateway Uber documenta ResponseProjection e exposição progressiva. Critérios de preservação para cada tarefa são propostas a testar. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q009, V4C-Q028, V4D-Q019.

## T214:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T214 → T151 [complements]
Como combinar: OmniMCP combina descoberta progressiva e projeção de resposta para reduzir exposição desnecessária de contexto.
Interface: Schema resolvido e lista de campos solicitados.
Condição: A projeção respeita a ferramenta escolhida.
Aceite proposto: Campo ausente é tratado como ausência explícita, não sucesso presumido.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S013. Casos: V4C-C014.

2. T214 → T238 [complements]
Como combinar: Após retorno resumido, permitir leitura pontual dos trechos necessários para diagnóstico ou validação.
Interface: Referência imutável e intervalo requerido.
Condição: Original permanece disponível e na mesma revisão.
Aceite proposto: Releitura entrega evidência exatamente correspondente à seleção inicial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013, V4C-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Cortar por caracteres pode destruir JSON, traceback ou registro multipartido.
- Resultado projetado deve indicar se houve paginação, truncamento ou falha parcial.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelo pequeno com projeção e fronteira com a mesma evidência relevante. Vantagem por remoção de ruído não significa capacidade de reconstruir campos descartados.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T215, T238, T222

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S003 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://kairos.jetbrains.com/research/articles/the-complexity-trap](https://kairos.jetbrains.com/research/articles/the-complexity-trap)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação controlada de mascaramento de observações e resumo de trajetória; são transformações distintas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
