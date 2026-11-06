# T197 — JSON Schema Validation

**Nome canônico:** JSON Schema Validation  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T197  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** validação de JSON Schema

## T197:C01 — conceito

Validação de um documento JSON contra um schema com tipos, campos obrigatórios, enums e outras restrições. É uma verificação determinística de contrato estrutural dentro do dialeto e configuração usados. Não confirma existência de um cliente, verdade de uma afirmação ou autorização para uma ação.

Como funciona:
- Escolher dialeto e validar o próprio schema.
- Analisar JSON e aplicar as restrições ao documento.
- Devolver erros com localização antes de qualquer consumo ou efeito dependente.

## T197:C02 — aplicacao

Quando usar:
- Fronteiras entre agentes, ferramentas e serviços.
- Ingestão de dados com contrato estável e erros que precisam ser explicáveis.

Quando não usar:
- Assumir que toda regra de negócio pode ser expressa apenas no schema.

Implementação proposta:
- Declarar campos obrigatórios e política de campos extras.
- Diferenciar campo ausente, null e string vazia.
- Conferir comportamento de format e referências no validador escolhido.

Aplicação LAI proposta:
Proposta: todos os eventos e resultados de ferramentas da Helena passarem por schema versionado, seguido de verificação das regras de negócio.

## T197:C03 — riscos_validacao

Armadilhas:
- Defaults descritos no schema nem sempre são inseridos pelo validador.
- Configurações de format podem somente anotar, sem rejeitar valor inválido.

Métricas sugeridas:
- Rejeições corretas e aceitações incorretas do contrato.
- Erros por versão e localização de falhas nos documentos.

Testes propostos:
- Testar fronteiras numéricas, tipos errados e propriedades desconhecidas.
- Usar payload estruturalmente válido com referência inexistente e exigir validação de domínio adicional.

## T197:C04 — perguntas_proveniencia

Pergunta: Schema valida a veracidade do valor?
Resposta: Não. Valida restrições especificadas; fatos precisam de outra verificação.

Pergunta: Required impede null?
Resposta: Não sozinho. É preciso também definir um tipo que exclua null.

Pergunta: format email confirma que a caixa existe?
Resposta: Não. Mesmo uma checagem sintática de formato não confirma existência, titularidade ou capacidade de entrega.

Pergunta: Schema válido prova argumento autorizado?
Resposta: Não. Autorização depende do solicitante, recurso e operação, além da forma dos dados enviados.

Escopo das fontes:
As fontes sustentam o conceito ou mecanismo indicado; implementação, métricas, testes e aplicação LAI são propostas editoriais, sem execução ou benchmark no ambiente do usuário.

## T197:C05 — mecanismo_avancado

Declarar uma propriedade não a torna obrigatória: presença é controlada por required. Em composição, additionalProperties observa o subschema em que foi declarado e pode rejeitar extensões pretendidas; unevaluatedProperties permite considerar propriedades avaliadas por outras partes, conforme o dialeto. O keyword format também pode funcionar como anotação, sem checagem de validade, se a configuração não exigir o vocabulário de asserção correspondente.

Condição de contorno:
Dois validadores com dialetos ou suporte de format diferentes podem discordar sem que os mesmos bytes do JSON tenham mudado.

Contrato proposto:
- Entradas: JSON parseado, schema identificado, dialeto e configuração explícita do validador.
- Saídas: Resultado com caminhos dos erros e indicação de recursos não suportados.
- Estado: Versões do schema, resoluções de referências e política de formatos.
- Invariante: Uma restrição obrigatória desconhecida nunca é tratada como se tivesse sido verificada.

Compromissos de projeto:
- Schemas fechados detectam campos inesperados e dificultam evolução.
- Composição facilita reúso e exige compreender o escopo de cada restrição.

## T197:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: remover campo declarado mas não required, acrescentar propriedade por allOf e usar format inválido. Esperar resultados coerentes com o dialeto e a configuração documentados, sem supor validação inexistente.

Plano de avaliação proposto:
Plano proposto: criar casos válidos e inválidos por restrição, comparar implementações quando necessário e verificar mensagens de erro. Medir cobertura do contrato e compatibilidade entre produtores/consumidores; adicionar checagens externas para fatos e autorização.

Comparações:
- T196 (complements): Uma gramática de geração pode impor parte do schema, mas o objeto final ainda precisa ser validado.

Afirmação rastreável:
A documentação JSON Schema diferencia propriedades declaradas, obrigatórias, adicionais e propriedades avaliadas através de composição.
Suporte: direct; fontes: V3B-S024
Limite: A evidência cobre estrutura; existência de registros e significado dos valores dependem de validações de domínio.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T197:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou required e dialetos. A nova camada trata schemas como versões de interface, limites de resolução e a separação entre validação de forma e invariantes que dependem de estado externo.

