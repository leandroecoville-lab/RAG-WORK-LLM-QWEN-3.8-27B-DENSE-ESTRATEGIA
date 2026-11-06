# T130 — N-Gram Speculative Decoding

**Nome canônico:** N-Gram Speculative Decoding  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T130  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** ngram speculation; especulação por n-gramas

## T130:C01 — conceito

Gera candidatos de continuação buscando sequências de tokens repetidas no prompt ou em um pool de histórico permitido. Dispensa um modelo neural auxiliar para a proposta, mas o modelo alvo ainda verifica os candidatos. Favorece padrões repetitivos, como transformações de texto e código.

Como funciona:
- Indexar n-gramas e continuações observadas em tokens.
- Localizar correspondência para o final da sequência atual.
- Propor alguns tokens seguintes e submeter a verificação do alvo.

## T130:C02 — aplicacao

Quando usar:
- Saída reutiliza trechos do contexto ou padrões recorrentes.
- Memória ou complexidade não justificam carregar um draft neural.

Quando não usar:
- Conteúdo pouco repetitivo gera candidatos ruins e overhead maior que a economia.

Implementação proposta:
- Começar com pool privado por requisição e limites de tamanho.
- Ajustar tamanho da chave e quantidade de candidatos com avaliação de custo líquido.
- Preservar a identificação do tokenizer e da política de amostragem no experimento.

Aplicação LAI proposta:
Proposta LAI: candidato inicial para tarefas repetitivas do modelo local por não exigir treino de draft; validar separadamente conversa aberta e edição de código.

## T130:C03 — riscos_validacao

Armadilhas:
- Comparar texto decodificado em vez de tokens pode produzir correspondências inválidas.
- Pools compartilhados guardam conteúdo e precisam respeitar escopo de acesso e retenção.

Métricas sugeridas:
- Taxa de correspondência, comprimento aceito e custo de lookup.
- Latência por batch e memória de índices no host.

Testes propostos:
- Comparar textos repetitivos e aleatórios, exigindo ganho real no primeiro e degradação limitada no segundo.
- Inserir padrões ambíguos e confirmar que o alvo rejeita continuações inadequadas.

## T130:C04 — perguntas_proveniencia

Pergunta: A resposta armazenada é devolvida diretamente?
Resposta: Não. Ela pode fornecer candidatos; o alvo precisa verificá-los.

Pergunta: N-gram é busca semântica?
Resposta: Não. Trabalha principalmente com padrões exatos de tokens, não equivalência de significado.

Pergunta: Correspondência exata dispensa o alvo?
Resposta: Não. O padrão pode ter surgido em outro contexto e a próxima distribuição pode ser diferente.

Pergunta: Pode funcionar sem um segundo modelo?
Resposta: Sim. O proponente pode ser uma estrutura de tokens na CPU; ainda existem custo de busca e verificação.

Escopo das fontes:
As fontes fundamentam a definição. Implementação, critérios de teste e aplicação LAI são propostas editoriais, sem validação no servidor.

## T130:C05 — mecanismo_avancado

O tamanho da chave controla especificidade do padrão: correspondências curtas ocorrem mais, mas podem propor continuações ambíguas; longas têm menos cobertura. O comprimento da continuação controla trabalho adicional de verificação. Ambos precisam ser avaliados conjuntamente com concorrência. A consulta deve operar em token IDs compatíveis com o alvo, pois coincidência de caracteres após decodificação não garante a mesma segmentação.

Condição de contorno:
Em texto pouco repetitivo, manutenção do dicionário e verificação de candidatos podem custar mais que os passos economizados.

Contrato proposto:
- Entradas: Histórico permitido de tokens, comprimentos de chave e proposta, política para múltiplas ocorrências.
- Saídas: Continuação candidata e sua origem no índice.
- Estado: Pares de padrões, frequência ou ordem das ocorrências e limites de memória.
- Invariante: Correspondência serve apenas para propor; confirmação continua dependente do modelo alvo.

Compromissos de projeto:
- Chaves longas aumentam precisão de padrão e reduzem frequência de hits.
- Dicionários grandes ampliam cobertura e podem piorar localidade na CPU.

## T130:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: repetir o mesmo n-grama com continuações conflitantes e inserir mudança de tokenização. Esperar seleção determinável pela política e rejeição de índices incompatíveis.

Plano de avaliação proposto:
Plano proposto: comparar geração sem propostas e diferentes pares de comprimentos na mesma carga. Medir lookup, atualização, verificação, tokens confirmados e latência por concorrência; escolher pelo tempo total e não apenas pelo comprimento aceito.

Comparações:
- T131 (alternative): Estruturas de sufixos suportam padrões variáveis e outra organização das continuações históricas.

Afirmação rastreável:
A implementação documentada de N-Gram constrói padrões chave-continuação e verifica no alvo as propostas encontradas.
Suporte: direct; fontes: B-S041
Limite: O custo e as configurações eficientes descritos no artigo dependem da carga; não são defaults universais.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T130:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou comprimentos de chave e continuação. Esta camada usa o caso de produção do Hiring Assistant para delimitar padrões favoráveis e propõe controles de proveniência e de custo do índice.

Repetição que interessa
N-gramas são particularmente plausíveis quando a saída reaproveita sequências do prompt ou do histórico permitido. O relato do LinkedIn descreve esse perfil em saídas estruturadas do Hiring Assistant. Isso não autoriza extrapolar para raciocínio aberto, tradução livre ou textos com pouca repetição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

Origem e escopo
Defina de onde propostas podem vir: prompt atual, tokens confirmados ou memória compartilhada autorizada. Índices entre usuários exigem isolamento e regras de retenção. Mesmo com verificação pelo alvo, consultar um índice privado pode expor padrões ou ampliar canais de informação; a arquitetura deve limitar acesso desde a busca.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

