# R020 — Claude Code

**Nome canônico:** Claude Code — agente de programação da Anthropic  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R020  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Claude Code CLI; claude -p

## R020:C01 — conceito

Claude Code é um agente de programação da Anthropic que inspeciona código, edita arquivos e executa ferramentas no ambiente disponível. Sua CLI também permite execução não interativa. A continuidade combina histórico de sessão, instruções de projeto e memória; esses mecanismos não equivalem a executar indefinidamente nem a comprovar que uma tarefa foi concluída.

Como funciona:
- O ciclo de trabalho usa ferramentas para ler, alterar e verificar o projeto, alimentando o modelo com os resultados.
- Arquivos de instruções e auto memory carregam contexto entre sessões; a documentação distingue contexto de configuração efetivamente imposta.
- A execução por claude -p oferece saídas consumíveis por scripts e opções explícitas de ferramentas e continuidade.

Nota de nomenclatura: Não houve instalação, autenticação ou execução real do Claude Code. A ficha não fixa modelo, plano ou compatibilidade local.

## R020:C02 — aplicacao

Quando usar:
- Implementação, investigação de defeitos e revisão em repositórios com comandos de validação conhecidos.
- Automação limitada por tarefa quando um controlador acompanha resultado, custo e término.

Quando não usar:
- Como substituto de um workflow durável ou de verificação independente de mudanças e efeitos externos.

Implementação proposta:
- Proposta: registrar versão, modelo, diretório de trabalho e política de ferramentas antes de uma missão.
- Manter instruções curtas sobre arquitetura e testes; passar evidências e escopo da mudança de forma explícita.
- Em automação, capturar saída estruturada, status de término e artefatos; validar o diff e os testes antes da próxima etapa.

Aplicação LAI proposta:
Proposta LAI: usar Claude Code como referência de executor de programação, mantendo o controlador de continuidade e os verificadores da Helena separados do histórico conversacional.

## R020:C03 — riscos_validacao

Armadilhas:
- Instruções em Markdown orientam o modelo, mas não impõem uma barreira operacional; controles precisam existir na execução.
- Retomar a conversa não garante que arquivos, dependências e serviços continuam iguais aos vistos anteriormente.

Métricas sugeridas:
- Tarefas aceitas, regressões, chamadas de ferramenta, custo por correção e progresso verificável por tentativa.

Testes propostos:
- Proposta: resolver um defeito reproduzível em checkout de teste e comparar o patch com critérios de aceite.
- Interromper e retomar a tarefa após mudar um arquivo; conferir releitura do estado e ausência de operações repetidas indevidamente.

## R020:C04 — perguntas_proveniencia

Pergunta: Memória de projeto garante cumprimento de regras?
Resposta: Não. Ela fornece contexto; restrições obrigatórias precisam ser verificadas por controles e ferramentas apropriados.

Pergunta: Modo headless garante recuperação após queda?
Resposta: Não por si só. O controlador precisa registrar execução, artefatos e estado confirmado para decidir como retomar.

Pergunta: Restaurar a conversa restaura o código?
Resposta: A ação permite conservar o código; os dois estados devem ser selecionados e verificados separadamente.

Pergunta: Um checkpoint listado garante arquivos recuperáveis?
Resposta: Não. Snapshots podem ter sido removidos; é necessário conferir disponibilidade e resultado da restauração.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R020:C05 — mecanismo_avancado

O checkpoint de Claude Code tem escopo de sessão e distingue restauração de código, conversa ou ambos. Resumir a conversa não altera arquivos. Há uma diferença operacional no rastreamento: após a ferramenta de edição tocar um arquivo, mudanças posteriores por Bash nesse arquivo podem ser desfeitas; um arquivo modificado somente por Bash permanece fora desse rastreamento. Edições de subagentes têm regras específicas de execução e de arquivos já acompanhados, portanto não cabem na suposição de restauração integral. O controlador deve registrar o conjunto coberto antes de usar rewind como recuperação.

Condição de contorno:
Snapshots sujeitos à retenção podem desaparecer. Caminhos simbólicos ou hard links são ignorados pela restauração documentada; efeitos em bancos não pertencem ao checkpoint.

Contrato proposto:
- Entradas: ID da sessão, checkpoint escolhido, escopo de restauração e inventário de arquivos e efeitos.
- Saídas: Código e/ou conversa restaurados, com lista de caminhos preservados ou ignorados.
- Estado: Snapshots disponíveis, arquivos rastreados e revisão Git anterior à tentativa.
- Invariante: A recuperação só declara concluído o escopo cuja restauração foi conferida por conteúdo.

Compromissos de projeto:
- Rewind facilita experimentar alternativas, mas sua cobertura depende de como cada alteração ocorreu.
- Restaurar só a conversa conserva trabalho útil, porém pode deixar o modelo sem explicação das mudanças atuais.

## R020:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: editar um arquivo pela ferramenta e outro apenas por Bash; executar mudança externa. Restaurar código e conferir hashes: exigir cobertura documentada e reconciliação separada do efeito externo.

Plano de avaliação proposto:
Comparar rewind e reconstrução por revisão Git em cenários equivalentes. Medir arquivos recuperados, alterações remanescentes e tempo de retomada; escolher o mecanismo conforme o escopo exigido.

Comparações:
- T240 (distinct_from): Snapshot genérico precisa definir cobertura; o checkpoint do produto cobre apenas o estado documentado da sessão.
- R027 (complements): Git mantém histórico versionado de código independente da retenção dos checkpoints da conversa.

