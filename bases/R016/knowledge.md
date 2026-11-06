# R016 — Lost in the Middle

**Nome canônico:** Lost in the Middle: How Language Models Use Long Contexts  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R016  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** efeito de posição em contexto longo; lost-in-the-middle effect

## R016:C01 — conceito

Lost in the Middle avalia como a posição da evidência afeta modelos de linguagem em perguntas sobre múltiplos documentos e recuperação de pares chave-valor. Nos experimentos publicados, a informação no início ou fim frequentemente foi mais bem utilizada que no meio. O resultado é um alerta experimental sobre uso efetivo de contexto, não uma lei universal para todo modelo atual.

Como funciona:
- Mover a mesma evidência pelo contexto permite separar disponibilidade de informação e capacidade de utilizá-la.
- Aumentar distratores pode elevar o comprimento sem acrescentar informação útil; a janela aceita não mede compreensão.

Nota de nomenclatura: Primeira submissão em 2023; não é benchmark atual do checkpoint ou servidor do usuário.

## R016:C02 — aplicacao

Quando usar:
- Desenho de avaliações de RAG, montagem de contexto e comparação de modelos com janelas extensas.

Quando não usar:
- Para concluir, sem teste, que determinado modelo falha sempre no meio ou que evidências finais são universalmente melhores.

Implementação proposta:
- Proposta: construir perguntas com resposta verificável e evidência identificada, mantendo fixos pergunta e conteúdo relevante.
- Variar sistematicamente posição, comprimento e quantidade de distratores; controlar truncamento e orçamento de saída.
- Comparar contexto completo, recuperação seletiva e diferentes ordenações usando o mesmo checkpoint e configuração de geração.

Aplicação LAI proposta:
Proposta LAI: usar uma bateria de posições como critério para escolher o orçamento e a ordenação do contexto no RAG da Helena.

## R016:C03 — riscos_validacao

Armadilhas:
- Mover documentos pode mudar relações entre trechos; controlar essa variável antes de atribuir tudo à posição.
- Uma resposta correta por conhecimento prévio pode esconder que o modelo ignorou a evidência fornecida.

Métricas sugeridas:
- Acerto por posição relativa, suporte das citações, degradação com distratores e tokens consumidos por resposta correta.

Testes propostos:
- Proposta: incluir fatos sintéticos ou versões contraditórias controladas para exigir uso do material apresentado.
- Testar também ausência de evidência e múltiplas evidências necessárias; registrar variância entre execuções e falhas de truncamento.

## R016:C04 — perguntas_proveniencia

Pergunta: Uma janela maior garante recuperação melhor?
Resposta: Não. O estudo mostra que aceitar mais tokens e utilizar a evidência corretamente são propriedades diferentes.

Pergunta: Basta colocar tudo importante no final?
Resposta: Isso é uma hipótese de ordenação a testar. Evidência distribuída, dependências e o modelo escolhido podem alterar o resultado.

Pergunta: Devo colocar toda evidência importante no começo e no fim?
Resposta: Não existe regra universal. Isso pode duplicar tokens e não resolver relações complexas. Teste a montagem no modelo e tarefa efetivamente usados.

Pergunta: Uma janela maior elimina a necessidade de recuperação?
Resposta: Não necessariamente. Recuperação pode selecionar conteúdo útil mesmo quando tudo caberia; compare qualidade e custo sob condições controladas.

Escopo das fontes:
Resumo e metadados da versão arXiv foram consultados novamente em 2026-11-05. As observações pertencem aos modelos e tarefas estudados; a bateria proposta não foi executada no ambiente LAI.

## R016:C05 — mecanismo_avancado

O valor metodológico de Lost in the Middle está no controle de posição: manter a evidência e mudar sua localização permite testar utilização, em vez de apenas disponibilidade. Para uma avaliação atual, posição absoluta e relativa precisam ser separadas do comprimento total e da quantidade de distratores. Reordenar trechos também pode alterar relações entre eles, portanto a intervenção deve preservar o conteúdo e a estrutura necessária à pergunta.

Condição de contorno:
A tendência observada não é lei universal de toda arquitetura ou modelo atual; tarefas de agregação e múltiplas evidências podem apresentar padrões diferentes de recuperação pontual.

Contrato proposto:
- Entradas: Contextos controlados, evidência identificada, posições alternativas e configuração fixa do modelo.
- Saídas: Desempenho por posição e comprimento, com registro de evidência realmente utilizada na resposta.
- Estado: Versão do modelo, ordem dos trechos, geração de distratores e divisão independente de avaliação.
- Invariante: Aceitar o tamanho da entrada não é interpretado como capacidade uniforme de utilizar toda a informação contida nela.

