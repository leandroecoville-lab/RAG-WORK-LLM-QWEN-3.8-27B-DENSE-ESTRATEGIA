# T229 — Diff-Only Editing / Patch-Based Coding

**Nome canônico:** Diff-Only Editing / Patch-Based Coding  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T229  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** patch based coding; edição por patch

## T229:C01 — conceito

Edição expressa como alterações localizadas sobre uma base conhecida, em vez de substituir desnecessariamente o conteúdo completo. Um patch descreve intenção e facilita revisão do delta. O formato compacto pode reduzir material transmitido, mas não garante aplicação correta nem preservação do comportamento fora do trecho alterado.

Como funciona:
- O agente lê uma revisão e produz um conjunto explícito de mudanças.
- O aplicador verifica precondições e tenta aplicar o delta à base correspondente.
- A validação posterior inspeciona tanto o patch final quanto os efeitos sobre contratos e dependentes.

## T229:C02 — aplicacao

Quando usar:
- Correções pontuais, revisões de código e colaboração em arquivos existentes com necessidade de rastrear mudanças.

Quando não usar:
- Forçar patches textuais para arquivos binários ou aceitar aplicação aproximada quando o alvo ficou ambíguo.

Implementação proposta:
- Proposta: identificar revisão, caminhos autorizados e hashes dos arquivos que serão alterados.
- Escolher formato suportado pelo aplicador, como unified diff ou substituições literais com contexto suficiente.
- Aplicar primeiro em área isolada ou validar a aplicabilidade antes de gravar.
- Se a base mudou, reler e reconstruir o patch a partir do conteúdo atual, preservando alterações independentes.
- Revisar o delta resultante e executar verificações proporcionais ao comportamento modificado.

Aplicação LAI proposta:
Proposta LAI: entregar alterações como patches rastreáveis ligados à missão e à revisão inicial, com validação antes de integração ao repositório principal.

## T229:C03 — riscos_validacao

Armadilhas:
- Um patch pequeno pode causar efeito amplo em uma API compartilhada.
- Correspondência por contexto não equivale a verificação criptográfica da base.
- Mudanças de formatação podem ocultar alterações semânticas relevantes.

Métricas sugeridas:
- Arquivos e linhas alterados; rejeições por base divergente; alterações fora do escopo; falhas após aplicação.

Testes propostos:
- Alterar a base após geração e verificar rejeição ou reconstrução consciente.
- Inspecionar o diff final para identificar mudanças não solicitadas.
- Testar um consumidor afetado por uma alteração pequena em contrato compartilhado.

## T229:C04 — perguntas_proveniencia

Pergunta: Diff-only significa que o agente não precisa ler o arquivo?
Resposta: Não. O delta deve ser fundamentado no conteúdo e no contrato atuais. Ler trechos relevantes continua necessário para formular uma mudança correta.

Pergunta: Qual a diferença para Unified Diff?
Resposta: Patch-based coding é o padrão de edição. Unified Diff é um formato específico para representar alterações textuais dentro desse padrão.

Pergunta: Um patch aplicado sem erro pode estar errado?
Resposta: Sim. Pode alterar um local semanticamente inadequado ou produzir comportamento incorreto apesar da compatibilidade textual.

Pergunta: Um diff do Aider é sempre Unified Diff?
Resposta: Não. O formato chamado diff pelo Aider usa blocos search/replace; formato e aplicador precisam corresponder.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T229:C05 — mecanismo_avancado

Uma edição baseada em patch define o delta sobre uma base, mas o aplicador determina como usa contexto e resolve conflitos. Em Git, aplicar à árvore de trabalho, ao índice ou a ambos são operações diferentes. A opção de merge em três vias depende de identidades de blobs e disponibilidade da base; não é uma forma genérica de adivinhar qualquer patch. Após aplicação, o delta efetivo precisa ser inspecionado, pois contexto parecido pode ocultar alvo errado.

Condição de contorno:
Patches pequenos podem ser ambíguos em trechos repetidos e não garantem preservação de comportamento fora da alteração.

