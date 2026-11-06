# T045 — Tool Retrieval

**Nome canônico:** Tool Retrieval  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T045  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** descoberta de ferramentas; tool search

## T045:C01 — conceito

Busca ferramentas apropriadas em um catálogo e carrega seus schemas quando necessários. A recuperação seleciona capacidades; a execução continua sujeita a contrato e autorização. Descobrir uma ferramenta não autoriza usá-la nem prova que o serviço está disponível.

Como funciona:
- Indexar nome, descrição, entradas, saídas e restrições da ferramenta.
- Pesquisar pelo objetivo e selecionar candidatas.
- Carregar definição completa, validar argumentos e só então executar.

## T045:C02 — aplicacao

Quando usar:
- Catálogos extensos que não cabem economicamente no contexto.
- Sistemas com ferramentas especializadas de muitos serviços.

Quando não usar:
- Não ocultar a própria ferramenta de descoberta nem capacidades essenciais para recuperar o catálogo.

Implementação proposta:
- Proposta: manter versões e exemplos de intenção nos metadados.
- Aplicar filtros de permissão antes de apresentar candidatos.
- Testar descoberta por paráfrases e diferenciação de ferramentas com nomes parecidos.

Aplicação LAI proposta:
Proposta LAI: oferecer à Helena catálogo de capacidades e carregar contratos específicos antes da chamada; manter separadas descoberta, autorização e execução.

## T045:C03 — riscos_validacao

Armadilhas:
- Descrição vaga faz a ferramenta correta parecer irrelevante.
- Recuperar schema antigo pode gerar argumentos incompatíveis.

Métricas sugeridas:
- Recall de ferramentas adequadas por tarefa.
- Tokens de schemas carregados e chamadas inválidas.

Testes propostos:
- Pedir uma operação sem mencionar o nome da ferramenta e avaliar seleção.
- Revogar permissão e garantir que a ferramenta não seja executada por ter sido recuperada anteriormente.

## T045:C04 — perguntas_proveniencia

Pergunta: Tool retrieval é apenas busca vetorial?
Resposta: Não. Busca lexical, filtros, regras e combinações também podem servir.

Pergunta: Ferramentas adiadas precisam existir no servidor?
Resposta: Sim. Adiar o schema no contexto não cria uma implementação nem elimina requisitos do provedor.

Pergunta: Resultado vazio significa que a capacidade não existe?
Resposta: Significa ausência de correspondência nessa busca. Descrição ruim, filtro ou consulta inadequada também podem ocultar uma ferramenta existente.

Pergunta: A referência pode substituir o schema para sempre?
Resposta: Não. Ela precisa ser resolvida por um contrato compatível. Sua existência não garante versão, permissão ou disponibilidade da implementação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T045:C05 — mecanismo_avancado

Adiar uma ferramenta no contexto não significa remover sua definição do transporte ao servidor. Na implementação documentada pela Anthropic, o catálogo completo continua no parâmetro de ferramentas; a busca devolve referências expandidas para o modelo. Assim, economia de contexto e redução de bytes enviados são métricas distintas. O mecanismo também precisa diferenciar busca sem correspondência, falha da busca e ferramenta descoberta mas indisponível.

Condição de contorno:
Quando o catálogo é pequeno e quase todas as ferramentas serão usadas, o custo e a latência de descoberta podem superar a economia na janela.

Contrato proposto:
- Entradas: Catálogo completo e versionado, consulta de capacidade e restrições da sessão.
- Saídas: Referências resolvíveis e schemas compatíveis, ou resultado explícito de ausência ou falha.
- Estado: Ferramentas já carregadas, versão do catálogo e disponibilidade verificada no momento da chamada.
- Invariante: Um nome recuperado só pode ser executado com definição conhecida e validação vigente de argumentos.

Compromissos de projeto:
- Carregar poucas ferramentas reduz competição de descrições e introduz uma etapa adicional.
- Preservar o catálogo completo no servidor simplifica resolução, mas mantém custos de transporte e governança do catálogo.

