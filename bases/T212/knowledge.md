# T212 — Auto-Compact por gatilho

**Nome canônico:** Auto-Compact por gatilho  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T212  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compactação automática por limiar

## T212:C01 — conceito

Compactação acionada automaticamente por uma condição de execução, como pressão no orçamento de contexto. O histórico selecionado é transformado em representação menor, preservando informações necessárias à continuidade. O gatilho e a forma de compactar são decisões distintas; nenhum percentual único serve para todos os modelos e ferramentas.

Como funciona:
- O monitor estima contexto ocupado e reserva espaço para resposta e retorno de ferramentas.
- Ao atingir a condição, seleciona material antigo ou menos útil e cria uma representação reduzida.
- A execução prossegue com instruções relevantes, estado atual e referências ao conteúdo externo preservado.

## T212:C02 — aplicacao

Quando usar:
- Conversas extensas com crescimento previsível ou ferramentas que produzem muito texto.

Quando não usar:
- Quando não existe margem para produzir e validar a compactação ou o único registro dos fatos seria descartado.

Implementação proposta:
- Proposta: definir gatilho com margem, histerese e limite de compactações sucessivas.
- Manter objetivos, restrições, decisões abertas, evidências recentes e identificadores de operações fora do descarte indiscriminado.
- Guardar histórico original recuperável e registrar origem, revisão e conteúdo substituído.
- Validar fatos críticos após compactar; reduzir a fonte de crescimento se uma única saída imediatamente lotar o contexto novamente.

Aplicação LAI proposta:
Proposta LAI: acionar compactação em fronteiras de etapa com um núcleo de estado verificado, deixando documentos completos acessíveis por referência.

## T212:C03 — riscos_validacao

Armadilhas:
- Resumos podem omitir negações, números ou condições.
- Compactação recorrente pode produzir deriva cumulativa.
- O mecanismo disponível em Claude Code não implica configuração idêntica em Codex ou outro runtime.

Métricas sugeridas:
- Tokens antes e depois; fatos críticos preservados; frequência de compactação; custo de recuperação posterior.

Testes propostos:
- Plantar uma restrição antiga e exigir seu cumprimento após o gatilho.
- Simular retorno grande de ferramenta e testar a reserva de espaço.
- Repetir compactações e medir se os mesmos identificadores e pendências permanecem corretos.

## T212:C04 — perguntas_proveniencia

Pergunta: Auto-Compact aumenta a janela física do modelo?
Resposta: Não. Reorganiza ou reduz o conteúdo enviado, dentro dos limites suportados pelo modelo e pelo runtime.

Pergunta: O gatilho precisa usar apenas tokens?
Resposta: Não. Pode combinar tokens, fase da tarefa e crescimento previsto, desde que a regra seja observável e testável.

Pergunta: Um resumo gerado em paralelo pode substituir o histórico inteiro?
Resposta: Somente se abranger exatamente essa versão; caso contrário, é necessário preservar a cauda que chegou depois.

Pergunta: Taxa de compressão alta prova boa compactação?
Resposta: Não. É preciso medir preservação de decisões, evidências e capacidade de continuar o trabalho.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T212:C05 — mecanismo_avancado

Compactação concorrente exige definir qual prefixo do histórico foi resumido. Enquanto o resumo é produzido, novos turnos podem chegar; substituí-los junto com o prefixo causaria perda. Uma proposta prende a compactação a um cursor e combina o resumo com a cauda posterior, validando a versão antes da troca. A documentação atual da Anthropic distingue compactação sob demanda, em segundo plano e por limiar, com contratos próprios para reinserção de turnos.

Condição de contorno:
O gatilho pode disparar corretamente e o resumo ainda omitir informação necessária; controle de ocupação e qualidade da síntese são problemas separados.

Contrato proposto:
- Entradas: Histórico versionado, cursor a compactar, instruções de preservação e orçamento.
- Saídas: Resumo do intervalo, referências e cauda não resumida preservada.
- Estado: Job de compactação, base observada e turno mais recente.
- Invariante: Nenhum turno posterior ao cursor é descartado por uma síntese que não o recebeu.

