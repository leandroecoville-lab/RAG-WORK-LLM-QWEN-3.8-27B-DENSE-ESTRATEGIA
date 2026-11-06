# R027 — Git

**Nome canônico:** Git — controle distribuído de versões  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R027  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Git version control; controle de versões com Git

## R027:C01 — conceito

Git organiza versões de arquivos em objetos e commits que registram snapshots, pais e metadados. O histórico permite comparar mudanças, relacionar decisões à revisão de código e reconstruir arquivos versionados. Em agentes de programação, isso fornece uma base verificável para checkpoints de código, sem capturar automaticamente bancos, serviços externos ou estado de execução.

Como funciona:
- Blobs representam conteúdo; árvores organizam caminhos; commits apontam para uma árvore e para seus ancestrais.
- Branches identificam linhas de trabalho; diffs mostram alterações entre versões ou entre o estado de trabalho e uma referência.
- Worktrees permitem diretórios de trabalho separados vinculados ao mesmo repositório, úteis para missões paralelas.

Nota de nomenclatura: Referência ao Git, sem confundir com um serviço específico de hospedagem. Nenhum commit, branch ou worktree do usuário foi criado ou alterado.

## R027:C02 — aplicacao

Quando usar:
- Rastreamento de código, instruções, memória textual e artefatos pequenos que precisam de comparação por versão.

Quando não usar:
- Como único mecanismo de recuperação de processos, confirmação de operações externas ou preservação de arquivos não incluídos no commit.

Implementação proposta:
- Proposta: registrar a revisão inicial e as alterações existentes antes de iniciar uma missão.
- Usar branch e worktree por mudança independente; revisar o diff e adicionar explicitamente os arquivos que compõem cada etapa.
- Criar commits coerentes com evidências de verificação; guardar referências externas de testes e confirmar sincronização quando recuperação remota for necessária.

Aplicação LAI proposta:
Proposta LAI: vincular missões, patches e resultados de validação a revisões Git; usar esse vínculo para retomar trabalho e comparar mudanças sem depender somente do histórico conversacional.

## R027:C03 — riscos_validacao

Armadilhas:
- Um commit pode conter código incorreto; hash e histórico identificam conteúdo, não comprovam comportamento.
- Integrar sem conflito textual não garante compatibilidade semântica; recursos externos usados por worktrees podem continuar compartilhados.

Métricas sugeridas:
- Rastreabilidade entre tarefa e commit, alterações indevidas, conflitos de integração e sucesso da reconstrução de uma revisão.

Testes propostos:
- Proposta: reconstruir o projeto pela revisão registrada em diretório separado e executar verificações relevantes.
- Integrar mudanças paralelas com interação funcional conhecida e conferir testes; testar recuperação incluindo os artefatos externos necessários.

## R027:C04 — perguntas_proveniencia

Pergunta: Commit é um snapshot completo do agente?
Resposta: Não. Ele representa arquivos versionados e metadados; conversa, memória volátil e efeitos externos exigem mecanismos próprios.

Pergunta: Worktrees impedem todos os conflitos entre agentes?
Resposta: Não. Isolam diretórios de trabalho, mas alterações ainda precisam ser integradas e serviços ou recursos externos podem continuar compartilhados.

Pergunta: Mesmo conteúdo implica mesmo commit?
Resposta: Não. Pais e metadados também compõem o commit; compare árvores quando a questão for conteúdo.

Pergunta: Testar o working tree valida um commit parcialmente staged?
Resposta: Somente se os conteúdos coincidirem. Verifique a árvore candidata ou teste um checkout construído a partir dela.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R027:C05 — mecanismo_avancado

Git separa objetos imutáveis de referências mutáveis. Uma árvore identifica conteúdo e caminhos; um commit acrescenta pais e metadados, então commits diferentes podem apontar à mesma árvore. Publicar uma etapa envolve mover uma referência para o commit validado, operação diferente de construir objetos. git update-ref aceita o valor anterior esperado, permitindo rejeitar publicação quando outro processo moveu a referência. Transações com várias referências validam e bloqueiam atualizações, mas leitores concorrentes podem observar um subconjunto das mudanças. Essa propriedade não deve ser ampliada para um snapshot global de leitura.

Condição de contorno:
O commit normalmente usa o índice; com staging parcial, o conteúdo commitado pode diferir do diretório testado. Nenhum hash demonstra correção funcional.

Contrato proposto:
- Entradas: Árvore validada, commit candidato, referência de destino e identificador anterior esperado.
- Saídas: Nova referência confirmada ou conflito explícito sem sobrescrever trabalho concorrente.
- Estado: Índice, working tree, objetos e referências registrados separadamente.
- Invariante: A revisão publicada corresponde ao conteúdo validado; atualização concorrente força reconciliação.

Compromissos de projeto:
- Publicação condicional evita perda silenciosa, mas requer resolver conflitos de evolução legítimos.
- Commits pequenos melhoram rastreabilidade, porém testes precisam acompanhar a composição final das etapas.

## R027:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: validar um commit e mover a referência por outro processo antes da publicação. Exigir falha da atualização condicional; repetir com staging parcial e detectar divergência entre árvore testada e publicada.

Plano de avaliação proposto:
Comparar publicação direta com condicional sob concorrência controlada. Medir sobrescritas, conflitos corretamente detectados e divergências de conteúdo; aceitar somente estratégia que preserve histórico e vínculo de validação.

