# R021 — OpenAI Codex

**Nome canônico:** OpenAI Codex — agente e CLI de programação  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R021  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Codex CLI; codex exec

## R021:C01 — conceito

OpenAI Codex oferece um agente de programação capaz de inspecionar arquivos, editar código e executar comandos no ambiente autorizado. Esta ficha enfatiza a CLI e sua automação documentada. Codex é o produto e seu ciclo de ferramentas; o modelo configurado, a sessão e o estado do repositório são elementos diferentes que precisam ser registrados.

Como funciona:
- A CLI compõe contexto do projeto e ferramentas com chamadas de modelo; arquivos AGENTS.md fornecem instruções descobertas por escopo.
- codex exec executa uma tarefa sem interface interativa; a opção --json produz eventos JSONL, incluindo conclusão e falha de turno.
- Uma sessão pode ser retomada por identificador explícito, preservando vínculo com a execução anterior sem substituir a verificação do código atual.

Nota de nomenclatura: A documentação consultada informa que --full-auto deixou de ser suportado; não reutilizar flags antigas sem conferir a CLI. Não fixa modelo, plano ou versão instalada.

## R021:C02 — aplicacao

Quando usar:
- Investigação, implementação e revisão de mudanças em repositórios com requisitos e testes claros.
- Pipelines que precisam consumir eventos e artefatos de uma tarefa de programação delimitada.

Quando não usar:
- Para considerar uma mensagem final ou um turno concluído como prova suficiente de aceitação do software.

Implementação proposta:
- Proposta: conferir a CLI instalada, instruções aplicáveis, modelo, diretório e permissões necessárias à missão.
- Usar execução não interativa com registro de eventos, ID de sessão, revisão Git inicial e artefatos produzidos.
- Definir critérios de aceite externos; retomar pelo ID correto, reler mudanças concorrentes e limitar tentativas sem progresso.

Aplicação LAI proposta:
Proposta LAI: integrar Codex como executor de missões de programação com eventos estruturados, mantendo aceitação e continuidade sob controle verificável da aplicação.

## R021:C03 — riscos_validacao

Armadilhas:
- Usar a sessão mais recente em trabalhadores paralelos pode retomar a missão errada; preferir identificação explícita.
- Instruções de projeto não substituem controles de execução; configurações e flags mudam entre versões.

Métricas sugeridas:
- Tarefas aceitas, regressões, custo por alteração, tentativas, falhas de ferramentas e rastreabilidade entre sessão e commit.

Testes propostos:
- Proposta: executar um reparo reproduzível em checkout isolado e verificar testes e diff independentemente da mensagem final.
- Simular duas sessões concorrentes e interrupção; confirmar que a retomada utiliza a missão, o diretório e o estado esperados.

## R021:C04 — perguntas_proveniencia

Pergunta: codex exec cria um serviço durável de workflow?
Resposta: Não por si só. Ele executa a tarefa; persistência operacional, reconciliação e política de retomada precisam de desenho próprio.

Pergunta: Qual evidência comprova a correção?
Resposta: Resultados de verificações relevantes e o estado dos artefatos, vinculados à revisão analisada; a declaração do agente sozinha não basta.

Pergunta: Um evento item.completed encerra necessariamente a tarefa?
Resposta: Não. Concluir um item não substitui o status do turno e a verificação externa dos artefatos.

Pergunta: Por que evitar a sessão implicitamente mais recente?
Resposta: Execuções paralelas podem tornar a escolha ambígua; registre e retome o identificador da missão.

Escopo das fontes:
A inspeção do workspace não localizou CLI ou código local do Codex. Foram lidas páginas oficiais da OpenAI, incluindo redirecionamentos para ChatGPT Learn. Os passos de integração e testes são propostas; nenhuma execução Codex foi realizada.

## R021:C05 — mecanismo_avancado

Na automação do Codex, eventos e resposta final têm contratos distintos. --json produz eventos JSONL; --output-schema define o schema da resposta final, não a validação de todos os eventos. O consumidor distingue itens intermediários, conclusão e falha de turno, preservando eventos desconhecidos para diagnóstico em mudanças de versão. Retomar por ID identifica a conversa; o controlador ainda precisa associá-la ao diretório e à revisão de trabalho. A descoberta de AGENTS.md segue escopos e limites documentados: existir um arquivo no repositório não prova que entrou no contexto daquela execução.

