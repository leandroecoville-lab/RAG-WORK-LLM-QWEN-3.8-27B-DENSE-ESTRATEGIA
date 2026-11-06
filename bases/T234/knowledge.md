# T234 — Persistent Project Memory File — incluindo memória por módulo

**Nome canônico:** Persistent Project Memory File — incluindo memória por módulo  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T234  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** project memory file; memória persistente por módulo

## T234:C01 — conceito

Arquivo persistente que fornece contexto reutilizável sobre um projeto e, quando necessário, seus módulos. As documentações de Claude Code e Codex descrevem arquivos de instruções e mecanismos próprios de carregamento. Um arquivo de memória pode reunir decisões e referências; seu conteúdo não é, por si só, um banco transacional ou controle de acesso.

Como funciona:
- O contexto é recuperado entre sessões por regras explícitas do produto ou do controlador.
- Uma camada geral descreve o projeto; arquivos locais acrescentam informação relevante ao módulo.
- Referências a documentos e decisões permitem expandir detalhes sem carregar todo o histórico.

## T234:C02 — aplicacao

Quando usar:
- Convenções estáveis, comandos verificados de desenvolvimento, decisões arquiteturais e orientação para novos agentes.

Quando não usar:
- Armazenar grandes logs, credenciais ou estados de operações externas que exigem atualização transacional.

Implementação proposta:
- Proposta: separar instruções vigentes, fatos verificados, decisões e pendências, com origem e data quando relevantes.
- Usar nomes e hierarquia realmente documentados pelo executor escolhido, como AGENTS.md ou CLAUDE.md, sem presumir regras idênticas.
- Manter o arquivo principal curto e distribuir detalhes por módulo com referências explícitas.
- Revisar entradas quando mudarem ferramentas, contratos ou estrutura do repositório.
- Confrontar memória antiga com a revisão atual antes de executar comandos ou modificar código.

Aplicação LAI proposta:
Proposta LAI: manter memória curta por projeto e módulo, vinculada a fontes e revisões, deixando estado operacional e histórico detalhado em registros próprios.

## T234:C03 — riscos_validacao

Armadilhas:
- Anotações antigas podem parecer instruções vigentes.
- Arquivos volumosos consomem contexto em toda sessão.
- Uma instrução escrita não garante que o runtime a carregou ou aplicou.

Métricas sugeridas:
- Entradas com proveniência; referências quebradas; conteúdo desatualizado; tokens carregados; erros causados por instruções antigas.

Testes propostos:
- Iniciar uma sessão no módulo e verificar quais instruções o executor realmente carregou.
- Alterar um comando do projeto e conferir revisão da memória associada.
- Inserir uma pendência como hipótese e verificar que ela não é apresentada como fato confirmado.

## T234:C04 — perguntas_proveniencia

Pergunta: AGENTS.md e CLAUDE.md funcionam da mesma forma?
Resposta: Não se deve presumir isso. Nomes, descoberta, escopo e precedência dependem da documentação e versão de cada executor.

Pergunta: O arquivo pode afirmar que uma tarefa terminou?
Resposta: Pode referenciar a evidência de conclusão, mas uma anotação isolada não substitui o estado confirmado, os artefatos e os resultados de verificação.

Pergunta: Colocar AGENTS.md em qualquer pasta garante leitura?
Resposta: Não. É necessário conhecer o caminho de descoberta, o diretório de execução e os limites do produto.

Pergunta: Memória de módulo deve copiar todas as regras globais?
Resposta: Não por padrão. Referências e responsabilidades claras reduzem divergência entre cópias que envelhecem separadamente.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T234:C05 — mecanismo_avancado

Memória por módulo depende de descoberta e escopo, não apenas de existir um arquivo no disco. No Codex documentado, arquivos de instrução são coletados ao longo do caminho até o diretório corrente, com precedência entre nomes e um limite de tamanho. Assim, um guia de módulo pode não ser carregado em uma execução iniciada noutro local. Uma proposta mantém decisões e fatos separados de instruções operacionais, incluindo revisão e referência à evidência.

Condição de contorno:
Um arquivo antigo pode continuar sendo carregado corretamente e ainda transmitir informação obsoleta sobre o projeto.

Contrato proposto:
- Entradas: Diretório de execução, política de descoberta, arquivos do projeto e revisão vigente.
- Saídas: Conjunto efetivamente carregado e referências de memória aplicáveis ao módulo.
- Estado: Versões, precedência e responsáveis por atualização das decisões.
- Invariante: Existência de um arquivo não é registrada como prova de que o agente o recebeu ou aplicou.

Compromissos de projeto:
- Arquivos locais ao módulo reduzem contexto irrelevante e podem fragmentar regras compartilhadas.
- Um arquivo central facilita governança e cresce até perder densidade ou ultrapassar limites de carregamento.

## T234:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar execuções em diretórios diferentes com instruções locais divergentes; conferir o conjunto carregado e a versão utilizada antes de avaliar comportamento.

Plano de avaliação proposto:
Comparar memória central e por módulo em tarefas que atravessam fronteiras do projeto. Medir contexto carregado, decisões obsoletas e contradições. Definir fonte canônica para regras compartilhadas e referências explícitas entre módulos.

Comparações:
- T211 (distinct_from): Handoff descreve uma transferência de trabalho; memória de projeto conserva conhecimento reutilizável.
- T155 (complements): Instruções enxutas podem apontar para detalhes de módulo carregados quando necessários.

