# T233 — Patch Validation — incluindo verificação de hash-base

**Nome canônico:** Patch Validation — incluindo verificação de hash-base  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T233  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** base hash validation; validação de patch

## T233:C01 — conceito

Validação de um patch antes e depois de aplicá-lo, incluindo a identidade da base quando necessária. O hash-base detecta que os bytes ou a revisão observados mudaram desde a leitura. Ele não comprova autoria, legitimidade do conteúdo ou correção funcional; essas propriedades exigem controles e evidências diferentes.

Como funciona:
- A aplicação compara a base atual com a identidade esperada e verifica o escopo dos caminhos.
- Uma etapa de aplicabilidade detecta conflitos de contexto e formato.
- Depois da gravação, inspeção do delta e verificações semânticas avaliam o resultado produzido.

Nota de nomenclatura: Verificação criptográfica da base é uma recomendação de protocolo; não se presume que todo editor a faça automaticamente.

## T233:C02 — aplicacao

Quando usar:
- Edições concorrentes, patches gerados por agentes e integração de alterações em arquivos compartilhados.

Quando não usar:
- Aceitar um hash calculado depois da mudança como se fosse a precondição original ou tratar dry-run como prova de comportamento.

Implementação proposta:
- Proposta: registrar revisão e hashes dos arquivos lidos, usando a mesma definição de bytes em leitura e comparação.
- Validar caminhos, operações permitidas e aplicabilidade sem ultrapassar o escopo autorizado.
- Comparar novamente a base no momento da escrita para reduzir a janela entre verificação e uso.
- Aplicar em checkout isolado; operações em vários arquivos exigem estratégia explícita de integração, pois renomeação atômica de um arquivo não torna o lote inteiro atômico.
- Recalcular hashes finais, revisar o diff e associar os resultados de testes à revisão efetivamente validada.

Aplicação LAI proposta:
Proposta LAI: exigir precondições de base e recibos de aplicação na integração de patches, preservando revisões concorrentes e identificando resultados parciais.

## T233:C03 — riscos_validacao

Armadilhas:
- Normalização silenciosa de finais de linha pode invalidar a comparação.
- A base pode mudar após um check separado.
- Reaplicar patch parcialmente aplicado pode duplicar alterações.

Métricas sugeridas:
- Conflitos de base; hunks rejeitados; mudanças fora do escopo; resultados parciais; verificações vinculadas à revisão correta.

Testes propostos:
- Modificar o arquivo após leitura e exigir conflito antes da escrita.
- Interromper um lote e reconciliar quais arquivos foram alterados antes de retomar.
- Verificar que uma aprovação sintática não é reportada como teste funcional executado.

## T233:C04 — perguntas_proveniencia

Pergunta: O comando de check substitui hash-base?
Resposta: Não necessariamente. Aplicabilidade e identidade exata da base são verificações diferentes; o protocolo deve exigir cada uma conforme o risco.

Pergunta: O que fazer depois de um conflito?
Resposta: Reler a revisão atual, preservar alterações independentes e reconstruir apenas o delta ainda necessário. Nunca forçar a base antiga por conveniência.

Pergunta: Um hash-base lido anteriormente elimina concorrência?
Resposta: Não. A comparação precisa participar da guarda da escrita ou publicação, não ser apenas uma verificação separada.

Pergunta: Por que registrar hash do resultado testado?
Resposta: Para demonstrar que o artefato entregue corresponde à versão avaliada e não a uma edição posterior sem validação.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T233:C05 — mecanismo_avancado

Verificar hash e aplicar depois deixa uma janela de corrida: outro escritor pode alterar a base entre as duas operações. Uma proposta prepara a alteração em árvore isolada, verifica o resultado e publica uma referência somente se o destino ainda apontar para a revisão esperada. git-update-ref oferece comparação com old-oid para esse tipo de atualização de ref. Isso protege publicação da revisão; não torna efeitos de scripts ou bancos parte da mesma transação.

Condição de contorno:
Um teste aprovado em árvore diferente da publicada não sustenta a conclusão sobre o artefato entregue.

Contrato proposto:
- Entradas: Patch, revisão-base, critérios de validação e referência de destino.
- Saídas: Artefato validado identificado ou conflito de base/publicação.
- Estado: Hashes de entrada e saída, evidências dos testes e referência esperada.
- Invariante: O objeto publicado é exatamente aquele ao qual se referem as evidências de validação.

Compromissos de projeto:
- Preparação isolada reduz disputas e exige integração explícita.
- Revalidar após mudanças concorrentes custa tempo e evita publicar evidência obsoleta.

## T233:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aprovar um candidato e avançar a referência de destino antes da publicação; exigir rejeição condicional e nova integração, sem sobrescrever o avanço concorrente.

Plano de avaliação proposto:
Comparar check seguido de escrita livre e publicação condicionada à base. Medir conflitos detectados, revisões erradas publicadas e custo de revalidação. Separar integridade dos bytes, aplicação do patch e correção funcional.

Comparações:
- T229 (complements): A estratégia de patch precisa dessa ligação entre base, delta e resultado.
- T236 (complements): Commits podem identificar o artefato validado e seu ponto de integração.

Afirmação rastreável:
git-update-ref permite atualizar uma ref somente quando seu valor atual corresponde ao old-oid informado.
Suporte: direct; fontes: V3C-S037
Limite: A guarda cobre a referência Git; não é uma transação global de todo o ambiente de execução.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T233:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 eliminava corrida entre hash e aplicação. A expansão organiza um pacote de evidência de validação, seleciona verificadores conforme o delta e trata publicação como operação condicional sobre o artefato realmente testado.

