# T109 — Local / Window Attention

**Nome canônico:** Local / Window Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T095  
**Data da curadoria:** 2026-11-05

## T109:C01 — conceito

Família de padrões em que uma posição atende a uma região local. Neste inventário, a variante de janela contígua sobrepõe-se a Sliding Window Attention. Uma janela de encoder pode ser bidirecional, enquanto um decoder causal atende apenas a posições permitidas no passado.

Como funciona:
- Escolher vizinhança local e orientação causal ou bidirecional.
- Aplicar conectividade correspondente em cada camada.
- Combinar várias camadas ou conexões adicionais quando a tarefa exigir maior alcance.

Nota de nomenclatura: Sobreposição de nomenclatura preservada; a equivalência vale para a variante de janela local contígua.

## T109:C02 — aplicacao

Quando usar:
- Dados possuem estrutura local forte e modelo foi preparado para esse padrão.
- Análise de documentos ou sequências em arquiteturas com atenção local explícita.

Quando não usar:
- Chamar de local qualquer sistema que apenas recupere um subconjunto de documentos por RAG.

Implementação proposta:
- Anotar a definição exata de janela, incluindo se o tamanho conta passado, futuro e posição atual.
- Testar fronteiras e padding com sequências pequenas inspecionáveis.
- Documentar quais camadas mantêm conexões de alcance maior.

Aplicação LAI proposta:
Proposta LAI: manter esta entrada como alias explicativo da família local e consultar T095 para o caso comum de janela deslizante no decode.

## T109:C03 — riscos_validacao

Armadilhas:
- Janelas com mesmo número podem ter semânticas diferentes entre bibliotecas.
- Não existe garantia de que empilhar camadas recupere perfeitamente toda dependência distante.

Métricas sugeridas:
- Alcance efetivo necessário para as tarefas e densidade de conexões.
- Memória por camada e acerto conforme a distância de evidências.

Testes propostos:
- Construir matriz de máscara esperada para pequena sequência e comparar todos os pares permitidos.
- Mover a mesma evidência para fora da vizinhança e medir a resposta do sistema.

## T109:C04 — perguntas_proveniencia

Pergunta: Local é necessariamente causal?
Resposta: Não. Encoders podem ver vizinhos dos dois lados; decoders causais precisam impedir futuro.

Pergunta: É técnica independente de Sliding Window Attention?
Resposta: A janela contígua frequentemente é a mesma ideia; outros padrões locais precisam ser definidos explicitamente.

Pergunta: Largura W define a máscara completamente?
Resposta: Não. É preciso saber se inclui o centro, quantos tokens ficam em cada direção e quais fronteiras existem.

Pergunta: Pode reutilizar uma máscara em todo o lote?
Resposta: Somente quando posições, comprimentos e separação documental produzem a mesma conectividade ou broadcasting corretamente definido.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T109:C05 — mecanismo_avancado

Vizinhança local precisa declarar orientação, inclusão da própria posição e tratamento de limites. Uma janela bidirecional em encoder e uma janela causal em decoder podem ter a mesma largura nominal e conjuntos visíveis diferentes. Em sequências empacotadas, a proximidade física de tokens não permite cruzar fronteiras documentais. O padrão local também pode ser combinado com dilatação, alterando quais distâncias são acessíveis por camada.

Condição de contorno:
Usar máscara local em pesos treinados com outro padrão altera a função e pode reduzir qualidade mesmo quando o kernel é correto.

Contrato proposto:
- Entradas: Comprimentos, fronteiras de documentos, orientação da janela e alcance por camada.
- Saídas: Máscara ou metadados que representam exatamente a vizinhança permitida.
- Estado: Posições lógicas e identificação documental independente do offset físico.
- Invariante: Nenhuma conexão atravessa limites sem autorização explícita da arquitetura.

Compromissos de projeto:
- Vizinhanças curtas reduzem trabalho e aumentam a distância de propagação entre fatos.
- Empacotar exemplos economiza padding, mas exige isolamento rigoroso das máscaras.

## T109:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: colocar dois documentos adjacentes e modificar somente o segundo. Em configuração causal ou isolada, esperar que a representação das posições não autorizadas do primeiro permaneça inalterada.

Plano de avaliação proposto:
Plano proposto: comparar implementação local com referência densa mascarada, incluindo bordas e comprimentos curtos. Depois medir tarefas com dependências em distâncias diferentes; separar correção do kernel de adequação do padrão à aplicação.

