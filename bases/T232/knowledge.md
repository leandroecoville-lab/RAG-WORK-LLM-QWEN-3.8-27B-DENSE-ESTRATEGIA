# T232 — AST Editing

**Nome canônico:** AST Editing  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T232  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** structural editing; codemod; CST Editing

## T232:C01 — conceito

Transformação de código por sua estrutura sintática, como nós de funções, chamadas ou declarações. Uma árvore abstrata de sintaxe, AST, pode omitir comentários e detalhes de formatação. Ferramentas de árvore concreta, CST, como LibCST para Python, preservam esses elementos e são úteis para mudanças estruturais com fidelidade textual.

Como funciona:
- O parser converte código em nós e relações estruturais.
- Um transformador seleciona nós por critérios explícitos e modifica propriedades definidas.
- A serialização reconstrói o código, seguido de análise sintática e verificação semântica adequada ao caso.

## T232:C02 — aplicacao

Quando usar:
- Migrações repetitivas de APIs, inserção de argumentos e refatorações que exigem compreender a estrutura do código.

Quando não usar:
- Assumir que uma transformação sintática conhece automaticamente resolução de nomes, comportamento dinâmico ou contratos externos.

Implementação proposta:
- Proposta: escolher parser compatível com a linguagem e versão do projeto.
- Definir o padrão estrutural alvo e condições de exclusão, incluindo escopo e importações quando necessários.
- Usar análise de bindings para distinguir símbolos homônimos; marcar casos dinâmicos para revisão.
- Transformar uma cópia, reanalisar o resultado e inspecionar o diff.
- Executar exemplos positivos, negativos e verificações do comportamento afetado antes de ampliar a migração.

Aplicação LAI proposta:
Proposta LAI: preparar codemods limitados por linguagem e padrão, com amostragem revisável e exceções explícitas para casos que a análise estrutural não resolve.

## T232:C03 — riscos_validacao

Armadilhas:
- Renomear por nome de nó pode atingir variáveis locais sem relação com a API.
- ASTs podem perder comentários importantes.
- Sintaxe válida não demonstra equivalência funcional nem compatibilidade de versões.

Métricas sugeridas:
- Alvos transformados; falsos alvos; alterações de formatação; arquivos que não parseiam; regressões por padrão migrado.

Testes propostos:
- Criar duas funções homônimas em escopos diferentes e transformar somente a pretendida.
- Verificar preservação de comentários quando essa propriedade for exigida.
- Aplicar novamente a transformação para testar idempotência, quando esse for o contrato desejado.
- Incluir uma chamada dinâmica e exigir indicação de cobertura incompleta.

## T232:C04 — perguntas_proveniencia

Pergunta: AST Editing e CST Editing são iguais?
Resposta: Não. Ambas operam sobre estrutura, mas a representação concreta retém detalhes textuais que uma AST frequentemente descarta.

Pergunta: Uma refatoração por AST dispensa testes?
Resposta: Não. Ela melhora a precisão da seleção sintática, mas não prova que os consumidores e efeitos do código preservam o comportamento esperado.

Pergunta: Uma árvore sintaticamente válida prova refatoração correta?
Resposta: Não. A mudança pode atingir outro vínculo ou alterar comportamento, apesar de preservar a gramática.

Pergunta: Posso reutilizar metadados depois de substituir nós?
Resposta: Somente conforme o contrato da ferramenta; referências por identidade podem pertencer à árvore anterior e precisar de nova resolução.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T232:C05 — mecanismo_avancado

Renomear um identificador exige resolver vínculo, não somente reconhecer um nó Name. O mesmo texto pode referir-se a importação, variável local ou símbolo sombreado. LibCST oferece metadados de escopo e nomes qualificados, inclusive múltiplos candidatos em situações condicionais. Uma transformação deve preservar ambiguidades não resolvidas em vez de escolher um vínculo arbitrário. Após mudar a árvore, metadados da versão anterior podem precisar ser recalculados.

Condição de contorno:
Reflexão, geração dinâmica de nomes e imports condicionais podem impedir resolução estática completa.

