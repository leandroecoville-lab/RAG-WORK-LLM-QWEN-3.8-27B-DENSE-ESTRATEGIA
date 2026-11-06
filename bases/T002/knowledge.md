# T002 — Prompt Caching

**Nome canônico:** Prompt Caching  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T002  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cache de prompt

## T002:C01 — conceito

Reutiliza processamento de um prefixo de entrada já visto pelo servidor de inferência. A nova geração ainda é executada. O benefício depende do provedor, da identidade do prefixo, do prazo de retenção e da frequência de reutilização; não representa memória durável do agente nem acesso a fatos fora do prompt.

Como funciona:
- Organizar instruções e recursos estáveis antes da parte variável.
- O servidor identifica prefixos elegíveis para reutilização.
- Contabilizar leitura e escrita do cache separadamente da geração.

## T002:C02 — aplicacao

Quando usar:
- Muitas chamadas compartilham instruções, documentos ou definições de ferramentas.
- Conversas acumulam um prefixo estável entre rodadas.

Quando não usar:
- Não esperar benefício importante quando cada chamada altera o início inteiro da entrada.

Implementação proposta:
- Proposta: fixar ordem de schemas e versão das instruções.
- Instrumentar tokens de cache, latência até o primeiro token e custo por tarefa.
- Comparar execução fria e aquecida usando o mesmo conteúdo e critérios de qualidade.

Aplicação LAI proposta:
Proposta LAI: estabilizar políticas e contratos de ferramentas da Helena; configurar o cache conforme a versão efetivamente instalada do servidor, sem assumir suporte apenas pelo nome Qwen.

## T002:C03 — riscos_validacao

Armadilhas:
- Inserir um timestamp no começo pode reduzir reaproveitamento.
- Reutilizar resposta final é outro mecanismo e exige regras próprias de validade.

Métricas sugeridas:
- Taxa de tokens atendidos por cache.
- Economia líquida descontando armazenamento e escritas cobradas.

Testes propostos:
- Mudar um bloco do prefixo e observar os contadores reais do servidor.
- Verificar que duas perguntas diferentes geram respostas próprias mesmo compartilhando prefixo.

## T002:C04 — perguntas_proveniencia

Pergunta: Prompt caching aumenta a janela?
Resposta: Não. Reaproveita computação de uma entrada elegível; o limite de contexto continua aplicável.

Pergunta: É igual a semantic caching?
Resposta: Não. O cache semântico pode devolver uma resposta pronta; prompt caching reutiliza processamento da entrada.

Pergunta: Um cache hit demonstra que a informação continua atual?
Resposta: Não. Demonstra reutilização de processamento. Atualidade depende da versão das fontes e de decidir quais informações entram no prompt.

Pergunta: Devo aumentar o prompt apenas para obter cache?
Resposta: Só após comparar o custo total e a qualidade. Um hit artificial pode acrescentar trabalho e conteúdo irrelevante sem benefício líquido.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T002:C05 — mecanismo_avancado

O benefício econômico depende de quantas reutilizações acontecem antes de o prefixo mudar ou expirar. Se W é o custo da primeira gravação, R o custo de cada leitura e U o custo sem cache, uma sequência com m reutilizações economiza quando W+mR<(m+1)U. Todas as parcelas devem usar a mesma unidade e excluir economias imaginadas na geração da saída.

Condição de contorno:
Prefixos frequentemente alterados, pedidos abaixo dos requisitos do provedor ou baixa repetição podem impedir amortização, mesmo com conteúdo conceitualmente semelhante.

Contrato proposto:
- Entradas: Prefixo serializado estável, modelo e configuração documentados.
- Saídas: Resposta nova e indicadores de leitura ou criação de cache reportados.
- Estado: Revisões do prefixo, intervalos entre chamadas e uso observado.
- Invariante: Um ganho de cache só é contabilizado quando houver evidência de reutilização no serviço.

Compromissos de projeto:
- Colocar material estável primeiro favorece reutilização, mas não justifica preservar instruções obsoletas.
- Compactar pode recuperar contexto e simultaneamente invalidar processamento já armazenado.

## T002:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: modificar uma ferramenta no prefixo e repetir a chamada. Verificar a invalidação indicada pelo provedor e impedir que o relatório conte um hit apenas porque o texto do usuário não mudou.

Plano de avaliação proposto:
Avaliação proposta: comparar séries com repetição, expiração e mudança de prefixo. Controlar entrada, saída e modelo; medir tokens reportados, latência de início e custo total, incluindo gravações sem reutilização.

Comparações:
- T007 (distinct_from): Cache de resposta evita uma geração; prompt caching reutiliza processamento de entrada e ainda gera a resposta.
- T043 (complements): Compactação e caching precisam ser avaliados juntos porque editar o prefixo muda a reutilização.

