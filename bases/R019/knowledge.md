# R019 — Aider

**Nome canônico:** Aider — programação assistida no terminal  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R019  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** aider.chat; AI pair programming com Aider

## R019:C01 — conceito

Aider é uma ferramenta de programação assistida que combina conversa com uma LLM, contexto do repositório e edição de arquivos. Seu repo map apresenta símbolos relevantes sem enviar necessariamente todo o código. Formatos de edição diferentes permitem substituir arquivos completos ou aplicar mudanças localizadas, conforme o modelo e a configuração.

Como funciona:
- O mapa sintetiza arquivos, classes, funções e assinaturas para orientar dependências e localização de código.
- O formato chamado diff pelo Aider usa blocos SEARCH/REPLACE; o formato udiff é baseado em unified diff, com adaptações.
- Comandos de teste podem devolver erros ao ciclo de correção; o código de saída informa falha operacional do comando.

Nota de nomenclatura: Nenhuma chamada ao Aider ou modelo foi executada. Formatos e recursos devem corresponder à versão instalada.

## R019:C02 — aplicacao

Quando usar:
- Mudanças localizadas em projetos Git, refatorações e correções com testes e critérios verificáveis.

Quando não usar:
- Quando faltam especificação e ambiente de validação, mas se pretende tratar uma edição aplicada como solução comprovada.

Implementação proposta:
- Proposta: trabalhar em branch ou worktree isolado e registrar a revisão inicial do repositório.
- Selecionar arquivos editáveis e referências relevantes; conferir o formato de edição aceito pelo modelo escolhido.
- Configurar comando de teste confiável e limite de tentativas; revisar o diff resultante contra a tarefa e os testes existentes.

Aplicação LAI proposta:
Proposta LAI: usar Aider como referência para repo map e edição incremental; comparar essas escolhas com o executor existente em pequenos reparos controlados.

## R019:C03 — riscos_validacao

Armadilhas:
- Repo map é uma seleção, não uma descrição completa de toda semântica ou de dependências dinâmicas.
- Trechos de busca repetidos ou arquivos alterados em paralelo podem provocar falha ou aplicação indevida de edições.

Métricas sugeridas:
- Aplicação correta do patch, testes relevantes aprovados, regressões, tokens e tentativas por alteração aceita.

Testes propostos:
- Proposta: usar um defeito conhecido, reproduzi-lo antes da edição e confirmar que o teste passa depois.
- Inserir trecho repetido e mudança concorrente para conferir se o executor identifica ambiguidade em vez de aceitar silenciosamente o resultado.

## R019:C04 — perguntas_proveniencia

Pergunta: O diff do Aider é sempre um unified diff?
Resposta: Não. O formato denominado diff usa busca e substituição; udiff é outro formato documentado.

Pergunta: Um patch aplicado e sem erro encerra a tarefa?
Resposta: Não. Ainda é necessário verificar comportamento, requisitos e possíveis regressões no código afetado.

Pergunta: Editor correto no formato significa plano implementado?
Resposta: Não. Compare as diferenças com requisitos e testes comportamentais específicos.

Pergunta: Por que um formatador pode confundir a correção automática?
Resposta: Se retornar código não zero por ter formatado código, o executor pode interpretar sucesso de formatação como falha de lint.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R019:C05 — mecanismo_avancado

O modo architect do Aider separa duas tarefas: formular a alteração e traduzi-la em instruções de edição. Os papéis podem usar modelos diferentes ou o mesmo modelo em duas chamadas. Isso separa erro de raciocínio de erro de formatação, mas uma tradução sintaticamente válida ainda pode contrariar o plano. O editor usa um formato próprio: diff significa SEARCH/REPLACE; udiff pertence a outra convenção. O repo map orienta localização, enquanto o conteúdo atual do arquivo determina a alteração aplicável. Na integração de lint, o código de saída precisa distinguir erro real de um formatador que apenas modificou arquivos.

Condição de contorno:
Dois estágios não garantem maior qualidade. Um plano incompleto, mapa desatualizado ou comando de validação mal configurado pode aumentar ciclos de correção.

Contrato proposto:
- Entradas: Revisão base, arquivos editáveis, proposta do architect, formato do editor e comandos de validação.
- Saídas: Alterações aplicadas, diagnóstico do parser e resultados associados à revisão modificada.
- Estado: Plano original, resposta do editor, diferenças resultantes e tentativas de reparo.
- Invariante: A edição preserva o escopo aprovado e é validada no conteúdo efetivamente produzido.

Compromissos de projeto:
- Separar papéis facilita localizar a causa da falha, mas acrescenta latência e consumo de contexto.
- SEARCH/REPLACE economiza saída, porém depende de trechos identificáveis no arquivo atual.

## R019:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer plano correto e fazer o editor emitir formato incompatível. Exigir rejeição explícita; configurar formatador com saída não zero e conferir que não produz falso ciclo de reparação.

Plano de avaliação proposto:
Comparar code e architect nas mesmas tarefas, revisões e orçamento total. Medir acerto funcional, aplicação de edições, divergência do plano e custo incluindo reparos; selecionar pela taxa de alterações aceitas.