Condição de contorno:
Interromper o processo pode deixar artefatos sem resposta final. Texto válido em stdout não demonstra que o turno ou a tarefa foram aceitos.

Contrato proposto:
- Entradas: Versão da CLI, sessão explícita, diretório, revisão Git, schema final e política de ferramentas.
- Saídas: Log de eventos, resposta final quando disponível e manifesto dos arquivos produzidos.
- Estado: Último evento persistido, status terminal, instruções carregadas e revisão verificada.
- Invariante: Artefatos e evidências ficam vinculados à sessão e ao conteúdo analisado; eventos intermediários não definem sucesso.

Compromissos de projeto:
- JSONL permite acompanhamento incremental, mas exige parser tolerante a evolução e interrupções.
- Schema final facilita integração, porém não comprova correção das mudanças ou completude dos testes.

## R021:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: encerrar uma execução após alteração de arquivo e antes do evento terminal. Exigir estado incompleto; retomar por ID e revalidar a revisão antes de aceitar o resultado.

Plano de avaliação proposto:
Comparar parser incremental com leitura da resposta final em traços controlados de sucesso, falha e truncamento. Medir classificações incorretas, perda de eventos e rastreabilidade; exigir identificação inequívoca do término.

Comparações:
- T235 (complements): O controlador headless transforma eventos e artefatos do executor em estado persistente da missão.
- R027 (complements): A revisão Git identifica o conteúdo; a sessão identifica a conversa e não substitui esse vínculo.

Afirmação rastreável:
--output-schema especifica o formato da resposta final; --json disponibiliza eventos separados em JSONL.
Suporte: direct; fontes: V3C-S039
Limite: A CLI não foi localizada no PATH nesta pesquisa; a análise documental não valida flags em instalação local.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R021:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda os contratos de automação com isolamento reproduzível por tarefa, verificação do artefato final e observabilidade que permite localizar onde o agente perdeu o requisito.

Ambiente identificável
Proposta: associar cada execução a revisão de código, configuração de ferramentas e conjunto de testes. Isolar diretório e recursos por tarefa evita que um resultado aprovado em um ambiente seja atribuído ao código de outro trabalhador. Isso exige controle além da conversa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

Evidência para o agente
Instrumentar comandos e testes com resultados concisos e referências ao trace completo. Dar ao modelo acesso sob demanda à falha relevante reduz a necessidade de despejar logs. A evidência precisa dizer o que foi executado, sobre qual artefato e qual condição falhou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

Conclusão composta
Tratar finalização do turno, término do processo, criação do patch e aceite como estados diferentes. A resposta final é uma declaração do agente; o controlador decide conclusão usando artefato e verificações. Se o processo termina antes do relatório, o resultado permanece desconhecido até reconciliação local.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

USO AVANÇADO — Fila de correções independentes
Cenário: Vários bugs podem ser trabalhados em paralelo.
Estratégia: Criar ambiente por tarefa, limitar ferramentas e integrar somente a revisão que passou pelos testes registrados.
Papel do modelo pequeno: No harness próprio, modelo pequeno resolve alteração local; integração continua externa.
Aceite proposto: Nenhum worker modifica base de outro; a árvore integrada é verificada novamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

USO AVANÇADO — Falha de teste com log enorme
Cenário: O agente precisa interpretar uma regressão localizada.
Estratégia: Extrair sumário determinístico e permitir leitura da seção relevante por referência.
Papel do modelo pequeno: 3–14B classifica causa provável e propõe próximo experimento curto.
Aceite proposto: O teste confirmatório diferencia a hipótese de causas alternativas antes de alterar código.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: transferir contratos de ferramenta e evidência ao próprio harness; não equiparar o modelo ao produto Codex.
8–14B: 8–14B: tarefas locais com ambiente reproduzível e execução real de testes.
15–30B: 15–30B: mudanças maiores somente quando orçamento, ferramentas e resultados justificarem.
Requisitos de treino/runtime: Suporte a modelo/backend é propriedade da versão instalada; a ficha não garante compatibilidade de qualquer 3–30B.
Não aplicar quando: Não concluir sucesso apenas porque houve evento final ou JSON válido.

