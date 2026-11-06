# P015 — Execution Integrity Controller

**Nome canônico:** Execution Integrity Controller  
**Grupo:** Componentes arquiteturais propostos  
**Escopo:** proposta  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** P015  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** controlador proposto de integridade da execução

## P015:C01 — conceito

Execution Integrity Controller é um nome editorial proposto para vincular uma intenção autorizada ao artefato, versão e efeito realmente executados. Verificaria pré-condições e recibos para evitar que uma operação correta seja aplicada ao alvo errado ou a uma base obsoleta. As fontes apoiam identidade de intenção e versionamento; não atestam esse controlador LAI implementado.

Como funciona:
- Associar o comando ao objetivo vigente, destino exato, entradas versionadas e identificador único de intenção.
- Conferir pré-condições imediatamente antes da escrita, incluindo hash ou versão da base quando o backend oferecer esse controle.
- Registrar resultado confirmado, rejeição ou desfecho desconhecido, preservando recibos e referências à operação.

## P015:C02 — aplicacao

Quando usar:
- Aplicação de patches, atualização de documentos, execução de ferramentas e publicação de artefatos com risco de concorrência ou duplicação.

Quando não usar:
- Como substituto do controle de acesso do serviço ou como prova de correção funcional baseada somente em um hash.

Implementação proposta:
- Proposta: formar um envelope de execução com alvo, base esperada, alteração pretendida e chave de idempotência.
- Validar que o efeito solicitado corresponde às decisões atuais e enviar a escrita com a pré-condição nativa disponível.
- Após resposta incerta, consultar estado e recibos antes de decidir nova tentativa; o reaparecimento do conteúdo sozinho pode não provar autoria ou conclusão daquela operação.

Aplicação LAI proposta:
Proposta LAI: P015 confere a ligação entre decisão e efeito do P011, enquanto P012 avalia o resultado e P013 administra falhas operacionais.

## P015:C03 — riscos_validacao

Armadilhas:
- Hash igual verifica igualdade dos bytes representados, mas não demonstra que o conteúdo está correto ou que a ação foi autorizada.
- Ler a versão e escrever sem uma guarda atômica deixa uma janela de concorrência.
- Reconstruir IDs a partir de nomes parecidos pode direcionar o efeito a outro recurso.

Métricas sugeridas:
- Conflitos detectados antes da escrita, operações sem recibo, efeitos duplicados e correspondência entre intenção e alvo.

Testes propostos:
- Aceite proposto: alterar a base entre preparação e escrita; exigir rejeição da guarda ou reconciliação explícita.
- Simular timeout após aplicação e verificar que a intenção original é consultada antes de repetir o efeito.

## P015:C04 — perguntas_proveniencia

Pergunta: Um hash-base elimina toda disputa de concorrência?
Resposta: Somente quando a comparação e a escrita são protegidas pelo backend ou por protocolo equivalente; comparação local isolada não basta.

Pergunta: Qual estado registrar se a resposta da escrita se perdeu?
Resposta: Resultado desconhecido, com os IDs da intenção e da tentativa, até obter evidência suficiente para reconciliar o desfecho.

Pergunta: Hash correto significa implementação correta?
Resposta: Não. Ele identifica bytes; testes e critérios verificam propriedades e comportamento.

Pergunta: Quando uma operação fica pendente?
Resposta: Quando houve intenção ou envio, mas a confirmação não permite determinar com segurança o efeito externo.

Escopo das fontes:
Fontes apoiam idempotência, objetos versionados e transações; envelope e controlador são proposta editorial.

## P015:C05 — mecanismo_avancado

Execution Integrity Controller propõe vincular cada mutação à versão de origem, à intenção e à evidência de resultado. Em edição de código, o patch deve declarar o estado-base e ser recusado se esse estado mudou sem reconciliação. Em operações externas, uma intenção estável e uma chave idempotente ajudam a distinguir repetição de uma nova ação. Hash comprova identidade do conteúdo comparado, mas não prova que seu significado está correto ou que a ação remota foi concluída.

Condição de contorno:
Não existe uma transação local capaz de tornar automaticamente atômicos arquivo, banco, fila e API externa independentes. A fronteira de confirmação deve ser explicitada por sistema.

