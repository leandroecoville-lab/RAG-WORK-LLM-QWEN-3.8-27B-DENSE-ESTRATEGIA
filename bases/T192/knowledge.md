# T192 — Self-Refine

**Nome canônico:** Self-Refine  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T192  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** autorefino

## T192:C01 — conceito

Refinamento iterativo em que o mesmo modelo gera uma saída, produz feedback e a revisa. O método estudado não exige treinamento adicional durante o ciclo. Pode corrigir problemas visíveis no texto, mas o crítico pode compartilhar os mesmos erros e critérios incompletos do gerador.

Como funciona:
- Gerar versão inicial com objetivo e restrições explícitos.
- Pedir feedback específico sobre defeitos observáveis.
- Produzir revisão e comparar com os critérios e a versão anterior.

## T192:C02 — aplicacao

Quando usar:
- Textos, planos ou artefatos que admitem melhoria por crítica localizada.
- Há rubrica capaz de distinguir melhora de mera reescrita.

Quando não usar:
- Tratar autocrítica como prova independente de fatos ou de execução.

Implementação proposta:
- Usar rubrica curta com critérios verificáveis.
- Limitar rodadas e conservar melhor versão avaliada.
- Encerrar quando não houver melhoria específica ou surgirem regressões.

Aplicação LAI proposta:
Proposta: usar autorefino para clareza e organização de artefatos da Helena, combinando testes e fontes externos para critérios objetivos.

## T192:C03 — riscos_validacao

Armadilhas:
- Revisão pode remover informação correta ou tornar texto apenas mais convincente.
- Modelo pode inventar defeitos para justificar uma nova rodada.

Métricas sugeridas:
- Melhorias aceitas por critério e regressões introduzidas.
- Custo por revisão útil e número de rodadas sem progresso.

Testes propostos:
- Fornecer versão inicial já correta e testar se ela permanece preservada.
- Inserir defeito conhecido e verificar se feedback o localiza e a revisão o corrige.

## T192:C04 — perguntas_proveniencia

Pergunta: Self-Refine treina o modelo?
Resposta: Não no procedimento descrito; modifica saídas dentro da execução.

Pergunta: É auditoria independente?
Resposta: Não. O mesmo modelo pode repetir seus próprios pontos cegos.

Pergunta: Mais rodadas significam mais inteligência útil?
Resposta: Não. Elas podem gerar oscilação, redundância ou regressão; acompanhe mudança real no objetivo.

Pergunta: Como detectar ausência de progresso?
Resposta: Compare defeitos pendentes e resultados externos entre versões; paráfrases e aumento de detalhes não contam automaticamente como melhoria.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T192:C05 — mecanismo_avancado

Feedback útil precisa identificar um defeito acionável e um critério de melhoria. Comentários genéricos podem apenas alongar a próxima resposta. Como proposta, conserve a versão anterior, registre mudanças e rejeite revisões que perdem requisitos já satisfeitos. O mesmo modelo pode alternar preferências entre rodadas; repetir até declarar satisfação não demonstra convergência para correção.

Condição de contorno:
Em tarefas que exigem informação nova, revisão sem ferramenta ou fonte adicional pode reorganizar o mesmo erro com mais confiança.

Contrato proposto:
- Entradas: Saída inicial, rubrica, limites de revisão e evidências acessíveis.
- Saídas: Versão escolhida acompanhada das mudanças relevantes e pendências.
- Estado: Histórico, críticas específicas, requisitos preservados e orçamento.
- Invariante: Nenhuma revisão é considerada melhor apenas porque é posterior ou mais longa.

Compromissos de projeto:
- Iterações podem corrigir defeitos locais e aumentar custo.
- Guardar versões permite regressão controlada e exige comparação por critérios consistentes.

## T192:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: começar com resposta correta e fornecer uma crítica equivocada produzida pelo próprio modelo. Esperar que a avaliação independente identifique a regressão e preserve ou restaure a versão anterior.

Plano de avaliação proposto:
Plano proposto: comparar geração única, revisão livre e revisão com rubrica em problemas independentes. Medir melhorias, regressões, comprimento e custo; aceitar o procedimento apenas quando o saldo de correção externa supera os danos introduzidos.

Comparações:
- T190 (alternative): Verifier loop exige critério de aceitação explícito; Self-Refine pode operar somente com feedback do mesmo modelo.

Afirmação rastreável:
Self-Refine utiliza o mesmo LLM para gerar, criticar e refinar saídas sem treinamento adicional durante o procedimento.
Suporte: direct; fontes: C-S045
Limite: A fonte relata resultados de tarefas específicas, não uma garantia de autoavaliação confiável.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T192:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu críticas acionáveis e preservação da versão anterior. Esta camada distingue melhoria de apresentação de correção factual e define quando incorporar evidência externa ao refinamento.

