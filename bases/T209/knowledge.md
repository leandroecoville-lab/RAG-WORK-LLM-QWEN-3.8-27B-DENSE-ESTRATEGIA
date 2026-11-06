# T209 — Reflexion

**Nome canônico:** Reflexion  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T209  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reflexão episódica por feedback

## T209:C01 — conceito

Método de agentes que transforma feedback de tentativas em reflexão textual mantida em memória episódica para orientar tentativas posteriores. Reflexion aprende operacionalmente por contexto, sem atualizar os pesos do modelo nesse mecanismo. Seu diferencial é a relação entre tentativa, avaliação, reflexão e nova tentativa.

Como funciona:
- Executar a tarefa e obter feedback de um avaliador, ambiente ou teste.
- Produzir uma reflexão sobre decisões que contribuíram para o resultado, vinculando-a ao feedback concreto.
- Recuperar reflexões pertinentes na próxima tentativa e observar se a estratégia mudou de forma útil.

## T209:C02 — aplicacao

Quando usar:
- Problemas repetíveis de programação, navegação ou raciocínio com resultado avaliável e tentativas comparáveis.

Quando não usar:
- Quando repetir a tarefa pode duplicar um efeito externo irreversível ou quando não existe feedback confiável.

Implementação proposta:
- Proposta: guardar tentativa, condições iniciais, resultado e uma reflexão curta com hipótese verificável.
- Priorizar feedback de testes e ambiente sobre autoconfiança verbal; registrar contradições entre avaliadores.
- Limitar tentativas e o tamanho da memória, consolidando lições redundantes sem apagar contraexemplos.
- Avaliar a nova tentativa em casos adicionais para distinguir melhoria da simples adaptação ao teste observado.

Aplicação LAI proposta:
Proposta LAI: registrar lições de falhas de integração com a evidência original e reutilizá-las apenas em tarefas compatíveis.

## T209:C03 — riscos_validacao

Armadilhas:
- Reflexões plausíveis podem atribuir a falha à causa errada.
- Acumular conselhos incompatíveis piora a próxima decisão.
- Memória textual não equivale a treinamento paramétrico.

Métricas sugeridas:
- Reincidência do mesmo erro; melhoria entre tentativas; custo de reflexão; generalização em casos reservados.

Testes propostos:
- Fornecer erro de compilação e verificar que a reflexão menciona a evidência relevante.
- Criar feedback enganoso e exigir incerteza, em vez de uma lição categórica.
- Comparar execução com e sem memória reflexiva sob o mesmo orçamento.

## T209:C04 — perguntas_proveniencia

Pergunta: Reflexion e Self-Refine são sinônimos?
Resposta: Não. Reflexion mantém feedback reflexivo entre tentativas; Self-Refine itera geração, autocrítica e revisão de uma saída.

Pergunta: Uma reflexão correta garante a próxima solução?
Resposta: Não. Ela é orientação contextual; a nova execução continua precisando de avaliação independente e controle de efeitos.

Pergunta: Uma reflexão deve sempre orientar a próxima tarefa?
Resposta: Não. É necessário comparar escopo, condições e evidências; uma regra local pode ser incorreta fora da tentativa original.

Pergunta: Como distinguir aprendizado de repetição retórica?
Resposta: Verificar se a próxima ação muda de maneira relevante e se o erro deixa de ocorrer sob avaliação independente.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T209:C05 — mecanismo_avancado

A reflexão textual precisa preservar a ligação entre tentativa, feedback e recomendação. Um erro de ferramenta pode produzir uma lição incorreta se interpretado como falha de estratégia. Da mesma forma, passar em testes fracos pode reforçar um atalho inválido. Uma proposta trata reflexões como hipóteses procedurais com escopo e evidência, permitindo substituição quando novas tentativas contradizem a regra, sem convertê-las em verdades globais sobre o projeto.

Condição de contorno:
Sem feedback informativo ou com avaliador sistematicamente errado, acumular reflexões pode consolidar o mesmo erro em linguagem mais convincente.

Contrato proposto:
- Entradas: Trajetória referenciada, feedback verificável e objetivo da próxima tentativa.
- Saídas: Reflexão acionável, condições de aplicação e vínculo com o resultado.
- Estado: Memória de tentativas, revisões das lições e evidências contraditórias.
- Invariante: Uma recomendação registra de qual falha foi inferida e não apaga o feedback original.

Compromissos de projeto:
- Lições curtas facilitam reutilização e podem omitir condições importantes.
- Histórico amplo preserva contexto e pode consumir a janela com experiências irrelevantes.

## T209:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar feedback equivocado por falha do ambiente e depois corrigir o ambiente; verificar se a reflexão é revisada, em vez de continuar culpando uma estratégia válida.

Plano de avaliação proposto:
Comparar nova tentativa sem memória, com resumo factual e com reflexão acionável. Fixar número de tentativas e avaliador. Medir sucesso acumulado, repetição do erro e transferência indevida de lições para outros casos; incluir tarefas onde a regra aprendida não se aplica.

Comparações:
- T192 (distinct_from): Self-Refine revisa um candidato; Reflexion conserva feedback para orientar tentativas futuras.
- T204 (complements): Lições verificadas podem alimentar procedimentos, com critérios de promoção separados.