Contrato proposto:
- Entradas: Mutação proposta, identidade do alvo, hash ou revisão esperada, escopo autorizado e ID estável da operação.
- Saídas: Aceite ou conflito, nova revisão, registro de intenção e confirmação verificável ou pendência de reconciliação.
- Estado: Versões anteriores, resultados por operação, outbox quando aplicável e evidências vinculadas ao conteúdo efetivo.
- Invariante: Um resultado não pode ser atribuído a artefato diferente do verificado; repetição não deve converter a mesma intenção em novo efeito lógico.

Compromissos de projeto:
- Verificação de versão impede sobrescrita silenciosa, mas pode exigir recomposição do patch após concorrência.
- Registrar intenção e resultado melhora rastreabilidade, acrescentando armazenamento e contratos de retenção.

## P015:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: alterar o arquivo entre leitura e aplicação do patch e perder a confirmação de uma operação externa; exigir conflito no primeiro caso e consulta ou deduplicação no segundo.

Plano de avaliação proposto:
Comparar execução sem controle de versão e com precondições em cenários concorrentes conhecidos. Medir sobrescritas indevidas, efeitos duplicados, conflitos legítimos e recuperação. Verificar também que hashes são recalculados sobre o artefato realmente consumido.

Comparações:
- T233 (complements): Validação de patch verifica precondições e aplicabilidade.
- T162 (complements): Idempotência controla repetição de uma intenção.

Afirmação rastreável:
Identificadores idempotentes e outbox ajudam a controlar repetição e a fronteira entre alteração local e notificação.
Suporte: related; fontes: C-S026, V3D-S018
Limite: O controlador e o vínculo entre hashes e operações são uma proposta; não há garantia universal de exatamente uma vez.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## P015:C07 — estrategia_3_30b

NOVA CAMADA v4 — Vai além do hash-base e da reconciliação já tratados: distingue igualdade de bytes de história de alterações, trata expiração da deduplicação e impede reutilizar uma identidade de operação com intenção diferente.

A→B→A: bytes iguais, história diferente
Proposta: quando a regra depende de nenhuma alteração intermediária, comparar somente conteúdo não detecta uma escrita seguida de restauração. Exigir revisão ou geração monotônica com comparação atômica no destino, incluindo identidade da criação quando uma chave pode ser apagada e recriada. Se o contrato depende apenas dos bytes atuais, a alteração histórica pode ser irrelevante; não impor bloqueio sem necessidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

Janela finita de idempotência
Persistir a semântica de retenção do destino junto da operação. Uma chave que já foi expurgada pode representar nova requisição; retomada muito tardia precisa consultar recibo/status ou permanecer em reconciliação. Manter registro local não obriga o servidor remoto a deduplicar. Versionar a política: comportamento de respostas falhas e retenção pode diferir entre versões de API.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

Identidade com impressão da intenção
Vincular operation_id a tenant, destino estável, versão da API e argumentos normalizados sob regra explícita. Reutilizar a chave com parâmetros diferentes deve ser conflito, não retry. Duas solicitações legítimas iguais em conteúdo precisam de identidades distintas quando representam duas intenções; deduplicar apenas pelo hash dos argumentos pode suprimir trabalho válido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

USO AVANÇADO — Retomada após longa indisponibilidade
Cenário: O agente reaparece depois da janela de deduplicação remota.
Estratégia: Preservar a identidade original e verificar evidência do destino; não gerar chave nova para contornar estado desconhecido.
Papel do modelo pequeno: 3–14B interpreta status documentado; o controlador decide conforme contrato de retenção.
Aceite proposto: Simular expurgo da chave e confirmar que resultado incerto não dispara efeito duplicado automaticamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

