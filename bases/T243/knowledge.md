# T243 — Reconciliação de operações externas

**Nome canônico:** Reconciliação de operações externas  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T243  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** external operation reconciliation; reconciliação de efeitos incertos

## T243:C01 — conceito

Processo de comparar a intenção registrada de uma operação com o estado observado no sistema externo e resolver divergências sem presumir que ausência de resposta significa ausência de efeito. É essencial quando um timeout, queda ou resposta perdida deixa incerto se a operação foi concluída.

Como funciona:
- O controlador registra identidade e intenção antes de iniciar a operação.
- A tentativa produz resultado confirmado ou estado incerto, preservando a distinção.
- O reconciliador consulta recibos, status ou recursos externos e decide confirmar, repetir com segurança ou manter a pendência.

## T243:C02 — aplicacao

Quando usar:
- Criação de recursos, envio de mensagens, gravações remotas e outras mutações cuja resposta possa se perder após execução.

Quando não usar:
- Marcar automaticamente timeout como falha sem efeito, repetir com nova identidade ou inventar uma garantia de exatamente uma vez.

Implementação proposta:
- Proposta: registrar operation_id, destino, parâmetros relevantes, chave idempotente suportada e estado inicial.
- Persistir identificadores externos e recibos assim que disponíveis; separar attempted, confirmed, failed e uncertain.
- Para uncertain, consultar o provedor usando identidade confiável e respeitar atrasos de consistência.
- Repetir apenas quando o protocolo permitir deduplicação ou houver evidência suficiente de não execução.
- Quando não for possível concluir, preservar a incerteza para decisão explícita; compensação é outra operação, não um rollback universal.

Aplicação LAI proposta:
Proposta LAI: manter um ledger de operações externas e reconciliar pendências antes de retomar missões, permitindo auditoria do que foi tentado e do que foi confirmado.

## T243:C03 — riscos_validacao

Armadilhas:
- Busca por payload parecido pode confundir operações legítimas diferentes.
- Chaves idempotentes podem ter escopo e validade limitados.
- Uma leitura desatualizada pode sugerir falsamente que o recurso não existe.

Métricas sugeridas:
- Operações incertas; tempo até resolução; duplicações; divergências persistentes; confirmações com recibo; compensações necessárias.

Testes propostos:
- Simular conclusão externa seguida de perda da resposta e verificar confirmação sem duplicar.
- Simular leitura temporariamente desatualizada e evitar retry prematuro.
- Reutilizar chave com intenção diferente e exigir rejeição ou novo processo conforme contrato.
- Testar provedor sem consulta confiável e manter estado incerto.

## T243:C04 — perguntas_proveniencia

Pergunta: Qual é a diferença entre retry e reconciliação?
Resposta: Retry tenta executar novamente. Reconciliação primeiro determina a relação entre intenção e estado observado para escolher uma ação segura.

Pergunta: Sempre é possível resolver automaticamente?
Resposta: Não. Sem identidade, recibo ou consulta confiável, pode restar ambiguidade. O sistema deve reportá-la em vez de fabricar sucesso ou falha definitiva.

Pergunta: Não encontrei o objeto: posso repetir imediatamente?
Resposta: Somente se a leitura e o contrato sustentarem ausência conclusiva; com consistência eventual, pode ser cedo demais.

Pergunta: Compensação é igual a rollback?
Resposta: Não. É outra operação de domínio, possivelmente com efeitos observáveis e falhas próprias, que precisa de identidade e verificação.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T243:C05 — mecanismo_avancado

Reconciliação precisa distinguir efeito observado e efeito desta intenção. Encontrar um objeto parecido não prova que a tentativa incerta o criou; correlação por chave, ID ou recibo é mais forte. Uma consulta pode ainda refletir consistência eventual e retornar ausência temporária. A proposta usa estados confirmado, ausente com evidência suficiente e desconhecido, mantendo prazo e política de nova observação antes de decidir repetir ou compensar.

Condição de contorno:
Se o sistema externo não oferece identidade consultável nem leitura com garantias adequadas, alguns desfechos permanecem desconhecidos.

Contrato proposto:
- Entradas: Intenção, tentativa, chave externa, resultado incerto e contrato de consulta.
- Saídas: Conclusão fundamentada, nova observação ou ação de recuperação elegível.
- Estado: Recibos, consultas realizadas, versões e janela de convergência.
- Invariante: Ausência de resposta ou de leitura imediata não é tratada automaticamente como ausência de efeito.

Compromissos de projeto:
- Observar mais vezes reduz algumas incertezas e aumenta atraso e custo.
- Compensar pode corrigir efeito indesejado e criar outro efeito que também exige rastreabilidade.

## T243:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: perder a resposta de uma escrita e atrasar sua visibilidade na consulta; exigir estado desconhecido inicial e reconhecimento posterior, sem criar um segundo objeto.

Plano de avaliação proposto:
Comparar retry imediato e reconciliação sob resposta perdida, duplicatas e leitura atrasada. Medir efeitos duplicados, tempo até conclusão e casos corretamente mantidos como desconhecidos. Usar o contrato real de idempotência e retenção do serviço.

Comparações:
- T162 (complements): A chave idempotente ajuda reconhecer uma intenção, dentro de seu escopo e prazo.
- T228 (complements): A fila deve conservar estado incerto para não converter reconciliação em nova execução cega.

Afirmação rastreável:
Kubernetes descreve controllers que observam estado atual e agem para aproximá-lo do estado desejado.
Suporte: related; fontes: V2A-S024
Limite: A identificação de efeitos externos incertos é aplicação editorial desse princípio, complementada por contratos concretos de idempotência.

