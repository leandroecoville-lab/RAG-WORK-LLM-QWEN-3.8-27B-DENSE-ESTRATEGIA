# T238 — Read On Demand com faixa de linhas

**Nome canônico:** Read On Demand com faixa de linhas  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T238  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** just in time file reading; leitura dirigida por linhas

## T238:C01 — conceito

Recuperação de trechos de arquivos somente quando a tarefa exige o conteúdo, usando intervalos de linhas e referências verificáveis. É uma aplicação de contexto sob demanda. A seleção deve preservar o contexto semântico necessário: uma linha isolada pode ocultar importações, condições, escopo e tratamento de erro relevantes.

Como funciona:
- Busca ou mapa do repositório localiza candidatos.
- Uma leitura limitada expande o trecho em torno do alvo.
- Referências à revisão e ao caminho mantêm a ligação entre a evidência lida e o arquivo que poderá ser alterado.

## T238:C02 — aplicacao

Quando usar:
- Repositórios extensos, logs volumosos e investigação de poucos símbolos em muitos arquivos.

Quando não usar:
- Tomar decisões com trechos incompletos sem reconhecer a limitação ou confiar indefinidamente em números de linha após edições.

Implementação proposta:
- Proposta: localizar o símbolo com busca e registrar caminho e revisão observada.
- Ler um intervalo que inclua a unidade relevante, como função, classe ou bloco de configuração.
- Expandir para chamadores, imports e testes somente quando uma hipótese depender deles.
- Marcar truncamento e distinguir ausência no trecho de ausência no arquivo inteiro.
- Depois de uma alteração, atualizar a posição ou resolver novamente o símbolo antes de reutilizar referências.
- Manter o original recuperável para conferência e revisão.

Aplicação LAI proposta:
Proposta LAI: combinar mapa do repositório com leituras por unidade de código e revisão, mantendo evidência suficiente para editar sem carregar arquivos inteiros indiscriminadamente.

## T238:C03 — riscos_validacao

Armadilhas:
- Linhas deslocam após inserções.
- Uma busca literal pode não encontrar nomes gerados dinamicamente.
- A redução excessiva transforma contexto incompleto em falsa certeza.

Métricas sugeridas:
- Bytes e tokens lidos; expansões por investigação; leituras redundantes; referências desatualizadas; hipóteses confirmadas por leitura.

Testes propostos:
- Inserir linhas antes do alvo e verificar atualização da referência.
- Apresentar erro cujo tratamento esteja fora do primeiro intervalo e exigir expansão antes da conclusão.
- Consultar texto ausente no trecho e impedir a alegação de ausência global sem busca apropriada.

## T238:C04 — perguntas_proveniencia

Pergunta: Faixa de linhas é uma referência estável?
Resposta: Somente em uma revisão determinada. Para trabalho entre revisões, use também identidade do arquivo, símbolo e contexto de busca.

Pergunta: Quando vale ler o arquivo completo?
Resposta: Quando suas relações internas são necessárias e ele cabe no orçamento. A técnica prioriza evidência adequada, não a menor leitura possível a qualquer custo.

Pergunta: O número da linha identifica uma função permanentemente?
Resposta: Não. Ele depende da revisão; símbolo, caminho e conteúdo ajudam a reidentificar o alvo após mudanças.

Pergunta: Quando ampliar a leitura?
Resposta: Quando faltarem definições, condições, chamadas ou erros necessários para interpretar o trecho e decidir a alteração.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T238:C05 — mecanismo_avancado

Uma faixa de linhas é endereço relativo a uma versão do arquivo. Inserções anteriores deslocam posições sem mudar o símbolo procurado; renomes e geração de código podem invalidar ainda mais a referência. Uma proposta combina caminho, revisão, intervalo e âncora sintática ou hash do trecho. Expandir a faixa deve responder a uma necessidade concreta, como obter definição de variável, condição envolvente ou contrato chamado.

Condição de contorno:
Um trecho pode parecer suficiente e omitir um guard, decorator, import ou tratamento de erro que muda seu significado.

Contrato proposto:
- Entradas: Arquivo e revisão, intervalo solicitado, símbolo e objetivo da leitura.
- Saídas: Trecho com limites claros, proveniência e indicação de contexto adicional necessário.
- Estado: Âncoras, hashes e faixas já lidas na mesma revisão.
- Invariante: Linha antiga não é reutilizada como localização exata após mudança de base sem verificação.

Compromissos de projeto:
- Faixas pequenas economizam contexto e aumentam chamadas de expansão.
- Faixas grandes preservam relações e podem introduzir material irrelevante.

