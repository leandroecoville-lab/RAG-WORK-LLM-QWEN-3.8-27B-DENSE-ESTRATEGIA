# T115 — Activation Checkpointing

**Nome canônico:** Activation Checkpointing  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T115  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** gradient checkpointing; checkpointing de ativações

## T115:C01 — conceito

Técnica principalmente de treinamento que troca cálculo adicional por menor memória de ativações. Guarda alguns pontos do forward e recomputa intermediários durante o backward. Não é checkpoint de uma missão do agente nem persistência de KV para retomar uma conversa.

Como funciona:
- Escolher segmentos da rede cujas ativações não serão todas preservadas.
- Guardar entradas e informações necessárias para reconstrução.
- Reexecutar o segmento quando o cálculo de gradientes precisar dos intermediários.

Nota de nomenclatura: Classificação original em inferência foi preservada por ID; aplicação principal explicada como treinamento.

## T115:C02 — aplicacao

Quando usar:
- Fine-tuning ou treinamento é limitado por memória de ativações.
- Cálculo extra é aceitável para aumentar sequência ou batch útil.

Quando não usar:
- Esperar aceleração da inferência comum sem backward apenas ativando gradient checkpointing.

Implementação proposta:
- Medir pesos, estados do otimizador, gradientes e ativações separadamente.
- Escolher segmentos custosos em memória e toleráveis em recomputação.
- Verificar preservação de aleatoriedade, efeitos colaterais e compatibilidade com o treinamento adotado.

Aplicação LAI proposta:
Proposta LAI: considerar em experimentos de LoRA/QLoRA quando ativações forem o gargalo; não registrar como melhoria comprovada do servidor de inferência.

## T115:C03 — riscos_validacao

Armadilhas:
- Funções com efeitos colaterais podem se comportar diferentemente quando reexecutadas.
- Economizar ativações não resolve automaticamente memória de otimizador ou pesos.

Métricas sugeridas:
- Memória máxima por passo de treino e duração do passo.
- Tokens de treino úteis por segundo e diferença de gradientes frente à referência.

Testes propostos:
- Em um modelo pequeno, comparar perdas e gradientes com e sem checkpointing sob controle de aleatoriedade.
- Executar treino até completar passos representativos sem OOM e medir custo extra.

## T115:C04 — perguntas_proveniencia

Pergunta: É o mesmo que salvar state.json?
Resposta: Não. Um é técnica numérica de treino; o outro é persistência operacional do agente.

Pergunta: Checkpointing acelera o treino?
Resposta: Geralmente adiciona recomputação; pode viabilizar uma configuração maior, mas o resultado deve ser medido.

Pergunta: Checkpointing reduz diretamente a latência de geração?
Resposta: Não é esse seu objetivo; atua no armazenamento de ativações durante treinamento com retropropagação.

Pergunta: Igualdade de loss em uma etapa basta?
Resposta: Não. Gradientes podem divergir apesar de uma saída forward semelhante; compare também o caminho de atualização dos parâmetros.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T115:C05 — mecanismo_avancado

Reexecutar um segmento no backward pressupõe que ele represente a mesma função do forward original. Aleatoriedade, buffers mutáveis e efeitos colaterais podem violar essa hipótese: avançar um contador ou consumir outra máscara de dropout altera a recomputação. O mecanismo precisa administrar estados aleatórios suportados e distinguir variantes de autograd; economizar ativações não é equivalente a comprimir pesos ou cache de inferência.

Condição de contorno:
Funções com dependência de estado externo ou transferência para dispositivos não contemplados podem produzir gradientes diferentes silenciosamente.

Contrato proposto:
- Entradas: Segmento diferenciável, entradas, política de preservação aleatória e variante de checkpoint.
- Saídas: Saída forward e gradientes consistentes com o cálculo sem checkpoint.
- Estado: Entradas preservadas, estado RNG necessário e metadados do autograd.
- Invariante: A recomputação mantém a função e os efeitos numéricos exigidos pelo treinamento.

Compromissos de projeto:
- Menos ativações residentes exige mais computação no backward.
- Preservar RNG custa trabalho, mas evita diferenças causadas por amostragem repetida.

## T115:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir dropout e um contador mutável no segmento. Comparar gradientes com execução sem checkpoint; o efeito colateral deve ser removido ou explicitamente controlado antes da aprovação.

Plano de avaliação proposto:
Plano proposto: controlar lote, seed, pesos e dtype, medindo pico de memória, duração da etapa e erro de gradientes. Avaliar vários segmentos; aceitar economia somente quando a trajetória de treinamento respeita o requisito de equivalência definido.

Comparações:
- T116 (distinct_from): Recomposição de KV ocorre na inferência; activation checkpointing economiza intermediários exigidos pelo backward.

Afirmação rastreável:
A documentação PyTorch descreve preservação de RNG e limitações quando dispositivos ou aleatoriedade não estão cobertos.
Suporte: direct; fontes: B-S029
Limite: O mecanismo não torna qualquer função com efeitos colaterais segura para recomputação.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T115:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 abordou equivalência da recomputação. Esta camada introduz seleção de ativações pelo custo, interação com adapters e avaliação do verdadeiro limitante de memória no treinamento.

