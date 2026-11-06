# T089 — Early Stopping — EOS, stop sequences, limites e parada semântica

**Nome canônico:** Critérios de término da geração  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T089  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Early Stopping; parada antecipada; EOS; stop sequences; parada semântica

## T089:C01 — conceito

Early Stopping nesta ficha cobre término de inferência por EOS, sequências de parada, limites operacionais ou condição semântica validada. EOS é um token especial; stop sequences são padrões configurados; limite de tokens ou tempo é interrupção por orçamento. A opção early_stopping em beam search tem semântica própria e não indica que uma tarefa arbitrária foi resolvida.

Como funciona:
- Identificar término normal emitido pelo modelo e distinguir essa condição de truncamento, timeout e cancelamento.
- Monitorar a geração incremental para detectar sequências de parada, inclusive padrões divididos entre tokens ou fragmentos de streaming.
- Para parada semântica, usar um verificador externo definido para a tarefa, como objeto completo validado ou teste executável satisfeito.

## T089:C02 — aplicacao

Quando usar:
- Saídas estruturadas, respostas com delimitador explícito ou ciclos de agente com condição verificável de conclusão.

Quando não usar:
- Para considerar o trabalho completo apenas porque o modelo escreveu “concluído” ou porque o orçamento acabou.

Implementação proposta:
- Proposta: declarar motivos de término distintos e propagar finish_reason até o consumidor; validar integridade antes de aceitar a saída.
- Testar a política exata do servidor para inclusão ou remoção da sequência de parada e compatibilidade com tokenizer.
- Reservar tamanho suficiente para fechar estruturas. JSON truncado deve produzir resultado incompleto, sem executar argumentos parciais de ferramenta.
- Avaliar detectores semânticos com casos positivos e negativos; escolher um critério observável e limitar o custo das verificações adicionais.

Aplicação LAI proposta:
Proposta LAI: encerrar uma etapa somente quando seu contrato estiver satisfeito; usar limites como proteção operacional e registrar pendências quando interromper.

## T089:C03 — riscos_validacao

Armadilhas:
- Um delimitador pode aparecer legitimamente dentro de texto, string JSON ou código.
- Limites de tempo da biblioteca podem ser verificados somente ao concluir um passo, sem interrupção instantânea.

Métricas sugeridas:
- Tokens poupados, conclusões prematuras, saídas truncadas, falsos términos semânticos e latência do detector.

Testes propostos:
- Teste proposto: emitir delimitador dividido em fragmentos e também dentro de uma string permitida, conferindo o comportamento especificado.
- Forçar EOS, limite e cancelamento sobre a mesma tarefa e verificar que seus estados finais permanecem diferentes.

## T089:C04 — perguntas_proveniencia

Pergunta: Atingir max_new_tokens conta como sucesso?
Resposta: Não por si só. É um limite operacional; o consumidor precisa verificar se a saída e a tarefa ficaram completas.

Pergunta: Como tornar parada semântica verificável?
Resposta: Defina antes um predicado externo, como schema válido mais campos obrigatórios conferidos, e teste seus falsos positivos.

Pergunta: EOS prova que a tarefa acabou?
Resposta: Apenas indica o término escolhido pelo modelo; a aplicação ainda precisa verificar seu contrato de resultado.

Pergunta: early_stopping tem uma única semântica?
Resposta: Não. Em APIs de geração, esse nome pode se referir especificamente à conclusão da busca com beams.

Escopo das fontes:
Transformers documenta EOS, limites, stop strings e beam search. Detector semântico e critérios LAI são propostas.

## T089:C05 — mecanismo_avancado

Uma condição de parada precisa operar na unidade correta: EOS é um token, uma sequência textual pode atravessar fronteiras de tokens e uma restrição semântica depende do artefato produzido. Em streaming, o detector deve conservar o sufixo necessário para reconhecer padrões repartidos. A parada por orçamento encerra computação, mas não transforma um JSON parcial ou uma prova incompleta em resultado concluído.

Condição de contorno:
Marcadores podem aparecer legitimamente dentro de conteúdo citado; uma regra textual cega pode interromper a tarefa cedo demais.

Contrato proposto:
- Entradas: Tokens decodificados, padrões de parada, orçamento e contrato de completude.
- Saídas: Saída entregue, razão terminal e indicação separada de validação semântica.
- Estado: Sufixo de detecção, contador e estado terminal por sequência.
- Invariante: Término de uma sequência não conclui outras sequências ainda ativas no lote.

Compromissos de projeto:
- Bufferizar caracteres facilita detectar padrões e adiciona atraso ao streaming.
- Paradas muito permissivas desperdiçam tokens; paradas agressivas podem cortar evidências necessárias.

## T089:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: dividir o marcador entre chunks, usar padrões sobrepostos e atingir orçamento antes de fechar um objeto. Esperar detecção consistente e marcação explícita de truncamento no último caso.

Plano de avaliação proposto:
Plano proposto: comparar saída integral e streaming com mesmas sequências controladas. Medir detecções incorretas, tokens excedentes, atraso e completude estrutural; aprovar quando regras terminam consistentemente sem confundir limite computacional com sucesso.

Comparações:
- T197 (complements): Um validador pode rejeitar uma estrutura interrompida, mesmo quando a geração terminou normalmente no transporte.

