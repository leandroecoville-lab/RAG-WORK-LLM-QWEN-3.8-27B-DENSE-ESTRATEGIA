# T042 — Token-Based Window

**Nome canônico:** Token-Based Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T042  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela baseada em tokens

## T042:C01 — conceito

Mantém uma seleção de mensagens ou trechos respeitando orçamento em tokens do modelo. É mais adequada que contar caracteres para controlar a janela, mas precisa incluir overhead do template, ferramentas e espaço de saída. A estimativa deve usar tokenizer compatível quando disponível.

Como funciona:
- Calcular orçamento de entrada após reservar saída e margens.
- Contar todos os blocos da requisição.
- Selecionar unidades completas sem ultrapassar o limite efetivo.

## T042:C02 — aplicacao

Quando usar:
- Históricos com mensagens e retornos de tamanhos muito diferentes.
- Modelos locais com memória e janela limitadas.

Quando não usar:
- Não tratar estimativa aproximada de caracteres como contagem exata do servidor.

Implementação proposta:
- Proposta: separar orçamento fixo, evidências, histórico e saída.
- Contar schemas e template de chat além do texto visível.
- Falhar de forma explícita quando o conteúdo obrigatório não cabe, permitindo dividir a tarefa.

Aplicação LAI proposta:
Proposta LAI: definir orçamento a partir da configuração real do checkpoint e servidor do Qwen; não copiar um número de janela de outra instalação.

## T042:C03 — riscos_validacao

Armadilhas:
- Tokenizer incorreto subestima tokens de código e português.
- Uma expansão automática de ferramenta pode consumir espaço não contabilizado.

Métricas sugeridas:
- Diferença entre tokens estimados e medidos pelo backend.
- Percentual de chamadas rejeitadas por limite de contexto.

Testes propostos:
- Testar entradas com acentos, JSON, emojis e código.
- Reservar uma resposta longa e verificar que a entrada foi reduzida antes de chamar o modelo.

## T042:C04 — perguntas_proveniencia

Pergunta: O orçamento de entrada é igual à janela total?
Resposta: Geralmente não. É preciso reservar geração e contabilizar overhead conforme o backend.

Pergunta: Devo cortar exatamente no último token disponível?
Resposta: Não. Uma margem operacional reduz falhas por diferenças de contagem e expansão de conteúdo.

Pergunta: A janela nominal é um orçamento suficiente?
Resposta: Não. Verifique as regras do modelo e servidor para entrada, saída e expansões. O valor anunciado não descreve sozinho o envelope operacional.

Pergunta: Devo reduzir sempre a mensagem mais longa?
Resposta: Não. Ela pode conter a única evidência necessária. O custo em tokens precisa ser combinado com obrigatoriedade e relações entre unidades.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T042:C05 — mecanismo_avancado

A contagem útil é da requisição efetivamente serializada, incluindo definições de ferramentas e conteúdo multimodal conforme o backend. Um estimador local pode errar de forma sistemática; medir seu resíduo permite escolher margem operacional baseada nos casos observados. O orçamento também precisa suportar resultados de ferramentas ainda não recebidos, evitando preencher toda a janela antes de uma etapa que necessariamente acrescentará conteúdo.

Condição de contorno:
A garantia de caber deixa de valer se o servidor expande referências, muda o template ou aplica uma contagem que o estimador não representa.

Contrato proposto:
- Entradas: Requisição montada, estimador compatível, reserva de geração e necessidades previstas da próxima etapa.
- Saídas: Plano de seleção e estimativa total com margem e componentes de custo identificados.
- Estado: Versão do tokenizer, template, erros observados e política para conteúdo obrigatório excedente.
- Invariante: A reserva não é consumida implicitamente por schemas ou resultados adicionados depois da contagem.

Compromissos de projeto:
- Contagem precisa melhora utilização e pode exigir chamada adicional ao provedor.
- Margens conservadoras reduzem rejeições e também diminuem evidência disponível; devem ser ajustadas por classe de requisição.

