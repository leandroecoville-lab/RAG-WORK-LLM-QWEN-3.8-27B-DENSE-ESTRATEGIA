# T183 — QLoRA

**Nome canônico:** QLoRA  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T183  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ajuste fino com LoRA sobre base quantizada

## T183:C01 — conceito

Método de ajuste fino que mantém a base quantizada e congelada enquanto treina adaptadores LoRA. A proposta original combina quantização de quatro bits, NF4, dupla quantização e gerenciamento de memória por otimizadores paginados. Não equivale a qualquer treino ou inferência com pesos INT4.

Como funciona:
- Carregar base em representação quantizada compatível com a implementação de treino.
- Propagar gradientes através das operações para atualizar adaptadores.
- Avaliar adaptador com o caminho real de inferência e quantização adotado.

## T183:C02 — aplicacao

Quando usar:
- Treinamento de adaptação limitado por memória da GPU.
- Há stack compatível e dataset com qualidade suficiente para justificar o treino.

Quando não usar:
- Supor que checkpoint AWQ, GPTQ ou outro formato de serving pode ser treinado pela mesma receita sem adaptação.

Implementação proposta:
- Confirmar suporte do modelo, módulos e bibliotecas antes de estimar VRAM.
- Controlar tamanho de sequência, batch e acumulação de gradiente.
- Comparar memória alocada, qualidade e estabilidade com alternativas viáveis.

Aplicação LAI proposta:
Proposta: estimar viabilidade de QLoRA no hardware real da LAI por medição; o número de parâmetros sozinho não determina se o treino cabe.

## T183:C03 — riscos_validacao

Armadilhas:
- Memória de ativações cresce com comprimento e pode dominar a economia dos pesos.
- Exportação ou troca de quantização pode alterar resultado do adaptador.

Métricas sugeridas:
- Pico de VRAM, velocidade de treinamento e qualidade reservada.
- Diferença entre avaliação durante treino e no servidor final.

Testes propostos:
- Executar pequeno treino de compatibilidade com dados conhecidos antes de ampliar.
- Recarregar checkpoint exportado e verificar regressão em formato e conteúdo.

## T183:C04 — perguntas_proveniencia

Pergunta: QLoRA significa treinar todos os pesos em quatro bits?
Resposta: Não. A base fica congelada; os adaptadores recebem as atualizações.

Pergunta: Rodar modelo INT4 prova que consigo treiná-lo?
Resposta: Não. Treino exige memória e operadores adicionais.

Pergunta: O checkpoint final necessariamente é NF4?
Resposta: Não. A estratégia de exportação e serviço pode usar outra representação, exigindo avaliação após a conversão.

Pergunta: Quatro bits no peso significam quatro bits no cálculo?
Resposta: Não. Desquantização e acumulação podem usar precisão maior; inspecione o caminho efetivo.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T183:C05 — mecanismo_avancado

A base quantizada permanece congelada, mas o gradiente atravessa a operação que a utiliza para chegar aos adaptadores. NF4 é uma representação de quatro bits com níveis próprios, não sinônimo de inteiro uniforme INT4. Double quantization comprime constantes de quantização; otimizadores paginados tratam picos de memória de treinamento. Nenhum desses componentes descreve automaticamente o cache KV ou o caminho final do servidor.

Condição de contorno:
A memória reduzida da base não elimina ativações extensas, temporários e estados dos parâmetros treináveis.

Contrato proposto:
- Entradas: Base quantizada, configuração NF4 ou alternativa declarada, adaptadores e dados de ajuste.
- Saídas: Adaptador treinado e avaliação no caminho exato de implantação.
- Estado: Escalas quantizadas, base congelada, otimizador e dtype de computação.
- Invariante: Somente os parâmetros autorizados recebem atualização; representação da base permanece identificável.

Compromissos de projeto:
- Base menor permite ajuste em menos memória e introduz aproximação numérica.
- Exportar e requantizar pode acrescentar erro além daquele observado durante treino.

## T183:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: verificar que pesos base não mudam enquanto fatores recebem gradientes; depois comparar adaptador separado, fusão e requantização. Esperar diferenças explicitamente medidas, não equivalência presumida.

