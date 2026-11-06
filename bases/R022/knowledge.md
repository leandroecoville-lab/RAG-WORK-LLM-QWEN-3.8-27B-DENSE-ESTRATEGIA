# R022 — Qwen

**Nome canônico:** Qwen — família de modelos  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R022  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Tongyi Qianwen; família Qwen

## R022:C01 — conceito

Qwen designa uma família de modelos do Qwen Team, Alibaba, com diferentes gerações, tamanhos, modalidades e variantes. O nome sozinho não identifica um checkpoint nem suas capacidades. A documentação diferencia modelos densos, variantes MoE e modos de uso; decisões de implantação precisam partir do identificador e da revisão exatos do modelo escolhido.

Como funciona:
- Pesos e arquitetura determinam o modelo; tokenizer, template de conversa e configuração de geração definem como a aplicação o utiliza.
- Variantes base, instruct e thinking têm objetivos e formatos distintos; controles válidos em uma não são automaticamente válidos em outra.
- Em MoE, parâmetros ativados por token e parâmetros totais são medidas diferentes, relevantes para computação e armazenamento.

Nota de nomenclatura: As páginas consultadas incluem exemplos Qwen3; eles não são declarados como geração mais recente nem como modelo instalado. Nenhum checkpoint do usuário foi inspecionado.

## R022:C02 — aplicacao

Quando usar:
- Avaliação de modelos para geração, programação ou outras modalidades suportadas pelo checkpoint específico.

Quando não usar:
- Para deduzir memória necessária, limite de contexto ou qualidade apenas pela palavra Qwen ou pelo tamanho ativo de um MoE.

Implementação proposta:
- Proposta: registrar model_id, revisão, licença, arquitetura, tokenizer, precisão e quantização do artefato candidato.
- Ler a model card e os requisitos atuais do backend; conferir template, tokens de parada e formato de ferramentas.
- Medir memória para pesos, KV e buffers sob o contexto e a concorrência pretendidos, antes de escolher a configuração.

Aplicação LAI proposta:
Proposta LAI: inventariar primeiro o checkpoint realmente instalado e então escolher as técnicas de inferência aplicáveis; esta ficha não verifica o modelo atual do usuário.

## R022:C03 — riscos_validacao

Armadilhas:
- A mesma família inclui comportamentos diferentes; aplicar um parser de raciocínio ou flag de outra variante pode quebrar a saída.
- Uma receita oficial demonstra uma combinação específica; não comprova compatibilidade com qualquer GPU, versão ou checkpoint local.

Métricas sugeridas:
- Qualidade por tarefa, memória máxima, tempo até primeiro token, latência por token e validade de chamadas estruturadas.

Testes propostos:
- Proposta: testar português, ferramentas, contexto longo e casos sem resposta com a revisão exata selecionada.
- Comparar backend e quantização contra uma referência documentada, mantendo prompts e critérios de avaliação equivalentes.

## R022:C04 — perguntas_proveniencia

Pergunta: Todo Qwen usa o mesmo template e modo de raciocínio?
Resposta: Não. Esses detalhes variam entre gerações e variantes e devem ser conferidos na documentação do checkpoint.

Pergunta: Esta ficha confirma que o modelo cabe na GPU local?
Resposta: Não. Isso exige identificar pesos, formato, backend, contexto, concorrência e memória efetivamente disponível.

Pergunta: Um modelo com poucos parâmetros ativos cabe como um denso desse tamanho?
Resposta: Não necessariamente. Os pesos totais, KV e buffers também ocupam memória.

Pergunta: Que informação falta para escolher a execução?
Resposta: Checkpoint e revisão exatos, hardware, contexto, concorrência e tarefa; o nome da família é insuficiente.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R022:C05 — mecanismo_avancado

Qwen identifica uma família de modelos, não uma configuração única de memória, contexto ou execução. A documentação de conceitos explica nomes que distinguem parâmetros totais e ativos por token em modelos MoE. O número ativo ajuda a interpretar computação, mas não equivale à memória total necessária para hospedar os pesos. Antes de integrar um checkpoint, leia configuração, tokenizer, template e capacidades declaradas para aquela revisão específica.

