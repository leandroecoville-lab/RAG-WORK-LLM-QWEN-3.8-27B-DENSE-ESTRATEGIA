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