Plano de avaliação proposto:
Plano proposto: comparar LoRA em base de maior precisão e QLoRA com mesmos dados e módulos. Medir memória de cada parcela, estabilidade e qualidade final; repetir a avaliação após exportação no runtime de destino antes de aprovar implantação.

Comparações:
- T093 (distinct_from): Paged optimizers gerenciam memória de treinamento; PagedAttention organiza KV de inferência.

Afirmação rastreável:
QLoRA combina base quantizada congelada, adaptadores, NF4, quantização de constantes e otimizadores paginados.
Suporte: direct; fontes: C-S037
Limite: Esses mecanismos descrevem o método original; uma implementação chamada QLoRA pode selecionar opções diferentes.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T183:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou base congelada e NF4. A nova camada separa memória de treinamento de memória de serving, compara caminhos de exportação e trata qualidade como propriedade da composição final.

Contabilidade completa
QLoRA reduz armazenamento da base durante adaptação, mas ativações, gradientes dos adapters e estados do otimizador continuam existindo. Contexto, lote e módulos-alvo alteram o pico. Meça fases de forward, backward e atualização, pois um número único de memória média pode ocultar o limite real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

Treino não é entrega
O adapter treinado sobre base quantizada pode ser servido com outra representação somente após validação. Fundir em pesos de maior precisão e requantizar muda o caminho numérico. Preserve uma referência do treino e compare todas as rotas candidatas, incluindo templates e versões de kernels.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

Intervenções separadas
NF4, double quantization, otimizador paginado e checkpointing atuam em componentes diferentes. Documente quais estão ativos. O estudo da plataforma Uber explora combinações, mas isso não prova que qualquer receita funciona em toda GPU ou que cada configuração experimental virou produto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

USO AVANÇADO — Adaptação sob memória limitada
Cenário: O checkpoint cabe quantizado, mas ajuste completo é inviável no orçamento.
Estratégia: Selecione módulos e lote, meça picos e acrescente checkpointing apenas quando ativações forem o problema. Teste estabilidade e compare com LoRA em precisão maior numa escala controlada.
Papel do modelo pequeno: Um 8–14B pode ser adaptado com menos memória de pesos, sem prometer uma placa específica.
Aceite proposto: Atingir qualidade-alvo com memória e tempo registrados no ambiente real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

USO AVANÇADO — Entrega em outro runtime
Cenário: O treinamento e o servidor usam bibliotecas distintas.
Estratégia: Planeje conversão e teste antes de investir no treino. Valide base, adapter, fusão e quantização final por etapas para localizar a origem de perdas.
Papel do modelo pequeno: Um 15–30B exige atenção ao custo de manter cópias temporárias durante a exportação.
Aceite proposto: Reproduzir respostas e métricas de tarefa no caminho de implantação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S037, V4B-S006, V4B-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Pode facilitar experimentação, mas curadoria e avaliação continuam sendo custos centrais.
8–14B: Contextos longos podem tornar ativações dominantes apesar da base em quatro bits.
15–30B: Planeje recursos de exportação e validação, além do pico do treinamento.
Requisitos de treino/runtime: Treinamento eficiente com base quantizada e adapters; NF4 não é sinônimo de INT4 uniforme ou GGUF.
Não aplicar quando: Não afirmar que economia de treino garante latência menor ou o mesmo formato na inferência.

## T183:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C006 — Uber / Michelangelo — infraestrutura interna de LLM
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: treinamento de LLM.
Uso observado: Uber descreve uma infraestrutura interna usada para preparar dados, treinar modelos, salvar checkpoints e avaliar resultados com scorer distribuído.
Mecanismo documentado: Ray coordena workers; Transformers Trainer e DeepSpeed realizam treino; vLLM participa da avaliação offline. LoRA/QLoRA aparecem nos estudos de configurações suportadas.
Correspondência com esta base: QLoRA é configuração estudada na infraestrutura; métricas são experimentais.
Transferência proposta para modelo pequeno: Proposta: separar preparação, treino e avaliação para modelos 3–30B, mantendo artefatos de dados e checkpoints reproduzíveis e avaliação independente do treino.
Limite: Produção aqui qualifica plataforma interna, não todos os modelos/otimizações experimentais. Não replicar a formulação imprecisa do blog de que FlashAttention densa elimina a complexidade aritmética quadrática.
Fontes: V4B-S006.