Contrato proposto:
- Entradas: Árvore da revisão atual, metadados de escopo, alvo semântico e regra de transformação.
- Saídas: Código transformado, locais alterados e casos não resolvidos.
- Estado: Versão do parser, árvore de origem e metadados associados.
- Invariante: Uma transformação usa metadados da mesma árvore cuja identidade está sendo analisada.

Compromissos de projeto:
- CST preserva comentários e formatação com maior complexidade de estrutura.
- Análise estática reduz colisões textuais e não cobre toda semântica dinâmica da linguagem.

## T232:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar o mesmo identificador em importação, parâmetro e variável sombreada, além de import condicional; alterar somente o vínculo especificado e reportar ambiguidade restante.

Plano de avaliação proposto:
Comparar substituição textual e codemod em casos com escopos variados. Medir mudanças corretas, preservação de comentários, parse após edição e comportamento. Testes funcionais continuam necessários mesmo quando a transformação produz sintaxe válida.

Comparações:
- T231 (alternative): Busca literal é mais simples quando o alvo é inequívoco; estrutura ajuda quando texto igual possui significados diferentes.
- T216 (complements): O mapa do repositório orienta descoberta de símbolos, mas não substitui metadados do trecho editado.

Afirmação rastreável:
QualifiedNameProvider do LibCST pode devolver múltiplos nomes possíveis para um nó em situações como imports condicionais.
Suporte: direct; fontes: V3C-S033
Limite: Os metadados são análise estática e não demonstram qual caminho foi executado em todos os ambientes.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T232:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava resolução de vínculos e metadados. A expansão seleciona regras estruturalmente elegíveis, separa transformação determinística de decisão semântica e usa recusa explícita para os casos que a análise não cobre.

Pré-condições da regra
Declare padrões aceitos, contexto de escopo e propriedades a preservar antes de transformar. Uma remoção de flag pode exigir conhecer seu valor definitivo e distinguir expressões com efeitos. Quando a pré-condição não pode ser comprovada, encaminhe exceção para análise em vez de aplicar a regra por similaridade de árvore.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S008, V4C-S009.

AST, CST e emissão
A árvore abstrata representa sintaxe relevante ao compilador, mas comentários e formatação podem exigir árvore concreta ou mecanismo de preservação. Escolha a representação conforme o objetivo, incluindo linguagem e parser. Após modificar, reanalise o resultado e atualize metadados; objetos de escopo calculados antes da mudança podem não continuar válidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S035, V4C-S006.

LLM como controlador de exceções
Use modelo para interpretar diagnóstico, selecionar regra ou analisar contexto que a ferramenta não resolveu. Não peça à LLM para reproduzir manualmente uma transformação mecânica bem definida sem necessidade. Essa divisão reduz geração livre, mas a decisão de que a regra se aplica continua exigindo evidência e teste.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S006.

USO AVANÇADO — Limpeza de feature flags
Cenário: Código tem caminhos mortos após decisão operacional confirmada.
Estratégia: Valide estado da flag e escopo dos repositórios, execute transformação estrutural e gere diff. Rode CI e verificações adicionais de intenção. Casos dinâmicos ou referências não resolvidas permanecem pendentes; a ferramenta não deve adivinhar o valor por nome ou frequência de uso.
Papel do modelo pequeno: 3–7B classifica resultados simples; 8–14B trata exceções; 15–30B integra impacto entre módulos.
Aceite proposto: Proposta: eliminar apenas caminhos elegíveis e rejeitar mudanças sem evidência da pré-condição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S008, V4C-S009.

