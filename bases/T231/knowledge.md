# T231 — Search/Replace Editing

**Nome canônico:** Search/Replace Editing  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T231  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** search replace blocks; edição por substituição literal

## T231:C01 — conceito

Edição por pares de texto a localizar e texto substituto, com escopo explícito. É apropriada para alterações literais quando o alvo pode ser identificado sem ambiguidade. Aider documenta formatos dessa família; diferenças de sintaxe entre ferramentas não devem ser ignoradas pelo agente que produz a edição.

Como funciona:
- O aplicador procura o texto original dentro de um arquivo conhecido.
- A operação confirma o número esperado de ocorrências e as precondições da base.
- Somente então substitui o trecho, preservando o conteúdo restante segundo o contrato do editor.

## T231:C02 — aplicacao

Quando usar:
- Rewording, correção de constantes e pequenos ajustes em blocos com contexto literal suficiente.

Quando não usar:
- Renomeação semântica que depende de escopo ou substituição global de uma palavra comum sem análise dos alvos.

Implementação proposta:
- Proposta: ler o trecho exato e registrar caminho, hash da base e quantidade esperada de correspondências.
- Incluir contexto inalterado suficiente para identificar uma ocorrência única, sem ampliar a mudança pretendida.
- Agrupar substituições independentes com semântica clara: todas sobre a base original ou sequenciais, conforme o aplicador.
- Se o alvo não existir ou houver duplicidade, reler e reconstruir a operação; não improvisar correspondência aproximada.
- Verificar o conteúdo final e o diff para confirmar que somente os alvos pretendidos mudaram.

Aplicação LAI proposta:
Proposta LAI: usar substituições literais protegidas por base para edições pequenas, preservando rastreabilidade do texto original e escalando transformações semânticas para análise estrutural.

## T231:C03 — riscos_validacao

Armadilhas:
- Espaços, escapes e finais de linha alteram a correspondência literal.
- Regras sequenciais podem fazer uma substituição afetar o resultado de outra.
- Uma ocorrência única ainda pode estar no módulo errado.

Métricas sugeridas:
- Correspondências esperadas e encontradas; rejeições por ambiguidade; alterações fora do alvo; conflitos de versão.

Testes propostos:
- Criar duas ocorrências do mesmo trecho e exigir desambiguação.
- Alterar a base entre leitura e escrita e conferir o guard de versão.
- Testar substituições que se sobrepõem e verificar rejeição ou ordenação expressamente definida.

## T231:C04 — perguntas_proveniencia

Pergunta: Search/replace é sempre regex?
Resposta: Não. O padrão desta entrada é literal. Expressões regulares adicionam outra linguagem e exigem escopo, escaping e critérios de correspondência próprios.

Pergunta: Posso substituir todas as ocorrências?
Resposta: Somente quando esse conjunto é o alvo intencional e foi verificado. Uma operação global não deve ser inferida a partir de uma ocorrência solicitada.

Pergunta: Nenhuma ocorrência deve provocar uma substituição aproximada automática?
Resposta: Não por padrão. Pode haver revisão incorreta; o erro precisa ser diagnosticado antes de relaxar a correspondência.

Pergunta: Duas ocorrências iguais podem ser ambas corretas?
Resposta: Sim, quando o objetivo exige alterar ambas e o contrato declara isso; igualdade textual sozinha não decide.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T231:C05 — mecanismo_avancado

O contrato de search/replace precisa declarar cardinalidade esperada: zero correspondências significa base divergente ou busca inadequada; várias podem indicar ambiguidade. Trocar todas as ocorrências é uma decisão semântica adicional. Espaços, quebras de linha e normalização influenciam matching; tolerância aumenta taxa de aplicação e pode atingir um bloco parecido que não era o alvo. No Aider, o formato diff usa esses blocos e não deve ser confundido com Unified Diff.

Condição de contorno:
Texto repetido ou código gerado pode inviabilizar localização única sem aumentar contexto ou usar estrutura sintática.

Contrato proposto:
- Entradas: Arquivo versionado, trecho de busca, substituição e quantidade esperada de ocorrências.
- Saídas: Alteração aplicada ou diagnóstico de ausência e ambiguidade.
- Estado: Hash-base, ocorrências localizadas e conteúdo resultante.
- Invariante: A cardinalidade e o escopo observados correspondem ao pedido antes da substituição.

Compromissos de projeto:
- Matching exato é previsível e sensível a pequenas mudanças de formatação.
- Matching tolerante aceita mais variações e exige confirmação mais forte do alvo semântico.

## T231:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir o mesmo trecho em duas funções e alterar whitespace em apenas uma; exigir rejeição da ambiguidade ou seleção por contexto explícito.

Plano de avaliação proposto:
Comparar matching exato, tolerante e edição estrutural em bases com repetição controlada. Medir aplicação correta, alterações fora do alvo e tokens necessários para desambiguar. Escolher o método por risco de colisão e complexidade da mudança.

Comparações:
- T230 (distinct_from): Unified Diff inclui hunks e intervalos; blocos search/replace localizam conteúdo literal.
- T232 (alternative): Edição sintática pode distinguir símbolos iguais em escopos diferentes.