USO AVANÇADO — Configuração alterada e restaurada
Cenário: Outro processo modifica um recurso e devolve o conteúdo inicial antes do commit.
Estratégia: Usar comparação atômica da revisão de modificação e identidade da criação quando histórico importa; rejeitar guardas somente de conteúdo nesse contrato.
Papel do modelo pequeno: LLM propõe mudança; backend aplica precondição de revisão, sem delegar detecção ao texto.
Aceite proposto: Teste A→B→A é rejeitado quando o contrato exige ausência de intervenção; igualdade de bytes continua aceita quando for o requisito correto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: 3–7B: emitir intenção estruturada sem fabricar IDs de recursos ou revisar sozinho as regras de deduplicação.
8–14B: 8–14B: interpretar respostas e conflitos documentados, mantendo decisão temporal no controlador.
15–30B: 15–30B: investigar casos ambíguos com evidências; capacidade maior não recupera recibo inexistente.
Requisitos de treino/runtime: Exige contratos de retenção, comparação atômica e namespace do destino; restauração de backend também precisa de política de épocas.
Não aplicar quando: Não confundir um hash de conteúdo, versão reiniciável ou chave expirada com garantia histórica permanente.

## P015:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Este ID P nomeia um componente editorial. Seus exemplos são analogias; nenhuma empresa é apresentada como usuária de um produto LAI com esse nome.

V4C-C001 — Amazon Web Services / EC2 RunInstances
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: A AWS descreve uso de identificadores fornecidos pelo cliente na criação de instâncias e reutilização pelos SDKs/CLI em tentativas repetidas.
Mecanismo documentado: O identificador conserva a intenção; parâmetros divergentes são rejeitados e respostas semanticamente equivalentes permitem recuperar confirmação perdida.
Correspondência com esta base: Identidade, parâmetros e resposta exemplificam princípios do controlador editorial, sem existência do componente LAI.
Transferência proposta para modelo pequeno: Proposta: um modelo 3–30B produz argumentos; código determinístico atribui a intenção e impede que reparo textual gere uma segunda operação. Validar timeout depois do efeito e parâmetros divergentes.
Limite: Caso de API de infraestrutura, sem LLM. Retenção e identidade são específicas do serviço; não prova exactly-once universal nem ganho de qualidade de modelos.
Fontes: C-S026.

V4C-C026 — Anthropic / Scion
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: laboratório de IA — contado separadamente.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Monorepo migrado para sistema interno de controle de versões; CI e agentes usam consultas e materialização seletiva.
Mecanismo documentado: Changesets e conteúdo imutáveis, dados derivados, caches hierárquicos e alteração de referência separada da criação de conteúdo.
Correspondência com esta base: Publicação e autoria por versão inspiram o componente editorial.
Transferência proposta para modelo pequeno: Proposta: armazenar artefatos por conteúdo e ler arquivos necessários; adotar princípios sem recriar Scion ou atribuir seus ganhos à faixa 3–30B.
Limite: Infraestrutura excepcional, sistema distinto de Git; uma adoção, não um caso para cada cache ou ferramenta.
Fontes: V4C-S027.

V4C-C004 — Uber / Up CD
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: O relato de Up CD descreve adoção interna de deployment automatizado, gates implementados em Cadence e incorporação de ações manuais na visão do serviço.
Mecanismo documentado: Eventos de commits identificam serviços afetados; workflows de gates liberam estágios conforme condições e mantêm vínculo entre revisão e estado implantado.
Correspondência com esta base: Vínculo entre revisão e implantação ilustra integridade de execução.
Transferência proposta para modelo pequeno: Proposta: modelo pequeno prepara mudança e diagnóstico; código verifica commit, resultados e condições antes de promover uma etapa. Retorno do modelo nunca substitui o gate determinístico.
Limite: Caso de CD de software, não benchmark de agente de programação. Gates relevantes ao usuário precisam ser definidos e medidos localmente.
Fontes: V4C-S002.

V4C-C014 — Uber / MCP Gateway e Omni MCP
Evidência: produção documentada; analogia; não é adoção deste componente. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber descreve seu gateway central de interações MCP, com registro de ferramentas e descoberta incremental por intenção.
Mecanismo documentado: Omni MCP separa descobrir servidor, listar ferramentas, obter schema e invocar; o gateway projeta campos de resposta e propaga configurações revisadas ao plano de execução.
Correspondência com esta base: Revisões e controle de exposição apoiam integridade editorial.
Transferência proposta para modelo pequeno: Proposta: oferecer a 3–7B busca curta de ferramentas e schema apenas do candidato escolhido; 8–30B podem compor chamadas delimitadas, mantendo habilitação e projeção verificadas fora da LLM.
Limite: Um caso de gateway, sem contar cada servidor interno. Projeção reduz informação e precisa preservar campos indispensáveis; heartbeat de descoberta não é conclusão de trabalho.
Fontes: V4C-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: P015 é proposta. APIs idempotentes, Git e controles de repositório são analogias delimitadas; não se atribui às empresas o controlador LAI completo.
Consultas registradas: V4C-Q001, V4C-Q005, V4C-Q015, V4C-Q022.

