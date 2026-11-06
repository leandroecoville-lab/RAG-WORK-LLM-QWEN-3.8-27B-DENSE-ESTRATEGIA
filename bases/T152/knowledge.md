# T152 — Token Budget Allocation

**Nome canônico:** Token Budget Allocation  
**Grupo:** Orquestração, execução e resiliência  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T152  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** alocação de orçamento de tokens

## T152:C01 — conceito

Distribuição do orçamento de tokens entre instruções, ferramentas, estado, evidências, histórico e saída. É uma política de engenharia de contexto. A soma deve respeitar o limite efetivo do backend, incluindo template e tokens especiais; contagem por caracteres é apenas estimativa.

Como funciona:
- Contabilizar entrada com tokenizer e template do modelo de destino.
- Reservar espaço de saída antes de preencher o contexto recuperado.
- Selecionar evidências dentro do saldo, preservando conteúdo obrigatório.

## T152:C02 — aplicacao

Quando usar:
- RAG com muitos trechos candidatos.
- Agentes cujo histórico e schemas crescem durante a missão.

Quando não usar:
- Remover restrições essenciais só para caber mais texto de baixa utilidade.

Implementação proposta:
- Definir regiões obrigatórias e prioridades das opcionais.
- Registrar tokens previstos e reportados pelo backend para corrigir estimativas.
- Tratar separadamente limites de contexto, custo e saída máxima.

Aplicação LAI proposta:
Proposta: a Helena reservar instruções e estado antes de distribuir espaço entre fontes; o orçamento proposto deve ser calibrado no modelo realmente servido.

## T152:C03 — riscos_validacao

Armadilhas:
- Tokenizer diferente altera a contagem real.
- Uma ferramenta pode retornar volume inesperado e estourar a reserva.

Métricas sugeridas:
- Taxa de overflow e diferença entre contagem prevista e efetiva.
- Recall das evidências necessárias por token de entrada.

Testes propostos:
- Montar prompt próximo ao limite e conferir contagem após aplicar template.
- Injetar resultado de ferramenta grande e exigir recorte com referência ao original.

## T152:C04 — perguntas_proveniencia

Pergunta: Uma janela de 32 mil permite 32 mil tokens de entrada?
Resposta: Depende do backend e da reserva de saída; não se deve assumir.

Pergunta: Reduzir tokens sempre melhora?
Resposta: Não. Pode remover evidência crítica e aumentar erros.

Pergunta: Tokens de prefixo em cache deixam de ocupar contexto?
Resposta: Não necessariamente. Reutilização computacional e capacidade lógica da janela são dimensões distintas.

Pergunta: Por que reservar espaço para ferramentas futuras?
Resposta: Porque a chamada pode caber e seu resultado não; sem plano de ingestão, a observação necessária pode ser perdida.

Escopo das fontes:
A documentação de tokenização sustenta a contagem; regiões, prioridades e critérios de seleção são proposta editorial de controle de contexto.

## T152:C05 — mecanismo_avancado

O orçamento deve distinguir ocupação da janela e consumo acumulado da missão. Um prefixo reutilizado pode continuar ocupando contexto mesmo quando seu custo computacional ou faturado diminui. Resultados de ferramentas ainda não recebidos precisam de reserva ou estratégia de truncamento controlado. A contagem antecipada inclui template, definições de ferramentas e multimodalidade, e continua sujeita às particularidades do backend.

Condição de contorno:
Uma soma baseada apenas nos textos visíveis não protege o limite quando mensagens estruturadas acrescentam tokens ou quando a resposta esperada cresce.

Contrato proposto:
- Entradas: Capacidade do modelo, entrada montada, reservas de saída e resultados esperados.
- Saídas: Cotas por bloco, margem disponível e decisão de redução ou divisão.
- Estado: Estimativa inicial, consumo observado, reservas e orçamento acumulado.
- Invariante: Economia por cache não é tratada automaticamente como aumento da janela física.