Afirmação rastreável:
O repositório dos autores implementa diferentes agentes e estratégias de reflexão em ambientes experimentais.
Suporte: direct; fontes: V3C-S029
Limite: Uma estratégia bem-sucedida em um ambiente não demonstra que toda autocrítica verbal produz aprendizado útil.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T209:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava reflexões como hipóteses procedurais. A ampliação define quando uma lição merece ser recuperada, como testar seu benefício e como impedir que feedback ruim se torne política permanente.

Separar diagnóstico e regra
Uma reflexão deve registrar o que falhou, qual observação sustenta a causa e qual mudança será tentada. Não converter um erro transitório em regra global como evitar uma ferramenta. Se a causa continua incerta, preserve hipóteses concorrentes e um teste discriminante; a reflexão útil orienta coleta de evidência, não apenas reescreve a tentativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S029, V3C-S032.

Validade contextual
Indexe a lição por classe de tarefa, ferramenta e versão. Uma solução de compatibilidade antiga pode se tornar contraproducente após atualização. Recuperação deve exigir correspondência de condições e permitir expiração ou revisão; manter todo conselho acumulado no prompt cria conflitos que o modelo pequeno pode não conseguir resolver.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S001, V4C-S030.

Avaliar transferência
Compare novas tarefas com e sem as reflexões candidatas usando o mesmo orçamento. Uma lição que só explica o exemplo que a gerou não demonstra generalização. Meça também efeitos negativos: correções excessivas, chamadas evitadas indevidamente e aumento de tokens. Promova a regra somente quando seu escopo e benefício forem verificáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S029, V3C-S032.

USO AVANÇADO — Reparo de chamadas de ferramenta
Cenário: O agente repete uma classe específica de argumento inválido.
Estratégia: Guarde erro estruturado, schema vigente e exemplo mínimo corrigido. Na próxima tarefa semelhante, recupere a regra antes de gerar argumentos. Se a falha ocorreu depois de efeito incerto, a lição deve mandar reconciliar, não simplesmente trocar o formato e reenviar.
Papel do modelo pequeno: 3–7B aplica exemplos estreitos; 8–14B diagnostica a classe; controlador verifica efeito.
Aceite proposto: Proposta: menor repetição do mesmo erro sem aumento de chamadas semanticamente incorretas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S029, C-S026.

USO AVANÇADO — Ciclos de programação
Cenário: Uma tentativa falha num teste de comportamento.
Estratégia: Extraia a propriedade violada e formule a próxima hipótese de reparo. Preserve o teste que falhou e evite ensinar a remover a asserção. Quando o teste estava errado, corrija sua origem de requisito e registre por que a lição anterior foi invalidada.
Papel do modelo pequeno: 8–14B analisa falha local; 15–30B propõe alternativas sob testes independentes.
Aceite proposto: Proposta: resolver novos defeitos da mesma classe e detectar regressões produzidas pela lição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S032, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Lições curtas ligadas a erros tipados e condições claras de aplicação.
8–14B: Diagnóstico local e comparação de hipóteses com feedback executável.
15–30B: Síntese de regras condicionais entre tarefas, mantendo revisão e possibilidade de descarte.
Requisitos de treino/runtime: Memória de tentativas, avaliador informativo e casos reservados para medir transferência.
Não aplicar quando: Não acumular reflexões quando feedback é arbitrário ou quando só há autoconcordância do gerador.

## T209:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Foram encontrados loops de revisão em operadores, mas não comprovação de adoção exata de Reflexion nesses casos. O método permanece apoiado em pesquisa, sem inflar produção.
Consultas registradas: V4C-Q024, V4C-Q027, V4C-Q028.

## T209:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T209 → T218 [complements]
Como combinar: Repetições sem progresso disparam diagnóstico, que propõe mudança testável em vez de outro turno equivalente.
Interface: Assinatura do ciclo, observações e hipótese nova.
Condição: Existe sinal de estagnação além de mero número de passos.
Aceite proposto: A próxima tentativa altera variável relevante e seu efeito é medido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T209 → T234 [complements]
Como combinar: Guardar apenas lições promovidas e contextualizadas na memória do projeto.
Interface: Regra, escopo, origem e condição de invalidação.
Condição: A regra passou por revisão e teste de transferência.
Aceite proposto: Atualização de versão remove ou revisa orientação incompatível.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S030, V3C-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Uma lição eloquente pode explicar a causa errada; exigir evidência discriminante.
- Não confundir reflexão textual com atualização de pesos ou com o método formal de uma implantação não identificada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare pequeno com memória de reflexões e fronteira com o mesmo feedback. Avalie generalização em tarefas novas; mais iterações no próprio exemplo não provam aprendizado transferível.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T192, T207, T217

## Fontes primárias associadas

### V2A-S001 — Reflexion: Language Agents with Verbal Reinforcement Learning

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Feedback linguístico, memória episódica reflexiva e revisão de tentativas sem atualizar pesos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S002 — Self-Refine: Iterative Refinement with Self-Feedback

[https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração, feedback e refinamento iterativo pelo mesmo modelo; distinção de Reflexion.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S029 — Reflexion — authors implementation and experiments

[https://github.com/noahshinn/reflexion](https://github.com/noahshinn/reflexion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementações, notebooks e estratégias de reflexão associadas a tipos de agente e ambientes experimentais.

Limite: Repositório de pesquisa em branch mutável; resultados publicados não foram reproduzidos nem usados como avaliação deste corpus.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
