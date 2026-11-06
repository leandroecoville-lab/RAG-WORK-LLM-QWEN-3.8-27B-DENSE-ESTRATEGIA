# T210 — Session Rotation

**Nome canônico:** Session Rotation  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T210  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** renovação de sessão; context reset com handoff

## T210:C01 — conceito

Padrão operacional de encerrar uma sessão de agente e iniciar outra usando estado persistido, referências e objetivos explícitos. A rotação reduz a dependência de um histórico extenso, mas exige reconstruir o contexto necessário. Não é um recurso universal com o mesmo comando em todos os produtos.

Como funciona:
- Escolher uma fronteira estável: etapa concluída, contexto pressionado ou mudança de especialidade.
- Persistir objetivo, revisão do código, evidências, pendências e efeitos externos ainda incertos.
- A próxima sessão valida esse pacote contra o ambiente antes de assumir a continuação.

## T210:C02 — aplicacao

Quando usar:
- Tarefas longas atravessando janelas de contexto ou execução interrompida por limites operacionais.

Quando não usar:
- No meio de uma operação externa cujo resultado não foi registrado nem pode ser reconciliado.

Implementação proposta:
- Proposta: atribuir ID ao trabalho durável e IDs próprios às sessões sucessivas.
- Gerar handoff com próximo passo, critérios de conclusão, hashes e resultados de testes, preservando autorizações relevantes.
- Iniciar a sessão seguinte lendo instruções de projeto, status do repositório e evidências recentes.
- Resolver divergências entre handoff e ambiente; impedir que duas sessões se tornem escritoras simultâneas da mesma etapa.

Aplicação LAI proposta:
Proposta LAI: permitir renovação de contexto ao terminar micro-missões, mantendo um identificador de trabalho e evidências persistentes entre sessões.

## T210:C03 — riscos_validacao

Armadilhas:
- Uma sessão nova pode repetir exploração já feita ou perder restrições.
- Um resumo desatualizado pode mencionar arquivos que mudaram.
- Rotacionar frequentemente acrescenta custo de reconstrução.

Métricas sugeridas:
- Tempo para retomar trabalho útil; reexploração; perda de requisitos; conflitos entre sessões.

Testes propostos:
- Retomar de um pacote incompleto e exigir identificação dos campos ausentes.
- Alterar o commit depois do handoff e verificar detecção da divergência.
- Interromper após envio externo e exigir reconciliação antes de repetir.

## T210:C04 — perguntas_proveniencia

Pergunta: Rotação mantém a memória interna do modelo?
Resposta: Não. A continuidade depende do material persistido e do que o novo contexto consegue recuperar.

Pergunta: É sempre melhor começar uma sessão nova?
Resposta: Não. Se o contexto atual ainda está adequado, a rotação pode aumentar custo e risco de perda de informações.

Pergunta: Encerrar a sessão cancela todos os efeitos antigos?
Resposta: Não. Operações remotas podem continuar; sua identidade e resultado devem atravessar a transferência.

Pergunta: O resumo basta para assumir a missão?
Resposta: Não quando há estado operacional. A nova sessão precisa localizar versões, pendências e critérios de conclusão verificáveis.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T210:C05 — mecanismo_avancado

Rotacionar sessões pode ser tratado como transferência de responsabilidade sobre uma versão de estado. A sessão antiga publica um ponto consistente; a nova confirma leitura e assume a geração vigente. Chamadas atrasadas da sessão anterior continuam possíveis, por isso escritas precisam ser associadas à revisão ou propriedade atual. Uma lease ajuda a detectar ausência de comunicação, mas não impede sozinha um processo antigo de escrever em serviço externo que ignora essa identidade.

Condição de contorno:
Se a sessão nova recebe apenas um resumo sem cursor, artefatos e operações pendentes, ela não consegue reconstruir o limite entre concluído e desconhecido.

Contrato proposto:
- Entradas: Estado confirmado, manifesto de transferência e geração atual da missão.
- Saídas: Sessão sucessora preparada e responsabilidade de escrita transferida.
- Estado: Geração, cursor, operações em voo e confirmação de leitura.
- Invariante: A sessão anterior não aplica atualizações obsoletas a um estado que já mudou de responsável.

Compromissos de projeto:
- Esperar drenar operações simplifica transferência e pode alongar a pausa.
- Transferir com operações pendentes reduz espera e exige reconciliação explícita.

## T210:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar uma nova sessão e entregar depois um resultado da antiga; exigir tratamento como resposta tardia vinculada à tentativa original, sem sobrescrever decisões novas.

Plano de avaliação proposto:
Comparar rotação em fronteira estável e rotação durante operação. Medir retomada correta, duplicação, perda de estado e tempo de reorientação. Aceitar a política quando preservar o mesmo objetivo e evidências sob interrupção.

Comparações:
- T211 (complements): Handoff carrega o manifesto e os pontos necessários à transferência.
- T243 (complements): Operações pendentes precisam de reconciliação após a troca de sessão.

Afirmação rastreável:
etcd fornece transações condicionais por revisão e leases que expiram na ausência de keepalive.
Suporte: related; fontes: V3C-S028
Limite: Essas primitivas apoiam coordenação; a proteção contra escritor antigo precisa alcançar cada destino de escrita.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T210:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 modelava transferência de propriedade do estado. A expansão define critérios para rotacionar, preserva contexto que não pode ser reconstruído e trata a retomada como operação verificável com custo próprio.

