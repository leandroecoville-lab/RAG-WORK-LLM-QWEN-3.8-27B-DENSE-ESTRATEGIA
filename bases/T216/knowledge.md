# T216 — Repo Map / mapa do repositório

**Nome canônico:** Repo Map / mapa do repositório  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T216  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** repository map; repo map

## T216:C01 — conceito

Índice compacto do repositório que apresenta arquivos, símbolos e relações úteis para orientar uma alteração. Aider documenta mapas com classes, funções e assinaturas. O mapa oferece navegação e contexto estrutural; decisões sobre comportamento exigem leitura do código pertinente, dos contratos e dos testes.

Como funciona:
- Um extrator identifica símbolos e referências a partir de uma revisão conhecida.
- Um seletor prioriza partes relevantes para a tarefa, respeitando um orçamento de contexto.
- Links para caminhos e posições permitem recuperar a implementação quando uma hipótese precisa ser confirmada.

## T216:C02 — aplicacao

Quando usar:
- Repositórios grandes, investigação inicial, descoberta de pontos de extensão e identificação de dependentes de uma mudança.

Quando não usar:
- Como prova de que uma função faz o que seu nome sugere ou como representação completa de dependências dinâmicas.

Implementação proposta:
- Proposta: gerar o mapa a partir de uma revisão identificada e registrar versão do extrator.
- Incluir caminho, linguagem, símbolo, assinatura e origem da relação; excluir artefatos gerados quando não acrescentam informação.
- Atualizar arquivos alterados e remover símbolos apagados; marcar dados de outra revisão como potencialmente desatualizados.
- Combinar consulta ao mapa com leitura dirigida e rastreamento dos testes associados antes de editar.

Aplicação LAI proposta:
Proposta LAI: gerar um mapa por projeto e módulo, deixando cada agente expandir somente os arquivos necessários à sua micro-missão.

## T216:C03 — riscos_validacao

Armadilhas:
- Reflexão, configuração e chamadas construídas em runtime podem escapar à análise estática.
- Um mapa antigo aponta para símbolos inexistentes.
- Excesso de detalhes recria o problema de consumir todo o contexto.

Métricas sugeridas:
- Cobertura de símbolos; referências inválidas; tokens do mapa; leituras necessárias até encontrar o alvo correto.

Testes propostos:
- Renomear um símbolo em uma cópia e conferir atualização das referências.
- Consultar um fluxo com ligação dinâmica e verificar que o mapa admite cobertura incompleta.
- Confirmar que cada posição recuperada corresponde à revisão declarada.

## T216:C04 — perguntas_proveniencia

Pergunta: O mapa substitui a leitura do arquivo?
Resposta: Não. Ele ajuda a localizar o arquivo e suas conexões; a implementação e seus invariantes continuam sendo a evidência do comportamento.

Pergunta: Um grafo de chamadas é obrigatório?
Resposta: Não. Assinaturas e hierarquia de arquivos já ajudam. Relações adicionais devem ser usadas quando o extrator consegue produzi-las com precisão conhecida.

Pergunta: Posso editar apenas com assinatura vista no mapa?
Resposta: Somente quando o contrato é suficiente e confirmado; normalmente é preciso ler implementação, usos e condições relevantes.

Pergunta: Por que registrar a revisão do mapa?
Resposta: Porque arquivos, símbolos e linhas mudam; sem ela, uma referência aparentemente válida pode apontar para outra realidade.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T216:C05 — mecanismo_avancado

O repo map do Aider seleciona partes relevantes usando ranking de um grafo de arquivos e dependências sob orçamento de tokens. Isso fornece orientação estrutural, mas não identifica automaticamente o comportamento executado em tempo de execução. Imports dinâmicos, geração de código e configuração podem escapar do grafo estático. Um mapa ligado à revisão do repositório evita que nomes e posições antigos orientem uma edição sobre código já alterado.

Condição de contorno:
Símbolos centrais no grafo podem não ser os relevantes para um defeito localizado ou ativado por configuração rara.

Contrato proposto:
- Entradas: Revisão do repositório, arquivos indexáveis, símbolos e objetivo da navegação.
- Saídas: Mapa compacto, relações selecionadas e referências resolvíveis.
- Estado: Índice por linguagem, revisão analisada e critérios de ranking.
- Invariante: O mapa é uma representação de uma revisão identificada, não autoridade sobre código que não foi lido.

Compromissos de projeto:
- Mapas amplos ajudam orientação inicial e consomem janela com relações pouco úteis.
- Ranking focado melhora densidade e pode esconder caminhos raros de execução.

## T216:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mover uma função, atualizar o repositório e manter mapa antigo; exigir detecção da revisão divergente antes de usar a posição para editar.

Plano de avaliação proposto:
Comparar navegação por busca textual, mapa e combinação de ambos em tarefas independentes. Medir leituras até localizar o trecho correto, cobertura de dependências e alterações em lugar errado. Separar tarefas estáticas de casos dependentes de configuração.