Custo de busca
Um proponente sem rede neural ainda consome CPU, memória e sincronização. Meça tempo por consulta e atualização, especialmente com contextos grandes e concorrência. Uma chave curta pode produzir muitas ocorrências; a política para escolher continuação precisa ser determinística ou explicitamente amostrada e reprodutível.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

USO AVANÇADO — Extração estruturada com cópia
Cenário: A resposta reutiliza nomes e trechos da entrada.
Estratégia: Teste n-gramas no prompt atual, mantendo o verificador do alvo e a gramática quando suportada. Compare diferentes comprimentos sem ajustar ao conjunto final de avaliação.
Papel do modelo pequeno: Um 8–14B pode executar extração especializada com pouco custo adicional de proponente.
Aceite proposto: Medir aceitação, CPU, latência e validade semântica da extração.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

USO AVANÇADO — Reescrita com baixa alteração
Cenário: O usuário pede correções pontuais em um texto.
Estratégia: Use a entrada como fonte de candidatos e teste casos em que a continuação mais frequente precisa ser alterada. A verificação deve rejeitar a cópia incorreta.
Papel do modelo pequeno: Um 3–7B pode ser adequado a tarefas locais estreitas, sujeito à qualidade-base.
Aceite proposto: Confirmar alterações obrigatórias e ausência de cópia indevida apesar de alta repetição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S041, V4B-S001, V4B-S029.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Custo de busca pode ser relevante frente a um alvo barato; manter índice restrito ao pedido simplifica.
8–14B: Boa hipótese para formatos repetitivos e respostas longas, sem ganho presumido.
15–30B: Em alvos maiores, verificação pode amortizar mais trabalho, mas concorrência continua determinante.
Requisitos de treino/runtime: Runtime de especulação com proponente de tokens; não requer treinar um draft neural.
Não aplicar quando: Não descrever preservação da distribuição como garantia de texto idêntico em todas as sementes e implementações.

## T130:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 1. Lacuna: 9. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 1. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C001 — LinkedIn (Microsoft) / Hiring Assistant
Evidência: produção documentada; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: O operador descreve uso em produção do Hiring Assistant para analisar correspondência entre vagas e candidatos, com saídas estruturadas e repetição de trechos de entrada.
Mecanismo documentado: N-gramas propõem tokens e o alvo verifica; o serving descrito também reutiliza prefixos e recompõe lotes a cada iteração.
Correspondência com esta base: O proponente escolhido usa correspondências por n-gramas, sem modelo auxiliar.
Transferência proposta para modelo pequeno: Proposta: testar extração especializada com alvo 3–30B, n-gramas e prefixos estáveis, preservando aceitação correta e medindo custo por relatório válido.
Limite: Não comprova o porte exato do modelo do usuário nem ganhos em outro hardware. Distribuição preservada não implica a mesma amostra textual. É um único caso, embora apoie vários mecanismos.
Fontes: V4B-S001, V4B-S010.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q001, V4B-Q018.

## T130:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T130 → T079 [feeds]
Como combinar: O LinkedIn usa propostas n-gram verificadas pelo alvo no Hiring Assistant.
Interface: Sequência candidata e estado do alvo.
Condição: Regra correta de aceitação e configuração compatível.
Aceite proposto: Comparar execução especulativa com o alvo sem proponente.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S001. Casos: V4B-C001.

2. T130 → T196 [complements]
Como combinar: Restrições estruturais precisam ser consideradas no caminho de verificação.
Interface: Estado de gramática e prefixo confirmado.
Condição: Implementação suporta a combinação sem aceitar tokens proibidos.
Aceite proposto: Testar fronteiras de strings, delimitadores e rejeição de candidatos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S041, V4B-S001, V4B-S029. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar índice compartilhado sem domínio de acesso explícito.
- Relatar taxa de aceitação com denominador correto e custo do proponente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Especulação n-gram pode acelerar uma tarefa em que o modelo já é competente. A repetição da entrada facilita proposta, mas não garante que o conteúdo copiado seja a resposta certa.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T079, T131, T132

## Fontes primárias associadas

### B-S041 — N-Gram Speculative Decoding in TensorRT LLM

[https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog07_NGram_performance_Analysis_And_Auto_Enablement.html](https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog07_NGram_performance_Analysis_And_Auto_Enablement.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Propostas a partir de n-gramas, pools privados ou compartilhados e verificação pelo modelo alvo.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V4B-S001 — Accelerating LLM inference with speculative decoding: Lessons from LinkedIn's Hiring Assistant

[https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant](https://www.linkedin.com/blog/engineering/ai/accelerating-llm-inference-with-speculative-decoding-lessons-from-linkedins-hiring-assistant)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Uso de especulação por n-gramas em vLLM no Hiring Assistant; workload estruturado com sobreposição lexical.

Limite: Relato do operador para carga própria; igualdade de distribuição não deve ser confundida com texto idêntico sob amostragem. Ganhos não transferidos.

### V4B-S029 — Per-Request Acceptance Metrics — vLLM

[https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/](https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Métricas de aceitação por requisição, histograma de comprimentos e distinção do token bônus; interface experimental.

Limite: Medições de aceitação não garantem ganho; coleta, streaming e múltiplas sequências têm condições específicas.

### V4B-S010 — How we leveraged vLLM to power our GenAI applications at LinkedIn

[https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications](https://www.linkedin.com/blog/engineering/ai/how-we-leveraged-vllm-to-power-our-genai-applications)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Adoção interna de vLLM para workloads online e offline; evolução do scheduler e interface de serving.

Limite: Versões históricas do relato não são recomendação atual; casos citados não equivalem a implantações independentes de cada recurso.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