Compromissos de projeto:
- Compactação em segundo plano reduz pausa e introduz corrida de versões.
- Compactar mais cedo reduz pressão e pode repetir o custo de síntese sem necessidade.

## T212:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma decisão enquanto o resumo está em produção; exigir que a decisão apareça na cauda preservada ou em nova síntese corretamente identificada.

Plano de avaliação proposto:
Comparar compactação bloqueante e concorrente com a mesma política de preservação. Medir pausa, perda de fatos, tokens finais e recomputações. Separar compressão alcançada e capacidade de retomar a tarefa.

Comparações:
- T168 (complements): O limiar suave precisa reservar espaço para executar a compactação.
- T215 (alternative): Masking remove observações antigas sem produzir uma síntese semântica delas.

Afirmação rastreável:
A documentação Anthropic diferencia compactação por limiar e sob demanda, incluindo operação em segundo plano.
Suporte: direct; fontes: V3C-S031
Limite: Os recursos consultados são específicos da API e têm condições de suporte; a proposta não presume disponibilidade local.

Nota de pesquisa:
Fontes primárias reabertas nesta pesquisa; contratos, cenários de falha e avaliação são propostas editoriais.

## T212:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descrevia cursor de compactação e cauda concorrente. A expansão seleciona o que pode ser resumido, protege dependências abertas e mede o efeito da compactação sobre recuperação e término da tarefa.

Compactar por utilidade residual
Separe observações consumidas, decisões vigentes, evidências ainda necessárias e histórico de tentativas. Logs repetitivos podem ser candidatos; recibos de efeito e exceções pendentes precisam de preservação explícita. Um gatilho por ocupação inicia a análise, mas não decide sozinho quais unidades podem ser substituídas por resumo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S031.

Resumo com acesso ao original
O resumo deve indicar o intervalo coberto e referências para recuperar detalhes. Se a próxima etapa falhar por falta de informação, registre essa reconsulta como custo da política. Compressão que reduz tokens agora e exige várias releituras depois pode piorar a missão; compare custo completo e não somente tamanho do prompt seguinte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S031.

Efeito sobre comportamento
Resumir pode remover sinais de que uma abordagem já foi tentada ou de que o trabalho deve terminar. Preserve critérios de conclusão e hipóteses rejeitadas relevantes. Avalie repetição, duração e decisões após compactação, além de fidelidade textual. O mesmo modelo resumidor pode carregar o erro original para uma versão mais curta e convincente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S031, V3C-S032.

USO AVANÇADO — Longa sessão de ferramentas
Cenário: O histórico cresce com buscas e saídas intermediárias.
Estratégia: Quando atingir limite suave, compactar apenas o prefixo fechado e manter observações protegidas. Valide o resumo contra obrigações pendentes antes de trocar o contexto. Se a validação falhar, use poda seletiva ou rotação com artefatos, sem insistir em resumir tudo.
Papel do modelo pequeno: 3–7B extrai estados simples; 8–14B resume trechos com schema; 15–30B revisa exceções.
Aceite proposto: Proposta: menor contexto ativo sem perda de campos necessários à próxima decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S031, V4C-S031.

USO AVANÇADO — Campanha de programação
Cenário: Várias iterações do mesmo teste ocupam a janela.
Estratégia: Guarde logs integrais fora do prompt, resuma evolução do defeito e preserve último erro completo. Compare compactação por fase com masking de observações antigas. Não adote limiar de outro operador sem medir janela, tokenizer e custo dos próprios modelos.
Papel do modelo pequeno: 8–14B acompanha estado local; controlador mede gatilho e preserva logs.
Aceite proposto: Proposta: resolução, custo e repetição de hipóteses sob as duas políticas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S031.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extração de campos estáveis pode ser mais confiável que sumarização aberta de histórico extenso.
8–14B: Resumos por episódio com referências e limites curtos, verificados antes da inserção.
15–30B: Integração de episódios e exceções; compacidade não deve apagar obrigações críticas.
Requisitos de treino/runtime: Cursor consistente, reserva para resumir e validar, contagem real de tokens e arquivo integral recuperável.
Não aplicar quando: Não aplicar limiar de 400k de um harness com janela maior a um modelo pequeno sem compatibilidade real.

