# T236 — Git Commit por etapa

**Nome canônico:** Git Commit por etapa  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T236  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** incremental commits; checkpoint de código em Git

## T236:C01 — conceito

Registro de alterações coerentes em commits Git associados a etapas de trabalho. Cada commit preserva uma árvore versionada e sua relação com o histórico, facilitando revisão e recuperação de código. Ele não captura automaticamente arquivos não versionados, processos, banco de dados ou efeitos enviados a serviços externos.

Como funciona:
- O conjunto escolhido de alterações é registrado em um commit com mensagem e identidade verificáveis.
- Uma etapa pode apontar para esse commit e para evidências de validação.
- Sessões posteriores consultam o histórico para localizar a última mudança relevante e compreender sua intenção.

## T236:C02 — aplicacao

Quando usar:
- Desenvolvimento em etapas, handoffs, revisão de alterações e recuperação de versões de código conhecidas.

Quando não usar:
- Criar um commit por cada pequena digitação ou considerar que um commit equivale a publicação, implantação ou checkpoint completo da aplicação.

Implementação proposta:
- Proposta: escolher uma unidade lógica revisável e inspecionar o diff antes de selecionar os arquivos.
- Incluir somente alterações pertencentes à etapa, preservando trabalho independente de outros colaboradores.
- Registrar na mensagem o problema e o comportamento resultante, com referência à missão quando útil.
- Associar testes à revisão efetivamente testada; declarar explicitamente verificações não executadas.
- Usar o commit local como ponto de referência; push, merge e implantação dependem do fluxo e da autorização correspondentes.

Aplicação LAI proposta:
Proposta LAI: vincular cada marco de código a um commit revisável e a seus resultados de verificação, usando o histórico para continuidade entre sessões.

## T236:C03 — riscos_validacao

Armadilhas:
- Um commit pode conter código defeituoso.
- Misturar mudanças sem relação dificulta revisão e reversão.
- Credenciais ou artefatos grandes podem entrar no histórico se a seleção não for inspecionada.

Métricas sugeridas:
- Escopo de cada commit; alterações sem relação; revisões com evidência; facilidade de localizar a mudança causadora de regressão.

Testes propostos:
- Conferir se a árvore do commit contém exatamente os arquivos da etapa.
- Retomar uma sessão a partir do histórico e verificar identificação do próximo trabalho pendente.
- Comparar a revisão testada com o commit entregue para detectar alterações posteriores sem validação.

## T236:C04 — perguntas_proveniencia

Pergunta: Commit por etapa garante que cada commit passa todos os testes?
Resposta: Não. Essa é uma política adicional. Se um commit representar trabalho intermediário, seu estado e as limitações precisam estar claros.

Pergunta: Reverter o commit desfaz uma chamada de API?
Resposta: Não. Git registra código versionado; efeitos externos exigem reconciliação ou compensação específica quando disponível e autorizada.

Pergunta: Testar antes de git commit basta?
Resposta: Somente se o estado testado corresponder ao índice/árvore que será registrado; staging parcial pode quebrar essa equivalência.

Pergunta: Um commit de checkpoint deve ser apresentado como pronto?
Resposta: Não. Pode preservar progresso incompleto, desde que esse estado e as pendências sejam explícitos.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T236:C05 — mecanismo_avancado

O commit usual registra o índice, que pode diferir da árvore de trabalho onde os testes foram executados. Com staging parcial, um teste verde pode depender de alteração não incluída no commit. A proposta verifica o delta preparado e identifica a árvore efetivamente aceita. Uma etapa incompleta ainda pode ser salva como checkpoint, mas seu status deve permanecer distinto de entrega aprovada; mensagens de commit não substituem evidência de execução.

Condição de contorno:
Um commit coerente de código não captura automaticamente migração aplicada, dados externos ou configuração não versionada.