Afirmação rastreável:
A documentação de context editing registra que limpar resultados de ferramentas pode invalidar prefixos em cache.
Suporte: direct; fontes: V3A-S008
Limite: O comportamento preciso e os preços dependem do provedor e da configuração consultada.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T002:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou amortização. A nova camada trata escalonamento de cargas para tornar prefixos reutilizáveis sem congelar informação variável.

Projeto e decomposição
Classifique blocos em estáveis, derivados por versão e específicos da requisição. Ordene o prefixo pela probabilidade de reutilização, preservando precedência de instruções. Datas e identificadores voláteis pertencem ao sufixo quando o protocolo permitir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S002, V4A-S015.

Controle adaptativo
Planeje aquecimento apenas para grupos com reutilização prevista. Se o lote atrasar além da vida útil, cancelar aquecimento pode ser melhor que recriar continuamente. Registre hits reais, não oportunidades estimadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S002, V4A-S015.

Validação contrafactual
Compare chamadas na ordem de chegada e agrupadas por prefixo sob o mesmo prazo de resposta. Inclua espera de fila, escritas e leituras do cache. Unidade de avaliação: sessão de chamadas. No teste de carga, misture sessões de prefixo popular e prefixo raro com os mesmos prazos. Agrupar chamadas pode melhorar hits e piorar espera das sessões raras. A política só deve ser aceita quando a economia persistir incluindo atraso, aquecimento desperdiçado e renovação; não basta observar tokens cacheados em uma sequência artificialmente ordenada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S002, V4A-S015.

USO AVANÇADO — Revisão repetida de catálogo
Cenário: Várias perguntas compartilham documentação estável.
Estratégia: Fixar revisão do catálogo, distribuir perguntas pelo mesmo prefixo e renovar somente quando a revisão mudar.
Papel do modelo pequeno: 3–7B responde extrações simples sobre o prefixo.
Aceite proposto: Exigir mesma fidelidade que chamada sem cache e menor custo líquido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S002, V4A-S015.

USO AVANÇADO — Equipe com instrução comum
Cenário: Agentes recebem a mesma política.
Estratégia: Empacotar instrução comum antes das atribuições, mas não compartilhar material privado entre escopos. Separar grupos quando permissões diferirem.
Papel do modelo pequeno: 8–14B executa papéis com sufixos próprios.
Aceite proposto: Verificar igualdade de prefixos autorizados e ausência de contaminação entre grupos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S002, V4A-S015.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Usar instrução curta reutilizada em muitas chamadas de classificação.
8–14B: Reusar manuais maiores em extração e respostas contextualizadas.
15–30B: Amortizar leitura extensa em revisões profundas com perguntas independentes.
Requisitos de treino/runtime: Runtime com suporte real a prefix caching e telemetria de tokens cacheados; treino não é necessário.
Não aplicar quando: Cada chamada muda o prefixo inteiro ou espera de agrupamento viola o prazo.

## T002:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C016 — Google Cloud / Gemini context caching
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Manual disponibiliza caches implícitos e explícitos de contexto.
Mecanismo documentado: Reuso de prefixos, referências a objetos de cache e contabilidade de tokens.
Correspondência com esta base: Reaproveitamento documentado de contexto comum.
Transferência proposta para modelo pequeno: Proposta de engenharia: Agrupar chamadas pequenas com prefixo estável quando runtime suportar e medir custo líquido.
Limite: Modelos e condições de serviço variam; caching não aumenta janela nem reduz obrigação de evidência. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q011.

## T002:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T002 → T171 [complements]
Como combinar: Agrupar execução por afinidade de prefixo.
Interface: Hash do prefixo, modelo, revisão e prazo.
Condição: Servidor oferecer cache e isolamento adequados.
Aceite proposto: Medir hit real e atraso de fila conjuntamente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S002, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T002 → T042 [requires]
Como combinar: Contar também tokens cacheados na janela.
Interface: Contagem integral, reserva de saída e cache_id.
Condição: Cache não altera limite de contexto.
Aceite proposto: Rejeitar requisição que cabe no custo mas excede a janela.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S002, V4A-S015. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Invalidar reutilização após mudança de modelo ou serialização.
- Evitar tratar hit de cache como prova de resposta atualizada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo de leitura repetida com qualidade constante; caching não melhora por si só raciocínio do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T081, T082, T171

## Fontes primárias associadas

### A-S002 — Prompt caching

[https://platform.claude.com/docs/en/build-with-claude/prompt-caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reutilização computacional de prefixos de prompt; sem reutilização automática da resposta gerada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S015 — Context caching overview

[https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Caching implícito e explícito, metadados de uso e duração; recurso disponível.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