Afirmação rastreável:
A configuração de geração diferencia limites de novos tokens, strings de parada e early stopping de métodos com beams.
Suporte: direct; fontes: B-S009
Limite: Essas opções controlam geração; nenhuma constitui prova geral de que a resposta está correta.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T089:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu EOS, sequência textual e truncamento. Esta expansão define término como evento de protocolo: produção encerrada, artefato completo, validação concluída e resultado publicável são estados distintos que precisam de critérios próprios.

Estados de conclusão
Mantenha razões separadas para EOS, stop configurado, limite, cancelamento e erro. Depois do encerramento, valide o artefato antes de declarar sucesso. Uma resposta pode terminar normalmente e falhar no contrato, ou ser interrompida após já produzir um objeto completo; a aplicação precisa decidir sem apagar a causa real.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

Streaming e fronteira de publicação
Quando texto parcial não pode ser consumido com segurança, acumule uma região mínima até que o parser reconheça uma unidade completa. Não retenha a resposta inteira se campos independentes podem ser publicados. Porém, uma validação final pode invalidar o conjunto; deixe explícito ao consumidor quais fragmentos são provisórios.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

Parada orientada à tarefa
Use um critério externo para encerrar busca ou refinamento quando a tarefa observável estiver satisfeita. Um modelo afirmar pronto não basta. Se o critério é teste executável, registre qual teste passou e qual cobertura ele fornece; se depende de evidência faltante, termine com abstenção ou encaminhamento explícito.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

USO AVANÇADO — Extração de objeto estruturado
Cenário: Um endpoint deve devolver um registro com campos obrigatórios.
Estratégia: Combine gramática com parser incremental e limite de tamanho. Ao concluir o objeto, valide schema e regras de domínio; pare geração de texto residual apenas se o formato do modelo permitir. Não conserte silenciosamente chaves ou valores importantes.
Papel do modelo pequeno: Um 3–7B pode produzir a estrutura, enquanto código determinístico decide completude.
Aceite proposto: Exigir término classificado e rejeição de truncamentos, objetos duplicados ou campos inválidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

USO AVANÇADO — Revisão de código com orçamento
Cenário: Um agente tenta corrigir um defeito verificável.
Estratégia: Encerre ao passar o conjunto de critérios ou ao atingir limite de tentativas/tempo. Preserve a melhor versão válida e o histórico de falhas. Não trate esgotamento de orçamento como aprovação do último patch.
Papel do modelo pequeno: Um 8–30B pode propor alterações; o ambiente de testes determina quando cessar tentativas.
Aceite proposto: Medir custo por correção aceita e taxa de encerramento indevido, com falhas deliberadas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: B-S009, V4B-S015, V4B-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, formatos curtos e critérios determinísticos reduzem geração desnecessária sem depender de autocrítica sofisticada.
8–14B: Em 8–14B, separar resposta final e regiões auxiliares evita cortar delimitadores exigidos pelo template.
15–30B: Em 15–30B, controlar saídas longas por orçamento explícito e checkpoint de artefatos já válidos.
Requisitos de treino/runtime: É runtime/aplicação; EOS e convenções de template pertencem ao checkpoint, enquanto sucesso pertence ao domínio.
Não aplicar quando: Não usar uma palavra comum como stop global nem assumir que fim do stream significa resultado íntegro.

## T089:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: Delimitadores e estados de término participam do formato, sem decidir sucesso da tarefa.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013.

## T089:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T089 → T196 [complements]
Como combinar: Restringir a linguagem de saída e reconhecer término permitido pelo matcher.
Interface: Estado do parser, delimitadores e token de término.
Condição: Gramática e tokenizer representam a mesma convenção.
Aceite proposto: Testar limites em cada posição e objetos incompletos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S009, V4B-S015, V4B-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T089 → T190 [feeds]
Como combinar: Enviar razão de encerramento e artefato ao verificador antes de publicar sucesso.
Interface: Conteúdo, finish reason, tentativa e critérios satisfeitos.
Condição: O verificador distingue falha, incompletude e validade.
Aceite proposto: Interromper em limites artificiais e conferir classificação correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: B-S009, V4B-S015, V4B-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Preservar razões originais de término em logs e respostas.
- Testar padrões stop dentro de valores escapados e nas fronteiras de fragmentos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo por artefato completo e correto com a fronteira, incluindo recusas e truncamentos. Parar cedo economiza trabalho somente quando preserva o objetivo; não compensa capacidade insuficiente.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T153, T195, T196, P012

## Fontes primárias associadas

### B-S009 — Generation — GenerationConfig

[https://huggingface.co/docs/transformers/main_classes/text_generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Critérios de parada, limite de novos tokens e semântica específica de early_stopping em beam search.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### C-S008 — XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models

[https://arxiv.org/abs/2411.15100](https://arxiv.org/abs/2411.15100)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas e restrições de decodificação permitem saídas estruturadas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V4B-S015 — Structural Tag Usage — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/structural_tag.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de formatos, tags, regiões livres/estruturadas e delimitadores de tokens.

Limite: Restrições formais não validam autorização, conteúdo factual nem sucesso de ferramenta.

### V4B-S016 — Tool Calling and Reasoning — XGrammar

[https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html](https://xgrammar.mlc.ai/docs/latest/structural_tag/tool_calling_and_reasoning.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas específicas de formato de modelo e escolhas auto/required/forced/none para chamadas de ferramenta.

Limite: Lista de estilos não verifica checkpoint do usuário; interoperabilidade precisa ensaio por tokenizer e backend.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
