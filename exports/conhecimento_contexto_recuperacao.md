# Contexto, compressão e recuperação

Exportação das fichas para ingestão documental. As fontes e os estados de evidência acompanham cada item.



---

# T001 — Map-Reduce

**Nome canônico:** Map-Reduce  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T001  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** MapReduce; mapear e reduzir

## T001:C01 — conceito

Decompõe uma coleção em partes processadas separadamente e agrega os resultados por uma chave ou contrato comum. Em agentes, é uma adaptação do padrão de processamento distribuído: cada trabalhador extrai evidências e o redutor consolida achados. Não é garantia de raciocínio global nem substitui análise das relações entre partes.

Como funciona:
- Definir partições com identificadores estáveis e escopo explícito.
- Executar mapas independentes e produzir saídas compatíveis.
- Agrupar resultados, verificar cobertura e reduzir preservando referências.

## T001:C02 — aplicacao

Quando usar:
- Auditoria de muitos arquivos com extração padronizada.
- Comparação de documentos que excedem uma única entrada do modelo.

Quando não usar:
- Quando cada parte depende fortemente de todas as outras e a decomposição omite essas dependências.

Implementação proposta:
- Proposta: criar manifesto com número de partes e hash da origem.
- Exigir dos mapas fatos, dúvidas e localização de evidências em JSON.
- Reduzir em lotes se a soma dos resultados exceder o orçamento e reconciliar conflitos antes da resposta.

Aplicação LAI proposta:
Proposta LAI: usar mapas para inventário de repositórios e um redutor para contratos entre softwares; dependências entre repositórios devem ser uma etapa própria.

## T001:C03 — riscos_validacao

Armadilhas:
- O redutor pode ignorar uma parte ausente.
- Resumos independentes podem perder uma condição situada em outro arquivo.

Métricas sugeridas:
- Cobertura: partes aceitas divididas pelas partes previstas.
- Latência e custo total, incluindo mapas repetidos e redução.

Testes propostos:
- Remover um resultado e exigir estado incompleto, sem conclusão universal.
- Plantar contradição entre duas partes e exigir referência a ambas.

## T001:C04 — perguntas_proveniencia

Pergunta: Map-Reduce exige vários modelos?
Resposta: Não. Um mesmo modelo pode processar partes sequencialmente; o paralelismo é uma decisão de execução.

Pergunta: Mais mapas sempre melhoram o resultado?
Resposta: Não. Partes pequenas demais aumentam custo e removem relações necessárias para interpretar a evidência.

Pergunta: Quando um combiner local é correto?
Resposta: Quando a operação admite a combinação parcial usada e preserva o resultado esperado. Essa propriedade deve ser demonstrada para o contrato, não presumida para texto gerado.

Pergunta: Como comparar dois redutores que escrevem diferente?
Resposta: Compare fatos, contagens, conflitos e evidências preservadas. Igualdade literal de prosa mede uma propriedade diferente de equivalência factual.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T001:C05 — mecanismo_avancado

A etapa de redução precisa distinguir identidade da partição e identidade da evidência. Repetir um map após falha não pode multiplicar um achado. Em uma adaptação com LLMs, a agregação textual pode depender da ordem e do agrupamento: propriedades algébricas de somas ou conjuntos não são herdadas por resumos. Partições desbalanceadas também deixam o tempo total dominado pelo trabalhador mais lento.

Condição de contorno:
O paralelismo perde valor quando a conclusão exige relações entre documentos que nenhum map observou, ou quando custo de coordenação supera processamento local.

Contrato proposto:
- Entradas: Partições versionadas, chaves de agrupamento e contrato de extração comum.
- Saídas: Resultados identificados e síntese com cobertura e lacunas declaradas.
- Estado: Tentativas por partição, evidências deduplicadas e versão do redutor.
- Invariante: Cada evidência original contribui uma vez para uma contagem, mesmo quando a execução é repetida.

Compromissos de projeto:
- Partições pequenas aumentam paralelismo, chamadas e fronteiras que podem separar fatos relacionados.
- Redução hierárquica limita contexto, mas adiciona oportunidades de perda e dependência da ordem.

## T001:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir deliberadamente uma partição e omitir outra. O redutor deve deduplicar a repetição, identificar a lacuna e não apresentar cobertura integral.

Plano de avaliação proposto:
Avaliação proposta: comparar processamento sequencial e paralelo com os mesmos documentos e extrator. Medir cobertura, consistência de contagens, custo e duração; variar distribuição de tamanho e ordem de redução antes de escolher a decomposição.

Comparações:
- T008 (complements): Uma hierarquia pode organizar a redução, mas ainda exige identidade das evidências e controle das perdas.

Afirmação rastreável:
No modelo MapReduce, valores intermediários são agrupados pela chave para processamento pelo redutor.
Suporte: direct; fontes: A-S001
Limite: A fonte descreve processamento distribuído; contratos para síntese por agentes são uma adaptação editorial.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T001:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou retries e redução não associativa. Aqui o foco novo é escolher partições pelo custo de inferência e separar agregação exata de síntese linguística.

Projeto e decomposição
Particione por unidades com custo estimado semelhante, não apenas quantidade de documentos. Um contrato extenso pode dominar o tempo de vários extratores 3–7B. Use amostra inicial para estimar tokens e reorganize apenas tarefas ainda não iniciadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S001, C-S030.

Controle adaptativo
Produza tabela intermediária de afirmações e evidências. Agregações numéricas ficam em código; o redutor recebe discrepâncias e cobertura. Permita segunda passagem somente sobre grupos inconclusivos, evitando reprocessar o corpus inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S001, C-S030.

Validação contrafactual
Compare partição por arquivo, por tokens e por domínio. A métrica decisiva é cobertura correta das unidades exigidas por tempo total, incluindo cauda dos trabalhadores. Unidade de avaliação: lote documental. Teste adicional: dividir uma entidade entre duas partições com nomes diferentes e exigir reconciliação pelo identificador canônico antes da soma. Compare tempo de cauda e cobertura quando uma partição contém documentos muito mais longos. Se redistribuir carga alterar a conclusão, investigar dependência do redutor à ordem, em vez de atribuir o problema ao paralelismo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S001, C-S030.

USO AVANÇADO — Inventário de interfaces
Cenário: Muitos módulos expõem contratos semelhantes.
Estratégia: Extrair endpoints por módulo, normalizar assinaturas em código e enviar apenas colisões ao redutor. Interromper publicação quando faltar módulo obrigatório.
Papel do modelo pequeno: 3–7B extrai; 15–30B interpreta colisões.
Aceite proposto: Exigir correspondência com manifesto de módulos e ausência de endpoints inventados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S001, C-S030.

USO AVANÇADO — Comparação de versões
Cenário: Documentação muda em várias áreas.
Estratégia: Mapear somente arquivos alterados, preservar resultados anteriores compatíveis e reduzir efeitos cruzados. Reabrir dependências afetadas por mudança de identidade.
Papel do modelo pequeno: 8–14B compara alterações locais.
Aceite proposto: Confirmar cada conclusão com trechos de ambas as versões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S001, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de esquema fixo com unidade curta e rejeição de campo desconhecido.
8–14B: Classificador de alterações que decide quais grupos precisam nova extração.
15–30B: Redutor de conflitos entre grupos, com acesso pontual às origens.
Requisitos de treino/runtime: Fila, manifesto de cobertura e estimativa de tokens por tarefa; treinamento opcional em extrações rotuladas.
Não aplicar quando: A conclusão depende de ler simultaneamente quase todas as unidades ou a divisão destrói relações essenciais.

## T001:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C001 — Google / MapReduce nos clusters Google
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura geral; transferência para LLM é proposta.
Uso observado: Artigo dos operadores descreve execução recorrente de jobs nos clusters Google.
Mecanismo documentado: Map por pares, agrupamento por chave e reduce distribuído.
Correspondência com esta base: Mesmo modelo de programação map/shuffle/reduce; a adaptação com LLM continua proposta.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar extratores pequenos independentes e reduzir registros estruturados; verificar cobertura antes da síntese.
Limite: Relato de 2004; não é implantação de redução linguística nem comprovação de escala atual. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S001.

V4A-C002 — Anthropic / Research multi-agent system
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A equipe descreve passagem do protótipo à produção do recurso Research.
Mecanismo documentado: Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.
Correspondência com esta base: Distribuição e agregação de pesquisa, sem garantia de semântica MapReduce.
Transferência proposta para modelo pequeno: Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.
Limite: Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q001, V4A-Q002.

## T001:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T001 → T065 [requires]
Como combinar: Confirmar resultados intermediários antes de reduzir.
Interface: job_id, partição, revisão e status de commit.
Condição: Existir armazenamento com confirmação verificável.
Aceite proposto: Injetar trabalhador atrasado e conferir que resultado parcial não fecha lote.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S001, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T001 → T028 [complements]
Como combinar: Ordenar discrepâncias para revisão do redutor.
Interface: Par de afirmações, fontes e prioridade.
Condição: Ranking não elimina discrepâncias obrigatórias.
Aceite proposto: Comparar fila completa e fila priorizada por conflitos resolvidos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S001, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Impor limite de tentativas por partição e preservar motivo da falha.
- Deduplicar afirmações pela origem, sem apagar relatos divergentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar extração completa e síntese de divergências; o ganho buscado é paralelismo controlado, não criatividade geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T147, T169

## Fontes primárias associadas

### A-S001 — MapReduce: Simplified Data Processing on Large Clusters

[https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo map/reduce, agrupamento por chave e execução distribuída tolerante a falhas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# T003 — Sliding Window de contexto — incluindo descarte FIFO

**Nome canônico:** Janela deslizante do histórico com descarte FIFO  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T003  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Sliding Window de contexto; janela deslizante de histórico; descarte FIFO de contexto; histórico recente por tokens

## T003:C01 — conceito

Sliding Window de contexto mantém uma porção recente do histórico na entrada ativa do modelo. O descarte FIFO remove primeiro as unidades mais antigas elegíveis. Essa política opera antes da inferência; sliding-window attention limita conexões dentro do modelo e não é equivalente. Arquivar mensagens retiradas permite recuperá-las posteriormente sem consumir a janela em todas as chamadas.

Como funciona:
- Calcular orçamento disponível após reservar instruções fixas, resposta e resultados de ferramentas esperados.
- Ordenar unidades descartáveis por chegada e retirar as mais antigas até caber; uma unidade pode ser um turno completo ou um par chamada/resultado.
- Preservar fora da fila removível objetivos vigentes, decisões atuais e operações pendentes, com referências ao histórico original.

## T003:C02 — aplicacao

Quando usar:
- Conversas longas em que a maior parte do contexto relevante é recente e o histórico completo permanece recuperável.

Quando não usar:
- Como única memória para contratos, requisitos antigos ainda válidos ou fatos cuja importância não acompanha a idade.

Implementação proposta:
- Proposta: separar estado persistente da missão, histórico integral e janela enviada; contar tokens com o tokenizer do modelo escolhido.
- Definir FIFO por sequência de registro, sem presumir que a data mencionada no conteúdo corresponde à ordem de chegada.
- Se a mensagem mais recente sozinha exceder o orçamento, extrair trechos ou resumir com proveniência; não quebrar arbitrariamente o protocolo de ferramentas.

Aplicação LAI proposta:
Proposta LAI: manter objetivo e decisões em estado durável, usar FIFO apenas na área de histórico recente e registrar o intervalo arquivado em cada avanço da janela.

## T003:C03 — riscos_validacao

Armadilhas:
- FIFO não avalia relevância: uma restrição crítica antiga pode desaparecer.
- Cortar somente uma metade de uma interação com ferramenta produz histórico inválido ou interpretação incompleta.

Métricas sugeridas:
- Tokens ativos, quantidade de unidades removidas e proporção de perguntas históricas respondidas com evidência correta.

Testes propostos:
- Teste proposto: ultrapassar o limite com dez turnos e verificar ordem FIFO, preservação de pares e orçamento final.
- Introduzir uma obrigação antiga ainda vigente e exigir sua recuperação antes de uma ação incompatível.

## T003:C04 — perguntas_proveniencia

Pergunta: FIFO apaga automaticamente a memória persistente?
Resposta: Não. Nesta proposta ele remove a cópia do contexto ativo; retenção ou exclusão do arquivo histórico pertence a outra política.

Pergunta: Posso descartar uma tool call antiga mantendo seu resultado recente?
Resposta: Somente se o protocolo permitir uma representação independente. O padrão recomendado mantém chamada e resultado como unidade indivisível.

Pergunta: Arquivar torna o descarte sem perdas?
Resposta: Preserva o original no armazenamento, mas ainda pode falhar a recuperação no momento necessário. Perda operacional e perda física são propriedades diferentes.

Pergunta: E quando todos os blocos restantes forem obrigatórios?
Resposta: O montador deve declarar orçamento insuficiente e mudar a estratégia: reduzir tarefa, buscar outra representação válida ou usar capacidade compatível.

Escopo das fontes:
A-S003 fundamenta gestão e redução do histórico; A-S006 fundamenta engenharia do contexto. Proteções de estado, definição de FIFO e testes são escolhas editoriais propostas.

## T003:C05 — mecanismo_avancado

A unidade segura de descarte pode ser maior que uma mensagem: uma chamada e seu resultado formam uma dependência de protocolo. A janela também precisa preservar estados não resolvidos, como uma pergunta ainda sem resposta. Uma implementação robusta calcula um fechamento de dependências antes de cortar o histórico; recência define preferência, não validade semântica.

Condição de contorno:
A hipótese de que o passado é dispensável falha quando uma restrição antiga permanece vigente ou uma ação atual depende de identificadores removidos.

Contrato proposto:
- Entradas: Histórico ordenado, orçamento e grupos de mensagens dependentes.
- Saídas: Contexto válido com fronteira de descarte e referências ao arquivo completo.
- Estado: Cursor de arquivamento e conjunto de fatos protegidos ainda necessários.
- Invariante: Nenhum resultado de ferramenta fica associado a uma chamada inexistente no protocolo enviado.

Compromissos de projeto:
- FIFO é previsível e barato, mas ignora valor de informações antigas.
- Proteger dependências melhora continuidade, porém pode impedir que a janela caiba sem outra forma de redução.

## T003:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma chamada no limite da janela e seu resultado depois do corte. A montagem deve manter o par necessário ou externalizá-lo por um mecanismo compatível, sem histórico inválido.

Plano de avaliação proposto:
Avaliação proposta: comparar FIFO por mensagens e descarte por grupos completos. Variar tamanho das saídas e distância de restrições relevantes; medir erros de protocolo, recuperação posterior e sucesso das etapas dependentes.

Comparações:
- T041 (complements): Last-N escolhe tamanho por quantidade de mensagens; a janela genérica pode usar outras unidades.
- T039 (alternative): Seleção por importância pode preservar um fato antigo que FIFO retiraria.

Afirmação rastreável:
Context editing documenta remoção de resultados antigos com placeholders e opções de preservação.
Suporte: direct; fontes: V3A-S008
Limite: Isso apoia uma implementação específica de descarte; não demonstra que todo histórico admite FIFO sem perda.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T003:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou pares de ferramentas. Aqui a janela móvel ganha transições planejadas por fase e testes de retenção de obrigações.

Projeto e decomposição
Defina fronteiras de fase em vez de descartar continuamente. Ao terminar coleta, transforme resultados confirmados em tabela e remova apenas conversas de busca. A janela da fase seguinte começa com objetivos e pendências explícitos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Controle adaptativo
Use duas filas: observações recentes e obrigações ainda abertas. FIFO governa a primeira; uma obrigação só sai por resolução identificada. Isso evita que repetição de logs empurre uma condição antiga necessária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Validação contrafactual
Variar tamanho dos logs sem mudar decisões permite medir sensibilidade da política ao volume incidental. Avalie obrigações recuperadas corretamente após mudanças de fase. Unidade de avaliação: trajetória de tarefa. Inclua uma mudança de fase com resultado tardio pertencente à fase anterior. O controlador deve registrar a observação, avaliar se ela invalida decisão atual e evitar reinseri-la como instrução recente. Medir separadamente quantidade de eventos preservados e quantidade de obrigações corretamente aplicadas impede confundir arquivo completo com contexto útil.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Triagem contínua
Cenário: Chamados chegam durante um incidente.
Estratégia: Agrupar observações por intervalo, persistir ações confirmadas e carregar pendências antigas antes de decidir próximo passo.
Papel do modelo pequeno: 3–7B classifica observações curtas.
Aceite proposto: Não perder restrição ativa quando o volume aumenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Extração em etapas
Cenário: Um arquivo exige várias leituras.
Estratégia: Manter cursor e campos faltantes fora da fila; trocar trechos a cada bloco sem reintroduzir páginas concluídas.
Papel do modelo pequeno: 8–14B reconcilia campos extraídos.
Aceite proposto: Cobrir todos os campos obrigatórios ou marcar ausência com referência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Janela curta por fase com obrigações enumeradas em campos.
8–14B: Janela com duas fontes simultâneas para comparar correções locais.
15–30B: Integração de fases complexas usando referências, sem carregar histórico integral.
Requisitos de treino/runtime: Estado explícito de obrigações e cursor; limites calculados no tokenizer do leitor.
Não aplicar quando: A tarefa requer dependências globais que não podem ser representadas num estado compacto.

## T003:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T003:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T003 → T040 [complements]
Como combinar: Separar conteúdo recente de estado vigente.
Interface: Fila de observações e lista versionada de obrigações.
Condição: Existir evento explícito de conclusão.
Aceite proposto: Introduzir logs irrelevantes e verificar estabilidade da decisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T003 → T070 [feeds]
Como combinar: Arquivar unidades removidas para reconsulta.
Interface: Episódio, intervalo, cursor e motivo do descarte.
Condição: Armazenamento acessível após rotação.
Aceite proposto: Solicitar episódio antigo e conferir localização exata.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar silêncio recente como cancelamento.
- Aplicar descarte somente a grupos de protocolo completos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade em tarefas com ruído volumoso; manter mesma informação obrigatória no baseline.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T050, T063, T069, P002

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T004 — Summarization em cadeia

**Nome canônico:** Summarization em Cadeia  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T004  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** rolling summary; resumo acumulado; Summarization em Cadeia

## T004:C01 — conceito

Mantém um resumo acumulado atualizado por novos blocos de conteúdo. Cada passo usa o resumo anterior e o próximo trecho para produzir a nova versão. É econômico em contexto, mas uma perda ou distorção inicial pode propagar-se nas versões seguintes.

Como funciona:
- Ordenar os blocos e manter os originais acessíveis.
- Atualizar resumo com decisões, fatos e pendências do próximo bloco.
- Associar cada afirmação importante à evidência que a originou.

## T004:C02 — aplicacao

Quando usar:
- Históricos cronológicos de atendimento ou execução.
- Fluxos que recebem novos eventos continuamente.

Quando não usar:
- Evitar como único registro quando são necessárias citações literais ou reconstrução completa.

Implementação proposta:
- Proposta: usar campos estáveis para fatos, decisões, dúvidas e referências.
- Versionar cada resumo e guardar quais blocos foram incorporados.
- Em intervalos definidos, reconstruir a síntese dos originais para medir deriva acumulada.

Aplicação LAI proposta:
Proposta LAI: produzir notas compactas de missão para Helena mantendo decisões e fontes separadas; a síntese serve à navegação, não à autoridade factual.

## T004:C03 — riscos_validacao

Armadilhas:
- Uma hipótese pode virar fato ao ser reescrita repetidamente.
- Eventos recentes podem dominar a síntese e apagar obrigações persistentes.

Métricas sugeridas:
- Retenção de fatos críticos em cada atualização.
- Número de afirmações do resumo sem evidência recuperável.

Testes propostos:
- Injetar uma correção tardia e exigir preservação do histórico da mudança.
- Comparar a décima versão com uma síntese independente dos mesmos originais.

## T004:C04 — perguntas_proveniencia

Pergunta: O resumo anterior é suficiente para auditar?
Resposta: Não. Uma cadeia de resumos pode perder informação; os eventos e documentos originais precisam permanecer disponíveis.

Pergunta: Como evitar que uma correção desapareça?
Resposta: Registrar validade, versão e relação de substituição em campos próprios, além do texto resumido.

Pergunta: Como detectar deriva sem reler tudo?
Resposta: Amostre fatos críticos, verifique referências e compare campos protegidos com sua fonte. Essa auditoria reduz risco, mas não prova ausência de perdas não amostradas.

Pergunta: Um resumo antigo pode ser a única fonte?
Resposta: Pode ser a única representação disponível, mas deve ser marcado como evidência derivada. Sem o original, não é possível confirmar detalhes que ele omitiu.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T004:C05 — mecanismo_avancado

A atualização recorrente s_t=f(s_(t-1),bloco_t) cria dependência de caminho: um fato ausente de s_(t-1) não reaparece sem consulta ao original. Por isso, uma cadeia deve separar resumo narrativo de campos verificáveis, como identificadores e decisões vigentes. Aumentar a fluência da síntese pode esconder degradação factual acumulada em ciclos longos.

Condição de contorno:
Quando a tarefa exige detalhes arbitrários do passado, um resumo de tamanho fixo não oferece garantia de recuperação completa, independentemente da qualidade aparente da prosa.

Contrato proposto:
- Entradas: Resumo anterior versionado, novo bloco e política de preservação.
- Saídas: Nova síntese e referências às evidências incorporadas ou substituídas.
- Estado: Originais recuperáveis, versão do sumarizador e decisões protegidas.
- Invariante: Correções explícitas permanecem distinguíveis das afirmações anteriores que corrigem.

Compromissos de projeto:
- Atualização incremental reduz leitura repetida, mas transmite erros entre ciclos.
- Campos estruturados preservam precisão, porém exigem esquema e manutenção além do texto livre.

## T004:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir um valor, corrigi-lo após vários blocos e continuar resumindo. A memória final deve indicar o valor vigente e permitir verificar a correção sem reconstruí-la por adivinhação.

Plano de avaliação proposto:
Avaliação proposta: comparar resumo recorrente com resumo regenerado dos originais sob orçamento equivalente. Variar número de ciclos e frequência de correções; medir omissões, inversões de negação, atribuição e custo acumulado.

Comparações:
- T008 (alternative): A hierarquia preserva caminhos locais para revisar perdas sem reprocessar toda a cadeia.
- T069 (complements): O resultado textual pode alimentar consolidação persistente sem alterar parâmetros do modelo.

Afirmação rastreável:
O método de memória recursiva combina memória anterior com diálogos subsequentes para produzir a próxima memória.
Suporte: direct; fontes: V3A-S005
Limite: Ganhos experimentais de consistência não equivalem a conservação integral do histórico.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T004:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou deriva acumulada. Aqui resumos são especializados por consumidor e acompanhados de um registro de mudanças de entendimento.

Projeto e decomposição
Produza resumo operacional e resumo explicativo distintos. O primeiro contém próximos passos e restrições; o segundo conserva justificativas. Um consumidor pequeno recebe apenas o primeiro e abre justificativas quando identifica conflito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

Controle adaptativo
Cada atualização declara fatos adicionados, corrigidos e ainda incertos. A cadeia pode assim detectar transformação de hipótese em certeza, mesmo quando o texto final continua fluente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

Validação contrafactual
Compare consumidores recebendo resumo único e duas visões especializadas. Meça decisões corretas e frequência de abertura do original, incluindo custo dessas leituras. Unidade de avaliação: histórico com revisões. Uma prova útil fornece resumo operacional com decisão vigente e resumo explicativo ainda defendendo a decisão anterior. O consumidor deve detectar a revisão incompatível antes de agir. Conte casos de retomada correta, justificativa incoerente e abertura necessária do original; isso avalia a interface entre vistas, não apenas a qualidade individual de cada resumo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

USO AVANÇADO — Passagem entre turnos de operação
Cenário: Equipes retomam trabalho incompleto.
Estratégia: Gerar quadro de pendências e histórico de decisões separadamente; exigir evidência da conclusão antes de retirar pendência.
Papel do modelo pequeno: 3–7B atualiza campos; 8–14B explica desvios.
Aceite proposto: Preservar responsável, prazo e condição de cada pendência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

USO AVANÇADO — Pesquisa com hipóteses concorrentes
Cenário: Novas fontes alteram conclusões.
Estratégia: Manter resumo por hipótese e um quadro de diferenças; somente consolidar após comparar evidências conflitantes.
Papel do modelo pequeno: 15–30B integra argumentos com citações.
Aceite proposto: Não converter falta de evidência em refutação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S005, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Atualização de campos fechados a partir de observação curta.
8–14B: Produção de resumo operacional com rastreio de alterações.
15–30B: Síntese de justificativas concorrentes, com verificação por fonte.
Requisitos de treino/runtime: Esquema de diferenças e fontes estáveis; exemplos de correções ajudam ajuste supervisionado.
Não aplicar quando: Exatidão literal integral é obrigatória ou a sequência não possui evidências recuperáveis.

## T004:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.
Mecanismo documentado: Aplicação específica de um modelo local para condensar transcrições.
Correspondência com esta base: Há sumarização; não está documentada uma cadeia de resumos.
Transferência proposta para modelo pequeno: Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.
Limite: Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.
Fontes: V4D-S005.

V4D-C004 — Google / Chrome built-in AI / Summarizer API
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação lista a Summarizer API no Chrome estável desde a versão 138.
Mecanismo documentado: Interface local de geração com modelo gerenciado pelo navegador e requisitos de disponibilidade.
Correspondência com esta base: Não documenta cadeia de sumarização por trás da API.
Transferência proposta para modelo pequeno: Proposta: detectar disponibilidade local e limitar a tarefa a texto fornecido; manter o contrato de saída igual quando um backend alternativo for necessário.
Limite: Disponibilidade não constitui prova de implantação em cliente, volume de tráfego ou porte exato do modelo. As etapas de preview e estável precisam ser verificadas por API.
Fontes: V4D-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q022.

## T004:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T004 → T072 [requires]
Como combinar: Versionar cada visão e sua base comum.
Interface: revision_id, covered_until e lista de alterações.
Condição: Visões derivadas da mesma revisão.
Aceite proposto: Detectar mistura de resumo operacional novo e explicativo antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T004 → T015 [complements]
Como combinar: Ligar justificativas a originais sob demanda.
Interface: Afirmação, referência e intervalo de origem.
Condição: Referência resolver conteúdo específico.
Aceite proposto: Conferir leitura original quando uma hipótese muda.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S005, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar queda de certeza explicitamente.
- Não fundir opiniões de fontes distintas como consenso.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar decisões após sucessivas correções, sem usar concisão ou fluência como medida principal.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T043, T059, T072

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S005 — Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

[https://arxiv.org/abs/2308.15022](https://arxiv.org/abs/2308.15022)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização recursiva de memória a partir do resumo anterior e novos diálogos, sem equivaler a mudança dos pesos.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4D-S005 — Pixel December 2023 feature drop

[https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Lançamento de Gemini Nano em Pixel 8 Pro e resumo offline no Recorder.

Limite: Não identifica o checkpoint nem sua contagem de parâmetros. Smart Reply no Gboard era developer preview; não confundir resumo com cadeia hierárquica ou destilação.

### V4D-S007 — Built-in AI APIs

[https://developer.chrome.com/docs/ai/built-in-apis](https://developer.chrome.com/docs/ai/built-in-apis)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade e estágio das APIs locais do Chrome; Summarizer documentado como estável desde Chrome 138.

Limite: Tabela é mutável e partes textuais podem acompanhar versões em ritmos diferentes. API disponível não comprova uso por cliente; não identifica porte exato do checkpoint.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T005 — Semantic Caching

**Nome canônico:** Semantic Caching  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T005  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** cache semântico

## T005:C01 — conceito

Armazena perguntas ou representações de contexto e respostas anteriores para reutilizar uma resposta quando uma nova consulta for semanticamente equivalente dentro de um escopo permitido. Similaridade vetorial é um sinal de proximidade, não uma prova de que a resposta continua correta.

Como funciona:
- Aplicar filtros de identidade, versão e escopo antes da busca.
- Comparar embedding da pergunta com entradas válidas do cache.
- Aceitar somente candidatos que satisfaçam limiar e condições de reutilização.

## T005:C02 — aplicacao

Quando usar:
- Perguntas frequentes sobre conteúdo estável.
- Variações de redação que realmente pedem o mesmo fato.

Quando não usar:
- Não reutilizar indiscriminadamente resultados de saldos, permissões, horários ou estados mutáveis.

Implementação proposta:
- Proposta: incluir versão documental e do modelo na chave lógica.
- Calibrar limiar com pares equivalentes e pares parecidos com respostas diferentes.
- Invalidar entradas por mudança da fonte e registrar por que cada acerto foi aceito.

Aplicação LAI proposta:
Proposta LAI: começar por FAQs técnicas estáveis e segmentadas; só expandir após medir falsos acertos no vocabulário real da empresa.

## T005:C03 — riscos_validacao

Armadilhas:
- Perguntas sobre clientes distintos podem ser quase idênticas.
- Negação, data ou unidade numérica podem inverter a resposta apesar da alta similaridade.

Métricas sugeridas:
- Precisão dos acertos do cache, não apenas taxa de acertos.
- Tempo e custo poupados após custo de busca e manutenção.

Testes propostos:
- Testar pares que diferem só por não, data, tenant ou valor.
- Alterar a política fonte e verificar que respostas antigas não são retornadas.

## T005:C04 — perguntas_proveniencia

Pergunta: Um embedding muito parecido garante mesma resposta?
Resposta: Não. Os detalhes decisivos podem ter pouco peso no vetor; use filtros e avaliação de equivalência.

Pergunta: Cache semântico substitui RAG?
Resposta: Não. Ele reaproveita respostas; RAG recupera evidência para construir uma resposta nova.

Pergunta: Posso copiar um limiar entre modelos de embedding?
Resposta: Não com confiança. Distribuições e métricas mudam; recalibre usando pares relevantes ao domínio e declare a unidade da distância.

Pergunta: Um hit frequente deve renovar a validade?
Resposta: A frequência pode justificar permanência em memória, mas não atualidade factual. Renovar TTL sem validar dependências pode perpetuar uma resposta obsoleta.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T005:C05 — mecanismo_avancado

O erro mais caro costuma ser aceitar uma pergunta próxima cuja resposta difere em um pequeno detalhe: negação, unidade, data ou identidade. A decisão precisa combinar similaridade com condições exatas de elegibilidade. Embeddings de versões diferentes também não devem compartilhar a mesma comparação apenas por terem dimensões iguais; o espaço vetorial faz parte do contrato.

Condição de contorno:
O cache deixa de ser confiável quando a resposta depende de estado pessoal ou temporal ausente da chave e dos filtros, mesmo que a distância seja muito pequena.

Contrato proposto:
- Entradas: Consulta, escopo autorizado, versão das fontes e identificador do embedding.
- Saídas: Hit elegível com origem e validade, ou miss que segue para geração.
- Estado: Índice vetorial segregado por versões compatíveis e metadados de dependência.
- Invariante: Proximidade vetorial nunca sobrepõe uma incompatibilidade de escopo ou versão.

Compromissos de projeto:
- Limiar permissivo eleva reutilização e também falsos acertos.
- Filtros mais estritos reduzem cobertura, mas evitam compartilhar respostas entre contextos diferentes.

## T005:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar duas consultas quase iguais que mudem apenas o sujeito ou a validade temporal. A resposta armazenada deve ser recusada quando esses campos alterarem a resposta correta.

Plano de avaliação proposto:
Avaliação proposta: comparar cache exato, cache semântico e execução sem cache. Usar pares equivalentes e quase equivalentes criados para o domínio; medir precisão dos hits, cobertura e custo. Escolher limiar pela tolerância real ao falso acerto.

Comparações:
- T031 (complements): Respostas reutilizáveis precisam de uma regra explícita de validade e invalidação.
- T007 (alternative): Identidade exata evita a decisão de equivalência semântica, mas perde paráfrases.

Afirmação rastreável:
RedisVL SemanticCache expõe distância, filtros, vetorizador e TTL como controles distintos.
Suporte: direct; fontes: V3A-S007
Limite: Esses controles não demonstram automaticamente equivalência semântica ou correção da resposta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T005:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou falsos hits e filtros. A camada nova é admissão seletiva de respostas e cache de artefatos parciais verificáveis.

Projeto e decomposição
Diferencie cache da resposta completa e cache de evidências recuperadas. Perguntas similares podem compartilhar documentos sem compartilhar conclusão. Priorize reuso de candidatos quando pequenas mudanças alterarem o resultado final.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

Controle adaptativo
Admitir uma resposta exige fonte vigente e estabilidade do domínio. Registre quais atributos tornam a equivalência inválida, como versão, unidade e finalidade. Um classificador pode sugerir hit; regras fechadas confirmam elegibilidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

Validação contrafactual
Construa pares mínimos que mudam somente um atributo decisivo. Compare taxa de aceitação errada e custo evitado, não apenas similaridade média. Unidade de avaliação: família de consultas. Separe validação de admissão e validação de reutilização. Uma resposta pode ter sido correta quando entrou no cache e inadequada para a consulta atual. Teste pares com mesma intenção geral, mas população, unidade ou versão diferente, e registre em qual filtro o hit foi recusado. Isso permite reduzir custo sem esconder falsos acertos no agregado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

USO AVANÇADO — Suporte com perguntas recorrentes
Cenário: Usuários reformulam dúvida sobre uma versão.
Estratégia: Buscar candidato, validar versão e pré-condições, reutilizar resposta apenas se o contrato continuar equivalente.
Papel do modelo pequeno: 3–7B extrai atributos para filtros.
Aceite proposto: Nenhum hit em versão incompatível no conjunto de validação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

USO AVANÇADO — Pesquisa repetida com novo critério
Cenário: Consultas variam o julgamento solicitado.
Estratégia: Reusar trechos elegíveis e gerar nova conclusão; não devolver resposta anterior quando muda o critério de comparação.
Papel do modelo pequeno: 8–14B reinterpreta evidências existentes.
Aceite proposto: Citação atual e conclusão sensível à mudança do critério.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S016, V3A-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de atributos que alimenta chave de elegibilidade.
8–14B: Verificador de equivalência contextual em candidatos curtos.
15–30B: Leitor de evidências cacheadas para síntese de critérios múltiplos.
Requisitos de treino/runtime: Índice vetorial, metadados de dependência e caminho de bypass; calibrar limiar por domínio.
Não aplicar quando: Respostas variam por identidade, tempo ou estado que o cache não consegue verificar.

## T005:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C017 — Microsoft / API Management semantic response cache
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Política disponível busca respostas em cache externo por proximidade.
Mecanismo documentado: Embedding, limiar e particionamento de cache por expressões.
Correspondência com esta base: Retorno de resposta por similaridade semântica explicitado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Aceitar somente domínio estável e validar pares quase iguais com entidades ou negações diferentes.
Limite: Não comprova implantação nem taxa de falsos acertos; limiares do serviço não são probabilidades. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q012.

## T005:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T005 → T031 [requires]
Como combinar: Revogar itens derivados quando a base muda.
Interface: dependency_ids, revisão e lista de respostas afetadas.
Condição: Dependências registradas no momento de admissão.
Aceite proposto: Alterar fonte e medir sobrevivência indevida de hits.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S016, V3A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T005 → T205 [complements]
Como combinar: Testar equivalência antes de reutilizar resposta.
Interface: Par de pedidos e atributos relevantes.
Condição: Verificação mais barata que refazer e validada no domínio.
Aceite proposto: Incluir negações e quantificadores quase iguais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S016, V3A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar resposta cuja origem não pode ser reaberta.
- Separar falha do cache de ausência de candidato.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo por resposta correta com reexecução completa; mais hits podem piorar o sistema.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T007, T031, T205

## Fontes primárias associadas

### A-S005 — LLM Caching

[https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/](https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico com embeddings, limiar de distância, TTL e filtros de acesso.

Limite: Documentação consultada da versão 0.10.0, não afirma ser a versão corrente do pacote.

### V3A-S007 — RedisVL LLM Cache API

[https://redis.io/docs/latest/develop/ai/redisvl/api/cache/](https://redis.io/docs/latest/develop/ai/redisvl/api/cache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: SemanticCache com filtros, distância, vetorizador e TTL; diferenças de capacidades entre implementações.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S016 — Get cached responses of large language model API requests

[https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy](https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico por proximidade vetorial, limiar e particionamento vary-by.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T006 — Context Compression

**Nome canônico:** Context Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão de contexto

## T006:C01 — conceito

Família de métodos que reduz a representação entregue ao modelo: selecionar trechos, remover redundância, resumir ou usar representações aprendidas. É necessário declarar o tipo de compressão: texto legível, seleção extrativa e estados latentes têm requisitos e perdas diferentes.

Como funciona:
- Identificar informação obrigatória e redundância permitida.
- Escolher transformação compatível com a tarefa e o modelo.
- Preservar ligações para a informação original e avaliar o resultado.

## T006:C02 — aplicacao

Quando usar:
- Excesso de documentos ou histórico dentro do orçamento de entrada.
- Repetição extensa de instruções e resultados de ferramentas.

Quando não usar:
- Não comprimir cegamente código, números, negações ou evidências que exigem reprodução exata.

Implementação proposta:
- Proposta: definir orçamento por seção e lista de campos protegidos.
- Comparar uma linha de base sem compressão com versões em diferentes razões.
- Medir tempo do compressor junto da inferência e restaurar originais quando faltar evidência.

Aplicação LAI proposta:
Proposta LAI: aplicar primeiro seleção e deduplicação auditáveis; experimentar métodos aprendidos apenas quando a economia compensar a infraestrutura adicional.

## T006:C03 — riscos_validacao

Armadilhas:
- Texto menor pode exigir mais chamadas de recuperação.
- A compressão pode produzir uma síntese plausível que remove justamente a exceção relevante.

Métricas sugeridas:
- Razão entre tokens originais e enviados.
- Qualidade final, fidelidade factual e latência total.

Testes propostos:
- Inserir condições de exceção em posições variadas e conferir sua retenção.
- Usar perguntas com números próximos e rejeitar compressões que alterem valores.

## T006:C04 — perguntas_proveniencia

Pergunta: Comprimir contexto equivale a treinar o modelo?
Resposta: Não. Muitos métodos alteram apenas a entrada; alguns métodos latentes ou paramétricos exigem treinamento.

Pergunta: Menos tokens significa menor custo total?
Resposta: Só se a economia superar o custo da compressão, de buscas extras e de eventuais reexecuções.

Pergunta: Texto extraído garante fidelidade?
Resposta: Garante que os trechos selecionados vieram da entrada quando o processo é realmente extrativo. Não garante que o conjunto preservou o sentido e as condições do original.

Pergunta: Como interpretar uma compressão vazia?
Resposta: Como decisão de não acrescentar evidência, não como prova de que não existe resposta. O gerador precisa respeitar as regras de evidência da tarefa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T006:C05 — mecanismo_avancado

A função objetivo deve incluir custo do compressor, custo de leitura do resultado e perda na tarefa final. Uma representação curta que exige releituras frequentes pode custar mais que o original. Também importa definir suficiência: compressão para extração numérica exige preservar valores e condições, enquanto síntese temática pode tolerar detalhes ausentes. Não existe uma taxa que expresse todas essas perdas.

Condição de contorno:
O ganho desaparece quando compressão e reconstrução superam o trabalho economizado, ou quando o consumidor não entende a representação produzida.

Contrato proposto:
- Entradas: Conteúdo original, classe de tarefa, orçamento e consumidor identificado.
- Saídas: Representação reduzida com tipo declarado e vínculo à fonte.
- Estado: Versões do compressor, política de preservação e artefatos originais.
- Invariante: Uma saída latente não é tratada como texto intercambiável entre modelos incompatíveis.

Compromissos de projeto:
- Extração conserva palavras selecionadas, mas ainda pode remover relações e negações.
- Abstração integra informações dispersas, porém acrescenta risco de afirmações geradas sem suporte.

## T006:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: comprimir um conjunto com exceção rara indispensável à decisão. O consumidor deve preservá-la ou reconhecer insuficiência; uma resposta confiante baseada apenas na regra geral constitui falha.

Plano de avaliação proposto:
Avaliação proposta: comparar entrada integral, seleção simples e compressor candidato com o mesmo modelo final. Medir custo total, suporte factual, respostas incorretas e releituras; escolher pela fronteira de custo e qualidade da tarefa.

Comparações:
- T020 (complements): Compressão aprendida é uma família particular que exige treinamento ou modelo especializado.
- T037 (complements): Condicionar à pergunta muda quais perdas são aceitáveis para a resposta atual.

Afirmação rastreável:
RECOMP oferece compressores extrativo e abstrativo e permite saída vazia quando a recuperação não acrescenta informação.
Suporte: direct; fontes: V3A-S003
Limite: O mecanismo publicado não estabelece que qualquer resumo curto melhora qualquer consumidor.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T006:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou custos de compressão. Aqui a estratégia escolhe representações diferentes por tipo de informação e consumidor.

Projeto e decomposição
Transforme tabelas em registros tipados e narrativa em trechos extraídos. Números, relações e ressalvas exigem representações diferentes; aplicar a mesma taxa a tudo desperdiça capacidade do leitor pequeno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

Controle adaptativo
Reserve passagem sem compressão para campos de alta sensibilidade e compacte redundâncias de apresentação. O compressor deve emitir mapa de cobertura por requisito, permitindo ampliar somente a parte insuficiente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

Validação contrafactual
Compare compressão uniforme, por tipo e ausência de compressão. Meça respostas sensíveis a unidade, exceção e atribuição de fonte, além de tokens. Unidade de avaliação: documento com consulta. Na validação, uma tabela deve conter o mesmo número em colunas com unidades diferentes e uma nota que altera apenas uma linha. A representação comprimida precisa conservar essas relações. Compare resposta com objeto estruturado, texto linearizado e resumo abstrativo; esse contraste localiza se o erro foi criado pelo parser, pelo compressor ou pela leitura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

USO AVANÇADO — Manual com especificações
Cenário: Texto mistura requisitos e explicações.
Estratégia: Extrair requisitos literalmente, resumir justificativas e manter tabelas estruturadas; reabrir se um requisito não puder ser ligado à seção.
Papel do modelo pequeno: 3–7B lê campos; 8–14B integra exceções.
Aceite proposto: Não perder valor, unidade ou condição obrigatória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

USO AVANÇADO — Dossiê repetitivo
Cenário: Vários documentos repetem o mesmo fato.
Estratégia: Agrupar duplicações por origem, preservar divergências e enviar exemplos representativos acompanhados da contagem de fontes independentes.
Papel do modelo pequeno: 15–30B sintetiza controvérsias.
Aceite proposto: Conservar posição minoritária documentada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S027, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de representação estruturada curta, sem reconstruir texto telegráfico complexo.
8–14B: Leitor misto de registros e trechos, apto a pedir expansão específica.
15–30B: Integrador de múltiplas representações com verificador de consistência.
Requisitos de treino/runtime: Parser de tipos, mapa de cobertura e tokenizer do consumidor; treinamento opcional para leitura comprimida.
Não aplicar quando: O compressor altera relação entre condições ou custa mais que a leitura integral.

## T006:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C003 — Google / Pixel 8 Pro Recorder / Gemini Nano
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O lançamento de dezembro de 2023 disponibilizou resumo no Recorder processado no aparelho.
Mecanismo documentado: Aplicação específica de um modelo local para condensar transcrições.
Correspondência com esta base: Resumo é redução de conteúdo, mas não comprova algoritmo específico de compressão contextual.
Transferência proposta para modelo pequeno: Proposta: reproduzir a fronteira da tarefa com transcrições delimitadas e verificar entidades, negações e compromissos contra o original antes de promover o resumo a memória.
Limite: Fonte não identifica checkpoint/contagem de parâmetros; não o certificar como 3–30B. Não prova mecanismo de memória durável, chunking hierárquico ou raciocínio geral.
Fontes: V4D-S005.

V4D-C002 — Microsoft / Windows Click to Do / Phi Silica NPU
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Click to Do integra Phi Silica para operações locais sobre texto selecionado.
Mecanismo documentado: A configuração publicada em dezembro/2024 descreve quantização e prefill em blocos. A documentação NPU consultada em novembro/2026 descreve draft speculative decoding. São evidências de versões diferentes do ecossistema Phi; não se afirma uma única pilha simultânea e imutável.
Correspondência com esta base: Compressão de prompt é recurso do runtime NPU; a fonte não prova sua ativação em toda ação Click to Do.
Transferência proposta para modelo pequeno: Proposta: medir um executor local de reescrita/extração sobre seleções curtas, com contratos por backend, e adotar fallback somente após avaliar os erros reais.
Limite: Não fixa porte exato entre revisões nem prova fronteira. A documentação de novembro de 2026 anuncia mudança futura para Aion Instruct; todos os mecanismos têm escopo de versão/hardware. Fonte de 2024 não sustenta KV quadrático. Nenhuma destas configurações foi executada neste pacote.
Fontes: V4D-S003, V4D-S004, V4D-S009.

V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação expõe ferramenta de compressão utilizável em fluxo.
Mecanismo documentado: Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.
Correspondência com esta base: Compressão textual explícita.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.
Limite: Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S027.

V4D-C004 — Google / Chrome built-in AI / Summarizer API
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A documentação lista a Summarizer API no Chrome estável desde a versão 138.
Mecanismo documentado: Interface local de geração com modelo gerenciado pelo navegador e requisitos de disponibilidade.
Correspondência com esta base: Sumarização acessível via API; não demonstra técnica particular de poda/compressão.
Transferência proposta para modelo pequeno: Proposta: detectar disponibilidade local e limitar a tarefa a texto fornecido; manter o contrato de saída igual quando um backend alternativo for necessário.
Limite: Disponibilidade não constitui prova de implantação em cliente, volume de tráfego ou porte exato do modelo. As etapas de preview e estável precisam ser verificadas por API.
Fontes: V4D-S007.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## T006:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T006 → T033 [requires]
Como combinar: Identificar tipos antes de compactar.
Interface: Seções, tabelas, listas e seus identificadores.
Condição: Parser preservar unidades e fronteiras.
Aceite proposto: Verificar casos com tabela atravessando páginas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T006 → T044 [complements]
Como combinar: Expandir apenas o requisito insuficiente.
Interface: Lacuna, referência e orçamento restante.
Condição: Original permanecer acessível.
Aceite proposto: Medir releitura e recuperação da condição omitida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S027, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não declarar compressão sem perda sem prova.
- Preservar distinção entre citação literal e paráfrase.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar qualidade final por tipo de informação; compressão bem lida por fronteira pode falhar em 3–7B.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T018, T020, T021, T043, T052

## Fontes primárias associadas

### A-S015 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models

[https://aclanthology.org/2023.emnlp-main.825/](https://aclanthology.org/2023.emnlp-main.825/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão textual com orçamento e seleção iterativa de tokens.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S016 — Compressing Context to Enhance Inference Efficiency of Large Language Models

[https://aclanthology.org/2023.emnlp-main.391/](https://aclanthology.org/2023.emnlp-main.391/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Selective Context: remoção de redundância no contexto de entrada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S003 — RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation

[https://arxiv.org/abs/2310.04408](https://arxiv.org/abs/2310.04408)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressores extrativo e abstrativo orientados à tarefa; possibilidade de retornar contexto vazio quando não agrega informação.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S027 — LLMLingua Prompt Compression — Prompt flow

[https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html](https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração documentada de compressor e contrato de entrada/saída; não comprova carga real.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4D-S003 — Get started with Phi Silica in the Windows App SDK

[https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica](https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Execução local; diferenças NPU/GPU; especulação com modelo de rascunho na NPU; preparação do modelo e transição anunciada para Aion Instruct.

Limite: Página mutável consultada em 2026-11-05. Rollout retail/removação em janeiro de 2027 é plano futuro. Especulação e compressão NPU não estão disponíveis no caminho GPU descrito; não inferir equivalência entre revisões.

### V4D-S004 — Manage Click to Do

[https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do](https://learn.microsoft.com/en-us/windows/client-management/manage-click-to-do)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ações locais de texto do Click to Do usam Phi Silica em Copilot+ PCs; resposta exibida progressivamente e controles de administração.

Limite: Não demonstra memória persistente aprendida. Ação e seleção da interface não provam qual técnica de compressão interna foi utilizada em cada chamada.

### V4D-S005 — Pixel December 2023 feature drop

[https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Lançamento de Gemini Nano em Pixel 8 Pro e resumo offline no Recorder.

Limite: Não identifica o checkpoint nem sua contagem de parâmetros. Smart Reply no Gboard era developer preview; não confundir resumo com cadeia hierárquica ou destilação.

### V4D-S007 — Built-in AI APIs

[https://developer.chrome.com/docs/ai/built-in-apis](https://developer.chrome.com/docs/ai/built-in-apis)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade e estágio das APIs locais do Chrome; Summarizer documentado como estável desde Chrome 138.

Limite: Tabela é mutável e partes textuais podem acompanhar versões em ritmos diferentes. API disponível não comprova uso por cliente; não identifica porte exato do checkpoint.

### V4D-S009 — Phi Silica, small but mighty on-device SLM

[https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/](https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração Windows: quantização de pesos com QuaRot/GPTQ, ativações de 16 bits na configuração descrita, prefill em blocos de 64 e KV compartilhado entre fases.

Limite: Não confirma 3,3B para essa revisão: descreve derivado de Phi-3.5-mini. A generalização textual de crescimento quadrático do KV é imprecisa para cache padrão de arquitetura fixa; não foi adotada nesta curadoria. Especulação da API atual não é atribuída automaticamente a dezembro de 2024.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T007 — Response Caching por Hash

**Nome canônico:** Response Caching por Hash  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T007  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** exact response cache; cache exato por hash

## T007:C01 — conceito

Cache de resposta por identidade exata de uma requisição normalizada. Um hash funciona como endereço compacto de todos os fatores que alteram a resposta. Não reconhece paráfrases e não verifica a verdade do conteúdo armazenado.

Como funciona:
- Construir representação canônica da requisição e de suas dependências.
- Calcular hash criptográfico e procurar entrada válida no mesmo escopo.
- Retornar a resposta ou executar e gravar o resultado com política de expiração.

Nota de nomenclatura: Padrão de engenharia formado por cache exato e endereçamento por conteúdo; não é um algoritmo específico de LLM.

## T007:C02 — aplicacao

Quando usar:
- Transformações repetidas sobre o mesmo documento e versão.
- Consultas determinísticas de custo alto e dados estáveis.

Quando não usar:
- Evitar reutilização quando estado externo relevante não faz parte da chave ou das condições de validade.

Implementação proposta:
- Proposta: hashear modelo, parâmetros, prompt, fontes, schemas e namespace.
- Manter a requisição canônica ou sua descrição para auditar colisões lógicas.
- Não armazenar respostas incompletas, erros transitórios ou saídas sem validação mínima.

Aplicação LAI proposta:
Proposta LAI: cachear extrações técnicas verificadas por hash de arquivo e versão de schema; manter namespaces separados para evitar mistura entre contextos.

## T007:C03 — riscos_validacao

Armadilhas:
- Omitir a versão de uma fonte torna a chave semanticamente incompleta.
- Normalizar excessivamente pode tornar iguais entradas que significam coisas diferentes.

Métricas sugeridas:
- Acertos corretos e acertos indevidos.
- Tempo economizado e tamanho do armazenamento.

Testes propostos:
- Mudar um único campo decisivo e exigir uma chave diferente.
- Permutar campos de JSON sem alterar significado e verificar normalização estável.

## T007:C04 — perguntas_proveniencia

Pergunta: SHA-256 elimina todos os erros de cache?
Resposta: Não. Um bom hash não corrige uma chave que deixou de fora informação relevante.

Pergunta: Como tratar temperatura maior que zero?
Resposta: Reutilizar fixa uma amostra anterior; documente esse comportamento ou desative cache quando diversidade for necessária.

Pergunta: SHA-256 elimina todo risco de cache incorreto?
Resposta: Não. Um hash forte não corrige uma chave incompleta nem uma resposta originalmente errada; colisão de projeto costuma ser mais relevante que colisão criptográfica.

Pergunta: Cache de resposta pode repetir uma ferramenta de escrita?
Resposta: Reutilizar texto não equivale a executar nem confirmar um efeito. Operações de escrita precisam de identidade e reconciliação próprias, separadas deste cache.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T007:C05 — mecanismo_avancado

A chave deve representar a requisição efetiva, não apenas o texto visível da pergunta. Modelo, parâmetros, instruções, escopo e revisão das fontes podem alterar a resposta. Canonicalização resolve diferenças de serialização, como ordem de propriedades, mas não decide que duas instruções significam a mesma coisa. Normalizar arrays, tipos ou espaços significativos indevidamente cria colisões semânticas mesmo com hash criptográfico correto.

Condição de contorno:
Requisições dependentes de relógio, aleatoriedade desejada ou estado externo mutável não são reutilizáveis sem incorporar uma fronteira válida desses fatores.

Contrato proposto:
- Entradas: Envelope completo do pedido e versão da regra de canonicalização.
- Saídas: Chave, resposta elegível e metadados da execução que a originou.
- Estado: Entradas associadas à revisão das dependências e ao escopo de acesso.
- Invariante: Pedidos distintos em um fator que muda o resultado não recebem deliberadamente a mesma identidade.

Compromissos de projeto:
- Chaves completas diminuem hits, mas reduzem reutilização incorreta.
- Canonicalização acrescenta trabalho e exige tratamento rigoroso de números, Unicode e campos opcionais.

## T007:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: enviar objetos com propriedades em ordem diferente e depois mudar um parâmetro relevante. Os primeiros devem compartilhar a identidade definida; a alteração de parâmetro deve produzir outra chave.

Plano de avaliação proposto:
Avaliação proposta: comparar identidade de bytes e envelope canonicalizado com casos equivalentes e distintos. Medir hits corretos, colisões de significado, tempo de chaveamento e recuperação após mudança de política.

Comparações:
- T005 (alternative): Cache semântico busca equivalência aproximada; o hash depende de equivalência explicitamente definida.
- T061 (complements): Endereçamento por conteúdo pode armazenar os artefatos associados à resposta.

Afirmação rastreável:
RFC 8785 define representação JSON determinística apropriada a operações reproduzíveis de hashing.
Suporte: direct; fontes: V3A-S006
Limite: A especificação não define quais campos de uma requisição de LLM são semanticamente obrigatórios.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T007:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu identidade canônica da requisição. Aqui o cache ganha admissão por valor econômico e separação entre resultado calculado e apresentação.

Projeto e decomposição
Cacheie artefatos determinísticos antes da resposta linguística: extração validada, conjunto de candidatos ou tabela calculada. Isso mantém reutilização quando muda apenas o estilo solicitado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

Controle adaptativo
Use política de admissão que considere custo evitado e frequência prevista. Respostas enormes consultadas uma vez podem expulsar pequenos resultados caros e recorrentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

Validação contrafactual
Compare cache de resposta, cache intermediário e execução integral. Inclua tempo de serialização, transferência e verificação de dependências. Unidade de avaliação: requisição versionada. Teste duas apresentações do mesmo resultado calculado e uma terceira com configuração de cálculo diferente. As primeiras podem reutilizar o artefato intermediário, enquanto a terceira deve provocar recomputação. Medir esse padrão separa economia legítima de uma chave insuficiente. Avalie também quando transferir o artefato custa mais do que refazer uma computação pequena.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

USO AVANÇADO — Reformatação recorrente
Cenário: O mesmo relatório precisa formatos diferentes.
Estratégia: Reusar tabela validada e gerar apresentação por pedido; invalidar se qualquer fonte mudar.
Papel do modelo pequeno: 3–7B formata sem recalcular fatos.
Aceite proposto: Valores devem coincidir com artefato canônico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

USO AVANÇADO — Validação repetida
Cenário: Vários agentes verificam o mesmo arquivo.
Estratégia: Reusar laudo por hash do conteúdo, versão do validador e configuração. Resultado parcial não entra no cache.
Papel do modelo pequeno: Modelo pequeno interpreta laudo; código verifica identidade.
Aceite proposto: Arquivo alterado precisa provocar miss.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S006, V4A-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Formatador sobre resultado exato previamente validado.
8–14B: Explicador de laudos e diagnósticos cacheados por revisão.
15–30B: Sintetizador de múltiplos artefatos sem reutilizar conclusão incompatível.
Requisitos de treino/runtime: Armazenamento por chave e estatísticas de custo; separar conteúdo, configuração e versão do produtor.
Não aplicar quando: Resultado depende de estado externo não representado na chave.

## T007:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q011.

## T007:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T007 → T061 [complements]
Como combinar: Endereçar artefatos reutilizáveis pelo conteúdo.
Interface: Digest, codec e versão do formato.
Condição: Bytes e interpretação forem estáveis.
Aceite proposto: Alterar configuração e verificar nova identidade lógica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S006, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T007 → T150 [complements]
Como combinar: Unificar computações simultâneas da mesma chave.
Interface: Chave completa e promessa de resultado.
Condição: Cancelamento de cliente não apagar trabalho compartilhado.
Aceite proposto: Executar pedidos concorrentes e contar computações reais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S006, V4A-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não armazenar falha transitória como resultado definitivo.
- Conservar fonte e idade do artefato cacheado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar trabalho evitado com corretude idêntica; cache não deve ser creditado como capacidade cognitiva.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T031, T061, T157

## Fontes primárias associadas

### A-S005 — LLM Caching

[https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/](https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico com embeddings, limiar de distância, TTL e filtros de acesso.

Limite: Documentação consultada da versão 0.10.0, não afirma ser a versão corrente do pacote.

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S006 — RFC 8785: JSON Canonicalization Scheme (JCS)

[https://www.rfc-editor.org/rfc/rfc8785.html](https://www.rfc-editor.org/rfc/rfc8785.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Serialização JSON determinística para hashing e assinatura; preservação de conteúdo e restrições do formato. Caching é aplicação editorial. 

Limite: RFC informativo, não norma IETF Standards Track. Não fornece autorização, semântica de equivalência de pedidos nem veracidade do conteúdo.

### V4A-S010 — The CacheLib Caching Engine: Design and Experiences at Scale

[https://www.usenix.org/conference/osdi20/presentation/berg](https://www.usenix.org/conference/osdi20/presentation/berg)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção de CacheLib no Facebook e requisitos comuns de caches.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T008 — Hierarchical Summarization

**Nome canônico:** Hierarchical Summarization  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** sumarização hierárquica

## T008:C01 — conceito

Cria resumos em níveis: partes são sintetizadas, grupos de resumos formam sínteses maiores e cada nível conserva vínculos aos seus descendentes. Permite navegar por visão geral e detalhe, mas níveis superiores acumulam perdas se não houver revisão e acesso aos originais.

Como funciona:
- Separar o conteúdo em unidades coerentes e identificáveis.
- Resumir unidades e depois grupos, respeitando orçamento por nível.
- Guardar relações pai-filho e evidências de afirmações importantes.

## T008:C02 — aplicacao

Quando usar:
- Coleções extensas com estrutura temática ou documental.
- Relatórios gerais que precisam permitir rastreamento até trechos específicos.

Quando não usar:
- Não usar o resumo raiz como substituto dos dados quando a resposta exige detalhe exato.

Implementação proposta:
- Proposta: construir árvore com versões de nós e hashes dos filhos.
- Recalcular apenas ancestrais afetados por uma atualização.
- Recuperar folhas para conferir números ou conflitos citados em um resumo superior.

Aplicação LAI proposta:
Proposta LAI: organizar conhecimento por software, módulo e contrato; usar sínteses para descoberta e documentos originais para comprovação.

## T008:C03 — riscos_validacao

Armadilhas:
- O mesmo fato pode ser contado duas vezes em ramos diferentes.
- Mudança em uma folha pode deixar ancestrais desatualizados.

Métricas sugeridas:
- Fidelidade entre nós pais e fontes descendentes.
- Cobertura de perguntas globais e pontuais por nível.

Testes propostos:
- Alterar uma folha e exigir invalidação dos resumos dependentes.
- Perguntar por uma exceção rara e verificar navegação ao texto original.

## T008:C04 — perguntas_proveniencia

Pergunta: É igual ao RAPTOR?
Resposta: RAPTOR é uma arquitetura específica que combina agrupamento, embeddings e resumos recursivos. A sumarização hierárquica é mais geral.

Pergunta: Todos os resumos precisam caber na chamada?
Resposta: Não. A hierarquia existe justamente para selecionar níveis e ramos conforme a pergunta.

Pergunta: Uma árvore de resumos garante rastreabilidade?
Resposta: Somente se a implementação preservar referências e versões. Uma árvore contendo apenas prosa pode perder a ligação verificável com as fontes.

Pergunta: Devo sempre recuperar a raiz?
Resposta: Não. A raiz pode ser genérica demais. Selecione o nível conforme a pergunta e expanda até evidência suficiente, respeitando o orçamento.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T008:C05 — mecanismo_avancado

A profundidade da hierarquia influencia tanto navegação quanto número de transformações sofridas por uma evidência. Atualizar uma folha exige invalidar os resumos que dependem dela; conservar um nó superior antigo junto de folhas novas cria versões incoerentes. Uma política de reconstrução deve registrar dependências e publicar uma árvore consistente, em vez de trocar nós isolados sem fronteira identificável.

Condição de contorno:
Quando perguntas exigem detalhes que os resumos descartaram e as folhas não são recuperáveis, mais níveis apenas reorganizam a perda.

Contrato proposto:
- Entradas: Unidades originais versionadas, agrupamento e orçamento por nível.
- Saídas: Nós resumidos com referências aos descendentes e à revisão da árvore.
- Estado: DAG de dependências, versões de sumarizadores e fila de nós inválidos.
- Invariante: Cada afirmação resumida é distinguida da evidência original e aponta para sua origem.

Compromissos de projeto:
- Mais níveis reduzem contexto por leitura, mas aumentam ingestão e manutenção.
- Resumos amplos ajudam perguntas globais, enquanto trechos locais preservam especificidade e exceções.

## T008:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: corrigir uma folha depois de construir a hierarquia. Consultas não devem combinar a correção com um resumo ancestral que ainda afirme o valor antigo sem sinalizar desatualização.

Plano de avaliação proposto:
Avaliação proposta: comparar busca apenas nas folhas com busca em múltiplos níveis, mantendo o orçamento final. Medir recuperação de fatos, perguntas globais, custo de atualização e proporção de nós obsoletos após mudanças.

Comparações:
- T023 (complements): A árvore recursiva explicita uma organização possível da sumarização hierárquica.
- T030 (complements): RAPTOR combina hierarquia com embeddings, agrupamento e recuperação em seus níveis.

Afirmação rastreável:
O código oficial de RAPTOR permite construir, persistir e carregar uma árvore para recuperação.
Suporte: direct; fontes: V3A-S011
Limite: A publicação de estados consistentes e a invalidação incremental aqui descritas são propostas de engenharia.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T008:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 abordou invalidação de ancestrais. A novidade é síntese com orçamento desigual e expansão direcionada por desacordo entre níveis.

Projeto e decomposição
Distribua orçamento por diversidade de evidências, não pelo número de folhas. Um ramo consensual pode receber menos espaço que outro com condições incompatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Controle adaptativo
Conserve resumo e contraexemplos separados em cada nó. Se a conclusão do pai excluir exceção presente no filho, abrir o ramo antes de responder.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Validação contrafactual
Compare árvore uniforme e alocação por divergência. Avalie preservação de exceções e custo de expansão, sem confundir profundidade com qualidade. Unidade de avaliação: árvore documental. Introduza uma exceção sustentada por uma única folha num ramo com muitos relatos concordantes. A síntese deve preservar a exceção quando ela afeta a pergunta, mesmo que a maioria dos documentos repita a regra geral. Compare seleção por quantidade de folhas e por diversidade de condições, registrando quais requisitos desapareceram em cada nível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Revisão de políticas
Cenário: Departamentos descrevem regras parcialmente diferentes.
Estratégia: Resumir por escopo, detectar incompatibilidades e produzir síntese condicionada ao departamento.
Papel do modelo pequeno: 8–14B resume folhas; 15–30B integra conflitos.
Aceite proposto: Nenhuma regra local vira regra universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Panorama técnico
Cenário: Muitos relatórios sobre sistemas distintos.
Estratégia: Gerar mapas temáticos e abrir folhas somente para afirmações decisivas ou contestadas.
Papel do modelo pequeno: 3–7B extrai evidência por tema.
Aceite proposto: Toda conclusão comparativa deve apontar suportes específicos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de afirmações e exceções dentro de uma folha.
8–14B: Resumidor intermediário de poucos documentos relacionados.
15–30B: Integrador de ramos conflitantes com expansão seletiva.
Requisitos de treino/runtime: Árvore com vínculos estáveis e orçamento por nó; rotular divergência separadamente de redundância.
Não aplicar quando: As relações centrais cruzam tantos ramos que a hierarquia oculta mais do que organiza.

## T008:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C024 — Microsoft Research / Project GraphRAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto de pesquisa publica combinação de extração, análise de redes e geração.
Mecanismo documentado: Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.
Correspondência com esta base: Síntese hierárquica faz parte da abordagem.
Transferência proposta para modelo pequeno: Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.
Limite: Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S024, A-S024.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q021.

## T008:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T008 → T029 [alternative]
Como combinar: Usar comunidades quando relações cruzarem a árvore.
Interface: Conjunto de documentos e vínculos temáticos.
Condição: Grafo representar relações sustentadas por fontes.
Aceite proposto: Comparar cobertura de relações entre ramos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T008 → T044 [complements]
Como combinar: Abrir descendente responsável por exceção.
Interface: node_id, exceção e referência de folha.
Condição: Origem da exceção permanecer rastreável.
Aceite proposto: Recuperar detalhe sem expandir toda a árvore.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar repetição da mesma fonte como consenso.
- Preservar diferença entre resumo do nó e evidência primária.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar síntese de exceções distribuídas; uma árvore maior não implica melhor entendimento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T023, T026, T030, T062

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S011 — RAPTOR: official implementation

[https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore recuperável, serialização e interfaces de sumarização, embeddings e resposta. Código de pesquisa não instalado.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S021 — Recursively Summarizing Books with Human Feedback

[https://arxiv.org/abs/2109.10862](https://arxiv.org/abs/2109.10862)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Decomposição recursiva de sumarização e treinamento com feedback humano; avaliação em níveis distintos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### A-S024 — Welcome to GraphRAG

[https://microsoft.github.io/graphrag/](https://microsoft.github.io/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração de grafo, hierarquia de comunidades, resumos e consultas estruturadas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T009 — RAG — Retrieval-Augmented Generation; incluindo RAG temporal

**Nome canônico:** RAG com filtragem temporal explícita  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T009  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** RAG — Retrieval-Augmented Generation; Retrieval-Augmented Generation; geração aumentada por recuperação; RAG temporal; temporal retrieval-augmented generation

## T009:C01 — conceito

RAG recupera informação externa e a fornece à geração para fundamentar respostas. RAG temporal acrescenta uma interpretação explícita de quando a evidência vale e, quando necessário, de quando passou a ser conhecida pelo sistema. Não constitui um algoritmo único: combina recuperação com modelagem temporal, versionamento e critérios de citação. Nem recuperação nem recência garantem verdade.

Como funciona:
- Transformar a pergunta em consulta, escopo de acesso e referência temporal; distinguir “válido em junho” de “o que sabíamos em junho”.
- Filtrar versões elegíveis por intervalos de validade e de registro antes da seleção final de evidências.
- Combinar busca lexical ou vetorial, reranking e geração com documento, versão, trecho e datas verificáveis.

## T009:C02 — aplicacao

Quando usar:
- Políticas que mudam, contratos com vigência, histórico de projetos e decisões que precisam ser reconstruídas como eram em determinada data.

Quando não usar:
- Para substituir consultas transacionais exatas ou inferir uma data ausente apenas porque o documento foi indexado recentemente.

Implementação proposta:
- Proposta: armazenar valid_from/valid_to e recorded_from/recorded_to, além de origem, identidade e controle de acesso; adotar convenção explícita para limites dos intervalos.
- Preservar correções tardias como novas versões. Indexação recente de um documento antigo não muda a data de validade do fato.
- Ao faltar data ou existir conflito, retornar a limitação e evidências concorrentes; não escolher silenciosamente a versão com maior similaridade.

Aplicação LAI proposta:
Proposta LAI: exigir data de referência em consultas de evolução do projeto e manter citações que permitam reconstruir o estado consultado.

## T009:C03 — riscos_validacao

Armadilhas:
- Recency boosting sozinho favorece documentos novos, mas não responde consultas históricas.
- Filtrar depois de top-k pequeno pode deixar de fora toda evidência temporalmente correta.

Métricas sugeridas:
- Recall de evidências elegíveis, acurácia das respostas históricas, vazamento de versões futuras e suporte das citações.

Testes propostos:
- Teste proposto: cadastrar uma regra de janeiro e substituição de março; perguntas sobre fevereiro e abril devem selecionar versões diferentes.
- Inserir em maio uma correção retroativa e testar separadamente validade histórica e conhecimento disponível antes da correção.

## T009:C04 — perguntas_proveniencia

Pergunta: Ordenar documentos por data de publicação já produz RAG temporal?
Resposta: É apenas uma heurística de recência. Consultas temporais exigem interpretar a pergunta e verificar quais versões eram válidas no intervalo solicitado.

Pergunta: Uma correção recebida hoje deve alterar toda resposta sobre o passado?
Resposta: Depende da pergunta: pode corrigir o fato historicamente válido, mas não o que o sistema sabia antes de recebê-la.

Pergunta: Uma citação correta garante resposta correta?
Resposta: Não. O trecho pode existir e ainda ser mal interpretado, estar fora do corte temporal ou não sustentar a conclusão apresentada.

Pergunta: Quando não recuperar é aceitável?
Resposta: Quando o contrato da tarefa dispensa evidência externa e a decisão é justificada. Uma pergunta factual atual ou histórica pode exigir busca mesmo que pareça simples.

Escopo das fontes:
O artigo RAG fundamenta recuperação mais geração; XTDB fundamenta validade e tempo de sistema. A combinação e o contrato temporal LAI são propostas de arquitetura.

## T009:C05 — mecanismo_avancado

A qualidade final resulta de etapas separáveis: existir evidência elegível, recuperá-la, preservar seu sentido no contexto e usá-la corretamente. RAG temporal acrescenta filtros de validade e conhecimento: uma correção publicada hoje pode mudar a resposta sobre ontem sem mudar o que o sistema sabia ontem. Avaliar só similaridade do trecho mistura erros de indexação, tempo e leitura.

Condição de contorno:
Se o acervo não contém evidência suficiente ou as datas representam publicação sem validade de domínio, recuperação não pode fabricar uma resposta temporal bem definida.

Contrato proposto:
- Entradas: Pergunta, escopo, instante de validade e eventual instante de conhecimento.
- Saídas: Resposta com evidências elegíveis, versões e lacunas explicitadas.
- Estado: Índices por revisão, metadados temporais e registro dos candidatos utilizados.
- Invariante: Nenhuma evidência posterior ao corte de conhecimento é apresentada como já conhecida naquele corte.

Compromissos de projeto:
- Filtros temporais rígidos aumentam precisão histórica, mas exigem metadados confiáveis.
- Mais candidatos ampliam cobertura e também ruído, custo e oportunidades de contradição.

## T009:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um fato válido no passado e uma correção registrada depois. Perguntas sobre o passado segundo conhecimento atual e segundo conhecimento antigo devem produzir resultados compatíveis com seus cortes diferentes.

Plano de avaliação proposto:
Avaliação proposta: isolar recuperação e leitura usando candidatos conhecidos e depois o pipeline completo. Medir evidência elegível recuperada, atribuição, atualização e abstenção; comparar com busca sem filtro temporal sobre o mesmo corpus.

Comparações:
- T056 (complements): Bitemporalidade explicita os dois cortes necessários a consultas históricas mais rigorosas.
- T025 (complements): Adaptive RAG decide estratégias adicionais de recuperação conforme a necessidade observada.

Afirmação rastreável:
LongMemEval distingue atualização de conhecimento, raciocínio temporal e abstenção como capacidades de memória.
Suporte: related; fontes: V3A-S002
Limite: A avaliação de memória apoia a separação de capacidades; o contrato temporal proposto não é uma API do benchmark.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T009:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou recuperação temporal e leitura. Aqui o desenho novo é orçamento de evidência orientado por tipo de afirmação e custo do erro.

Projeto e decomposição
Classifique a resposta em afirmações verificáveis antes de preencher contexto. Uma data exige fonte exata; uma comparação exige evidências simétricas; um panorama exige diversidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

Controle adaptativo
Monte pacotes por afirmação com apoio, contradição e lacuna. O leitor pequeno deve decidir somente dentro do pacote, sem completar campos ausentes com lembrança paramétrica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

Validação contrafactual
Compare recuperação única e pacotes de evidência mantendo o mesmo corpus. Conte respostas parcialmente corretas e citações que não sustentam a frase. Unidade de avaliação: pergunta com evidências. Use casos em que o documento recuperado é correto, mas o trecho não sustenta o atributo pedido. O sistema deve marcar essa célula como insuficiente, em vez de premiar a presença de uma citação. Para comparações, medir cobertura por alternativa impede que a opção mais documentada pareça melhor apenas por receber mais contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

USO AVANÇADO — Comparação de produtos técnicos
Cenário: Atributos vêm de documentos diferentes.
Estratégia: Recuperar cada atributo por item, normalizar unidades em código e gerar tabela com células ausentes explícitas.
Papel do modelo pequeno: 3–7B extrai; 8–14B redige comparação.
Aceite proposto: Cada célula preenchida precisa de suporte elegível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

USO AVANÇADO — Investigação de divergência
Cenário: Duas fontes discordam sobre uma decisão.
Estratégia: Recuperar versões e contexto de autoria, separar conflito factual de diferença de escopo e evitar votação por quantidade.
Papel do modelo pequeno: 15–30B integra versões incompatíveis.
Aceite proposto: Resposta deve preservar conflito ainda não resolvido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S019, V4A-S014.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor extrativo de pacotes pequenos com abstenção por campo.
8–14B: Leitor especializado em citações e comparação de poucas fontes.
15–30B: Integrador multietapas quando cada elo possuir evidência recuperável.
Requisitos de treino/runtime: Esquema por afirmação, filtros e referências estáveis; especialização contextual é opcional, não garantia.
Não aplicar quando: As fontes necessárias não existem ou o objetivo exige descoberta que o corpus não sustenta.

## T009:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Recuperação antecede geração e inclui múltiplas fontes.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Documentação oferece índice semântico para Chat e cloud agent.
Mecanismo documentado: Busca de seções de código por significado e atualização do índice.
Correspondência com esta base: Contexto recuperado do repositório orienta respostas.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.
Limite: Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S023.

V4A-C020 — Google / NotebookLM com fontes multimodais
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Produto oferece análise de documentos, áudio e vídeo com citações.
Mecanismo documentado: Conteúdo de fontes e transcrições fundamenta respostas referenciadas.
Correspondência com esta base: Fundamentação em fontes é relacionada, sem pipeline interno publicado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.
Limite: Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S025.

V4A-C021 — Google DeepMind / DataGemma RIG/RAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto publica variantes para fundamentar geração em Data Commons.
Mecanismo documentado: RIG troca números por dados; RAG usa modelo Gemma para preparar contexto de Gemini 1.5 Pro.
Correspondência com esta base: Recuperação contextual é objetivo explícito.
Transferência proposta para modelo pequeno: Proposta de engenharia: Testar roteador pequeno para consulta estatística, mantendo unidade, período e população.
Limite: RAG citado não é pipeline integral 3–30B; não há implantação de usuário comprovada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S014.

V4A-C022 — Salesforce / SFR-RAG 9B
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa apresenta modelo de nove bilhões especializado em fidelidade contextual.
Mecanismo documentado: Pós-treino privilegia leitura de evidência, citações e reconhecimento de insuficiência.
Correspondência com esta base: Leitor especializado para RAG.
Transferência proposta para modelo pequeno: Proposta de engenharia: Considerar leitor 8–14B especializado e comparar com modelo geral do mesmo porte.
Limite: Resultados experimentais publicados não garantem produção nem superioridade universal; nenhuma pergunta de benchmark foi incorporada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S019.

V4B-C025 — Google DeepMind / RETRO
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: O trabalho avalia um modelo treinado para consumir trechos recuperados por uma arquitetura específica de atenção.
Mecanismo documentado: Codificação de vizinhos recuperados e cross-attention por trechos fazem parte da função treinada.
Correspondência com esta base: A família usa conhecimento recuperado, mas não equivale a anexar trechos a um prompt comum.
Transferência proposta para modelo pequeno: Proposta: estudar custo e benefício de arquitetura treinada versus RAG externo antes de escolher uma intervenção em 3–30B.
Limite: Pesquisa não comprova produto implantado. Alterar um checkpoint convencional para reproduzir RETRO requer treinamento e compatibilidade; não é uma opção intercambiável de serving.
Fontes: B-S026.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q010, V4A-Q016, V4A-Q020.

## T009:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T009 → T028 [complements]
Como combinar: Ordenar candidatos por necessidade de evidência.
Interface: claim_id, candidato e tipo de suporte.
Condição: Reranker não excluir contradições obrigatórias.
Aceite proposto: Avaliar cobertura por afirmação, além do ranking global.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S019, V4A-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T009 → T200 [requires]
Como combinar: Verificar suporte após geração.
Interface: Frase, citação e trecho utilizado.
Condição: Verificador acessar a origem exata.
Aceite proposto: Detectar citação verdadeira mas irrelevante para a frase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S019, V4A-S014. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não converter ausência de documento em prova de inexistência.
- Separar dados recuperados de instruções de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar fidelidade contextual e abstenção; capacidade geral do modelo permanece fora da conclusão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T027, T056, T072, P007

## Fontes primárias associadas

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S032 — Time in XTDB

[https://docs.xtdb.com/about/time-in-xtdb.html](https://docs.xtdb.com/about/time-in-xtdb.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tempo de validade e tempo do sistema como eixos de consulta distintos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S002 — LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[https://arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separação entre indexação, recuperação e leitura; atualização de conhecimento, tempo e abstenção como capacidades distintas.

Limite: Foram consultados resumo e descrição geral, sem ler perguntas ou gabaritos do benchmark. Não transferir resultados publicados para a LAI.

### V3A-S009 — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

[https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação e crítica adaptativas aprendidas com tokens de reflexão; distingue arquitetura treinada de simples instrução de autocrítica.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S014 — DataGemma

[https://deepmind.google/models/gemma/datagemma/](https://deepmind.google/models/gemma/datagemma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RIG substitui números por dados; variante RAG prepara contexto consumido por Gemini 1.5 Pro.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### B-S026 — Improving language models by retrieving from trillions of tokens

[https://arxiv.org/abs/2112.04426](https://arxiv.org/abs/2112.04426)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RETRO combina recuperação, codificador e cross-attention por trechos.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews

[https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto fundamentado em fontes com citações e transcrições; recursos disponíveis.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T010 — Fixed-Size Chunking

**Nome canônico:** Fixed-Size Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T010  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação de tamanho fixo

## T010:C01 — conceito

Divide documentos em segmentos de tamanho alvo medido em caracteres, palavras ou tokens, geralmente com sobreposição opcional. O tamanho só faz sentido acompanhado da unidade e do tokenizer. É uma linha de base simples e reproduzível para construir índices.

Como funciona:
- Definir unidade, tamanho máximo e quantidade de sobreposição.
- Percorrer o documento preservando offsets e identificador da origem.
- Indexar cada trecho com metadados suficientes para localizar o original.

## T010:C02 — aplicacao

Quando usar:
- Primeiro protótipo de recuperação e comparação de estratégias.
- Documentos relativamente uniformes sem estrutura confiável.

Quando não usar:
- É insuficiente quando tabelas, código ou cláusulas devem permanecer como unidades completas.

Implementação proposta:
- Proposta: aplicar tokenizer do embedding e respeitar seu limite real.
- Guardar início e fim do trecho e versão do segmentador.
- Avaliar vários tamanhos no mesmo conjunto de perguntas, mantendo filtros e retriever constantes.

Aplicação LAI proposta:
Proposta LAI: usar como baseline mensurável para manuais; preferir parsers estruturais em contratos de eventos, schemas e código.

## T010:C03 — riscos_validacao

Armadilhas:
- Sobreposição excessiva aumenta duplicação no contexto.
- Quebrar uma condição da sua consequência prejudica interpretação.

Métricas sugeridas:
- Distribuição real dos tamanhos e tokens descartados pelo embedding.
- Recall de respostas cruzando fronteiras de trechos.

Testes propostos:
- Colocar pergunta e resposta em lados opostos de uma fronteira.
- Reconstituir cobertura de offsets e detectar lacunas na ingestão.

## T010:C04 — perguntas_proveniencia

Pergunta: Quinhentos caracteres equivalem a quinhentos tokens?
Resposta: Não. A correspondência varia com idioma, símbolos e tokenizer.

Pergunta: Mais overlap resolve qualquer quebra?
Resposta: Não. Pode ajudar em fronteiras próximas, mas não substitui preservação da estrutura do documento.

Pergunta: Sobreposição deve ser removida antes do embedding?
Resposta: Se remover o conteúdo sobreposto, muda o método. A deduplicação costuma ser considerada na montagem dos candidatos, preservando o contexto usado na indexação.

Pergunta: Tokens e caracteres produzem o mesmo tamanho efetivo?
Resposta: Não. Idioma, código e símbolos mudam a relação; o contrato deve usar a unidade realmente relevante para o consumidor.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T010:C05 — mecanismo_avancado

Tamanho e sobreposição determinam quantidade de unidades e redundância. Para um documento longo com N tokens, blocos de c tokens e sobreposição o<c produzem aproximadamente N/(c-o) blocos, desconsiderando bordas. O orçamento de recuperação deve considerar duplicação de evidências entre vizinhos; contar os mesmos tokens duas vezes pode expulsar outra fonte relevante do contexto final.

Condição de contorno:
O modelo deixa de ser uma aproximação útil para documentos curtos, segmentação por caracteres ou processamento que altera a tokenização entre ingestão e consulta.

Contrato proposto:
- Entradas: Texto normalizado, tokenizer identificado, tamanho e sobreposição declarados.
- Saídas: Chunks com offsets, ordem e revisão do documento de origem.
- Estado: Versão do segmentador e mapeamento entre bytes e unidades indexadas.
- Invariante: Todo trecho recuperado pode ser relacionado a uma região identificável do original.

Compromissos de projeto:
- Blocos maiores preservam entorno, mas podem diluir sinais específicos na representação vetorial.
- Sobreposição protege fronteiras, porém aumenta índice, ingestão e repetição na resposta.

## T010:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: posicionar uma condição e sua exceção em lados opostos da fronteira. Comparar recuperação com e sem sobreposição e verificar se a montagem reconhece que o primeiro trecho está incompleto.

Plano de avaliação proposto:
Avaliação proposta: usar tamanho fixo como baseline e variar tamanho e sobreposição mantendo corpus, embeddings e orçamento de resposta. Medir recall de evidências, redundância, custo de índice e qualidade da resposta, sem escolher pelo número bruto de chunks.

Comparações:
- T011 (alternative): Fronteiras semânticas acrescentam cálculo; precisam demonstrar ganho sobre esta linha de base.
- T032 (complements): Trechos pequenos podem localizar um pai maior que fornece contexto após a recuperação.

Afirmação rastreável:
Um estudo comparativo não encontrou ganhos consistentes que justificassem sempre o custo adicional da segmentação semântica.
Suporte: direct; fontes: V3A-S013
Limite: Esse resultado é restrito às tarefas e configurações avaliadas; não demonstra superioridade universal do tamanho fixo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T010:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 calculou duplicação por overlap. Aqui chunks fixos são dimensionados pela tarefa e por restrições de leitura do modelo.

Projeto e decomposição
Use varredura de tamanhos na validação e escolha pelo custo por resposta correta. Chunks menores aumentam candidatos; maiores diluem sinais e ocupam leitura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

Controle adaptativo
Trate overlap como orçamento de relações atravessando fronteiras. Registre onde uma resposta exige dois chunks, para ajustar sobreposição com evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

Validação contrafactual
Compare tamanhos com mesmo orçamento final de tokens, evitando favorecer configuração que simplesmente fornece mais conteúdo ao leitor. Unidade de avaliação: documento com fronteiras. Crie documentos com resposta perto de cada posição possível da fronteira e com condições separadas por diferentes distâncias. A curva de cobertura por distância ajuda a escolher overlap com base em dependências reais. Controle o orçamento total recuperado: duplicar contexto através de sobreposição não deve ser confundido com melhora intrínseca da segmentação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

USO AVANÇADO — Logs padronizados
Cenário: Registros longos têm formato estável.
Estratégia: Particionar por teto de tokens respeitando registros completos; recuperar vizinhos apenas quando uma operação cruza a borda.
Papel do modelo pequeno: 3–7B identifica eventos tipados.
Aceite proposto: Nenhum registro obrigatório pode aparecer mutilado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

USO AVANÇADO — Documentação homogênea
Cenário: Manuais repetem estrutura previsível.
Estratégia: Criar grade de tamanhos, medir cobertura por pergunta e escolher configuração por família documental.
Papel do modelo pequeno: 8–14B responde com contexto de poucos chunks.
Aceite proposto: Aceitar tamanho que preserve qualidade dentro do prazo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, A-S007.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor com pequeno conjunto de chunks e campos previamente identificados.
8–14B: Comparador de chunks adjacentes para requisitos que cruzam fronteiras.
15–30B: Síntese com vários chunks quando benefício superar custo de leitura.
Requisitos de treino/runtime: Tokenizer correto, offsets e avaliação reservada por documento; segmentação continua determinística.
Não aplicar quando: Tabelas ou relações essenciais são rompidas repetidamente pelo teto fixo.

## T010:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Tamanho fixo configurável.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T010:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T010 → T032 [complements]
Como combinar: Expandir vizinhança quando o trecho é insuficiente.
Interface: chunk_id, documento, offsets e parent_id.
Condição: Pai pertencer à mesma revisão.
Aceite proposto: Verificar que expansão recupera condição sem duplicar evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T010 → T042 [requires]
Como combinar: Dimensionar recuperação pela janela do consumidor.
Interface: Tokens por chunk e reserva de resposta.
Condição: Contar serialização efetiva.
Aceite proposto: Comparar configurações sob orçamento idêntico.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, A-S007. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter offsets antes e depois da normalização.
- Não duplicar confiança por sobreposição textual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar extração de fatos próximos às bordas; grande janela não substitui análise das fronteiras.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T011, T012, T033

## Fontes primárias associadas

### A-S004 — Splitting recursively

[https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores ordenados, limite de tamanho e sobreposição na divisão recursiva de texto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S013 — Is Semantic Chunking Worth the Computational Cost?

[https://arxiv.org/abs/2410.13070](https://arxiv.org/abs/2410.13070)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de segmentação semântica e tamanho fixo em recuperação de documentos, evidência e respostas; ganhos não universais.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T011 — Semantic Chunking

**Nome canônico:** Semantic Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T011  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação semântica

## T011:C01 — conceito

Escolhe fronteiras de trechos a partir de mudanças de significado, frequentemente comparando embeddings de sentenças ou grupos vizinhos. A noção de mudança depende do modelo e do limiar. A palavra semântico não garante automaticamente melhor recuperação.

Como funciona:
- Segmentar o texto em sentenças ou unidades iniciais.
- Medir a proximidade entre grupos vizinhos e propor fronteiras.
- Aplicar limites de tamanho e preservar posições na fonte.

## T011:C02 — aplicacao

Quando usar:
- Documentos longos que alternam temas sem cabeçalhos claros.
- Texto livre no qual cortes fixos separam explicações relacionadas.

Quando não usar:
- Não substitui um parser quando a estrutura formal do documento já é conhecida.

Implementação proposta:
- Proposta: testar limiares em documentação portuguesa e código misto.
- Impor teto em tokens do embedder mesmo quando não aparece mudança temática.
- Comparar custo de ingestão e recall com uma divisão recursiva simples.

Aplicação LAI proposta:
Proposta LAI: experimentar em transcrições e bases teóricas; manter fronteiras e documentos originais para revisar erros do segmentador.

## T011:C03 — riscos_validacao

Armadilhas:
- Paráfrases podem esconder uma mudança decisiva de regra.
- Pontuação ruim e transcrições ruidosas comprometem a segmentação inicial.

Métricas sugeridas:
- Coesão dos trechos e recall por pergunta.
- Custo de embeddings por documento ingerido.

Testes propostos:
- Inserir mudança de tema com vocabulário parecido e inspecionar a fronteira.
- Verificar que um capítulo homogêneo extenso não excede o limite de embedding.

## T011:C04 — perguntas_proveniencia

Pergunta: Semantic chunking usa sempre uma LLM geradora?
Resposta: Não. Muitas implementações usam embeddings e regras de distância, sem geração de texto.

Pergunta: Devo substituir todos os trechos fixos?
Resposta: Só após comparar em perguntas reais. A complexidade e o custo adicionais precisam produzir ganho observado.

Pergunta: Limiar por percentil evita calibragem?
Resposta: Não. Ele troca a escala absoluta por uma regra relativa, cuja frequência de cortes ainda precisa ser justificada e testada.

Pergunta: Coerência do chunk basta para boa recuperação?
Resposta: Não. A unidade também precisa conter o fato e suas condições em tamanho que o recuperador e o gerador utilizem adequadamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T011:C05 — mecanismo_avancado

O detector de fronteiras depende de como representa cada sentença e seu entorno. Um limiar absoluto de distância e um percentil das distâncias do próprio documento produzem comportamentos diferentes: o segundo pode impor cortes até em um texto uniforme. Mudanças de idioma, listas e tabelas também alteram a distribuição dos escores sem necessariamente representar uma troca real de assunto.

Condição de contorno:
Quando coerência local já é preservada por seções naturais, o cálculo semântico pode acrescentar custo sem melhorar a evidência recuperada.

Contrato proposto:
- Entradas: Texto, segmentação de sentenças, embedding e política explícita de fronteiras.
- Saídas: Chunks com escores de corte, offsets e limites de tamanho.
- Estado: Versões do segmentador e do modelo, mais distribuição observada de tamanhos.
- Invariante: A fronteira semântica não elimina a necessidade de limite operacional do consumidor.

Compromissos de projeto:
- Grupos maiores preservam continuidade, mas podem acumular assuntos independentes.
- Ajustar cortes por documento adapta a distribuição, porém dificulta comparar escores entre coleções.

## T011:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar um documento uniforme e outro com mudança de idioma sem mudança de assunto. Verificar cortes artificiais e a preservação de referências que atravessam a fronteira.

Plano de avaliação proposto:
Avaliação proposta: comparar tamanho fixo, divisão estrutural e semântica sob orçamento final equivalente. Controlar embedding e reranker; medir ingestão, distribuição de tamanho, evidência recuperada e resposta, incluindo documentos fora do domínio de ajuste.

Comparações:
- T010 (alternative): Tamanho fixo fornece baseline de custo e permite identificar ganhos atribuíveis às fronteiras.
- T033 (alternative): Estrutura editorial pode oferecer fronteiras úteis sem inferir mudança de assunto por vetor.

Afirmação rastreável:
O estudo de Qu e colaboradores encontrou benefícios inconsistentes da segmentação semântica nas tarefas examinadas.
Suporte: direct; fontes: V3A-S013
Limite: Não é prova de inutilidade; o resultado exige avaliar domínio, baseline e custo específicos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T011:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 questionou custo e limiar semântico. Aqui o foco é segmentação estável perante pequenas edições e adaptação por domínio.

Projeto e decomposição
Uma edição curta pode mudar várias fronteiras quando o limiar depende da distribuição do documento. Compare estabilidade dos IDs e custo de reindexação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

Controle adaptativo
Calibre segmentação separadamente para narrativa, perguntas frequentes e documentação técnica. Similaridade entre frases não identifica automaticamente unidade útil de resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

Validação contrafactual
Meça qualidade de recuperação e churn de chunks após alterações locais. Um ganho pequeno pode não justificar reconstrução frequente do índice. Unidade de avaliação: família de documentos. Uma edição de pontuação e outra de assunto devem produzir efeitos distintos. A primeira idealmente preserva a organização útil; a segunda pode exigir nova divisão. Medir churn de IDs, embeddings refeitos e respostas alteradas torna visível o custo operacional da segmentação semântica, que uma avaliação estática de recuperação tende a omitir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

USO AVANÇADO — Documentos vivos
Cenário: A base recebe edições diárias.
Estratégia: Identificar regiões alteradas, recomputar fronteiras locais e comparar com segmentação integral antes de publicar.
Papel do modelo pequeno: 3–7B apenas valida tópico de fronteiras candidatas.
Aceite proposto: Mudança local não deve esconder evidência fora da região.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

USO AVANÇADO — Corpus multilíngue
Cenário: Mesmos temas aparecem em idiomas diferentes.
Estratégia: Calibrar por idioma e testar mistura de termos técnicos; preservar identificadores literais independentemente do embedding.
Papel do modelo pequeno: 8–14B verifica coerência do segmento.
Aceite proposto: Cobertura deve permanecer estável entre idiomas avaliados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S013, V3A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Validador binário de fronteira candidata em poucos parágrafos.
8–14B: Revisor de continuidade temática e exceções entre segmentos.
15–30B: Integrador de segmentos heterogêneos, sem decidir fronteiras por intuição livre.
Requisitos de treino/runtime: Embedding versionado e conjunto de validação por domínio; trocar embedding exige recalibração.
Não aplicar quando: O custo de reindexação supera benefício ou documento exige separadores estruturais rígidos.

## T011:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Fronteiras por distância semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T011:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T011 → T072 [requires]
Como combinar: Publicar segmentação como versão do índice.
Interface: Documento, embedding, limiar e mapa de fronteiras.
Condição: Cada resultado apontar versão compatível.
Aceite proposto: Consultar durante atualização e detectar mistura de versões.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, V3A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T011 → T033 [complements]
Como combinar: Respeitar estruturas antes da distância semântica.
Interface: Blocos tipados e fronteiras permitidas.
Condição: Tabelas e código manterem integridade.
Aceite proposto: Injetar tabela semanticamente heterogênea e impedir corte destrutivo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S013, V3A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar limiar entre modelos sem validação.
- Medir mudança de fronteira causada por ruído de OCR.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar retorno útil por token e estabilidade de atualização; coerência textual não prova utilidade na resposta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T010, T012, T034

## Fontes primárias associadas

### A-S041 — Semantic splitter

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de parsers semânticos e janelas de sentenças.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S013 — Is Semantic Chunking Worth the Computational Cost?

[https://arxiv.org/abs/2410.13070](https://arxiv.org/abs/2410.13070)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de segmentação semântica e tamanho fixo em recuperação de documentos, evidência e respostas; ganhos não universais.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T012 — Recursive Chunking

**Nome canônico:** Recursive Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T012  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação recursiva

## T012:C01 — conceito

Aplica uma sequência de separadores, começando por unidades amplas e refinando apenas blocos grandes demais. Uma estratégia comum tenta parágrafos, linhas, espaços e, por último, caracteres. Recursivo descreve a divisão, não raciocínio recursivo do agente.

Como funciona:
- Tentar o separador de maior unidade disponível.
- Dividir novamente somente os blocos que ultrapassam o limite.
- Combinar fragmentos compatíveis e registrar sobreposições e offsets.

## T012:C02 — aplicacao

Quando usar:
- Textos gerais com parágrafos e linhas razoavelmente estruturados.
- Baseline de ingestão que exige simplicidade e previsibilidade.

Quando não usar:
- Não esperar reconhecimento completo de tabelas, AST de código ou relações entre documentos.

Implementação proposta:
- Proposta: adaptar separadores ao idioma e tipo de arquivo.
- Medir tamanho com tokenizer quando o limite relevante é em tokens.
- Preservar títulos como metadados e versionar a lista de separadores.

Aplicação LAI proposta:
Proposta LAI: adotar como divisão textual padrão inicial; encaminhar schemas e arquivos de código a parsers conscientes da estrutura.

## T012:C03 — riscos_validacao

Armadilhas:
- Medir caracteres enquanto o embedder limita tokens pode causar truncamento.
- Separadores mal escolhidos geram muitos fragmentos minúsculos.

Métricas sugeridas:
- Quantidade de trechos vazios ou acima do limite.
- Recall de evidência e tamanho médio efetivo.

Testes propostos:
- Usar textos com poucas quebras e garantir término e cobertura completa.
- Testar pontuação portuguesa e listas com quebras de linha para detectar fragmentação.

## T012:C04 — perguntas_proveniencia

Pergunta: Recursivo é igual a hierárquico?
Resposta: Não necessariamente. Um splitter recursivo pode produzir somente uma lista plana de trechos.

Pergunta: A ordem dos separadores importa?
Resposta: Sim. Ela define quais unidades o algoritmo tenta preservar antes de usar cortes mais finos.

Pergunta: A sobreposição configurada sempre aparece exatamente?
Resposta: Não se deve presumir. A preservação de unidades e a estratégia de junção podem alterar a sobreposição efetiva; inspecione offsets resultantes.

Pergunta: Quando usar parser em vez de separadores?
Resposta: Quando a semântica estrutural importa, como funções e tabelas. Um parser fornece relações que uma lista de caracteres não reconhece.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T012:C05 — mecanismo_avancado

A ordem dos separadores funciona como uma prioridade estrutural. Um bloco só desce para uma regra mais fina quando permanece grande demais. A configuração padrão de um divisor por caracteres não impõe automaticamente limite em tokens; trocar apenas o nome do parâmetro não muda a função de comprimento. Para línguas sem espaços, a lista de separadores deve considerar sua pontuação e convenções.

Condição de contorno:
Arquivos minificados, tabelas densas e unidades sem separadores reconhecidos podem chegar ao fallback mais fino e perder fronteiras úteis.

Contrato proposto:
- Entradas: Texto, separadores ordenados, função de comprimento e sobreposição alvo.
- Saídas: Segmentos com offsets e unidade de tamanho declarada.
- Estado: Versão da configuração, normalização aplicada e metadados de documento.
- Invariante: Cada fallback reduz uma unidade excessiva ou encerra com erro explícito, sem recursão improdutiva.

Compromissos de projeto:
- Regras simples tornam a ingestão reproduzível, mas não identificam relações semânticas implícitas.
- Mais separadores específicos preservam estrutura e também exigem testes por tipo de documento.

## T012:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: processar texto sem espaços e um bloco de código muito longo. Confirmar término, respeito ao limite medido e registro de cortes que atravessam uma unidade sintática.

Plano de avaliação proposto:
Avaliação proposta: comparar separadores genéricos e específicos por linguagem mantendo função de comprimento e índice iguais. Medir unidades quebradas, quantidade de chunks, custo e recuperação de evidências; escolher configuração por corpus, não por preferência nominal.

Comparações:
- T010 (complements): O limite de tamanho continua útil como restrição, embora os cortes tentem preservar unidades maiores.
- T033 (distinct_from): Recursão por delimitadores não equivale a interpretar uma árvore estrutural do documento.

Afirmação rastreável:
A documentação do RecursiveCharacterTextSplitter separa lista de separadores, função de comprimento e sobreposição.
Suporte: direct; fontes: A-S004
Limite: A configuração consultada é de uma biblioteca específica; outros divisores podem ter contratos diferentes.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T012:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu separadores e contagem. A novidade é preservar âncoras estáveis e limitar propagação de mudanças no particionamento recursivo.

Projeto e decomposição
Associe fragmentos a caminhos estruturais antes de aplicar separadores. Tamanho ainda governa fallback, mas o caminho permite localizar continuidade após inserções.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

Controle adaptativo
Registre qual nível de separador produziu cada fronteira. Muitos cortes no último nível indicam conteúdo incompatível ou parser ausente, não apenas chunk pequeno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

Validação contrafactual
Avalie reindexação após inserções no início e no meio do arquivo. Meça referências preservadas e necessidade real de recomputar embeddings. Unidade de avaliação: arquivo versionado. Teste inserção de uma seção antes de todas as demais e alteração interna num bloco protegido. Referências por caminho e revisão devem continuar localizando conteúdo sem depender do número ordinal do chunk. Se o bloco ficar grande demais, a saída precisa indicar oversize e oferecer estratégia de leitura; cortar silenciosamente não é fallback aceitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

USO AVANÇADO — Manuais em Markdown
Cenário: Seções mudam sem reorganização total.
Estratégia: Dividir por cabeçalhos, depois parágrafos e sentenças; conservar caminho da seção e número da revisão.
Papel do modelo pequeno: 3–7B extrai campos dentro do fragmento.
Aceite proposto: Citações devem resolver seção correta após edição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

USO AVANÇADO — Arquivos mistos
Cenário: Texto contém comandos longos e exemplos.
Estratégia: Reconhecer blocos protegidos e encaminhar oversize para leitura específica em vez de quebrar comando arbitrariamente.
Papel do modelo pequeno: 8–14B explica bloco protegido.
Aceite proposto: Nenhum exemplo executável pode ser alterado pelo splitter.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de unidades finais pequenas com contexto de cabeçalho.
8–14B: Comparador de fragmentos que compartilham uma seção.
15–30B: Síntese entre seções, pedindo bloco completo quando necessário.
Requisitos de treino/runtime: Separadores versionados, metadados de caminho e tratamento explícito de oversize.
Não aplicar quando: A estrutura depende de layout visual que os separadores textuais perderam.

## T012:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T012:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T012 → T015 [feeds]
Como combinar: Emitir referência independente do índice ordinal.
Interface: Caminho, revisão, offsets e digest.
Condição: Âncora representar conteúdo identificável.
Aceite proposto: Inserir parágrafo e verificar referências preservadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S004, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T012 → T033 [requires]
Como combinar: Detectar unidades protegidas antes do fallback.
Interface: Tipo de bloco e limites permitidos.
Condição: Parser reconhecer estrutura relevante.
Aceite proposto: Testar bloco longo sem corte em ponto inválido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S004, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar IDs baseados somente na posição na lista.
- Não ocultar trecho excessivo descartando o restante.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar localização e leitura após edições; a profundidade da recursão não mede qualidade semântica.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T010, T011, T033

## Fontes primárias associadas

### A-S004 — Splitting recursively

[https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores ordenados, limite de tamanho e sobreposição na divisão recursiva de texto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S013 — Is Semantic Chunking Worth the Computational Cost?

[https://arxiv.org/abs/2410.13070](https://arxiv.org/abs/2410.13070)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de segmentação semântica e tamanho fixo em recuperação de documentos, evidência e respostas; ganhos não universais.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T013 — Long-Context Models

**Nome canônico:** Long-Context Models  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T013  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** modelos de contexto longo

## T013:C01 — conceito

Modelos capazes de receber sequências longas dentro de limites declarados por arquitetura, treinamento e implantação. Capacidade nominal não prova utilização eficaz de cada trecho. O limite aceito pelo servidor, a reserva de saída e o comportamento em tarefas reais precisam ser medidos separadamente.

Como funciona:
- A implantação define comprimento e orçamento efetivamente disponíveis.
- A entrada longa mantém muitos dados simultaneamente acessíveis à atenção.
- A qualidade depende de posição, ruído, dependências e tipo de pergunta.

## T013:C02 — aplicacao

Quando usar:
- Comparação entre trechos distantes que são difíceis de recuperar isoladamente.
- Análise de um conjunto documental moderado com forte interdependência.

Quando não usar:
- Evitar enviar todo o acervo em cada chamada quando busca seletiva atende ao objetivo com menor custo.

Implementação proposta:
- Proposta: confirmar limite no checkpoint e na configuração de serviço.
- Reservar espaço para geração e retornos de ferramentas.
- Avaliar perguntas multissalto, contradições e fatos em diferentes posições, além de testes de agulha simples.

Aplicação LAI proposta:
Proposta LAI: tratar janela maior como recurso complementar; não eliminar memória externa, evidências ou orçamento de contexto da Helena.

## T013:C03 — riscos_validacao

Armadilhas:
- Um teste de recuperar uma palavra não mede síntese complexa.
- Contexto extenso pode aumentar memória, latência e custo mesmo com cache.

Métricas sugeridas:
- Acurácia por comprimento e posição da evidência.
- Tempo de prefill, consumo de memória e conclusão correta por missão.

Testes propostos:
- Mover a mesma evidência entre início, meio e fim mantendo a pergunta.
- Aumentar distratores e verificar se o modelo sabe declarar insuficiência.

## T013:C04 — perguntas_proveniencia

Pergunta: Janela maior significa mais inteligência?
Resposta: Não. Ela aumenta a quantidade admissível de entrada, sem garantir compreensão ou planejamento melhores.

Pergunta: O limite da ficha é sempre o do meu servidor?
Resposta: Não. Configuração, memória disponível, backend e reservas podem limitar a janela efetiva.

Pergunta: Um bom teste de agulha basta para escolher o modelo?
Resposta: Não. Ele demonstra uma habilidade restrita; a tarefa real pode exigir combinar premissas e distinguir versões contraditórias.

Pergunta: É sempre melhor usar a janela máxima?
Resposta: Não. O ponto adequado depende de utilidade marginal da informação, custo, prazo e qualidade observada para a operação desejada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T013:C05 — mecanismo_avancado

Capacidade útil precisa ser medida para a operação exigida: localizar um fato, reunir vários, aplicar uma exceção ou acompanhar uma cadeia de dependências. O mesmo comprimento pode funcionar para recuperação literal e falhar em agregação. A avaliação também deve variar posição e quantidade de distratores sem confundir tokens aceitos pela API com informação efetivamente usada na resposta.

Condição de contorno:
O tamanho anunciado não assegura qualidade quando a tarefa muda, a informação fica distribuída ou a reserva de saída e os custos tornam a chamada impraticável.

Contrato proposto:
- Entradas: Entrada tokenizada, tarefa definida, limite documentado e orçamento de saída.
- Saídas: Resposta com evidência e medidas de uso e duração.
- Estado: Modelo e configuração fixados, comprimento e posição dos fatos controlados.
- Invariante: Uma chamada aceita não é contada automaticamente como compreensão bem-sucedida do contexto.

Compromissos de projeto:
- Enviar tudo evita uma etapa de seleção, mas aumenta custo e exposição a ruído.
- Recuperação reduz entrada, porém pode omitir dependências; a escolha depende da tarefa e da cobertura exigida.

## T013:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter a resposta esperada constante e mover suas premissas para diferentes regiões da entrada, acrescentando distratores plausíveis. O sistema deve manter desempenho ou declarar a limitação observada.

Plano de avaliação proposto:
Avaliação proposta: comparar contexto integral e RAG com as mesmas fontes. Variar comprimento, posição, número de fatos e exigência de integração; medir exatidão, suporte, custo e latência por classe de tarefa, sem usar uma única nota agregada.

Comparações:
- T009 (alternative): RAG seleciona evidência antes da leitura; contexto longo permite mais conteúdo, mas ainda precisa utilizá-lo.
- R016 (complements): Lost in the Middle fornece uma dimensão de teste relacionada à posição da evidência.

Afirmação rastreável:
RULER inclui rastreamento e agregação além de recuperação literal para examinar capacidade de contexto.
Suporte: direct; fontes: V3A-S015
Limite: Foram consultadas capacidades e conclusões gerais; nenhum gabarito ou pergunta do benchmark orientou esta entrada.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T013:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu janela nominal e efetiva. Aqui a proposta compara alocação local de contexto com delegação sob limites reais de memória e latência.

Projeto e decomposição
Divida o custo em prefill, geração e armazenamento de estados. Um modelo 30B com contexto enorme pode perder viabilidade mesmo quando seus pesos cabem quantizados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S015, A-S019, V4A-S021.

Controle adaptativo
Escolha entre leitura integral e pacotes seletivos pelo tipo de dependência. Comparação global pode exigir visão ampla; extração de poucos campos favorece recortes verificáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S015, A-S019, V4A-S021.

Validação contrafactual
Varie comprimento com evidência constante e distrações controladas. Avalie falhas por posição, dependência e orçamento, sem aproveitar perguntas de benchmark público. Unidade de avaliação: tarefa longa. Faça comparação com carga concorrente, pois contexto longo pode reduzir quantidade de sessões viáveis. Registre memória de pico e latência de prefill para cada comprimento, junto do acerto em evidências distantes. Um modelo que vence isoladamente e viola prazo sob concorrência pode ser inadequado ao serviço, sem que isso invalide sua capacidade na tarefa individual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S015, A-S019, V4A-S021.

USO AVANÇADO — Revisão cruzada de especificações
Cenário: Contradições surgem em seções distantes.
Estratégia: Carregar mapa global, identificar pares candidatos e abrir conteúdo completo dos pares antes de concluir.
Papel do modelo pequeno: 15–30B integra pares; 3–7B localiza termos.
Aceite proposto: Toda contradição precisa de duas evidências compatíveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S015, A-S019, V4A-S021.

USO AVANÇADO — Leitura de corpus homogêneo
Cenário: Muitas perguntas repetem o mesmo material.
Estratégia: Comparar contexto integral cacheado com recuperação seletiva, incluindo amortização do prefixo e custo de cada resposta.
Papel do modelo pequeno: 8–14B responde consultas bem delimitadas.
Aceite proposto: Aceitar opção com qualidade mínima e custo total menor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S015, A-S019, V4A-S021.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Localizador de evidência em fatias pequenas; evitar depender da janela máxima anunciada.
8–14B: Leitor de pacote moderado com teste explícito de posição e ruído.
15–30B: Leitor global quando hardware, qualidade e benefício justificarem contexto extenso.
Requisitos de treino/runtime: Medição no servidor e tokenizer reais; contabilizar KV e concorrência além dos pesos.
Não aplicar quando: A memória ou latência de contexto extenso inviabiliza o serviço, mesmo sem erro de limite.

## T013:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q018.

## T013:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T013 → T009 [alternative]
Como combinar: Usar recuperação quando poucas regiões bastarem.
Interface: Consulta, referências e orçamento de leitura.
Condição: Corpus indexável e evidência localizável.
Aceite proposto: Comparar qualidade com leitura integral no mesmo conjunto.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S015, A-S019, V4A-S021. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T013 → T152 [requires]
Como combinar: Reservar recursos para contexto e saída.
Interface: Tokens, duração prevista e memória por sessão.
Condição: Estimativa validada no hardware alvo.
Aceite proposto: Medir picos com múltiplas sessões concorrentes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S015, A-S019, V4A-S021. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir 30B-A3B com modelo de apenas 3B residentes.
- Não transferir capacidade de uma família a outra pelo mesmo tamanho.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar dependências longas específicas; janela extensa não implica raciocínio de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T009, T042, T062

## Fontes primárias associadas

### A-S019 — Lost in the Middle: How Language Models Use Long Contexts

[https://arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Avaliação de efeitos da posição da evidência em perguntas e recuperação de pares chave-valor.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S015 — RULER: What's the Real Context Size of Your Long-Context Language Models?

[https://arxiv.org/abs/2404.06654](https://arxiv.org/abs/2404.06654)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Capacidade de contexto medida em tarefas distintas, incluindo rastreamento e agregação, além de recuperação literal.

Limite: Foram consultados resumo e descrição geral das capacidades, sem perguntas ou gabaritos. Resultados de modelos históricos não qualificam modelos atuais automaticamente.

### V4A-S021 — Welcome to Qwen — Qwen3 documentation

[https://qwen.readthedocs.io/en/v3.0/](https://qwen.readthedocs.io/en/v3.0/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Família com modelos densos 4B, 8B, 14B e MoE 30B-A3B; tamanhos não implicam equivalência de capacidade.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T014 — Progressive Disclosure

**Nome canônico:** Progressive Disclosure  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T014  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** divulgação progressiva; carregamento por camadas

## T014:C01 — conceito

Expõe informação em camadas conforme a necessidade: primeiro um catálogo enxuto, depois instruções e finalmente fontes completas. O recurso permanece acessível, mas somente a parte necessária entra na chamada. É um padrão de interface e contexto, não um mecanismo de memória paramétrica.

Como funciona:
- Publicar metadados que permitam descobrir a capacidade ou documento.
- Carregar instruções essenciais após a seleção.
- Abrir exemplos, arquivos e fontes detalhadas apenas quando a tarefa exigir.

## T014:C02 — aplicacao

Quando usar:
- Catálogos grandes de ferramentas, skills e documentação.
- Agentes com muitas capacidades especializadas usadas raramente.

Quando não usar:
- Não ocultar restrições obrigatórias nem dados cuja ausência impede perceber que uma busca é necessária.

Implementação proposta:
- Proposta: criar índice por objetivo, entradas e saídas de cada recurso.
- Preservar referências estáveis e indicar quando há conteúdo adicional.
- Medir descoberta com solicitações sem o nome exato da ferramenta e manter fallback de pesquisa.

Aplicação LAI proposta:
Proposta LAI: manter no contexto da Helena um catálogo compacto de capacidades e carregar contratos completos antes de qualquer execução dependente deles.

## T014:C03 — riscos_validacao

Armadilhas:
- Descrições vagas tornam recursos invisíveis.
- O agente pode confundir o resumo do recurso com sua instrução completa.

Métricas sugeridas:
- Taxa de descoberta da capacidade correta.
- Tokens carregados até resolver a tarefa, incluindo buscas adicionais.

Testes propostos:
- Pedir uma tarefa por paráfrase e conferir seleção correta da skill.
- Remover o documento detalhado e exigir aviso de leitura incompleta.

## T014:C04 — perguntas_proveniencia

Pergunta: Preciso colocar as 218 entradas no prompt inicial?
Resposta: Não. Um índice de descoberta pode selecionar as entradas pertinentes e seus trechos.

Pergunta: Progressive disclosure reduz conhecimento disponível?
Resposta: Reduz informação imediatamente carregada; o acervo continua acessível por recuperação.

Pergunta: Posso resumir todas as regras no catálogo?
Resposta: Pode aumentar custo e ambiguidade. Inclua condições discriminativas e mantenha a instrução completa acessível, identificando o resumo como resumo.

Pergunta: Carregar uma skill concede autorização para executar tudo nela?
Resposta: Não. Descoberta e leitura disponibilizam instruções; autorização continua vinculada à tarefa e aos controles do ambiente, sem expansão automática de escopo.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T014:C05 — mecanismo_avancado

O catálogo inicial funciona como um mecanismo de roteamento: se a descrição não expõe a condição de uso de um recurso, o agente pode nunca abrir o conteúdo que resolveria a tarefa. Assim, economizar tokens na primeira camada exige preservar informação discriminativa. A versão dos metadados também deve corresponder à versão das instruções e recursos carregados depois.

Condição de contorno:
O padrão falha quando detalhes essenciais à escolha ficam escondidos atrás de uma decisão que depende justamente desses detalhes.

Contrato proposto:
- Entradas: Catálogo resumido, objetivo atual e resolvedor das camadas seguintes.
- Saídas: Conjunto de recursos expandidos com justificativa e versão.
- Estado: Recursos já lidos, dependências e orçamento disponível para expansão.
- Invariante: Metadados orientam descoberta, mas não são tratados como conteúdo completo ou evidência de execução.

Compromissos de projeto:
- Descrições compactas reduzem custo inicial, porém podem aumentar falsos negativos de descoberta.
- Mais camadas preservam seletividade, mas acrescentam latência e risco de referências quebradas.

## T014:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar dois recursos com nomes semelhantes e condições de uso diferentes. Verificar se os metadados permitem selecionar o correto antes de ler instruções extensas.

Plano de avaliação proposto:
Avaliação proposta: comparar carregamento integral e progressivo com o mesmo acervo. Medir recursos necessários descobertos, leituras inúteis, tokens totais e tarefas abandonadas por descoberta insuficiente; revisar descrições que causam erros recorrentes.

Comparações:
- T015 (complements): Referências tornam possível adiar a transferência do conteúdo completo.
- T044 (complements): Expansão progressiva é a política que decide quando abrir a próxima camada.

Afirmação rastreável:
A especificação Agent Skills distingue carregamento de metadados, instruções e recursos sob demanda.
Suporte: direct; fontes: V3A-S018
Limite: O formato orienta organização; comportamento efetivo depende de como o executor implementa a descoberta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T014:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou descoberta por metadados. Aqui a camada nova é projetar descrições discriminativas e medir custo de escolhas erradas.

Projeto e decomposição
Descrições devem distinguir vizinhos, não resumir tudo igualmente. Inclua finalidade, exclusões e exemplo de decisão entre recursos parecidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

Controle adaptativo
Faça carregamento em duas etapas: contrato mínimo para escolher e corpo necessário para agir. Se o contrato não desambiguar, ampliar metadados antes do conteúdo inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

Validação contrafactual
Compare catálogo integral e descoberta progressiva usando recursos raros. Medir seleção incorreta, cargas extras e conclusão, não somente tokens iniciais. Unidade de avaliação: catálogo de recursos. Monte um catálogo com dois recursos quase sinônimos, um frequente e outro raro, cuja diferença está numa pré-condição. O teste deve mostrar se o descritor permite escolher o raro sem abrir tudo. Depois remova a pré-condição da descrição e confirme degradação; essa ablação mede a utilidade real dos metadados de descoberta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

USO AVANÇADO — Biblioteca de procedimentos
Cenário: Centenas de rotinas compartilham termos.
Estratégia: Criar índice por intenção e pré-condições; testar pares confundíveis e revisar descrições que causam carga errada.
Papel do modelo pequeno: 3–7B escolhe entre candidatos curtos.
Aceite proposto: Procedimento selecionado deve satisfazer todas as pré-condições.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

USO AVANÇADO — Projeto com muitos módulos
Cenário: Agente precisa localizar documentação apropriada.
Estratégia: Expor mapa de responsabilidades e abrir módulo pelo problema observado; expandir vizinhos apenas se interface cruzar fronteira.
Papel do modelo pequeno: 8–14B resolve dependências locais.
Aceite proposto: Toda expansão deve responder a lacuna identificada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Roteador entre poucos descritores contrastivos.
8–14B: Planejador de carga em duas etapas com identificação de dependências.
15–30B: Integrador de recursos especializados, mantendo teto de expansão.
Requisitos de treino/runtime: Catálogo curado e versionado; exemplos negativos são mais úteis que descrições promocionais.
Não aplicar quando: Metadados não permitem descobrir o recurso correto com custo menor que leitura direta.

## T014:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T014:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T014 → T045 [complements]
Como combinar: Aplicar descritores contrastivos às ferramentas.
Interface: Intenção, restrições e tool_id.
Condição: Schema completo carregado antes da chamada.
Aceite proposto: Confundir ferramentas semelhantes deve gerar correção antes de executar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T014 → T044 [feeds]
Como combinar: Abrir detalhe somente após identificar lacuna.
Interface: resource_id, motivo e limite de expansão.
Condição: A carga acrescentar informação necessária.
Aceite proposto: Medir utilidade marginal de cada abertura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Detectar ciclos de referências.
- Não conceder autoridade às instruções encontradas no conteúdo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar descoberta de recursos raros; economia inicial que aumenta erros de seleção não é melhoria.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T044, T045, T151

## Fontes primárias associadas

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T015 — Reference Passing

**Nome canônico:** Reference Passing  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T015  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** passagem por referência; artifact references

## T015:C01 — conceito

Passa identificadores recuperáveis de artefatos entre etapas ou agentes em vez de transmitir todo o conteúdo. A referência só é útil se um resolvedor puder abrir a versão correta com acesso autorizado. Um ponteiro curto não contém implicitamente o conhecimento do arquivo.

Como funciona:
- Persistir um artefato com ID, versão e metadados.
- Transmitir referência mais descrição mínima do conteúdo.
- Resolver a referência e carregar a parte necessária no ponto de uso.

Nota de nomenclatura: Padrão de engenharia aplicado a agentes; não identifica um método científico exclusivo.

## T015:C02 — aplicacao

Quando usar:
- Resultados grandes de ferramentas ou subagentes.
- Missões com muitos arquivos e evidências reutilizadas.

Quando não usar:
- Não serve quando o consumidor não tem acesso ao mesmo armazenamento ou precisa agir sem ler o conteúdo.

Implementação proposta:
- Proposta: adotar IDs opacos e resolver no serviço, sem concatenar caminhos recebidos.
- Incluir hash, tamanho e tipo para validar a leitura.
- Retornar estado explícito para referência inexistente, versão antiga ou conteúdo parcial.

Aplicação LAI proposta:
Proposta LAI: transportar referências de logs, contratos e relatórios entre especialistas; o executor lê a evidência necessária antes de aplicar uma decisão.

## T015:C03 — riscos_validacao

Armadilhas:
- O produtor pode transmitir referência antes de concluir a escrita.
- Um alias mutável pode resolver para conteúdo diferente daquele usado na decisão original.

Métricas sugeridas:
- Referências resolvidas corretamente por versão.
- Bytes ou tokens transferidos por etapa e falhas de acesso.

Testes propostos:
- Alterar o objeto após criar a referência e exigir detecção de versão divergente.
- Tentar uma referência de namespace diferente e rejeitar acesso indevido.

## T015:C04 — perguntas_proveniencia

Pergunta: O modelo conhece o arquivo ao receber seu caminho?
Resposta: Não. Ele precisa de conteúdo recuperado ou de uma ferramenta que o leia.

Pergunta: Devo usar apenas o nome do arquivo?
Resposta: Prefira ID e versão; nomes podem colidir, mudar ou apontar para conteúdo diferente.

Pergunta: Uma URL prova que o conteúdo foi lido?
Resposta: Não. Ela prova apenas que uma localização foi fornecida. O relato deve distinguir referência recebida, leitura bem-sucedida e conteúdo efetivamente utilizado.

Pergunta: Como evitar referências que perdem validade?
Resposta: Defina retenção e versões recuperáveis compatíveis com a tarefa; registre falhas e preserve uma representação autorizada quando o contrato exigir continuidade.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T015:C05 — mecanismo_avancado

Uma referência precisa distinguir identidade lógica de identidade de versão. Um caminho que aponta para a versão mais recente pode resolver conteúdo diferente entre planejamento e execução. Para continuidade verificável, transfira também revisão, tipo e descrição do que o destinatário deve ler. O custo evitado no envio pode reaparecer como latência de resolução ou indisponibilidade do recurso.

Condição de contorno:
Passar apenas um identificador é insuficiente quando o próximo agente não possui resolvedor, acesso ou capacidade para interpretar o artefato referenciado.

Contrato proposto:
- Entradas: Referência, versão esperada, finalidade e escopo da leitura.
- Saídas: Conteúdo autorizado ou erro classificado de ausência, versão ou acesso.
- Estado: Mapeamento de identificadores, revisões e leituras realizadas.
- Invariante: O destinatário não afirma conhecer o conteúdo antes de resolvê-lo ou receber evidência explícita suficiente.

Compromissos de projeto:
- Referências diminuem duplicação de conteúdo, mas introduzem dependência de disponibilidade.
- Versões fixadas favorecem reprodução, enquanto referências móveis facilitam atualização e exigem revalidação.

## T015:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar um arquivo entre a emissão e a resolução da referência. Um consumidor que exigiu a versão antiga deve receber essa versão ou erro claro, nunca substituição silenciosa.

Plano de avaliação proposto:
Avaliação proposta: comparar conteúdo embutido e referência resolvida sob diferentes tamanhos e taxas de reutilização. Medir tokens, tempo total, referências quebradas e divergências de versão; escolher por custo completo da troca.

Comparações:
- T066 (complements): O resolvedor aplica o contrato de leitura e versão usado na passagem.
- T061 (complements): Um hash de conteúdo pode identificar uma versão, mantendo localização e acesso como problemas separados.

Afirmação rastreável:
MCP identifica recursos por URI e define operações distintas de listagem e leitura.
Suporte: direct; fontes: V3A-S019
Limite: A especificação não torna toda URI imutável nem fornece automaticamente o versionamento editorial proposto.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T015:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou referência e leitura. Aqui referências transportam prova de disponibilidade e uma política de resolução por tarefa.

Projeto e decomposição
Uma referência entregue a outro agente deve declarar conteúdo disponível, recorte permitido e custo de abertura. O receptor pode planejar sem fingir que já leu.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

Controle adaptativo
Use leases ou verificação equivalente para artefatos temporários. Se a validade expirar, renovar acesso ou materializar cópia identificada antes da etapa dependente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

Validação contrafactual
Compare transporte integral e referências em tarefas com reuso desigual. Medir leituras evitadas, referências quebradas e conclusões sem abertura. Unidade de avaliação: cadeia de referências. Inclua referência válida no momento da delegação e indisponível na retomada. O receptor deve produzir diagnóstico de indisponibilidade, não reconstruir conteúdo a partir do título ou de um resumo antigo. Compare materialização antecipada e leitura tardia segundo prazo e probabilidade de uso; referências economizam transporte, mas podem aumentar risco operacional quando a origem é temporária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

USO AVANÇADO — Delegação de análise
Cenário: Subagente produz relatório extenso.
Estratégia: Retornar índice de afirmações e referências a evidências; líder abre somente suportes que usará no texto final.
Papel do modelo pequeno: 3–7B produz índice; 15–30B integra.
Aceite proposto: Nenhuma citação final pode apontar conteúdo não verificado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

USO AVANÇADO — Resultados grandes de ferramenta
Cenário: Tabela excede a janela.
Estratégia: Persistir resultado, devolver schema e referência; consultas posteriores pedem colunas ou linhas necessárias.
Papel do modelo pequeno: 8–14B escolhe projeções pequenas.
Aceite proposto: Resposta deve preservar filtro e versão da tabela.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de identificadores e schemas, com resolução determinística.
8–14B: Seletor de recortes e projeções por pergunta.
15–30B: Integrador que compara fontes grandes por aberturas direcionadas.
Requisitos de treino/runtime: Resolver com identidade, versão e status de disponibilidade; validade de acesso deve ser verificável.
Não aplicar quando: A origem não ficará acessível até o fim da tarefa e não há cópia durável.

## T015:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C020 — Google / NotebookLM com fontes multimodais
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Produto oferece análise de documentos, áudio e vídeo com citações.
Mecanismo documentado: Conteúdo de fontes e transcrições fundamenta respostas referenciadas.
Correspondência com esta base: Citações retornam às fontes; formato de Reference Passing não é especificado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.
Limite: Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S025.

V4A-C016 — Google Cloud / Gemini context caching
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Manual disponibiliza caches implícitos e explícitos de contexto.
Mecanismo documentado: Reuso de prefixos, referências a objetos de cache e contabilidade de tokens.
Correspondência com esta base: Nome de recurso referencia conteúdo cacheado, não referência semântica genérica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Agrupar chamadas pequenas com prefixo estável quando runtime suportar e medir custo líquido.
Limite: Modelos e condições de serviço variam; caching não aumenta janela nem reduz obrigação de evidência. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019, V4A-Q022.

## T015:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T015 → T066 [requires]
Como combinar: Resolver identidade antes de interpretar o conteúdo.
Interface: URI lógica, revisão, hash e seletor.
Condição: Resolver não substituir versão silenciosamente.
Aceite proposto: Testar expiração e versão inexistente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V4A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T015 → T061 [complements]
Como combinar: Vincular artefato recuperado ao digest esperado.
Interface: Bytes, codec e digest.
Condição: Hash representar o artefato efetivamente lido.
Aceite proposto: Alterar objeto e impedir aceitação pelo identificador antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V4A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não resumir referência como se fosse evidência lida.
- Conservar limite de acesso quando a referência atravessar agentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo de transporte e qualidade das citações, não presumir que referência curta melhora entendimento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T053, T061, T066

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews

[https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto fundamentado em fontes com citações e transcrições; recursos disponíveis.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S015 — Context caching overview

[https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Caching implícito e explícito, metadados de uso e duração; recurso disponível.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T016 — Tool Result Truncation

**Nome canônico:** Tool Result Truncation  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T016  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** limitação de saída de ferramenta

## T016:C01 — conceito

Limita a quantidade de uma saída de ferramenta inserida no contexto. Deve preservar o resultado completo fora da chamada e indicar a truncagem. Uma amostra de log não autoriza concluir que o trecho omitido contém ou não contém determinado fato.

Como funciona:
- Receber a saída integral e guardar metadados de tamanho.
- Selecionar partes pertinentes dentro do orçamento.
- Retornar indicador de conteúdo parcial e forma de obter continuação.

## T016:C02 — aplicacao

Quando usar:
- Logs extensos, consultas com muitas linhas e arquivos volumosos.
- Inspeção inicial que será seguida por busca direcionada.

Quando não usar:
- Não truncar silenciosamente resultados usados para afirmar cobertura completa ou ausência de erro.

Implementação proposta:
- Proposta: exigir campos truncated, total_size e artifact_ref no contrato.
- Priorizar cabeçalho, erros e intervalos pedidos, evitando corte cego no final.
- Permitir leitura por offset ou filtro e distinguir zero resultados de saída omitida.

Aplicação LAI proposta:
Proposta LAI: resumir saídas extensas da auditoria com links para o original; manter contagem de registros para que a Helena saiba o que ainda não viu.

## T016:C03 — riscos_validacao

Armadilhas:
- O erro decisivo pode estar fora da amostra.
- Cortar JSON ou uma linha de tabela pode produzir interpretação incorreta.

Métricas sugeridas:
- Fração omitida e número de leituras adicionais.
- Taxa de decisões incorretas causadas por resultado parcial.

Testes propostos:
- Colocar falha no meio de um log grande e recuperá-la com busca.
- Testar uma saída cortada no meio de JSON e exigir formato estruturado válido ou conteúdo bruto marcado.

## T016:C04 — perguntas_proveniencia

Pergunta: Truncar é a mesma coisa que resumir?
Resposta: Não. Truncar remove partes; resumir reescreve conteúdo. Ambos podem perder informação de maneiras diferentes.

Pergunta: Posso declarar não há erros após ler os primeiros resultados?
Resposta: Só se a ferramenta verificou todo o conjunto e retornou esse resultado de forma explícita.

Pergunta: Truncar e resumir são equivalentes?
Resposta: Não. Truncar retém uma parte literal; resumir produz outra representação. Ambos podem perder informação, mas têm riscos e testes de fidelidade diferentes.

Pergunta: O marcador de truncamento deve ficar só no log?
Resposta: Não. Quem toma a decisão precisa conhecer a cobertura. O marcador deve acompanhar o trecho entregue ao consumidor.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T016:C05 — mecanismo_avancado

A política de truncamento precisa preservar sinais de estado independentes do corpo: código de saída, paginação, contagem quando disponível e existência de erro. Cortar apenas pelo começo pode remover o diagnóstico final; guardar começo e fim pode omitir o único erro intermediário. Portanto, uma saída parcial exige contrato de cobertura e caminho para leitura direcionada do restante.

Condição de contorno:
Se o consumidor precisa provar ausência de ocorrências no conjunto inteiro, uma amostra truncada não fornece evidência suficiente, por maior que pareça.

Contrato proposto:
- Entradas: Resultado completo, limite de apresentação e metadados confiáveis da ferramenta.
- Saídas: Trecho parcial identificado e referência recuperável ao original.
- Estado: Artefato completo, regiões exibidas e versão do seletor de trechos.
- Invariante: Conteúdo omitido nunca é descrito como examinado apenas porque a ferramenta terminou sem erro de transporte.

Compromissos de projeto:
- Limites rígidos protegem contexto, mas podem esconder o sinal mais importante.
- Seleção orientada por erros preserva diagnóstico e exige conhecer o formato, sem substituir o original.

## T016:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar uma ocorrência relevante somente no meio omitido de um log. O agente deve reconhecer cobertura parcial e recuperar essa região antes de concluir ausência de problema.

Plano de avaliação proposto:
Avaliação proposta: comparar prefixo, início e fim, e seleção estruturada com igual orçamento. Medir diagnósticos preservados, releituras, falsos relatos de ausência e custo total; manter o original disponível em todas as variantes.

Comparações:
- T214 (distinct_from): Pruning pode selecionar campos ou regiões por relevância; truncamento aplica um limite de apresentação.
- T215 (distinct_from): Masking substitui observações antigas por marcadores; truncamento também pode ocorrer no primeiro recebimento.

Afirmação rastreável:
MCP separa a referência de um recurso da operação que lê seu conteúdo.
Suporte: related; fontes: V3A-S019
Limite: Isso apoia externalização do original; o protocolo de truncamento descrito é uma proposta editorial.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T016:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu parcial, erro e vazio. Aqui a saída truncada é uma projeção orientada pela pergunta, com caminho mensurável de recuperação.

Projeto e decomposição
Escolha projeção por tipo de resultado: amostra estratificada para exploração, agregação para contagem e linhas exatas para diagnóstico. Cortar os primeiros caracteres raramente é contrato suficiente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Controle adaptativo
Preserve total de itens, filtros, ordenação e cursor. O modelo decide se a projeção responde à pergunta ou solicita leitura adicional com campos definidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Validação contrafactual
Compare prefixo simples e projeções orientadas à tarefa. Meça conclusões corretas sobre o conjunto e custo das leituras adicionais. Unidade de avaliação: resultado de ferramenta. Para validar projeções, use conjunto cuja exceção aparece no final e outro com distribuição desigual entre categorias. Prefixo simples deve falhar de modo observável; amostra estratificada pode localizar a exceção, mas ainda não prova sua frequência. Contagens e conclusões exaustivas precisam vir da consulta completa, com filtro e ordenação registrados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Busca com muitos resultados
Cenário: A pergunta pede exceções raras.
Estratégia: Calcular contagens em código, devolver grupos e abrir amostras das categorias suspeitas. Não inferir ausência pela amostra.
Papel do modelo pequeno: 3–7B classifica categorias.
Aceite proposto: Contagem final deve vir da consulta completa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Falha de compilação volumosa
Cenário: Logs contêm cascata de erros.
Estratégia: Retornar primeiros erros por arquivo e resumo de frequências; preservar log integral para buscar causa anterior.
Papel do modelo pequeno: 8–14B prioriza diagnóstico.
Aceite proposto: Patch deve ser validado contra execução posterior, não resumo do log.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de schema e contagens calculadas, sem estimar totais pela amostra.
8–14B: Investigador que pede intervalos adicionais com hipótese explícita.
15–30B: Correlacionador de múltiplos logs por identificadores de operação.
Requisitos de treino/runtime: Ferramenta de projeção determinística e armazenamento do resultado completo quando necessário.
Não aplicar quando: O corte remove a única evidência disponível ou a tarefa exige exaustividade sem cursor.

## T016:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T016:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T016 → T238 [complements]
Como combinar: Abrir intervalos do artefato integral.
Interface: artifact_id, versão, intervalo e total.
Condição: Leitura manter ordenação e revisão.
Aceite proposto: Reconstituir trecho omitido sem trocar a origem.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T016 → T042 [requires]
Como combinar: Limitar projeção pelo orçamento real.
Interface: Tokens estimados, reserva e esquema de resposta.
Condição: Medir após serializar metadados.
Aceite proposto: Testar resultado cujo cabeçalho sozinho excede a cota.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar amostra de resultado completo.
- Propagar erro da ferramenta sem convertê-lo em conjunto vazio.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar diagnóstico e decisões sobre conjuntos grandes; concisão isolada não basta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T043, T066

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T017 — Context Folding

**Nome canônico:** Context Folding  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T017  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** dobramento de contexto

## T017:C01 — conceito

Fecha trabalho intermediário em representações menores e retorna ao contexto principal. Há trabalhos específicos chamados Context-Folding; um deles usa subtrajetórias branch/return e treinamento FoldGRPO. No runtime, uma versão arquitetural pode preservar somente resultado, evidências e pendências de cada subatividade.

Como funciona:
- Abrir uma subtarefa com contexto focado e limite claro.
- Executar ações locais mantendo o histórico completo fora do contexto principal.
- Retornar síntese contratada e referências, removendo detalhes intermediários da chamada principal.

## T017:C02 — aplicacao

Quando usar:
- Pesquisa ou desenvolvimento com muitas subtarefas delimitáveis.
- Histórico de tentativa e erro que não precisa permanecer ativo após conclusão.

Quando não usar:
- Não dobrar uma subtarefa ainda aberta quando seus detalhes são necessários para resolver dependências.

Implementação proposta:
- Proposta: definir retorno com estado, resultado, evidência e dúvidas.
- Versionar o registro fechado para poder reabri-lo.
- Comparar orquestração simples com modelo treinado para folding sem presumir equivalência entre ambos.

Aplicação LAI proposta:
Proposta LAI: especialistas retornam achados compactos ao decisor; a proposta de runtime não implica que o Qwen já recebeu treinamento FoldGRPO.

## T017:C03 — riscos_validacao

Armadilhas:
- Uma síntese pode ocultar falha ou incerteza da subtarefa.
- Branches isolados podem tomar decisões incompatíveis.

Métricas sugeridas:
- Tamanho do contexto ativo e frequência de reabertura.
- Sucesso em tarefas longas incluindo conflitos entre subtarefas.

Testes propostos:
- Introduzir uma dependência cruzada e verificar se é reportada ao principal.
- Reabrir uma subtarefa após interrupção e recuperar evidências originais.

## T017:C04 — perguntas_proveniencia

Pergunta: Context folding é apenas resumir tudo?
Resposta: Não necessariamente. A divisão e retomada de subtrajetórias também organiza o controle da execução.

Pergunta: Posso reproduzir o paper só adicionando um prompt?
Resposta: Não. Um padrão parecido em software não reproduz automaticamente o treinamento e os resultados publicados.

Pergunta: Uma dobra precisa guardar raciocínio interno completo?
Resposta: Não. O contrato deve preservar estado operacional e evidências úteis, sem presumir acesso ou necessidade de registrar processos internos ocultos do modelo.

Pergunta: Como saber se a decomposição foi boa?
Resposta: Observe integração, reaberturas e dependências que atravessam retornos. Uma redução aparente de contexto pode esconder repetição de trabalho nas subtarefas.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T017:C05 — mecanismo_avancado

O retorno de uma subtrajetória precisa preservar aquilo que o contexto pai ainda deve usar: resultado, premissas, evidências e pendências. Fechar a trajetória não desfaz seus efeitos. Uma dobra útil distingue uma conclusão comprovada de uma tentativa interrompida, e mantém forma de reabrir artefatos quando o resumo não responde a uma dúvida posterior.

Condição de contorno:
O ganho diminui quando subtarefas compartilham dependências extensas ou quando o retorno omite detalhes necessários à integração, causando reabertura frequente.

Contrato proposto:
- Entradas: Objetivo da subtrajetória, contexto mínimo e contrato de retorno.
- Saídas: Resultado compacto com referências e estado de conclusão explícito.
- Estado: Pilha de tarefas, artefatos produzidos e efeitos confirmados ou incertos.
- Invariante: Dobrar contexto não muda o estado real de operações nem converte pendência em conclusão.

Compromissos de projeto:
- Contexto ativo menor reduz leitura repetida, mas transfere responsabilidade para o contrato de retorno.
- Subtrajetórias mais independentes são fáceis de dobrar; decomposição inadequada multiplica coordenação.

## T017:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: encerrar uma subtrajetória após enviar uma operação cuja resposta se perdeu. O retorno deve preservar a incerteza e impedir que o pai repita a operação como se nunca tivesse ocorrido.

Plano de avaliação proposto:
Avaliação proposta: comparar histórico integral, resumos periódicos e branch/return com mesmas tarefas e orçamento. Medir contexto ativo, custo agregado, reaberturas e integração correta; avaliar separadamente política treinada e orquestração manual.

Comparações:
- T237 (complements): Subagentes podem materializar subtarefas, mas folding não exige equivalência entre agente e trajetória.
- T043 (distinct_from): Compactação geral reduz histórico; folding usa fronteiras explícitas de subtarefa e retorno.

Afirmação rastreável:
O trabalho Context Folding combina branch/return com FoldGRPO para aprender gerenciamento de contexto.
Suporte: direct; fontes: V3A-S020
Limite: Aplicar uma dobra manual não reproduz o treinamento nem os resultados experimentais do trabalho.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T017:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu retorno do folding. Aqui a novidade é decidir quais subtarefas merecem contexto isolado e medir a suficiência do retorno.

Projeto e decomposição
Escolha folding quando exploração produz muito material descartável e poucos resultados estáveis. Dependências densas entre subtarefas podem tornar o custo de comunicar estado maior que a economia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

Controle adaptativo
Retorne resultado, evidências e perguntas ainda abertas em canais separados. O chamador pode pedir expansão pontual sem reiniciar toda a exploração nem aceitar conclusão sem base.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

Validação contrafactual
Compare execução monolítica e subcontextos com mesmo limite total de chamadas. Meça trabalho duplicado, suficiência do retorno e necessidade de reabrir exploração. Unidade de avaliação: subtarefa delegada. Inclua subtarefa cujo resultado é correto localmente, mas incompatível com uma restrição do chamador. O contrato deve carregar essa restrição desde a delegação e devolver conflito, não uma solução aparentemente completa. Medir retrabalho por retorno insuficiente ajuda a decidir quando isolamento de contexto compensa a comunicação adicional entre trabalhadores.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

USO AVANÇADO — Investigação de componente
Cenário: Um erro pode estar em três módulos.
Estratégia: Abrir subcontexto por hipótese, exigir evidência discriminante e retornar também hipóteses descartadas com motivo.
Papel do modelo pequeno: 3–7B localiza; 8–14B investiga módulo.
Aceite proposto: Líder deve distinguir ausência de evidência de hipótese refutada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

USO AVANÇADO — Pesquisa de alternativas
Cenário: Cada opção tem documentação extensa.
Estratégia: Delegar coleta em esquema comum e comparar somente atributos respaldados; reabrir opção quando critério novo surgir.
Papel do modelo pequeno: 15–30B integra comparações.
Aceite proposto: Nenhuma diferença deve resultar apenas de cobertura desigual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S020, C-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Subtarefa estreita de localização ou extração com retorno fechado.
8–14B: Investigador local capaz de pedir uma expansão adicional.
15–30B: Coordenador de retornos heterogêneos e lacunas entre hipóteses.
Requisitos de treino/runtime: Contrato de retorno, referências duráveis e orçamento por subcontexto; folding aprendido exige treino próprio.
Não aplicar quando: Todos os trabalhadores precisam continuamente do mesmo estado mutável.

## T017:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T017:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T017 → T169 [complements]
Como combinar: Isolar exploração por hipótese e devolver contrato comum.
Interface: Objetivo, limites, resultado e evidências.
Condição: Não houver escrita concorrente irrestrita.
Aceite proposto: Medir duplicação e efeitos de informação omitida.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S020, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T017 → T015 [feeds]
Como combinar: Retornar referências para detalhes reabríveis.
Interface: Resultado, artifact_id e seletores.
Condição: Artefato sobreviver ao encerramento do subcontexto.
Aceite proposto: Reabrir suporte após encerrar o trabalhador.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S020, C-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir isolamento de contexto com isolamento de efeitos.
- Conservar incertezas no retorno condensado.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas decomponíveis; dobrar agentes não garante compensar um leitor insuficiente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T004, T043, T169

## Fontes primárias associadas

### A-S037 — Scaling Long-Horizon LLM Agent via Context-Folding

[https://context-folding.github.io/](https://context-folding.github.io/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Subtrajetórias branch/return e treinamento FoldGRPO para gestão do contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S020 — Scaling Long-Horizon Agent via Context Folding

[https://proceedings.mlr.press/v306/sun26x.html](https://proceedings.mlr.press/v306/sun26x.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Branch de subtrajetória, retorno resumido e treinamento FoldGRPO; não equivalente a simples resumo externo.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T018 — Context Pruning

**Nome canônico:** Context Pruning  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T018  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda de contexto

## T018:C01 — conceito

Remove unidades de contexto consideradas dispensáveis antes da inferência. Pode usar regras, relevância, dependências ou modelos. Diferentemente de uma síntese abstrativa, a poda extrativa mantém o texto dos trechos escolhidos; ainda assim pode eliminar premissas essenciais.

Como funciona:
- Separar contexto em unidades com origem identificada.
- Atribuir elegibilidade e prioridade sem remover campos obrigatórios.
- Selecionar unidades dentro do orçamento e registrar descartes.

## T018:C02 — aplicacao

Quando usar:
- Documentos recuperados com muito ruído.
- Histórico que contém saídas repetidas ou superadas.

Quando não usar:
- Não usar apenas similaridade lexical quando a resposta depende de exceções ou condições indiretas.

Implementação proposta:
- Proposta: proteger negações, números, restrições e pares de chamada/resultado.
- Combinar relevância à pergunta com fechamento de dependências.
- Manter índice do que foi removido para permitir recuperação posterior.

Aplicação LAI proposta:
Proposta LAI: começar removendo duplicatas e logs já resolvidos; decisões atuais e evidências de autorização devem obedecer regras determinísticas de preservação.

## T018:C03 — riscos_validacao

Armadilhas:
- Uma premissa útil pode parecer pouco semelhante à pergunta.
- Remover trechos intermediários pode alterar a leitura de uma sequência causal ou temporal.

Métricas sugeridas:
- Tokens removidos e cobertura de evidência crítica.
- Qualidade final em comparação com contexto integral.

Testes propostos:
- Plantar uma exceção relevante em um parágrafo de baixa similaridade.
- Comparar explicação e resposta antes e depois da poda em casos negativos.

## T018:C04 — perguntas_proveniencia

Pergunta: Poda extrativa é sempre fiel?
Resposta: O texto preservado é original, mas a combinação de trechos pode omitir qualificações e induzir erro.

Pergunta: Posso podar depois do resultado da busca?
Resposta: Sim. Esse é um ponto comum, desde que o processo retenha evidências suficientes para a pergunta.

Pergunta: Uma frase irrelevante à pergunta pode ser necessária?
Resposta: Sim. Ela pode definir quem é o sujeito, qual unidade está em uso ou quando a regra vale. Relevância direta e suporte são funções distintas.

Pergunta: Como auditar o seletor?
Resposta: Guarde a máscara de seleção e os offsets. Assim é possível localizar exatamente o que foi removido e investigar uma resposta incorreta.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T018:C05 — mecanismo_avancado

A seleção independente de frases pode conservar uma conclusão e remover a condição que a limita. Uma poda orientada por dependências trata definição, unidade, negação e referente como parte da evidência necessária. O orçamento deve ser aplicado depois desse fechamento: escolher os trechos mais pontuados e descobrir tarde que suas dependências não cabem produz contexto incoerente.

Condição de contorno:
O critério de relevância deixa de ser suficiente quando as unidades selecionadas dependem de elementos com baixa pontuação isolada.

Contrato proposto:
- Entradas: Blocos identificados, orçamento e critérios de relevância e dependência.
- Saídas: Subconjunto literal acompanhado dos trechos de suporte necessários.
- Estado: Mapa de seleção, pontuações e localização do conteúdo retirado.
- Invariante: A poda não transforma uma afirmação condicional em regra incondicional por remoção silenciosa.

Compromissos de projeto:
- Poda por bloco mantém mais contexto e reduz economia em relação a tokens isolados.
- Critérios aprendidos capturam padrões, mas podem falhar em exceções raras e fora de domínio.

## T018:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atribuir alta relevância a um resultado e baixa relevância à frase que informa sua unidade e exceção. O seletor deve manter suporte suficiente ou indicar que o orçamento não permite resposta confiável.

Plano de avaliação proposto:
Avaliação proposta: comparar ranking independente e seleção com dependências no mesmo orçamento. Medir conservação de condições, respostas apoiadas, tokens e custo do seletor; avaliar também casos em que a ausência de informação exige abstenção.

Comparações:
- T038 (complements): Selective Context acrescenta critérios específicos de seleção à família de poda.
- T006 (specializes): Poda é compressão por remoção; não sintetiza necessariamente um texto novo.

Afirmação rastreável:
Selective Context reduz entrada removendo redundância, enquanto LLMLingua-2 aprende seleção de tokens com contexto bidirecional.
Suporte: direct; fontes: A-S016, V3A-S001
Limite: Os métodos não oferecem garantia universal de preservação de toda dependência semântica.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T018:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou dependências na poda. Aqui o novo critério é medir valor marginal dos blocos com ablações e controlar deriva da política.

Projeto e decomposição
Remova blocos candidatos individualmente em validação e observe quais decisões mudam. Atribua importância pelo efeito na tarefa, separando evidência redundante de condição rara.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

Controle adaptativo
Aprenda política de poda por família de pergunta e congele sua versão durante avaliação. Feedback de uso pode criar viés se só forem observadas respostas que passaram pelo filtro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

Validação contrafactual
Compare poda baseada em comprimento, score e efeito contrafactual. Meça perda de requisitos raros e ganho de custo, incluindo expansão de recuperação. Unidade de avaliação: pacote de evidências. Uma ablação deve remover um bloco redundante e outra deve remover uma condição rara do mesmo tamanho. Se a política atribuir valor semelhante aos dois, o score não representa utilidade da tarefa. Registre quais respostas mudaram e se houve recuperação posterior; avaliação apenas sobre tokens removidos esconderia perda de capacidade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

USO AVANÇADO — Dossiê com duplicatas
Cenário: Muitos textos repetem o mesmo anúncio.
Estratégia: Reter origem primária e versões que adicionam condição nova; não remover discordância por parecer redundante.
Papel do modelo pequeno: 3–7B detecta duplicação com verificação de campos.
Aceite proposto: Manter todas as condições únicas relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

USO AVANÇADO — Assistência técnica
Cenário: Logs comuns escondem uma exceção.
Estratégia: Proteger códigos de erro e mudança de estado; podar mensagens repetidas e recuperar bloco completo se diagnóstico permanecer ambíguo.
Papel do modelo pequeno: 8–14B interpreta conjunto reduzido.
Aceite proposto: Causa escolhida deve persistir no teste com log integral.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de blocos elegíveis para remoção, sob regras determinísticas.
8–14B: Leitor que sinaliza requisito perdido e pede expansão.
15–30B: Avaliador de conflitos entre blocos antes da poda final.
Requisitos de treino/runtime: Amostras de ablação e rastreamento de blocos descartados; não usar respostas de avaliação como treino.
Não aplicar quando: Não existe forma de recuperar conteúdo removido e omissão tem custo alto.

## T018:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C031 — Microsoft Research / LLMLingua-2
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa formula compressão como classificação de tokens treinada com dados destilados.
Mecanismo documentado: Compressor especializado seleciona texto para um leitor posterior.
Correspondência com esta base: Seleção aprendida especializa poda de contexto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.
Limite: Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V3A-S001, V4A-S028.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## T018:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T018 → T039 [feeds]
Como combinar: Transformar valor marginal em prioridade da janela.
Interface: block_id, ganho observado e dependências.
Condição: Estimativa válida para a família de tarefa.
Aceite proposto: Verificar estabilidade em novas fontes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T018 → T044 [complements]
Como combinar: Reabrir bloco quando surgir lacuna concreta.
Interface: Requisito faltante e referência descartada.
Condição: Política registrar o descarte.
Aceite proposto: Comparar recuperação dirigida com reinserção integral.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Conservar casos rejeitados para avaliar viés de seleção.
- Não usar frequência de acesso como único valor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar perda causada pela poda em leitores pequenos e fronteira; tolerância à informação incompleta varia.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T038, T039

## Fontes primárias associadas

### A-S016 — Compressing Context to Enhance Inference Efficiency of Large Language Models

[https://aclanthology.org/2023.emnlp-main.391/](https://aclanthology.org/2023.emnlp-main.391/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Selective Context: remoção de redundância no contexto de entrada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T019 — Few-Shot Pruning

**Nome canônico:** Few-Shot Pruning  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T019  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda de demonstrações

## T019:C01 — conceito

Seleciona ou remove demonstrações de um prompt few-shot para economizar contexto sem perder exemplos necessários de comportamento. O alvo são exemplos de tarefa, não fatos atuais. Redundância visual não implica redundância funcional: um caso raro pode ensinar a única exceção importante.

Como funciona:
- Inventariar exemplos por intenção, formato e dificuldade.
- Estimar contribuição e redundância no conjunto.
- Manter um subconjunto que cubra comportamentos e casos de falha.

Nota de nomenclatura: Rótulo descritivo de seleção de exemplos, não método único; a fonte documenta uma ferramenta de seleção relacionada.

## T019:C02 — aplicacao

Quando usar:
- Prompts com muitos exemplos semelhantes.
- Extração ou classificação com poucos padrões realmente distintos.

Quando não usar:
- Não remover a única demonstração de uma classe rara sem testar o efeito correspondente.

Implementação proposta:
- Proposta: avaliar remoção de um exemplo por vez em um conjunto separado.
- Impor cobertura mínima por classe e tipo de erro.
- Fixar ordem e versão do subconjunto para tornar resultados comparáveis.

Aplicação LAI proposta:
Proposta LAI: reduzir exemplos repetidos em contratos de ferramentas; preservar casos que ensinam ausência de evidência, erro de schema e necessidade de recuperação.

## T019:C03 — riscos_validacao

Armadilhas:
- Escolher exemplos usando o conjunto de teste causa vazamento de avaliação.
- A ordem dos exemplos pode mudar resultados mesmo com o mesmo subconjunto.

Métricas sugeridas:
- Acurácia por classe e número de tokens de exemplos.
- Degradação nos casos raros após cada remoção.

Testes propostos:
- Usar consultas não vistas de todas as classes e condições negativas.
- Comparar seleção podada com aleatória sob igual orçamento.

## T019:C04 — perguntas_proveniencia

Pergunta: Few-shot pruning modifica os pesos?
Resposta: Não. Ele muda o conjunto de exemplos apresentado na entrada.

Pergunta: É igual a seleção dinâmica?
Resposta: Não. Pode produzir um subconjunto fixo; seleção dinâmica escolhe exemplos para cada nova consulta.

Pergunta: Exemplos quase duplicados são sempre dispensáveis?
Resposta: Não. Podem mostrar diferenças mínimas que ensinam uma fronteira de decisão. Verifique a função do exemplo antes de comparar apenas o texto.

Pergunta: Posso escolher o subconjunto pela melhor nota final?
Resposta: Use desenvolvimento separado. Escolher com o teste final transforma a avaliação em otimização sobre o gabarito e superestima generalização.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T019:C05 — mecanismo_avancado

Remover demonstrações altera simultaneamente cobertura de casos, distribuição de rótulos e posição dos exemplos restantes. Portanto, atribuir todo ganho à economia de tokens pode esconder um efeito de ordem. Uma política de poda deve proteger exemplos que ensinam exceções ou formatos raros, mesmo quando eles têm pouca similaridade superficial com a maioria das consultas.

Condição de contorno:
Quando o único exemplo de uma regra importante é removido, o conjunto reduzido pode deixar de especificar o comportamento que se pretendia demonstrar.

Contrato proposto:
- Entradas: Conjunto de demonstrações verificadas, categorias de comportamento e orçamento.
- Saídas: Subconjunto ordenado com razões de exclusão e cobertura declarada.
- Estado: Versão do pool, critérios de seleção e separação do conjunto de avaliação.
- Invariante: Exemplos e respostas reservados à avaliação não entram no pool usado para escolher ou ajustar a poda.

Compromissos de projeto:
- Menos exemplos reduzem entrada e podem eliminar ruído, mas também retiram contraexemplos úteis.
- Diversidade aumenta cobertura, porém consome orçamento com casos menos próximos da consulta.

## T019:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir uma exceção demonstrada apenas uma vez e vários exemplos redundantes da regra comum. A poda deve preservar a exceção quando ela pertence ao contrato da tarefa.

Plano de avaliação proposto:
Avaliação proposta: comparar conjunto integral, remoção aleatória e poda orientada, controlando ordem e orçamento. Medir acerto por categoria, formato e sensibilidade a permutações; escolher pelo comportamento dos casos relevantes, não só pela média.

Comparações:
- T046 (complements): Seleção dinâmica escolhe exemplos por consulta; poda pode reduzir previamente o pool ou o conjunto final.

Afirmação rastreável:
O estudo sobre ordem de prompts mostra que a permutação das demonstrações afeta desempenho e não transfere automaticamente entre modelos.
Suporte: direct; fontes: V3A-S017
Limite: Os experimentos são históricos e restritos; a entrada propõe controle de ordem, não um efeito universal de magnitude fixa.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T019:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou ordem e classes. Aqui a poda de demonstrações considera cobertura de confusões específicas e incompatibilidade entre exemplos.

Projeto e decomposição
Construa matriz de confusões do modelo e selecione exemplos que distingam classes confundidas. Exemplos fáceis redundantes consomem janela sem alterar decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

Controle adaptativo
Remova demonstração apenas após testar fronteiras que ela representa. Preserve exemplos de abstenção e exceção, evitando selecionar somente respostas positivas frequentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

Validação contrafactual
Compare seleção por similaridade, diversidade e erro corrigido. Faça validação com novos documentos para não medir memorização de exemplos quase iguais. Unidade de avaliação: família de exemplos. Teste exemplos que corrigem uma confusão específica e exemplos apenas semelhantes no vocabulário. O ganho esperado deve aparecer nos casos de fronteira, sem aumentar cópia de entidades ou valores. Uma análise leave-one-out pode identificar demonstração indispensável, mas a escolha final precisa ser confirmada em documentos diferentes dos usados nessa análise.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

USO AVANÇADO — Extração de requisitos
Cenário: Permissão e obrigação são confundidas.
Estratégia: Manter pares contrastivos de modalidade e eliminar exemplos que apenas repetem formato. Testar frases novas com negação.
Papel do modelo pequeno: 3–7B extrai modalidade em esquema fechado.
Aceite proposto: Não transformar recomendação em obrigação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

USO AVANÇADO — Classificação de atendimento
Cenário: Categorias raras são comercialmente relevantes.
Estratégia: Escolher exemplos por fronteira entre categorias, reservando demonstração de informação insuficiente.
Papel do modelo pequeno: 8–14B classifica e explica evidência.
Aceite proposto: Recall das classes raras deve satisfazer critério acordado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Poucos pares contrastivos com rótulos estáveis e esquema simples.
8–14B: Conjunto variado por tipo de ambiguidade, não apenas proximidade lexical.
15–30B: Exemplos de decisões compostas e justificativas verificáveis.
Requisitos de treino/runtime: Banco de demonstrações rotulado, separado da avaliação; mudanças de modelo exigem nova análise de confusão.
Não aplicar quando: Exemplos contradizem instrução atual ou revelam dados fora do escopo.

## T019:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q016, V4A-Q024.

## T019:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T019 → T046 [complements]
Como combinar: Selecionar subconjunto por confusão prevista.
Interface: Intenção, classes candidatas e exemplos elegíveis.
Condição: Selector não consultar resposta esperada.
Aceite proposto: Testar exemplos irrelevantes com formato semelhante.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T019 → T198 [feeds]
Como combinar: Calibrar abstenção com exemplos difíceis.
Interface: Classe, evidência e sinal mensurável de incerteza.
Condição: Calibração independente dos exemplos exibidos.
Aceite proposto: Comparar erros confiantes antes e depois da poda.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não escolher ordem usando o conjunto final de teste.
- Evitar duplicatas da mesma origem como diversidade.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar acerto nas fronteiras difíceis; redução do prompt pode expor limitações do modelo pequeno.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T046, T155

## Fontes primárias associadas

### A-S031 — SemanticSimilarityExampleSelector

[https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector](https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Seleção de exemplos por similaridade semântica.

Limite: Resultado de busca e módulo oficial consultados; abertura direta rejeitada por content-type text/markdown.

### V3A-S017 — Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity

[https://aclanthology.org/2022.acl-long.556/](https://aclanthology.org/2022.acl-long.556/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sensibilidade à ordem de demonstrações e não transferência automática de uma boa permutação entre modelos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S016 — What Makes Good In-Context Examples for GPT-3?

[https://arxiv.org/abs/2101.06804](https://arxiv.org/abs/2101.06804)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de demonstrações por recuperação de exemplos semelhantes; comportamento depende do conjunto e do modelo.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T020 — Learned Prompt Compression

**Nome canônico:** Learned Prompt Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T020  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão aprendida de prompts

## T020:C01 — conceito

Família de compressão em que um modelo treinado decide o que preservar ou produz uma representação compacta. Inclui compressão textual e representações latentes como gist tokens. Essas saídas não são intercambiáveis: algumas exigem um modelo consumidor especificamente treinado.

Como funciona:
- Definir a representação de saída: texto, tokens especiais ou estados.
- Treinar ou selecionar compressor compatível com o consumidor.
- Avaliar perda de informação e custo do compressor na tarefa alvo.

## T020:C02 — aplicacao

Quando usar:
- Prompts longos recorrentes com economia potencial significativa.
- Cenários em que regras simples removem conteúdo importante.

Quando não usar:
- Não enviar vetores arbitrários a uma API textual esperando que ela compreenda a representação.

Implementação proposta:
- Proposta: versionar compressor, tokenizer e modelo consumidor conjuntamente.
- Separar tarefas de treino e avaliação por documentos e cenários.
- Preservar entrada original para comparação e fallback quando a fidelidade cair.

Aplicação LAI proposta:
Proposta LAI: testar após estabelecer uma linha de base de recuperação e seleção; a compatibilidade com o checkpoint local precisa ser comprovada.

## T020:C03 — riscos_validacao

Armadilhas:
- Compressão treinada em outro domínio pode apagar detalhes essenciais.
- Mudança do consumidor pode tornar a representação latente incompatível.

Métricas sugeridas:
- Qualidade por razão de compressão.
- Latência total, memória adicional e custo de treinamento amortizado.

Testes propostos:
- Avaliar casos fora do domínio e instruções com exceções.
- Comparar texto integral, compressão simples e compressor aprendido com orçamento idêntico.

## T020:C04 — perguntas_proveniencia

Pergunta: LLMLingua e gist tokens são a mesma coisa?
Resposta: Não. Um pode produzir texto reduzido; gist tokens dependem de uma representação aprendida e de suporte do consumidor.

Pergunta: É compressão sem perda?
Resposta: Em geral não. É uma aproximação cuja utilidade precisa ser medida na resposta final.

Pergunta: Compressor treinado dispensa validação de fidelidade?
Resposta: Não. O objetivo pode aproximar utilidade média sem preservar todos os detalhes críticos de uma aplicação específica.

Pergunta: Como versionar uma representação latente persistida?
Resposta: Vincule-a ao encoder, consumidor, tokenizer e configuração necessários. Se houver incompatibilidade, regenere a partir do original em vez de reinterpretar bytes silenciosamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T020:C05 — mecanismo_avancado

Aprender um compressor pode significar treinar seleção textual ou aprender um canal latente específico. No primeiro caso, a saída ainda pode circular entre consumidores de texto; no segundo, representação, máscara de atenção e modelo consumidor precisam ser compatíveis. O custo de treinamento e preparação deve ser amortizado pela quantidade de contextos ou chamadas em que o compressor será reutilizado.

Condição de contorno:
Mudanças de domínio, idioma, tokenizer ou consumidor podem invalidar a qualidade medida, mesmo quando o formato da saída continua aceito.

Contrato proposto:
- Entradas: Dados de treino separados da avaliação, objetivo de compressão e consumidor alvo.
- Saídas: Compressor versionado e representação com tipo e formato documentados.
- Estado: Pesos, tokenizer, configuração e relação entre entrada original e saída.
- Invariante: A avaliação mede a tarefa final em dados não usados para treinar ou escolher o compressor.

Compromissos de projeto:
- Seleção textual facilita inspeção, mas tem limites de compressão e pode quebrar relações.
- Slots latentes compactam mais agressivamente, porém diminuem portabilidade e auditabilidade direta.

## T020:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: aplicar o compressor a exemplos de outro domínio contendo unidades e identificadores raros. Verificar preservação dos elementos necessários e reconhecer degradação em vez de extrapolar a validação original.

Plano de avaliação proposto:
Avaliação proposta: comparar método aprendido, seleção simples e texto integral, incluindo treinamento amortizado e custo por chamada. Controlar consumidor e orçamento; medir qualidade final, fidelidade e desempenho fora de distribuição.

Comparações:
- T052 (complements): Latent Context especifica uma possível representação, não a totalidade dos métodos aprendidos.
- T179 (distinct_from): Treinar um compressor não equivale necessariamente a internalizar a tarefa no modelo que responde.

Afirmação rastreável:
LLMLingua-2 formula compressão como classificação de tokens; ICAE aprende slots de memória consumidos por uma LLM compatível.
Suporte: direct; fontes: V3A-S001, V3A-S004
Limite: Resultados dependem dos modelos e objetivos de treinamento utilizados nas respectivas pesquisas.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T020:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu compatibilidade e amortização. Aqui o desenho novo adapta compressor ao consumidor e acompanha mudanças de domínio.

Projeto e decomposição
Treine ou selecione compressor conforme o leitor final. Tokens que um modelo grande reconstrói podem ser ambíguos para 3–7B; a função de perda precisa refletir tarefa do consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

Controle adaptativo
Use perfil de compressão por domínio e detectar mudança de distribuição com amostras de reconstrução funcional. A detecção não exige restaurar todo o texto, mas preservar respostas a requisitos definidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

Validação contrafactual
Compare compressor universal, especializado e extração determinística. Inclua treino, manutenção e falhas de transferência no custo amortizado. Unidade de avaliação: par compressor-consumidor. Após quantizar ou trocar o consumidor, repetir teste de preservação é obrigatório: o compressor não mudou, mas sua linguagem pode ter ficado menos interpretável. Compare erros em números, relações e exceções, além de acerto global. Se o ganho desaparecer, usar texto menos comprimido pode ser melhor que retreinar toda a cadeia.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

USO AVANÇADO — Leitor local de manuais
Cenário: Modelo pequeno recebe contexto de servidor.
Estratégia: Aprender seleção de trechos que preservam campos necessários; enviar conteúdo original quando detector indicar domínio desconhecido.
Papel do modelo pequeno: 3–7B lê formato treinado.
Aceite proposto: Qualidade deve atingir mínimo no domínio e degradar de forma detectável fora dele.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

USO AVANÇADO — Fluxo com várias tarefas
Cenário: Mesmo corpus atende perguntas distintas.
Estratégia: Usar compressor geral para descoberta e compressão específica após selecionar objetivo; manter ambos vinculados à origem.
Papel do modelo pequeno: 8–14B decide campos necessários.
Aceite proposto: Não reutilizar representação específica para objetivo incompatível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S001, V3A-S004, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor treinado em representação simples e explícita.
8–14B: Compressor ou leitor especializado em poucas famílias de tarefa.
15–30B: Professor ou avaliador de preservação funcional, sem garantir decodificação universal.
Requisitos de treino/runtime: Dados de treino separados por origem, leitor fixado por versão e avaliação após quantização.
Não aplicar quando: Modelo é fechado sem interface compatível para memória latente ou domínio muda rápido demais.

## T020:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C031 — Microsoft Research / LLMLingua-2
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa formula compressão como classificação de tokens treinada com dados destilados.
Mecanismo documentado: Compressor especializado seleciona texto para um leitor posterior.
Correspondência com esta base: Compressão aprendida explícita.
Transferência proposta para modelo pequeno: Proposta de engenharia: Compressor menor que o leitor pode preparar trechos para 3–30B; validar capacidade de ler texto comprimido.
Limite: Página declara demonstração de pesquisa; integrações não comprovam ganho para todo leitor. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V3A-S001, V4A-S028.

V4A-C023 — IBM / Granite RAG LoRAs experimentais
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Anúncio distingue modelos disponíveis de adaptadores publicados no Granite Experiments.
Mecanismo documentado: Adaptadores para subtarefas como reescrita de consultas e detecção de alucinação.
Correspondência com esta base: Especialização aprendida é relacionada, mas não comprova compressor de prompts.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir especialização de 8B por papel sem ativar o mesmo adaptador em tarefas incompatíveis.
Limite: Experimentos não são implantação; não transferir compatibilidade KV de aLoRA a qualquer LoRA. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q017, V4A-Q024.

## T020:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T020 → T177 [complements]
Como combinar: Adaptar leitura ao formato comprimido.
Interface: Pares original/comprimido e tarefa rotulada.
Condição: Treino autorizado e dados separados.
Aceite proposto: Medir benefício além de simples exposição ao domínio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S001, V3A-S004, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T020 → T037 [complements]
Como combinar: Aplicar compressão condicionada à pergunta quando necessário.
Interface: Consulta, representação e versão do compressor.
Condição: Objetivo da consulta permanecer estável.
Aceite proposto: Trocar pergunta e detectar necessidade de recompressão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S001, V3A-S004, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não transportar estados latentes entre arquiteturas apenas pela dimensão.
- Conservar caminho de leitura sem compressão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar pares completos compressor-leitor; ganho isolado do compressor não demonstra qualidade do sistema.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T022, T052, R005

## Fontes primárias associadas

### A-S015 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models

[https://aclanthology.org/2023.emnlp-main.825/](https://aclanthology.org/2023.emnlp-main.825/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão textual com orçamento e seleção iterativa de tokens.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S033 — Learning to Compress Prompts with Gist Tokens

[https://arxiv.org/abs/2304.08467](https://arxiv.org/abs/2304.08467)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações compactas de prompt treinadas com alterações de máscara de atenção.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V3A-S004 — In-context Autoencoder for Context Compression in a Large Language Model

[https://arxiv.org/abs/2307.06945](https://arxiv.org/abs/2307.06945)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Slots de memória latente treinados por objetivos de reconstrução e linguagem; condicionamento de um consumidor compatível.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs

[https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo 8B disponível e adaptadores experimentais por subtarefa RAG; separar disponibilidade e experimento.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T021 — Context Compression On-the-Fly

**Nome canônico:** Context Compression On-the-Fly  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T006  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão dinâmica em execução

## T021:C01 — conceito

Aplica compressão durante a execução, quando novos dados ou crescimento do histórico ultrapassam um orçamento. O que a diferencia é o momento e a adaptação ao estado atual; não é uma nova classe universal de algoritmo de compressão.

Como funciona:
- Medir o contexto antes de cada chamada relevante.
- Acionar seleção ou síntese quando um limiar operacional é atingido.
- Validar o novo pacote e conservar a versão anterior recuperável.

Nota de nomenclatura: Variante operacional da família Context Compression; mantida para preservar o inventário.

## T021:C02 — aplicacao

Quando usar:
- Agentes de muitas etapas com volume imprevisível de ferramentas.
- Sessões cuja pergunta atual muda o que precisa permanecer ativo.

Quando não usar:
- Evitar compressor pesado por rodada quando o custo supera a economia de inferência.

Implementação proposta:
- Proposta: usar um limiar de alerta e outro de bloqueio.
- Comprimir blocos concluídos, preservando objetivo, pendências e vínculos de ferramentas.
- Registrar tamanho antes/depois, origem e versão para explicar decisões futuras.

Aplicação LAI proposta:
Proposta LAI: colocar o controle no runtime da Helena, com regras de orçamento, em vez de depender apenas de o modelo perceber que está ficando sem contexto.

## T021:C03 — riscos_validacao

Armadilhas:
- Recompressões sucessivas acumulam erro.
- Acionar compressão somente após estourar a janela pode impedir produzir a própria síntese.

Métricas sugeridas:
- Frequência de compactação e tempo gasto nela.
- Retenção de restrições ao longo de múltiplos ciclos.

Testes propostos:
- Executar histórico sintético longo com mudanças de objetivo e checar o estado vigente.
- Simular falha durante compressão e manter disponível o checkpoint anterior.

## T021:C04 — perguntas_proveniencia

Pergunta: Preciso retreinar o modelo para comprimir em tempo real?
Resposta: Não para seleção e síntese textual; métodos latentes específicos podem exigir treinamento.

Pergunta: Comprimir a cada turno é ideal?
Resposta: Não. A frequência deve equilibrar custo, volume e risco de perda acumulada.

Pergunta: A margem deve ser uma porcentagem fixa?
Resposta: Não necessariamente. Resultados de ferramentas e saídas variam em tamanho; uma reserva baseada nas próximas etapas pode ser mais informativa.

Pergunta: O que fazer se a compactação falhar?
Resposta: Preserve a versão anterior e registre a falha. Não avance com um resumo parcial como se tivesse conservado os requisitos indispensáveis.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T021:C05 — mecanismo_avancado

Compressão durante execução é um problema de controle com custo de intervenção. Um gatilho próximo demais do limite pode não deixar espaço para produzir a nova representação; acionamento frequente também perde tempo e cache. A política deve considerar tamanho provável do próximo resultado, margem para saída e uma condição de rearme, evitando compactar continuamente em torno do mesmo limiar.

Condição de contorno:
Se o próximo artefato indispensável exceder o orçamento disponível, compressão oportunista do histórico pode não resolver a incompatibilidade da tarefa.

Contrato proposto:
- Entradas: Contexto atual, próxima etapa, reservas e regiões protegidas.
- Saídas: Nova representação validada e manifesto do que foi substituído.
- Estado: Versões antes e depois, último gatilho e referências aos originais.
- Invariante: A nova versão só substitui a anterior após preservar o estado operacional necessário à próxima ação.

Compromissos de projeto:
- Gatilhos antecipados deixam margem, mas podem comprimir conteúdo que ainda seria útil.
- Reduções maiores amortizam intervenção, ao custo de retirar mais informação de uma vez.

## T021:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: simular crescimento abrupto por saída de ferramenta e, depois, pequenas oscilações de tamanho. Verificar reserva suficiente e ausência de repetidas compressões sem trabalho útil entre elas.

Plano de avaliação proposto:
Avaliação proposta: comparar limiar simples e política com margem e rearme sobre sequências equivalentes. Medir intervenções, tokens recuperados, perda de fatos, invalidações de cache e tempo total até concluir a tarefa.

Comparações:
- T006 (specializes): É uma política de aplicação temporal dos mecanismos de compressão.
- T212 (complements): Auto-Compact por gatilho pode implementar parte desta política, com comportamento próprio do executor.

Afirmação rastreável:
A documentação de context editing permite condicionar a limpeza a um ganho mínimo de tokens para justificar a invalidação de cache.
Suporte: direct; fontes: V3A-S008
Limite: O desenho de controlador aqui proposto é mais geral que as opções de um provedor específico.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T021:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 usou histerese. Aqui a decisão de comprimir considera previsão de crescimento e custo de interromper a execução.

Projeto e decomposição
Estime tamanho dos próximos resultados antes da chamada. Compressão preventiva pode evitar estouro, mas previsão pessimista demais desperdiça chamadas e destrói detalhes cedo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

Controle adaptativo
Escolha momento de compactar em fronteira estável: após confirmar resultado e antes de abrir nova fase. Se chegam eventos concorrentes, preservar fila posterior à revisão usada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

Validação contrafactual
Compare gatilho somente por ocupação e gatilho por crescimento previsto. Meça estouros, compressões inúteis e tempo parado. Unidade de avaliação: trajetória com crescimento. Teste dois resultados de ferramenta com tamanhos medianos iguais e caudas diferentes. A previsão deve distinguir risco de estouro, não apenas média histórica. Registre compactações acionadas sem necessidade e compactações tardias que interrompem a tarefa; ambos os erros precisam entrar na escolha do gatilho e da margem de reserva.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

USO AVANÇADO — Agente de investigação
Cenário: Uma próxima busca pode retornar material enorme.
Estratégia: Projetar tamanho por ferramenta, reservar margem e reduzir apenas blocos recuperáveis; ajustar previsão com uso observado.
Papel do modelo pequeno: 3–7B estima categoria; código contabiliza tokens.
Aceite proposto: Não exceder limite em cenários de cauda.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

USO AVANÇADO — Sessão interativa
Cenário: Usuário precisa resposta com baixa demora.
Estratégia: Agendar compressão entre etapas, mantendo um pacote mínimo pronto para interrupções e novas instruções.
Papel do modelo pequeno: 8–14B produz estado resumido.
Aceite proposto: Nova instrução deve ser preservada sem aguardar resumo obsoleto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, V3A-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de crescimento provável com contabilidade determinística externa.
8–14B: Resumidor preventivo de blocos encerrados.
15–30B: Controlador de alternativas entre resumir, expandir janela e decompor tarefa.
Requisitos de treino/runtime: Telemetria por ferramenta e política de revisão; medir custos no hardware e protocolo reais.
Não aplicar quando: Não há conteúdo dispensável e a próxima operação exige mais contexto que o limite útil.

## T021:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q024.

## T021:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T021 → T222 [requires]
Como combinar: Observar consumo e previsão por operação.
Interface: Ocupação, margem, tipo de ferramenta e quantis de resultado.
Condição: Previsão recalibrada com tráfego real.
Aceite proposto: Testar resultados maiores que o esperado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, V3A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T021 → T210 [alternative]
Como combinar: Rotacionar sessão quando compactação não preservar requisitos.
Interface: Handoff, revisão e pendências.
Condição: Novo contexto receber contrato completo.
Aceite proposto: Comparar continuidade e custo da rotação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, V3A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não comprimir repetidamente o mesmo texto sem ganho.
- Registrar divergência entre previsão e tamanho real.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar execução contínua sob pressão de contexto; evitar confundir menos estouros com respostas melhores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T043, T168

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T022 — Instruction Compression

**Nome canônico:** Instruction Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T022  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão de instruções

## T022:C01 — conceito

Reduz o espaço ocupado por instruções preservando as regras necessárias. Pode significar reescrita textual concisa ou compressão aprendida; o método precisa ser declarado. Alterar o texto não é o mesmo que internalizar uma política nos pesos.

Como funciona:
- Separar regras obrigatórias, exemplos e explicações auxiliares.
- Eliminar redundância ou produzir representação compatível.
- Comparar cumprimento de regras no prompt original e no comprimido.

## T022:C02 — aplicacao

Quando usar:
- Instruções estáveis com muita repetição.
- Múltiplos blocos que expressam a mesma regra em linguagem diferente.

Quando não usar:
- Não remover condições, prioridades ou exceções para obter uma taxa arbitrária de redução.

Implementação proposta:
- Proposta: extrair uma tabela de requisitos observáveis antes de reescrever.
- Gerar casos positivos, negativos e de conflito para cada regra.
- Versionar original e versão compacta e proibir promoção sem avaliação de cumprimento.

Aplicação LAI proposta:
Proposta LAI: compactar orientações recorrentes de ferramenta; manter permissões obrigatórias também em verificações do runtime, não apenas em linguagem natural.

## T022:C03 — riscos_validacao

Armadilhas:
- Uma frase curta pode ampliar a autorização originalmente restrita.
- Abreviações podem ser interpretadas de formas distintas por modelos diferentes.

Métricas sugeridas:
- Taxa de cumprimento por regra.
- Tokens economizados e necessidade de esclarecimentos adicionais.

Testes propostos:
- Testar conflitos entre regras e exceções raras.
- Executar o mesmo conjunto em dois consumidores se o prompt pretende ser portátil.

## T022:C04 — perguntas_proveniencia

Pergunta: Posso substituir instruções por siglas inventadas?
Resposta: Só se o consumidor tiver uma forma confiável de resolver essas siglas; do contrário você retirou informação.

Pergunta: É Context Distillation?
Resposta: A reescrita textual não. Destilação paramétrica envolve treinamento para internalizar comportamento.

Pergunta: Posso validar somente se a resposta parece adequada?
Resposta: Isso perde violações raras. Transforme cada regra relevante em casos observáveis e examine erros por categoria.

Pergunta: Qual conteúdo não convém abreviar agressivamente?
Resposta: Identificadores, condições numéricas, exceções e escopos que mudam decisões precisam de representação inequívoca; a escolha deve seguir o contrato da tarefa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T022:C05 — mecanismo_avancado

Instruções devem ser testadas como contratos de comportamento: condição, ação, exceção e precedência. Uma reescrita curta pode preservar os verbos e perder o escopo de uma proibição. Em compressão latente, a verificação muda de inspeção textual para comportamento do par encoder/consumidor. Ambas exigem casos que distingam interpretações próximas, não apenas exemplos típicos de sucesso.

Condição de contorno:
Quando uma regra nova contradiz ou especializa a antiga, reutilizar sua representação comprimida sem atualização pode manter um comportamento obsoleto.

Contrato proposto:
- Entradas: Instruções versionadas, casos de comportamento e método de compressão declarado.
- Saídas: Texto reduzido ou representação latente ligada ao consumidor correto.
- Estado: Versão da política original, compressor e resultados de validação.
- Invariante: Exceções e limites de autorização não desaparecem por serem pouco frequentes nos exemplos.

Compromissos de projeto:
- Reescrita textual é inspecionável, mas depende da interpretação posterior.
- Compressão aprendida pode reutilizar representações, porém exige compatibilidade e testes quando as regras mudam.

## T022:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar uma regra geral com exceção explícita e depois alterar somente a exceção. A representação nova deve acompanhar a mudança, enquanto a anterior permanece identificável como obsoleta.

Plano de avaliação proposto:
Avaliação proposta: comparar instrução integral e comprimida em pares de casos que diferem em condição, negação ou precedência. Medir violações por regra, tokens e custo, mantendo exemplos de desenvolvimento separados dos testes finais.

Comparações:
- T020 (complements): Métodos aprendidos podem comprimir instruções, mas também outros tipos de contexto.
- T179 (distinct_from): Destilação paramétrica pode eliminar a necessidade do contexto de tarefa; compressão textual ainda precisa ser fornecida.

Afirmação rastreável:
Gisting treina um modelo com máscaras de atenção para representar prompts em conjuntos menores de gist tokens.
Suporte: direct; fontes: A-S033
Limite: O mecanismo requer treinamento e consumidor compatível; não é uma abreviação que qualquer API de texto interprete.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T022:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 preservou exceções e precedência. Aqui instruções são compiladas em contratos testáveis antes da redução textual.

Projeto e decomposição
Separe objetivos, restrições e formato de saída em estrutura intermediária. Só então gere instrução curta; a forma reduzida precisa representar o mesmo conjunto de condições.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

Controle adaptativo
Use testes de fronteira para detectar mudança semântica: permissões condicionais, prioridades e exceções. Frases redundantes podem funcionar como sinal ao modelo pequeno e não devem ser removidas por estética.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

Validação contrafactual
Compare instrução original, abreviada e estruturada. Meça violações por tipo, incluindo pedidos que ativam simultaneamente condições conflitantes. Unidade de avaliação: família de instruções. Use pares de pedidos que ativam a regra geral e sua exceção, incluindo um caso em que duas restrições competem. A instrução reduzida deve preservar a mesma precedência observada na especificação. Quando a forma curta falhar apenas num consumidor pequeno, aumentar explicitação local pode ser preferível a copiar integralmente todo o prompt original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

USO AVANÇADO — Classificador de documentos
Cenário: Política extensa define poucos campos.
Estratégia: Converter regras em tabela de decisão, fornecer apenas ramo aplicável e manter justificativa de seleção.
Papel do modelo pequeno: 3–7B executa decisão delimitada.
Aceite proposto: Saída deve cumprir todas as regras ativas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

USO AVANÇADO — Agente com ferramentas
Cenário: Instruções misturam planejamento e protocolos.
Estratégia: Manter contrato de chamada em schema e resumo de intenção no prompt; carregar procedimento completo para operação rara.
Papel do modelo pequeno: 8–14B escolhe operação.
Aceite proposto: Nenhuma pré-condição pode desaparecer na versão curta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S033, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Executor de regras curtas com poucos ramos e exemplos contrastivos.
8–14B: Interpretador de contrato estruturado com exceções explícitas.
15–30B: Planejador que seleciona subcontratos sem alterar sua autoridade.
Requisitos de treino/runtime: Especificação de regras, testes independentes e versão do prompt; métodos paramétricos exigem treino distinto.
Não aplicar quando: A redução muda prioridade ou o modelo não interpreta confiavelmente a estrutura escolhida.

## T022:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C032 — Eshita Jha, Mingxian Wang, Andrei Barbu, Chetan Aggarwal / PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo identificado estuda internalização seletiva de componente de prompt.
Mecanismo documentado: Diagnóstico distingue padrões e procedimentos; dados derivados do professor treinam LoRA.
Correspondência com esta base: Internalização de instrução se relaciona à redução de prompt, mas não é simples abreviação.
Transferência proposta para modelo pequeno: Proposta de engenharia: Comparar adapter 3–30B ao mesmo modelo com instrução completa e medir custo de atualização.
Limite: Não encontrada implantação bigtech exata nesta pesquisa; resultados não legitimam trocar de PRISM homônimo. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S011.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q017, V4A-Q024.

## T022:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T022 → T197 [complements]
Como combinar: Validar formato fora do texto de instrução.
Interface: Schema, campos obrigatórios e versão.
Condição: Validação sintática não substituir semântica.
Aceite proposto: Produzir saída bem formada que viole regra e exigir rejeição.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S033, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T022 → T014 [complements]
Como combinar: Carregar regra especializada somente quando aplicável.
Interface: Intenção, pré-condições e referência ao procedimento.
Condição: Roteamento manter cobertura de exceções.
Aceite proposto: Testar operação rara omitida do resumo inicial.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S033, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir compressão textual com PRISM ou destilação paramétrica.
- Preservar teste da instrução original como controle.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar aderência a regras difíceis; instrução curta não garante capacidade de interpretação equivalente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T020, T155, T179

## Fontes primárias associadas

### A-S033 — Learning to Compress Prompts with Gist Tokens

[https://arxiv.org/abs/2304.08467](https://arxiv.org/abs/2304.08467)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Representações compactas de prompt treinadas com alterações de máscara de atenção.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S040 — Learning by Distilling Context

[https://arxiv.org/abs/2209.15189](https://arxiv.org/abs/2209.15189)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fine-tuning para internalizar benefícios de instruções e exemplos antes fornecidos no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### A-S011 — PRISM: Prompt Representation Internalization via Selective Compression into LoRA Weights

[https://aclanthology.org/2026.emnlp-main.2431/](https://aclanthology.org/2026.emnlp-main.2431/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diagnóstico de componentes do prompt e autodestilação seletiva em adaptadores LoRA.

Limite: Identificação pelo título completo; há projetos homônimos. Resultados publicados não foram reproduzidos nesta entrega.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T023 — Recursive Summarization Tree

**Nome canônico:** Recursive Summarization Tree  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** árvore recursiva de resumos

## T023:C01 — conceito

Árvore de resumos recursivos em que folhas representam trechos originais e nós internos sintetizam seus descendentes. É uma forma estrutural de sumarização hierárquica, preservada aqui como entrada própria do inventário, sem contabilizá-la como mecanismo independente.

Como funciona:
- Criar folhas com referências exatas às fontes.
- Agrupar folhas e gerar resumos com ligações aos filhos.
- Repetir até um nível de visão geral que caiba no orçamento.

Nota de nomenclatura: Representação estrutural da sumarização hierárquica; não deve ser contada como tecnologia independente.

## T023:C02 — aplicacao

Quando usar:
- Navegação de acervos extensos por nível de detalhe.
- Perguntas amplas que precisam descer a documentos específicos para comprovação.

Quando não usar:
- Não confiar em um nó superior para citar literalmente texto que só existe nas folhas.

Implementação proposta:
- Proposta: armazenar parent_id, child_ids, hash dos filhos e versão do resumidor.
- Limitar profundidade e tamanho de nó de acordo com a distribuição dos documentos.
- Ao atualizar conteúdo, invalidar o caminho até a raiz e reconstruir somente a parte afetada.

Aplicação LAI proposta:
Proposta LAI: manter uma árvore por domínio de software e ligações entre domínios; fontes originais continuam acessíveis para auditoria.

## T023:C03 — riscos_validacao

Armadilhas:
- Profundidade excessiva amplia perdas de detalhe.
- Agrupamento instável pode mudar toda a árvore após pequenas alterações.

Métricas sugeridas:
- Profundidade média de navegação até a evidência.
- Custo de atualização e fidelidade de cada nível.

Testes propostos:
- Pedir uma afirmação do resumo raiz e localizar sua folha de origem.
- Alterar uma folha e verificar que nenhum ancestral antigo é servido como atual.

## T023:C04 — perguntas_proveniencia

Pergunta: A árvore precisa ser binária?
Resposta: Não. A ramificação deve refletir orçamento, estrutura e qualidade de agregação.

Pergunta: Qual diferença para sumarização em cadeia?
Resposta: Na cadeia, cada versão acumula a anterior; na árvore, ramos podem ser sintetizados e atualizados separadamente.

Pergunta: Como manter uma citação precisa no resumo superior?
Resposta: Preserve o caminho até a folha e cite a evidência original quando ela sustentar a afirmação. Citar apenas outro resumo pode esconder erro intermediário.

Pergunta: A raiz pode ser recalculada sem todas as folhas?
Resposta: Pode usar filhos já válidos. Depois de mudanças, é necessário reconstruir os dependentes afetados, mantendo uma revisão consistente da árvore.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T023:C05 — mecanismo_avancado

Uma árvore permite localizar a primeira camada em que uma afirmação desapareceu ou foi alterada. Para isso, cada nó deve conservar seus filhos e a versão do processo que o gerou. A estrutura também distingue cobertura e abstração: visitar um nó ancestral cobre uma síntese de seus descendentes, não prova que o leitor examinou cada folha nem preservou cada detalhe.

Condição de contorno:
Se a síntese não reduz informação suficiente, a profundidade aumenta sem benefício; se reduz demais, perguntas locais exigem voltar às folhas.

Contrato proposto:
- Entradas: Folhas identificadas, regra de agrupamento e condição de término.
- Saídas: Árvore com níveis, resumos e ligações verificáveis aos filhos.
- Estado: Versões dos nós, dependências e estado de reconstrução.
- Invariante: Nenhum nó interno é apresentado como fonte independente dos descendentes que sintetiza.

Compromissos de projeto:
- Árvores balanceadas limitam profundidade, mas podem agrupar unidades pouco relacionadas.
- Agrupamento semântico melhora coerência local e pode produzir tamanhos irregulares e manutenção mais complexa.

## T023:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma exceção numa folha e acompanhar sua passagem por cada nível. Quando houver perda, a consulta deve expandir o nó relevante ou registrar insuficiência, sem inventar a exceção no topo.

Plano de avaliação proposto:
Avaliação proposta: comparar cadeia incremental e árvore sob igual orçamento de saída. Medir profundidade, custo de reconstrução, localização de erros e recuperação de detalhes; variar ordem dos documentos e distribuição de tamanho das folhas.

Comparações:
- T008 (specializes): A árvore explicita uma implementação estrutural da sumarização hierárquica.
- T030 (distinct_from): RAPTOR acrescenta procedimentos de embeddings, agrupamento e busca; uma árvore de resumos isolada não o reproduz.

Afirmação rastreável:
O trabalho sobre livros resume pequenas seções e depois resume recursivamente essas sínteses.
Suporte: direct; fontes: V3A-S021
Limite: O treinamento com feedback humano do estudo não está implícito em qualquer árvore construída por prompts.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T023:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou erro recursivo. Aqui a árvore pode ser materializada sob demanda e manter níveis orientados a perguntas distintas.

Projeto e decomposição
Crie nós apenas quando houver utilidade de consulta, evitando resumir todos os níveis antecipadamente. Popularidade da região e custo de atualização orientam materialização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Controle adaptativo
Separe resumo descritivo e índice de perguntas respondíveis pelo nó. O índice melhora roteamento; o resumo sozinho pode ocultar detalhe que seria necessário.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Validação contrafactual
Compare árvore completa e parcial sob carga com consultas frequentes e raras. Meça tempo inicial, atualização e custo acumulado. Unidade de avaliação: árvore de sínteses. Inclua uma consulta rara sobre folha recém-adicionada e uma consulta frequente sobre ramo já materializado. A árvore parcial deve responder ambas sem apresentar nó pendente como vazio. Medir tempo de primeira consulta e custo acumulado distingue trabalho adiado de trabalho eliminado, evitando atribuir economia a uma construção simplesmente incompleta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Acervo crescente
Cenário: Novos documentos chegam continuamente.
Estratégia: Adicionar folhas e materializar ancestrais de regiões consultadas; marcar nós pendentes para que o leitor não trate ausência como resumo vazio.
Papel do modelo pequeno: 3–7B extrai índice de perguntas.
Aceite proposto: Consulta rara deve chegar à folha mesmo sem ancestral pronto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Relatórios em múltiplos níveis
Cenário: Diretoria e operação exigem detalhes diferentes.
Estratégia: Construir vistas por granularidade usando as mesmas folhas; manter divergências disponíveis em ambos os níveis.
Papel do modelo pequeno: 15–30B redige síntese executiva.
Aceite proposto: Conclusão executiva não pode contrariar evidência operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de descritores de folha e perguntas possíveis.
8–14B: Resumidor de conjuntos pequenos com teste de cobertura.
15–30B: Integrador de vistas com escopos e granularidades diferentes.
Requisitos de treino/runtime: Catálogo de nós materializados, custo de geração e dependências de origem; política de atualização explícita.
Não aplicar quando: Cada consulta exige combinação inédita que atravessa quase toda a árvore.

## T023:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q021, V4A-Q022.

## T023:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T023 → T026 [feeds]
Como combinar: Usar índice de perguntas para navegar até evidências.
Interface: node_id, temas, perguntas cobertas e filhos.
Condição: Índice não for tratado como resposta comprovada.
Aceite proposto: Testar pergunta cuja resposta está em folha pouco popular.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T023 → T007 [complements]
Como combinar: Cachear síntese por conjunto de filhos e política.
Interface: Digest dos filhos, prompt e versão do leitor.
Condição: Dependências completas comporem a chave.
Aceite proposto: Modificar folha e exigir regeneração do ancestral consultado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar nó não materializado como ausência de conteúdo.
- Evitar circularidade entre síntese e sua própria evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar amortização por perfil de consulta; síntese hierárquica não deve substituir evidência de detalhe.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T004, T008, T026, T030

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S021 — Recursively Summarizing Books with Human Feedback

[https://arxiv.org/abs/2109.10862](https://arxiv.org/abs/2109.10862)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Decomposição recursiva de sumarização e treinamento com feedback humano; avaliação em níveis distintos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T024 — Context Broker e Context Builder

**Nome canônico:** Context Broker / Context Builder  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T024  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** montador de contexto; gerenciador de contexto; Context Broker / Context Builder

## T024:C01 — conceito

Componente do runtime que monta a entrada de cada chamada a partir de objetivo, regras, estado, histórico e evidências. É uma fronteira de engenharia para tornar seleção e orçamento observáveis. Não existe um único algoritmo padronizado com esse nome.

Como funciona:
- Receber objetivo, identidade, modelo e limites de entrada/saída.
- Selecionar fontes autorizadas e informações necessárias.
- Ordenar, validar e emitir um pacote de contexto com manifesto.

Nota de nomenclatura: Nome arquitetural descritivo; implementação e critérios propostos são editoriais.

## T024:C02 — aplicacao

Quando usar:
- Sistemas com vários agentes, fontes e modelos.
- Necessidade de explicar por que uma informação entrou ou ficou fora de uma decisão.

Quando não usar:
- Não delegar ao broker a criação de permissões que não existem no sistema de origem.

Implementação proposta:
- Proposta: manter políticas obrigatórias fora da seleção probabilística.
- Registrar documentos, versões, critérios de seleção e estimativa de tokens.
- Se o essencial não couber, dividir a tarefa ou reduzir saída, em vez de cortar silenciosamente restrições.

Aplicação LAI proposta:
Proposta LAI: centralizar seleção de contexto sob Helena, mantendo contratos de entrada e saída independentes do provedor de LLM.

## T024:C03 — riscos_validacao

Armadilhas:
- O broker pode se tornar gargalo de latência.
- Pontuações de relevância podem remover informação necessária mas semanticamente distante.

Métricas sugeridas:
- Violações de orçamento e taxa de omissão de campos obrigatórios.
- Custo de construção, cache hit e sucesso da missão.

Testes propostos:
- Criar contexto com documentos de dois tenants e permitir somente o autorizado.
- Forçar orçamento menor que as instruções obrigatórias e exigir erro controlado.

## T024:C04 — perguntas_proveniencia

Pergunta: É obrigatório usar um framework específico?
Resposta: Não. A interface pode ser implementada com funções e armazenamento próprios.

Pergunta: O broker deve resumir tudo?
Resposta: Não. Ele decide quais originais, resumos e referências são adequados à chamada atual.

Pergunta: O manifesto precisa copiar todo o prompt?
Resposta: Não necessariamente. Pode referenciar blocos imutáveis e registrar versões e posições, desde que permita reconstrução autorizada da entrada.

Pergunta: Como diagnosticar uma resposta sem fundamento?
Resposta: Verifique primeiro se a evidência existia, depois se foi recuperada, incluída e corretamente interpretada. Cada etapa exige observáveis diferentes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T024:C05 — mecanismo_avancado

O montador de contexto pode ser tratado como uma função observável: recebe estado e candidatos, produz a requisição e um manifesto de seleção. Isso permite distinguir falha de recuperação de falha de montagem. Categorias como instrução vigente, observação externa e hipótese derivada precisam permanecer identificáveis; concatenar tudo como texto homogêneo facilita confusão de autoridade e origem.

Condição de contorno:
Um builder não consegue reparar uma fonte inexistente ou um estado inconsistente apenas reorganizando mensagens; precisa detectar e expor a falta.

Contrato proposto:
- Entradas: Objetivo, estado versionado, regras vigentes, candidatos e orçamento do modelo.
- Saídas: Requisição compatível e manifesto de blocos incluídos e excluídos.
- Estado: Versões de seletores, fontes, templates e contagem de tokens.
- Invariante: Conteúdo recuperado permanece evidência ou dado, sem ganhar autoridade de instrução pelo simples posicionamento.

Compromissos de projeto:
- Centralizar seleção facilita auditoria, mas pode criar ponto de latência e acoplamento.
- Regras determinísticas melhoram reprodução; relevância aprendida acrescenta adaptação e variabilidade.

## T024:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir em um documento recuperado uma instrução que contradiga o objetivo. O manifesto deve mantê-la como conteúdo da fonte e a montagem não deve promovê-la a regra do sistema.

Plano de avaliação proposto:
Avaliação proposta: comparar montagem fixa e seletiva com candidatos idênticos. Medir fatos excluídos indevidamente, custo, estabilidade entre execuções e clareza da proveniência; decidir pela qualidade da tarefa e capacidade de explicar a seleção.

Comparações:
- T222 (complements): O monitor fornece orçamento; o builder decide como distribui-lo entre conteúdos.
- T066 (complements): O resolvedor entrega versões e conteúdos que o builder pode incorporar.

Afirmação rastreável:
MCP descreve recursos como dados de contexto cuja incorporação é decidida pela aplicação hospedeira.
Suporte: related; fontes: V3A-S019
Limite: A fonte apoia a responsabilidade do host; Context Broker é um componente arquitetural proposto, não uma API universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T024:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu manifesto e confiança. Aqui broker e builder negociam orçamento de aquisição por utilidade marginal e prazo.

Projeto e decomposição
O broker propõe candidatos com custo, atraso e tipo de suporte. O builder seleciona evidências para afirmações prioritárias, expondo lacunas que justificam nova aquisição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

Controle adaptativo
Imponha prazo por estágio e caminho de resposta parcial. Fontes lentas só são aguardadas quando podem alterar decisão importante; paralelismo sem critério pode apenas aumentar custo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

Validação contrafactual
Compare busca fixa e negociação iterativa. Meça cobertura por afirmação, diversidade relevante e tempo até evidência suficiente. Unidade de avaliação: requisição com fontes. Simule fonte lenta que poderia alterar a conclusão e fonte lenta que só acrescentaria contexto decorativo. A política deve esperar ou marcar insuficiência no primeiro caso e poder concluir no segundo. Registre essa classificação antes do resultado chegar, para não avaliar decisão de espera com informação retrospectiva que o controlador não possuía.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

USO AVANÇADO — Resposta com sistemas heterogêneos
Cenário: Fatos estão em documentos e APIs.
Estratégia: Consultar primeiro dados estruturados para campos exatos, depois textos para justificativas; marcar divergências entre canais.
Papel do modelo pequeno: 3–7B roteia campos; 8–14B integra.
Aceite proposto: Cada fato deve vir do canal adequado e revisão conhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

USO AVANÇADO — Análise sob prazo
Cenário: Uma fonte externa está lenta.
Estratégia: Preparar resposta parcial identificada e aguardar somente lacuna decisiva; atualizar quando evidência nova mudar conclusão.
Papel do modelo pequeno: 15–30B avalia impacto de lacunas.
Aceite proposto: Não afirmar completude enquanto fonte obrigatória estiver pendente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S022.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Roteador de necessidades tipadas para fontes autorizadas.
8–14B: Compositor de pacotes por afirmação com orçamento moderado.
15–30B: Planejador de aquisição condicional para perguntas interdependentes.
Requisitos de treino/runtime: Catálogo de fontes com custos e semântica de timeout; decisões de prioridade devem ser registradas.
Não aplicar quando: A política não consegue distinguir fonte opcional de evidência indispensável.

## T024:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Seleção de fontes inspira broker, sem confirmar componente LAI.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C002 — Anthropic / Research multi-agent system
Evidência: produção documentada; somente família relacionada. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: A equipe descreve passagem do protótipo à produção do recurso Research.
Mecanismo documentado: Agente líder salva plano, delega pesquisa paralela, recebe sínteses e decide novas buscas.
Correspondência com esta base: Coordena aquisição e síntese de contexto; não usa o nome editorial como produto.
Transferência proposta para modelo pequeno: Proposta de engenharia: Atribuir pesquisas delimitadas a 3–14B e reservar integração difícil a 15–30B ou escalonamento.
Limite: Relato usa Claude Opus/Sonnet; custo, qualidade e métricas publicados não se transferem aos portes propostos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: C-S030.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q020.

## T024:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T024 → T152 [requires]
Como combinar: Negociar tokens entre aquisição, evidência e saída.
Interface: Orçamento, prioridade e custo estimado.
Condição: Cotas respeitarem requisitos obrigatórios.
Aceite proposto: Testar fonte grande que compete com outra indispensável.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T024 → T067 [feeds]
Como combinar: Transformar lacuna específica em nova consulta.
Interface: claim_id, evidência faltante e limite de tentativas.
Condição: Consulta nova poder modificar a decisão.
Aceite proposto: Medir novas evidências úteis por tentativa.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S022. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar timeout como inexistência de informação.
- Conservar conflitos entre fontes no pacote final.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar qualidade por prazo e custo; coordenação melhor não elimina limites do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T042, T067, T152

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T025 — Adaptive RAG

**Nome canônico:** Adaptive RAG  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T025  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Adaptive-RAG; RAG adaptativo

## T025:C01 — conceito

Escolhe uma estratégia de recuperação conforme dificuldade e necessidade de evidência. O trabalho Adaptive-RAG usa classificação de complexidade para alternar entre resposta sem busca, recuperação única e recuperação iterativa. Em produção, necessidade de atualidade e autorização também deve influenciar a decisão.

Como funciona:
- Classificar a consulta e identificar requisitos de fonte.
- Escolher rota e orçamento compatíveis.
- Reavaliar quando a primeira busca não fornece suporte suficiente.

## T025:C02 — aplicacao

Quando usar:
- Mistura de perguntas simples e análises multissalto.
- Necessidade de controlar custo sem tratar toda pergunta da mesma forma.

Quando não usar:
- Não usar rota sem busca quando a resposta exige fatos internos ou estado atual que o modelo não possui.

Implementação proposta:
- Proposta: construir conjunto rotulado de consultas com rota mínima suficiente.
- Registrar decisão do roteador e comparar com a resposta obtida.
- Permitir escalada por falha de evidência, com limite de tempo e chamadas.

Aplicação LAI proposta:
Proposta LAI: roteador pode selecionar consultas diretas ao corpus, busca cruzada entre técnicas ou análise de dependências; o critério de evidência prevalece sobre economia de tokens.

## T025:C03 — riscos_validacao

Armadilhas:
- Classificar uma pergunta difícil como simples pode produzir resposta convincente sem suporte.
- Consultas curtas nem sempre são fáceis.

Métricas sugeridas:
- Qualidade e custo por classe de complexidade.
- Taxa de escaladas corretas e erros do roteador.

Testes propostos:
- Testar perguntas curtas com duas dependências documentais.
- Comparar todas as rotas sob o mesmo conjunto, incluindo casos em que buscar é obrigatório.

## T025:C04 — perguntas_proveniencia

Pergunta: Adaptive RAG é só escolher top-k?
Resposta: Não. Pode mudar número de buscas, decomposição e uso do gerador; top-k é apenas uma possível variável.

Pergunta: O modelo decide sozinho que não precisa buscar?
Resposta: Pode sugerir, mas regras de atualidade e acesso devem restringir essa escolha.

Pergunta: Self-RAG é a mesma implementação?
Resposta: Não. Self-RAG treina um modelo com tokens de reflexão para controlar recuperação e crítica. O roteador de Adaptive-RAG constitui outro desenho.

Pergunta: Devo continuar buscando até obter alguma resposta?
Resposta: Não. Defina suficiência e orçamento; ausência persistente de evidência precisa levar a lacuna explícita, não a uma conclusão forçada.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T025:C05 — mecanismo_avancado

O roteador precisa considerar assimetria de erros: evitar uma busca desnecessária poupa recursos; omitir uma busca indispensável pode comprometer a resposta inteira. Complexidade aparente e necessidade de atualidade são dimensões diferentes. Uma pergunta curta sobre um estado que muda pode exigir recuperação, enquanto uma transformação longa de texto fornecido pode dispensar conhecimento externo.

Condição de contorno:
Classificadores ajustados em um domínio podem encaminhar consultas novas incorretamente, especialmente quando o custo do erro muda ou o corpus disponível não contém a evidência necessária.

Contrato proposto:
- Entradas: Consulta, restrições de evidência, rotas disponíveis e estimativas de custo.
- Saídas: Rota escolhida, justificativa operacional e condição de fallback.
- Estado: Versão do roteador, decisões anteriores e resultados verificáveis.
- Invariante: Escolher uma rota barata não remove uma exigência de evidência imposta pela tarefa.

Compromissos de projeto:
- Mais rotas permitem adaptação fina e aumentam superfície de teste.
- Fallback protege casos incertos, mas reduz economia e pode criar buscas repetidas sem avanço.

## T025:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: apresentar consulta simples dependente de fato atualizado e consulta complexa resolúvel com texto fornecido. Verificar que a decisão não usa apenas comprimento ou aparência de dificuldade.

Plano de avaliação proposto:
Avaliação proposta: comparar recuperação sempre, nunca e adaptativa em classes definidas por necessidade real. Medir acerto do roteamento, custo total, respostas sem suporte e qualidade final; calibrar pelo custo de cada tipo de erro.

Comparações:
- T009 (specializes): A adaptação escolhe quando e como aplicar etapas de RAG.
- T067 (complements): Recuperação ativa pode reavaliar a necessidade de memória depois da decisão inicial.

Afirmação rastreável:
Adaptive-RAG utiliza um classificador de complexidade para selecionar entre rotas sem recuperação, recuperação única e iterativa.
Suporte: direct; fontes: A-S017
Limite: A exigência de atualidade e o fallback de domínio são extensões editoriais ao critério descrito.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T025:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou complexidade e necessidade de atualização. Aqui o roteamento adapta o esforço à perda esperada de cada tipo de erro.

Projeto e decomposição
Crie rotas distintas para extração exata, comparação e investigação. A decisão inicial usa sinais verificáveis: presença de identificador, necessidade temporal, número de entidades e disponibilidade de fontes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S017, V4A-S014, V4A-S019.

Controle adaptativo
Faça uma recuperação barata antes de escolher profundidade quando a consulta for ambígua. Um conjunto vazio ou contraditório altera a rota; confiança verbal do gerador não substitui esses sinais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S017, V4A-S014, V4A-S019.

Validação contrafactual
Compare política fixa e adaptativa usando custo por resposta aceita. Separe erro de encaminhamento, falha de busca e erro de leitura; uma rota barata que encaminha casos difíceis para abstenção excessiva não demonstra eficiência. Unidade de avaliação: classe de decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S017, V4A-S014, V4A-S019.

USO AVANÇADO — Perguntas técnicas de catálogo
Cenário: Algumas pedem campo exato; outras comparação.
Estratégia: Identificar atributo e versão, consultar registro estruturado e recorrer a documentos somente para exceções ou explicações.
Papel do modelo pequeno: 3–7B escolhe rota simples; 8–14B lê exceções.
Aceite proposto: Medir falsa escolha da rota direta em consultas com exceção documentada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S017, V4A-S014, V4A-S019.

USO AVANÇADO — Investigação com fontes incompletas
Cenário: O acervo pode não responder.
Estratégia: Tentar busca inicial, classificar lacuna e expandir apenas se existir canal plausível. Encerrar com insuficiência após limite de rotas.
Papel do modelo pequeno: 15–30B integra evidências quando necessário.
Aceite proposto: Contabilizar buscas adicionais sem evidência nova e respostas indevidamente completas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S017, V4A-S014, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Roteador de poucas classes com regras para atualização e identidade.
8–14B: Leitor especializado que avalia suficiência de um pacote pequeno.
15–30B: Planejador de investigação em rotas interdependentes, com teto de orçamento.
Requisitos de treino/runtime: Custos por rota, sinais de cobertura e validação por família; calibrar após mudança de corpus ou leitor.
Não aplicar quando: Roteador custa quase tanto quanto resolver ou seus erros não podem ser detectados antes de efeitos.

## T025:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q010, V4A-Q016, V4A-Q017, V4A-Q020.

## T025:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T025 → T036 [feeds]
Como combinar: Escolher reformulação conforme a lacuna.
Interface: Intenção, entidades preservadas e tipo de evidência.
Condição: Rota selecionada exigir busca adicional.
Aceite proposto: Verificar que reformulação mantém entidade e tempo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S017, V4A-S014, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T025 → T203 [complements]
Como combinar: Escalonar quando teste de correção falhar.
Interface: Resultado, falha identificada e evidência disponível.
Condição: Existir verificação independente da confiança declarada.
Aceite proposto: Medir escalonamentos evitáveis e erros que escapam.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S017, V4A-S014, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir consulta simples com informação estável.
- Registrar rota recusada e motivo para investigar viés.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas por rota com fronteira usando as mesmas fontes; reportar ganhos de custo sem esconder abstenções.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T036, T133, T202

## Fontes primárias associadas

### A-S017 — Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity

[https://aclanthology.org/2024.naacl-long.389/](https://aclanthology.org/2024.naacl-long.389/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Classificador seleciona ausência de busca, busca única ou recuperação iterativa conforme complexidade.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S009 — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

[https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação e crítica adaptativas aprendidas com tokens de reflexão; distingue arquitetura treinada de simples instrução de autocrítica.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S014 — DataGemma

[https://deepmind.google/models/gemma/datagemma/](https://deepmind.google/models/gemma/datagemma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RIG substitui números por dados; variante RAG prepara contexto consumido por Gemini 1.5 Pro.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T026 — Hierarchical Retrieval

**Nome canônico:** Hierarchical Retrieval  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T026  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** recuperação hierárquica

## T026:C01 — conceito

Recupera informação usando níveis de organização, como coleção, documento, seção e trecho. A busca pode descer do resumo ao detalhe ou combinar candidatos de vários níveis. O objetivo é melhorar descoberta sem perder precisão e contexto local.

Como funciona:
- Construir ligações entre unidades amplas e unidades específicas.
- Pesquisar no nível adequado à pergunta.
- Expandir candidatos relevantes e entregar evidência na granularidade necessária.

## T026:C02 — aplicacao

Quando usar:
- Bases com muitos documentos e estrutura temática consistente.
- Perguntas que alternam visão geral e detalhe de implementação.

Quando não usar:
- Não impor uma hierarquia rígida quando temas relevantes atravessam vários ramos sem ligações.

Implementação proposta:
- Proposta: armazenar nível, parent_id e caminho de origem.
- Aplicar filtros de acesso em todos os níveis, inclusive resumos.
- Comparar rota de cima para baixo com busca plana para detectar poda prematura de ramos relevantes.

Aplicação LAI proposta:
Proposta LAI: índice por domínio, técnica e seção, com busca direta alternativa para não depender de navegar sempre pela taxonomia.

## T026:C03 — riscos_validacao

Armadilhas:
- Um resumo superior ruim impede encontrar uma folha correta.
- A expansão de muitos pais pode exceder o orçamento.

Métricas sugeridas:
- Recall de documentos e trechos em cada estágio.
- Número de nós lidos até encontrar evidência suficiente.

Testes propostos:
- Criar resposta situada em ramo cuja descrição é pouco semelhante à pergunta.
- Consultar tema transversal e verificar recuperação de mais de uma categoria.

## T026:C04 — perguntas_proveniencia

Pergunta: Recuperação hierárquica exige resumos por LLM?
Resposta: Não. Cabeçalhos, pastas e metadados podem fornecer a hierarquia.

Pergunta: É igual a Parent-Child Retrieval?
Resposta: Parent-child é um caso particular; uma hierarquia pode ter muitos níveis e diferentes políticas de expansão.

Pergunta: Um nó relevante garante filhos relevantes?
Resposta: Não. A síntese pode representar apenas parte dos descendentes. É preciso selecionar e verificar quais folhas sustentam a pergunta.

Pergunta: Como contar cobertura sem inflá-la?
Resposta: Deduplicate referências à mesma evidência e registre a contribuição de cada nível. Um fato citado pelo resumo e pela folha não se torna duas confirmações independentes.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T026:C05 — mecanismo_avancado

A navegação descendente pode tornar um erro inicial irreversível: ao excluir uma coleção no topo, seus melhores trechos deixam de competir. Uma alternativa é manter mais de um caminho e combinar candidatos de níveis diferentes, com deduplicação por evidência. Resumos superiores orientam descoberta, mas os detalhes recuperados ainda precisam sustentar a resposta final.

Condição de contorno:
Quando títulos e resumos não representam os fatos procurados, restringir busca a poucos ramos reduz recall mesmo com um excelente buscador local.

Contrato proposto:
- Entradas: Consulta, hierarquia versionada e orçamento de caminhos e candidatos.
- Saídas: Evidências selecionadas com nível, origem e caminho de recuperação.
- Estado: Mapeamento entre nós e folhas, pontuações e ramos descartados.
- Invariante: A resposta distingue material original de sínteses usadas para orientar a busca.

Compromissos de projeto:
- Busca em poucos ramos reduz custo, mas amplifica erros de roteamento.
- Combinar níveis aumenta cobertura e pode repetir a mesma evidência em resumo e folha.

## T026:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ocultar um fato relevante sob um título pouco relacionado à pergunta. Comparar navegação restrita e busca global de fallback; a política deve reconhecer a limitação do roteamento inicial.

Plano de avaliação proposto:
Avaliação proposta: comparar busca plana, descendente e combinação de níveis com igual orçamento final. Medir recall por estágio, diversidade de fontes, duplicação e latência; decidir conforme perguntas locais e globais do domínio.

Comparações:
- T032 (complements): Parent-child expande o entorno após localizar um filho; a hierarquia também pode orientar a localização inicial.
- T030 (complements): RAPTOR oferece uma estrutura concreta de recuperação em níveis de abstração.

Afirmação rastreável:
RAPTOR constrói representações recursivas e permite recuperar informação em diferentes níveis de abstração.
Suporte: direct; fontes: A-S014
Limite: A política de múltiplos caminhos e fallback proposta precisa ser avaliada separadamente da arquitetura publicada.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T026:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu perda no roteamento hierárquico. Aqui busca em feixe e orçamento de exploração protegem ramos pouco prováveis.

Projeto e decomposição
Mantenha mais de um ramo candidato quando descritores se sobrepõem. O tamanho do feixe depende de diversidade e custo dos ramos, não de um top-k fixo em toda a árvore.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

Controle adaptativo
Reserve cota para um ramo alternativo quando o melhor ramo não fornecer evidência suficiente. Registre cobertura real dos ramos; navegar repetidamente pelo mesmo ancestral não é exploração nova.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

Validação contrafactual
Compare top-1, feixe fixo e expansão por insuficiência. Meça recall de folhas relevantes, custo de navegação e falhas em documentos inseridos recentemente, ainda pouco representados nos resumos. Unidade de avaliação: consulta hierárquica.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

USO AVANÇADO — Manuais por produto
Cenário: Uma consulta cruza versões e componentes.
Estratégia: Roteie por produto e versão obrigatórios, depois explore componentes candidatos. Rejeite ramo semanticamente próximo com versão incompatível.
Papel do modelo pequeno: 3–7B roteia; 8–14B verifica folhas.
Aceite proposto: Toda evidência final deve respeitar produto e revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

USO AVANÇADO — Revisão interdisciplinar
Cenário: Termos iguais aparecem em áreas diferentes.
Estratégia: Abrir ramos de sentidos alternativos, reunir evidências discriminantes e somente depois fechar interpretação.
Papel do modelo pequeno: 15–30B integra resultados por sentido.
Aceite proposto: Não excluir um sentido correto apenas pelo resumo dominante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Navegador com poucas opções e filtros estruturados.
8–14B: Avaliador de suficiência e desambiguação entre ramos próximos.
15–30B: Planejador de exploração limitada em hierarquias múltiplas.
Requisitos de treino/runtime: Descritores de nós, custo por expansão e vínculos às folhas; testar também ramos novos e raros.
Não aplicar quando: A taxonomia não representa a organização das perguntas e quase toda consulta cruza todos os ramos.

## T026:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q009, V4A-Q021.

## T026:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T026 → T008 [requires]
Como combinar: Construir descritores adequados para cada nível.
Interface: node_id, escopo, filhos e resumo de descoberta.
Condição: Resumo não eliminar termos distintivos.
Aceite proposto: Testar consulta respondível apenas em folha minoritária.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T026 → T027 [complements]
Como combinar: Usar busca lexical e vetorial nas folhas elegíveis.
Interface: Lista de ramos permitidos e filtros.
Condição: Ambos os canais respeitarem escopo.
Aceite proposto: Comparar recall antes e depois do filtro hierárquico.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Separar ramo não explorado de ramo sem resposta.
- Impedir ciclo em hierarquias que permitem múltiplos pais.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar recall por custo de navegação; uma árvore profunda não prova raciocínio melhor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T023, T030, T032

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S039 — Markdown node parser

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segmentação por cabeçalhos com metadados de caminho estrutural.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S011 — RAPTOR: official implementation

[https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore recuperável, serialização e interfaces de sumarização, embeddings e resposta. Código de pesquisa não instalado.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V3A-S023 — GraphRAG Global Search

[https://microsoft.github.io/graphrag/query/global_search/](https://microsoft.github.io/graphrag/query/global_search/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Consulta global por relatórios de comunidades com map-reduce; efeito do nível de comunidade no custo e detalhe.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T027 — Hybrid Retrieval — BM25 + vetores

**Nome canônico:** Hybrid Retrieval — BM25 + Vetores  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T027  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** hybrid search; busca híbrida; Hybrid Retrieval — BM25 + Vetores

## T027:C01 — conceito

Combina busca lexical e vetorial para aproveitar correspondência exata e semelhança de significado. BM25 ajuda com siglas, códigos e nomes; vetores podem recuperar paráfrases. Os rankings precisam ser fundidos de forma explícita, pois seus escores geralmente não são comparáveis diretamente.

Como funciona:
- Executar ambos os recuperadores com filtros equivalentes.
- Unificar candidatos por identidade documental.
- Combinar posições, por exemplo por RRF, e opcionalmente reranquear.

## T027:C02 — aplicacao

Quando usar:
- Bases técnicas com códigos exatos e perguntas em linguagem natural.
- Consultas que misturam nomes conhecidos e descrição de problema.

Quando não usar:
- Não chamar uma busca lexical com expansão de sinônimos de híbrida vetorial se nenhum embedding for usado.

Implementação proposta:
- Proposta: versionar analisador lexical, modelo de embedding e parâmetros de fusão.
- Garantir que ambos os lados busquem o mesmo snapshot autorizado.
- Calibrar conjunto de candidatos antes de escolher o top-k final.

Aplicação LAI proposta:
Proposta LAI: manter busca lexical funcional como base e adicionar embeddings quando um modelo de vetorização estiver configurado e avaliado.

## T027:C03 — riscos_validacao

Armadilhas:
- Somar escores sem normalização favorece um recuperador arbitrariamente.
- Filtros diferentes entre índices podem causar vazamento ou inconsistência.

Métricas sugeridas:
- Recall@k e nDCG comparados a cada recuperador sozinho.
- Latência dos dois caminhos e custo do reranker.

Testes propostos:
- Testar códigos raros e paráfrases sem palavras em comum.
- Verificar que documentos expirados não entram por um dos caminhos.

## T027:C04 — perguntas_proveniencia

Pergunta: RRF mistura os valores de BM25 e cosine?
Resposta: Ele usa posições nos rankings, evitando assumir que os escores têm a mesma escala.

Pergunta: Busca híbrida sempre vence?
Resposta: Não. Qualidade de índices, filtros e fusão deve ser medida no conjunto de perguntas do domínio.

Pergunta: Peso igual significa contribuição igual?
Resposta: Não. Escalas, cobertura e distribuição dos scores importam. Mesmo após normalização, pesos iguais não garantem influência semântica equivalente.

Pergunta: Qual canal devo remover se quiser reduzir custo?
Resposta: Meça a evidência exclusiva que cada um recupera nas consultas relevantes. A decisão por média agregada pode prejudicar códigos raros ou linguagem do domínio.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T027:C05 — mecanismo_avancado

A fusão começa antes da soma: ambos os canais precisam usar identidades e filtros compatíveis. Na normalização por conjunto retornado, mudar a quantidade de candidatos altera a escala dos escores, mesmo para um documento cujo score bruto ficou igual. RRF reduz dependência das escalas, mas troca intensidade de relevância por posições e continua sensível à cobertura de cada lista.

Condição de contorno:
Combinar dois rankings que falham nos mesmos documentos pode acrescentar custo sem recall; somar escores não calibrados pode deixar um canal dominar arbitrariamente.

Contrato proposto:
- Entradas: Consulta, índices alinhados, filtros comuns e política de fusão.
- Saídas: Ranking deduplicado com posição e contribuição de cada canal.
- Estado: Versões dos índices, embeddings, pesos ou parâmetros de fusão.
- Invariante: Um documento inelegível não reaparece pela união de um canal com filtros menos restritivos.

Compromissos de projeto:
- Normalização preserva diferenças de score e depende da distribuição de candidatos.
- Fusão por ranking evita comparar escalas diretamente, mas perde informação sobre distância entre posições.

## T027:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: produzir um outlier lexical e variar o tamanho das listas. Conferir se a fusão muda como previsto e se o resultado continua respeitando os filtros em ambos os canais.

Plano de avaliação proposto:
Avaliação proposta: comparar BM25, vetores, RRF e normalização sobre o mesmo corpus. Controlar candidatos e orçamento final; medir recall complementar, qualidade do topo, latência e desempenho por consultas com identificadores e paráfrases.

Comparações:
- T028 (complements): Reranking pode avaliar a união de candidatos depois da fusão.
- T009 (complements): A busca híbrida implementa a etapa de recuperação, sem resolver sozinha o uso da evidência pelo gerador.

Afirmação rastreável:
OpenSearch calcula estatísticas de normalização a partir dos resultados retornados por cada cláusula.
Suporte: direct; fontes: V3A-S022
Limite: A consequência depende da técnica de normalização; não deve ser generalizada a toda fusão híbrida.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T027:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou fusão de escores. Aqui canais recebem orçamento conforme sinais da consulta e são avaliados por contribuição exclusiva.

Projeto e decomposição
Consultas com códigos literais exigem quota lexical protegida. Paráfrases e descrições vagas podem justificar mais candidatos vetoriais. O ajuste deve ocorrer antes de reranking, preservando filtros comuns.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

Controle adaptativo
Registre candidatos encontrados exclusivamente por cada canal. Quando ambos retornam quase o mesmo conjunto, manter duas buscas pode custar mais sem ampliar cobertura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

Validação contrafactual
Compare fusão fixa e orçamento condicionado por intenção com o mesmo número total de candidatos. Separe consultas de identificador, terminologia rara e paráfrase; médias globais podem esconder regressão crítica. Unidade de avaliação: consulta e candidatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

USO AVANÇADO — Suporte de API
Cenário: Usuário fornece erro exato ou descrição livre.
Estratégia: Detectar identificador sem removê-lo, recuperar lexicalmente e complementar semanticamente quando o termo não aparecer. Rerankear conjunto deduplicado.
Papel do modelo pequeno: 3–7B extrai sinais; 8–14B lê candidatos.
Aceite proposto: Exigir recuperação do código exato quando presente no corpus.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

USO AVANÇADO — Pesquisa de decisões
Cenário: O usuário não lembra a formulação original.
Estratégia: Gerar consulta semântica preservando nomes e datas; recuperar também registros literais desses filtros.
Papel do modelo pequeno: 15–30B sintetiza decisões relacionadas.
Aceite proposto: Não confundir decisão de entidade homônima com correspondência válida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, A-S021.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator determinístico assistido de códigos, nomes e datas.
8–14B: Reformulador controlado de intenção para canal vetorial.
15–30B: Integrador de evidências de canais diferentes e conflitos.
Requisitos de treino/runtime: Índices versionados, fusão explícita e métricas por canal; orçamento total deve permanecer comparável.
Não aplicar quando: Um único canal já cobre os casos relevantes com menor custo e sem regressão nas classes raras.

## T027:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C014 — Microsoft / Azure AI Search semantic ranker
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve recurso comercial disponível.
Mecanismo documentado: Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.
Correspondência com esta base: Documenta canal híbrido com RRF como entrada elegível.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.
Limite: Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q020.

## T027:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T027 → T028 [feeds]
Como combinar: Rerankear união deduplicada dos canais.
Interface: document_id, posições lexicais/vetoriais e filtros.
Condição: Candidatos elegíveis e versões compatíveis.
Aceite proposto: Medir ganho de ranking sem perder candidatos exclusivos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, A-S021. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T027 → T036 [complements]
Como combinar: Preservar identificadores na reformulação.
Interface: Consulta original, termos protegidos e expansão.
Condição: Expansão não substituir requisito literal.
Aceite proposto: Testar códigos parecidos e nomes com acentos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, A-S021. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não somar escores heterogêneos sem regra validada.
- Não remover candidato raro só por aparecer em um canal.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar cobertura e evidência final com contexto equivalente; recuperação forte não garante leitura correta.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T028, T036

## Fontes primárias associadas

### A-S021 — Reciprocal rank fusion

[https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação por posições de múltiplos rankings, incluindo busca lexical e vetorial.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S022 — Normalization processor

[https://docs.opensearch.org/latest/search-plugins/search-pipelines/normalization-processor/](https://docs.opensearch.org/latest/search-plugins/search-pipelines/normalization-processor/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Normalização e combinação de scores; estatísticas calculadas sobre candidatos retornados e sensibilidade ao tamanho desse conjunto.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S026 — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models

[https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Generalização entre domínios e comparação de recuperadores lexicais, densos e reranking com custos distintos.

Limite: Consultados resumo e conclusões gerais de avaliação; perguntas e gabaritos do benchmark não foram consultados. Comparações publicadas não se transferem automaticamente a modelos atuais.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T028 — Reranking

**Nome canônico:** Reranking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T028  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** reordenação de resultados; cross-encoder reranking

## T028:C01 — conceito

Reordena um conjunto inicial de candidatos com um avaliador mais caro ou específico. Um cross-encoder considera consulta e trecho conjuntamente. O reranker melhora seleção dentro dos candidatos disponíveis; não recupera um documento que a primeira etapa nunca encontrou.

Como funciona:
- Recuperar um conjunto amplo com busca eficiente.
- Pontuar pares consulta-trecho com o reranker.
- Selecionar evidências relevantes e diversas dentro do orçamento.

## T028:C02 — aplicacao

Quando usar:
- Busca inicial retorna muitos trechos aparentemente próximos.
- Perguntas dependem de distinções finas entre conceitos semelhantes.

Quando não usar:
- Não adicionar reranker antes de resolver recall insuficiente ou fontes ausentes.

Implementação proposta:
- Proposta: escolher modelo compatível com idioma e comprimento dos trechos.
- Manter consulta e documento sem truncar o detalhe decisivo.
- Comparar precisão final com e sem reranking e registrar os documentos descartados.

Aplicação LAI proposta:
Proposta LAI: usar para distinguir técnicas com nomes próximos, como compressão textual e destilação paramétrica, após garantir que ambas são recuperáveis.

## T028:C03 — riscos_validacao

Armadilhas:
- Reranker treinado em outro domínio pode preferir textos genéricos.
- Scores altos não certificam verdade, validade temporal ou permissão de acesso.

Métricas sugeridas:
- nDCG, MRR e precisão dos trechos usados na resposta.
- Latência por par e total por consulta.

Testes propostos:
- Colocar documento correto fora dos candidatos e confirmar a limitação.
- Testar duas definições parecidas que diferem por modificar ou não os pesos.

## T028:C04 — perguntas_proveniencia

Pergunta: Reranking é geração de resposta?
Resposta: Não. É seleção e ordenação de evidências antes ou durante a montagem do contexto.

Pergunta: O primeiro resultado deve ser tratado como verdadeiro?
Resposta: Não. Relevância e verdade são dimensões diferentes; a fonte e a evidência ainda precisam ser avaliadas.

Pergunta: Posso excluir um candidato por score abaixo de um valor copiado?
Resposta: Somente após calibrar o uso desse score no modelo e domínio. Escalas de rerankers diferentes não são intercambiáveis.

Pergunta: Uma passagem bem ranqueada basta para citar uma conclusão?
Resposta: Não. Relevância e sustentação são diferentes; a conclusão precisa ser conferida contra o conteúdo e suas condições.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T028:C05 — mecanismo_avancado

O teto do reranker é determinado pelos candidatos recebidos. Separar recall da primeira etapa e qualidade da ordenação evita culpar o avaliador por um documento ausente. Também é necessário conhecer o truncamento interno de consulta e passagem: um classificador pode receber apenas o início do trecho, atribuindo score sem observar a parte que contém a evidência decisiva.

Condição de contorno:
O estágio não ajuda quando a evidência relevante está fora do conjunto candidato ou quando seu custo consome o prazo disponível sem melhorar a seleção final.

Contrato proposto:
- Entradas: Consulta, candidatos identificados e limite efetivo do modelo de ranking.
- Saídas: Ordem revisada e scores associados às versões originais.
- Estado: Modelo, configuração de truncamento, candidatos iniciais e seleção final.
- Invariante: Score de relevância não é apresentado como probabilidade calibrada de verdade ou suporte lógico.

Compromissos de projeto:
- Mais candidatos elevam o teto de recall e o trabalho de avaliação.
- Modelos conjuntos capturam interação consulta-texto, mas são mais caros que comparar vetores pré-computados.

## T028:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar a evidência relevante no fim de uma passagem longa e depois fora do conjunto candidato. O diagnóstico deve distinguir truncamento do reranker de falha de recuperação inicial.

Plano de avaliação proposto:
Avaliação proposta: usar a mesma lista para comparar ordenação original e reranking, e depois variar sua cobertura. Medir ranking, suporte das passagens selecionadas, duração e custo; incluir uma ordenação ideal dos candidatos para estimar o teto disponível.

Comparações:
- T027 (complements): A união híbrida pode aumentar a diversidade de candidatos oferecida ao reranker.
- T037 (distinct_from): Reranking ordena unidades; compressão condicionada à pergunta modifica a representação enviada.

Afirmação rastreável:
O trabalho de Nogueira e Cho aplica BERT à reordenação de passagens em função da consulta.
Suporte: direct; fontes: V3A-S025
Limite: A técnica publicada é uma implementação específica; modelos atuais têm outros limites e distribuições de scores.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T028:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrou teto de candidatos e truncamento. Aqui reranking ganha comparação em pares difíceis e decisão de parada por utilidade marginal.

Projeto e decomposição
Separe relevância temática de capacidade de sustentar resposta. Um texto sobre o assunto pode não conter a condição pedida; rótulos de treino e validação precisam refletir suporte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

Controle adaptativo
Use segunda rodada apenas quando os melhores candidatos forem redundantes ou contraditórios. O orçamento deve priorizar diversidade de evidência, preservando versões e documentos de autoridade necessária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

Validação contrafactual
Compare cross-encoder, julgamento pequeno por pares e ranking original. Meça posição da primeira evidência suficiente, diversidade útil e latência por tamanho de lista; incluir documentos longos que excedem entrada do reranker. Unidade de avaliação: lista de candidatos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

USO AVANÇADO — Pergunta com exceção
Cenário: Resultados populares omitem condição rara.
Estratégia: Rerankear pelo requisito completo e manter candidato que contém a exceção mesmo com menor similaridade global.
Papel do modelo pequeno: 3–7B julga suporte binário em trechos.
Aceite proposto: Exceção deve chegar ao leitor em consultas que a exigem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

USO AVANÇADO — Contradições de versão
Cenário: Dois documentos parecem igualmente relevantes.
Estratégia: Aplicar elegibilidade temporal antes de relevância; sinalizar conflito quando ambos forem válidos em escopos diferentes.
Papel do modelo pequeno: 8–14B explica distinção de escopo.
Aceite proposto: Não promover documento obsoleto por linguagem mais parecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S009, V3A-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de suporte em pares curtos, preferencialmente especializado.
8–14B: Reranker de listas pequenas com justificativa vinculada a trecho.
15–30B: Revisor de candidatos conflitantes, usado somente em listas difíceis.
Requisitos de treino/runtime: Candidatos com evidência rotulada e tamanho real de entrada; considerar modelos menores que 3B quando suficientes.
Não aplicar quando: A evidência correta está fora do conjunto inicial ou o custo de julgamento supera benefício.

## T028:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C008 — Microsoft / Bing: transformers na busca global
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Operador afirma modelos transformer aplicados às consultas Bing globais no período descrito.
Mecanismo documentado: Compreensão contextual de consultas e páginas com inferência otimizada.
Correspondência com esta base: Ranking neural é relacionado; fonte não especifica integralmente o pipeline desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Empregar modelo compacto para julgar pares consulta-trecho, medindo custo e ordenação.
Limite: BERT destilado do relato não é um gerador 3–30B; números de infraestrutura não são transportáveis. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S008.

V4A-C014 — Microsoft / Azure AI Search semantic ranker
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve recurso comercial disponível.
Mecanismo documentado: Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.
Correspondência com esta base: Segundo ranking explícito.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.
Limite: Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q016.

## T028:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T028 → T027 [requires]
Como combinar: Receber candidatos diversos antes de reordenar.
Interface: União de resultados e proveniência de cada canal.
Condição: Filtros aplicados de maneira consistente.
Aceite proposto: Testar recuperação da evidência antes de atribuir erro ao reranker.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T028 → T037 [feeds]
Como combinar: Comprimir depois de selecionar suporte.
Interface: Trechos selecionados e requisitos da pergunta.
Condição: Compressão preservar evidência que justificou posição.
Aceite proposto: Comparar decisão com trecho integral e comprimido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S009, V3A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar score de ranking como verdade.
- Não avaliar somente documentos que o próprio reranker selecionou.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar suporte entregue ao leitor e custo por pergunta; qualidade de ranking não equivale à qualidade de raciocínio geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T027, T036, T198

## Fontes primárias associadas

### A-S020 — Retrieve & Re-Rank

[https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recuperação inicial seguida de pontuação conjunta consulta-documento por cross-encoder.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S025 — Passage Re-ranking with BERT

[https://arxiv.org/abs/1901.04085](https://arxiv.org/abs/1901.04085)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de BERT para reordenar passagens em função da consulta, como estágio específico de recuperação.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S026 — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models

[https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Generalização entre domínios e comparação de recuperadores lexicais, densos e reranking com custos distintos.

Limite: Consultados resumo e conclusões gerais de avaliação; perguntas e gabaritos do benchmark não foram consultados. Comparações publicadas não se transferem automaticamente a modelos atuais.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S008 — Bing delivers its largest improvement in search experience using Azure GPUs

[https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/](https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos transformer aplicados às consultas Bing; inferência otimizada e compreensão da consulta.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T029 — GraphRAG

**Nome canônico:** GraphRAG  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T029  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** graph-based RAG; RAG com grafos

## T029:C01 — conceito

Família de RAG apoiado em grafos e, neste inventário, também referência à implementação da Microsoft. Essa implementação extrai entidades e relações, organiza comunidades e produz resumos para diferentes modos de consulta. O grafo organiza relações; uma aresta extraída por LLM não é automaticamente um fato comprovado.

Como funciona:
- Extrair entidades e relações ligadas aos trechos de origem.
- Organizar grafo e resumos de comunidades conforme o método escolhido.
- Consultar relações locais ou temas globais e recuperar evidência.

## T029:C02 — aplicacao

Quando usar:
- Perguntas sobre dependências e relações entre documentos.
- Sínteses globais que trechos isolados cobrem mal.

Quando não usar:
- Pode ser custo desnecessário para perguntas factuais simples respondidas por poucos trechos.

Implementação proposta:
- Proposta: definir identidade de entidades antes da extração.
- Separar arestas extraídas, verificadas e inferidas.
- Medir custo de indexação e atualização, além da qualidade da resposta, contra RAG plano.

Aplicação LAI proposta:
Proposta LAI: experimentar com contratos e dependências entre softwares; manter trechos de código e documentação como base de verificação das arestas.

## T029:C03 — riscos_validacao

Armadilhas:
- Resolver duas entidades distintas como uma contamina muitas consultas.
- Erros de extração podem se propagar para resumos de comunidades.

Métricas sugeridas:
- Precisão de entidades e relações com evidência.
- Qualidade de perguntas relacionais e custo por atualização.

Testes propostos:
- Criar duas APIs com o mesmo nome em softwares distintos e manter identidades separadas.
- Retirar a evidência de uma relação e exigir invalidação ou marcação de incerteza.

## T029:C04 — perguntas_proveniencia

Pergunta: Qualquer banco de grafos é GraphRAG?
Resposta: Não. É necessário um processo de recuperação que use o grafo para fundamentar a geração.

Pergunta: GraphRAG substitui busca lexical?
Resposta: Não obrigatoriamente. Muitas arquiteturas combinam os mecanismos conforme a pergunta.

Pergunta: Mais arestas significam mais conhecimento confiável?
Resposta: Não. Também podem significar mais duplicatas e associações erradas. A qualidade precisa considerar identidade, proveniência e precisão das relações.

Pergunta: Como atualizar um documento alterado?
Resposta: Identifique suas contribuições e regenere estruturas dependentes conforme o pipeline. Manter relatórios antigos com fatos novos exige marcação explícita ou reconstrução consistente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T029:C05 — mecanismo_avancado

Na implementação Microsoft, busca global e local usam materiais diferentes: relatórios de comunidades favorecem síntese do corpus; entidades, relações e trechos originais favorecem investigação localizada. A escolha do modo é parte da consulta. Erros de resolução de entidades, como unir homônimos, propagam-se para relações e relatórios, multiplicando a aparência de suporte de um fato incorreto.

Condição de contorno:
Grafos pouco conectados, extração imprecisa ou perguntas predominantemente literais podem não justificar o custo de construir e atualizar comunidades e resumos.

Contrato proposto:
- Entradas: Documentos versionados, esquema de entidades e modo de consulta definido.
- Saídas: Resposta com referências às fontes e distinção entre extração e síntese.
- Estado: Grafo, relatórios, mapeamento para trechos e versão da ingestão.
- Invariante: Uma relação extraída não ganha confirmação independente por aparecer também num relatório gerado dela.

Compromissos de projeto:
- Relatórios globais ampliam cobertura temática, mas acumulam decisões de síntese.
- Expansão local preserva detalhe e pode perder relações distantes que não entraram no subgrafo.

## T029:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir duas entidades homônimas com relações incompatíveis. Verificar se a resolução evita fusão ou mantém ambiguidade, sem produzir um perfil híbrido inexistente.

Plano de avaliação proposto:
Avaliação proposta: comparar busca textual, modo local e global em tarefas correspondentes. Controlar corpus e orçamento; medir suporte das relações, cobertura temática, custo de ingestão e atualização, além da qualidade final.

Comparações:
- T051 (complements): Memória em grafo pode compartilhar entidades, mas GraphRAG acrescenta um pipeline de recuperação e geração.
- T057 (distinct_from): Relações do grafo não identificam causalidade sem hipóteses e evidências causais adicionais.

Afirmação rastreável:
GraphRAG documenta busca global com relatórios de comunidades e busca local combinando grafo e texto original.
Suporte: direct; fontes: V3A-S023, V3A-S024
Limite: As capacidades descritas não garantem correção das extrações nem ganho em toda classe de pergunta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T029:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou consultas locais e globais. Aqui o grafo distingue camadas de evidência, hipótese e decisão para evitar propagação indevida.

Projeto e decomposição
Crie arestas tipadas por natureza: relação declarada, inferência extraída e hipótese analítica. Não permita que comunidades resumidas tratem todas como observações equivalentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

Controle adaptativo
Propague proveniência por caminho e limite profundidade por utilidade. Um caminho longo com cada elo plausível pode produzir conclusão que nenhuma fonte sustenta; composição exige teste próprio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

Validação contrafactual
Compare busca textual, grafo factual e grafo com hipóteses separadas. Meça identidade correta, suporte de caminhos e afirmações novas indevidamente apresentadas como fatos. Unidade de avaliação: subgrafo consultado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

USO AVANÇADO — Dependências de produto
Cenário: Documentos descrevem componentes e responsáveis.
Estratégia: Extrair relações explícitas, resolver identidade e consultar impacto por caminho. Validar cada salto antes de recomendar mudança.
Papel do modelo pequeno: 3–7B extrai; 15–30B explica impacto.
Aceite proposto: Nenhum impacto obrigatório pode depender de aresta sem fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

USO AVANÇADO — Panorama de controvérsias
Cenário: Fontes discordam sobre relações.
Estratégia: Agrupar posições por origem e gerar resumo de comunidades mantendo arestas incompatíveis separadas.
Papel do modelo pequeno: 8–14B resume posições locais.
Aceite proposto: Preservar desacordo e independência das fontes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S024, V3A-S023, V3A-S024.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de relações em ontologia pequena com opção desconhecido.
8–14B: Resumidor de comunidade já validada por identidade.
15–30B: Leitor de caminhos e controvérsias, sem inferir causalidade por conectividade.
Requisitos de treino/runtime: Ontologia, resolução de entidades e estados de evidência; orçamento de extração e atualização pode dominar consulta.
Não aplicar quando: Relações são instáveis ou pouco confiáveis e o grafo amplifica erros de extração.

## T029:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C024 — Microsoft Research / Project GraphRAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto de pesquisa publica combinação de extração, análise de redes e geração.
Mecanismo documentado: Grafo derivado de texto e resumos sustentam consulta em diferentes níveis.
Correspondência com esta base: Trabalho específico GraphRAG.
Transferência proposta para modelo pequeno: Proposta de engenharia: Extrair entidades com modelo pequeno e auditar amostra antes de resumir comunidades.
Limite: Projeto/README não prova implantação bigtech; densidade de grafo não equivale a qualidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S024, A-S024.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q015, V4A-Q021.

## T029:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T029 → T051 [complements]
Como combinar: Persistir relações com tipo epistemológico e origem.
Interface: Entidades, aresta, fonte e status de evidência.
Condição: Grafo separar inferência de observação.
Aceite proposto: Inserir hipótese e impedir promoção automática a fato.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S024, V3A-S023, V3A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T029 → T057 [conflicts]
Como combinar: Impedir leitura causal de simples conexão.
Interface: Caminho associativo e hipótese causal separada.
Condição: Não existir identificação causal independente.
Aceite proposto: Testar pergunta causal e exigir pressupostos explícitos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S024, V3A-S023, V3A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar centralidade como medida de verdade.
- Evitar contar derivados da mesma origem como corroboradores independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar perguntas relacionais específicas; um grafo maior pode apenas multiplicar conexões espúrias.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T051, T077

## Fontes primárias associadas

### A-S024 — Welcome to GraphRAG

[https://microsoft.github.io/graphrag/](https://microsoft.github.io/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Extração de grafo, hierarquia de comunidades, resumos e consultas estruturadas.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S023 — GraphRAG Global Search

[https://microsoft.github.io/graphrag/query/global_search/](https://microsoft.github.io/graphrag/query/global_search/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Consulta global por relatórios de comunidades com map-reduce; efeito do nível de comunidade no custo e detalhe.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S024 — GraphRAG Local Search

[https://microsoft.github.io/graphrag/query/local_search/](https://microsoft.github.io/graphrag/query/local_search/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de entidades, relações, relatórios e trechos originais para consultas locais.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T030 — RAPTOR

**Nome canônico:** RAPTOR  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T030  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Recursive Abstractive Processing for Tree-Organized Retrieval

## T030:C01 — conceito

RAPTOR significa Recursive Abstractive Processing for Tree-Organized Retrieval. O método constrói representações em vários níveis por embeddings, agrupamento e resumos recursivos, e recupera material dessa estrutura. Foi proposto para ampliar a visão de documentos além de pequenos trechos contíguos.

Como funciona:
- Criar trechos e embeddings dos documentos.
- Agrupar e sintetizar repetidamente formando níveis de abstração.
- Buscar informação relevante entre os nós da árvore.

## T030:C02 — aplicacao

Quando usar:
- Perguntas temáticas sobre documentos extensos.
- Consultas que combinam detalhe e visão geral.

Quando não usar:
- Não assumir vantagem para dados transacionais de alta frequência sem avaliar custo de reconstrução.

Implementação proposta:
- Proposta: preservar folhas originais e ligações de cada resumo aos filhos.
- Versionar agrupamento, embedder e gerador de resumos.
- Comparar com RAG plano sob o mesmo modelo de resposta e conjunto de perguntas.

Aplicação LAI proposta:
Proposta LAI: avaliar sobre bases teóricas extensas e manuais; não tratar o nome RAPTOR como garantia de ganho na configuração local.

## T030:C03 — riscos_validacao

Armadilhas:
- Resumos podem omitir exceções ou introduzir relações indevidas.
- Atualizações no corpus podem exigir revisar agrupamentos e ancestrais.

Métricas sugeridas:
- Correção de perguntas globais e pontuais.
- Custo de construção, atualização e tokens recuperados.

Testes propostos:
- Exigir evidência original para afirmações vindas de nós de resumo.
- Medir comportamento após alteração de um documento, sem aceitar resumo antigo como atual.

## T030:C04 — perguntas_proveniencia

Pergunta: RAPTOR muda os pesos da LLM?
Resposta: A estrutura de recuperação não exige, por si só, retreinar o gerador.

Pergunta: Basta uma pasta com resumos para ter RAPTOR?
Resposta: Não. É preciso implementar e registrar o processo específico de agrupamento, níveis e recuperação ou declarar que é apenas inspirado nele.

Pergunta: BIC escolhe o melhor número de grupos para responder perguntas?
Resposta: Não diretamente. Ele avalia um critério estatístico do modelo de mistura, não a utilidade downstream de cada agrupamento.

Pergunta: Posso trocar o embedding sem reconstruir a estrutura?
Resposta: Isso pode tornar representações e grupos incompatíveis. A migração deve incluir nova indexação e validação, preservando a versão anterior para comparação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T030:C05 — mecanismo_avancado

O código consultado reduz dimensionalidade com UMAP e usa misturas gaussianas, selecionando número de componentes por BIC. A associação por probabilidades acima de um limiar permite que um trecho pertença a mais de um grupo. Consequentemente, a estrutura chamada árvore não deve ser interpretada como partição necessariamente disjunta; duplicação de origens precisa ser considerada na recuperação e síntese.

Condição de contorno:
Agrupamento de poucos pontos, embeddings inadequados ou textos altamente heterogêneos podem produzir grupos frágeis, independentemente da qualidade do sumarizador.

Contrato proposto:
- Entradas: Chunks, embeddings compatíveis, configuração de agrupamento e sumarização.
- Saídas: Representações em níveis e referências aos trechos que sustentam cada nó.
- Estado: Versões dos modelos, seeds, configurações e relações de pertencimento.
- Invariante: Múltiplos caminhos até a mesma origem não contam como confirmações independentes.

Compromissos de projeto:
- Pertencimento múltiplo preserva temas transversais, mas aumenta redundância e custo de resumos.
- Redução dimensional torna agrupamento viável e pode alterar vizinhanças relevantes para consultas específicas.

## T030:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir um trecho que conecte dois temas e rastrear sua presença em resumos diferentes. A resposta deve evitar duplicar contagens e continuar permitindo acesso à mesma origem.

Plano de avaliação proposto:
Avaliação proposta: comparar folhas, resumos em níveis e conjunto combinado com orçamento idêntico. Variar agrupamento e resumidor; medir estabilidade, recuperação de detalhes e temas, custo de ingestão e redundância de evidências.

Comparações:
- T023 (specializes): RAPTOR implementa uma hierarquia recursiva com escolha específica de agrupamento e recuperação.
- T029 (alternative): GraphRAG organiza entidades e comunidades; RAPTOR agrupa representações de texto para produzir resumos.

Afirmação rastreável:
O código oficial usa probabilidades de GaussianMixture acima de limiar para atribuir grupos.
Suporte: direct; fontes: V3A-S029
Limite: Foi realizada leitura de código, sem execução; detalhes podem mudar em outras revisões do repositório.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T030:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhou clustering do RAPTOR. Aqui o foco é atualização de árvores e controle do custo de sobreposição entre clusters.

Projeto e decomposição
A participação de uma folha em vários clusters melhora rotas possíveis, mas também multiplica sínteses e dependências de atualização. Registre grau de participação por documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

Controle adaptativo
Após alteração de folha, escolha entre atualização local e reconstrução segundo mudança de vizinhança. Reusar resumos quando a composição do cluster mudou pode conservar uma interpretação inválida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

Validação contrafactual
Compare índice original, atualização local e reconstrução completa em corpus editado. Meça cobertura, custo de regeneração e duplicação de evidência no contexto final, mantendo consultas reservadas. Unidade de avaliação: coleção resumida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

USO AVANÇADO — Base técnica em evolução
Cenário: Poucos documentos mudam por semana.
Estratégia: Marcar resumos dependentes, recalcular clusters afetados e publicar revisão completa somente após validar ligações às folhas.
Papel do modelo pequeno: 3–7B extrai mudanças; 8–14B resume clusters.
Aceite proposto: Consulta não pode misturar resumo antigo e folha nova sem indicação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

USO AVANÇADO — Perguntas de síntese
Cenário: Resposta exige vários níveis de abstração.
Estratégia: Recuperar resumos para orientação e folhas para afirmações precisas; deduplicar folhas alcançadas por caminhos diferentes.
Papel do modelo pequeno: 15–30B integra níveis.
Aceite proposto: Cada detalhe factual deve apontar à folha original.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S014, V3A-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de atributos e verificador de cobertura das folhas.
8–14B: Resumidor de grupos pequenos, com limites de tamanho e conteúdo.
15–30B: Integrador de múltiplos níveis quando síntese realmente exigir abstração.
Requisitos de treino/runtime: Implementação RAPTOR compatível, vínculos muitos-para-muitos e versionamento de clusters; não substituir por árvore genérica.
Não aplicar quando: Atualizações frequentes fazem reconstrução dominar custo ou resumos não melhoram tarefas do acervo.

## T030:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q021.

## T030:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T030 → T072 [requires]
Como combinar: Publicar uma revisão coerente de folhas e resumos.
Interface: Manifesto de clusters, versões e dependências.
Condição: Consulta pinada a revisão consistente.
Aceite proposto: Testar leitura durante troca de índice.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S014, V3A-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T030 → T032 [alternative]
Como combinar: Preferir pais documentais quando hierarquia natural basta.
Interface: Documento, filho e pai estrutural.
Condição: Estrutura documental conservar contexto necessário.
Aceite proposto: Comparar custo e qualidade com agrupamento aprendido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S014, V3A-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar mesma folha várias vezes como evidência adicional.
- Não chamar configuração diferente de clustering de reprodução exata.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar questões de abstração e detalhe separadamente; ganhos relatados do RAPTOR não garantem ganhos com leitores pequenos.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T008, T023, T026

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S029 — RAPTOR cluster_utils.py

[https://github.com/parthsarthi03/raptor/blob/master/raptor/cluster_utils.py](https://github.com/parthsarthi03/raptor/blob/master/raptor/cluster_utils.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: UMAP, GaussianMixture, seleção por BIC e associação por probabilidades acima de limiar; leitura do código, sem execução.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V3A-S011 — RAPTOR: official implementation

[https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore recuperável, serialização e interfaces de sumarização, embeddings e resposta. Código de pesquisa não instalado.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T031 — Semantic Cache Invalidation

**Nome canônico:** Semantic Cache Invalidation  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T031  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** invalidação de cache semântico

## T031:C01 — conceito

Define quando uma resposta reutilizável por similaridade deixa de ser válida. A proximidade semântica da pergunta pode permanecer alta enquanto fontes, políticas ou contexto mudam. Por isso, expiração e dependências são condições adicionais à busca vetorial.

Como funciona:
- Registrar fontes e versões usadas em cada resposta cacheada.
- Detectar alteração, expiração ou mudança de escopo.
- Remover ou tornar inelegíveis entradas afetadas antes da próxima reutilização.

## T031:C02 — aplicacao

Quando usar:
- FAQs cuja documentação é atualizada.
- Caches de consultas condicionadas a versão de produto ou contrato.

Quando não usar:
- Não depender somente de TTL quando uma mudança exige invalidação imediata.

Implementação proposta:
- Proposta: manter vetor de dependências ou geração do índice na entrada.
- Combinar expiração temporal com invalidação por evento.
- Em caso de falha na propagação, preferir recomputar a resposta a servir uma entrada de validade desconhecida.

Aplicação LAI proposta:
Proposta LAI: vincular respostas técnicas a hashes de contratos e snapshots de repositórios; decisões comerciais mutáveis não devem depender só de similaridade.

## T031:C03 — riscos_validacao

Armadilhas:
- Invalidação parcial pode deixar respostas antigas em réplicas.
- A mesma pergunta pode mudar de resposta por contexto não registrado na dependência.

Métricas sugeridas:
- Tempo entre mudança da fonte e rejeição do cache.
- Taxa de respostas obsoletas e recomputações desnecessárias.

Testes propostos:
- Atualizar uma regra e consultar uma paráfrase da pergunta antiga.
- Simular atraso no evento de invalidação e exigir checagem de versão.

## T031:C04 — perguntas_proveniencia

Pergunta: Um TTL curto resolve tudo?
Resposta: Não. Ainda existe uma janela de obsolescência e TTL curto pode anular a economia do cache.

Pergunta: Preciso refazer todos os embeddings após mudar uma resposta?
Resposta: Não necessariamente. A política deve distinguir atualização de resposta, metadados e representação vetorial.

Pergunta: Um cache negativo pode ser reutilizado?
Resposta: Somente se a ausência observada tiver escopo e validade definidos. Falha de recuperação ou indisponibilidade não equivale a inexistência do fato.

Pergunta: Como tratar uma entrada acessada durante invalidação?
Resposta: Defina o contrato de consistência. Para exigência forte, verifique versão ou época no caminho de leitura; apenas apagar em segundo plano deixa uma janela de reutilização.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T031:C05 — mecanismo_avancado

Uma resposta pode ficar inválida por mudança na fonte, no direito de acesso, na política ou no modelo de interpretação. TTL limita idade, mas não acompanha necessariamente essas mudanças. Um desenho por dependências registra quais revisões sustentam cada entrada e verifica sua elegibilidade no hit; invalidação por evento e expiração podem coexistir como controles de problemas diferentes.

Condição de contorno:
Se não é possível identificar dependências ou sua versão vigente, o cache não pode prometer atualização imediata somente ajustando o limiar semântico.

Contrato proposto:
- Entradas: Entrada candidata, revisões das dependências e contexto atual de acesso.
- Saídas: Decisão de servir, revalidar ou remover a entrada, com motivo.
- Estado: Índice de dependências, época de política e prazo de retenção.
- Invariante: Um hit semelhante não ignora revogação ou revisão incompatível conhecida no momento da leitura.

Compromissos de projeto:
- Invalidação precisa exige metadados e coordenação entre serviços.
- Expiração ampla simplifica operação, mas provoca misses e ainda permite obsolescência até o vencimento.

## T031:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: armazenar uma resposta e corrigir a fonte antes de vencer o TTL. A próxima consulta equivalente deve rejeitar ou revalidar a entrada, sem esperar a expiração para reconhecer a correção.

Plano de avaliação proposto:
Avaliação proposta: comparar TTL isolado, versão por namespace e dependências explícitas. Variar frequência de mudanças e reutilização; medir respostas obsoletas, tempo de propagação, misses evitáveis e custo de revalidação.

Comparações:
- T005 (complements): A invalidação decide elegibilidade; a similaridade só localiza uma resposta candidata.
- T072 (complements): Versões de memória e fonte permitem detectar dependências incompatíveis.

Afirmação rastreável:
RedisVL oferece controles separados de TTL, filtros e exclusão de entradas de cache.
Suporte: direct; fontes: V3A-S007
Limite: A rastreabilidade das dependências e sua propagação são responsabilidades adicionais da aplicação.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T031:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 diferenciou TTL e invalidação. Aqui a estratégia usa granularidade de dependências e prazo de frescor observável por resposta.

Projeto e decomposição
Associe cada resposta às entidades, fontes e versões que poderiam alterá-la. Dependência apenas no documento inteiro provoca invalidação excessiva; dependência estreita demais deixa resposta antiga ativa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

Controle adaptativo
Defina frescor por classe de dado e meça atraso entre correção confirmada e último hit obsoleto. A verificação deve consultar o caminho visto pelo cliente, incluindo réplicas e índices.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

Validação contrafactual
Compare invalidação por documento, por entidade e TTL. Injete atualização e preenchimento atrasado para medir sobrevivência indevida; hit rate não é métrica de consistência. Unidade de avaliação: resposta derivada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

USO AVANÇADO — FAQ com políticas alteradas
Cenário: Uma cláusula muda várias respostas.
Estratégia: Publicar nova revisão, revogar respostas dependentes e verificar réplicas antes de liberar reutilização para cláusula sensível.
Papel do modelo pequeno: 3–7B identifica candidatos afetados; código confirma vínculos.
Aceite proposto: Nenhum hit antigo após o prazo de frescor definido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

USO AVANÇADO — Cache de busca derivada
Cenário: Índice recebe correções assíncronas.
Estratégia: Marcar resultados por revisão da projeção e desviar consultas sensíveis para origem quando o atraso exceder o limite.
Papel do modelo pequeno: 8–14B responde com evidência elegível.
Aceite proposto: Resposta deve informar insuficiência em vez de citar projeção revogada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S011, V4A-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de entidades para construir dependências candidatas.
8–14B: Revisor de alcance semântico de uma alteração e seus efeitos.
15–30B: Analista de conflitos entre versões quando regras de invalidação não bastarem.
Requisitos de treino/runtime: Eventos de atualização, versões monotônicas por objeto e monitoramento do caminho de leitura; LLM não controla sozinho a coerência.
Não aplicar quando: Não é possível saber a origem da resposta ou detectar atualizações relevantes.

## T031:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C010 — Meta / TAO e observabilidade Polaris
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: sistema de dados distribuído; transferência para LLM é proposta.
Uso observado: Meta descreve caches operados e monitoramento de inconsistências observáveis pelo cliente.
Mecanismo documentado: Invalidações e preenchimentos concorrem; verificações em diferentes tempos identificam divergências.
Correspondência com esta base: Invalidação de cache convencional, não proximidade semântica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Monitorar respostas derivadas após correções, incluindo eventos atrasados e evicção de versões.
Limite: Não transferir percentuais de consistência a caches RAG; uma única implantação não vira vários casos. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S011.

V4A-C017 — Microsoft / API Management semantic response cache
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Política disponível busca respostas em cache externo por proximidade.
Mecanismo documentado: Embedding, limiar e particionamento de cache por expressões.
Correspondência com esta base: Particionamento protege escopo, mas política de invalidação completa é desenho adicional.
Transferência proposta para modelo pequeno: Proposta de engenharia: Aceitar somente domínio estável e validar pares quase iguais com entidades ou negações diferentes.
Limite: Não comprova implantação nem taxa de falsos acertos; limiares do serviço não são probabilidades. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q004, V4A-Q007, V4A-Q012.

## T031:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T031 → T007 [requires]
Como combinar: Guardar dependências junto ao item cacheado.
Interface: Chave, origem, revisão e estado de revogação.
Condição: Admissão ocorrer com proveniência completa.
Aceite proposto: Alterar entidade e localizar todos os itens afetados.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S011, V4A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T031 → T075 [complements]
Como combinar: Reconciliar preenchimento atrasado com versão atual.
Interface: Versão observada, versão vigente e operação pendente.
Condição: Regra impedir regressão de versão.
Aceite proposto: Reproduzir chegada de valor antigo após invalidar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S011, V4A-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apagar a única informação de versão durante evicção.
- Não interpretar ausência temporária como exclusão definitiva.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar exposição a resposta obsoleta; modelos maiores também erram quando recebem cache inconsistente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T005, T007, T072

## Fontes primárias associadas

### A-S005 — LLM Caching

[https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/](https://redis.io/docs/latest/develop/ai/redisvl/0.10.0/user_guide/llmcache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico com embeddings, limiar de distância, TTL e filtros de acesso.

Limite: Documentação consultada da versão 0.10.0, não afirma ser a versão corrente do pacote.

### V3A-S007 — RedisVL LLM Cache API

[https://redis.io/docs/latest/develop/ai/redisvl/api/cache/](https://redis.io/docs/latest/develop/ai/redisvl/api/cache/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: SemanticCache com filtros, distância, vetorizador e TTL; diferenças de capacidades entre implementações.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S011 — Cache made consistent

[https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: TAO em produção; corridas entre preenchimento e invalidação; observabilidade Polaris.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S016 — Get cached responses of large language model API requests

[https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy](https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Cache semântico por proximidade vetorial, limiar e particionamento vary-by.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T032 — Parent-Child Retrieval / Parent-Child Chunking

**Nome canônico:** Parent-Child Chunking e Parent-Child Retrieval  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T032  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Parent-Child Retrieval; recuperação pai-filho; Parent-Child Chunking; segmentação pai-filho

## T032:C01 — conceito

Parent-Child Chunking cria unidades grandes de contexto e trechos filhos menores para indexação. Parent-Child Retrieval usa os filhos encontrados para recuperar os pais correspondentes. São etapas complementares de preparação e consulta, não nomes de um método de treinamento. O objetivo é localizar passagens específicas sem perder definições, exceções e relações presentes no entorno.

Como funciona:
- Dividir o documento em pais coerentes, como seções; dividir cada pai em filhos com vínculo estável.
- Indexar representações dos filhos e guardar o texto integral dos pais em armazenamento endereçável.
- Na consulta, localizar filhos, resolver parent_id, deduplicar pais e selecionar expansões compatíveis com o orçamento.

## T032:C02 — aplicacao

Quando usar:
- Manuais, contratos e documentos técnicos nos quais uma frase responde à busca, mas sua interpretação exige a seção correspondente.

Quando não usar:
- Quando documentos já são curtos ou os pais incluem grandes blocos irrelevantes que tornam a expansão mais prejudicial que útil.

Implementação proposta:
- Proposta: registrar document_id, version_id, parent_id, child_id, offsets e namespace; um pai pode ser uma seção, não obrigatoriamente o arquivo inteiro.
- Dimensionar filhos pela precisão da busca e pais pela suficiência contextual, avaliando perguntas reais; não presumir um tamanho universal.
- Manter o filho que originou o resultado para destacar a evidência e aplicar as mesmas permissões ao filho e ao pai.
- Reindexar vínculos quando mudar a segmentação ou a versão, removendo referências órfãs antes da publicação do índice.

Aplicação LAI proposta:
Proposta LAI: usar módulos ou seções como pais e preservar os trechos filhos que justificaram sua inclusão no contexto de programação.

## T032:C03 — riscos_validacao

Armadilhas:
- Misturar filho antigo com pai atualizado pode produzir uma citação inexistente.
- Muitos filhos do mesmo pai podem ocupar o ranking e reduzir diversidade de documentos.

Métricas sugeridas:
- Recall dos filhos, diversidade de pais, tokens de expansão e proporção de respostas que preservam exceções relevantes.

Testes propostos:
- Teste proposto: buscar uma cláusula cujo pai contém a exceção e conferir que ambas chegam à geração.
- Atualizar e excluir uma seção; verificar integridade dos vínculos, versão e permissões na próxima consulta.

## T032:C04 — perguntas_proveniencia

Pergunta: Parent-Child Chunking já executa recuperação?
Resposta: Não. Ele prepara a hierarquia; a recuperação precisa consultar os filhos e resolver os pais armazenados.

Pergunta: O documento pai precisa ser o arquivo completo?
Resposta: Não. Pode ser um bloco maior ou seção. A implementação oficial permite um parent_splitter separado do child_splitter.

Pergunta: Pai é sempre o documento completo?
Resposta: Não. Pode ser um bloco maior gerado previamente. O tamanho adequado depende do contexto necessário e do orçamento de leitura.

Pergunta: Top-k de filhos é igual a top-k de pais?
Resposta: Não. Vários filhos podem apontar ao mesmo pai. Controle diversidade e cobertura no nível realmente entregue ao gerador.

Escopo das fontes:
Código oficial ParentDocumentRetriever inspecionado. Versionamento, critérios de expansão, testes e aplicação LAI são propostas editoriais, sem resultado de benchmark alegado.

## T032:C05 — mecanismo_avancado

O vínculo filho-pai precisa incluir revisão, além de identidade lógica. Se o índice vetorial contém um filho antigo e o docstore devolve o pai novo, o trecho usado para localizar a resposta pode não existir no conteúdo entregue. Também é necessário deduplicar pais: muitos filhos semelhantes podem consumir todo o conjunto candidato e devolver apenas um documento.

Condição de contorno:
A expansão perde valor quando o pai é grande demais para o orçamento, inclui conteúdo inelegível ou não corresponde à versão do filho recuperado.

Contrato proposto:
- Entradas: Filhos indexados, mapa de parent_id e pais com versões recuperáveis.
- Saídas: Pais elegíveis ou regiões selecionadas, com evidência dos filhos que motivaram a expansão.
- Estado: Revisão de ingestão, presença dos pais e política de publicação do índice.
- Invariante: Nenhum filho é apresentado como evidência da versão de um pai à qual ele não pertence.

Compromissos de projeto:
- Filhos pequenos localizam detalhes, mas exigem lookup adicional e manutenção de relações.
- Pais maiores preservam contexto e podem introduzir ruído ou duplicação na montagem final.

## T032:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: interromper ingestão entre a escrita de filhos e pais, e depois alterar um pai sem reindexar. A consulta deve detectar ausência ou incompatibilidade, sem substituir silenciosamente o conteúdo.

Plano de avaliação proposto:
Avaliação proposta: comparar filhos isolados e expansão parental com orçamento igual. Medir pais únicos recuperados, integridade dos vínculos, recall de condições e custo de lookup; avaliar também muitas correspondências concentradas num único pai.

Comparações:
- T026 (complements): A hierarquia pode orientar busca; parent-child separa unidade de indexação da unidade entregue.
- T010 (complements): Um divisor simples pode gerar filhos, desde que os vínculos e versões sejam preservados.

Afirmação rastreável:
O ParentDocumentRetriever armazena o identificador do pai nos metadados dos filhos e mantém os pais num docstore.
Suporte: direct; fontes: V2C-S003
Limite: O código consultado faz operações em stores distintos; atomicidade entre eles não deve ser presumida.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T032:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou consistência filho-pai. Aqui a expansão é seletiva por regiões do pai, com cota compartilhada entre evidências concorrentes.

Projeto e decomposição
Expanda somente regiões que restauram dependências do filho, como cabeçalho, definição e ressalva. Carregar o pai inteiro pode introduzir ruído e consumir a janela de outros documentos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

Controle adaptativo
Una filhos do mesmo pai antes de expandir e preserve todos os motivos de seleção. A deduplicação do pai não pode apagar evidência de que vários trechos respondem a partes distintas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

Validação contrafactual
Compare expansão integral, janela local e blocos estruturais. Meça cobertura de condições por token, diversidade de pais e versões indevidas; manter constante a recuperação inicial. Unidade de avaliação: grupo de filhos recuperados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

USO AVANÇADO — Contratos técnicos
Cenário: Cláusula recuperada depende de definição anterior.
Estratégia: Abrir definição e exceções relacionadas, preservando seções e revisão; gerar resposta condicionada ao escopo do contrato.
Papel do modelo pequeno: 8–14B integra fragmentos.
Aceite proposto: A resposta deve incluir condição que muda interpretação da cláusula.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

USO AVANÇADO — Código distribuído
Cenário: Função encontrada depende de tipo ou chamada.
Estratégia: Expandir assinatura, tipo referenciado e ponto de uso, não todo o arquivo. Se dependência não resolver, declarar lacuna.
Papel do modelo pequeno: 3–7B localiza; 15–30B integra fluxo.
Aceite proposto: Não atribuir comportamento sem verificar interfaces relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2C-S003, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Localizador de trechos e dependências explícitas de um filho.
8–14B: Leitor de pequenos conjuntos de blocos do mesmo pai.
15–30B: Integrador entre pais quando a resposta exige contexto cruzado.
Requisitos de treino/runtime: Mapeamento filho-pai com offsets e revisão, parser estrutural e orçamento por evidência.
Não aplicar quando: Os vínculos não são confiáveis ou todo pai é necessário para qualquer interpretação.

## T032:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Recuperação de filhos seguida da substituição por pais.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T032:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T032 → T033 [requires]
Como combinar: Identificar blocos que completam contexto.
Interface: Cabeçalho, definição, ressalva e intervalos.
Condição: Parser conservar identidade dos blocos.
Aceite proposto: Testar cláusula com exceção distante.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2C-S003, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T032 → T042 [complements]
Como combinar: Distribuir expansão entre pais distintos.
Interface: Tokens previstos, requisitos e número de pais únicos.
Condição: Pai dominante não consumir toda a cota.
Aceite proposto: Comparar respostas com evidência distribuída em vários pais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V2C-S003, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Reaplicar filtros no conteúdo expandido.
- Não confundir número de filhos com número de fontes independentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar completude interpretativa por token; contexto extra só ajuda se o leitor distinguir escopo e exceções.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T026, T035, P007

## Fontes primárias associadas

### V2C-S003 — ParentDocumentRetriever — source code

[https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain_classic/retrievers/parent_document_retriever.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores parent_splitter e child_splitter, indexação dos filhos e retorno dos pais por IDs.

Limite: Código de referência consultado em branch móvel. A página da API anterior retornou content-type não suportado; o código oficial foi aberto e inspecionado. Não atesta implantação local.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T033 — Structure-Aware Chunking

**Nome canônico:** Structure-Aware Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T033  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação consciente da estrutura

## T033:C01 — conceito

Segmenta respeitando a estrutura do documento: títulos, seções, tabelas, listas, funções ou schemas. A unidade recuperável segue fronteiras com significado formal, e não apenas comprimento. Ainda precisa de limites de tamanho e de uma estratégia para unidades maiores que a janela.

Como funciona:
- Interpretar o formato e extrair sua estrutura.
- Criar unidades com caminho de cabeçalhos ou símbolos.
- Subdividir unidades grandes sem perder a relação com o bloco original.

## T033:C02 — aplicacao

Quando usar:
- Documentação Markdown, HTML, código e contratos estruturados.
- Perguntas que dependem de escopo de uma seção ou função.

Quando não usar:
- Não confiar no parser quando a extração de PDF perdeu colunas, tabelas ou ordem de leitura.

Implementação proposta:
- Proposta: escolher parser por MIME e guardar sua versão.
- Preservar nomes de seção, página, função e relações pai-filho.
- Em tabelas, repetir cabeçalho necessário sem inventar células ou separar chave do valor.

Aplicação LAI proposta:
Proposta LAI: usar para README, contratos de eventos e módulos de software, preservando o caminho até a evidência original.

## T033:C03 — riscos_validacao

Armadilhas:
- Cabeçalho pode ser confundido com texto dentro de bloco de código.
- Estruturas muito grandes exigem subdivisão contextual adicional.

Métricas sugeridas:
- Fração de unidades com metadados estruturais válidos.
- Recall de tabelas, exceções e símbolos de código.

Testes propostos:
- Usar Markdown com cerquilhas dentro de código e verificar que não viram títulos.
- Testar tabela multipágina e conferir associação entre coluna e valor.

## T033:C04 — perguntas_proveniencia

Pergunta: Structure-aware é sempre semântico?
Resposta: Ele reconhece estrutura formal; significado profundo ainda depende da interpretação e da pergunta.

Pergunta: Preciso guardar o texto integral?
Resposta: Sim, para reconstrução, verificação e nova segmentação se o parser estiver errado.

Pergunta: A versão do splitter basta para reproduzir os chunks?
Resposta: Não. Também registre o particionador e seus parâmetros. Alterar reconhecimento de títulos ou tabelas modifica a estrutura antes da divisão.

Pergunta: Uma tabela deve sempre permanecer inteira?
Resposta: Somente se couber e for utilizável. A subdivisão precisa conservar identificação das colunas, unidades e vínculo com a tabela original.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T033:C05 — mecanismo_avancado

A estrutura usada para agrupar trechos é resultado de uma etapa anterior de interpretação. Um erro de classificação transforma uma legenda em título e pode mudar os limites de todas as unidades seguintes. O chunker precisa conservar elementos originais e separar limites rígidos, como tamanho máximo, de preferências, como não juntar seções. Unidades estruturais gigantes ainda exigem subdivisão explícita.

Condição de contorno:
A vantagem diminui quando a estrutura é inferida de extração desordenada ou quando a pergunta depende de relações que atravessam vários elementos.

Contrato proposto:
- Entradas: Elementos tipados com ordem, documento, seção e coordenadas ou offsets recuperáveis.
- Saídas: Chunks com lista de elementos de origem, divisões internas e metadados herdados.
- Estado: Versões do particionador, regras de agrupamento e tratamento de elementos excedentes.
- Invariante: A reconstrução da origem não depende de interpretar novamente o texto sintetizado do chunk.

Compromissos de projeto:
- Agrupar elementos inteiros conserva relações locais, mas pode desperdiçar orçamento ao respeitar fronteiras.
- Mesclar seções pequenas reduz fragmentação; também pode juntar assuntos cuja separação tinha significado.

## T033:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: classificar deliberadamente uma legenda como título e inserir uma tabela maior que o limite. O processamento deve expor a segmentação derivada e conservar associação entre cabeçalho, linhas e fonte.

Plano de avaliação proposto:
Avaliação proposta: comparar segmentação por elementos e recursiva usando a mesma extração inicial. Medir fidelidade estrutural, cobertura de relações tabela-texto, proporção de subdivisões e recuperação por orçamento; separar falhas do parser das do chunker.

Comparações:
- T012 (alternative): A divisão recursiva usa separadores textuais; elementos estruturados carregam tipos e relações produzidos antes do agrupamento.
- T032 (complements): A expansão parental pode recuperar contexto que uma unidade estrutural pequena não contém.

Afirmação rastreável:
O Unstructured agrupa elementos previamente particionados e divide elementos que excedem o tamanho máximo.
Suporte: direct; fontes: V3A-S027
Limite: O comportamento depende da estratégia e configuração; preservar toda seção não é uma garantia universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T033:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 analisou erros de parsing. Aqui estruturas viram unidades de evidência com contratos distintos de leitura e comparação.

Projeto e decomposição
Trate tabela, procedimento, figura e código como tipos diferentes. Uma tabela precisa de cabeçalhos e unidades; procedimento precisa de ordem; código precisa de contexto sintático.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

Controle adaptativo
Produza duas representações: texto para busca e objeto estruturado para leitura. O índice pode omitir detalhes, mas a geração deve acessar a representação que conserva relações necessárias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

Validação contrafactual
Compare texto linearizado e blocos tipados em perguntas que dependem de linhas, colunas ou ordem. Meça erros de associação, não só recuperação do documento correto. Unidade de avaliação: bloco estrutural.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

USO AVANÇADO — Tabelas comparativas
Cenário: Valores similares pertencem a modelos diferentes.
Estratégia: Recuperar tabela pelo tema, selecionar linhas em código e fornecer cabeçalho completo ao leitor. Preservar notas de rodapé aplicáveis.
Papel do modelo pequeno: 3–7B verbaliza células selecionadas.
Aceite proposto: Não trocar coluna, unidade ou condição de nota.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

USO AVANÇADO — Procedimento operacional
Cenário: Passos incluem ramos condicionais.
Estratégia: Preservar ordem e condições em estrutura; fornecer somente ramo aplicável, mantendo ponto de retorno.
Papel do modelo pequeno: 8–14B explica execução.
Aceite proposto: Toda ação deve respeitar pré-condições e ordem documentadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S027, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de células e campos com relações explícitas.
8–14B: Interpretador de listas condicionais e blocos de código pequenos.
15–30B: Comparador de múltiplas estruturas com referências cruzadas.
Requisitos de treino/runtime: Parser com testes por formato e ligação entre texto indexado e objeto de leitura; OCR exige avaliação própria.
Não aplicar quando: Extração não preserva layout decisivo e não há imagem ou original disponível para conferir.

## T033:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C015 — Amazon Web Services / Bedrock Knowledge Bases chunking
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Manual lista modos de ingestão e recuperação disponíveis.
Mecanismo documentado: Chunks fixos, semânticos e hierarquia de filhos substituídos por pais.
Correspondência com esta base: Respeita limites lógicos em conteúdo analisado, sem todos os parsers desta ficha.
Transferência proposta para modelo pequeno: Proposta de engenharia: Escolher splitter por família documental, testando contexto consumido por 3–30B.
Limite: Não prova implantação particular; modos alternativos não são todos ativados no mesmo documento. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S013.

V4A-C020 — Google / NotebookLM com fontes multimodais
Evidência: produto/recurso disponível; analogia; não é adoção deste componente. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Produto oferece análise de documentos, áudio e vídeo com citações.
Mecanismo documentado: Conteúdo de fontes e transcrições fundamenta respostas referenciadas.
Correspondência com esta base: Transcrições permitem endereçar trechos, sem comprovar splitter estrutural próprio.
Transferência proposta para modelo pequeno: Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.
Limite: Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S025.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q019, V4A-Q022.

## T033:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T033 → T032 [feeds]
Como combinar: Expandir filho em estrutura completa necessária.
Interface: Tipo, bloco_id, cabeçalhos e revisão.
Condição: Pai estrutural corresponder à mesma origem.
Aceite proposto: Recuperar célula sem perder cabeçalho que muda significado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S027, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T033 → T195 [complements]
Como combinar: Verificar propriedades calculáveis da estrutura.
Interface: Tabela tipada ou código e regras de validação.
Condição: Execução autorizada e ambiente adequado.
Aceite proposto: Detectar soma ou sintaxe inválida antes da resposta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S027, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar ordem visual como sequência temporal sem indicação.
- Conservar vínculo entre nota e células afetadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar leitura relacional de tabelas e procedimentos; domínio estrutural pode permitir bons resultados com modelos menores.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T010, T012, T032, T035

## Fontes primárias associadas

### A-S039 — Markdown node parser

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segmentação por cabeçalhos com metadados de caminho estrutural.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S027 — Chunking

[https://docs.unstructured.io/open-source/core-functionality/chunking](https://docs.unstructured.io/open-source/core-functionality/chunking)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Particionamento em elementos estruturais antes de agrupar chunks; tratamento de tabelas, tamanho e fronteiras por título.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews

[https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto fundamentado em fontes com citações e transcrições; recursos disponíveis.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T034 — Agentic Chunking

**Nome canônico:** Agentic Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T034  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação por agente

## T034:C01 — conceito

Rótulo amplo para usar uma LLM ou um agente na definição de unidades de conhecimento, fronteiras ou agrupamentos durante a ingestão. Não designa um algoritmo universal. Precisa distinguir seleção de trechos originais de geração de novas proposições, pois a segunda pode introduzir informação falsa.

Como funciona:
- Fornecer unidades iniciais e um contrato de segmentação.
- Solicitar fronteiras ou agrupamentos com referências à origem.
- Validar cobertura, tamanho e fidelidade antes de indexar.

Nota de nomenclatura: Termo descritivo sem implementação única identificada; fontes fornecem os conceitos de segmentação relacionados, não validam um método exclusivo.

## T034:C02 — aplicacao

Quando usar:
- Acervos heterogêneos cujo layout não fornece boa estrutura.
- Prototipagem de unidades conceituais difíceis de obter com regras simples.

Quando não usar:
- Não adotar sem controle de custo e verificação quando ingestão determinística já atende às perguntas.

Implementação proposta:
- Proposta: pedir offsets ou IDs existentes, evitando reescrita livre da fonte.
- Validar que cada unidade citada pertence ao documento e que não há lacunas.
- Separar proposições geradas das passagens originais no índice.

Aplicação LAI proposta:
Proposta LAI: reservar para bases teóricas complexas em experimento isolado; manter divisão estrutural como comparação de menor custo.

## T034:C03 — riscos_validacao

Armadilhas:
- A LLM pode agrupar fatos incompatíveis ou criar uma conexão inexistente.
- Resultados variáveis dificultam reproduzir atualizações e depurar recuperação.

Métricas sugeridas:
- Cobertura e fidelidade dos trechos.
- Custo por documento e ganho de recall frente ao splitter convencional.

Testes propostos:
- Executar duas vezes o mesmo documento e medir estabilidade.
- Inserir instrução maliciosa no texto e exigir que seja tratada como dado, sem mudar o segmentador.

## T034:C04 — perguntas_proveniencia

Pergunta: Usar um agente para dividir texto torna o RAG melhor?
Resposta: Não automaticamente. O ganho depende de perguntas reais, e a ingestão pode ficar mais cara e menos previsível.

Pergunta: Posso indexar fatos reescritos como originais?
Resposta: Não. Marque-os como derivados e mantenha as fontes correspondentes.

Pergunta: Toda proposição precisa repetir o nome da entidade?
Resposta: Precisa ser interpretável na recuperação. Uma referência estruturada pode cumprir esse papel sem repetir texto, desde que o leitor a resolva.

Pergunta: Como atualizar uma proposição após correção da fonte?
Resposta: Recalcule as derivadas dependentes da revisão alterada. Similaridade de texto não basta para detectar quais relações ficaram inválidas.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T034:C05 — mecanismo_avancado

Há duas decisões distintas sob esse rótulo: escolher fronteiras entre segmentos existentes e produzir proposições independentes. A segunda resolve pronomes e combina contexto, mas cria texto novo. Sua validação deve verificar sustentação e escopo: sujeito, quantificador, modalidade e condição temporal. Uma proposição curta pode ter boa recuperabilidade e ainda inverter a conclusão por remover uma palavra como “pode”.

Condição de contorno:
A extração proposicional é arriscada quando interpretação depende de ironia, discordância entre participantes ou condições distribuídas em várias partes do documento.

Contrato proposto:
- Entradas: Segmentos identificados, contexto necessário e contrato indicando seleção literal ou derivação.
- Saídas: Grupos de offsets ou proposições marcadas como derivadas, cada uma ligada às evidências.
- Estado: Modelo, instrução, revisões documentais e resultados de verificações de sustentação.
- Invariante: Uma reescrita nunca recebe automaticamente o mesmo status de uma afirmação literal da fonte.

Compromissos de projeto:
- Proposições autocontidas facilitam localização de fatos específicos, mas aumentam tamanho do índice e custo de ingestão.
- Verificação adicional reduz erros de derivação; pode anular a economia obtida na geração final.

## T034:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: apresentar falas contraditórias de dois autores e uma hipótese condicional. A extração deve preservar atribuição, discordância e modalidade, sem fundi-las numa afirmação categórica.

Plano de avaliação proposto:
Avaliação proposta: comparar chunks estruturais, fronteiras escolhidas por modelo e proposições derivadas com mesmo corpus. Medir recall, fidelidade por proposição, expansão do índice e custo de atualização; inspecionar separadamente erros de atribuição e negação.

Comparações:
- T033 (alternative): Estrutura formal fornece fronteiras sem exigir que um modelo reconstrua cada afirmação.
- T054 (complements): Proposições validadas podem alimentar memória semântica, mantendo proveniência e grau de confirmação.

Afirmação rastreável:
Dense X Retrieval investiga proposições autocontidas como unidade de recuperação, comparando granularidades de indexação.
Suporte: related; fontes: V3A-S012
Limite: A fonte sustenta uma abordagem proposicional, não padroniza todos os métodos chamados Agentic Chunking.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T034:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou fronteiras e proposições. Aqui decisões do agente sobre segmentação ficam sujeitas a estabilidade e custo de revisão.

Projeto e decomposição
O agente deve escolher entre fronteiras candidatas produzidas por regras, não inventar livremente texto derivado. Isso limita variação e preserva alinhamento com origem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

Controle adaptativo
Registre justificativa de fronteira por dependência: mudança de assunto, entidade ou escopo. Repetir a segmentação com pequena edição deve modificar apenas regiões justificáveis.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

Validação contrafactual
Compare splitter determinístico e agente com orçamento de chamadas igualado por corpus. Meça recuperação, estabilidade de IDs, custo de ingestão e taxa de fronteiras que separam condição e consequência. Unidade de avaliação: documento segmentado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

USO AVANÇADO — Documentos heterogêneos
Cenário: Seções misturam FAQ e narrativa.
Estratégia: Classificar região e selecionar política de divisão específica; usar julgamento do agente somente em fronteiras ambíguas.
Papel do modelo pequeno: 3–7B classifica tipos; 8–14B decide bordas.
Aceite proposto: Nenhuma condição essencial deve ficar sem referência ao trecho dependente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

USO AVANÇADO — Notas de pesquisa
Cenário: Uma observação interrompe tópico e retorna depois.
Estratégia: Criar segmentos por unidade argumentativa e relações de continuidade; não fundir trechos distantes sem registrar origem.
Papel do modelo pequeno: 15–30B identifica dependências complexas.
Aceite proposto: Cada segmento deve ser reconstruível a partir de intervalos explícitos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S012, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de região com conjunto fechado de políticas.
8–14B: Árbitro de poucas fronteiras ambíguas, com justificativa curta.
15–30B: Analista de continuidade argumentativa em documentos difíceis.
Requisitos de treino/runtime: Candidatos de fronteira, alinhamento por offsets e orçamento de ingestão; decisão estocástica precisa versão registrada.
Não aplicar quando: Conteúdo é homogêneo e splitter simples tem qualidade equivalente com custo muito menor.

## T034:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q022.

## T034:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T034 → T033 [requires]
Como combinar: Detectar estruturas antes da escolha pelo agente.
Interface: Blocos protegidos e cortes permitidos.
Condição: Agente não poder romper unidade obrigatória.
Aceite proposto: Testar tabela e bloco de código que parecem mudar de tema.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S012, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T034 → T072 [feeds]
Como combinar: Versionar decisões de segmentação.
Interface: Modelo, prompt, fronteiras e revisão documental.
Condição: Reindexação preservar histórico de referência.
Aceite proposto: Repetir ingestão e medir mudança injustificada de IDs.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S012, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar reescrita de texto de simples chunking.
- Comparar fronteiras com origem, não só com fluência dos segmentos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar benefício marginal sobre regras; usar modelo maior na ingestão só se o ganho persistir na leitura.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T011, T033, T195

## Fontes primárias associadas

### A-S039 — Markdown node parser

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Segmentação por cabeçalhos com metadados de caminho estrutural.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S041 — Semantic splitter

[https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Implementação de parsers semânticos e janelas de sentenças.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S012 — Dense X Retrieval: What Retrieval Granularity Should We Use?

[https://arxiv.org/abs/2312.06648](https://arxiv.org/abs/2312.06648)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Granularidade de recuperação e proposições autossuficientes como unidades de indexação.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T035 — Contextual Chunking

**Nome canônico:** Contextual Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T035  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** contextualização de chunks; Contextual Retrieval

## T035:C01 — conceito

Expressão usada de forma variável para preservar contexto ao segmentar ou para enriquecer cada trecho antes da indexação. Neste pacote, refere-se principalmente a contextualização de chunks: adicionar uma descrição curta que situa o trecho no documento, mantendo separado o texto original.

Como funciona:
- Identificar documento, seção e entidades relevantes ao trecho.
- Gerar ou extrair um pequeno contexto explicativo.
- Indexar contexto e trecho sem perder a fronteira entre fonte e texto derivado.

Nota de nomenclatura: O nome original é amplo; o mecanismo específico documentado pela Anthropic é Contextual Retrieval, não um splitter universal.

## T035:C02 — aplicacao

Quando usar:
- Trechos com pronomes ou nomes abreviados que ficam ambíguos isoladamente.
- Coleções de relatórios semelhantes de produtos ou versões distintas.

Quando não usar:
- Não adicionar resumo inventado ou informações externas como se fizessem parte da fonte.

Implementação proposta:
- Proposta: preferir metadados determinísticos quando suficientes.
- Se usar LLM, validar contexto produzido contra o documento original.
- Preservar campos separados original_text e contextual_prefix para auditoria e citações.

Aplicação LAI proposta:
Proposta LAI: acrescentar software, versão e seção em cada fragmento técnico antes de buscar descrições geradas mais elaboradas.

## T035:C03 — riscos_validacao

Armadilhas:
- Contextualização errada contamina simultaneamente busca lexical e vetorial.
- Um prefixo grande pode dominar o embedding e reduzir discriminação do trecho.

Métricas sugeridas:
- Recall de perguntas com entidades implícitas.
- Taxa de contextos adicionados sem apoio no documento.

Testes propostos:
- Usar relatórios de dois produtos com os mesmos termos e exigir distinção correta.
- Trocar o documento pai e verificar invalidação da contextualização derivada.

## T035:C04 — perguntas_proveniencia

Pergunta: Contextual Retrieval muda necessariamente as fronteiras?
Resposta: Não. Pode manter os mesmos chunks e acrescentar informação que os situa no documento.

Pergunta: A descrição adicionada pode ser citada como fonte primária?
Resposta: Não por si só. A citação deve apontar para o trecho original que a sustenta.

Pergunta: Late Chunking produz uma explicação textual adicional?
Resposta: Não necessariamente. A informação contextual entra nas representações dos tokens antes do agrupamento que forma o embedding do trecho.

Pergunta: O prefixo precisa conter um resumo completo?
Resposta: Não. O objetivo é resolver o que torna aquele trecho ambíguo. Resumo amplo pode ocupar espaço e reduzir sua especificidade.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T035:C05 — mecanismo_avancado

A contextualização altera a representação de busca antes da consulta: termos de entidade, período e escopo passam a integrar o texto indexado. Isso pode elevar a recuperação de um trecho ambíguo, mas também contaminar dois caminhos simultaneamente quando o prefixo é usado em embeddings e BM25. A atualização documental deve considerar dependências além do chunk: o prefixo pode depender de outra seção.

Condição de contorno:
Quando metadados determinísticos já resolvem a ambiguidade, gerar uma descrição pode adicionar custo e erro sem melhorar a discriminação entre trechos.

Contrato proposto:
- Entradas: Chunk original, contexto documental autorizado e revisão consistente da fonte.
- Saídas: Anotação contextual separada do texto citado, com dependências documentais registradas.
- Estado: Modelo contextualizador, template, versões do índice e associação entre prefixo e original.
- Invariante: Termos acrescentados para busca permanecem identificáveis como anotação, sem se tornarem evidência primária.

Compromissos de projeto:
- Contexto específico resolve referências locais, mas prefixos semelhantes podem aproximar artificialmente todos os chunks.
- Gerar anotações na ingestão amortiza custo de consulta e exige reprocessamento quando as dependências mudam.

## T035:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar a entidade descrita na introdução sem alterar o chunk. A indexação deve invalidar o prefixo dependente e impedir recuperação que ainda atribua o trecho à entidade antiga.

Plano de avaliação proposto:
Avaliação proposta: comparar original, metadados determinísticos e contexto gerado, mantendo recuperador e orçamento iguais. Medir recuperação de referências implícitas, erros adicionados, custo de reindexação e diversidade dos candidatos; distinguir ganho lexical de ganho vetorial.

Comparações:
- T011 (distinct_from): Mudar fronteiras por similaridade não equivale a contextualizar a representação de um chunk existente.
- T027 (complements): Contextualização pode beneficiar busca lexical e vetorial; a fusão ainda precisa ser avaliada com candidatos equivalentes.

Afirmação rastreável:
Contextual Retrieval acrescenta contexto específico do trecho antes da indexação vetorial e lexical; Late Chunking contextualiza vetores antes do pooling.
Suporte: direct; fontes: A-S025, V3A-S014
Limite: São mecanismos distintos; resultados de um não demonstram eficácia do outro nem superioridade em qualquer acervo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T035:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou contaminação do prefixo contextual. Aqui a expansão contextual é controlada por contrafactuais de identidade e granularidade.

Projeto e decomposição
Limite contexto adicionado a identificadores e localização que realmente desambiguam o trecho. Comentário explicativo longo pode dominar embedding e aproximar chunks diferentes indevidamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

Controle adaptativo
Separe texto original, contexto gerado e campos estruturados. A busca pode usar todos; o leitor deve saber qual parte foi extraída e qual foi inferida na ingestão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

Validação contrafactual
Compare prefixos curtos, longos e ausência de prefixo. Troque entidades em documentos estruturalmente iguais para detectar vazamento de identidade e medir ranking de homônimos. Unidade de avaliação: chunk contextualizado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

USO AVANÇADO — Relatórios padronizados
Cenário: Trechos iguais pertencem a períodos distintos.
Estratégia: Adicionar organização, período e seção verificados; preservar esses atributos também como filtros, não apenas palavras no prefixo.
Papel do modelo pequeno: 3–7B gera contexto a partir de campos.
Aceite proposto: Consulta histórica não pode recuperar período errado por similaridade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

USO AVANÇADO — Documentação de componentes
Cenário: Pronome referencia módulo distante.
Estratégia: Resolver referente pelo escopo documental e anexar identificação mínima; se houver ambiguidade, manter candidatos em vez de escolher silenciosamente.
Papel do modelo pequeno: 8–14B resolve referência local.
Aceite proposto: Toda identidade adicionada precisa de apoio no documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de prefixo determinístico verbalizado a partir de metadados.
8–14B: Resolvedor contextual para pronomes e escopo de seção.
15–30B: Revisor de casos ambíguos que atravessam vários documentos.
Requisitos de treino/runtime: Campos verificados, marcação de conteúdo gerado e reindexação quando escopo mudar.
Não aplicar quando: Contexto só pode ser obtido por especulação ou prefixo melhora similaridade mas piora precisão de evidências.

## T035:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q019, V4A-Q022.

## T035:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T035 → T066 [requires]
Como combinar: Confirmar entidade e versão usadas no prefixo.
Interface: Identificador, escopo e evidência da resolução.
Condição: Resolver preservar ambiguidade não resolvida.
Aceite proposto: Testar duas entidades de mesmo nome.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S025, V3A-S014, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T035 → T027 [complements]
Como combinar: Aplicar contexto com avaliação separada por canal.
Interface: Texto original, prefixo e campos filtráveis.
Condição: Prefixo não apagar termos literais raros.
Aceite proposto: Medir contribuição lexical e vetorial independentemente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S025, V3A-S014, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não citar prefixo gerado como fonte primária.
- Evitar copiar título desatualizado para todos os chunks.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar desambiguação e precisão; contexto adicional pode ajudar indexação e prejudicar um leitor pequeno se não for rotulado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T033, T036, T027

## Fontes primárias associadas

### A-S025 — Introducing Contextual Retrieval

[https://www.anthropic.com/research/contextual-retrieval](https://www.anthropic.com/research/contextual-retrieval)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contextualização de trechos antes da indexação vetorial e lexical.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S014 — Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models

[https://arxiv.org/abs/2409.04701](https://arxiv.org/abs/2409.04701)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contextualização antes da segmentação final e do mean pooling; distinta de gerar prefixos textuais para chunks.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T036 — Query-Aware RAG

**Nome canônico:** Query-Aware RAG  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T036  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** RAG orientado à consulta

## T036:C01 — conceito

Adapta recuperação e montagem do contexto à pergunta atual. Pode reescrever a consulta, decompô-la em subperguntas, escolher índices ou selecionar trechos. É uma família de desenhos; a simples existência de uma consulta já condiciona a busca, portanto é preciso especificar qual adaptação adicional foi implementada.

Como funciona:
- Identificar entidades, intenção, data e escopo da pergunta.
- Produzir consultas direcionadas e combinar evidências.
- Verificar se cada parte da pergunta possui suporte antes de gerar resposta.

## T036:C02 — aplicacao

Quando usar:
- Perguntas com múltiplas condições ou dependências.
- Vocabulário do usuário diferente do utilizado nos documentos.

Quando não usar:
- Não reescrever de modo a apagar negação, identidade, intervalo temporal ou requisito de acesso.

Implementação proposta:
- Proposta: guardar consulta original e consultas derivadas.
- Aplicar filtros obrigatórios fora da reescrita probabilística.
- Medir a utilidade de cada expansão, evitando buscas circulares sem nova evidência.

Aplicação LAI proposta:
Proposta LAI: decompor comparações entre técnicas e pedir evidência separada para mecanismo, limites e compatibilidade com o runtime.

## T036:C03 — riscos_validacao

Armadilhas:
- O agente pode buscar apenas confirmação da hipótese inicial.
- Muitas consultas ampliam ruído e custo sem elevar cobertura.

Métricas sugeridas:
- Cobertura das subperguntas e precisão da evidência.
- Custo por resposta correta e número de buscas redundantes.

Testes propostos:
- Perguntar por diferença entre dois conceitos e exigir fonte para ambos.
- Usar uma pergunta negativa ou temporal e confirmar que a reescrita preserva a condição.

## T036:C04 — perguntas_proveniencia

Pergunta: É um algoritmo específico?
Resposta: Não. O nome precisa vir acompanhado das regras concretas de adaptação.

Pergunta: Como evitar confirmação seletiva?
Resposta: Buscar evidências que poderiam refutar a hipótese e registrar lacunas e fontes conflitantes.

Pergunta: A hipótese deve aparecer na resposta?
Resposta: Somente se identificada como hipótese e útil ao raciocínio comunicado. Não deve ser citada como descoberta documental.

Pergunta: Uma expansão pode adicionar filtros?
Resposta: Pode propor filtros opcionais, mas não trocar restrições explícitas. Identidade, período e autorização devem ser controlados fora da geração livre.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T036:C05 — mecanismo_avancado

Uma adaptação concreta é HyDE: gerar um documento hipotético para a pergunta, codificá-lo e buscar documentos reais próximos. O texto gerado pode conter falsidades; sua função é oferecer uma representação de busca. A decisão final precisa voltar às fontes recuperadas. Preservar consulta original e expansões permite diagnosticar deriva, especialmente quando a hipótese acrescenta uma entidade ou solução que o usuário não informou.

Condição de contorno:
A expansão tende a prejudicar quando a pergunta depende de identificador exato, versão específica ou exceção que o gerador substitui por uma resposta típica.

Contrato proposto:
- Entradas: Pergunta original, restrições obrigatórias e política de geração de consultas derivadas.
- Saídas: Consultas ou hipóteses de busca e evidências reais recuperadas separadamente.
- Estado: Origem de cada candidato, filtros aplicados e revisão dos modelos de expansão.
- Invariante: Conteúdo sintético de expansão nunca serve como prova da própria resposta.

Compromissos de projeto:
- A hipótese amplia correspondência semântica, mas pode aproximar a busca de uma solução errada.
- Buscar também a consulta original aumenta custo e oferece uma comparação útil contra deriva da expansão.

## T036:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: formular pergunta sobre uma versão antiga enquanto a hipótese gerada descreve a atual. Os filtros devem manter a versão solicitada; ausência de evidência deve continuar explícita.

Plano de avaliação proposto:
Avaliação proposta: comparar consulta original, reescrita e HyDE com mesmo orçamento de candidatos. Medir recall elegível, deriva de entidades, preservação de restrições e custo total; inspecionar respostas corretas por acaso apoiadas em documentação incompatível.

Comparações:
- T037 (distinct_from): Adaptar a busca muda candidatos; comprimir para a pergunta seleciona informação depois da recuperação.
- T025 (complements): Um roteador pode decidir quando a expansão compensa, sem alterar filtros obrigatórios.

Afirmação rastreável:
HyDE utiliza um documento hipotético gerado para construir uma representação de consulta e recuperar documentos reais.
Suporte: direct; fontes: V3A-S028
Limite: A codificação da hipótese não oferece garantia de remover toda informação falsa ou recuperar suporte suficiente.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T036:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu deriva em HyDE. Aqui a consulta é decomposta em requisitos preserváveis e estratégias de recuperação por requisito.

Projeto e decomposição
Extraia entidades, período, relação pedida e formato esperado antes de reformular. Marque elementos que nenhuma expansão pode alterar, como versão e quantificador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

Controle adaptativo
Use consultas diferentes para suporte e contradição. Buscar somente textos que parecem confirmar a hipótese favorece respostas coerentes e incompletas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

Validação contrafactual
Compare consulta original, reformulação única e decomposição por requisito. Meça cobertura e deriva semântica com casos de negação, comparação e restrição temporal. Unidade de avaliação: consulta decomposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

USO AVANÇADO — Pergunta comparativa
Cenário: Usuário pede diferenças com mesma condição.
Estratégia: Criar subconsultas simétricas por item e atributo; impedir que uma opção receba evidência mais ampla que outra.
Papel do modelo pequeno: 3–7B decompõe campos; 8–14B lê respostas.
Aceite proposto: Cobertura deve ser equivalente nos atributos comparados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

USO AVANÇADO — Verificação de afirmação
Cenário: Há suspeita de regra revogada.
Estratégia: Buscar versão vigente, histórico de mudança e fontes contrárias; separar não encontrado de refutado.
Papel do modelo pequeno: 15–30B integra conflito temporal.
Aceite proposto: Conclusão deve refletir escopo e data das evidências.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S022, V4A-S009, V4A-S020.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Reformulador controlado com termos protegidos e saídas estruturadas.
8–14B: Decompositor de perguntas compostas com poucas dependências.
15–30B: Planejador de consultas sequenciais quando resposta anterior determina a próxima.
Requisitos de treino/runtime: Esquema de intenção e comparação da reformulação com pedido original; exemplos de negativos ajudam especialização.
Não aplicar quando: Reformulação remove requisitos ou cria documentos hipotéticos tratados como prova.

## T036:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C012 — Amazon / Rufus shopping assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Amazon descreve assistente em uso no aplicativo de compras.
Mecanismo documentado: RAG seleciona catálogo, avaliações, perguntas comunitárias e APIs conforme a pergunta.
Correspondência com esta base: Relevância de cada fonte varia com a consulta.
Transferência proposta para modelo pequeno: Proposta de engenharia: Separar busca factual de texto opinativo e exigir evidência de atributo antes da comparação por 8–14B.
Limite: Porte do LLM customizado não é indicado; não explicita BM25+vetores nem cada técnica de chunking. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S022.

V4A-C008 — Microsoft / Bing: transformers na busca global
Evidência: produção documentada; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: NLP não generativo; não é LLM autoregressiva 3–30B.
Uso observado: Operador afirma modelos transformer aplicados às consultas Bing globais no período descrito.
Mecanismo documentado: Compreensão contextual de consultas e páginas com inferência otimizada.
Correspondência com esta base: Consulta orienta compreensão e seleção; não comprova leitor RAG específico.
Transferência proposta para modelo pequeno: Proposta de engenharia: Empregar modelo compacto para julgar pares consulta-trecho, medindo custo e ordenação.
Limite: BERT destilado do relato não é um gerador 3–30B; números de infraestrutura não são transportáveis. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S008.

V4A-C023 — IBM / Granite RAG LoRAs experimentais
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Anúncio distingue modelos disponíveis de adaptadores publicados no Granite Experiments.
Mecanismo documentado: Adaptadores para subtarefas como reescrita de consultas e detecção de alucinação.
Correspondência com esta base: Reescrita específica de consulta é subtarefa nomeada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir especialização de 8B por papel sem ativar o mesmo adaptador em tarefas incompatíveis.
Limite: Experimentos não são implantação; não transferir compatibilidade KV de aLoRA a qualquer LoRA. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q010, V4A-Q017, V4A-Q020.

## T036:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T036 → T027 [feeds]
Como combinar: Distribuir subconsultas para canais adequados.
Interface: Termos literais, intenção e filtros comuns.
Condição: Canais preservarem restrições originais.
Aceite proposto: Testar versão alterada durante paráfrase.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S009, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T036 → T037 [complements]
Como combinar: Comprimir contexto conforme requisito específico.
Interface: Subconsulta, requisito e trechos recuperados.
Condição: Retorno manter ligação ao pedido global.
Aceite proposto: Conferir que compressões locais não eliminam ponte entre requisitos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S022, V4A-S009, V4A-S020. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar consulta sintetizada como evidência factual.
- Registrar cada reformulação para rastrear perda de condição.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar cobertura de requisitos com mesmo acervo; bom planejamento de busca não garante síntese geral superior.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T025, T027, T028, T037

## Fontes primárias associadas

### A-S007 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de modelo gerador e memória não paramétrica recuperável.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S017 — Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity

[https://aclanthology.org/2024.naacl-long.389/](https://aclanthology.org/2024.naacl-long.389/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Classificador seleciona ausência de busca, busca única ou recuperação iterativa conforme complexidade.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S028 — Precise Zero-Shot Dense Retrieval without Relevance Labels

[https://arxiv.org/abs/2212.10496](https://arxiv.org/abs/2212.10496)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: HyDE gera um documento hipotético para orientar busca em documentos reais; o texto hipotético pode conter falsidades.

Limite: Fonte primária consultada; não houve reprodução, instalação ou validação de desempenho na LAI. Contratos e cenários adicionais são propostas editoriais.

### V4A-S022 — The technology behind Amazon’s GenAI-powered shopping assistant, Rufus

[https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus](https://www.amazon.science/blog/the-technology-behind-amazons-genai-powered-shopping-assistant-rufus)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Rufus usa RAG com catálogo, avaliações, perguntas e APIs de lojas no atendimento de compras.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S020 — IBM Granite 3.3: Speech recognition, refined reasoning, and RAG LoRAs

[https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras](https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo 8B disponível e adaptadores experimentais por subtarefa RAG; separar disponibilidade e experimento.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S008 — Bing delivers its largest improvement in search experience using Azure GPUs

[https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/](https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos transformer aplicados às consultas Bing; inferência otimizada e compreensão da consulta.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T037 — Query-Aware Compression

**Nome canônico:** Query-Aware Compression  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T037  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compressão orientada à consulta

## T037:C01 — conceito

Reduz um conjunto de informações levando em conta a pergunta atual. Preserva conteúdo que ajuda a responder aquela consulta e pode descartar informação útil para outras. O resultado é uma representação condicionada à pergunta, não um resumo universal do documento.

Como funciona:
- Receber pergunta e documentos candidatos já autorizados.
- Pontuar passagens por utilidade para as condições da consulta.
- Preservar evidências e qualificações dentro do orçamento.

## T037:C02 — aplicacao

Quando usar:
- RAG retorna documentos extensos com poucos trechos relevantes.
- Perguntas muito específicas sobre um acervo amplo.

Quando não usar:
- Não reutilizar a versão comprimida para uma nova pergunta sem reavaliar o que foi omitido.

Implementação proposta:
- Proposta: incluir hash da pergunta e versão documental nos metadados.
- Proteger trechos que definem exceções, unidades e escopo.
- Armazenar offsets da seleção e indicar campos da pergunta ainda sem evidência.

Aplicação LAI proposta:
Proposta LAI: usar para montar respostas sobre mecanismos específicos, mantendo definições exatas e limitações; uma seleção para custo não deve ser reutilizada para compatibilidade.

## T037:C03 — riscos_validacao

Armadilhas:
- O compressor pode escolher apenas trechos que confirmam uma resposta provável.
- Compressão agressiva pode remover a relação entre condição e conclusão.

Métricas sugeridas:
- Cobertura de cada requisito da pergunta.
- Tokens economizados, fidelidade e tempo do compressor.

Testes propostos:
- Fazer duas perguntas diferentes sobre o mesmo documento e comparar seleções.
- Incluir evidência contraditória e exigir que ambas as posições relevantes sobrevivam.

## T037:C04 — perguntas_proveniencia

Pergunta: É igual a resumir o documento inteiro?
Resposta: Não. A relevância é definida pela consulta; informações importantes para outras tarefas podem ficar de fora.

Pergunta: A consulta também pode ser comprimida?
Resposta: Pode, mas deve preservar intenção, negação, identidade e escopo; perder isso invalida a seleção.

Pergunta: Como cachear a compressão?
Resposta: Inclua pergunta ou intenção formal, versões das fontes e configuração do compressor. Cache por documento apenas mistura seleções feitas para objetivos diferentes.

Pergunta: Uma síntese fiel basta para responder bem?
Resposta: Não. Ela pode ser fiel ao que selecionou e omitir uma condição indispensável. Fidelidade e suficiência precisam ser avaliadas separadamente.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T037:C05 — mecanismo_avancado

O compressor condicionado à pergunta implementa uma decisão sobre utilidade futura, não apenas sobre relevância lexical imediata. Em problemas com várias etapas, um trecho aparentemente secundário pode conter a ligação necessária para a próxima busca. RECOMP também permite saída vazia quando os documentos não acrescentam informação útil, evitando alimentar o gerador com contexto irrelevante. Essa escolha exige distinguir ausência de utilidade e ausência de evidência.

Condição de contorno:
Uma representação comprimida perde validade quando muda a finalidade, a pergunta ou a versão das fontes; correspondência temática não garante reutilização segura.

Contrato proposto:
- Entradas: Pergunta, documentos candidatos, orçamento e requisitos de sustentação da resposta.
- Saídas: Trechos ou síntese condicionada, referências de suporte e campos sem cobertura.
- Estado: Identidade da consulta, versões documentais, seletor e motivos de descarte recuperáveis.
- Invariante: Saída vazia não é registrada automaticamente como prova de que a afirmação consultada é falsa.

Compromissos de projeto:
- Seleção agressiva reduz leitura, mas aumenta risco de excluir pontes necessárias a inferências posteriores.
- Compressão treinada para o gerador pode melhorar compatibilidade e restringe transferência entre tarefas e modelos.

## T037:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: usar duas fontes em que a ligação depende de uma definição pouco semelhante à pergunta. O compressor deve preservar a ponte ou indicar cobertura insuficiente, sem fabricar a conexão.

Plano de avaliação proposto:
Avaliação proposta: comparar contexto integral, seleção extrativa e síntese com custo completo de compressão e geração. Medir sustentação, recall de relações intermediárias e erros por falsa ausência; repetir após mudança de pergunta para detectar reutilização indevida.

Comparações:
- T036 (complements): A consulta pode ser adaptada antes da busca, mas a compressão precisa respeitar a intenção original.
- T020 (complements): Um compressor aprendido pode ser condicionado à consulta; aprendizado e condicionamento são dimensões diferentes.

Afirmação rastreável:
RECOMP estuda compressores extrativos e abstrativos orientados ao desempenho posterior e permite contexto vazio quando não acrescenta utilidade.
Suporte: direct; fontes: V3A-S003
Limite: Os experimentos do artigo não justificam um limiar universal de descarte nem garantem cobertura de tarefas novas.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T037:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 abordou utilidade e pontes de evidência. Aqui compressão por consulta produz pacotes diferentes para resposta e verificação.

Projeto e decomposição
O leitor precisa de suporte suficiente; o verificador precisa também de contexto que possa desmentir a resposta. Usar um único recorte altamente favorável para ambos enfraquece auditoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

Controle adaptativo
Preserve identificadores e condições em faixa protegida, compactando explicações periféricas. A seleção deve poder retornar vazio sem obrigar o leitor a preencher uma resposta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

Validação contrafactual
Compare pacote único e pacote de verificação expandido. Meça respostas sustentadas, falsos aceites do verificador e custo adicional; avaliar perguntas cuja exceção fica fora da frase mais semelhante. Unidade de avaliação: consulta e documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

USO AVANÇADO — Resposta factual curta
Cenário: Documento longo contém um número condicionado.
Estratégia: Extrair número, unidade, população e período; manter parágrafo adjacente para verificar ressalvas.
Papel do modelo pequeno: 3–7B lê campos; 8–14B verifica escopo.
Aceite proposto: Nenhum valor pode ser citado sem seus qualificadores relevantes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

USO AVANÇADO — Comparação de argumentos
Cenário: Há evidências dos dois lados.
Estratégia: Produzir recortes separados de apoio e oposição, com ligação entre eles; não reduzir tudo a conclusão única.
Papel do modelo pequeno: 15–30B integra posições.
Aceite proposto: A síntese deve preservar objeção material presente na fonte.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S003, A-S018, V4A-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Extrator de spans diretamente ligados a campos da pergunta.
8–14B: Compressor que preserva relações e exceções em poucos documentos.
15–30B: Sintetizador de argumentos com pacote de auditoria separado.
Requisitos de treino/runtime: Consulta estável, alinhamento com origem e medição do par compressor-leitor; treinamento pode ser necessário para compressão abstrativa.
Não aplicar quando: Pergunta muda continuamente ou a seleção esconde contradições indispensáveis.

## T037:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C014 — Microsoft / Azure AI Search semantic ranker
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação descreve recurso comercial disponível.
Mecanismo documentado: Ranking secundário sobre resultados BM25/RRF, redução de campos e extração de captions.
Correspondência com esta base: Redução de entrada é relacionada, sem igualdade ao RECOMP.
Transferência proposta para modelo pequeno: Proposta de engenharia: Avaliar reranker pequeno com filtros e campo prioritário; manter cobertura de candidatos constante.
Limite: Disponibilidade não comprova escala de cliente; limites atuais do serviço não são universais. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S009.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q017, V4A-Q024.

## T037:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T037 → T200 [feeds]
Como combinar: Entregar ao verificador contexto ampliado e independente.
Interface: Resposta candidata, spans e vizinhança de fonte.
Condição: Verificador não ficar limitado ao recorte favorável.
Aceite proposto: Incluir exceção fora do span selecionado e exigir detecção.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S003, A-S018, V4A-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T037 → T015 [requires]
Como combinar: Manter acesso ao trecho integral.
Interface: Documento, revisão, offsets e tipo de transformação.
Condição: Referência permitir conferir paráfrases.
Aceite proposto: Abrir origem quando qualificador não estiver preservado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S003, A-S018, V4A-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não reutilizar compressão de pergunta diferente.
- Distinguir vazio por irrelevância de falha do compressor.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar precisão de qualificadores; leitor de fronteira pode compensar lacunas que 3–7B não consegue detectar.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T018, T036

## Fontes primárias associadas

### A-S018 — LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression

[https://arxiv.org/abs/2310.06839](https://arxiv.org/abs/2310.06839)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão voltada à informação relevante em contextos longos.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S003 — RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation

[https://arxiv.org/abs/2310.04408](https://arxiv.org/abs/2310.04408)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressores extrativo e abstrativo orientados à tarefa; possibilidade de retornar contexto vazio quando não agrega informação.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S009 — Semantic ranking in Azure AI Search

[https://learn.microsoft.com/en-us/azure/search/semantic-search-overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Ranking secundário, campos resumidos, limite de candidatos, BM25 e RRF.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T038 — Selective Context Pruning

**Nome canônico:** Selective Context Pruning  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T018  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** poda seletiva de contexto; Selective Context

## T038:C01 — conceito

Poda seletiva de contexto com base em uma medida de importância ou informação. É uma especialização de Context Pruning; Selective Context é também o nome de uma proposta de pesquisa sobre remoção de redundância. O critério concreto de seleção deve ser declarado, sem tratar todo texto previsível como dispensável.

Como funciona:
- Dividir o contexto em unidades selecionáveis.
- Atribuir pontuações segundo o método escolhido.
- Remover unidades abaixo do orçamento preservando dependências obrigatórias.

Nota de nomenclatura: Entrada mantida como variante do conceito geral T018; o método científico específico deve ser citado pelo título da fonte.

## T038:C02 — aplicacao

Quando usar:
- Entradas com passagens repetidas e baixa densidade informativa.
- Experimentos controlados de redução de prompt.

Quando não usar:
- Não excluir automaticamente frases comuns que expressem negação ou restrição essencial.

Implementação proposta:
- Proposta: registrar o seletor usado e os trechos removidos.
- Criar lista de invariantes que não podem desaparecer.
- Comparar poda por informação, por relevância e por regras em perguntas independentes.

Aplicação LAI proposta:
Proposta LAI: empregar inicialmente como opção de seleção auditável em documentação; não usar para descartar autorização, identificação de cliente ou decisão vigente.

## T038:C03 — riscos_validacao

Armadilhas:
- Previsibilidade estatística não equivale a inutilidade para a tarefa.
- Pontuação local pode ignorar relações entre frases distantes.

Métricas sugeridas:
- Retenção de invariantes e perda de qualidade.
- Razão de compressão e latência total.

Testes propostos:
- Inserir uma restrição em frase comum e exigir sua preservação.
- Avaliar casos em que a resposta depende de dois trechos cuja utilidade aparece somente em conjunto.

## T038:C04 — perguntas_proveniencia

Pergunta: Selective Context e qualquer poda seletiva são sinônimos exatos?
Resposta: Não. Um é uma proposta específica; o outro é um rótulo geral para várias políticas.

Pergunta: Um seletor pode ser usado sem treinamento?
Resposta: Sim. Há regras e escores que não exigem treinar o gerador, mas ainda precisam de avaliação.

Pergunta: Somar surpresa favorece unidades longas?
Resposta: Pode favorecer: a soma cresce com o número de tokens. A comparação precisa declarar agregação, tamanho e limiar utilizados.

Pergunta: LLMLingua-2 aplica exatamente o mesmo critério?
Resposta: Não. Formula retenção como classificação de tokens com aprendizado supervisionado e informação bidirecional; não é apenas outro limiar sobre surpresa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T038:C05 — mecanismo_avancado

No método Selective Context, a informação de um token é sua surpresa sob um modelo: I(x) = −log₂ P(x | prefixo), em bits. Pontuações podem ser agregadas em unidades lexicais antes do descarte. Isso mede improbabilidade contextual, não valor causal para a resposta. Uma condição previsível pode ter baixo escore, enquanto um erro de digitação raro recebe pontuação elevada.

Condição de contorno:
A transferência falha quando o modelo que estima probabilidades trata linguagem técnica ou idioma de forma muito diferente do gerador que lerá o resultado.

Contrato proposto:
- Entradas: Texto tokenizado, modelo de pontuação, unidade selecionável e orçamento de retenção.
- Saídas: Máscara de seleção com offsets, pontuações e motivos de preservação obrigatória.
- Estado: Tokenizer, definição de agregação, limiar e contexto usado no cálculo das probabilidades.
- Invariante: Uma unidade removida por baixa surpresa não é declarada semanticamente dispensável sem avaliação da tarefa.

Compromissos de projeto:
- Unidades maiores preservam sintaxe e tornam a seleção menos granular.
- Pontuação probabilística dispensa treinar o gerador, mas acrescenta inferência e pode privilegiar ruído incomum.

## T038:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma restrição frequente junto de códigos aleatórios sem utilidade. A avaliação deve revelar se a política prefere o ruído; regras obrigatórias precisam impedir a perda da restrição.

Plano de avaliação proposto:
Avaliação proposta: comparar surpresa, seleção por relevância e LLMLingua-2 sob o mesmo orçamento final. Medir retenção de condições, resposta sustentada, custo do seletor e degradação por idioma; controlar o tamanho das unidades para não atribuir seu efeito ao escore.

Comparações:
- T018 (specializes): O registro preserva a associação ao conceito geral de poda, detalhando um critério informacional específico.
- T020 (distinct_from): Um seletor treinado com rótulos de retenção aprende outra função; surpresa não equivale a probabilidade de relevância.

Afirmação rastreável:
Selective Context calcula auto-informação com um modelo causal e usa unidades lexicais para reduzir conteúdo considerado redundante.
Suporte: direct; fontes: A-S016
Limite: A interpretação como importância operacional é uma hipótese adicional; o artigo não transforma previsibilidade em garantia de inutilidade.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T038:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou surprisal e alias de poda. Aqui a seleção é estratificada por função textual para evitar viés contra unidades previsíveis.

Projeto e decomposição
Negações, unidades e operadores podem ser previsíveis linguisticamente e decisivos semanticamente. Separe seleção de tokens livres e proteção de classes funcionais relevantes à tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

Controle adaptativo
Calibre dentro de tipos de conteúdo, evitando que código, nomes raros ou OCR dominem score por surpresa. Alta perplexidade pode sinalizar ruído, não valor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

Validação contrafactual
Compare seleção global e estratificada com mesmo número de tokens. Meça perda de relação, erro em negação e excesso de ruído preservado; o alvo é utilidade do leitor, não surpresa média. Unidade de avaliação: bloco selecionado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

USO AVANÇADO — Especificação com fórmulas
Cenário: Símbolos curtos mudam condições.
Estratégia: Proteger operadores e unidades, selecionar explicação por relevância e verificar fórmula completa após compressão.
Papel do modelo pequeno: 3–7B lê estrutura validada.
Aceite proposto: Expressão resultante deve manter equivalência operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

USO AVANÇADO — Texto com OCR imperfeito
Cenário: Ruído recebe score elevado.
Estratégia: Detectar regiões suspeitas, conferir imagem ou original e impedir que a seleção priorize lixo por raridade.
Papel do modelo pequeno: 8–14B interpreta trecho corrigido.
Aceite proposto: Não aumentar taxa de erro por preservar caracteres corrompidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S016, V3A-S001, V4A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de spans com operadores protegidos por regras.
8–14B: Classificador de conteúdo útil versus ruído antes da seleção.
15–30B: Revisor de relações complexas quando poda por token for insuficiente.
Requisitos de treino/runtime: Tags funcionais e amostra de validação por tipo; manter relação com T018 como especialização, não algoritmo universal novo.
Não aplicar quando: Proteções ocupam quase toda janela ou linguagem comprimida fica ilegível para o consumidor.

## T038:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C025 — Microsoft / LLMLingua integrado ao Prompt flow
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação expõe ferramenta de compressão utilizável em fluxo.
Mecanismo documentado: Entrada de prompt e taxa alvo, conexão para probabilidades, saída textual comprimida.
Correspondência com esta base: Seleção de tokens pertence à família; mecanismo específico depende da versão.
Transferência proposta para modelo pequeno: Proposta de engenharia: Medir compressor mais leitor compacto; armazenar original e recuperar quando requisitos falharem.
Limite: Integração disponível não é uso operacional de cliente nem promessa de perda mínima. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S027.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q024.

## T038:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T038 → T018 [complements]
Como combinar: Usar estratos como política específica de poda.
Interface: Token, classe funcional, dependência e score.
Condição: Poda preservar fechamento das relações.
Aceite proposto: Testar frase previsível cuja negação muda a decisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V3A-S001, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T038 → T195 [complements]
Como combinar: Verificar expressão ou código após seleção.
Interface: Representação original e selecionada.
Condição: Existir propriedade executável adequada.
Aceite proposto: Detectar mudança de operador apesar de formato válido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S016, V3A-S001, V4A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar raridade como sinônimo de importância.
- Não tratar LLMLingua-2 e Selective Context como mesmo estimador.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar preservação de relações com tokens iguais; score do compressor não mede compreensão do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T006, T018, T039

## Fontes primárias associadas

### A-S016 — Compressing Context to Enhance Inference Efficiency of Large Language Models

[https://aclanthology.org/2023.emnlp-main.391/](https://aclanthology.org/2023.emnlp-main.391/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Selective Context: remoção de redundância no contexto de entrada.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S001 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression

[https://aclanthology.org/2024.findings-acl.57/](https://aclanthology.org/2024.findings-acl.57/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compressão extrativa treinada como classificação de tokens, com contexto bidirecional e distilação de dados.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S028 — LLMLingua Series

[https://www.microsoft.com/en-us/research/project/llmlingua/](https://www.microsoft.com/en-us/research/project/llmlingua/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Diferencia LLMLingua, LongLLMLingua e LLMLingua-2; página declara finalidade de demonstração de pesquisa.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

### V4A-S027 — LLMLingua Prompt Compression — Prompt flow

[https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html](https://microsoft.github.io/promptflow/integrations/tools/llmlingua-prompt-compression-tool.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Integração documentada de compressor e contrato de entrada/saída; não comprova carga real.

Limite: Não demonstra dez implantações bigtech nem desempenho de um pipeline local 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T039 — Importance-Aware Window

**Nome canônico:** Importance-Aware Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T039  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela orientada à importância

## T039:C01 — conceito

Janela de contexto que prioriza unidades pelo valor esperado para a tarefa, em vez de manter apenas as mais recentes. Importância pode combinar obrigatoriedade, relevância, impacto e recência. Esses critérios são decisões de engenharia; um escore de LLM não é uma medida objetiva de verdade.

Como funciona:
- Classificar unidades por papel e obrigatoriedade.
- Pontuar conteúdo opcional e considerar dependências.
- Escolher conjunto que caiba no orçamento preservando o essencial.

Nota de nomenclatura: Nome descritivo de uma política de seleção, não algoritmo universal ou benchmark estabelecido.

## T039:C02 — aplicacao

Quando usar:
- Missões longas com decisões antigas ainda relevantes.
- Histórico volumoso com poucos marcos decisivos.

Quando não usar:
- Não deixar permissões e restrições críticas dependerem exclusivamente de um escore probabilístico.

Implementação proposta:
- Proposta: separar conteúdo fixado por regra de conteúdo elegível a ranking.
- Registrar justificativa curta de inclusão e origem.
- Reavaliar importância quando objetivo ou estado da missão mudar.

Aplicação LAI proposta:
Proposta LAI: fixar decisões vigentes e evidências operacionais da Helena; usar ranking somente para material complementar e casos semelhantes.

## T039:C03 — riscos_validacao

Armadilhas:
- Autoavaliação do modelo pode dar peso excessivo à própria hipótese.
- A importância muda com o problema e não deve ser congelada para sempre.

Métricas sugeridas:
- Recall de fatos críticos antigos.
- Tokens usados por evidência efetivamente aproveitada na resposta.

Testes propostos:
- Colocar uma decisão antiga indispensável entre muitos eventos recentes.
- Alterar o objetivo e verificar que a seleção muda sem apagar o histórico.

## T039:C04 — perguntas_proveniencia

Pergunta: Importante significa verdadeiro?
Resposta: Não. Uma hipótese muito relevante ainda pode ser falsa e precisa manter seu status.

Pergunta: Preciso usar embeddings para medir importância?
Resposta: Não. Regras de domínio, tipo de evento e dependências podem ser mais apropriados para certos campos.

Pergunta: É adequado normalizar todos os escores juntos?
Resposta: Depende do significado e da distribuição de cada critério. Normalização por candidatos pode mudar prioridades quando novos itens entram.

Pergunta: Como evitar que uma memória acessada domine para sempre?
Resposta: Separe frequência de acesso, validade e novidade. Faça avaliações com fatos antigos pouco acessados que continuam necessários à tarefa.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T039:C05 — mecanismo_avancado

Selecionar por importância pode ser formulado como alocação de orçamento: maximizar utilidade estimada de unidades com custos em tokens. Entretanto, a utilidade raramente é aditiva. Uma definição e sua exceção podem ser úteis apenas juntas; dois exemplos quase idênticos competem pelo mesmo benefício. O seletor deve considerar dependências e redundância, além de pontuações individuais, para evitar escolher um conjunto aparentemente forte e logicamente incompleto.

Condição de contorno:
Quando a função de utilidade é mal calibrada, otimizar o ranking apenas torna mais consistente uma seleção equivocada de conteúdo.

Contrato proposto:
- Entradas: Unidades com custo, origem, status, dependências e escores separados por critério.
- Saídas: Conjunto selecionado e relatório das restrições preservadas e dependências não atendidas.
- Estado: Modelo de importância, pesos, histórico de acesso e orçamento efetivo da chamada.
- Invariante: Prioridade de leitura não altera confiança factual, autorização ou validade temporal de uma memória.

Compromissos de projeto:
- Escores combinados permitem adaptação, mas tornam difícil explicar qual critério excluiu uma evidência.
- Atualizar importância por acesso favorece continuidade e pode criar ciclos em que apenas lembranças já populares permanecem visíveis.

## T039:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: adicionar uma conclusão relevante e uma ressalva de baixo escore cuja remoção muda seu alcance. A seleção deve conservar a dependência ou recusar a conclusão isolada.

Plano de avaliação proposto:
Avaliação proposta: comparar recência, ranking individual e seleção com dependências sob orçamento igual. Medir cobertura de pares necessários, diversidade, custo de seleção e persistência de erros autorreforçados; testar mudança explícita de objetivo.

Comparações:
- T018 (complements): A poda executa a exclusão; importância fornece um dos critérios para decidir quais unidades podem sair.
- T040 (complements): O estado da tarefa fornece dependências obrigatórias que um ranking de importância sozinho pode desconhecer.

Afirmação rastreável:
Generative Agents combina critérios de recuperação para escolher memórias pertinentes ao comportamento simulado.
Suporte: related; fontes: A-S008
Limite: A evidência apoia seleção multifatorial em uma arquitetura específica, não uma função universal de importância operacional.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T039:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 formulou valor não aditivo. Aqui prioridades da janela incluem custo de reconstrução e risco de esquecimento de obrigações.

Projeto e decomposição
Calcule prioridade por necessidade imediata, custo de reabrir e impacto de omissão. Conteúdo fácil de recuperar pode sair antes de uma decisão rara que exige vários passos para reconstruir.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

Controle adaptativo
Use envelhecimento de prioridades para impedir que informação sempre citada monopolize janela. Fixação precisa de condição de liberação, ou a política deixa de administrar recursos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

Validação contrafactual
Compare prioridade por recência, frequência e custo de reconstrução. Meça retomadas, leituras adicionais e obrigações perdidas; manter iguais os limites de janela e saída. Unidade de avaliação: janela de execução.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

USO AVANÇADO — Diagnóstico longo
Cenário: Uma hipótese depende de evidência antiga cara.
Estratégia: Fixar evidência até testar a hipótese; liberar após registrar resultado e referência, não após mero número de turnos.
Papel do modelo pequeno: 8–14B gerencia hipóteses locais.
Aceite proposto: Não repetir investigação porque a evidência decisiva foi removida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

USO AVANÇADO — Projeto com várias frentes
Cenário: Assuntos recentes competem com decisão crítica.
Estratégia: Reservar espaço para contratos ativos e mover detalhes reabríveis; revisar prioridades quando a tarefa mudar.
Papel do modelo pequeno: 3–7B classifica blocos; 15–30B integra.
Aceite proposto: Decisão deve manter restrições mesmo com ruído recente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S006, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tipo e recuperabilidade de blocos.
8–14B: Controlador de hipóteses com liberação explícita de conteúdo fixado.
15–30B: Planejador entre frentes com custos de reconstrução diferentes.
Requisitos de treino/runtime: Metadados de dependência, custo de leitura e estados de obrigação; limites devem ser aplicados em código.
Não aplicar quando: Todos os blocos são declarados indispensáveis sem possibilidade de decompor a tarefa.

## T039:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T039:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T039 → T074 [feeds]
Como combinar: Usar prioridade para escolher conteúdo removível.
Interface: Valor, custo de recarga e condição de fixação.
Condição: Evicção não destruir única cópia durável.
Aceite proposto: Medir recargas e repetição de trabalho.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T039 → T040 [requires]
Como combinar: Recalcular importância após mudança de fase.
Interface: Estado atual, objetivo e contratos ativos.
Condição: Mudança de estado ser confirmada.
Aceite proposto: Cancelar hipótese e verificar liberação do bloco fixado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S006, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não premiar acesso causado pelo próprio ranking sem correção.
- Preservar conteúdo raro exigido por obrigação ativa.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade com igual janela; mais tokens de alta prioridade não significam raciocínio melhor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T018, T040, T048

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T040 — State-Aware Window

**Nome canônico:** State-Aware Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T040  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela orientada ao estado

## T040:C01 — conceito

Seleciona contexto segundo o estado atual da tarefa: etapa em andamento, dependências, ações pendentes e critérios de conclusão. Distingue o que foi concluído do que continua necessário. É uma política do runtime que depende de estado estruturado confiável.

Como funciona:
- Ler estado e versão da missão.
- Determinar informações necessárias à próxima transição.
- Compor janela com essas informações e histórico recente suficiente.

## T040:C02 — aplicacao

Quando usar:
- Workflows com etapas e pré-condições claras.
- Execuções que precisam retomar após falha sem repetir efeitos.

Quando não usar:
- Não usar um resumo narrativo não verificado como única fonte do estado.

Implementação proposta:
- Proposta: representar etapa, pendências, resultados e evidências em campos explícitos.
- Manter chamadas iniciadas e seus resultados em pares rastreáveis.
- Construir o contexto a partir de um snapshot consistente para evitar leitura de versões conflitantes.

Aplicação LAI proposta:
Proposta LAI: usar máquina de estados da missão como âncora da Helena; recuperar detalhes apenas das tarefas e contratos que condicionam a próxima ação.

## T040:C03 — riscos_validacao

Armadilhas:
- Estado atrasado pode omitir uma ação ainda pendente.
- O agente pode marcar uma etapa como concluída antes de validar seu resultado.

Métricas sugeridas:
- Transições inválidas e ações duplicadas.
- Contexto necessário por etapa e sucesso na retomada.

Testes propostos:
- Interromper entre executar ferramenta e confirmar resultado e verificar reconciliação.
- Criar dependência não satisfeita e impedir que ela desapareça da janela.

## T040:C04 — perguntas_proveniencia

Pergunta: Estado estruturado substitui o histórico?
Resposta: Não. Ele representa o momento atual; o histórico permite auditar e reconstruir como o estado foi obtido.

Pergunta: O estado deve ser editado livremente pela LLM?
Resposta: A LLM pode propor atualizações; o runtime valida transições, versões e evidências antes de persistir.

Pergunta: O último timestamp basta para detectar conflito?
Resposta: Nem sempre. Relógios e resolução temporal podem esconder concorrência. Prefira revisões ou condições de escrita definidas pelo armazenamento.

Pergunta: Uma ferramenta pode terminar depois do cancelamento?
Resposta: Pode. Preserve o resultado tardio e reconcilie seu efeito; não trate o cancelamento local como prova de que o serviço parou.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T040:C05 — mecanismo_avancado

Uma janela orientada ao estado deve registrar a revisão usada para montar a requisição. Enquanto o modelo responde, outro ator pode concluir uma etapa, cancelar uma missão ou atualizar uma dependência. O contexto gerado continua coerente com sua leitura, mas pode estar desatualizado para executar a ação seguinte. A proposta de transição precisa ser revalidada contra o estado atual antes de produzir efeitos.

Condição de contorno:
O mecanismo não resolve concorrência apenas por usar JSON: leituras consistentes e regras de transição precisam existir no armazenamento ou controlador.

Contrato proposto:
- Entradas: Snapshot identificado, etapa pretendida, dependências e operações externas ainda sem confirmação.
- Saídas: Contexto específico da transição e revisão que deverá ser conferida no momento de aplicá-la.
- Estado: Versão do workflow, tentativas em andamento, resultados observados e agenda de próximas ações.
- Invariante: Uma decisão calculada sobre estado antigo não sobrescreve silenciosamente atualizações posteriores.

Compromissos de projeto:
- Janelas por etapa reduzem ruído e acoplam montagem de contexto ao modelo de execução.
- Revalidar versões evita decisões obsoletas, mas pode exigir nova geração quando há muita concorrência.

## T040:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: atualizar uma pré-condição enquanto a chamada ao modelo está em curso. A resposta antiga deve ser rejeitada ou reavaliada antes da transição, preservando o novo estado.

Plano de avaliação proposto:
Avaliação proposta: comparar histórico recente e contexto por transição em tarefas concorrentes. Medir decisões obsoletas aceitas, repetição de geração, cobertura de pendências e tempo de conclusão; variar atraso entre leitura e aplicação.

Comparações:
- T065 (complements): Controle transacional pode proteger aplicação de propostas calculadas com uma versão conhecida.
- T060 (complements): Checkpoint fornece estado e agenda de retomada, mas não valida sozinho efeitos externos.

Afirmação rastreável:
Os checkpoints do LangGraph incluem valores de estado, próximos nós e tarefas, além de identificadores de execução.
Suporte: related; fontes: V3A-S031
Limite: Usar esses campos para montar uma janela por transição é uma proposta de arquitetura, não um comportamento automático do mecanismo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T040:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu revisão antes de efeitos. Aqui contexto é uma projeção tipada por estado, com transições que determinam quais informações mudam de função.

Projeto e decomposição
Defina vistas para coletar, verificar e executar. Evidência incompleta pode ser suficiente para coletar, mas não para confirmar ação; a mudança de fase altera requisitos do contexto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

Controle adaptativo
Registre por que cada campo entrou na vista. Quando objetivo muda, recalcule relevância e mantenha obrigações transversais; não preserve automaticamente todos os detalhes da fase anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

Validação contrafactual
Compare janela uniforme e vistas por estado. Meça ações prematuras, repetição de coleta e perda de restrições em transições, incluindo resultados tardios de ferramentas. Unidade de avaliação: transição de tarefa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

USO AVANÇADO — Preparação de alteração
Cenário: Agente passa de análise para edição.
Estratégia: Na análise, carregar hipóteses; na execução, exigir especificação confirmada, revisão-base e teste de aceite. Bloquear salto sem esses campos.
Papel do modelo pequeno: 3–7B verifica checklist estruturado.
Aceite proposto: Nenhuma edição pode usar revisão-base desconhecida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

USO AVANÇADO — Investigação interrompida
Cenário: Nova informação invalida plano.
Estratégia: Voltar a estado de análise, marcar plano anterior como suspenso e reconstruir contexto com evidência nova.
Papel do modelo pequeno: 15–30B replaneja; 8–14B valida.
Aceite proposto: Não executar etapa pendente do plano revogado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S030, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Validador de campos obrigatórios por estado, com máquina de estados externa.
8–14B: Gerador de propostas locais dentro da fase autorizada.
15–30B: Replanejador de transições complexas com justificativa de mudança.
Requisitos de treino/runtime: Máquina de estados, revisões e contratos de entrada por fase; prompt não substitui validação do controlador.
Não aplicar quando: Estado é inferido apenas da conversa e não existe registro confiável das transições.

## T040:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T040:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T040 → T065 [requires]
Como combinar: Confirmar transição e suas pré-condições juntas.
Interface: Estado anterior, revisão, evento e estado proposto.
Condição: Transação cobrir invariantes locais.
Aceite proposto: Simular duas transições concorrentes e rejeitar a obsoleta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T040 → T043 [complements]
Como combinar: Compactar por fases encerradas.
Interface: Fronteira de fase, obrigações ativas e referências.
Condição: Resumo não ocultar requisito da próxima fase.
Aceite proposto: Retomar execução com evidência obrigatória ausente e exigir bloqueio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S030, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar mensagem do modelo como confirmação de estado.
- Distinguir intenção de executar e execução observada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar correção de transições sob interrupções; capacidade linguística não substitui estado explícito.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T024, T060, T064, T065

## Fontes primárias associadas

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S029 — Transaction Isolation

[https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Níveis de isolamento e anomalias de concorrência, incluindo serialização.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S031 — LangGraph Checkpointers

[https://docs.langchain.com/oss/python/langgraph/checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoints por super-step, StateSnapshot e pending writes de tarefas concluídas; estado de execução e retomada.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V3A-S030 — LangGraph Fault tolerance

[https://docs.langchain.com/oss/python/langgraph/fault-tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reexecução de nós, fronteiras de checkpoints, chaves idempotentes e resultado desconhecido quando falta confirmação externa.

Limite: Documentação dinâmica consultada nesta data. APIs e comportamento dependem da versão instalada; nenhum runtime foi executado ou alterado nesta pesquisa.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T041 — Last-N Messages Window

**Nome canônico:** Last-N Messages Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T041  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela das últimas mensagens

## T041:C01 — conceito

Mantém as últimas N mensagens, preservando separadamente instruções obrigatórias. É a forma mais simples de janela móvel. N mede mensagens, não tokens: uma única resposta de ferramenta pode ser maior que dezenas de mensagens de conversa.

Como funciona:
- Definir o que conta como mensagem ou turno.
- Selecionar o sufixo recente sem quebrar interações estruturadas.
- Anexar estado essencial e referências ao histórico arquivado.

## T041:C02 — aplicacao

Quando usar:
- Protótipos e conversas de mensagens curtas.
- Baseline para comparar políticas de contexto mais sofisticadas.

Quando não usar:
- Não é suficiente para limitar tokens quando o tamanho das mensagens varia muito.

Implementação proposta:
- Proposta: definir janela em turnos completos quando houver ferramentas.
- Aplicar um teto de tokens adicional.
- Persistir decisões que continuam válidas fora da janela e recuperar detalhes antigos quando referenciados.

Aplicação LAI proposta:
Proposta LAI: usar como componente de histórico recente, sem confundir com memória durável ou política de planejamento da Helena.

## T041:C03 — riscos_validacao

Armadilhas:
- Uma mensagem longa pode ultrapassar o limite sozinha.
- N mensagens podem cortar uma pergunta, mantendo apenas sua resposta.

Métricas sugeridas:
- Tokens máximos por chamada.
- Esquecimento de fatos anteriores à janela.

Testes propostos:
- Gerar uma mensagem de ferramenta muito longa e exigir proteção por orçamento.
- Colocar uma decisão no turno N+1 anterior e confirmar preservação no estado essencial.

## T041:C04 — perguntas_proveniencia

Pergunta: N=20 significa vinte trocas completas?
Resposta: Só se o runtime definiu assim. É necessário distinguir mensagens individuais e turnos.

Pergunta: É melhor aumentar N sempre?
Resposta: Não. Isso aumenta custo e pode adicionar ruído; a escolha deve seguir avaliação de qualidade e orçamento.

Pergunta: Reexecutar o corte deve produzir o mesmo resultado?
Resposta: Sim, se histórico, N e regras forem iguais. Novas mensagens ou mudanças de agrupamento devem explicar qualquer diferença.

Pergunta: Como detectar exclusão persistente acidental?
Resposta: Compare o histórico armazenado antes e depois da montagem. Uma política de apresentação não deveria apagar eventos sem contrato explícito.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T041:C05 — mecanismo_avancado

O tamanho N depende da serialização da conversa. Uma resposta do assistente pode conter várias chamadas paralelas, seguidas por resultados em mensagens separadas; outro backend pode agrupar resultados. Assim, N constante não preserva a mesma interação entre provedores. A política deve operar sobre unidades conversacionais definidas e gerar uma visão para a chamada, distinguindo esse corte de uma exclusão persistente no estado.

Condição de contorno:
Se o histórico é altamente assimétrico ou ferramentas produzem muitas mensagens intermediárias, contar mensagens passa a refletir detalhes do protocolo mais que contexto útil.

Contrato proposto:
- Entradas: Histórico ordenado, definição de turno e vínculos entre chamadas e resultados de ferramentas.
- Saídas: Sufixo válido para o provedor, acompanhado de decisão explícita sobre arquivamento e persistência.
- Estado: Sequência de eventos, IDs de mensagens e política de agrupamento de interações.
- Invariante: Aplicar uma visão limitada não elimina o histórico original por consequência não declarada.

Compromissos de projeto:
- Contagem de mensagens é simples de explicar e pouco estável diante de mudanças de protocolo.
- Agrupar interações evita pares quebrados e faz o tamanho efetivo variar em relação ao N nominal.

## T041:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: emitir três chamadas paralelas no mesmo turno e cortar entre seus resultados. O montador deve manter a unidade necessária ou indicar a impossibilidade de caber no orçamento.

Plano de avaliação proposto:
Avaliação proposta: comparar N mensagens, N turnos e orçamento por tokens no mesmo histórico lógico serializado de formas diferentes. Medir validade protocolar, contexto útil preservado e tokens reais; separar perda por corte de perda por persistência indevida.

Comparações:
- T003 (specializes): FIFO define a política de saída dos antigos; Last-N especifica uma medida particular da capacidade.
- T042 (complements): O limite em tokens pode impedir que um sufixo válido exceda a capacidade efetiva.

Afirmação rastreável:
LangChain distingue estratégias de corte, remoção de mensagens do estado e substituição por resumos.
Suporte: direct; fontes: A-S003
Limite: Exemplos de middleware podem modificar o estado; não se deve presumir que toda função chamada trim cria apenas uma visão temporária.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T041:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrou variabilidade de mensagens. Aqui Last-N é um baseline controlado e uma política por classe de interação.

Projeto e decomposição
Escolha N por classe de diálogo usando distribuição real de mensagens e densidade de informação. Uma conversa com ferramentas extensas não deve compartilhar configuração com chat curto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Controle adaptativo
Reinicie a seleção recente após mudança confirmada de objetivo, conservando contratos ativos fora da fila. A janela não deve importar detalhes de assunto antigo só porque ainda estão entre os últimos turnos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Validação contrafactual
Compare N fixo, N por classe e janela por tokens com o mesmo teto máximo. Meça requisitos antigos esquecidos, custo médio e picos; não usar apenas conversas sem interrupções. Unidade de avaliação: conversa com mudança de tema.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Atendimento com questões independentes
Cenário: Usuário muda de assunto várias vezes.
Estratégia: Detectar mudança explícita, carregar identidade e preferências necessárias e limitar histórico do assunto anterior.
Papel do modelo pequeno: 3–7B classifica tema.
Aceite proposto: Não reutilizar resposta ou entidade do tema abandonado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Fluxo de extração repetitiva
Cenário: Cada turno processa um item novo.
Estratégia: Manter instrução fixa e poucos exemplos recentes, arquivando resultados em tabela fora da janela.
Papel do modelo pequeno: 8–14B trata exceções.
Aceite proposto: Itens anteriores não podem contaminar campos do item atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tema com janela curta e instrução estável.
8–14B: Leitor de poucas interações que incluem correções locais.
15–30B: Supervisor de mudanças de objetivo, usando referências ao histórico quando necessário.
Requisitos de treino/runtime: Agrupamento por turnos lógicos e perfil de tamanho; ajuste de N não requer treino do modelo.
Não aplicar quando: Dependências antigas são frequentes e não existe mecanismo separado para obrigações ou recuperação.

## T041:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T041:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T041 → T042 [complements]
Como combinar: Aplicar teto de tokens à seleção Last-N.
Interface: Turnos elegíveis, custo real e reserva.
Condição: Grupos de protocolo permanecerem completos.
Aceite proposto: Testar uma única mensagem maior que o orçamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T041 → T047 [requires]
Como combinar: Manter fatos duráveis fora da fila recente.
Interface: Preferência confirmada, escopo e origem.
Condição: Persistência não ser inferida da presença recente.
Aceite proposto: Retomar fato após ele sair dos últimos N turnos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar mensagens de sistema e ferramenta como unidades equivalentes.
- Não concluir que conteúdo arquivado será lembrado automaticamente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Usar Last-N como controle simples; comparar retenção de obrigações e custo, sem atribuir ganho cognitivo ao tamanho N.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T042, T050

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

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


---

# T043 — Context Compaction

**Nome canônico:** Context Compaction  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T043  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** compactação de contexto

## T043:C01 — conceito

Reorganiza um histórico extenso em uma representação operacional menor para continuar a execução. Pode combinar síntese, poda e externalização. Uma boa compactação conserva objetivo, decisões vigentes, pendências e referências; não deve fingir que todos os detalhes sobrevivem.

Como funciona:
- Capturar um ponto consistente do histórico e estado.
- Produzir pacote compacto com campos obrigatórios.
- Persistir originais e substituir a entrada ativa somente após validação.

## T043:C02 — aplicacao

Quando usar:
- Sessões que se aproximam do limite de contexto.
- Retomada de missões longas em nova chamada ou processo.

Quando não usar:
- Não usar compactação como substituto de log completo quando a tarefa exige auditabilidade.

Implementação proposta:
- Proposta: incluir versão, objetivo, concluído, pendente, riscos e evidências.
- Marcar explicitamente o que não foi lido ou foi truncado.
- Manter a compactação anterior até concluir a gravação da nova e verificar invariantes.

Aplicação LAI proposta:
Proposta LAI: gerar checkpoints compactos da Helena acompanhados dos eventos que os originaram; retomada exige ler esse estado antes de continuar.

## T043:C03 — riscos_validacao

Armadilhas:
- Uma síntese pode converter suspeita em conclusão.
- IDs, versões ou proibições antigas podem desaparecer durante a reescrita.

Métricas sugeridas:
- Redução de tokens e retenção de campos críticos.
- Taxa de retomada correta após vários ciclos.

Testes propostos:
- Compactar um histórico com correção de decisão e exigir a versão vigente.
- Interromper a gravação e verificar disponibilidade do checkpoint anterior.

## T043:C04 — perguntas_proveniencia

Pergunta: Compactação é uma memória permanente?
Resposta: Não necessariamente. Ela é uma representação reduzida; persistência e recuperação precisam ser implementadas.

Pergunta: Posso confiar em uma compactação sem referências?
Resposta: Ela serve como pista, mas não como prova suficiente de execução ou resultado.

Pergunta: Uma compactação precisa ser textual?
Resposta: Não obrigatoriamente. Pode combinar campos estruturados, trechos literais e referências; a representação precisa ser consumível pelo runtime.

Pergunta: Como recuperar detalhe omitido?
Resposta: Use referências ao prefixo original e reabra o trecho necessário. A síntese deve orientar a busca, não substituir a evidência em casos ambíguos.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T043:C05 — mecanismo_avancado

Uma compactação pode ser tratada como uma nova projeção de um prefixo fechado do histórico. Ela deve declarar até qual evento cobre e quais mensagens posteriores permanecem literais; sem essa fronteira, o sistema pode duplicar fatos ou perder eventos que chegaram durante a síntese. A troca do contexto ativo deve publicar a projeção completa somente depois de verificar referências, pendências e cobertura.

Condição de contorno:
Se o histórico continua recebendo escritas sem uma fronteira identificável, não é possível saber com segurança o que a nova compactação já incorporou.

Contrato proposto:
- Entradas: Prefixo identificado, estado vigente, política de retenção e eventos posteriores separados.
- Saídas: Pacote compacto com marcador de cobertura, referências e incertezas preservadas.
- Estado: Versão anterior, fonte original, configuração do compactador e geração em preparação.
- Invariante: Toda informação posterior à fronteira continua disponível até ser incorporada explicitamente em outra revisão.

Compromissos de projeto:
- Compactar menos vezes preserva mais detalhes, mas pode aproximar a chamada do limite.
- Compactações frequentes reduzem pressão da janela e acumulam erros de síntese e custo de processamento.

## T043:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma correção durante a geração do resumo e publicar a compactação anterior a ela. A montagem seguinte deve incluir a correção literal, evitando que a síntese antiga prevaleça.

Plano de avaliação proposto:
Avaliação proposta: comparar compactação por tamanho e por fronteiras de tarefa com várias rodadas. Medir perda de correções, duplicação, cobertura de eventos e retomada; incluir custos de geração, releitura das fontes e invalidação de cache.

Comparações:
- T004 (complements): Resumos encadeados podem compor compactação, mas exigem controle de cobertura e propagação de erros.
- T016 (distinct_from): Truncar ou limpar um resultado remove conteúdo; não produz necessariamente uma representação resumida dele.

Afirmação rastreável:
A Anthropic descreve compactação por síntese do histórico e diferencia essa técnica de notas estruturadas e limpeza de resultados de ferramentas.
Suporte: direct; fontes: A-S006, V3A-S008
Limite: O protocolo de fronteira e publicação aqui descrito é uma proposta editorial; não é uma garantia de todo produto de compactação.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T043:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 protegeu commit de compactação. Aqui o resumo é um contrato de retomada adaptado ao próximo consumidor e à fase da tarefa.

Projeto e decomposição
Defina campos mínimos por tarefa: objetivo vigente, decisões confirmadas, evidências, pendências e próximos testes. A compactação deve produzir um estado utilizável, não apenas narrativa da conversa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Controle adaptativo
Teste o resumo com um leitor diferente do autor antes de usá-lo em fluxos críticos. Se o consumidor não consegue identificar próximo passo e condições de parada, reabrir conteúdo específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

Validação contrafactual
Compare retomada pelo mesmo modelo e por outro porte. Meça ações corretas após a fronteira, fatos reinterpretados e leituras adicionais; resumo que só seu autor entende é contrato frágil. Unidade de avaliação: ponto de retomada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Troca de modelo por custo
Cenário: Fronteira inicia e modelo local continua.
Estratégia: Gerar pacote com decisões explícitas e exemplos de formato, retirar pressupostos tácitos e validar uma etapa de retomada.
Papel do modelo pequeno: 3–7B executa subtarefa; 15–30B resume integração.
Aceite proposto: Consumidor deve reproduzir restrições sem inventar decisões omitidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

USO AVANÇADO — Sessão longa de desenvolvimento
Cenário: Histórico contém tentativas descartadas.
Estratégia: Guardar tentativas rejeitadas com motivo verificável, para que nova sessão não repita caminho inútil. Separar falha observada de hipótese não testada.
Papel do modelo pequeno: 8–14B retoma diagnóstico.
Aceite proposto: Medir repetição de tentativas já refutadas e preservação do teste pendente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V4A-S002, A-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de estado estruturado com próximo passo delimitado.
8–14B: Autor e leitor de pacote de retomada por módulo.
15–30B: Integrador de decisões cruzadas e conflitos ainda abertos.
Requisitos de treino/runtime: Schema de retomada, revisão-base e teste de leitura por consumidor; preservar artefatos independentes do resumo.
Não aplicar quando: Não é possível representar obrigações essenciais e fontes no orçamento disponível.

## T043:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 1; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C003 — Anthropic / Claude Code: compaction e memória entre sessões
Evidência: produção documentada; correspondência exata do mecanismo. Organização: laboratório de IA — contado separadamente.
Domínio observado: aplicação com LLM.
Uso observado: Cookbook oficial afirma uso em produção de compactação e sistemas complementares de memória no Claude Code.
Mecanismo documentado: Redução da conversa e persistência de informação reutilizável fora da janela.
Correspondência com esta base: Compactação implementada no produto é explicitada.
Transferência proposta para modelo pequeno: Proposta de engenharia: Treinar leitor pequeno para retomar pacote estruturado; testar obrigações antigas após compactação.
Limite: Não revela todos os algoritmos, nem prova que armazenamento de notas torna conclusões corretas. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S002, A-S006.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T043:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T043 → T211 [feeds]
Como combinar: Publicar pacote de retomada como handoff.
Interface: Objetivo, decisões, testes, artefatos e revisão.
Condição: Pacote corresponder à fronteira confirmada.
Aceite proposto: Retomar em sessão limpa sem acesso à conversa anterior.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T043 → T055 [complements]
Como combinar: Carregar procedimento específico para a fase seguinte.
Interface: Procedimento versionado e pré-condições.
Condição: Resumo não substituir contrato de execução.
Aceite proposto: Verificar que instrução operacional completa foi aberta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V4A-S002, A-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não condensar resultados de ferramenta incertos como sucesso.
- Não confundir reflexão interna com registro factual de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar continuidade após troca de consumidor; compactação não preserva automaticamente capacidade de planejamento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T004, T006, T021, T060

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S022 — Persistence

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers para estado por thread; stores para dados duráveis entre threads.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S008 — Context editing

[https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Remoção seletiva de resultados de ferramentas, placeholders, preservação configurável e interação com invalidação de prompt cache.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T044 — Progressive Context Expansion

**Nome canônico:** Progressive Context Expansion  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T044  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** expansão progressiva de contexto

## T044:C01 — conceito

Começa com contexto suficiente para orientar a tarefa e amplia a informação conforme surgem lacunas verificáveis. É o movimento complementar ao carregamento progressivo: a expansão precisa ter motivo, orçamento e condição de parada, não apenas adicionar cada vez mais texto.

Como funciona:
- Iniciar com objetivo, estado e evidência de maior valor.
- Identificar lacunas ou referências que precisam ser abertas.
- Buscar detalhe adicional e revisar a suficiência do contexto.

## T044:C02 — aplicacao

Quando usar:
- Perguntas cuja profundidade necessária não é conhecida antecipadamente.
- Análise de incidentes que começa por sintomas e segue dependências.

Quando não usar:
- Não reduzir a entrada inicial a ponto de ocultar restrições obrigatórias ou identidade da tarefa.

Implementação proposta:
- Proposta: manter lista explícita de perguntas não respondidas.
- Abrir fontes por referência exata antes de expandir semanticamente quando possível.
- Limitar rodadas e encerrar com lacunas declaradas se nenhuma nova evidência surgir.

Aplicação LAI proposta:
Proposta LAI: usar índice, ficha técnica e fonte original como níveis sucessivos; informações obrigatórias continuam carregadas desde o começo.

## T044:C03 — riscos_validacao

Armadilhas:
- Expansão pode virar loop de busca sem progresso.
- Um modelo confiante pode não perceber que faltam premissas.

Métricas sugeridas:
- Ganho de cobertura por rodada.
- Tokens e chamadas extras até evidência suficiente.

Testes propostos:
- Criar uma pergunta que exige abrir um documento citado e conferir a expansão.
- Fornecer buscas repetidas sem informação nova e exigir parada controlada.

## T044:C04 — perguntas_proveniencia

Pergunta: Mais contexto sempre melhora a resposta?
Resposta: Não. A expansão deve resolver uma lacuna identificada, pois dados extras também introduzem ruído.

Pergunta: Quem decide que a evidência é suficiente?
Resposta: Uma política de cobertura e verificação, auxiliada pelo modelo; confiança textual isolada não basta.

Pergunta: Como estimar o valor da próxima busca?
Resposta: Use o tipo de lacuna, custo e histórico de tentativas. É uma heurística operacional que precisa ser comparada com expansão fixa.

Pergunta: Quando expandir o documento em vez da coleção?
Resposta: Quando a lacuna é local, como uma definição ou ressalva próxima. Ausência de identidade ou fonte independente pode exigir busca mais ampla.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T044:C05 — mecanismo_avancado

A expansão pode escolher entre abrir uma referência exata, aumentar a região de um documento ou iniciar nova busca. Essas ações têm custos e riscos diferentes. Uma política útil associa cada ação a uma lacuna: identidade ambígua, premissa ausente ou contradição. O progresso é redução verificável dessa lacuna, não crescimento de tokens nem confiança retórica do modelo após mais leitura.

Condição de contorno:
Um agente pode permanecer confiante apesar de uma premissa falsa; gatilhos baseados apenas em incerteza do gerador não detectam todos os casos que precisam expandir.

Contrato proposto:
- Entradas: Lista de lacunas, contexto atual, referências disponíveis e orçamento restante de busca e leitura.
- Saídas: Nova evidência vinculada à lacuna ou registro de tentativa sem resolução.
- Estado: Consultas já feitas, fontes abertas, versões e razões de parada.
- Invariante: Repetir a mesma evidência não conta como confirmação independente nem como ganho de cobertura.

Compromissos de projeto:
- Expansão sob demanda evita leitura desnecessária e acrescenta latência sequencial.
- Abrir fontes vizinhas conserva escopo; novas buscas ampliam cobertura e aumentam risco de desvio temático.

## T044:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: fornecer evidência que responde metade de uma comparação e resultados repetidos para a outra metade. O agente deve identificar cobertura parcial e parar após esgotar a política, sem completar por analogia.

Plano de avaliação proposto:
Avaliação proposta: comparar recuperação única, expansão fixa e expansão por lacunas com orçamento máximo igual. Medir cobertura incremental, custo por lacuna resolvida e encerramentos justificados; incluir casos de alta confiança com premissa ausente.

Comparações:
- T014 (complements): Carregamento progressivo define níveis disponíveis; expansão escolhe quando percorrê-los por necessidade concreta.
- T067 (complements): Recuperação ativa oferece gatilhos e consultas durante a geração, compondo uma política de expansão.

Afirmação rastreável:
FLARE antecipa a continuação textual e usa baixa confiança em tokens para acionar recuperação e regeneração.
Suporte: direct; fontes: V3A-S010
Limite: É um mecanismo específico de acionamento; confiança do modelo não equivale a uma prova geral de suficiência da evidência.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T044:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 expandiu por lacuna. Aqui a ordem de abertura considera valor esperado de informação e custo de verificar hipóteses.

Projeto e decomposição
Associe cada abertura a uma decisão que pode mudar. Abrir mais documentos sem hipótese de utilidade aumenta contexto e latência sem necessariamente reduzir incerteza.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

Controle adaptativo
Escolha primeiro a fonte com maior poder de discriminar alternativas, respeitando autoridade e custo. Se o resultado não mudar as opções, revise a hipótese antes de repetir busca semelhante.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

Validação contrafactual
Compare expansão por top-k e por lacuna discriminante. Meça decisões alteradas por abertura, leituras redundantes e tempo até evidência suficiente; incluir fontes indisponíveis. Unidade de avaliação: sequência de aberturas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

USO AVANÇADO — Diagnóstico de erro
Cenário: Duas causas levam a correções diferentes.
Estratégia: Abrir o log ou configuração que distingue causas, depois carregar código correspondente; não ler todo o repositório antecipadamente.
Papel do modelo pequeno: 8–14B escolhe teste discriminante.
Aceite proposto: Cada expansão deve reduzir alternativas ou justificar insuficiência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

USO AVANÇADO — Consulta de política
Cenário: Uma exceção pode mudar a regra.
Estratégia: Abrir seção de exceções antes de resposta conclusiva, mantendo versão e escopo da regra principal.
Papel do modelo pequeno: 3–7B identifica condição; 15–30B integra.
Aceite proposto: Não afirmar regra absoluta sem verificar exceção aplicável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S030, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Detector de campo obrigatório ausente e seletor de referência exata.
8–14B: Planejador de uma abertura discriminante por vez.
15–30B: Coordenador de hipóteses múltiplas com limite de custo.
Requisitos de treino/runtime: Representação de lacunas e alternativas, referências estáveis e contabilização por abertura.
Não aplicar quando: O acervo não contém informação discriminante ou o sistema não consegue avaliar progresso.

## T044:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C019 — GitHub / Microsoft / Copilot semantic repository indexing
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Documentação oferece índice semântico para Chat e cloud agent.
Mecanismo documentado: Busca de seções de código por significado e atualização do índice.
Correspondência com esta base: Busca sob demanda relacionada à expansão.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar 3–7B para formular consulta e 8–14B para explicar trecho com revisão do commit.
Limite: Não comprova Git-backed memory do agente nem AST chunking; índices podem atrasar. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S023.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T044:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T044 → T078 [feeds]
Como combinar: Transformar falta semântica explícita em evento de carga.
Interface: Campo ausente, decisão afetada e candidatos.
Condição: Rótulo de falta ter critério verificável.
Aceite proposto: Recuperar conteúdo irrelevante e impedir encerramento falso da lacuna.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T044 → T218 [complements]
Como combinar: Detectar repetição de expansões sem progresso.
Interface: Referências visitadas e alternativas restantes.
Condição: Equivalência de buscas ser observável.
Aceite proposto: Repetir consultas parafraseadas e exigir mudança de estratégia.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S030, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não interpretar volume lido como progresso.
- Parar quando nenhuma abertura plausível puder alterar a decisão.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar resolução de hipóteses com custo de leitura; modelos maiores podem escolher aberturas melhores, exigindo medição local.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T026, T067, T078

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S010 — Active Retrieval Augmented Generation

[https://arxiv.org/abs/2305.06983](https://arxiv.org/abs/2305.06983)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: FLARE usa previsão da próxima sentença e sinais de confiança para decidir consultas e regeneração.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### C-S030 — How we built our multi-agent research system

[https://www.anthropic.com/research/multi-agent-research-system](https://www.anthropic.com/research/multi-agent-research-system)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Arquitetura coordenador-especialistas e contextos separados pode paralelizar pesquisa e usar artefatos de transferência.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T045 — Tool Retrieval

**Nome canônico:** Tool Retrieval  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T045  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** descoberta de ferramentas; tool search

## T045:C01 — conceito

Busca ferramentas apropriadas em um catálogo e carrega seus schemas quando necessários. A recuperação seleciona capacidades; a execução continua sujeita a contrato e autorização. Descobrir uma ferramenta não autoriza usá-la nem prova que o serviço está disponível.

Como funciona:
- Indexar nome, descrição, entradas, saídas e restrições da ferramenta.
- Pesquisar pelo objetivo e selecionar candidatas.
- Carregar definição completa, validar argumentos e só então executar.

## T045:C02 — aplicacao

Quando usar:
- Catálogos extensos que não cabem economicamente no contexto.
- Sistemas com ferramentas especializadas de muitos serviços.

Quando não usar:
- Não ocultar a própria ferramenta de descoberta nem capacidades essenciais para recuperar o catálogo.

Implementação proposta:
- Proposta: manter versões e exemplos de intenção nos metadados.
- Aplicar filtros de permissão antes de apresentar candidatos.
- Testar descoberta por paráfrases e diferenciação de ferramentas com nomes parecidos.

Aplicação LAI proposta:
Proposta LAI: oferecer à Helena catálogo de capacidades e carregar contratos específicos antes da chamada; manter separadas descoberta, autorização e execução.

## T045:C03 — riscos_validacao

Armadilhas:
- Descrição vaga faz a ferramenta correta parecer irrelevante.
- Recuperar schema antigo pode gerar argumentos incompatíveis.

Métricas sugeridas:
- Recall de ferramentas adequadas por tarefa.
- Tokens de schemas carregados e chamadas inválidas.

Testes propostos:
- Pedir uma operação sem mencionar o nome da ferramenta e avaliar seleção.
- Revogar permissão e garantir que a ferramenta não seja executada por ter sido recuperada anteriormente.

## T045:C04 — perguntas_proveniencia

Pergunta: Tool retrieval é apenas busca vetorial?
Resposta: Não. Busca lexical, filtros, regras e combinações também podem servir.

Pergunta: Ferramentas adiadas precisam existir no servidor?
Resposta: Sim. Adiar o schema no contexto não cria uma implementação nem elimina requisitos do provedor.

Pergunta: Resultado vazio significa que a capacidade não existe?
Resposta: Significa ausência de correspondência nessa busca. Descrição ruim, filtro ou consulta inadequada também podem ocultar uma ferramenta existente.

Pergunta: A referência pode substituir o schema para sempre?
Resposta: Não. Ela precisa ser resolvida por um contrato compatível. Sua existência não garante versão, permissão ou disponibilidade da implementação.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T045:C05 — mecanismo_avancado

Adiar uma ferramenta no contexto não significa remover sua definição do transporte ao servidor. Na implementação documentada pela Anthropic, o catálogo completo continua no parâmetro de ferramentas; a busca devolve referências expandidas para o modelo. Assim, economia de contexto e redução de bytes enviados são métricas distintas. O mecanismo também precisa diferenciar busca sem correspondência, falha da busca e ferramenta descoberta mas indisponível.

Condição de contorno:
Quando o catálogo é pequeno e quase todas as ferramentas serão usadas, o custo e a latência de descoberta podem superar a economia na janela.

Contrato proposto:
- Entradas: Catálogo completo e versionado, consulta de capacidade e restrições da sessão.
- Saídas: Referências resolvíveis e schemas compatíveis, ou resultado explícito de ausência ou falha.
- Estado: Ferramentas já carregadas, versão do catálogo e disponibilidade verificada no momento da chamada.
- Invariante: Um nome recuperado só pode ser executado com definição conhecida e validação vigente de argumentos.

Compromissos de projeto:
- Carregar poucas ferramentas reduz competição de descrições e introduz uma etapa adicional.
- Preservar o catálogo completo no servidor simplifica resolução, mas mantém custos de transporte e governança do catálogo.

## T045:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover uma definição mantendo sua referência em resultados antigos. A chamada deve detectar a incompatibilidade; não deve inventar parâmetros nem substituir por ferramenta parecida.

Plano de avaliação proposto:
Avaliação proposta: comparar catálogo integral e descoberta com tarefas de uma e várias ferramentas. Medir recall de capacidade, tentativas inválidas, tokens ativos, bytes transmitidos e latência; separar erro de seleção de indisponibilidade do serviço.

Comparações:
- T014 (specializes): A ferramenta é uma unidade específica de carregamento progressivo com schema executável.
- T015 (complements): Referências economizam representação somente quando o resolvedor pode obter a definição correspondente.

Afirmação rastreável:
Tool search retorna referências que a API expande; definições adiadas continuam incluídas no catálogo enviado nas requisições.
Suporte: direct; fontes: A-S038
Limite: Esse contrato pertence à implementação documentada da Anthropic; um catálogo customizado pode usar transporte e expansão diferentes.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T045:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu schemas adiados. Aqui busca de ferramentas é avaliada como descoberta de capacidade e compatibilidade operacional.

Projeto e decomposição
Indexe finalidade, entradas necessárias, efeitos e limites. Nome parecido não basta: ferramenta de consultar e ferramenta de modificar podem atender palavras iguais com consequências diferentes.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

Controle adaptativo
Depois da recuperação, valide que argumentos disponíveis satisfazem schema e que capacidade está habilitada. Se faltar dado obrigatório, coletá-lo antes de tentar chamada e reparo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

Validação contrafactual
Compare catálogo integral e recuperação em tarefas com ferramentas raras e versões concorrentes. Meça seleção correta, chamadas inviáveis e custo de carregar schemas não usados. Unidade de avaliação: seleção de ferramenta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

USO AVANÇADO — Catálogo empresarial amplo
Cenário: Agente conhece intenção mas não ferramenta.
Estratégia: Recuperar poucas capacidades, comparar efeitos e pré-condições e carregar contrato completo da escolhida.
Papel do modelo pequeno: 3–7B roteia capacidades.
Aceite proposto: Nenhuma ferramenta de escrita deve ser escolhida para pedido apenas de leitura.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

USO AVANÇADO — Ferramentas versionadas
Cenário: Dois schemas têm campos diferentes.
Estratégia: Resolver versão elegível, mapear argumentos a partir de dados observados e rejeitar preenchimento inventado.
Papel do modelo pequeno: 8–14B constrói chamada.
Aceite proposto: Chamada deve validar no schema efetivamente carregado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S038, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Selector de capacidades descritas por metadados contrastivos.
8–14B: Construtor de argumentos para poucas ferramentas elegíveis.
15–30B: Planejador de composição entre ferramentas quando dependências exigirem várias etapas.
Requisitos de treino/runtime: Registry versionado, filtros de disponibilidade e validação de argumentos; treino de tool use depende do modelo.
Não aplicar quando: Ferramenta não está disponível ou o catálogo não distingue efeitos e pré-condições.

## T045:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T045:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T045 → T158 [requires]
Como combinar: Recuperar somente capacidades registradas e habilitadas.
Interface: tool_id, versão, efeitos e disponibilidade.
Condição: Registry ser fonte autorizada do contrato.
Aceite proposto: Remover ferramenta e impedir chamada por lembrança do modelo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S038, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T045 → T170 [requires]
Como combinar: Fixar versão após descoberta.
Interface: Schema, revisão e compatibilidade dos argumentos.
Condição: Versão não mudar silenciosamente entre seleção e execução.
Aceite proposto: Alterar campo obrigatório e exigir revalidação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S038, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não confundir busca sem resultado com catálogo vazio.
- Não executar a partir de descrição resumida quando schema falta.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar sucesso de chamada válida e seleção de efeitos; bom ranking textual não demonstra uso correto de ferramentas.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T014, T151, T158, T170

## Fontes primárias associadas

### A-S038 — Tool search tool

[https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Descoberta de ferramentas e carregamento adiado de schemas no contexto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.


---

# T046 — Dynamic Few-Shot Selection

**Nome canônico:** Dynamic Few-Shot Selection  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T046  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** seleção dinâmica de demonstrações

## T046:C01 — conceito

Escolhe exemplos de demonstração para cada consulta, conforme similaridade, diversidade, dificuldade e orçamento. Adapta o comportamento mostrado ao modelo sem atualizar pesos. Os exemplos devem ensinar a tarefa e não vazar a resposta do conjunto de avaliação.

Como funciona:
- Manter banco de exemplos com entrada, saída validada e metadados.
- Selecionar exemplos relevantes para a nova tarefa.
- Limitar redundância e compor prompt com ordem controlada.

## T046:C02 — aplicacao

Quando usar:
- Muitas classes ou formatos de solicitação.
- Tarefas em que exemplos estáticos ocupam contexto sem ajudar a pergunta atual.

Quando não usar:
- Não selecionar demonstrações com saídas não verificadas apenas porque se parecem semanticamente com a consulta.

Implementação proposta:
- Proposta: indexar exemplos por tarefa, versão de schema e idioma.
- Aplicar diversidade ou cotas para incluir exceções úteis.
- Separar exemplos de treino, desenvolvimento e teste por origem documental.

Aplicação LAI proposta:
Proposta LAI: selecionar exemplos de extração e ferramentas já aprovados conforme a missão, preservando casos de erro e ausência de dados.

## T046:C03 — riscos_validacao

Armadilhas:
- Exemplos quase idênticos reduzem cobertura de comportamentos.
- Mudança de schema pode tornar demonstrações antigas nocivas.

Métricas sugeridas:
- Qualidade por classe e orçamento de exemplos.
- Ganho sobre seleção fixa e aleatória com mesmo número de tokens.

Testes propostos:
- Consultar uma classe rara e verificar presença de uma demonstração válida.
- Alterar schema de saída e impedir seleção de exemplos incompatíveis.

## T046:C04 — perguntas_proveniencia

Pergunta: Isso é fine-tuning?
Resposta: Não. Os exemplos entram no contexto de cada chamada; os parâmetros do modelo permanecem iguais.

Pergunta: O exemplo mais parecido é sempre o melhor?
Resposta: Não. Diversidade e cobertura de exceções podem ser mais úteis que repetição de um caso quase idêntico.

Pergunta: É preciso recuperar entrada e saída juntas?
Resposta: A busca pode usar a entrada, mas a demonstração final precisa de saída validada e compatível. Não busque por uma resposta de teste desconhecida.

Pergunta: Mais diversidade sempre ajuda?
Resposta: Não. Exemplos desconectados podem confundir a tarefa. Compare diversidade condicionada ao objetivo com similaridade pura usando o mesmo orçamento.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T046:C05 — mecanismo_avancado

A seleção dinâmica altera a distribuição das demonstrações vista a cada pergunta. Buscar vizinhos muito semelhantes pode concentrar uma classe e induzir o modelo a tratá-la como resposta padrão. A ordem também é parte do experimento: manter exemplos selecionados e variar sua sequência pode modificar resultados. Um banco de exemplos precisa registrar origem para que duplicatas de um mesmo documento não atravessem as divisões de avaliação.

Condição de contorno:
Similaridade de superfície é insuficiente quando exemplos parecidos exigem decisões diferentes por uma exceção, versão de schema ou condição negativa.

Contrato proposto:
- Entradas: Consulta, exemplos validados, origem documental e política de cobertura por tarefa.
- Saídas: Demonstrações elegíveis com ordem, orçamento e justificativa de seleção registrados.
- Estado: Encoder, banco versionado, divisões por origem e histórico de revisão das saídas.
- Invariante: Exemplos de avaliação e suas variantes derivadas não entram no banco usado para avaliá-los.

Compromissos de projeto:
- Vizinhos semânticos aproximam a demonstração da pergunta e podem reduzir diversidade de decisões.
- Controlar classe, dificuldade e ordem melhora diagnóstico, mas torna a seleção mais complexa e menos puramente baseada em distância.

## T046:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar vizinhos quase idênticos com rótulos distintos por uma única condição. O seletor deve conservar exemplos que mostrem a fronteira, sem escolher todos de uma classe.

Plano de avaliação proposto:
Avaliação proposta: comparar exemplos fixos, aleatórios e recuperados com tokens equivalentes. Variar ordem separadamente, medir desempenho por classe e estabilidade, e fazer divisão por documento ou origem; não atribuir ganho de quantidade ao algoritmo de seleção.

Comparações:
- T019 (complements): Poda reduz o conjunto de demonstrações; seleção dinâmica determina quais são úteis para a consulta atual.
- T005 (distinct_from): Uma demonstração orienta comportamento, enquanto uma resposta em cache tenta reutilizar um resultado já produzido.

Afirmação rastreável:
Pesquisas sobre exemplos em contexto investigam seleção por similaridade e mostram sensibilidade à ordem das demonstrações.
Suporte: direct; fontes: V3A-S016, V3A-S017
Limite: Os resultados dependem de modelos e tarefas estudados; uma ordenação favorável não transfere automaticamente para outro modelo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T046:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou viés e vazamento. Aqui seleção de exemplos é orientada por necessidade de habilidade e custo de interferência.

Projeto e decomposição
Recupere exemplos pelo tipo de transformação necessário, não apenas pelo assunto. Uma pergunta sobre finanças pode precisar de exemplo de extração temporal, não de narrativa financeira.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

Controle adaptativo
Separe exemplos de formato, decisão e exceção. Escolher vários exemplos da mesma função pode reforçar estilo e deixar a dificuldade real sem demonstração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

Validação contrafactual
Compare similaridade semântica e cobertura de habilidades com orçamento igual. Meça erros de transferência de entidade, rótulo e valor dos exemplos para o caso novo. Unidade de avaliação: consulta com demonstrações.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

USO AVANÇADO — Extração variável
Cenário: Documentos diferem em layout e ambiguidade.
Estratégia: Selecionar um exemplo de formato e outro da exceção relevante; substituir nomes e valores somente quando isso não alterar o mecanismo demonstrado.
Papel do modelo pequeno: 3–7B aprende formato local.
Aceite proposto: Não copiar valores do exemplo para a saída real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

USO AVANÇADO — Tarefas com ferramentas
Cenário: Modelo confunde ordem de operações.
Estratégia: Selecionar demonstração com a mesma dependência entre chamadas, preservando diferenças de schema da ferramenta atual.
Papel do modelo pequeno: 8–14B planeja sequência curta.
Aceite proposto: Argumentos e versão devem vir do caso atual, não da demonstração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S016, V3A-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Poucas demonstrações contrastivas por habilidade fechada.
8–14B: Exemplos de sequência e tratamento de insuficiência.
15–30B: Demonstrações de integração de evidências sem depender de nomes do domínio.
Requisitos de treino/runtime: Banco de exemplos com metadados de habilidade e origem; particionar avaliação por fonte para evitar quase duplicatas.
Não aplicar quando: Exemplos disponíveis são contraditórios ou incompatíveis com o protocolo atual.

## T046:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q003, V4A-Q016.

## T046:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T046 → T019 [complements]
Como combinar: Remover demonstrações redundantes após selecionar habilidades.
Interface: Lista de exemplos, função e custo de tokens.
Condição: Todas as habilidades necessárias continuarem cobertas.
Aceite proposto: Excluir exemplo e testar fronteira que ele representava.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T046 → T036 [requires]
Como combinar: Extrair necessidade de habilidade da consulta.
Interface: Transformação, restrições e formato esperado.
Condição: Análise não depender da resposta desconhecida.
Aceite proposto: Testar assunto parecido com habilidade diferente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S016, V3A-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não selecionar pelo gabarito de avaliação.
- Não usar exemplos antigos de ferramenta como contrato atual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar transferência de habilidade em casos novos; mais exemplos semelhantes podem aumentar cópia indevida.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T019, T155, T204

## Fontes primárias associadas

### A-S031 — SemanticSimilarityExampleSelector

[https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector](https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector)

Consulta: 2026-11-05; estado: `search_result`.

Sustenta: Seleção de exemplos por similaridade semântica.

Limite: Resultado de busca e módulo oficial consultados; abertura direta rejeitada por content-type text/markdown.

### V3A-S016 — What Makes Good In-Context Examples for GPT-3?

[https://arxiv.org/abs/2101.06804](https://arxiv.org/abs/2101.06804)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Seleção de demonstrações por recuperação de exemplos semelhantes; comportamento depende do conjunto e do modelo.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V3A-S017 — Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity

[https://aclanthology.org/2022.acl-long.556/](https://aclanthology.org/2022.acl-long.556/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Sensibilidade à ordem de demonstrações e não transferência automática de uma boa permutação entre modelos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