Comparações:
- T095 (complements): As fichas se sobrepõem na janela contígua; orientação e fronteiras precisam ser declaradas para comparar implementações.

Afirmação rastreável:
Longformer combina conexões locais com mecanismos globais para tarefas de documentos extensos.
Suporte: direct; fontes: B-S015
Limite: A fonte descreve uma arquitetura; suas propriedades não tornam qualquer janela local adequada a decoders.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T109:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 definiu orientação e fronteiras da janela. A nova análise distingue dependência alcançável em várias camadas, retenção efetiva de estados e posicionamento da informação relevante no fluxo.

Alcance efetivo
Camadas locais sucessivas podem transmitir informação além da janela de uma camada, mas isso não equivale a acesso direto a cada token remoto. O efeito depende de profundidade, resíduos e treinamento. Teste relações que exigem copiar um detalhe antigo, combinar fatos e revisar uma conclusão: cada tarefa expõe uma limitação diferente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

Janela e estado físico
Uma máscara local economiza trabalho apenas se o kernel explora o padrão e o runtime limita estados quando a arquitetura permite. Guardar todo KV enquanto mascara posições antigas pode preservar facilidade de implementação, mas não entrega a mesma economia de memória. Em modelos híbridos, algumas camadas continuam exigindo histórico maior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

Organização do contexto
Mover fatos recentes para perto da pergunta pode ajudar uma arquitetura local, mas resumo não preserva todos os detalhes. Uma estratégia proposta mantém uma lista pequena de fatos verificáveis e recupera a origem quando necessário. A política de atualização deve detectar correções, não simplesmente acrescentar versões contraditórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

USO AVANÇADO — Assistente de eventos recentes
Cenário: O sistema acompanha uma operação com histórico extenso.
Estratégia: Use janela para o fluxo recente e um registro externo para decisões duráveis. Ao consultar um fato antigo, recupere a evidência e reinsira-a no contexto disponível.
Papel do modelo pequeno: Um 3–7B atua sobre eventos e consultas delimitadas, com memória externa auditável.
Aceite proposto: Testar eventos antigos relevantes e medir omissões após várias rotações da janela.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

USO AVANÇADO — Extração de documentos segmentados
Cenário: A tarefa encontra informações locais em documentos longos.
Estratégia: Segmente respeitando estrutura, sobreponha fronteiras e consolide resultados com identificadores de origem. Use uma etapa adicional para relações entre segmentos.
Papel do modelo pequeno: Um 8–14B resolve trechos; uma agregação explícita trata dependências distantes.
Aceite proposto: Cobertura deve incluir fatos nas bordas e relações que cruzam seções.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S015, V3B-S007, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Contextos locais e respostas curtas reduzem exigências, mas exigem mecanismo externo para fatos duráveis.
8–14B: Janelas por camada e tokens recuperados precisam entrar na avaliação de leitura longa.
15–30B: Um 15–30B não recupera automaticamente informação que sua máscara torna inacessível.
Requisitos de treino/runtime: Adotar janela diferente exige suporte arquitetural e validação; implementação do kernel não substitui treinamento.
Não aplicar quando: Não truncar contexto de um modelo denso e chamar o resultado de comportamento equivalente.

## T109:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T109:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T109 → T110 [complements]
Como combinar: Posições globais podem criar caminhos para informação que a janela não alcança diretamente.
Interface: Máscara global e identificadores de documentos.
Condição: Arquitetura treinada com a combinação.
Aceite proposto: Avaliar dependências remotas sem permitir leitura de tokens futuros.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V3B-S007, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T109 → T009 [complements]
Como combinar: Recuperação externa reinsere fatos relevantes numa janela limitada.
Interface: Trechos, proveniência e versão.
Condição: Recuperador encontra a evidência necessária.
Aceite proposto: Separar falhas de recuperação de falhas de interpretação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S015, V3B-S007, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Verificar comportamento no primeiro e último token de cada documento empacotado.
- Não tratar resumo como cópia semanticamente perfeita do histórico removido.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avalie uma tarefa em que a evidência necessária é local ou recuperável. Uma vantagem de custo nesse cenário não demonstra equivalência em raciocínio sobre todo o histórico original.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T095, T096, T110

## Fontes primárias associadas

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V3B-S007 — Mistral 7B — full text

[https://arxiv.org/html/2310.06825v1](https://arxiv.org/html/2310.06825v1)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campo receptivo em camadas, cache circular e chunking com janela.

Limite: Refere-se à arquitetura publicada; não prova qualidade para contexto arbitrário nem compatibilidade com checkpoint do usuário.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