Nota de pesquisa:
Contratos, cenários de falha e planos de avaliação são propostas editoriais fundamentadas nas fontes indicadas.

## T243:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguia efeito desta intenção de objeto parecido. A expansão organiza um protocolo de incerteza, escalona observações e define quando repetir, compensar ou manter pendência sem fabricar certeza.

Ledger de intenção
Registre o que se pretendia fazer, chave externa, parâmetros, envio e último resultado conhecido. A reconciliação consulta a identidade da operação e confronta o efeito observado com a intenção. Encontrar recurso com nome semelhante não basta; pode pertencer a outra tentativa, usuário ou ação legítima independente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S025.

Ausência tem força variável
Uma leitura vazia pode significar operação não executada, processamento em andamento ou atraso de visibilidade. Use garantias do destino e sinais de status para decidir quando a ausência é suficiente. Se não houver consulta confiável, mantenha desconhecido e limite novas ações; disponibilidade não deve ser obtida por duplicação silenciosa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S028.

Compensação é nova operação
Desfazer um efeito externo não é restaurar memória local. A compensação possui pré-condições, identidade e possibilidade de falha próprias. Um recurso pode ter sido usado ou modificado depois da operação original; reverter cegamente pode apagar trabalho válido. Planeje compensações por contrato e registre seu resultado separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V4C-S002.

USO AVANÇADO — Criação com timeout
Cenário: O agente solicita um ambiente e perde a resposta.
Estratégia: Consulte pelo identificador da intenção e aguarde visibilidade conforme contrato. Se confirmado, continue com o recurso existente; se ausente com evidência suficiente, repita usando identidade apropriada. Se a chave expirou e não há correlação confiável, não assuma que é seguro criar outro automaticamente.
Papel do modelo pequeno: 3–7B preenche pedido; 8–14B interpreta estados tipados; runtime decide repetição segura.
Aceite proposto: Proposta: nenhum recurso duplicado em falhas antes, durante e depois da confirmação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026.

USO AVANÇADO — Deploy ou publicação interrompida
Cenário: Estado local diz pendente, mas o destino pode ter avançado.
Estratégia: Leia versão efetiva e histórico de operação, compare com versão desejada e verifique saúde do resultado. Se houve mudança concorrente, suspenda compensação automática e reconcilie autoridade. Um rollout parcialmente aplicado exige tratamento por etapa, não só marcar o workflow como falho.
Papel do modelo pequeno: 15–30B analisa alternativas; controlador preserva identidades e regras de publicação.
Aceite proposto: Proposta: convergir para estado aceito ou pendência explícita, sem sobrescrever mudança concorrente legítima.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S002, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumir estados confirmado, ausente e desconhecido definidos pelo adaptador, sem inferir efeito pelo texto.
8–14B: Diagnosticar divergências de parâmetros e necessidade de nova observação.
15–30B: Planejar compensação ou revisão de intenção em situações complexas, submetida a contratos e evidências.
Requisitos de treino/runtime: Identidade consultável, ledger persistente, garantias de leitura conhecidas e orçamento de observação.
Não aplicar quando: Não prometer exatamente uma vez quando o serviço não oferece deduplicação nem correlação suficiente.

## T243:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Ações manuais são incorporadas à representação do estado efetivo.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C001 — Amazon Web Services / EC2 RunInstances
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.
Mecanismo documentado: O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.
Correspondência com esta base: O relato discute a ambiguidade de recursos existentes e a necessidade de identificar a operação que os criou.
Transferência proposta para modelo pequeno: Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.
Limite: Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.
Fontes: C-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: EC2 e UpCD apoiam mecanismos de identidade e reconciliação em contextos específicos. A aplicação genérica a agentes é proposta com limites explícitos.
Consultas registradas: V4C-Q001, V4C-Q002, V4C-Q019.

## T243:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T243 → T162 [complements]
Como combinar: Chave idempotente liga tentativas à mesma intenção e permite interpretar resultados repetidos.
Interface: Chave, payload e horizonte de retenção.
Condição: Destino garante a semântica documentada da chave.
Aceite proposto: Repetição após timeout não cria efeito adicional.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T243 → T225 [complements]
Como combinar: Antes de liberar o executor reiniciado, resolver operações cujo desfecho ficou incerto.
Interface: Geração anterior, intenções pendentes e observações atuais.
Condição: Restart não apaga o ledger nem renova a identidade da ação.
Aceite proposto: Nova instância não repete automaticamente tudo após o último snapshot.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026, V3C-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Consulta de estado atual e repetição de intenção histórica são operações distintas.
- Compensação pode falhar ou ser inadequada após mudança concorrente; manter seu próprio estado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare integridade de efeitos e tempo de resolução sob falhas reproduzíveis. A LLM ajuda a interpretar casos, mas certeza operacional depende das garantias do destino e do registro local.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T228, T220, T225, T241, T240

## Fontes primárias associadas

### V2A-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade de intenção, deduplicação de requisições e equivalência semântica de retentativas.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S012 — Timeouts, retries, and backoff with jitter

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Retentativas limitadas, espera exponencial, jitter e incerteza de efeitos após timeout.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S024 — Controllers

[https://kubernetes.io/docs/concepts/architecture/controller/](https://kubernetes.io/docs/concepts/architecture/controller/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Laços de controle com observação do estado atual e aproximação ao estado desejado.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S025 — Stripe API — Idempotent requests

[https://docs.stripe.com/api/idempotent_requests](https://docs.stripe.com/api/idempotent_requests)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: API v1 guarda resposta após início de execução, compara parâmetros e possui retenção finita; API v2 tem semântica distinta explicitada.

Limite: Exemplo concreto de contrato; não generalizar política de retenção ou tratamento de erros a toda API.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
