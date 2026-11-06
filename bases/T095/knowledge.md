# T095 — Sliding Window Attention

**Nome canônico:** Sliding Window Attention  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T095  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** atenção de janela deslizante

## T095:C01 — conceito

Restrição da atenção a uma vizinhança de posições, geralmente uma janela recente em decoders causais. É propriedade da arquitetura ou do padrão de atenção, diferente de descartar mensagens na aplicação. Reduz as interações por camada, mas limita acesso direto a posições fora da janela.

Como funciona:
- Definir quais posições são visíveis para cada consulta.
- Aplicar máscara e kernel compatíveis com a janela.
- Reter apenas os estados que o modelo ainda pode usar, considerando camadas locais e globais.

## T095:C02 — aplicacao

Quando usar:
- Checkpoint foi treinado ou validado para atenção local.
- Sequências extensas possuem dependências predominantemente locais.

Quando não usar:
- Impor uma janela arbitrária a modelo denso e presumir equivalência sem reavaliação.

Implementação proposta:
- Inspecionar configuração por camada, tamanho da janela e sentido causal.
- Testar dependências antes e depois da fronteira da janela.
- Preservar mecanismo externo de recuperação para informação que precise voltar ao contexto.

Aplicação LAI proposta:
Proposta LAI: verificar a arquitetura do checkpoint antes de usar a janela como justificativa para um limite de memória; combinar com recuperação explícita quando necessário.

## T095:C03 — riscos_validacao

Armadilhas:
- Atenção local em uma camada não prova que todo o modelo usa memória limitada ao mesmo tamanho.
- Um resumo ou fato distante pode não ser diretamente acessível no passo atual.

Métricas sugeridas:
- KV efetivamente retido por camada e custo por comprimento.
- Acerto em tarefas que exigem dependências além da janela.

Testes propostos:
- Variar distância entre instrução e pergunta para localizar degradação de acesso.
- Comparar alocação real de cache com a configuração e verificar camadas de atenção plena.

## T095:C04 — perguntas_proveniencia

Pergunta: É igual a manter apenas as últimas mensagens?
Resposta: Não. Uma técnica opera dentro da atenção; a outra altera o texto enviado ao modelo.

Pergunta: Posso ligar isso em qualquer modelo?
Resposta: Não sem suporte e avaliação. Mudar o padrão pode alterar o comportamento aprendido.

Pergunta: O índice circular pode substituir a posição absoluta?
Resposta: Não. O slot é armazenamento; a posição lógica determina relações causais e informação posicional.

Pergunta: Janela é uma flag neutra em modelo global?
Resposta: Não. Restringir conectividade muda a função do modelo e exige validação de qualidade e compatibilidade.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T095:C05 — mecanismo_avancado

Uma janela por camada não limita necessariamente toda influência histórica ao mesmo tamanho. Informações podem propagar-se por camadas sucessivas, ampliando o campo receptivo teórico. Isso não equivale a recuperar fielmente qualquer detalhe antigo. Em cache circular, o slot físico pode ser posição módulo capacidade, mas a posição lógica continua absoluta; confundir as duas afeta máscaras e codificação posicional.

Condição de contorno:
A remoção de estados só é válida nas camadas cuja atenção realmente deixou de consultá-los; camadas globais exigem tratamento distinto.

Contrato proposto:
- Entradas: Posições lógicas, largura da janela, configuração por camada e tokens novos.
- Saídas: Atenção local correta e atualização dos slots que podem ser substituídos.
- Estado: Mapa de posições para slots, idade dos estados e políticas por camada.
- Invariante: Nenhuma chave fora da janela é reutilizada como se fosse um token recente.

Compromissos de projeto:
- Memória limitada reduz acesso direto a detalhes distantes.
- Janelas maiores preservam mais conexões e elevam tráfego e capacidade necessária.

## T095:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: gerar além de duas voltas do buffer e colocar fatos nas fronteiras. Comparar com implementação de máscara local explícita; erros de wraparound devem aparecer sem alterar o modelo de referência.

Plano de avaliação proposto:
Plano proposto: manter arquitetura e pesos fixos, variando somente a implementação do cache. Medir equivalência, memória estabilizada e latência; avaliar capacidade de dependência distante em conjunto separado, sem tratá-la como garantia arquitetural.

Comparações:
- T109 (specializes): A janela deslizante especifica como a vizinhança avança com a posição.