Comparações:
- T238 (complements): O mapa indica onde ler; faixas de linhas fornecem o conteúdo necessário à decisão.
- T232 (complements): Metadados sintáticos podem enriquecer referências sem provar comportamento dinâmico.

Afirmação rastreável:
Aider documenta seleção do repo map por ranking de um grafo de arquivos e dependências dentro de orçamento ativo.
Suporte: direct; fontes: V2A-S007
Limite: O grafo e o ranking são mecanismos de orientação; não equivalem a análise completa de fluxo em execução.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T216:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicava ranking de símbolos e limites do grafo estático. A expansão usa o mapa para formular leituras direcionadas, verifica sua validade incremental e combina estrutura de código com evidência de execução.

Mapa orienta, arquivo decide
Inclua símbolos, caminhos e relações suficientes para localizar candidatos, mas confirme conteúdo atual antes de editar. Nomes centrais podem ser irrelevantes para a falha; arquivos raros ativados por configuração podem ser decisivos. Use o mapa como índice de hipóteses de localização, sem tratá-lo como descrição completa do comportamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S026.

Atualização por mudança
Uma edição pode alterar assinatura, import ou relação de dependência. Marque partes afetadas do mapa e regenere o índice correspondente antes de delegar nova tarefa. Um mapa ligado ao commit original pode continuar útil para explicar o passado, mas não deve orientar substituição textual em uma revisão posterior sem revalidação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V3C-S027.

Estrutura e execução
Combine símbolos estáticos com trace, teste ou configuração que indique o caminho realmente exercitado. Não acrescente todo o runtime ao mapa: mantenha camadas consultáveis por finalidade. O modelo pequeno recebe uma trilha curta de arquivos e a evidência que justificou cada leitura, reduzindo busca ampla sem ocultar alternativas relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V4C-S029.

USO AVANÇADO — Defeito em monorepo
Cenário: O agente precisa localizar a implementação entre muitos módulos.
Estratégia: Comece por ponto de entrada e símbolo provável, leia interfaces e siga chamadores ou consumidores relevantes. Se o teste aponta para código gerado ou import dinâmico, abandone a hipótese puramente estática e examine geração e configuração. Atualize a trilha de evidência após cada descoberta.
Papel do modelo pequeno: 3–7B lê funções curtas; 8–14B navega dependências; 15–30B resolve ligações transversais.
Aceite proposto: Proposta: localizar o arquivo correto com menos leituras, sem perder defeitos ativados por configuração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S026.

USO AVANÇADO — Delegação por módulo
Cenário: Vários agentes editam partes independentes do projeto.
Estratégia: Forneça mapa global curto e mapa local da revisão atribuída. Defina símbolos compartilhados que não podem mudar sem coordenação. Ao integrar, regenere relações afetadas e verifique se todos os consumidores continuam compatíveis.
Papel do modelo pequeno: 8–14B executa módulos; integrador maior usa o mapa para escolher testes de fronteira.
Aceite proposto: Proposta: nenhum uso de assinatura obsoleta e custo de atualização menor que reconstrução desnecessária do mapa inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Contexto local com assinatura e poucas relações; evitar mapas enormes que só repetem nomes.
8–14B: Navegação entre arquivos e seleção de leituras baseada em dependências explícitas.
15–30B: Análise de impacto entre módulos, com confirmação em código e testes.
Requisitos de treino/runtime: Índice por revisão, extração de símbolos confiável e acesso ao conteúdo atual dos arquivos.
Não aplicar quando: Não editar somente a partir do mapa nem presumir que análise estática captura configuração e geração dinâmica.

## T216:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Aider documenta repo map; relatos internos mostram navegação assistida, mas não foram convertidos em adoções exatas do algoritmo de ranking do Aider.
Consultas registradas: V4C-Q023, V4C-Q024, V4C-Q027.

## T216:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T216 → T238 [feeds]
Como combinar: Transformar caminhos e símbolos do mapa em pedidos de leitura de trechos relevantes.
Interface: Arquivo, revisão, símbolo e intervalo a resolver.
Condição: Posições são recalculadas ou validadas contra o conteúdo atual.
Aceite proposto: Leitura inclui contexto suficiente para a alteração pretendida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S033. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T216 → T213 [complements]
Como combinar: Usar relações estruturais para escolher unidades com baixo acoplamento e interfaces explícitas.
Interface: Subgrafo de módulos e símbolos compartilhados.
Condição: Critérios de aceite cobrem as fronteiras entre unidades.
Aceite proposto: Integração detecta consumidores omitidos pelo mapa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S033, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mapas muito compactos podem ocultar a única relação necessária ao diagnóstico.
- A centralidade no grafo não substitui evidência de que o código participa do comportamento defeituoso.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare localização e reparo com mapa, busca textual e modelo de fronteira sob o mesmo acesso ao repositório. Redução de leitura não demonstra compreensão completa do sistema.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T238, T222, T213

## Fontes primárias associadas

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

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

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