Identidade do candidato
Vincule base, patch e árvore resultante a uma identidade imutável. Cada teste registra qual árvore e ambiente executou. Se o agente altera código depois do teste, o resultado não acompanha automaticamente a nova versão. O pacote de validação deve permitir reproduzir a ligação entre requisito, candidato e prova sem confiar na mensagem final do executor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S030.

Portões por propriedade
Separe estrutura, aplicabilidade, escopo e comportamento. Parser pode aprovar sintaxe e teste pode não cobrir intenção; revisão de propriedade acrescenta evidência diferente, sem se tornar prova formal. Escolha testes de impacto pelo delta e por dependências, mantendo um conjunto mínimo obrigatório quando o alcance não puder ser calculado com confiança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S010.

Publicação condicionada
Prepare e valide em árvore isolada, depois atualize a referência apenas se o destino ainda corresponde à base esperada. Se alguém avançou a referência, rebase ou reconcilie e invalide as provas afetadas. Essa condição protege o código publicado; scripts executados durante testes podem ter efeitos fora da transação e exigem isolamento próprio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S027.

USO AVANÇADO — Agente editor com integração automática
Cenário: Um trabalhador entrega patch e afirma que os testes passaram.
Estratégia: O integrador verifica identidade de base, aplica em ambiente isolado e exige evidência de execução sobre a árvore candidata. Rode verificações essenciais e publique condicionalmente. Se o trabalhador não entregou prova válida, trate a informação como relato a confirmar, não como aprovação suficiente.
Papel do modelo pequeno: 3–7B pode gerar patch; 8–14B interpreta falhas; controlador valida identidade e publicação.
Aceite proposto: Proposta: nenhum artefato entregue com testes de outra revisão ou base inesperada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S009.

USO AVANÇADO — Vários candidatos paralelos
Cenário: Múltiplos agentes propõem soluções para o mesmo defeito.
Estratégia: Valide cada candidato em isolamento e compare qualidade, escopo e custo. Depois de escolher, confirme que a base de integração permanece válida; não misture trechos de candidatos aprovados sem testar a composição. O novo conjunto é outro artefato com riscos próprios.
Papel do modelo pequeno: 15–30B avalia tradeoffs; verificadores externos decidem requisitos objetivos.
Aceite proposto: Proposta: seleção reproduzível e regressões de composição detectadas antes da publicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerar deltas pequenos que possam ser rejeitados ou aceitos por critérios externos claros.
8–14B: Diagnosticar falhas e sugerir verificações relevantes, sem emitir prova textual substituta.
15–30B: Integrar candidatos e analisar intenção, mantendo isolamento e gates determinísticos.
Requisitos de treino/runtime: Hashes, revisão base, ambientes reproduzíveis, evidência por teste e atualização condicional de referência.
Não aplicar quando: Não aceitar código apenas porque aplica, compila ou recebeu aprovação de outro modelo.

## T233:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 2. Lacuna: 8. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: Análises são associadas à mudança de código antes da integração.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Patches são verificados antes de serem oferecidos para integração.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Linters e testes estruturais verificam invariantes.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: Uso de testes e revisão é relatado; o artigo não demonstra o contrato completo de validação de patch com identidade de base e publicação.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Há etapas de validação, sem demonstração integral do protocolo de hash-base da ficha.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Fontes operacionais mostram partes de validação. Testes genéricos não foram usados como prova automática do contrato completo com hash-base e publicação condicional.
Consultas registradas: V4C-Q005, V4C-Q006, V4C-Q007, V4C-Q027.

## T233:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T233 → T239 [complements]
Como combinar: Usar worktrees ou isolamento equivalente para manter candidato e testes separados de outras mudanças.
Interface: Árvore candidata, ambiente e recursos externos exclusivos.
Condição: Isolamento cobre bancos, portas e outputs além dos arquivos.
Aceite proposto: Teste não depende de alteração não incluída na entrega.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V2A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T233 → T236 [complements]
Como combinar: Transformar candidato aprovado em commit identificado, mantendo a árvore testada como alvo da entrega.
Interface: Tree ID, commit e pacote de validação.
Condição: Índice corresponde aos bytes aceitos.
Aceite proposto: Commit parcial não omite dependência usada no teste.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S036, V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Hash-base sem exclusão ou publicação condicional deixa janela de corrida.
- Uma mudança posterior em teste, configuração ou código pode invalidar a prova anterior.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare patches aceitos, regressões e custo de revisão com modelo de fronteira. O pequeno modelo pode gerar candidatos competitivos sob gates fortes; a validade pertence ao artefato verificado, não ao porte.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T229, T230, T236, T239

## Fontes primárias associadas

### V2A-S014 — git-apply

[https://git-scm.com/docs/git-apply](https://git-scm.com/docs/git-apply)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação e aplicação de patches; contexto, índice e tratamento de caminhos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

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

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V2A-S019 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho associadas a um mesmo repositório.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S036 — Git — git-commit

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Commit usual registra o índice; opções com paths e seleção parcial mudam quais alterações são incluídas.

Limite: Commit não captura por si arquivos ignorados, banco de dados, processos ou efeitos externos.

### V4C-S006 — Getafix: How Facebook tools learn to fix bugs automatically

[https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/](https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Getafix implantado na Facebook, diferenças por AST e padrões aprendidos de correções humanas para sugerir patches.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S007 — Finding and fixing software bugs automatically with SapFix and Sapienz

[https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/](https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração e validação de patches com compilação, testes e aprovação humana, incluindo correções efetivamente implantadas.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