## T238:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir linhas antes da função e alterar uma condição externa ao trecho original; exigir resolução da revisão e expansão suficiente para perceber a condição.

Plano de avaliação proposto:
Comparar leitura integral, faixa fixa e expansão por símbolo em tarefas de diagnóstico. Medir tokens, rodadas, localização correta e decisões que ignoraram contexto externo. Escolher a janela pela unidade semântica necessária, não apenas por tamanho.

Comparações:
- T216 (complements): Repo map ajuda a escolher arquivo e símbolo, mas a leitura precisa confirmar a revisão.
- T232 (complements): Metadados de posição e escopo podem ligar trechos à estrutura sintática.

Afirmação rastreável:
LibCST oferece metadados de posição e escopo associados a nós de uma árvore específica.
Suporte: related; fontes: V3C-S033
Limite: Leitura sob demanda por linha é uma política editorial; metadados antigos não acompanham automaticamente edições posteriores.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T238:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 associava faixa de linhas à revisão e âncora. A expansão escolhe unidades de leitura por hipótese, controla ampliação de contexto e registra o que não foi lido para evitar conclusões globais a partir de fragmentos.

Leitura guiada por decisão
Antes de abrir um trecho, explicite a dúvida que ele deve resolver: assinatura, guard, chamador ou comportamento de erro. A faixa inicial inclui contexto suficiente para essa decisão. Se surge dependência externa ao trecho, faça leitura adicional direcionada, sem presumir que ausência no fragmento significa ausência no arquivo ou projeto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V4C-S026.

Âncora e revisão
Resolva símbolo ou padrão na revisão atual e obtenha a faixa a partir dessa resolução. Guardar números de linha continua útil para rastreabilidade, mas não como endereço permanente após edição. Para arquivos gerados ou renomeados, recupere também origem e processo de geração; editar a saída errada pode ser desfeito pelo próximo build.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S033, V3C-S027.

Orçamento de expansão
Defina progressão de leitura: trecho, função, contexto de classe ou módulo, consumidores relevantes. Uma expansão deve responder a necessidade concreta e ser contabilizada. Quando muitas dependências cruzadas aparecem, pode ser mais barato ler uma unidade maior ou trocar a decomposição do que fazer dezenas de chamadas minúsculas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S027, V4C-S030.

USO AVANÇADO — Correção localizada
Cenário: Um erro aponta para função em arquivo grande.
Estratégia: Leia a função com assinatura, decorators e tratamento de erro, examine definição dos símbolos usados e teste que reproduz o defeito. Só então edite. Após a mudança, recalcule faixa e valide o código atual; não reutilize trechos anteriores como se fossem bytes vigentes.
Papel do modelo pequeno: 3–7B analisa funções curtas; 8–14B segue dependências; 15–30B decide quando ampliar escopo.
Aceite proposto: Proposta: localizar e corrigir com menos tokens sem omitir contexto que muda o significado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S026, V3C-S033.

USO AVANÇADO — Revisão de patch em monorepo
Cenário: Um revisor precisa verificar alteração sem carregar todo o projeto.
Estratégia: Parta do diff e leia contexto ao redor, contratos chamados e consumidores afetados. Registre quais propriedades foram verificadas e quais exigiriam leitura maior. Materialização sob demanda pode reduzir I/O, mas não equivale a ter analisado tudo que permanece remoto.
Papel do modelo pequeno: 8–14B revisa partes; 15–30B integra propriedades que atravessam módulos.
Aceite proposto: Proposta: mesma detecção de falhas relevantes com leitura total e custo de recuperação contabilizados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S027, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Trechos semanticamente completos e poucas dependências reduzem carga de contexto.
8–14B: Navegação por símbolos e escolha da próxima faixa a partir de hipótese explícita.
15–30B: Análise de impacto e decisão de juntar contexto quando leitura fragmentada perde relações.
Requisitos de treino/runtime: Ferramenta de leitura com revisão, offsets e indicadores de truncamento; acesso ao conteúdo integral quando necessário.
Não aplicar quando: Não declarar propriedade global do repositório depois de ler somente linhas selecionadas.

