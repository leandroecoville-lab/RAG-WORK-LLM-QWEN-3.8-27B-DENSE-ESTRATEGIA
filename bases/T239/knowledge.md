# T239 — Git Worktrees

**Nome canônico:** Git Worktrees  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T239  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** linked worktree; árvores de trabalho Git

## T239:C01 — conceito

Mecanismo Git para manter várias árvores de trabalho ligadas ao mesmo repositório. Cada worktree oferece diretório e estado de checkout próprios, enquanto compartilha objetos e partes da administração do repositório. Isso facilita trabalho paralelo em revisões distintas, mas não constitui isolamento de processos, serviços ou credenciais.

Como funciona:
- O repositório compartilha o banco de objetos entre árvores relacionadas.
- Cada árvore mantém arquivos de trabalho e estado próprio de checkout e índice.
- Branches e commits permitem revisar e integrar os resultados produzidos em cada área.

## T239:C02 — aplicacao

Quando usar:
- Agentes alterando módulos em paralelo, reprodução de uma regressão e comparação de versões sem trocar continuamente o checkout principal.

Quando não usar:
- Como sandbox de segurança ou garantia de que duas execuções não disputarão portas, banco de dados e serviços externos.

Implementação proposta:
- Proposta: criar uma árvore com branch ou revisão apropriada à missão, respeitando as restrições documentadas pelo Git.
- Atribuir diretório e responsabilidade de escrita ao executor correspondente.
- Separar configuração de testes, portas e dados temporários quando houver execução paralela.
- Concluir e revisar o delta antes de integrar à branch de destino.
- Inspecionar alterações não commitadas antes de remover uma árvore; preservar trabalho útil e limpar metadados pelo fluxo suportado.

Aplicação LAI proposta:
Proposta LAI: dar a cada missão de código uma área de trabalho identificada, com integração coordenada e recursos de teste separados quando necessário.

## T239:C03 — riscos_validacao

Armadilhas:
- Árvores diferentes podem usar o mesmo banco de testes.
- Integração textual sem conflito pode manter incompatibilidade semântica.
- Objetos compartilhados e referências comuns exigem cuidado com operações de manutenção e histórico.

Métricas sugeridas:
- Conflitos de integração; alterações fora da árvore atribuída; colisões de recursos; tempo de preparação; trabalho perdido na limpeza.

Testes propostos:
- Editar arquivos em uma árvore e confirmar que o checkout de outra não muda.
- Executar testes simultâneos com recursos separados e verificar ausência de interferência.
- Integrar duas mudanças compatíveis textualmente, mas conflitantes no contrato, e exigir validação funcional.

## T239:C04 — perguntas_proveniencia

Pergunta: Worktree é uma cópia independente do repositório inteiro?
Resposta: Não. Ele compartilha objetos e estruturas do repositório, embora ofereça uma árvore de arquivos e checkout separados.

Pergunta: Posso considerar toda integração segura se Git não apontar conflito?
Resposta: Não. Git detecta determinados conflitos de conteúdo; mudanças podem conflitar em APIs, comportamento ou dados sem conflito textual.

Pergunta: worktree lock impede outro agente de editar arquivos?
Resposta: Não. Seu propósito documentado é proteger a árvore administrativa contra certas operações de limpeza, movimento ou remoção.

Pergunta: Um teste em outro worktree pode alterar meu ambiente?
Resposta: Sim, se usar recursos compartilhados fora do checkout, como banco, porta, cache ou diretório de build.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T239:C05 — mecanismo_avancado

Worktrees mantêm HEAD e índice próprios, enquanto compartilham objetos e grande parte das refs. Isso explica por que mudanças de referências podem afetar a visão do repositório sem editar arquivos da outra árvore. O comando worktree lock protege metadados contra poda e remoção; não funciona como mutex de edição dos arquivos. Serviços, portas, bancos e outputs fora da árvore ainda exigem isolamento específico para execução paralela.

Condição de contorno:
Dois worktrees podem executar testes que escrevem no mesmo banco ou diretório externo e interferir apesar de seus arquivos de checkout estarem separados.

Contrato proposto:
- Entradas: Revisão-base, caminho da árvore, branch ou HEAD destacado e recursos externos.
- Saídas: Árvore identificada e contrato de integração do resultado.
- Estado: HEAD, índice, refs compartilhadas e recursos alocados por tarefa.
- Invariante: Isolamento de checkout não é anunciado como isolamento completo de processos ou efeitos.

Compromissos de projeto:
- Compartilhar objetos economiza armazenamento e mantém acoplamento administrativo do repositório.
- Separar árvores facilita paralelismo e exige limpeza e integração das revisões produzidas.

## T239:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: executar dois jobs em worktrees distintos usando o mesmo arquivo de saída externo; exigir detecção da colisão e atribuição de destinos separados.

Plano de avaliação proposto:
Comparar branches na mesma árvore e worktrees separados em alterações concorrentes. Medir conflitos de checkout, interferência de testes e custo de integração. Conferir também recursos externos, sem limitar a avaliação ao diff dos arquivos.

Comparações:
- T169 (complements): Agentes com contextos separados podem usar worktrees para também separar árvores de edição.
- T236 (complements): Commits identificam entregas que depois precisam ser integradas explicitamente.