Compromissos de projeto:
- Mover evidência ajuda diagnosticar atenção efetiva e pode introduzir mudanças de vizinhança que precisam controle.
- Encurtar contexto reduz distratores e também pode remover apoio necessário a tarefas de combinação.

## R016:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: deslocar a mesma evidência entre início, meio e fim, mantendo demais elementos equivalentes. Se o acerto variar, a avaliação deve reportar dependência posicional, sem explicar a diferença por ausência da informação.

Plano de avaliação proposto:
Avaliação proposta: comparar posições em vários comprimentos e tarefas, com amostras novas e configurações iguais. Medir resposta sustentada, variabilidade e custo; separar localização de uma evidência de combinação de várias, sem usar perguntas do benchmark como conteúdo do RAG.

Comparações:
- T013 (complements): Capacidade efetiva de contexto exige medir uso da informação, além do limite nominal do modelo.
- T028 (complements): Reranking e montagem podem alterar posição da evidência, mas precisam ser avaliados sem ocultar condições relevantes.

Afirmação rastreável:
O artigo observa degradação quando evidência relevante fica no meio de contextos longos nos modelos e tarefas estudados.
Suporte: direct; fontes: A-S019
Limite: Os resultados pertencem ao estudo publicado; RULER também evidencia a necessidade de avaliar capacidades distintas, sem estabelecer posição ótima universal.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R016:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 discutiu posição da evidência. Aqui a avaliação distingue efeito de posição, competição entre evidências e organização estrutural do contexto.

Projeto e decomposição
Mover evidência sem alterar conteúdo permite investigar posição; adicionar distrações investiga competição. Misturar as duas intervenções impede saber por que a resposta mudou.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

Controle adaptativo
Compare agrupamento por fonte e por afirmação mantendo citações e condições. Evidência no começo pode parecer forte apenas porque recebe rótulo mais claro ou é repetida.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

Validação contrafactual
Construa avaliações próprias por modelo e quantização, sem importar perguntas de benchmark. Meça acerto por posição absoluta, posição relativa e comprimento, além de sensibilidade a múltiplas evidências necessárias. Unidade de avaliação: pacote de contexto controlado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

USO AVANÇADO — Montagem de contexto RAG
Cenário: Informação decisiva pode ficar enterrada.
Estratégia: Ordenar por requisitos e inserir índice curto, mantendo detalhes originais; comparar com ordem aleatória sem duplicar evidência.
Papel do modelo pequeno: 3–7B lê pacotes curtos.
Aceite proposto: Ganho deve persistir quando posição e quantidade de tokens são controladas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

USO AVANÇADO — Tarefa de múltiplos saltos
Cenário: Resposta depende de dois trechos distantes.
Estratégia: Agrupar trechos relacionados por ID de requisito e testar se leitor combina ambos; não assumir que colocar um no fim resolve integração.
Papel do modelo pequeno: 8–14B integra; 15–30B compara baseline.
Aceite proposto: Nenhuma conclusão pode depender de apenas um dos elos necessários.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S019, V3A-S015, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor com evidência compacta e organização explícita por campo.
8–14B: Leitor de pacotes moderados testado em diferentes posições.
15–30B: Leitor de contexto amplo após medir robustez a distração e relações distantes.
Requisitos de treino/runtime: Controle experimental de posição, comprimento e repetição; resultados dependem de modelo, tarefa e configuração.
Não aplicar quando: O sistema toma Lost in the Middle como lei universal ou presume que todos os modelos atuais reproduzem o mesmo perfil.

## R016:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q018, V4A-Q024.

## R016:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R016 → T024 [complements]
Como combinar: Empacotar evidências por requisito com ordem testável.
Interface: Afirmação, trechos, posição e referências.
Condição: Builder registrar ordem efetivamente enviada.
Aceite proposto: Reordenar sem mudar conteúdo e medir decisão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S019, V3A-S015, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R016 → T013 [requires]
Como combinar: Avaliar janela efetiva no consumidor concreto.
Interface: Modelo, tokenizer, comprimento e distribuição de evidências.
Condição: Teste cobrir carga relevante do produto.
Aceite proposto: Comparar posições sob o mesmo orçamento total.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S019, V3A-S015, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não repetir a evidência para fabricar ganho de posição.
- Não extrapolar um resultado histórico para todos os modelos 3–30B.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar robustez a posição com dados idênticos; vantagem numa configuração não prova capacidade geral de longo contexto.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T013, T018, T028, T037, T039, T222

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

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