Condição de contorno:
Não se pode inferir qual modelo está instalado no ambiente do usuário nem concluir que o modelo exemplificado numa página é o mais recente de toda a família.

Contrato proposto:
- Entradas: Identificador e revisão do checkpoint, configuração, tokenizer, template de chat, dtype e limites efetivos do servidor.
- Saídas: Tokens e respostas com template correto, motivo de término, capacidade observada e manifesto de compatibilidade.
- Estado: Arquivos e hashes carregados, parâmetros de geração e adaptações aplicadas pelo servidor.
- Invariante: Toda medição deve permitir reconstruir qual revisão e qual serialização produziram a resposta; nome abreviado sozinho é insuficiente.

Compromissos de projeto:
- MoE pode reduzir computação ativa relativa ao total de parâmetros, mas os pesos e a comunicação continuam relevantes.
- Quantização e offload podem permitir hospedagem menor, com efeitos específicos sobre qualidade e latência a medir.

## R022:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: executar mensagens com papéis e chamadas de ferramenta usando template correto e template incompatível; comparar tokens especiais e validade do resultado, sem atribuir a diferença apenas ao modelo.

Plano de avaliação proposto:
Avaliar o checkpoint candidato no mesmo conjunto de tarefas e orçamento do baseline. Medir memória residente, throughput, cauda de latência e respostas aceitas. Registrar variantes de template e modo de raciocínio quando suportados pelo checkpoint.

Comparações:
- T184 (complements): Alguns checkpoints empregam MoE; a família não é sinônimo dessa arquitetura.
- R023 (complements): Transformers pode carregar checkpoints compatíveis e seus templates.

Afirmação rastreável:
A documentação Qwen diferencia parâmetros totais e ativos na nomenclatura de modelos MoE.
Suporte: direct; fontes: V3D-S009
Limite: Convenção documental; não identifica o modelo local nem garante suporte por todo servidor.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R022:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 exigiu identidade exata do checkpoint. Esta camada orienta seleção dentro da família, leitura de parâmetros totais/ativos e validação de modos de geração sem presumir o modelo existente no servidor.

Família e escolha concreta
O lançamento Qwen3 de 2025 fornece exemplos densos e MoE com configurações distintas. Use-o como referência datada, não como catálogo completo ou mais recente de toda a família. Antes de decidir, identifique modalidade, revisão, tamanho total, licença, template e capacidades declaradas do candidato específico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

Modos e contrato
Modos de geração e separação de campos internos ou finais podem mudar tokenização, comprimento e tratamento pelo cliente. Valide o template oficial da revisão e a forma de consumir a resposta. Uma aplicação que espera apenas JSON precisa tratar corretamente qualquer região adicional e término, sem assumir que todos os Qwen usam a mesma convenção.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

Dimensionamento honesto
Qwen3-30B-A3B ilustra a diferença entre total e ativo: computação por token não equivale a memória de pesos. Qwen3-32B denso está fora de uma faixa estrita de até 30B, embora seja próximo numericamente. Não alargue o intervalo solicitado sem declarar essa decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

USO AVANÇADO — Escolher aluno especializado
Cenário: A tarefa tem dados e critérios claros.
Estratégia: Compare candidatos dentro da faixa total desejada com o mesmo acesso a ferramentas e documentos. Avalie base, adaptação e quantização como versões distintas.
Papel do modelo pequeno: Modelos densos 3–7B podem ser candidatos a tarefas estreitas; suporte depende do checkpoint concreto.
Aceite proposto: Medir qualidade por categoria, custo de contexto e comportamento fora do domínio.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

USO AVANÇADO — Escolher MoE para serving
Cenário: A computação ativa parece atraente.
Estratégia: Inspecione pesos totais, roteamento e runtime, depois teste memória e comunicação. Compare com dense que cabe no mesmo orçamento físico.
Papel do modelo pequeno: Um MoE total 15–30B pode ser alternativa, sem ser tratado como dense de poucos bilhões.
Aceite proposto: Atender memória e prazos com qualidade observada, não estimada pelo nome.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S009, V4B-S020, V3D-S010.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Exemplos como Qwen3-4B ilustram a faixa; não confirmam qual versão é adequada ou instalada.
8–14B: Exemplos 8B e 14B permitem estudar especialização, respeitando revisão e template próprios.
15–30B: 30B-A3B exige orçamento de pesos totais; 32B não deve ser contado dentro do limite estrito.
Requisitos de treino/runtime: Modelo e runtime precisam suportar arquitetura, precisão e modo usados. Nenhum checkpoint local foi inspecionado nesta ficha.
Não aplicar quando: Não afirmar compatibilidade com uma GPU ou engine apenas pelo nome Qwen.