Memória que permanece
Checkpointing reduz ativações salvas, mas não remove pesos, estados do otimizador, gradientes ou buffers de comunicação. Faça uma decomposição do pico antes de habilitá-lo. Em um treino com poucos parâmetros ajustáveis, as ativações ainda podem dominar com contextos longos; em outro, a economia pode ser pequena.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

Política seletiva
As opções descritas pelo PyTorch permitem escolher quais operações recomputar e quais resultados preservar. Uma política proposta evita repetir operações muito caras quando uma ativação relativamente pequena basta. A decisão depende da forma e do hardware, e recursos de compilação ou orçamento de memória devem ser verificados na versão instalada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

Throughput útil do treinamento
Liberar memória pode permitir lote ou contexto maior, mas recomputação acrescenta trabalho por passo. Compare tokens úteis processados até atingir um critério de validação, não somente número de passos por segundo. Aumentar lote pode mudar a dinâmica da otimização e demandar ajuste de hiperparâmetros.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

USO AVANÇADO — LoRA em contexto longo
Cenário: O checkpoint cabe, mas ativações estouram o orçamento.
Estratégia: Meça picos por segmento, ative checkpointing onde há melhor relação entre bytes e recomputação e valide gradientes. Preserve estado aleatório necessário.
Papel do modelo pequeno: Um 8–14B pode adaptar comportamento em contexto longo sem ajustar todos os pesos.
Aceite proposto: Completar passos estáveis e atingir validação equivalente dentro do orçamento total.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

USO AVANÇADO — Comparar redução de memória
Cenário: Há opções de offload, checkpointing e quantização do modelo base.
Estratégia: Teste uma variável por vez, depois composições justificadas. Inclua tráfego de CPU, recomputação e precisão dos parâmetros treináveis.
Papel do modelo pequeno: Um 15–30B exige contabilizar estados além dos pesos antes de escolher a combinação.
Aceite proposto: Relatar pico real e tempo até qualidade-alvo, sem inferir capacidade a partir de memória nominal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S029, V4B-S028, V4B-S006.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Otimização pode ser dispensável em sequências curtas; manter caminho simples facilita depuração.
8–14B: Boa hipótese quando comprimento e lote tornam ativações relevantes, sujeita à medição.
15–30B: Combine com particionamento ou quantização somente depois de identificar o componente dominante do pico.
Requisitos de treino/runtime: É técnica de treinamento/backward. Não equivale a recomputar KV de uma conversa em inferência.
Não aplicar quando: Não aplicar a segmentos com efeitos colaterais ou aleatoriedade não preservada sem uma política correta.

## T115:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q017.

## T115:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T115 → T182 [complements]
Como combinar: Adapters reduzem parâmetros treináveis, enquanto checkpointing atua sobre ativações.
Interface: Módulos treináveis e fronteiras de recomputação.
Condição: Autograd mantém caminhos necessários aos adapters.
Aceite proposto: Comparar gradientes e convergência com referência pequena sem checkpoint.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S029, V4B-S028, V4B-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T115 → T183 [complements]
Como combinar: QLoRA e checkpointing atacam componentes diferentes da memória.
Interface: Base quantizada, ativações e configuração do otimizador.
Condição: Backend suporta a combinação específica.
Aceite proposto: Medir pico e estabilidade sem atribuir toda economia a uma técnica.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S029, V4B-S028, V4B-S006. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar dropout e buffers mutáveis durante recomputação.
- Registrar precisão, acumulação de gradientes e lote efetivo ao comparar configurações.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie o modelo ajustado numa tarefa especializada e o custo para treiná-lo. Economizar memória de treinamento não demonstra que o modelo alcançou capacidade geral de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T060, T116, T183

## Fontes primárias associadas

### B-S029 — torch.utils.checkpoint

[https://docs.pytorch.org/docs/2.15/checkpoint.html](https://docs.pytorch.org/docs/2.15/checkpoint.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointing de ativações economiza memória e recompõe tensores durante backward.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S028 — Current and New Activation Checkpointing Techniques in PyTorch

[https://pytorch.org/blog/activation-checkpointing-techniques/](https://pytorch.org/blog/activation-checkpointing-techniques/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpoint seletivo por operação e políticas de memória/recomputação para forward/backward.

Limite: Disponibilidade e estado experimental variam com versão; não demonstra aceleração de decode nem aplicação local.

### V4B-S006 — Open Source and In-House: How Uber Optimizes LLM Training

[https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/](https://www.uber.com/us/en/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Infraestrutura Michelangelo com Transformers, Ray e DeepSpeed; avaliações de LoRA/QLoRA e scorer distribuído com vLLM.

Limite: Mistura uso interno com experimentos; não tratar todas as configurações testadas como produto lançado. FlashAttention densa não reduz a complexidade aritmética quadrática.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