## R021:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C029 — OpenAI / Codex no desenvolvimento interno e harness beta
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Uso diário por equipes e beta interno com usuários reais relatados em duas publicações do operador.
Mecanismo documentado: Código e planos no repositório, aplicação e observabilidade por worktree, ferramentas de revisão e restrições estruturais executáveis.
Correspondência com esta base: Uso interno de Codex confirmado pelo operador.
Transferência proposta para modelo pequeno: Proposta: reproduzir tarefas pequenas com a mesma infraestrutura de testes e isolamento usando 3–30B; medir custo completo, inclusive supervisão e revisão.
Limite: Consolidado para evitar somar equipes e artigos como adoções independentes. Beta operacional não é prova de autonomia geral; modelos do relato não são demonstrados como 3–30B.
Fontes: V4C-S029, V4C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Relatos OpenAI de uso interno e harness foram consolidados num caso. São referência de sistema real, sem demonstração de paridade de uma LLM pequena.
Consultas registradas: V4C-Q027.

## R021:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R021 → T239 [complements]
Como combinar: Associar cada tarefa a área de trabalho e base verificáveis.
Interface: Task_id, worktree, commit-base e recursos isolados.
Condição: Trabalhadores podem editar simultaneamente.
Aceite proposto: Os testes e o patch referem-se à mesma base e ao mesmo trabalhador.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R021 → T195 [feeds]
Como combinar: Produzir artefato verificável e solicitar execução real do critério.
Interface: Patch, comandos, ambiente e resultados observados.
Condição: Há critério executável para a mudança.
Aceite proposto: Aceite é derivado do resultado registrado, não da narrativa do agente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S029, V4C-S030, V3C-S039, V2A-S005. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contabilizar testes descritos como se tivessem sido executados.
- Não afirmar que ambiente isolado elimina dependências externas compartilhadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sistemas na mesma revisão e infraestrutura, registrando tentativas e intervenção humana. O padrão de harness pode ser transferível sem reproduzir capacidades do modelo de referência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T217, T218, T234, T235, T236, T239, R027

## Fontes primárias associadas

### V2B-S013 — Codex CLI

[https://learn.chatgpt.com/docs/codex/cli](https://learn.chatgpt.com/docs/codex/cli)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Inspeção, edição e execução de código no terminal; configuração e composição com scripts.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V2B-S014 — Non-interactive mode

[https://learn.chatgpt.com/docs/non-interactive-mode](https://learn.chatgpt.com/docs/non-interactive-mode)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: codex exec, eventos JSONL, identificação e retomada de sessão, configuração explícita e remoção de --full-auto.

Limite: Página oficial consultada após redirecionamento de developers.openai.com. CLI e código Codex não estavam disponíveis no workspace; comandos não foram executados.

### V2B-S015 — Custom instructions with AGENTS.md

[https://learn.chatgpt.com/docs/agent-configuration/agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta e precedência de instruções globais e de projeto no início da execução.

Limite: Documentação primária consultada nesta data; compatibilidade depende de versão, modelo e ambiente. Nenhuma implantação ou avaliação LAI foi executada.

### V3C-S039 — Codex CLI — Command line options

[https://learn.chatgpt.com/docs/cli/reference](https://learn.chatgpt.com/docs/cli/reference)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Interfaces de execução não interativa, eventos JSONL, resposta final com schema e retomada de sessão.

Limite: Codex não foi encontrado no PATH local; análise documental, sem execução da CLI ou teste de suas opções.

### V2A-S005 — Non-interactive mode

[https://developers.openai.com/codex/noninteractive/](https://developers.openai.com/codex/noninteractive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução programática do Codex, retomada de sessão e resultados consumíveis por automações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S017 — Custom instructions with AGENTS.md

[https://developers.openai.com/codex/guides/agents-md/](https://developers.openai.com/codex/guides/agents-md/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta hierárquica de instruções de projeto pelo Codex e limites de carregamento.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

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
