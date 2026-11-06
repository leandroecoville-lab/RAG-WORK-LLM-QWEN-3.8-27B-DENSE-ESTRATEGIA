# T215 — Observation Masking

**Nome canônico:** Observation Masking  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T215  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** mascaramento de observações

## T215:C01 — conceito

Mecanismo de gestão de contexto que substitui observações antigas de ferramentas por marcadores curtos, preservando a estrutura necessária da trajetória. Ele descarta detalhes do contexto ativo em vez de gerar uma síntese semântica. O conteúdo original pode continuar disponível em armazenamento externo para recuperação posterior.

Como funciona:
- Aplicar uma política, como janela recente, para decidir quais observações permanecem visíveis.
- Trocar observações antigas por marcadores identificáveis sem apagar a relação entre ação e resultado.
- Preservar evidências críticas ou permitir recarregá-las por referência quando voltarem a ser necessárias.

## T215:C02 — aplicacao

Quando usar:
- Agentes com muitas observações extensas e repetitivas, como leitura de código e execução de testes.

Quando não usar:
- Quando o raciocínio seguinte depende de detalhes antigos que não foram preservados nem podem ser recuperados.

Implementação proposta:
- Proposta: armazenar resultados integrais por ID, medir tamanho e estabelecer uma janela de observações recentes.
- Mascarar o corpo das observações elegíveis, mantendo chamada, status e referência; preservar a validade estrutural das mensagens.
- Definir exceções para erros ainda abertos, contratos e evidências de efeitos externos.
- Avaliar a janela por tipo de tarefa; os resultados de um estudo em agentes de programação não garantem comportamento em outro domínio.

Aplicação LAI proposta:
Proposta LAI: experimentar mascaramento de logs antigos já resolvidos, preservando resultados atuais e referências a evidências auditáveis.

## T215:C03 — riscos_validacao

Armadilhas:
- O marcador não transmite o significado do conteúdo omitido.
- O agente pode esquecer por que uma opção falhou.
- Confundir mascaramento com resumo esconde qual informação foi realmente preservada.

Métricas sugeridas:
- Tokens removidos; releituras; taxa de conclusão; regressões por dependência de observações antigas.

Testes propostos:
- Criar tarefa cuja solução exige um resultado antigo e testar recuperação pelo marcador.
- Comparar masking e resumo usando mesmo modelo, tarefas e orçamento.
- Verificar que cada resposta de ferramenta continua associada à chamada correta.

## T215:C04 — perguntas_proveniencia

Pergunta: Observation Masking produz um resumo?
Resposta: Não. A operação central oculta o conteúdo e deixa um marcador; não tenta reescrever sua informação principal.

Pergunta: É comprovadamente superior em qualquer agente?
Resposta: Não. Há evidência em configurações estudadas; a escolha depende do tipo de observação, dependências temporais e custo de releitura.

Pergunta: Mascarar significa resumir com menos palavras?
Resposta: Não. O mecanismo pode apenas substituir o conteúdo por um marcador, sem representar semanticamente o que foi retirado.

Pergunta: Por que medir releituras na avaliação?
Resposta: Porque a economia inicial pode ser compensada por ferramentas repetidas para recuperar observações removidas cedo demais.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T215:C05 — mecanismo_avancado

Masking preserva a estrutura da trajetória enquanto retira o conteúdo de observações selecionadas. Essa assimetria pode deixar uma ação sem a evidência que a justificou, favorecendo releitura ou repetição. Uma política proposta marca observações protegidas por dependências ainda abertas: resultados que comprovam uma decisão pendente não entram na mesma regra de expiração que logs já consumidos. O marcador deve permitir localizar a observação integral quando necessário.

Condição de contorno:
Observações antigas continuam essenciais quando contêm único recibo, exceção ou detalhe ainda exigido pelo próximo passo.

Contrato proposto:
- Entradas: Trajetória, janela recente, dependências pendentes e referências ao arquivo original.
- Saídas: Histórico mascarado com marcadores estáveis e conteúdo protegido.
- Estado: Observações omitidas, motivos e acessos posteriores.
- Invariante: Mascarar contexto não significa apagar a evidência original nem declarar seu conteúdo irrelevante para sempre.

Compromissos de projeto:
- Regras simples reduzem custo de síntese e podem provocar novas consultas.
- Proteções por dependência preservam informação útil e exigem estado adicional do workflow.

## T215:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mascarar a única observação que contém um identificador necessário ao passo seguinte; exigir recuperação por referência ou proteção antecipada, sem inventar o identificador.

Plano de avaliação proposto:
Comparar histórico integral, masking e sumarização no mesmo agente e orçamento. Medir conclusão, releituras, repetição de ações e custo total, incluindo a síntese. Evitar extrapolar resultados de uma configuração para outros modelos e tarefas.

Comparações:
- T212 (alternative): Auto-compact produz resumo; masking decide quais observações deixar fora da janela.
- T214 (complements): Poda interna e masking por observação podem ser combinados com responsabilidades distintas.

Afirmação rastreável:
O estudo da JetBrains compara omissão de observações e sumarização e não encontra superioridade consistente da síntese em todas as configurações avaliadas.
Suporte: direct; fontes: V2A-S003
Limite: Os resultados pertencem aos agentes e benchmarks estudados; não demonstram que descarte sempre preserve melhor informação.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T215:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 protegia observações com dependências abertas. A expansão mede efeitos de masking na tomada de decisão, define recuperação de detalhes e distingue ocultação no prompt de remoção do histórico persistente.