## T045:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover uma definição mantendo sua referência em resultados antigos. A chamada deve detectar a incompatibilidade; não deve inventar parâmetros nem substituir por ferramenta parecida.

Plano de avaliação proposto:
Avaliação proposta: comparar catálogo integral e descoberta com tarefas de uma e várias ferramentas. Medir recall de capacidade, tentativas inválidas, tokens ativos, bytes transmitidos e latência; separar erro de seleção de indisponibilidade do serviço.

Comparações:
- T014 (specializes): A ferramenta é uma unidade específica de carregamento progressivo com schema executável.
- T015 (complements): Referências economizam representação somente quando o resolvedor pode obter a definição correspondente.

Afirmação rastreável:
Tool search retorna referências que a API expande; definições adiadas continuam incluídas no catálogo enviado nas requisições.
Suporte: direct; fontes: A-S038
Limite: Esse contrato pertence à implementação documentada da Anthropic; um catálogo customizado pode usar transporte e expansão diferentes.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T045:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu schemas adiados. Aqui busca de ferramentas é avaliada como descoberta de capacidade e compatibilidade operacional.

Projeto e decomposição
Indexe finalidade, entradas necessárias, efeitos e limites. Nome parecido não basta: ferramenta de consultar e ferramenta de modificar podem atender palavras iguais com consequências diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

Controle adaptativo
Depois da recuperação, valide que argumentos disponíveis satisfazem schema e que capacidade está habilitada. Se faltar dado obrigatório, coletá-lo antes de tentar chamada e reparo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

Validação contrafactual
Compare catálogo integral e recuperação em tarefas com ferramentas raras e versões concorrentes. Meça seleção correta, chamadas inviáveis e custo de carregar schemas não usados. Unidade de avaliação: seleção de ferramenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

USO AVANÇADO — Catálogo empresarial amplo
Cenário: Agente conhece intenção mas não ferramenta.
Estratégia: Recuperar poucas capacidades, comparar efeitos e pré-condições e carregar contrato completo da escolhida.
Papel do modelo pequeno: 3–7B roteia capacidades.
Aceite proposto: Nenhuma ferramenta de escrita deve ser escolhida para pedido apenas de leitura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

USO AVANÇADO — Ferramentas versionadas
Cenário: Dois schemas têm campos diferentes.
Estratégia: Resolver versão elegível, mapear argumentos a partir de dados observados e rejeitar preenchimento inventado.
Papel do modelo pequeno: 8–14B constrói chamada.
Aceite proposto: Chamada deve validar no schema efetivamente carregado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Selector de capacidades descritas por metadados contrastivos.
8–14B: Construtor de argumentos para poucas ferramentas elegíveis.
15–30B: Planejador de composição entre ferramentas quando dependências exigirem várias etapas.
Requisitos de treino/runtime: Registry versionado, filtros de disponibilidade e validação de argumentos; treino de tool use depende do modelo.
Não aplicar quando: Ferramenta não está disponível ou o catálogo não distingue efeitos e pré-condições.

## T045:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T045:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T045 → T158 [requires]
Como combinar: Recuperar somente capacidades registradas e habilitadas.
Interface: tool_id, versão, efeitos e disponibilidade.
Condição: Registry ser fonte autorizada do contrato.
Aceite proposto: Remover ferramenta e impedir chamada por lembrança do modelo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S038, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T045 → T170 [requires]
Como combinar: Fixar versão após descoberta.
Interface: Schema, revisão e compatibilidade dos argumentos.
Condição: Versão não mudar silenciosamente entre seleção e execução.
Aceite proposto: Alterar campo obrigatório e exigir revalidação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S038, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir busca sem resultado com catálogo vazio.
- Não executar a partir de descrição resumida quando schema falta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sucesso de chamada válida e seleção de efeitos; bom ranking textual não demonstra uso correto de ferramentas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T151, T158, T170

## Fontes primárias associadas

### A-S038 — Tool search tool

[https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas e carregamento adiado de schemas no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
