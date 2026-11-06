# T162 — Idempotência

**Nome canônico:** Idempotência  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T162  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** idempotency

## T162:C01 — conceito

Propriedade de uma operação cuja repetição, com a mesma intenção lógica, não produz efeitos adicionais relevantes. Em APIs, costuma exigir chave de idempotência, armazenamento do resultado e regra para pedidos concorrentes. Não significa que toda resposta de rede será idêntica nem que repetições nunca ocorrerão.

Como funciona:
- Associar a intenção a identificador estável antes da primeira tentativa.
- Registrar processamento e resultado de forma consistente com o efeito.
- Em repetição, devolver estado existente ou reconciliar em vez de repetir efeito.

## T162:C02 — aplicacao

Quando usar:
- Criação de registros, cobranças, mensagens ou jobs sujeitos a retries.
- Workers que podem receber o mesmo evento mais de uma vez.

Quando não usar:
- Reutilizar a mesma chave para intenções diferentes ou parâmetros incompatíveis.

Implementação proposta:
- Vincular chave ao tenant, operação e fingerprint dos argumentos.
- Definir retenção suficiente para a janela de retries e deduplicação.
- Resolver concorrência com transação ou exclusão apropriada.

Aplicação LAI proposta:
Proposta: toda mutação da Helena receber identificador de intenção que sobreviva a reinícios, com recibo consultável.

## T162:C03 — riscos_validacao

Armadilhas:
- Registrar chave depois do efeito deixa janela de duplicação.
- Expirar chave cedo demais permite repetir uma operação antiga.

Métricas sugeridas:
- Número de efeitos de negócio por intenção única.
- Conflitos de chave, duplicatas evitadas e estados incertos reconciliados.

Testes propostos:
- Enviar solicitações iguais simultaneamente e exigir um efeito lógico.
- Repetir chave com argumentos diferentes e exigir erro explícito.

## T162:C04 — perguntas_proveniencia

Pergunta: Idempotência é não repetir chamada?
Resposta: Não. Pode repetir a chamada preservando um único efeito lógico.

Pergunta: Timeout prova que a escrita falhou?
Resposta: Não. O efeito pode ter ocorrido antes da perda da resposta.

Pergunta: Reusar a mesma chave dias depois é sempre seguro?
Resposta: Não. É necessário conhecer retenção e expiração; após remoção, a chave pode criar uma nova operação.

Pergunta: É correto gerar nova chave a cada tentativa?
Resposta: Não para a mesma intenção. Isso elimina a identidade que permite ao servidor reconhecer a repetição.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T162:C05 — mecanismo_avancado

Idempotência prática possui horizonte temporal e identidade de payload. Depois de expirar o registro de uma chave, o servidor pode tratar a mesma chave como operação nova. Também precisa decidir o que ocorre quando a chave reaparece com parâmetros diferentes ou enquanto a primeira chamada está em andamento. Na Stripe API v1, respostas são guardadas após início de execução, inclusive erros 500; a documentação distingue esse comportamento da API v2.

Condição de contorno:
Uma chave sem retenção compatível com o período de retry não protege repetições tardias.

Contrato proposto:
- Entradas: Intenção estável, chave, parâmetros normalizados e versão do contrato.
- Saídas: Resultado lógico registrado, conflito de parâmetros ou operação pendente.
- Estado: Chave, digest do pedido, status e prazo de retenção.
- Invariante: A mesma chave não representa duas intenções distintas nem payloads incompatíveis.

Compromissos de projeto:
- Retenção longa amplia proteção e aumenta armazenamento e obrigações de limpeza.
- Reutilizar a resposta facilita repetição e pode conservar um erro que exige diagnóstico por outra via.

## T162:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir a chave com payload alterado, em concorrência e após expiração simulada; verificar os três comportamentos previstos pelo contrato.

Plano de avaliação proposto:
Comparar efeitos reais com e sem chave sob respostas perdidas e reentrega. Controlar período de retenção e normalização. Medir duplicações, conflitos e operações pendentes; a aceitação depende de cobrir o horizonte de repetição esperado.

Comparações:
- T243 (complements): Reconciliação consulta o efeito quando a camada idempotente não fornece conclusão suficiente.
- T150 (distinct_from): Compartilhar uma chamada ativa não conserva necessariamente a intenção após seu término.

Afirmação rastreável:
A Stripe documenta retenção finita, comparação de parâmetros e diferenças de idempotência entre APIs v1 e v2.
Suporte: direct; fontes: V3C-S025
Limite: Essas regras são exemplo concreto; outro serviço pode ter políticas completamente diferentes.

Nota de pesquisa:
Contratos e ensaios são propostas; os resultados citados pertencem às fontes, sem reprodução local.

## T162:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratava expiração e reutilização de chaves. A ampliação modela idempotência como protocolo de intenção, com decisões para duplicatas concorrentes, mudança legítima de objetivo e resultados cujo efeito persiste além da sessão.

