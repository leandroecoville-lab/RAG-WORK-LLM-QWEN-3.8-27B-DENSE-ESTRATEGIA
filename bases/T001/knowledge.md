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
