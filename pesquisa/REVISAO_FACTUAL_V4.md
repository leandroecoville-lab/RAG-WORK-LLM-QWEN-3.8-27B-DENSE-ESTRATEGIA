# Revisão documental e decisões da consolidação

Foram revisados os **98 registros de casos de origem**, com fontes primárias e profundidade declarada em cada auditoria. Eles representam 93 casos canônicos após deduplicação. Isso não equivale a testar implantações nem a certificar cada frase das 287 bases.

| Revisão | Decisão final |
|---|---|
| A→D | Quatro achados tratados: fonte primária Mooncake adicionada; streaming limitado a family; configurações Phi delimitadas por época. Novos mapeamentos Mooncake explicitamente apoiados na leitura direta da raiz. |
| A→C | Cinco achados tratados pelo autor antes de congelar. Auditor conferiu delta: oito relações exact→family em sete casos; não houve mudança das classes operacionais. |
| B→A | Sem falso positivo material nas alegações centrais examinadas. Duplicatas Claude Research, Rufus e Bing agrupadas; mais dois aliases conservadores da raiz documentados. |
| C→B | Removidas associações indevidas T197/T206 de V4B-C022. Observação opcional de promover SuffixDecoding a produto não aplicada: conserva-se o recorte de pesquisa do registro, sem promover evidência de implantação. |
| A→tail | P012/P015 repetiam material anterior. Foram reescritas e seu delta recebeu nova auditoria; dois achados de novidade materialmente resolvidos. |

Os relatórios originais permanecem em `revisoes/`. Seus hashes foram confrontados com os insumos. Alguns ainda registram achados abertos no snapshot histórico; a resolução final está neste documento e em `REVISAO_FACTUAL_V4.json`, com as alterações por campo em `PROVENIENCIA_V4.json`.

## Limites e alcance

- Revisão documental de registros e mecanismos centrais; não certifica cada frase nem implementação ou métricas das empresas.
- Os relatórios identificam snapshots originais. Correções finais estão em PROVENIENCIA_V4.json; novos detalhes de Mooncake foram lidos pela raiz.
- As 287 estratégias de engenharia não foram experimentadas com modelos 3–30B.
- Nenhum ganho de performance, paridade de fronteira ou ausência absoluta de erro é certificado.

## Decisões adicionais

- Domínio de implantação explícito, separando sistemas sem LLM de aplicações/serving/treino de LLM.
- Rastreabilidade de dez fichas corrigida com sete buscas adicionais reais, sem alterar retroativamente consultas congeladas.
- Casos e fontes suplementares não transformam métricas de replay em telemetria de produção.

Insumos congelados e históricos destinam-se à auditoria. Para ingestão, use somente o corpus consolidado, evitando incorporar versões anteriores à correção.