Afirmação rastreável:
A documentação Codex descreve descoberta de AGENTS.md por caminho, arquivos de override e limite de tamanho combinado.
Suporte: direct; fontes: V2A-S017
Limite: Essas regras são do produto documentado; outros agentes podem carregar arquivos de modo diferente.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T234:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava descoberta e escopo de arquivos por módulo. A expansão organiza memória como conhecimento versionado com dono, separa instruções de fatos e cria uma rotina de manutenção vinculada a mudanças reais.

Mapa e conhecimento local
Mantenha entrada curta com estrutura do projeto e caminhos para detalhes. Regras específicas vivem perto do módulo correspondente, enquanto decisões transversais ficam numa fonte comum. A descoberta precisa ser testada no diretório e runtime usados; colocar um arquivo no repositório não garante que todos os agentes o lerão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S039.

Fatos, instruções e decisões
Identifique natureza e validade de cada registro. Comando de teste é instrução operacional; resultado de teste é evidência de uma revisão; escolha arquitetural é decisão com contexto. Misturá-los faz uma evidência antiga parecer autorização atual ou um plano parecer execução. Referencie artefatos para evitar duplicar detalhes que envelhecem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V4C-S026.

Manutenção por mudança
Quando código ou contrato muda, atualize a memória afetada ou marque-a para revisão. Um agente pode propor correções, mas o critério é aderência ao estado real do projeto. Checagens de links e estrutura ajudam, enquanto a validade semântica pode exigir testes ou revisão. Não acumule toda sessão como instrução permanente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030.

USO AVANÇADO — Projeto operado por modelos locais
Cenário: Agentes retomam trabalho em módulos sem carregar conversas anteriores.
Estratégia: Forneça mapa geral curto, contrato do módulo, comandos válidos e decisões que limitam a alteração. Na retomada, confirme revisão e leia arquivos atuais. Ao concluir, proponha só fatos estáveis ou lições verificadas para memória, deixando logs transitórios em artefatos próprios.
Papel do modelo pequeno: 3–7B executa unidade; 8–14B atualiza registros locais; 15–30B revisa decisões transversais.
Aceite proposto: Proposta: menor custo de orientação e ausência de instruções incompatíveis com o código atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030.

USO AVANÇADO — Onboarding técnico
Cenário: Uma pessoa ou agente precisa entender a origem de um comportamento.
Estratégia: Recupere decisão relevante e caminho de código, distinguindo justificativa histórica de implementação vigente. Se houver conflito, registre a divergência e investigue; não escolher o arquivo de memória apenas porque foi escrito com linguagem confiante.
Papel do modelo pequeno: 8–14B localiza documentação; 15–30B integra contexto e código.
Aceite proposto: Proposta: respostas com referências válidas e identificação de memória obsoleta em casos inseridos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V4C-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Instruções curtas por módulo e exemplos de comandos reduzem carga de descoberta.
8–14B: Atualizações localizadas e checagem de referências, com validação contra o repositório.
15–30B: Síntese de decisões entre módulos, sem transformar toda reflexão em regra global.
Requisitos de treino/runtime: Versionamento, escopo, dono da informação e testes de descoberta no runtime escolhido.
Não aplicar quando: Não armazenar segredos em arquivo de instrução nem considerar presença no disco como prova de carregamento.

## T234:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 2; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: CLAUDE.md fornece instruções e contexto de navegação.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: AGENTS.md curto e documentação versionada no repositório oferecem memória persistente do projeto; não é mera configuração CI.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Instruções do repositório são usadas como contexto.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Anthropic e OpenAI relatam uso interno de arquivos e conhecimento no repositório. O desenho por módulo e critérios de manutenção precisam ser validados no projeto do usuário.
Consultas registradas: V4C-Q024, V4C-Q027.

## T234:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T234 → T155 [complements]
Como combinar: Harness Codex substitui instrução monolítica por mapa curto com referências para conhecimento do projeto.
Interface: Entrada de instruções, índice e documentos versionados.
Condição: Fontes detalhadas estão acessíveis quando necessárias.
Aceite proposto: Agente recupera regra relevante sem receber todo o manual.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

2. T234 → T213 [complements]
Como combinar: Planos versionados e conhecimento do repositório acompanham decomposição em blocos verificáveis no harness.
Interface: Plano, decisão e contrato de módulo.
Condição: Mudanças de requisito atualizam tarefas afetadas.
Aceite proposto: Micro-missão não executa orientação antiga sem revalidar.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

CONTROLES DE FALHA
- Memória corretamente carregada pode continuar semanticamente errada.
- Não converter sucesso alegado em fato persistente sem evidência de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare continuidade e orientação por arquivo com histórico bruto sob o mesmo conjunto de tarefas. Memória externa pode aumentar utilidade de 3–30B sem alterar pesos ou garantir retenção factual interna.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T064, T238

## Fontes primárias associadas

### V2A-S016 — How Claude remembers your project

[https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instruções persistentes em arquivos e memória automática; escopo e carregamento dependem da configuração.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S017 — Custom instructions with AGENTS.md

[https://developers.openai.com/codex/guides/agents-md/](https://developers.openai.com/codex/guides/agents-md/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta hierárquica de instruções de projeto pelo Codex e limites de carregamento.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

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

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