Contrato proposto:
- Entradas: Patch, revisão-base, destino e modo de aplicação declarado.
- Saídas: Delta aplicado ou conflito explícito, com revisão resultante.
- Estado: Base, índice quando usado, arquivos alterados e resultado do aplicador.
- Invariante: A alteração efetiva permanece dentro do escopo pretendido e referenciada à base correta.

Compromissos de projeto:
- Contexto amplo reduz ambiguidade e aumenta tamanho transmitido.
- Merge em três vias pode aproveitar base conhecida e deixar conflitos que exigem resolução semântica.

## T229:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aplicar o mesmo hunk a arquivo com dois blocos parecidos e base divergente; exigir falha ou identificação inequívoca, seguida de inspeção do delta real.

Plano de avaliação proposto:
Comparar substituição integral, search/replace e patch em mudanças localizadas. Medir taxa de aplicação correta, conflitos, tokens e alterações involuntárias. Separar sucesso de aplicação e testes de comportamento.

Comparações:
- T230 (complements): Unified Diff é um formato possível para representar mudanças localizadas; edição por patches também admite outras convenções.
- T233 (complements): Validação verifica base, escopo e comportamento antes de considerar a edição concluída.

Afirmação rastreável:
git-apply diferencia árvore e índice e condiciona merge em três vias à presença de identidades e blobs necessários.
Suporte: direct; fontes: V2A-S014
Limite: O sucesso do aplicador verifica compatibilidade textual, sem demonstrar correção funcional da mudança.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T229:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia destinos de aplicação e merge em três vias. A nova camada escolhe o delta mínimo verificável, controla escopo de patch e separa representação compacta de garantia semântica.

Delta com identidade de base
O patch deve declarar a revisão contra a qual foi produzido e os caminhos permitidos. Antes de aplicar, verifique base ou prepare uma adaptação explícita. Uma alteração pequena pode atingir o lugar errado em código repetido; contexto e hash ajudam a detectar divergência, mas não substituem revisão do resultado efetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V3C-S037.

Escopo do candidato
Avalie adições, remoções, modos, renomes e arquivos gerados. Um modelo que deveria mudar uma função pode incluir alterações em configuração ou testes para facilitar o aceite. Defina limites por tarefa e rejeite mudanças não justificadas, sem confundir pequeno número de linhas com baixo impacto: uma linha pode alterar todo o sistema.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V3C-S034.

Formato conforme capacidade
Diffs reduzem saída quando o arquivo é grande, mas exigem localizar corretamente os trechos. Em arquivos curtos ou modelos com baixa aderência ao formato, emissão completa pode ser mais confiável. Compare taxa de aplicação e correção final, incluindo reparo de formato, em vez de escolher diff apenas pela economia nominal de tokens.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S042.

USO AVANÇADO — Edição local com 3–7B
Cenário: A mudança afeta poucas linhas num arquivo conhecido.
Estratégia: Forneça trecho suficiente e base identificada, peça delta limitado e aplique em cópia isolada. Inspecione diff efetivo e execute teste focado. Se o patch não encaixar, releia a base atual antes de pedir reparo; não aumentar tolerância automaticamente até encaixar em qualquer lugar.
Papel do modelo pequeno: 3–7B produz delta curto; 8–14B diagnostica conflito de contexto.
Aceite proposto: Proposta: menos tokens por patch aceito, sem aumento de aplicação no alvo errado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S034.

USO AVANÇADO — Campanha de limpeza
Cenário: Muitas alterações repetitivas precisam ser auditáveis.
Estratégia: Use ferramenta estrutural quando a transformação for formalizável e apresente diff para revisão. Agrupe candidatos por regra e execute validações de propriedade. A saída compacta permite revisar intenção, mas a preservação de comportamento continua dependendo dos testes e dos limites da regra.
Papel do modelo pequeno: 8–14B classifica exceções; 15–30B integra conflitos entre mudanças.
Aceite proposto: Proposta: rastrear cada delta à regra e rejeitar alterações fora do objetivo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S009, V4C-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Patches pequenos com delimitadores estáveis e baixa ambiguidade de localização.
8–14B: Edições em alguns arquivos, usando diagnóstico de conflito e contexto adicional.
15–30B: Planejamento de mudanças maiores cuja execução continua dividida em deltas verificáveis.
Requisitos de treino/runtime: Aplicador com contrato conhecido, árvore isolada, base identificada e revisão do diff realmente aplicado.
Não aplicar quando: Não aceitar patch porque aplicou sem erro nem interpretar tamanho pequeno como prova de segurança semântica.