Intenção antes de tentativa
Gere o identificador da operação no controlador e persista-o antes do primeiro envio. Todas as tentativas da mesma intenção usam essa identidade, inclusive após reinício. Uma nova intenção com os mesmos parâmetros recebe outra chave; duas instâncias iguais podem ser desejadas. O texto do pedido sozinho não define equivalência operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

Reserva e resultado atômicos
No destino, associe chave, parâmetros e estado da operação. Se o processo registra a chave e cai antes do efeito, precisa retomar ou indicar pendência; se realiza o efeito e perde o registro, a deduplicação falha. A implementação deve garantir atomicidade onde possível e usar reconciliação quando atravessa sistemas sem transação comum.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

Efeito versus representação
Uma resposta anterior pode continuar sendo a resposta semântica da tentativa mesmo que o recurso tenha mudado depois. Repetir a chamada não deve recriar um objeto que o usuário apagou legitimamente. Separe consultar o estado atual de repetir a intenção histórica; exponha essa diferença aos agentes que interpretam o resultado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S025.

USO AVANÇADO — Criação de ambiente de teste
Cenário: Um agente solicita infraestrutura e perde a conexão durante a criação.
Estratégia: Persista pedido e chave; após timeout, consulte a operação por essa chave. Somente crie nova intenção quando o primeiro resultado estiver reconciliado ou quando o usuário realmente pedir outro ambiente. Expiração do registro exige investigação antes de tentar novamente.
Papel do modelo pequeno: 3–7B preenche parâmetros; código durável administra identidade e reconciliação.
Aceite proposto: Proposta: nenhuma duplicação sob timeout após commit remoto, queda local e resposta atrasada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

USO AVANÇADO — Publicação de artefato
Cenário: A mesma alteração é entregue após retomadas de vários workers.
Estratégia: Identifique publicação por tarefa, revisão base e hash do artefato. Uma segunda tentativa com conteúdo diferente deve falhar como conflito de intenção, não sobrescrever silenciosamente. Para substituir o candidato, crie uma nova revisão e preserve a ligação com a anterior.
Papel do modelo pequeno: 8–14B explica conflitos; 15–30B decide reformulação sem controlar o ledger por linguagem natural.
Aceite proposto: Proposta: duplicata retorna resultado consistente e divergência de payload é detectada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executar ações tipadas de escopo restrito com IDs fornecidos pelo runtime.
8–14B: Classificar resposta em concluída, pendente ou conflitante conforme contrato verificável.
15–30B: Planejar compensações e revisões sem confundir nova intenção com nova tentativa.
Requisitos de treino/runtime: Ledger persistente, retenção alinhada ao horizonte de repetição e payload normalizado; evitar IDs gerados de novo após crash.
Não aplicar quando: Não afirmar exatamente uma vez quando o destino não deduplica e o efeito não é consultável.

## T162:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C001 — Amazon Web Services / EC2 RunInstances
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.
Mecanismo documentado: O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.
Correspondência com esta base: O contrato documentado controla repetição da mesma intenção no RunInstances.
Transferência proposta para modelo pequeno: Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.
Limite: Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.
Fontes: C-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: EC2 é caso operacional de API idempotente. A aplicação a patches e agentes pequenos é proposta; deduplicação de mensagens não foi confundida com efeito exatamente uma vez.
Consultas registradas: V4C-Q001, V4C-Q019.

## T162:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T162 → T243 [complements]
Como combinar: Resolver efeito desconhecido por identidade antes de escolher retry ou compensação.
Interface: Chave, parâmetros, confirmação remota e janela de retenção.
Condição: O destino permite consulta ou deduplicação verificável.
Aceite proposto: Falha após efeito confirmado não produz uma segunda alteração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T162 → T159 [complements]
Como combinar: Persistir a chave no estado durável para que todas as tentativas representem a mesma intenção.
Interface: Workflow, atividade lógica e identificador externo.
Condição: A identidade sobrevive ao reinício do worker.
Aceite proposto: Reproduzir histórico e repetir atividade mantendo a chave.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S018, C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Mesmo payload pode representar intenção nova; mesmo ID com payload novo é conflito.
- A chave expirada não autoriza presumir que o efeito original nunca ocorreu.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sistemas pelo número de efeitos corretos, inclusive sob falhas. Capacidade linguística superior não substitui atomicidade nem identidade persistente da operação.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T136, T150, T159

## Fontes primárias associadas

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S025 — Stripe API — Idempotent requests

[https://docs.stripe.com/api/idempotent_requests](https://docs.stripe.com/api/idempotent_requests)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: API v1 guarda resposta após início de execução, compara parâmetros e possui retenção finita; API v2 tem semântica distinta explicitada.

Limite: Exemplo concreto de contrato; não generalizar política de retenção ou tratamento de erros a toda API.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V3C-S018 — Temporal Workflow Definition — determinism and code evolution

[https://docs.temporal.io/workflow-definition](https://docs.temporal.io/workflow-definition)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Replay exige compatibilidade da sequência de comandos com o histórico; evolução do código exige estratégia de versionamento.

Limite: Determinação de comandos não significa igualdade de cada instrução ou captura de memória arbitrária do processo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