## T042:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma ferramenta cujo schema é grande após selecionar mensagens. A validação final deve recomputar o total e reduzir apenas conteúdo opcional ou dividir a tarefa.

Plano de avaliação proposto:
Avaliação proposta: comparar contagem aproximada e compatível com o backend; medir erro absoluto, rejeições e evidência descartada. Estratificar por idioma, ferramentas e anexos; escolher margem conforme custo observado de falha e perda de contexto.

Comparações:
- T041 (alternative): Um orçamento em tokens controla tamanho real de forma mais direta que quantidade de mensagens.
- T045 (complements): Adiar definições de ferramentas pode reduzir tokens ativos, sem eliminar o catálogo necessário ao serviço.

Afirmação rastreável:
A documentação de memória curta do LangChain apresenta truncamento por orçamento de tokens e política de seleção de fronteiras.
Suporte: direct; fontes: A-S003
Limite: A fonte não estabelece a contagem exata de todos os provedores nem uma margem universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T042:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 contou serialização completa. Aqui orçamento por tokens é distribuído por incerteza de saída e custo de evidência.

Projeto e decomposição
Reserve saída conforme tipo de resposta e modo de execução. Uma extração de campos tem distribuição diferente de uma análise aberta; reserva fixa desperdiça espaço ou produz truncamento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S015.

Controle adaptativo
Selecione evidências pelo custo marginal de incluir unidade completa. Um trecho barato pode exigir cabeçalho e definição adicionais; orçamento precisa cobrar esse conjunto, não só o texto selecionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S015.

Validação contrafactual
Compare reserva fixa e reserva por tarefa. Meça estouro, término por limite, evidências excluídas e respostas aceitas; validar quantis em tráfego novo, não apenas no conjunto usado para escolher reservas. Unidade de avaliação: requisição serializada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S015.

USO AVANÇADO — Serviço local concorrente
Cenário: Várias sessões competem por memória.
Estratégia: Reduzir orçamento por sessão conforme concorrência medida, preservando campos obrigatórios; encaminhar tarefa grande para fila própria.
Papel do modelo pequeno: 3–7B responde pacotes curtos.
Aceite proposto: Não ultrapassar memória de pico com carga simultânea.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S015.

USO AVANÇADO — Relatório com tabela
Cenário: Número de linhas determina saída.
Estratégia: Estimar saída por schema e linhas, reservar espaço e dividir relatório quando conjunto obrigatório não couber.
Papel do modelo pequeno: 8–14B gera seções; código monta tabela.
Aceite proposto: Nenhuma linha pode desaparecer por término prematuro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Saída estruturada curta com reserva previsível por schema.
8–14B: Resposta de tamanho moderado com estimativa por número de evidências.
15–30B: Síntese extensa apenas quando reserva e hardware sustentarem contexto e saída.
Requisitos de treino/runtime: Tokenizer e protocolo reais, telemetria de término e modelo de memória do servidor; parâmetros não definem sozinhos custo.
Não aplicar quando: O conjunto obrigatório excede a janela útil e a aplicação não permite decomposição.

## T042:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q011.

## T042:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T042 → T152 [complements]
Como combinar: Distribuir orçamento entre fases antes de montar entrada.
Interface: Cotas, prioridades e estimativa de saída.
Condição: Soma incluir overhead e reservas.
Aceite proposto: Trocar modelo e recalcular todas as cotas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T042 → T033 [requires]
Como combinar: Contar custo de unidades completas.
Interface: Bloco, dependências e tokens agregados.
Condição: Estruturas não poderem ser cortadas arbitrariamente.
Aceite proposto: Testar tabela cuja legenda torna o bloco maior que a cota.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não descontar tokens cacheados do limite da janela.
- Não usar caracteres como tokens sem medir erro da aproximação.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade com orçamento efetivo igual; respostas truncadas entram na taxa de falha.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T024, T152, T168

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S038 — Tool search tool

[https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas e carregamento adiado de schemas no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S015 — Context caching overview

[https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Caching implícito e explícito, metadados de uso e duração; recurso disponível.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