Marcador informativo
Substitua observação ocultada por marcador com ferramenta, status, identificador e referência, conforme necessidade. Um marcador vazio informa que algo ocorreu, mas não ajuda a distinguir sucesso, erro ou efeito incerto. Preserve estrutura exigida pelo protocolo de mensagens para não deixar chamada sem resposta correspondente no histórico apresentado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S031.

Proteção por dependência
Mantenha observações que sustentam a próxima ação ou o critério de conclusão, mesmo se antigas. Uma janela temporal simples pode funcionar em carga homogênea e falhar em missões com longa espera entre decisão e uso da evidência. Expire a proteção quando a dependência fecha, registrando por que a observação se tornou dispensável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, C-S026.

Teste de recuperação
O agente deve reconhecer quando o marcador não basta e recuperar o original. Meça releituras e repetições de ferramentas causadas por masking; ocultar uma resposta e depois executar a mesma ação novamente pode ser mais caro ou perigoso que manter alguns campos. A política deve favorecer consulta do artefato antes de refazer efeito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, C-S026.

USO AVANÇADO — Pesquisa com muitas páginas
Cenário: Observações antigas ocupam a janela depois da extração.
Estratégia: Guarde os documentos, preserve tabela de alegações e oculte corpos já consumidos. Quando surgir contradição, recupere o trecho original por identidade. Compare masking com sumarização mantendo o mesmo número de documentos acessíveis e o mesmo critério de evidência.
Papel do modelo pequeno: 3–7B trabalha em extração local; 15–30B integra apenas registros necessários.
Aceite proposto: Proposta: cobertura e fidelidade de citações com custo total, incluindo recuperações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031.

USO AVANÇADO — Sessão longa de programação
Cenário: Muitos logs antigos repetem resultados já resolvidos.
Estratégia: Oculte logs encerrados, mantenha último erro completo e recibos de alterações externas. Preserve vínculo entre comando e versão do código testado. Se um defeito reaparecer, recuperar o log antigo permite comparar condições sem supor que a mesma mensagem tem a mesma causa.
Papel do modelo pequeno: 8–14B diagnostica localmente; runtime protege evidência de validação ainda vigente.
Aceite proposto: Proposta: menor contexto sem aumento de repetição ou perda de estado confirmado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V4C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Benefício potencial em trajetórias ruidosas; precisa de marcadores simples e recuperáveis.
8–14B: Classificação de observações consumidas e seleção de detalhes a reabrir.
15–30B: Integração de evidências preservadas, com acesso sob demanda a exceções antigas.
Requisitos de treino/runtime: Histórico persistente separado do prompt, referências estáveis e teste de compatibilidade com mensagens de ferramentas.
Não aplicar quando: Não ocultar único recibo de efeito ou evidência de requisito ainda em aberto.

## T215:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C030 — JetBrains Research / autores / SWE-agent com políticas de contexto
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo compara estratégias de contexto em tarefas SWE-bench Verified.
Mecanismo documentado: Masking oculta observações anteriores; sumarização substitui histórico por texto sintetizado; avaliação considera resolução e custo.
Correspondência com esta base: Observation masking é objeto central do experimento.
Transferência proposta para modelo pequeno: Proposta: avaliar remoção seletiva antes de acrescentar um resumidor 3–30B, preservando observações necessárias ao próximo teste.
Limite: Pesquisa controlada não conta como produção; não generalizar comparação para todo domínio ou modelo.
Fontes: V4C-S031.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Há estudo primário específico, classificado research_only. Não foi identificado nesta pesquisa um deployment de bigtech que documente esta mesma política como mecanismo comprovado.
Consultas registradas: V4C-Q028.

## T215:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T215 → T212 [alternative]
Como combinar: Comparar masking e resumo no mesmo scaffold, tratando diferenças de informação como variável explícita.
Interface: Trajetória, política e observações protegidas.
Condição: Mesmo conjunto de tarefas e orçamento total.
Aceite proposto: Medir resolução, duração, custo e reconsultas sem declarar vencedor universal.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T215 → T238 [complements]
Como combinar: Reabrir observação por referência quando o marcador deixa de bastar.
Interface: Identidade, versão e trecho solicitado.
Condição: Original acessível e não substituído silenciosamente.
Aceite proposto: Não repetir ferramenta com efeito só para recuperar uma informação já registrada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S031, C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Ocultar no prompt não equivale a apagar dados persistidos.
- Ausência da observação pode induzir repetição; o estado de conclusão deve permanecer explícito.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Use a comparação publicada como motivação para baseline, não como garantia para 3–30B. Os modelos locais avaliados no artigo incluem 32B e 480B, fora da faixa exata solicitada.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T214, T041, T004

## Fontes primárias associadas

### V2A-S003 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://kairos.jetbrains.com/research/articles/the-complexity-trap](https://kairos.jetbrains.com/research/articles/the-complexity-trap)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação controlada de mascaramento de observações e resumo de trajetória; são transformações distintas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S030 — Harness engineering: leveraging Codex in an agent-first world

[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Beta com usuários internos reais: aplicações por worktree, observabilidade isolada, planos versionados, instruções curtas e verificações mecânicas de arquitetura.

Limite: Experimento operacional de um time; não equivale a produto geral sem supervisão nem demonstra substituição por modelos pequenos. Ganhos autoestimados não transferidos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
