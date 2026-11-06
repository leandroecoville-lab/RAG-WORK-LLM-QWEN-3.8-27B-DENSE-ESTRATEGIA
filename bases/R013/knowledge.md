# R013 — Letta MemFS

**Nome canônico:** Letta MemFS — memória versionada em arquivos  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** MemFS; Letta / Letta MemFS

## R013:C01 — conceito

MemFS projeta a memória de longo prazo de um agente Letta em um checkout Git, manipulável com ferramentas comuns de arquivos. A documentação também o chama de context repository. O mecanismo combina persistência, organização hierárquica e carregamento seletivo; não transforma todos os arquivos em contexto simultaneamente nem valida a veracidade das memórias.

Como funciona:
- Arquivos de memória possuem caminhos e descrições; índices MEMORY.md ajudam o agente a localizar conteúdo aprofundado.
- Na documentação atual, arquivos na raiz permanecem no prompt; diretórios indexados são consultados sob demanda.
- Edições locais precisam ser confirmadas e sincronizadas para compor a memória compartilhada em outros computadores.

Nota de nomenclatura: O nome combinado da edição anterior é preservado como alias histórico. Não houve instalação nem teste de sincronização real.

## R013:C02 — aplicacao

Quando usar:
- Procedimentos, decisões e preferências textuais que precisam de histórico e inspeção.
- Conhecimento de projeto maior que o orçamento disponível no prompt.

Quando não usar:
- Eventos concorrentes de alto volume que exigem transações ou grandes arquivos sem valor contextual.

Implementação proposta:
- Proposta: definir poucos arquivos essenciais, diretórios por assunto e índices que descrevam quando consultar cada conteúdo.
- Registrar fonte, data e responsável por memória importante; separar fatos comprovados de hipóteses e instruções.
- Estabelecer fluxo de revisão, commit, sincronização e resolução de conflitos antes de permitir escritores concorrentes.

Aplicação LAI proposta:
Proposta LAI: experimentar MemFS para manuais e decisões de engenharia, mantendo eventos operacionais volumosos no armazenamento definido para sua carga.

## R013:C03 — riscos_validacao

Armadilhas:
- Commit local e sincronização remota são etapas distintas; não declarar propagação antes de confirmá-la.
- O blog original descreve system/; a documentação atual reserva essa organização a agentes antigos.

Métricas sugeridas:
- Tokens fixos de memória, recuperação por consulta, conflitos de edição e atraso de sincronização.

Testes propostos:
- Proposta: editar sem push, abrir outra sessão e conferir a diferença entre estado local e compartilhado.
- Alterar o mesmo fato em dois escritores e verificar preservação da proveniência e resolução explícita da divergência.

## R013:C04 — perguntas_proveniencia

Pergunta: MemFS exige carregar todo o repositório no prompt?
Resposta: Não. Sua hierarquia distingue conteúdo sempre carregado de referências lidas conforme a necessidade.

Pergunta: Um commit prova que a memória é verdadeira?
Resposta: Não. Ele registra uma versão; a confirmação factual depende das evidências e da revisão do conteúdo.

Pergunta: MemFS inclui automaticamente embeddings?
Resposta: Não. A documentação distingue busca comum de arquivos e modos semânticos ou híbridos opcionais, com componentes adicionais e indexação.

Pergunta: Busca de conversa e busca de memória são a mesma operação?
Resposta: Não. Conversas possuem histórico próprio; arquivos MemFS representam memória organizada. Encontrar um item num desses acervos não comprova cobertura do outro.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R013:C05 — mecanismo_avancado

No MemFS atual, arquivos de memória na raiz são carregados a cada turno; agentes antigos podem usar a pasta system. Diretórios com índice MEMORY.md permanecem fora da janela até consulta. Essa organização transforma nomes e descrições em sinais de descoberta. O mecanismo não inclui índice semântico por padrão: busca por arquivos, memória vetorial opcional e busca no histórico conversacional são capacidades separadas com requisitos próprios.

Condição de contorno:
Um arquivo persistido num diretório profundo pode continuar invisível na prática se o índice não orientar sua descoberta ou se o agente não abrir a referência necessária.

Contrato proposto:
- Entradas: Checkout do agente, arquivos com metadados, índices de diretórios e configuração de busca efetivamente instalada.
- Saídas: Contexto essencial carregado, referências descobríveis e conteúdo aprofundado lido sob demanda.
- Estado: Commits, alterações locais, sincronização e índices opcionais com revisões correspondentes.
- Invariante: Alegar que uma memória foi usada exige leitura ou carregamento efetivo; presença no repositório não basta.

Compromissos de projeto:
- Arquivos essenciais na raiz simplificam acesso recorrente e consomem orçamento em toda chamada.
- Hierarquia reduz contexto ativo e depende de bons índices; busca semântica opcional acrescenta instalação, indexação e manutenção.

## R013:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar memória profunda sem atualizar seu índice e depois mover o arquivo. A avaliação deve detectar perda de descoberta e referências quebradas, mesmo que o conteúdo continue versionado no Git.

Plano de avaliação proposto:
Avaliação proposta: comparar organização plana e hierárquica com tarefas que exigem referências antigas. Medir memória encontrada, arquivos abertos, tokens fixos e sincronização entre computadores; avaliar busca lexical e semântica como configurações distintas.