V4D-C006 — Microsoft / Learning Zone / Kahoot! / Phi Silica LoRA
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Equipe descreveu a preparação de um recurso educacional com Phi Silica especializado e avaliação do resultado; a capability Learning Zone consta na documentação atual.
Mecanismo documentado: Dados do professor filtrados alimentam LoRA; prompt reforça formato; guardrails precedem exibição; avaliação por agentes é confrontada com humanos.
Correspondência com esta base: Treino contra modelo quantizado não comprova todos os detalhes do método QLoRA original.
Transferência proposta para modelo pequeno: Proposta: especializar um aluno 3–30B em objetos de negócio e remover do caminho online o professor caro; medir rejeição, acerto factual, custo por resultado aceito e divergência do juiz.
Limite: Não chamar o experimento de 2025 de rollout geral: o artigo previa public preview. A ficha atual documenta o produto, sem comprovar escala nem identidade integral da configuração. Melhoria relativa de preferência não é multiplicação de inteligência ou precisão geral.
Fontes: V4D-S012, V4D-S013.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q007, V4B-Q017.

## T183:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T183 → T115 [complements]
Como combinar: Checkpointing reduz ativações enquanto QLoRA reduz custo da base congelada.
Interface: Fronteiras de recomputação e configuração de quantização.
Condição: Gradientes dos adapters continuam corretos.
Aceite proposto: Comparar picos e convergência, isolando cada técnica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S037, V4B-S006, V4B-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T183 → T126 [alternative]
Como combinar: Uma rota de entrega pode quantizar novamente com método suportado pelo servidor.
Interface: Modelo adaptado e nova calibração.
Condição: Exportação explícita e qualidade reavaliada.
Aceite proposto: Medir perda adicional da requantização e execução final.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S037, V4B-S006, V4B-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Registrar dtype de computação e precisão dos parâmetros treináveis.
- Evitar comparar lotes ou contextos diferentes como se a memória poupada viesse só de QLoRA.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
O resultado a comparar é o modelo adaptado no servidor final. QLoRA viabiliza um processo de treinamento; não demonstra por si mesma paridade de qualidade ou custo com fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T085, T124, T177, T182

## Fontes primárias associadas

### C-S037 — QLoRA: Efficient Finetuning of Quantized LLMs

[https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Treina adaptadores através de base quantizada e congelada; NF4, dupla quantização e otimizadores paginados fazem parte da proposta.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S036 — LoRA: Low-Rank Adaptation of Large Language Models

[https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Pesos base congelados recebem atualização treinável fatorada de baixo posto.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

### V4B-S028 — Current and New Activation Checkpointing Techniques in PyTorch

[https://pytorch.org/blog/activation-checkpointing-techniques/](https://pytorch.org/blog/activation-checkpointing-techniques/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoint seletivo por operação e políticas de memória/recomputação para forward/backward.

Limite: Disponibilidade e estado experimental variam com versão; não demonstra aceleração de decode nem aplicação local.

### V4D-S012 — Phi Silica task specialization using LoRA in Microsoft Learning Zone: A technical deep dive

[https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/](https://blogs.windows.com/windowsdeveloper/2025/07/31/phi-silica-task-specialization-using-lora-in-microsoft-learning-zone-a-technical-deep-dive/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo específico: dados do professor GPT-4o filtrados, adaptador LoRA, prompt menor, guardrails de formato e avaliação por agentes confrontada com avaliação humana.

Limite: O artigo informa lançamento em public preview ainda futuro naquela data. Ganhos reportados pertencem ao experimento de perguntas Kahoot!, não a capacidade geral, precisão absoluta ou equivalência com fronteira.

### V4D-S013 — Application card: AI in Microsoft 365 Education

[https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card](https://learn.microsoft.com/en-us/microsoft-365/education/guide/1-reference/microsoft-365-education-ai-application-card)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Learning Zone documentado como capacidade do produto, usando modelo de nuvem e Phi Silica local em hardware compatível, com validação e revisão de rascunhos.

Limite: Documentação de produto não prova volume de uso real nem que todo caminho atual preserve o experimento Kahoot! de 2025. Conteúdo e idiomas podem alterar qualidade; não há garantia de acerto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