Afirmação rastreável:
Arquivo alterado somente por Bash não é rastreado; alterações por Bash em arquivo previamente editado pela ferramenta podem ser restauradas.
Suporte: direct; fontes: V3C-S030
Limite: Regras consultadas nesta data; não afirmar que todos os subagentes ou tipos de arquivo têm cobertura idêntica.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R020:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda o uso de Claude Code como referência de engenharia: medir contaminação da memória de projeto, perda de obrigações na compactação e qualidade dos limites de delegação.

Memória por evidência
Proposta para harness próprio: cada orientação persistida distingue fato do repositório, preferência e hipótese. Vincular instruções derivadas de código à revisão observada e revalidá-las quando arquivos relevantes mudarem. A memória deixa de ser um depósito de conclusões que se perpetuam sem teste.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

Compactação com obrigações
Antes de compactar, extrair condições de aceite, decisões pendentes, efeitos confirmados e artefatos por hash. Depois, executar uma recuperação de obrigações numa tarefa de controle. Texto menor só é melhoria se preservar os compromissos que governam a próxima ação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

Delegação e retorno mínimo
Definir tarefa, arquivos permitidos, budget e formato de evidência antes de criar um trabalhador. O retorno inclui achado, fonte e incerteza; não concatena toda a sessão. O integrador precisa verificar conflitos de base e qualidade do resultado, mesmo quando o subagente afirma ter concluído.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

USO AVANÇADO — Diagnóstico assistido de incidente
Cenário: Logs extensos e muitas hipóteses competem por contexto.
Estratégia: Separar coleta, teste de hipótese e alteração; manter trace e comando que sustenta cada achado.
Papel do modelo pequeno: Um trabalhador pequeno pode extrair padrões; autorização e execução permanecem no controlador.
Aceite proposto: Hipótese só vira fato depois de evidência reproduzível; medir falsas conclusões e tempo até diagnóstico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

USO AVANÇADO — Sessão longa de manutenção
Cenário: Múltiplas subtarefas atravessam compactações.
Estratégia: Persistir obrigações e estado por módulo; retomar lendo artefatos atuais antes de editar.
Papel do modelo pequeno: No harness próprio, leitor 8–14B recompõe contexto local sob schema.
Aceite proposto: Após compactação, recuperar todos os aceites ainda abertos sem restaurar histórico irrelevante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: aplicar padrões de localização e extração em harness compatível; não se afirma suporte do Claude Code a qualquer modelo pequeno.
8–14B: 8–14B: reproduzir contratos de memória/retomada no próprio sistema, com validação externa.
15–30B: 15–30B: avaliar integração de subtarefas; não presumir reprodução da qualidade dos modelos Claude.
Requisitos de treino/runtime: Separar aprendizado arquitetural de disponibilidade comercial e de backends documentados do produto.
Não aplicar quando: Não usar rewind como rollback universal de banco, rede ou arquivos não cobertos.

## R020:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C025 — Anthropic / Claude Code em equipes internas
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Equipes internas usam Claude Code em repositórios, testes e diagnóstico de incidentes.
Mecanismo documentado: Leitura de instruções locais e código, testes executáveis, revisão de propostas e loops de implementação em tarefas delimitadas.
Correspondência com esta base: O operador descreve uso de Claude Code.
Transferência proposta para modelo pequeno: Proposta: delegar localização e testes focados a 3–30B, mantendo execução real e revisão de mudanças como critérios.
Limite: Consolidado como um caso de adoção interna, sem multiplicar equipes; não demonstra equivalência de modelos pequenos.
Fontes: V4C-S026.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Medições incluem sessões Claude Code, sem demonstrar todos os recursos do produto.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Casos de uso interno Anthropic e medições Uber foram identificados. Uma equipe, um recurso e uma fonte adicional do mesmo produto não foram multiplicados como implantações independentes.
Consultas registradas: V4C-Q024.

## R020:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R020 → T234 [complements]
Como combinar: Versionar instruções persistidas junto de sua evidência e escopo.
Interface: Regra, módulo, revisão de origem e condição de revalidação.
Condição: Conhecimento de projeto é reutilizado entre sessões.
Aceite proposto: Regra obsoleta é detectada antes de orientar uma alteração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R020 → T212 [complements]
Como combinar: Compactar somente com registro explícito de obrigações e artefatos.
Interface: Pacote de retomada com pendências e hashes.
Condição: A sessão atinge orçamento de contexto.
Aceite proposto: A retomada conserva os aceites ativos e não inventa conclusão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S026, V2A-S025, V3C-S030, V4C-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar uso interno de Claude Code como evidência de modelos 3–30B.
- Não promover automaticamente anotações de subagente a instruções permanentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar o padrão de harness no modelo pequeno com execução de referência na mesma tarefa, distinguindo diferenças de ferramentas, permissões e infraestrutura.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T217, T218, T234, T235, T237, T239, R027

## Fontes primárias associadas

### V2B-S010 — Claude Code overview

[https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Agente de programação com leitura, edição, comandos, integração Git e opções de automação.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S011 — How Claude remembers your project

[https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Instruções de projeto e auto memory; distinção entre conteúdo contextual e controles impostos na execução.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S012 — Run Claude Code programmatically

[https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução não interativa com claude -p, opções de saída e continuidade, códigos de término e diferenças entre modos.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V3C-S030 — Claude Code — Checkpointing

[https://code.claude.com/docs/en/checkpointing](https://code.claude.com/docs/en/checkpointing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointing distingue restauração de código, conversa e sumarização; escopo de arquivos e retenção são limitados.

Limite: Documentação consultada em 2026-11-05; não extrapolar cobertura para estado externo, todas as ferramentas ou outras versões.

### V2A-S018 — Create custom subagents

[https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subagentes com contexto próprio, capacidades delimitadas e retorno de resultados ao agente principal.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