## P015:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. P015 → T162 [complements]
Como combinar: Aplicar deduplicação sob identidade de intenção, escopo e janela conhecidos.
Interface: Operation_id, fingerprint de argumentos, namespace, API_version e política de retenção.
Condição: Uma ação pode ser repetida ou retomada após interrupção longa.
Aceite proposto: Mesma chave/intenção retorna estado conhecido; chave com intenção diferente é recusada e chave expurgada não é presumida segura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

2. P015 → T072 [complements]
Como combinar: Escolher revisão de estado capaz de representar o requisito de concorrência.
Interface: Content_hash, revisão de modificação, geração/criação e guarda atômica.
Condição: O efeito depende da história de alterações e não apenas de bytes atuais.
Aceite proposto: Teste de alteração e restauração distingue equivalência de conteúdo de continuidade da versão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4D-S021, V3C-S025, V3C-S028, V3D-S018. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não normalizar argumentos de modo a apagar diferenças semanticamente relevantes.
- Não inferir sucesso da própria operação pela existência de recurso semelhante.
- Não tratar restauração de snapshot do backend como continuidade automática da mesma época.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Injetar expiração de chaves, troca de parâmetros, exclusão/recriação e restauração A→B→A nos sistemas comparados. Medir duplicação e supressão indevida; essas falhas podem persistir mesmo com um gerador de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T072, T162, T200, T233, P011, P012, P013

## Fontes primárias associadas

### C-S026 — Making retries safe with idempotent APIs

[https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identificador de intenção do cliente permite repetir uma solicitação sem repetir seu efeito lógico.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S029 — Transaction Isolation

[https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Níveis de isolamento e anomalias de concorrência, incluindo serialização.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2C-S002 — PostgreSQL Documentation — Transactions

[https://www.postgresql.org/docs/current/tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atomicidade, commit, rollback e visibilidade das alterações transacionais.

Limite: Garantias referem-se à transação no banco configurado; serviços externos e armazenamento independente não entram automaticamente nela.

### V3D-S018 — AWS — Transactional outbox pattern

[https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Alteração local e evento pendente na mesma transação; publicação posterior pode duplicar mensagens.

Limite: Outbox não torna toda chamada externa exatamente uma vez; consumidores precisam de idempotência.

### V4D-S021 — Making retries safe with idempotent APIs — publicação atual no AWS Builder Center

[https://builder.aws.com/content/3Ev0BENTyBr0XxzRk5FDZzgNYos/m](https://builder.aws.com/content/3Ev0BENTyBr0XxzRk5FDZzgNYos/m)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Identidade fornecida pelo cliente, equivalência de resposta, diferença entre mesma aparência e mesma intenção e limites de repetição em APIs.

Limite: Não fornece garantia universal entre APIs; conferir contrato, retenção e versão do destino. Novo URL mantém acessível a fonte do Builders Library.

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

### V4C-S002 — Continuous deployment for large monorepos

[https://www.uber.com/us/en/blog/continuous-deployment/](https://www.uber.com/us/en/blog/continuous-deployment/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Up CD utiliza Cadence para etapas e gates, relaciona eventos a commits e incorpora implantações manuais ao estado observado.

Limite: Relato primário do operador; descreve o sistema e o período da publicação. Não reproduz resultados, não comprova disponibilidade atual de cada detalhe e não demonstra desempenho de modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S027 — Redesigning source control at Anthropic

[https://www.anthropic.com/research/redesigning-source-control](https://www.anthropic.com/research/redesigning-source-control)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implantação de Scion, dados endereçados por conteúdo, leitura sob demanda, hierarquia de caches e publicação separada de changesets.

Limite: Sistema interno distinto de Git, feito para escala e recursos excepcionais; não é recomendação geral de substituição.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