USO AVANÇADO — Renome de API
Cenário: Um símbolo aparece em múltiplos escopos e linguagens.
Estratégia: Resolva referências no escopo suportado, transforme consumidores elegíveis e produza lista de ocorrências não classificadas. Teste imports, geração de código e acesso dinâmico separadamente. Um grep final ajuda a localizar resíduos, mas ausência textual não prova preservação de comportamento.
Papel do modelo pequeno: 8–14B analisa ocorrências não resolvidas; ferramentas fazem renome verificável.
Aceite proposto: Proposta: nenhuma alteração em símbolo sombreado e compatibilidade de consumidores testados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S035, V4C-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Seleção de regra estreita e interpretação de saída estruturada, sem simular parser por linguagem natural.
8–14B: Diagnóstico de exceções locais e proposta de pré-condições adicionais.
15–30B: Análise de mudanças entre módulos e decisão de quais casos exigem revisão mais forte.
Requisitos de treino/runtime: Parser compatível, resolução de escopo, fontes de pré-condição e testes sobre o resultado emitido.
Não aplicar quando: Não generalizar transformação estática a reflexão e código gerado sem procedimento específico.

## T232:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: A fonte identifica diferenças e modificações em AST para construir reparos.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

V4C-C010 — Uber / AutoClean com PolyglotPiranha — evolução do cleanup
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve AutoClean executando continuamente nos monorepos, produzindo diffs de remoção de flags com CI e validação antes da revisão humana.
Mecanismo documentado: Agente chama transformação determinística por MCP; falhas de CI passam primeiro por fixers mecânicos; verificadores CodeCourt por propriedade executam em paralelo e agregam decisão.
Correspondência com esta base: Transformações determinísticas de código ficam no PolyglotPiranha.
Transferência proposta para modelo pequeno: Proposta: 3–7B classifica falhas mecânicas; 8–14B propõe alteração localizada; 15–30B avalia propagação de mudanças. Transformações booleanas e gates permanecem determinísticos; cada banda precisa de avaliação própria.
Limite: O operador não informa que as faixas propostas de modelos reproduzam o sistema. CI verde não prova semântica, e vereditos de agentes continuam sujeitos a erro. Pipeline e sua evolução histórica contam uma vez.
Fontes: V4C-S008, V4C-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Piranha/AutoClean e Getafix fornecem casos operacionais específicos. Transferência para bandas de parâmetros é proposta; ferramentas não são apresentadas como LLMs pequenas.
Consultas registradas: V4C-Q005, V4C-Q006.

## T232:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T232 → T140 [complements]
Como combinar: AutoClean expõe Piranha por MCP para que o agente invoque transformação estrutural.
Interface: Regra, argumentos e resultado da ferramenta.
Condição: A tarefa é elegível ao mecanismo determinístico.
Aceite proposto: Revisar o delta e tratar exceções sem alterar o objetivo.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

2. T232 → T217 [complements]
Como combinar: AutoClean executa CI e encaminha falhas a reparadores após a transformação.
Interface: Patch, logs e classe de falha.
Condição: Reparadores respeitam escopo e validam novamente.
Aceite proposto: Verde de CI não dispensa verificações de propriedade.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S009. Casos: V4C-C010.

CONTROLES DE FALHA
- Mesmo identificador textual pode ter vínculos diferentes; preservar ambiguidade não resolvida.
- Aprovação por LLM de preservação semântica não equivale a prova formal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare LLM pequena com ferramenta estrutural e modelo de fronteira editando livremente usando os mesmos testes. O ganho pode vir da ferramenta e da restrição do problema, não de inteligência geral equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T231, T229, T217

## Fontes primárias associadas

### V2A-S015 — LibCST documentation

[https://libcst.readthedocs.io/en/latest/](https://libcst.readthedocs.io/en/latest/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore sintática concreta para transformações Python preservando formatação, comentários e parênteses.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V3C-S035 — LibCST — Codemods

[https://libcst.readthedocs.io/en/latest/codemods.html](https://libcst.readthedocs.io/en/latest/codemods.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework de transformações, metadata e passes para codemods sobre CST.

Limite: Transformação automatizada não comprova comportamento preservado; validação depende do contrato da mudança.

### V4C-S008 — Introducing Piranha: An Open Source Tool to Automatically Delete Stale Code

[https://www.uber.com/us/en/blog/piranha/](https://www.uber.com/us/en/blog/piranha/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pipeline interno de remoção de flags obsoletas por transformação de AST e geração de diffs para revisão.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