Critério antes da crítica
Defina o que pode melhorar: clareza, cobertura de requisitos, correção ou concisão. O mesmo modelo pode editar estilo de modo útil e continuar incapaz de detectar um erro factual. Não misture essas dimensões num pedido genérico para 'melhorar tudo', que dificulta medir progresso.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

Feedback com evidência
Peça localização do defeito e motivo verificável. Quando a crítica exige conhecimento ausente, busque fonte ou ferramenta antes da revisão. O trabalho sobre limites de autocorreção alerta que feedback interno não substitui sinal externo; uma nova resposta mais confiante pode ser apenas outra hipótese.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

Seleção entre versões
Conserve versões e escolha pela rubrica, permitindo manter a inicial. Uma revisão pode satisfazer um requisito e perder outro; avalie o conjunto completo no fim. Limite alterações ao escopo autorizado e pare quando mudanças adicionais não oferecem benefício observado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

USO AVANÇADO — Texto de domínio
Cenário: A informação já foi verificada, mas a apresentação está ruim.
Estratégia: Forneça uma rubrica de clareza e requisitos imutáveis. Peça revisão e compare se fatos, números e citações foram preservados.
Papel do modelo pequeno: Um 3–7B pode melhorar forma de textos curtos com conteúdo estável.
Aceite proposto: Medir preservação factual e cumprimento de requisitos, sem premiar comprimento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

USO AVANÇADO — Resposta parcialmente correta
Cenário: O avaliador externo aponta falhas específicas.
Estratégia: Use feedback localizado para revisar o mínimo necessário e reexecute checagens. Se não houver sinal externo, registre a revisão como hipótese.
Papel do modelo pequeno: Um 8–14B pode refinar soluções especializadas com ferramentas, sujeito à validação.
Aceite proposto: A versão escolhida deve corrigir falha observada sem criar regressões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S045, V3B-S019, V4C-S009.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Bom candidato para ajustes de forma e erros estreitos; autocorreção geral não é presumida.
8–14B: Contexto suficiente para requisitos e diferenças entre versões ajuda a reduzir regressões.
15–30B: Um 15–30B pode revisar problemas maiores, mas continua sujeito a vieses compartilhados com a geração.
Requisitos de treino/runtime: Workflow em runtime, sem atualização persistente de pesos. Aprendizagem exige outro ciclo explícito.
Não aplicar quando: Não tratar a declaração 'agora está correto' do próprio modelo como evidência de melhoria.

## T192:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Pesquisa de refinamento e casos de revisão industrial consultados. AutoClean fornece exemplo de feedback externo; não é classificado como prova de autocorreção puramente interna.
Consultas registradas: V4B-Q011.

## T192:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T192 → T190 [complements]
Como combinar: Um loop com verificador externo transforma críticas em condições de aceite.
Interface: Versões e falhas específicas.
Condição: Verificador examina a revisão final.
Aceite proposto: Comparar refinamento interno e refinamento com evidência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S045, V3B-S019, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T192 → T205 [complements]
Como combinar: Testes de equivalência ajudam a preservar significado durante edição.
Interface: Observáveis, tolerâncias e versões.
Condição: Critério de equivalência adequado à tarefa.
Aceite proposto: Detectar mudanças de números, unidades ou efeitos laterais.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S045, V3B-S019, V4C-S009. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Manter a opção de rejeitar a revisão e conservar o original.
- Não interpretar maior fluência como maior correção.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare revisões com avaliação cega e critérios separados. Self-Refine pode melhorar uma resposta específica, mas não demonstra que repetição interna aproxima indefinidamente um modelo pequeno da fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T190, T199, T200

## Fontes primárias associadas

### C-S045 — Self-Refine: Iterative Refinement with Self-Feedback

[https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: O próprio modelo gera, critica e revisa sem treino adicional no procedimento descrito.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S019 — Large Language Models Cannot Self-Correct Reasoning Yet

[https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Limites empíricos da autocorreção intrínseca sem feedback externo.

Limite: Estudo de modelos e tarefas específicos; não é impossibilidade universal ou avaliação de modelos atuais do usuário.

### V4C-S009 — Using AI to Delete Code: Agentic Tech Debt Cleanup at Uber

[https://www.uber.com/us/en/blog/ai-code-cleanup/](https://www.uber.com/us/en/blog/ai-code-cleanup/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: AutoClean operacional combina agentes, PolyglotPiranha via MCP, CI, fixers delimitados, verificações estáticas e CodeCourt por propriedades.

Limite: Fonte primária aberta. Desempenho relatado pertence ao sistema e ao período descritos; não foi reproduzido e não comprova transferência para modelos 3–30B.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