Afirmação rastreável:
O Mistral publicado descreve propagação de informação entre camadas e armazenamento circular para a janela.
Suporte: direct; fontes: V3B-S007
Limite: O campo receptivo teórico não demonstra desempenho uniforme em qualquer comprimento.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T095:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu campo receptivo e posição lógica do cache circular. Agora a aplicação considera a distância das dependências, arquitetura híbrida e recuperação externa, para selecionar um modelo com janela local sem prometer acesso fiel a qualquer detalhe remoto.

Mapa de dependências da tarefa
Antes de escolher a janela, identifique quais respostas dependem de evidências distantes e quais precisam apenas da vizinhança recente. Construa exemplos que movem a mesma evidência pelo documento. A qualidade deve ser medida por distância e tipo de relação, pois bom desempenho em resumos não garante recuperação de exceções antigas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

Camadas locais e globais
Em modelos híbridos, mantenha políticas KV diferentes por camada. A economia das camadas locais pode ser real enquanto as globais continuam crescendo com o contexto. Dimensione o serviço pela soma concreta dessas camadas e não pela largura nominal de uma janela publicada como característica geral do modelo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

Reconexão por artefatos externos
Quando a tarefa exigir detalhe fora do alcance efetivo, recupere o trecho original e reapresente-o no contexto permitido. Essa estratégia opera na aplicação e precisa de proveniência; não transforma atenção local em global. Meça se a recuperação trouxe a evidência correta antes de atribuir falha ao gerador.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

USO AVANÇADO — Assistente para fluxo temporal
Cenário: Eventos recentes dominam a decisão, mas algumas regras permanecem estáveis.
Estratégia: Mantenha os eventos recentes no contexto local e carregue regras relevantes sob demanda. Teste mudanças de regra e referências a eventos antigos. Use armazenamento externo para fatos que precisam sobreviver, sem confiar em influência difusa entre camadas.
Papel do modelo pequeno: Um 3–7B local pode interpretar eventos recentes com custo limitado, dentro de uma tarefa estreita.
Aceite proposto: Aceitar por acerto em dependências recentes e recuperação correta das exceções antigas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

USO AVANÇADO — Análise de arquivo extenso
Cenário: Há seções independentes e relações pontuais entre elas.
Estratégia: Selecione um checkpoint treinado com padrão compatível. Faça leitura por seções com referências para trechos distantes, verificando relações cruzadas. Se o modelo híbrido já oferecer alcance global, teste esse caminho antes de acrescentar orquestração.
Papel do modelo pequeno: Um 8–30B pode combinar processamento local e consultas dirigidas sem ingerir tudo repetidamente.
Aceite proposto: Comparar erros por distância e custo total, incluindo recuperação e múltiplas chamadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S007, V4B-S017, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, preferir tarefas com dependências locais e memória externa explícita para fatos persistentes.
8–14B: Em 8–14B, testar modelos híbridos por camada e evitar inferir qualidade pelo tamanho anunciado do contexto.
15–30B: Em 15–30B, avaliar se camadas globais tornam KV dominante apesar da janela local.
Requisitos de treino/runtime: Padrão pertence à arquitetura e ao treinamento; runtime deve implementar máscara e descarte compatíveis com cada camada.
Não aplicar quando: Não impor janela nova a um checkpoint denso como otimização supostamente equivalente.

## T095:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q005.

## T095:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T095 → T009 [complements]
Como combinar: Recuperar a evidência antiga e inseri-la como novo contexto quando necessário.
Interface: Trecho original, fonte e posição documental.
Condição: Recuperação pode localizar a dependência e respeita o orçamento.
Aceite proposto: Mover evidências para fora da janela e verificar recuperação antes da resposta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S007, V4B-S017, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T095 → T106 [complements]
Como combinar: Calcular memória pelo padrão de retenção e cabeças de cada camada.
Interface: Configuração local/global, heads KV e dtype.
Condição: A configuração do checkpoint foi inspecionada.
Aceite proposto: Comparar estimativa com alocação real em diferentes comprimentos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S007, V4B-S017, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Testar fatos antigos contraditos por mensagens recentes.
- Separar limite de cache, alcance arquitetural e competência demonstrada.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar tarefas com dependências locais e remotas contra a fronteira. Eficiência local pode ser suficiente para o domínio, mas não sustenta paridade em síntese global ou raciocínio sobre documentos arbitrários.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T096, T109, T110

## Fontes primárias associadas

### B-S015 — Longformer: The Long-Document Transformer

[https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Combinação de atenção local e posições globais selecionadas.

Limite: Resumo e metadados acessados; artigo integral não auditado e resultados não reproduzidos.

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

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

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