## T229:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C018 — Amazon / Campanhas internas Java com Amazon Q Developer
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: A AWS relata Amazon utilizando Q Developer em campanhas internas de atualização de aplicações Java de produção.
Mecanismo documentado: Equipe central seleciona aplicações e dependências, define ondas e esforço residual; o agente propõe plano e alterações, seguidas de compilação e testes.
Correspondência com esta base: A transformação produz mudanças de código, sem documentar que a representação e aplicação sejam exclusivamente patches localizados.
Transferência proposta para modelo pequeno: Proposta: classificar previamente migrações reconhecidas; usar um 3–30B para substituições locais com documentação exata e ferramentas de build. Tratar bibliotecas internas ou upgrades parcialmente compilados como pendências específicas.
Limite: Modelos e tamanhos não identificados. Aplicação compilada não garante comportamento equivalente; números agregados de ganho não são reproduzidos nem projetados para outros códigos.
Fontes: V4C-S017.

V4C-C009 — Meta / Getafix / SapFix / Sapienz — reparo de código
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: A Meta relata Getafix e SapFix em seu processo de desenvolvimento, com correções testadas, aprovadas e levadas a produção.
Mecanismo documentado: Padrões de reparo são extraídos de alterações por AST; candidatos passam por compilação e testes de persistência do erro e novas falhas, antes da revisão humana.
Correspondência com esta base: Correções são produzidas e revisadas, mas o relato não documenta um protocolo específico de edição exclusivamente por diffs.
Transferência proposta para modelo pequeno: Proposta: um 3–30B escolhe entre transformações conhecidas ou prepara candidato; analisadores e testes verificam propriedades fora do modelo. Avaliar bugs fora das famílias de treinamento para medir generalização.
Limite: Um único caso integrado, sem contar Getafix, SapFix e Sapienz como três deployments independentes. Ferramentas históricas não são LLMs modernas; não se transfere taxa de acerto.
Fontes: V4C-S006, V4C-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Aider documenta representações; AutoClean e Getafix mostram reparos e transformações, sem provar que toda mudança usa exatamente este protocolo de patch.
Consultas registradas: V4C-Q005, V4C-Q006, V4C-Q023.

## T229:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T229 → T233 [complements]
Como combinar: Validar base, aplicação e comportamento antes de promover o candidato.
Interface: Patch, árvore base e resultados de verificação.
Condição: Testes correspondem aos bytes que serão entregues.
Aceite proposto: Rejeitar patch aplicado em revisão diferente sem nova validação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T229 → T232 [alternative]
Como combinar: Para padrões estruturais, gerar transformação AST e revisar o delta produzido em vez de pedir texto livre.
Interface: Regra, símbolos elegíveis e patch derivado.
Condição: Parser e resolução cobrem a linguagem e o caso.
Aceite proposto: Alteração preserva propriedades e falha explicitamente em ambiguidade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S009, V4C-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mudanças de fim de linha podem inflar o diff e esconder alteração real.
- Não reformatar arquivos inteiros sem necessidade da tarefa, dificultando revisão e integração.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare formatos com o mesmo modelo e tarefas antes de comparar portes. A redução de saída ajuda modelos pequenos, mas um patch sintaticamente correto ainda pode implementar a intenção errada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T230, T231, T233, T239

## Fontes primárias associadas

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S014 — git-apply

[https://git-scm.com/docs/git-apply](https://git-scm.com/docs/git-apply)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação e aplicação de patches; contexto, índice e tratamento de caminhos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

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

### V4C-S017 — Accelerate application upgrades with Amazon Q Developer agent for code transformation

[https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/](https://aws.amazon.com/blogs/devops/accelerate-application-upgrades-with-amazon-q-developer-agent-for-code-transformation/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campanhas internas de modernização Java com planos de transformação, dependências, compilação e testes.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