## T238:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Scion fornece consulta e materialização seletiva de arquivos sob demanda; não demonstra especificamente a API de faixa de linhas.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C011 — Google / Tricorder integrado a Critique
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: análise/reparo de software sem LLM demonstrada.
Uso observado: O livro de engenharia do Google descreve Tricorder como plataforma interna integrada à revisão de código, com análises de mudanças e feedback aos responsáveis.
Mecanismo documentado: Analisadores recebem metadados da mudança e acessam versões pertinentes; resultados aparecem junto ao diff, com controle de utilidade e falsos positivos.
Correspondência com esta base: A infraestrutura lê versões pertinentes à mudança, mas não demonstra leitura LLM por faixas de linhas.
Transferência proposta para modelo pequeno: Proposta: um modelo pequeno transforma diagnósticos em candidatos de reparo, mantendo analisadores como fontes de evidência. Medir avisos acionáveis, introdução de regressões e tempo de revisão, não apenas número de alertas.
Limite: Caso de análise estática sem LLM de 3–30B. Ausência de diagnóstico não garante ausência de erro; resultados históricos não definem capacidade atual.
Fontes: V4C-S010.

V4C-C020 — Microsoft / Windows — Git/GVFS
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A Microsoft relata rollout de Git/GVFS para equipes Windows e uso de commits, branches e builds de validação em sua engenharia.
Mecanismo documentado: Virtualização reduz a necessidade de materializar todo o repositório; proxies e melhorias de operações locais apoiam o fluxo de código versionado.
Correspondência com esta base: Materialização sob demanda inspira leitura seletiva, mas não é leitura LLM por faixa de linhas.
Transferência proposta para modelo pequeno: Proposta: manter um 3–30B trabalhando sobre arquivos materializados e referências de revisão, solicitando dependências quando necessário; não confundir arquivo ausente localmente com inexistente no repositório.
Limite: Relato histórico de 2017; não certifica configuração atual do Windows ou vantagem em toda dimensão. Não há LLM nem prova de método de edição autônoma.
Fontes: V4C-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Relatos operacionais de navegação e Scion apoiam leitura seletiva como família. A estratégia por linhas e seus critérios são proposta, sem contagem indevida de adoção exata.
Consultas registradas: V4C-Q024, V4C-Q027, V4C-Q023.

## T238:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T238 → T216 [complements]
Como combinar: Repo map fornece símbolos e relações para decidir quais faixas ler primeiro.
Interface: Caminho, símbolo, revisão e hipótese de localização.
Condição: Mapa corresponde à revisão ou é revalidado.
Aceite proposto: Trecho obtido contém a definição efetiva, não uma posição obsoleta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S033. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T238 → T233 [complements]
Como combinar: Leituras de contexto apoiam validação do patch, sem substituir teste da árvore completa quando necessário.
Interface: Diff, base e trechos de dependências.
Condição: Escopo da conclusão acompanha escopo da inspeção.
Aceite proposto: Revisor não afirma cobertura que não realizou.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Linhas omitidas podem conter guard, import ou efeito que altera a interpretação.
- Scion materializa conteúdo sob demanda; isso não prova a API específica de faixas de linhas proposta aqui.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare tokens lidos, chamadas de ferramenta e correção sob a mesma tarefa. Modelos pequenos podem aproveitar leitura dirigida, mas não inferem com segurança código que nunca foi observado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T216, T222, T214, T233

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S033 — LibCST — Metadata

[https://libcst.readthedocs.io/en/latest/metadata.html](https://libcst.readthedocs.io/en/latest/metadata.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MetadataWrapper e providers fornecem posições, escopos e nomes para transformações estruturais.

Limite: Metadados estáticos têm limites em código dinâmico; preserving CST não garante equivalência funcional.

### V4C-S026 — How Anthropic teams use Claude Code

[https://claude.com/resources/articles/how-anthropic-teams-use-claude-code](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso interno de Claude Code para navegar código, criar testes, depurar incidentes e operar ciclos de implementação e revisão.

Limite: Relatos do operador; não compara modelos pequenos nem estabelece ganhos causais controlados. URL anterior redireciona para esta página.

### V3C-S027 — Git — git-rev-parse

[https://git-scm.com/docs/git-rev-parse](https://git-scm.com/docs/git-rev-parse)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Resolução e verificação de revisões e identificação de objetos Git.

Limite: Uma revisão válida identifica objetos; não comprova qualidade funcional de uma alteração.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V4C-S010 — Software Engineering at Google — Static Analysis

[https://abseil.io/resources/swe-book/html/ch20.html](https://abseil.io/resources/swe-book/html/ch20.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tricorder integrado a Critique, análises ligadas à revisão de código e importância de falsos positivos efetivos.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

### V4C-S020 — The largest Git repo on the planet

[https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Migração operacional do código Windows para Git/GVFS, materialização sob demanda e infraestrutura de validação.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