## R022:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C016 — Alibaba / Qwen Team / Qwen3 — modelos publicados
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: treinamento de LLM.
Uso observado: O Qwen Team publicou checkpoints densos e MoE, com configurações de heads Q/KV e distinção entre parâmetros totais e ativos.
Mecanismo documentado: Modelos como Qwen3-30B-A3B têm dimensão total distinta da quantidade ativada por token; os checkpoints densos listados usam configurações próprias de heads.
Correspondência com esta base: Fonte oficial identifica a família e seus checkpoints.
Transferência proposta para modelo pequeno: Proposta: selecionar revisões específicas dentro de 3–30B por tarefa e memória total, comparando denso e MoE sem tratar parâmetros ativos como memória de pesos.
Limite: Lançamento e benchmarks não comprovam implantação cliente nem checkpoint atual do usuário. Qwen3-32B fica fora da faixa 15–30B estrita e não é usado como exemplo dentro dela.
Fontes: V4B-S020.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q016.

## R022:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R022 → T184 [complements]
Como combinar: Variantes MoE exigem leitura separada de total, ativo e comunicação.
Interface: Configuração do checkpoint e mapas de experts.
Condição: Variante realmente é MoE.
Aceite proposto: Conferir memória física e custo por token.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S009, V4B-S020, V3D-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R022 → R023 [complements]
Como combinar: Transformers fornece classes e templates para checkpoints suportados.
Interface: Revisão, tokenizer e mensagens.
Condição: Versão da biblioteca reconhece o modelo.
Aceite proposto: Comparar tokens serializados e término da geração.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S009, V4B-S020, V3D-S010. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar usar nome abreviado como identidade de artefato.
- Não transferir contexto, licença ou formato de uma geração Qwen para outra.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare o checkpoint escolhido em tarefas reais de domínio com fronteira. A família contém modelos distintos; nenhum resultado de um membro prova capacidade de todos os demais.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

R009, R011, R023, R024, T085, T086, T133, T184

## Fontes primárias associadas

### V2B-S016 — Key Concepts — Qwen

[https://qwen.readthedocs.io/en/latest/getting_started/concepts.html](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Qwen como família de modelos, variantes, tokenização e distinção entre parâmetros totais e ativos de MoE.

Limite: Página oficial contém exemplos de gerações específicas; não estabelece qual modelo está instalado nem deve ser usada para declarar a geração mais recente.

### V2B-S017 — Quickstart — Qwen

[https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Exemplos de uso com Transformers e serving; templates e modos de raciocínio variam entre variantes Qwen3.

Limite: Receitas de modelos específicos, sem validação no hardware do usuário. Versões e parâmetros dos exemplos não são requisitos universais da família.

### V3D-S009 — Qwen — Key Concepts

[https://qwen.readthedocs.io/en/latest/getting_started/concepts.html](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Nomenclatura de parâmetros totais e ativos em modelos MoE, identidade do checkpoint e formatos de uso.

Limite: Não identifica modelo local nem estabelece qual é o lançamento mais recente de toda a família.

### V4B-S020 — Qwen3: Think Deeper, Act Faster

[https://qwenlm.github.io/blog/qwen3/](https://qwenlm.github.io/blog/qwen3/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelos densos e MoE, cabeças Q/KV, distinção entre parâmetros totais/ativos e modos de raciocínio.

Limite: Resultados de modelo publicado não verificam checkpoint local nem equivalência geral com modelos de fronteira.

### V3D-S010 — Transformers — Chat templates

[https://huggingface.co/docs/transformers/main/chat_templating](https://huggingface.co/docs/transformers/main/chat_templating)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Serialização de mensagens, tokens especiais e cuidados para não duplicá-los após aplicar template.

Limite: Página main; confirmar API e template na revisão concreta do modelo.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