Afirmação rastreável:
Git documenta HEAD e índice por worktree, refs compartilhadas e lock voltado à proteção administrativa.
Suporte: direct; fontes: V2A-S019
Limite: O mecanismo não fornece exclusão mútua geral para escrita nem isola dependências externas.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T239:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia objetos compartilhados e recursos externos. A expansão trata worktrees como unidades de experimento, organiza ambiente e limpeza e integra candidatos sem confundir isolamento de arquivos com isolamento completo de execução.

Ambiente por candidato
Além do checkout, associe portas, banco, diretórios temporários e observabilidade à identidade do candidato. O harness Codex relata aplicação e métricas por worktree; a transferência proposta replica esse princípio conforme o projeto. Se algum recurso precisa ser compartilhado, documente coordenação ou somente leitura, evitando testes concorrentes que alteram o mesmo estado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V2A-S019.

Ciclo de vida recuperável
Registre criação, branch, tarefa, processos ativos e prazo de retenção. Remover diretório não encerra necessariamente servidor iniciado por um agente. Antes da limpeza, classifique tarefas e efeitos pendentes, preserve artefatos necessários e finalize recursos próprios. Não apagar worktree só porque o processo principal terminou com exit code zero.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S039.

Integração condicional
Candidatos partem de uma base identificada, mas a branch principal pode avançar enquanto os testes rodam. Escolher um candidato não elimina a necessidade de reconciliar essa diferença. Depois de rebase, merge ou combinação de patches, teste a árvore resultante; a aprovação antiga pertencia à versão isolada anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S030.

USO AVANÇADO — Alternativas de reparo
Cenário: Vários modelos tentam resolver o mesmo defeito.
Estratégia: Crie worktree e recursos por candidato, aplique o patch e rode o mesmo teste reproduzível. Compare resultados e preserve só candidatos necessários à revisão. Evite que um trabalhador leia arquivos não confirmados do outro e transforme variantes em soluções correlacionadas inadvertidamente.
Papel do modelo pequeno: 3–7B gera reparos locais; 15–30B integra evidência e escolhe candidato.
Aceite proposto: Proposta: resultados reproduzíveis sem interferência entre testes ou servidores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V2A-S019.

USO AVANÇADO — Trabalho simultâneo por módulos
Cenário: Agentes executam micro-missões independentes no mesmo repositório.
Estratégia: Atribua worktree e branch por missão, fixe interfaces compartilhadas e integre por ordem de dependência. Use registro de tarefas para evitar alterações concorrentes incompatíveis; worktree não é mutex do domínio. Após integrar, limpe ambientes e mantenha evidência de validação.
Papel do modelo pequeno: 8–14B executa módulo; 15–30B coordena dependências de integração.
Aceite proposto: Proposta: nenhuma colisão de recurso externo e rastreabilidade da árvore testada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Isolamento permite testar patches pequenos sem arriscar alterações de outra tarefa.
8–14B: Executar módulo com ambiente próprio e devolver artefato identificado.
15–30B: Gerenciar combinação de candidatos e conflitos sem supor independência semântica por diretório.
Requisitos de treino/runtime: Git compatível, branches e recursos únicos, limpeza de subprocessos e registros de criação/retomada.
Não aplicar quando: Não usar worktree lock como trava de edição nem presumir bancos e portas isolados automaticamente.

## T239:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Artigo de harness usa uma aplicação e observabilidade isoladas por Git worktree.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Checkouts esparsos/virtualizados não são Git worktrees.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: Virtualização de checkout não comprova uso de Git worktrees.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Ambiente isolado não é prova de uso do comando Git worktree.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: OpenAI oferece caso direto de worktrees; Git/GVFS, Sapling e Scion não foram convertidos em casos exatos deste mecanismo.
Consultas registradas: V4C-Q027, V4C-Q015, V4C-Q016.

## T239:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T239 → R021 [complements]
Como combinar: Harness interno OpenAI executa Codex com aplicação e observabilidade específicas por Git worktree.
Interface: Revisão candidata, instância da aplicação e logs correspondentes.
Condição: Recursos externos da tarefa são isolados conforme o projeto.
Aceite proposto: Agente valida comportamento na instância do próprio candidato.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S030. Casos: V4C-C029.

2. T239 → T233 [complements]
Como combinar: Fornecer árvore isolada para aplicar e testar antes de publicação condicionada.
Interface: Base, árvore final e evidência de testes.
Condição: Nenhuma mudança posterior invalida a prova sem nova verificação.
Aceite proposto: Artefato entregue corresponde ao candidato aceito.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Refs e objetos compartilhados podem mudar mesmo sem alterações nos arquivos do outro worktree.
- Limpeza precisa tratar processos e recursos fora da árvore, não apenas remover o checkout.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare throughput de candidatos com custo de ambiente e validação incluídos. Paralelismo com modelos pequenos só ajuda quando CPU, memória e integração suportam a concorrência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T237, T236, T233

## Fontes primárias associadas

### V2A-S019 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho associadas a um mesmo repositório.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

### V4C-S029 — How OpenAI uses Codex

[https://openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso diário interno em compreensão de código, migrações, testes e fluxo de trabalho; recomendações AGENTS.md e backlog.

Limite: Relatos e orientações não isolam causalidade nem demonstram faixa de parâmetros 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