Evolução do contrato
Adicionar um campo opcional pode ser compatível para alguns consumidores e quebrar outros que rejeitam propriedades extras. Versione schema e política de compatibilidade, incluindo defaults aplicados fora da validação. Teste produtor antigo com consumidor novo e a direção inversa antes de anunciar uma mudança transparente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

Referências e recursos
Resolução de referências precisa ser previsível e limitada. Prefira schemas conhecidos e cacheados, com limites de profundidade e tamanho quando entradas não são confiáveis. Um validador pode ser correto no dialeto e ainda consumir recursos excessivos em estruturas complexas; faça essa avaliação separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

Semântica além da forma
Schema pode garantir que valor é número e campo existe, mas não que saldo está atualizado, entidade pertence ao usuário ou citação sustenta a frase. Encaminhe essas condições a regras de negócio e fontes. Uma validação formal de política, como no Bedrock, é outra camada com alcance próprio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

USO AVANÇADO — API consumida por modelo pequeno
Cenário: O serviço exige argumentos tipados.
Estratégia: Use schema restrito ao que o gerador e o validador suportam, valide o objeto completo e gere erros por caminho. Reparo deve preservar campos já corretos e revalidar o conjunto.
Papel do modelo pequeno: Um 3–7B pode preencher contratos simples com ajuda de geração restrita.
Aceite proposto: Medir campos corretos e falhas de negócio, além da taxa de JSON parseável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

USO AVANÇADO — Migração de interface
Cenário: Uma ferramenta passa a exigir novos dados.
Estratégia: Crie adaptador explícito ou nova versão, mantendo testes cruzados. Não preencha automaticamente um valor de negócio desconhecido só para satisfazer required.
Papel do modelo pequeno: Um 8–14B pode explicar ou coletar o dado ausente, sem inventar defaults.
Aceite proposto: Detectar incompatibilidades e impedir execução com dados fabricados.
Natureza: proposta de engenharia; não medida neste pacote; fontes: C-S049, V3B-S024, V4B-S015, V4B-S027.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Schemas pequenos e campos claros reduzem carga de seleção e reparo.
8–14B: Composição complexa exige cobertura de teste e diagnóstico de erros compreensível.
15–30B: Mesmo 15–30B deve ter validação determinística na fronteira da interface.
Requisitos de treino/runtime: Biblioteca de validação, dialeto e recursos suportados explicitamente; não exige treinamento.
Não aplicar quando: Não assumir que annotation format foi validada nem que campos presentes são factualmente corretos.

## T197:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: JSON Schema pode alimentar a gramática, mas isso não substitui validação posterior independente.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013, V4B-Q019.

## T197:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T197 → T196 [complements]
Como combinar: Decodificação restrita pode reduzir saídas estruturalmente inválidas antes da checagem final.
Interface: Schema suportado e objeto completo.
Condição: Conjunto de recursos aceitos por ambos é conhecido.
Aceite proposto: Testar casos que a gramática não consegue expressar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S049, V3B-S024, V4B-S015, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T197 → T193 [feeds]
Como combinar: Resultado estrutural é uma entrada para controles de negócio e autorização.
Interface: Objeto validado, versão e erros.
Condição: Nenhuma regra externa é presumida pela aprovação estrutural.
Aceite proposto: Submeter objeto válido com valor não autorizado e exigir bloqueio.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: C-S049, V3B-S024, V4B-S015, V4B-S027. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar keywords obrigatórios desconhecidos como verificados.
- Manter testes negativos para campos extras, tipos, limites e referências.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Validação determinística pode tornar a interface de um modelo pequeno confiável quanto à estrutura. Compare qualidade dos dados separadamente; schema não é uma medida de inteligência.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T141, T170, T196

## Fontes primárias associadas

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S024 — JSON Schema — Object reference

[https://json-schema.org/understanding-json-schema/reference/object](https://json-schema.org/understanding-json-schema/reference/object)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Campos obrigatórios, propriedades adicionais e composição com unevaluatedProperties.

Limite: Validação estrutural depende do dialeto e implementação; não demonstra fatos externos ou autorização.

### V4B-S015 — Structural Tag Usage — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de formatos, tags, regiões livres/estruturadas e delimitadores de tokens.

Limite: Restrições formais não validam autorização, conteúdo factual nem sucesso de ferramenta.

### V4B-S027 — What are Automated Reasoning checks in Amazon Bedrock Guardrails?

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação contra política, resultados detect-only, limites de variáveis, idioma e ausência de streaming; recomenda testar tradução linguagem-lógica.

Limite: Consistência com política não valida fatos não modelados nem protege sozinha contra injeção; recursos não são caso de adoção de cliente.

### V4B-S016 — Tool Calling and Reasoning — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas específicas de formato de modelo e escolhas auto/required/forced/none para chamadas de ferramenta.

Limite: Lista de estilos não verifica checkpoint do usuário; interoperabilidade precisa ensaio por tokenizer e backend.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