Contrato proposto:
- Entradas: Alterações da etapa, índice preparado, objetivo e evidências de verificação.
- Saídas: Commit identificado, descrição do comportamento e status de aceitação.
- Estado: Revisão-base, árvore do commit e arquivos fora do escopo.
- Invariante: A evidência de teste corresponde à árvore que o commit efetivamente registra.

Compromissos de projeto:
- Commits pequenos facilitam revisão e podem dividir uma mudança que só funciona integrada.
- Commits amplos preservam uma entrega conjunta e dificultam localizar causa de regressão.

## T236:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deixar no working tree uma correção necessária, mas fora do índice; exigir detecção de que o commit preparado não corresponde ao estado testado.

Plano de avaliação proposto:
Comparar etapas por arquivo e por mudança funcional em revisões independentes. Medir capacidade de reverter, reproduzir testes e localizar regressões. Definir tamanho pela coerência do comportamento, sem impor um número universal de linhas ou arquivos.

Comparações:
- T233 (complements): Validação deve ligar resultado testado à revisão publicada.
- T240 (distinct_from): Commit captura uma árvore Git e metadados; snapshot operacional pode precisar de outros estados.

Afirmação rastreável:
A documentação Git informa que o commit padrão contém o estado atual do índice.
Suporte: direct; fontes: V3C-S036
Limite: Outras opções alteram seleção de conteúdo; o contrato precisa registrar o modo efetivamente utilizado.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T236:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrava diferença entre índice e árvore testada. A expansão define commits como fronteiras de aceitação e recuperação, organiza histórico de etapas e explicita o que continua fora do versionamento do código.

Checkpoint e entrega distintos
Uma etapa pode salvar trabalho incompleto para recuperação, mas seu status deve declarar que falta validação. Um commit aprovado precisa apontar ao artefato testado e ao requisito atendido. Mensagem descritiva não substitui esses vínculos; use metadados ou manifesto associado quando o histórico de validação não cabe no próprio commit.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S036, V4C-S030.

Unidade revisável
Escolha commits por mudança coerente, evitando misturar reparo funcional, reformatação e atualização de documentação sem relação. Etapas pequenas ajudam bisect e revisão, mas uma sequência de commits quebrados pode dificultar recuperação. Defina se a campanha exige cada commit válido ou apenas pontos de integração explicitamente marcados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S021, V3C-S036.

Publicação e efeitos externos
Criar commit local não significa que foi integrado ou implantado. Registre branch, referência esperada e resultado da publicação; se a conexão cai, consulte a referência antes de repetir ações associadas. Migrações de banco, recursos criados e segredos fora do repositório precisam de ledger próprio, não de confiança na existência do commit.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, C-S026.

USO AVANÇADO — Campanha longa por módulos
Cenário: Um agente precisa preservar progresso sem entregar tudo de uma vez.
Estratégia: Depois de cada unidade coerente, valide o conteúdo preparado e salve commit com vínculo ao requisito. Integre apenas etapas aceitas; checkpoints incompletos ficam separados do fluxo de entrega. Na retomada, leia árvore e estado de validação, não apenas a última mensagem de commit.
Papel do modelo pequeno: 3–7B edita módulo; 8–14B prepara resumo factual; 15–30B coordena integração.
Aceite proposto: Proposta: recuperação por etapa sem perder trabalho e sem promover checkpoint incompleto por engano.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S036.

USO AVANÇADO — Revisão de alternativas
Cenário: Vários candidatos resolvem o mesmo requisito em branches distintas.
Estratégia: Identifique a árvore de cada candidato, execute testes e registre decisão de seleção. Se combinar commits, valide a composição resultante; dois commits aprovados isoladamente podem conflitar semanticamente. Preserve candidatos descartados pelo prazo necessário à auditoria e limpe recursos associados depois.
Papel do modelo pequeno: 15–30B compara tradeoffs; modelos menores geram alternativas delimitadas.
Aceite proposto: Proposta: rastrear a solução escolhida e reproduzir a árvore realmente validada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S037, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Commits por alteração local coerente, com revisão determinística do índice.
8–14B: Agrupar mudanças relacionadas e redigir mensagens ancoradas no diff real.
15–30B: Planejar sequência de integração e recuperar regressões sem depender de narrativa do histórico.
Requisitos de treino/runtime: Git configurado, índice inspecionado, testes sobre árvore preparada e identidade de referência publicada.
Não aplicar quando: Não usar git commit como snapshot completo do ambiente nem assumir que staging parcial preserva todas as dependências testadas.