Comparações:
- T236 (complements): Commit por etapa precisa garantir que o índice representa a etapa testada, além de registrar mensagem.
- T239 (complements): Worktrees separam índices e diretórios, mas compartilham objetos e várias referências do repositório.

Afirmação rastreável:
git update-ref pode exigir correspondência com o objeto anterior; atualizar várias referências não garante visão conjunta atômica para todo leitor concorrente.
Suporte: direct; fontes: V3C-S037
Limite: A atomicidade descrita não cobre arquivos externos, serviços ou validação semântica do commit.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R027:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda a identidade de commits com atestação da árvore efetivamente testada, integração concorrente e vínculo entre código, modelo e medições.

Teste ligado à árvore
Proposta: registrar hash da árvore, dependências relevantes e configuração de teste no resultado. Se qualquer entrada muda após o teste, a evidência deixa de autorizar promoção. O commit preserva uma versão; não prova que essa versão é exatamente a que foi exercitada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

Integração concorrente
Validar cada candidato em isolamento e depois validar a composição. Dois patches corretos na mesma base podem interagir ao serem unidos. A atualização final de referência usa revisão esperada e o controlador trata rejeição concorrente como necessidade de reintegração, não como retry cego.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

Experimento versionado
Vincular revisão de código, checksum de pesos/adaptador, política de prompt e dataset ao relatório de desempenho. Grandes artefatos podem permanecer fora do repositório, identificados por manifestos. Reverter código sem reverter configuração do modelo pode não restaurar o comportamento observado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

USO AVANÇADO — Integração de agentes de código
Cenário: Dois trabalhadores mudam módulos relacionados.
Estratégia: Criar candidatos isolados, verificar contratos locais e executar testes de interação sobre a árvore combinada.
Papel do modelo pequeno: Modelos pequenos produzem mudanças estreitas; Git e CI preservam identidade e promoção.
Aceite proposto: Uma mudança concorrente de base invalida o aceite antigo e exige nova verificação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

USO AVANÇADO — Comparação de sistemas 3–30B
Cenário: Experimento mistura alterações de prompt, quantização e retrieval.
Estratégia: Congelar manifestos por condição e separar ablações em revisões identificáveis.
Papel do modelo pequeno: O modelo é objeto do experimento; não decide qual revisão foi executada.
Aceite proposto: Reproduzir o relatório a partir dos manifestos ou registrar precisamente a dependência indisponível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: editar unidades pequenas com diffs legíveis; versionamento não compensa raciocínio insuficiente.
8–14B: 8–14B: refatorações locais com integração validada por árvore.
15–30B: 15–30B: alterações maiores continuam exigindo controles de concorrência e evidência.
Requisitos de treino/runtime: Git atua sobre artefatos; não requer treino nem conhece semântica da tarefa.
Não aplicar quando: Não armazenar volumes ilimitados de traces ou pesos no Git apenas porque o repositório aceita arquivos.

## R027:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: O operador confirma migração e uso de Git.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Git e worktrees sustentam o ambiente.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: Fonte descreve um sistema de versionamento relacionado e diferenças para Git, não adoção interna integral de Git.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Sistema substituiu Git naquele ambiente; não comprova comportamento Git atual.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: Clonagem, commits e pull requests compõem o fluxo documentado.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Windows/Git, GitHub e Codex fornecem evidências delimitadas. Sapling e Scion mantêm mapeamentos de família/analogia quando o mecanismo Git não está comprovado.
Consultas registradas: V4C-Q015, V4C-Q016, V4C-Q011.

## R027:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R027 → T239 [complements]
Como combinar: Isolar candidatos e conservar a identidade de suas bases.
Interface: Worktree, tarefa e commit-base.
Condição: Há edição concorrente.
Aceite proposto: Nenhum índice ou diretório de um trabalhador contamina o candidato de outro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R027 → T233 [complements]
Como combinar: Invalidar a aprovação quando a árvore do candidato muda.
Interface: Tree_hash, ambiente de teste e revisão esperada da referência.
Condição: Uma alteração será integrada.
Aceite proposto: Só a árvore verificada é promovida, com nova validação após composição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V3C-S036, V4C-S020, V4C-S021, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir Sapling/Piper com Git por oferecerem operações semelhantes.
- Não interpretar hash ou assinatura como prova de correção funcional.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar taxa de mudanças aceitas e custo de integração, incluindo conflitos. Controle de versão é infraestrutura comum aos modelos comparados, não uma vantagem paramétrica.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T061, T072, T076, T229, T233, T236, T239, R013

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2B-S026 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho ligadas ao mesmo repositório e organização de branches em diretórios separados.

Limite: Manual oficial consultado; não descreve isolamento de serviços externos nem garante correção de merges. Nenhum worktree do usuário foi alterado.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S036 — Git — git-commit

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Commit usual registra o índice; opções com paths e seleção parcial mudam quais alterações são incluídas.

Limite: Commit não captura por si arquivos ignorados, banco de dados, processos ou efeitos externos.

### V2A-S019 — git-worktree

[https://git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Múltiplas árvores de trabalho associadas a um mesmo repositório.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V4C-S016 — GitHub Copilot: Meet the new coding agent

[https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recurso comercial de execução em GitHub Actions, edição, commits, contexto de repositório e PR; não comprova um cliente específico.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

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