Comparações:
- R014 (complements): R014 é um alias desta mesma referência, preservado para discutir colaboração; não representa outro mecanismo independente.
- T014 (specializes): MemFS concretiza carregamento progressivo por organização de arquivos e índices.

Afirmação rastreável:
A documentação MemFS descreve raiz ativa, diretórios sob demanda, ausência de índice vetorial padrão e sincronização via commits e push.
Suporte: direct; fontes: A-S010
Limite: Documentação dinâmica consultada em 2026-11-05; instalações antigas e modalidades locais podem ter organização e disponibilidade distintas.

Nota de pesquisa:
MemFS reaberto em 2026-11-05. Mantida a equivalência nominal oficial com context repository e a identidade canônica R013. Aprofundamento baseado na documentação atual, sem afirmar instalação de mods, índice semântico ou sincronização no ambiente do usuário. Contratos e testes são propostas.

## R013:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou residência e carregamento do MemFS. Aqui a proposta organiza arquivos por estabilidade, custo de leitura e frequência de mudança.

Projeto e decomposição
Separe identidade e convenções estáveis de notas voláteis de tarefa. Arquivo sempre carregado deve ser pequeno e discriminativo; detalhes grandes ficam em caminhos descobríveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Controle adaptativo
Projete índice para distinguir arquivos parecidos e declarar quando abri-los. Nome de arquivo sozinho pode não informar escopo; descritores devem apontar finalidade e limites.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

Validação contrafactual
Compare memória plana e organização por estabilidade. Meça arquivos abertos sem uso, leituras repetidas e instruções antigas aplicadas; contar tokens iniciais não capta custo de expansão. Unidade de avaliação: repositório de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Agente de projeto longo
Cenário: Memória reúne decisões e notas temporárias.
Estratégia: Manter visão inicial de objetivos e índices, carregar módulo ativo e arquivar detalhes concluídos com referência. Não promover nota temporária para convenção.
Papel do modelo pequeno: 3–7B lê índice; 8–14B trabalha por módulo.
Aceite proposto: Retomada deve carregar decisões vigentes sem trazer hipóteses encerradas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

USO AVANÇADO — Conhecimento compartilhado
Cenário: Vários agentes precisam dos mesmos procedimentos.
Estratégia: Separar conteúdo comum de notas individuais, versionar correções e testar se cada leitor abre procedimento completo quando necessário.
Papel do modelo pequeno: 15–30B integra conflitos.
Aceite proposto: Mudança compartilhada deve ser visível na revisão declarada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S010, V2B-S003, V3A-S046.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de índice curto e arquivos com estrutura explícita.
8–14B: Agente que carrega e atualiza módulos limitados.
15–30B: Integrador de memórias compartilhadas com conflitos entre fontes.
Requisitos de treino/runtime: MemFS e versão do produto identificados, arquivos acessíveis e política de edição; não presumir indexação semântica automática.
Não aplicar quando: Arquivos crescem sem catálogo ou usuários confundem conteúdo no disco com conteúdo recebido pelo modelo.

## R013:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C028 — Letta / MemFS e Context Repositories
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve memória em arquivos e repositórios de contexto.
Mecanismo documentado: Conteúdo seletivamente residente, edição de arquivos e versionamento Git.
Correspondência com esta base: MemFS é referência principal.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar índice de arquivos conciso e carregar procedimento por referência exata; validar conflitos.
Limite: Um único sistema não vira dois casos por alias; não prova conhecimento correto nem busca semântica automática. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S010, V2B-S003, V3A-S046.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R013:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R013 → T014 [complements]
Como combinar: Usar descritores para selecionar arquivos antes da carga.
Interface: Caminho, escopo, versão e finalidade.
Condição: Descrição distinguir recursos próximos.
Aceite proposto: Testar arquivo raro necessário à tarefa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R013 → T076 [requires]
Como combinar: Preservar revisão das alterações de memória.
Interface: Commit, arquivo, diff e origem.
Condição: Merge semântico revisado quando necessário.
Aceite proposto: Detectar duas decisões incompatíveis em arquivos separados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S010, V2B-S003, V3A-S046. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir busca de conversa com índice semântico dos arquivos.
- Não contar R014 como implantação adicional deste mesmo sistema.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade de retomada e custo de leitura; estrutura de arquivos não compensa instruções ambíguas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R002, R014, R027, T014, T053, T072, T076

## Fontes primárias associadas

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V2B-S003 — Introducing Context Repositories: Git-based Memory for Coding Agents

[https://www.letta.com/blog/context-repositories/](https://www.letta.com/blog/context-repositories/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Origem do nome Context Repositories, memória em Git, divulgação progressiva e trabalho de subagentes em worktrees.

Limite: Anúncio histórico de fevereiro de 2026; descreve system/ e ativação antigos. Regras atuais de MemFS prevalecem. Não houve reprodução dos fluxos descritos.

### V3A-S046 — Letta Shared memory

[https://docs.letta.com/concepts/shared-memory](https://docs.letta.com/concepts/shared-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: MemFS pertence a um agente; repositório compartilhado pertence à organização e requer commit, push e pull para sincronização entre checkouts.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