## T236:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Changesets versionam alterações mas não são git commit.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C021 — Meta / Sapling — fluxo interno de commits
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Meta descreve Sapling utilizado no monorepo e pilhas de commits pequenos submetidos individualmente à revisão.
Mecanismo documentado: Ferramentas visualizam dependências e evolução de commits; operações de recuperação e revisão integram o fluxo de desenvolvimento.
Correspondência com esta base: A prática de etapas pequenas e revisadas é explícita, porém usa Sapling e não o comando Git commit.
Transferência proposta para modelo pequeno: Proposta: gerar mudanças 3–30B em dependências explícitas, validar cada etapa e revalidar descendentes quando a base mudar. A aplicação decide quando consolidar etapas para evitar fragmentação.
Limite: Sapling não é Git; a fonte informa diferenças como ausência de staging area. Um caso de versionamento, sem multiplicação por cada comando ou equipe.
Fontes: V4C-S021.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: Há commits e validação, mas não uma política de commit por etapa de agente.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: O sistema acompanha commits, mas não demonstra um agente criando commit por micro-missão.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C017 — GitHub / Microsoft / Copilot coding agent
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O anúncio documenta recurso que inicia ambiente GitHub Actions, consulta repositório, edita, valida e publica commits em draft PR.
Mecanismo documentado: A tarefa mantém vínculo com issue, sessão, repositório e mudanças; instruções e feedback da revisão alimentam novas alterações.
Correspondência com esta base: O agente publica mudanças como commits em draft PR.
Transferência proposta para modelo pequeno: Proposta: reproduzir a separação tarefa→checkout→patch→testes→revisão com um 3–30B, avaliando artefatos e custo em tarefas delimitadas. Implementar controles de publicação na aplicação, não no prompt.
Limite: Classificado operational_product: a página descreve recurso, não uma implantação identificada de cliente. Configurações e exigências de aprovação mudaram desde o anúncio.
Fontes: V4C-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Git documenta semântica; Windows Git, Sapling e Codex fornecem contextos operacionais distintos. Não foram contados como prova universal de commits validados a cada etapa.
Consultas registradas: V4C-Q015, V4C-Q016, V4C-Q027.

## T236:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T236 → T233 [complements]
Como combinar: Gate valida a árvore preparada antes de marcar o commit como aceito.
Interface: Tree ID, testes e requisito.
Condição: Conteúdo testado coincide com o commit.
Aceite proposto: Mudança fora do índice não sustenta teste aprovado do commit parcial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S036, V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T236 → R027 [complements]
Como combinar: Usar objetos e referências Git para identificar etapas e publicar condicionalmente.
Interface: Commit, pais e valor anterior esperado da ref.
Condição: Operação escolhida respeita semântica documentada.
Aceite proposto: Conflito de avanço da ref provoca reconciliação, não sobrescrita silenciosa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Commit criado não significa push, merge ou deploy concluído.
- Sapling e Scion são sistemas distintos; seus changesets não provam comportamento específico do índice Git.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare produtividade por etapa aceita e custo de integração com modelos diferentes. Histórico bem formado favorece recuperação de qualquer porte, mas não valida automaticamente a qualidade do código.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T233, T239, T240

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S036 — Git — git-commit

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Commit usual registra o índice; opções com paths e seleção parcial mudam quais alterações são incluídas.

Limite: Commit não captura por si arquivos ignorados, banco de dados, processos ou efeitos externos.

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

### V4C-S021 — Sapling: Source control that’s user-friendly and scalable

[https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Sapling, pilhas de commits revisados, histórico e diferenças em relação a Git.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