Compromissos de projeto:
- Reservas generosas evitam estouro e podem excluir evidência útil.
- Redistribuição dinâmica usa melhor a janela e exige recontagem após mudanças relevantes.

## T152:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma ferramenta com schema longo e receber resultado maior que o previsto; exigir recontagem e política explícita de preservação dos dados necessários.

Plano de avaliação proposto:
Comparar cotas fixas e reservas adaptadas ao histórico de tamanho das ferramentas. Fixar tarefas e modelos. Medir estouro, qualidade de evidência, tokens descartados e custo acumulado. Ajustar a margem à variabilidade observada sem percentual universal.

Comparações:
- T168 (complements): Limites suave e rígido definem ações quando o orçamento se aproxima das fronteiras.
- T176 (complements): O plano estima demandas futuras que precisam de reserva.

Afirmação rastreável:
A contagem de tokens da Anthropic aceita mensagens estruturadas, ferramentas e entradas multimodais.
Suporte: direct; fontes: V3C-S022
Limite: O endpoint fornece estimativa específica do fornecedor e não conta por si todo o custo futuro da missão.

Nota de pesquisa:
Detalhamento e avaliação propostos; a fonte apoia o mecanismo, sem comprovar implementação LAI.

## T152:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou janela, gasto acumulado e reservas para ferramentas. A camada nova atribui utilidade a segmentos de contexto e vincula redução de tokens à preservação de obrigações verificáveis.

Orçamento por função documental
Reserve espaço para objetivo vigente, restrições, fatos, incertezas e saída. Cada segmento tem uma política de redução: logs podem virar referências, mas critérios de aceite não devem desaparecer por serem antigos. Distribuição fixa pode servir de baseline; adaptação só deve ocorrer com métricas de perda e custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V3C-S022.

Custo de ida e volta
Uma economia local pode gerar consultas adicionais depois. Remover detalhe de uma ferramenta reduz a entrada atual, mas pode exigir releitura ou induzir erro. Meça tokens e tempo até a tarefa aceita, incluindo resumos, buscas e reparos, para evitar otimizar um contador enquanto piora o fluxo completo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V4C-S013.

Reserva por etapa e tokenizer
Um plano com modelos diferentes não compartilha necessariamente a mesma contagem. Reconstrua o pacote no template do destino e reserve espaço para validação e resposta final. O custo faturado do prefixo e sua ocupação da janela continuam sendo medidas distintas, especialmente quando cache e compactação se combinam.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S022, V4C-S018.

USO AVANÇADO — Análise de repositório em janela curta
Cenário: O agente precisa alterar uma função sem carregar o projeto inteiro.
Estratégia: Inclua contrato, trecho alvo, chamadas relevantes e teste que define o comportamento. Use mapa para solicitar detalhes por necessidade; se a alteração afetar uma dependência, transfira parte do orçamento exploratório para essa evidência, preservando critérios de aceite.
Papel do modelo pequeno: 3–7B executa mudanças muito locais; 8–30B amplia escopo apenas com evidências recuperadas.
Aceite proposto: Proposta: medir regressões, leituras adicionais e tokens totais contra contexto amplo uniforme.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S014, V2A-S007.

USO AVANÇADO — Pesquisa com muitas respostas de ferramenta
Cenário: Cada consulta retorna texto e metadados volumosos.
Estratégia: Projete campos, mantenha referências e extraia somente fatos que respondem aos critérios. Antes de sintetizar, verifique cobertura; se uma lacuna depender de material omitido, recupere-o especificamente em vez de aumentar toda a janela.
Papel do modelo pequeno: 8–14B estrutura evidências; 15–30B integra conclusões condicionais.
Aceite proposto: Proposta: comparar sustentação, completude e custo incluindo recuperação posterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4C-S013, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Proposta: orçamento focado em fatos diretamente usados na próxima operação, com respostas curtas.
8–14B: Proposta: múltiplos segmentos documentais pequenos e reconsulta orientada por lacuna.
15–30B: Proposta: integração de evidências mais extensa, reservando verificação e conclusão desde o início.
Requisitos de treino/runtime: Contar com tokenizer e template reais; registrar consumo observado por etapa, não apenas estimativa prévia.
Não aplicar quando: Não reduzir contexto quando detalhes aparentemente acessórios determinam exceções ou identidade do recurso.