Motivo de rotação
Rotacione quando o histórico deixou de ajudar, a janela ficou pressionada ou uma fase terminou com fronteira clara. Reiniciar por um número fixo de turnos pode interromper raciocínio útil e aumentar reconsultas. Use sinais de ocupação e de término de fase, mantendo a decisão separada de erro de ferramenta ou falha do processo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S028, V4C-S014.

Pacote de retomada testável
Antes de encerrar, publique objetivo atual, artefatos, decisões, operações pendentes e próximo passo. Faça uma leitura de validação como se fosse um novo executor: referências resolvem, revisões coincidem e pendências não parecem concluídas. O custo dessa passagem deve entrar na comparação entre sessão longa e rotação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S004, V4C-S030.

Fronteira entre sessões
A sessão nova assume uma geração de estado; respostas atrasadas da anterior precisam ser classificadas por tarefa e revisão. Não descarte automaticamente um resultado válido só por ser antigo, mas não o publique sem verificar compatibilidade. Operações externas em andamento continuam pertencendo à mesma intenção até reconciliação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S026, V3C-S028.

USO AVANÇADO — Campanha com modelos locais
Cenário: Um agente trabalha horas em módulos separados.
Estratégia: Rotacione após validar e persistir uma micro-missão, não no meio de uma edição ainda sem teste. A nova sessão lê o mapa geral e a memória do módulo seguinte, reabrindo arquivos atuais. Preserve decisões compartilhadas que ainda condicionam os próximos módulos.
Papel do modelo pequeno: 3–7B executa micro-missões; 15–30B supervisiona fronteiras e integração.
Aceite proposto: Proposta: continuidade correta com menos contexto ativo e sem aumento excessivo de releituras.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S030, V3C-S028.

USO AVANÇADO — Mudança de papel
Cenário: Uma sessão coletou evidências e outra fará síntese crítica.
Estratégia: Publique matriz de alegações e referências, mantendo os documentos completos acessíveis. A nova sessão recebe perguntas de comparação e lacunas, reduzindo contaminação por hipóteses prematuras do coletor. Compare resultados para detectar perda de exceções na passagem.
Papel do modelo pequeno: 8–14B coleta; 15–30B sintetiza com critérios próprios.
Aceite proposto: Proposta: cobertura preservada e detecção de contradições após rotação de papel.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Sessões por tarefa estreita, com estado externo mínimo e verificável.
8–14B: Alternar coleta e análise mantendo fontes acessíveis por referência.
15–30B: Integração entre fases, avaliando se o pacote preserva dependências relevantes.
Requisitos de treino/runtime: Manifesto de estado, versões de artefatos e controle de geração; retorno de chamada antiga não publica sozinho.
Não aplicar quando: Não usar rotação para esconder falha não resolvida ou reiniciar orçamento e contadores.

## T210:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Relatos de planos persistidos e subagentes apoiam continuidade; não foi encontrado caso que comprove exatamente esta política de rotação como produto padronizado.
Consultas registradas: V4C-Q002, V4C-Q027.

## T210:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T210 → T211 [complements]
Como combinar: Handoff materializa o estado que a nova sessão precisa consumir.
Interface: Manifesto, revisão e operações pendentes.
Condição: Membros persistidos antes da publicação do manifesto.
Aceite proposto: Novo executor resolve referências e identifica próximo passo inequívoco.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2A-S004, V4C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T210 → T243 [complements]
Como combinar: Reconciliar efeitos enviados pela sessão anterior antes de novas tentativas.
Interface: Identidade da intenção e observações remotas.
Condição: A transferência mantém a mesma missão.
Aceite proposto: Nenhum efeito duplicado por tratar sessão nova como execução nova.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S026. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Resumo curto não prova completude de estado.
- Resultados tardios exigem checagem de versão e objetivo, não aceitação ou descarte automático.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare sessões rotacionadas e contínuas com os mesmos modelos e custo total. A técnica pode aliviar contexto de 3–30B, mas não recompõe informação que o handoff omitiu.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T211, T060, T243

## Fontes primárias associadas

### V2A-S004 — Effective harnesses for long-running agents

[https://www.anthropic.com/research/effective-harnesses-for-long-running-agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Continuidade entre sessões com progresso persistido, mudanças incrementais, commits e verificação.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S005 — Non-interactive mode

[https://developers.openai.com/codex/noninteractive/](https://developers.openai.com/codex/noninteractive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução programática do Codex, retomada de sessão e resultados consumíveis por automações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S006 — Run Claude Code programmatically

[https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Claude Code programático pelo CLI ou SDK; controle explícito de entrada, saída e ciclo de execução.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S028 — etcd v3.6 — API, revisions and transactions

[https://etcd.io/docs/v3.6/learning/api/](https://etcd.io/docs/v3.6/learning/api/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Revisões, transações condicionais e leases fornecem primitivas para coordenação e estado versionado.

Limite: Leases não desfazem efeitos já enviados a serviços que não participam do mesmo protocolo; desenho LAI é proposta.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

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

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
