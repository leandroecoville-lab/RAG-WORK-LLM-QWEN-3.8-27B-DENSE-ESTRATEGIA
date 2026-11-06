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