Afirmação rastreável:
Aider descreve seu formato diff como uma série de blocos de busca e substituição.
Suporte: direct; fontes: V2A-S008
Limite: A semântica precisa de matching depende do aplicador; esta ficha propõe cardinalidade e validação explícitas.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T231:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definia cardinalidade e ambiguidade. A expansão organiza seleção de âncoras, múltiplas substituições dependentes e alternativas quando o formato textual não consegue localizar o alvo de forma inequívoca.

Âncora suficiente
A busca deve conter contexto capaz de distinguir o trecho sem copiar arquivo inteiro. Inclua estrutura envolvente quando nomes ou blocos se repetem. Uma âncora maior aumenta custo e pode ficar obsoleta após mudanças não relacionadas; escolha o menor trecho cuja unicidade foi verificada na revisão atual, e não apenas presumida pelo modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S033.

Ordem de substituições
Duas operações podem interagir: a primeira altera a âncora da segunda. Defina se todos os searches referem-se à base original ou ao estado sucessivo e aplique consistentemente. Quando o protocolo não garante atomicidade, prepare todas as mudanças em cópia e publique apenas após validar o conjunto, evitando arquivo parcialmente editado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S027.

Escalonamento da localização
Zero ou múltiplas correspondências devem gerar diagnóstico específico. Releia a região e amplie contexto; se continuar ambíguo, use símbolo e parser ou escolha outro formato. Tolerância a espaços precisa ser explícita e não pode transformar duas funções parecidas em alvos intercambiáveis. Localização é parte da correção da edição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S035.

USO AVANÇADO — Correção curta em arquivo grande
Cenário: Um 3–7B precisa alterar um bloco conhecido.
Estratégia: Forneça região atual, peça SEARCH exato e REPLACE completo, conte correspondências e aplique só quando a cardinalidade esperada for satisfeita. Mostre o diff efetivo e rode verificação local. Se falhar a busca, não pedir ao modelo para inventar uma versão provável do arquivo.
Papel do modelo pequeno: 3–7B produz blocos curtos; 8–14B escolhe contexto adicional para desambiguar.
Aceite proposto: Proposta: nenhuma substituição no bloco errado e menor saída que reemitir o arquivo inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008.

USO AVANÇADO — Mudanças sequenciais relacionadas
Cenário: Uma assinatura e seus usos locais precisam mudar juntos.
Estratégia: Planeje substituições sobre uma base definida, verifique sobreposição e simule todas em árvore isolada. Se uma mudança invalida outra, regenere o conjunto a partir da revisão atual. Após aplicar, confirme que não sobraram consumidores incompatíveis no escopo relevante.
Papel do modelo pequeno: 8–14B organiza blocos; 15–30B analisa dependências entre arquivos.
Aceite proposto: Proposta: aplicação completa ou rejeição explícita, sem estados intermediários publicados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S008, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Blocos curtos, âncoras únicas e poucos delimitadores favorecem aderência ao protocolo.
8–14B: Seleção de contexto e diagnóstico de correspondências ambíguas.
15–30B: Planejamento de alterações múltiplas; aplicar com ferramenta determinística e verificação de conjunto.
Requisitos de treino/runtime: Leitura atual do arquivo, contagem de matches, política de whitespace e staging isolado.
Não aplicar quando: Não substituir todas as ocorrências por padrão nem usar aproximação textual quando houver alvos semanticamente distintos.

## T231:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: SEARCH/REPLACE é formato explicitamente descrito.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Aider documenta o formato como recurso; não foram encontrados dez deployments de bigtech com este protocolo exato, e udiff não foi confundido com SEARCH/REPLACE.
Consultas registradas: V4C-Q023, V4C-Q006.

## T231:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T231 → R019 [complements]
Como combinar: Usar o formato SEARCH/REPLACE documentado do Aider quando o modelo consegue seguir seus delimitadores.
Interface: Caminho, bloco SEARCH e bloco REPLACE.
Condição: Formato selecionado corresponde ao contrato do editor efetivo.
Aceite proposto: Rejeitar zero ou múltiplos alvos não autorizados e verificar diff.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S008, V3C-S042. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T231 → T232 [alternative]
Como combinar: Trocar localização textual por seleção estrutural quando o símbolo e seu vínculo precisam de precisão adicional.
Interface: Nó, escopo e intenção de transformação.
Condição: Parser e resolução semântica cobrem o caso.
Aceite proposto: Mesmo nome em outro escopo permanece inalterado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S035. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não aplicar primeiro bloco e ignorar rejeição dos seguintes.
- Strings de código gerado podem repetir um trecho válido sem serem o alvo autorizado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare taxa de localização correta, aplicação e testes entre formatos sob o mesmo modelo. Melhor aderência textual de 3–30B não demonstra equivalência em entender efeitos da mudança.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T229, T232, T233

## Fontes primárias associadas

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

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

### V3C-S035 — LibCST — Codemods

[https://libcst.readthedocs.io/en/latest/codemods.html](https://libcst.readthedocs.io/en/latest/codemods.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework de transformações, metadata e passes para codemods sobre CST.

Limite: Transformação automatizada não comprova comportamento preservado; validação depende do contrato da mudança.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