Comparações:
- T229 (complements): Aider pode concretizar edição por patches, mas também oferece formatos de arquivo completo; o contrato depende da configuração.
- R027 (complements): Git fixa a base e permite comparar o resultado entre as etapas de planejamento e edição.

Afirmação rastreável:
Architect e editor são etapas separadas e podem utilizar o mesmo modelo em duas solicitações.
Suporte: direct; fontes: V3C-S042
Limite: A documentação não demonstra que a separação supera todo modelo e tarefa de programação.

Nota de pesquisa:
Síntese documental; contrato e testes são propostas editoriais, sem execução do produto neste trabalho.

## R019:C07 — estrategia_3_30b

NOVA CAMADA v4 — Aprofunda architect/editor com contrato semântico de tradução, classificação de erros e política de encaminhamento baseada no tipo de edição.

Plano testável para editor menor
Proposta: o planejador entrega arquivos elegíveis, comportamento esperado e condições que devem permanecer verdadeiras. O editor traduz essas condições para uma alteração limitada. Um plano em prosa sem critérios deixa a segunda etapa reconstruir a intenção, anulando a separação de responsabilidades.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

Diagnóstico de falha
Distinguir localização incorreta, formato inválido, conflito de base e regressão semântica. Repetir a mesma chamada com mais tokens não é tratamento universal. Uma falha de formato pode voltar ao editor; uma mudança de requisito precisa voltar ao planejador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

Roteamento por superfície
Separar edições mecânicas, mudanças locais e refatorações atravessando módulos. Modelos menores podem ser úteis nos dois primeiros grupos se houver ferramentas e testes adequados. O roteador deve aprender com resultados aceitos por classe, incluindo tentativas que não produziram patch.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

USO AVANÇADO — Atualização mecânica em muitos arquivos
Cenário: Mudança repetitiva tem regra e exceções identificáveis.
Estratégia: Produzir candidatos por AST/busca, deixar o editor resolver somente ambiguidades delimitadas e validar o conjunto.
Papel do modelo pequeno: 3–7B pode traduzir planos pequenos; transformação determinística executa casos inequívocos.
Aceite proposto: Comparar cobertura e falsos positivos com script simples, contabilizando revisão humana.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

USO AVANÇADO — Correção localizada
Cenário: Bug tem reprodução e poucos arquivos candidatos.
Estratégia: Congelar teste e base, produzir patch numa cópia isolada e devolver evidência ao planejador.
Papel do modelo pequeno: 8–14B edita; modelo maior só entra se falha semântica justificar.
Aceite proposto: Patch aplica na base declarada, resolve reprodução e não quebra testes relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S042, V2B-S009, V2B-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: edição estreita com arquivo atual e invariantes explícitos, quando o backend e modelo forem compatíveis.
8–14B: 8–14B: correções locais com teste executável e contexto seletivo.
15–30B: 15–30B: planejamento multiarquivo sujeito a orçamento e comparação com decomposição menor.
Requisitos de treino/runtime: Validar suporte do provedor, formato de edição e comandos locais na versão utilizada.
Não aplicar quando: Não escolher dois modelos por prestígio; a tradução adicional pode elevar erro e custo.

## R019:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: Recurso nativo documentado do Aider.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Documentação do próprio Aider sustenta recursos disponíveis. Não foram confirmadas dez implantações Big Tech do produto; arquiteturas parecidas não foram renomeadas Aider.
Consultas registradas: V4C-Q023.

## R019:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R019 → T208 [complements]
Como combinar: Entregar ao executor uma intenção verificável em vez de apenas prosa livre.
Interface: Arquivos elegíveis, condição inicial, mudança e invariantes.
Condição: Há benefício medido em separar planejamento e edição.
Aceite proposto: O executor não precisa adivinhar requisito ausente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S042, V2B-S009, V2B-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R019 → T233 [feeds]
Como combinar: Submeter patch e base ao validador antes de integrar.
Interface: Patch, hash-base e comandos de verificação.
Condição: Toda alteração produz artefato revisável.
Aceite proposto: Conflito ou teste falho bloqueia a promoção do patch.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S042, V2B-S009, V2B-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar a opção diff como sinônimo universal de unified diff.
- Não avaliar apenas patches que aplicaram; tentativas inválidas também custam.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar arquiteturas de uma e duas chamadas no mesmo conjunto de bugs, com custo por correção aceita. Reportar editor pequeno e planejador maior como sistema híbrido, não capacidade isolada do editor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T216, T217, T229, T230, T231, T236, T239, R027

## Fontes primárias associadas

### V2B-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa conciso de arquivos e símbolos para contexto do código.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferença entre whole, diff com SEARCH/REPLACE e udiff adaptado.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V2B-S009 — Linting and testing

[https://aider.chat/docs/usage/lint-test.html](https://aider.chat/docs/usage/lint-test.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução de testes, interpretação de código de saída e configuração de testes após edições.

Limite: Documentação primária consultada nesta data; nenhuma instalação, benchmark ou avaliação no ambiente LAI foi executada.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