## T212:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 1.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C015 — Uber / Harnesses da Software Factory
Evidência: produção documentada; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: aplicação com LLM.
Uso observado: A Uber relata wrappers e políticas compartilhadas para sessões de agentes, incluindo subagentes com modelos mais econômicos e compactação configurada.
Mecanismo documentado: Seleção usa trabalho real, custo por resultado e qualidade; tool search, code-mode e políticas de cache reduzem trabalho repetido conforme o tipo de sessão.
Correspondência com esta base: Compactação automática é configurada nos harnesses interativos.
Transferência proposta para modelo pequeno: Proposta: avaliar separadamente líder e workers 3–30B, com orçamento de contexto ajustado à tarefa e ao checkpoint escolhido. Medir custo por alteração aceita mantendo modelo e mistura de tarefas constantes.
Limite: Os limiares e preços da publicação são específicos dos provedores e modelos usados; não são recomendados para janelas menores. Não se afirma que a frota use exatamente modelos das bandas propostas.
Fontes: V4C-S014.

V4C-C030 — JetBrains Research / autores / SWE-agent com políticas de contexto
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo compara estratégias de contexto em tarefas SWE-bench Verified.
Mecanismo documentado: Masking oculta observações anteriores; sumarização substitui histórico por texto sintetizado; avaliação considera resolução e custo.
Correspondência com esta base: Sumarização de trajetória é avaliada, sem provar uma política universal de gatilho de compactação.
Transferência proposta para modelo pequeno: Proposta: avaliar remoção seletiva antes de acrescentar um resumidor 3–30B, preservando observações necessárias ao próximo teste.
Limite: Pesquisa controlada não conta como produção; não generalizar comparação para todo domínio ou modelo.
Fontes: V4C-S031.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber relata compactação operacional; o estudo comparativo é pesquisa. Critérios e bandas propostos permanecem sem medição neste ambiente. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q009, V4C-Q028, V4D-Q019.

## T212:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T212 → T222 [complements]
Como combinar: Harness Uber usa ocupação de contexto como gatilho de compactação; a política local precisa de margem e contagem.
Interface: Ocupação, limiar e perfil do modelo.
Condição: Janela e implementação correspondem à configuração efetiva.
Aceite proposto: Compactação ocorre antes de estourar e deixa espaço para continuidade.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4C-S014. Casos: V4C-C015.

2. T212 → T215 [alternative]
Como combinar: Comparar resumo e masking para observações já consumidas, mantendo critérios iguais de tarefa e custo.
Interface: Histórico, observações protegidas e orçamento.
Condição: Ambas as políticas permitem recuperar detalhes necessários.
Aceite proposto: Escolher por resolução e consumo total, não pela sofisticação aparente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S031. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não resumir e apagar turnos que chegaram depois do cursor capturado.
- Não apresentar resultados do estudo com 32B como prova direta da faixa solicitada de até 30B.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare variantes dentro do mesmo harness antes de comparar portes. O estudo de masking mostra que estratégias simples merecem baseline, sem estabelecer uma vencedora universal.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T222, T004, T210

## Fontes primárias associadas

### V2A-S025 — How Claude Code works

[https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ciclo de contexto, ação e verificação; compactação automática e limites de checkpoints de arquivos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3C-S031 — Claude Platform — Compaction overview

[https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação sob demanda e por limiar, preservação de turnos recentes e gestão do bloco resultante.

Limite: Documentação dinâmica e recursos em beta na consulta; nenhuma flag ou suporte local foi presumido.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S031 — The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management

[https://arxiv.org/html/2508.21433v1](https://arxiv.org/html/2508.21433v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de masking e sumarização em agentes de engenharia de software, com custos e comportamento de continuidade.

Limite: Estudo experimental, não implantação de bigtech; resultados limitados a modelos, harness, tarefas e configurações avaliadas.

### V3C-S032 — Hypothesis — Stateful tests

[https://hypothesis.readthedocs.io/en/latest/stateful.html](https://hypothesis.readthedocs.io/en/latest/stateful.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Máquinas de estado e regras geram sequências de ações; modelos de referência permitem comparar comportamento acumulado.

Limite: Testes dependem de regras e invariantes corretos; não demonstram exaustividade de estados ou ausência total de defeitos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
