# T108 — Multi-Head Attention — MHA

**Nome canônico:** Multi-Head Attention — MHA  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T108  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** multi-head attention; atenção multicabeças

## T108:C01 — conceito

Mecanismo de atenção com múltiplas projeções de consultas, chaves e valores. Cada cabeça produz uma combinação de valores segundo compatibilidade entre consultas e chaves; os resultados são combinados. Na MHA convencional, cada cabeça tem seu próprio KV, diferentemente do compartilhamento de MQA/GQA.

Como funciona:
- Projetar a entrada em Q, K e V por cabeça.
- Calcular softmax(QKᵀ/√d) com a máscara adequada e aplicar aos valores.
- Combinar as saídas das cabeças por concatenação e projeção.

## T108:C02 — aplicacao

Quando usar:
- Entender e dimensionar checkpoints que usam MHA.
- Construir referência para comparar implementações alternativas de atenção.

Quando não usar:
- Tratar cada cabeça como especialista interpretável ou agente independente sem evidência.

Implementação proposta:
- Identificar número de cabeças, dimensão, máscara e esquema posicional.
- Conferir tensor shapes e evitar trocar eixos de batch, sequência e cabeça.
- Usar referência simples para validar um kernel otimizado ou nova forma de cache.

Aplicação LAI proposta:
Proposta LAI: usar MHA como fundamento para entender custos e como contraste com o esquema real do modelo local, sem tentar redesenhar o checkpoint em produção.

## T108:C03 — riscos_validacao

Armadilhas:
- Atenção causal incorreta permite acesso a tokens futuros.
- A quantidade de cabeças isolada não mede inteligência nem qualidade do modelo.

Métricas sugeridas:
- Memória KV por token e custo da atenção por comprimento.
- Erro numérico da implementação e desempenho de tarefa do modelo completo.

Testes propostos:
- Modificar apenas tokens futuros e exigir que posições anteriores permaneçam invariantes no modo causal.
- Comparar execução em lote e individual removendo diferenças de padding.

## T108:C04 — perguntas_proveniencia

Pergunta: Cada cabeça é um agente?
Resposta: Não. É um conjunto de projeções e operações internas treinadas conjuntamente.

Pergunta: Trocar MHA por GQA preserva o modelo automaticamente?
Resposta: Não. A mudança requer uma conversão válida e avaliação, normalmente com treinamento adicional.

Pergunta: Uma cabeça corresponde sempre a uma função humana?
Resposta: Não. Especializações podem surgir, mas precisam de evidência; a numeração sozinha não carrega significado.

Pergunta: A escala garante boa calibração?
Resposta: Não. Ela regula magnitude dos scores de atenção, não a probabilidade de uma resposta factual estar correta.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T108:C05 — mecanismo_avancado

A escala 1/√d controla a magnitude dos produtos entre consultas e chaves sob hipóteses usuais sobre seus componentes. Sem escala adequada, o softmax pode concentrar massa e produzir gradientes pouco informativos. A interpretação de uma cabeça também depende da projeção final: permutar cabeças juntamente com a permutação inversa nos blocos da projeção pode preservar a função, mostrando que números de cabeça não têm significado sem os pesos associados.

Condição de contorno:
Mapa de atenção visual não constitui prova causal de que determinado token sustentou a conclusão textual do modelo.

Contrato proposto:
- Entradas: Projeções QKV, dimensão por cabeça, máscara, escala e projeção de saída.
- Saídas: Representações combinadas preservando ordem e layout das cabeças.
- Estado: Pesos de projeção e convenção de concatenação dos resultados.
- Invariante: Carregamento e execução usam a mesma correspondência entre cabeças e projeção final.

Compromissos de projeto:
- Mais cabeças repartem capacidade em subespaços e afetam formas dos kernels.
- MHA convencional mantém KV separado, aumentando memória frente a compartilhamento arquitetural.

## T108:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: permutar cabeças com compensação na projeção final e depois sem compensação. Esperar equivalência no primeiro caso e divergência no segundo, isolando um erro de layout.

Plano de avaliação proposto:
Plano proposto: validar a operação contra implementação explícita em formas pequenas e diferentes máscaras. Medir erro de saída, estabilidade e custo, mantendo pesos idênticos; comparações de qualidade entre arquiteturas precisam controlar treinamento e capacidade.

Comparações:
- T099 (distinct_from): MQA compartilha K e V; isso muda a parametrização, não apenas a concatenação final.