## T152:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Uber documenta otimizações por sessão e NVIDIA controles específicos; nenhum limiar corporativo é recomendado automaticamente para 3–30B.
Consultas registradas: V4C-Q009, V4C-Q014.

## T152:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T152 → T222 [feeds]
Como combinar: O monitor informa ocupação e erro de previsão para ajustar reservas futuras.
Interface: Contagem real, estimativa, segmento e revisão do template.
Condição: As unidades são comparáveis dentro do mesmo backend.
Aceite proposto: Detectar mudança de tokenizer por desvio sistemático de contagem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T152 → T214 [complements]
Como combinar: Poda por campos implementa parte da redução planejada sem reescrever todos os dados.
Interface: Lista de campos necessários e referência ao payload integral.
Condição: O contrato preserva informação de controle e incerteza.
Aceite proposto: Reexecutar casos com campo decisivo fora da projeção inicial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4C-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não gastar a reserva de verificação para produzir mais deliberação ou candidatos.
- Manter separados tokenização real, caracteres e preços do provedor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare modelos com orçamento total e critérios iguais, incluindo releituras. Um modelo pequeno bem contextualizado pode resolver tarefas delimitadas sem equivalência geral de janela ou conhecimento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T024, T168, T176

## Fontes primárias associadas

### C-S017 — Tokenizer — Transformers

[https://huggingface.co/docs/transformers/main_classes/tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tokenização e limites de comprimento oferecem mecanismos para contabilização; política de orçamento proposta é editorial.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3C-S022 — Claude Platform — Token counting

[https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contagem considera mensagens estruturadas, system prompt, ferramentas e entradas multimodais; contagem antecipada é estimativa.

Limite: Endpoint específico do fornecedor; reserva de saída e orçamento global da missão exigem política da aplicação.

### V3C-S015 — vLLM — Automatic Prefix Caching design

[https://docs.vllm.ai/en/latest/design/prefix_caching/](https://docs.vllm.ai/en/latest/design/prefix_caching/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Hash de blocos incorpora hash do pai, tokens e extras como IDs LoRA, conteúdo multimodal e salting de cache.

Limite: Layout e implementação dependem da versão; reutilização não é garantia de qualidade ou disponibilidade permanente do bloco.

### V4C-S014 — Running a Software Factory Efficiently at Uber Scale

[https://www.uber.com/us/en/blog/efficient-software-factory/](https://www.uber.com/us/en/blog/efficient-software-factory/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Harnesses internos, seleção por tarefas reais, modelos diferentes para subagentes, compactação, cache e code-mode.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S013 — Designing MCP Gateway Uber's MCP Management Platform

[https://www.uber.com/us/en/blog/designing-mcp-gateway/](https://www.uber.com/us/en/blog/designing-mcp-gateway/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Registro, descoberta gradual, schemas, proxy de execução, revisão de configurações e projeção de respostas em uso interno.

Limite: Relato primário delimitado à data e sistema; não houve reprodução. Números e escolhas do operador não definem ganhos, preços ou limites para a LAI ou modelos 3–30B.

### V4C-S018 — NVIDIA-Nemotron-Nano-9B-v2 — model card

[https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Controle de raciocínio, orçamento com margem de término, template, amostragem e parser de ferramentas específicos do modelo.

Limite: Conteúdo primário consultado. Model cards e blueprints documentam recursos e experimentos, não uma implantação identificada; relatos históricos não estabelecem estado atual nem ganhos em LAI.

### V2A-S007 — Repository map

[https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Mapa compacto de arquivos, símbolos e assinaturas para orientar contexto de código.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