Afirmação rastreável:
O Transformer original combina múltiplas projeções de atenção e uma projeção final de suas saídas.
Suporte: direct; fontes: B-S024
Limite: A interpretação sobre permutações é uma derivação algébrica do layout, não um resultado experimental relatado.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T108:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou escala e correspondência das cabeças. A nova camada considera interoperabilidade de pesos, contribuições funcionais e alternativas de adaptação sem confundir inspeção visual com causalidade.

Convenções de carregamento
QKV pode estar fundido, intercalado por cabeça ou separado; a projeção final também possui ordem específica. Ao converter pesos, documente reshape, transposição, posição e dtype. Teste entradas curtas e longas, pois um erro de posição pode passar em exemplos mínimos mesmo quando as dimensões são válidas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

Cabeças como componentes
Mapas de atenção revelam pesos de mistura, não uma explicação completa da decisão. Para investigar uma cabeça, use ablação controlada e observe efeito na tarefa e em exemplos próximos. A projeção de saída, resíduos e demais camadas podem compensar alterações; uma visualização chamativa não prova especialização universal.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

Ajustar sem redesenhar
Quando o objetivo é domínio novo, adapters nas projeções podem ser uma intervenção mais controlada que remover cabeças. Identifique se o problema exige novas associações, formato ou evidência externa antes de alterar arquitetura. Reduzir cabeças modifica capacidade e demanda treinamento e avaliação, não apenas um parâmetro de serving.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

USO AVANÇADO — Migração de formato
Cenário: Pesos precisam passar entre ferramentas de treinamento e inferência.
Estratégia: Crie uma comparação progressiva de projeções e saídas por camada. Investigue o primeiro ponto divergente em vez de confiar somente numa resposta textual final aparentemente correta.
Papel do modelo pequeno: Um 3–7B permite validar a cadeia de conversão com custo menor antes de modelos maiores.
Aceite proposto: Logits devem obedecer tolerâncias declaradas e a máscara causal deve permanecer correta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

USO AVANÇADO — Diagnóstico de informação ignorada
Cenário: Um modelo recebe fatos no contexto mas não os usa.
Estratégia: Varie distância, distratores e posição da evidência; depois teste ablações ou adaptações pequenas. Use recuperação e organização do contexto como alternativas mensuráveis.
Papel do modelo pequeno: Um 8–14B pode melhorar num domínio restrito sem acrescentar capacidade arbitrária de memória.
Aceite proposto: A melhora deve sobreviver à troca de entidades e à inserção de informações contraditórias.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S024, V4B-S017.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Prefira preservar arquitetura conhecida e investir em contexto ou adaptação antes de redesenhar cabeças.
8–14B: Use adapters para hipóteses específicas; não atribua toda melhora à atenção se o treino modifica outros módulos.
15–30B: Conversões maiores ampliam custo de validar tensores e checkpoints; mantenha testes em amostras representativas.
Requisitos de treino/runtime: MHA é arquitetura treinada; kernels podem mudar sem mudar seu grafo matemático, dentro das tolerâncias numéricas.
Não aplicar quando: Não usar pesos de atenção como prova direta da fonte factual de uma resposta.

## T108:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T108:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T108 → T098 [complements]
Como combinar: Uma interface de atenção eficiente executa a operação com máscaras e layouts explícitos.
Interface: QKV, escala, máscara e convenção de eixos.
Condição: Backend suporta forma e dtype usados.
Aceite proposto: Comparar forward e, se houver treino, gradientes.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S024, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T108 → T182 [complements]
Como combinar: Adapters nas projeções permitem testar uma adaptação limitada.
Interface: Lista de módulos, posto e checkpoint base.
Condição: Pesos e nomes dos módulos correspondem ao modelo real.
Aceite proposto: Ablacionar módulos-alvo e validar retenção de capacidades.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S024, V4B-S017. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não aceitar conversão só porque tensores têm dimensões compatíveis.
- Tratar explicações produzidas por visualização como hipóteses a serem testadas.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Atenção com várias cabeças não é uma medida de inteligência. Compare a solução especializada com fronteira em localização e uso de evidência, incluindo casos em que a informação é insuficiente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T099, T100, T106, T090

## Fontes primárias associadas

### B-S024 — Attention Is All You Need

[https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Transformer e mecanismo multi-head como referência arquitetural.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### V4B-S017 — FlexAttention Part II: FlexAttention for Inference

[https://pytorch.org/blog/flexattention-for-inference/](https://pytorch.org/blog/flexattention-for-inference/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Backend de decode, suporte a GQA e PagedAttention e diferenças entre formas de prefill/decode.

Limite: Implementação e experimentos não constituem prova de adoção em produto; atenção customizada depende de máscara correta.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
