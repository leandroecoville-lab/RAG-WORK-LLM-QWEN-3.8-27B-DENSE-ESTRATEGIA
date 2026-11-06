# R025 — XGrammar

**Nome canônico:** XGrammar — motor de geração estruturada  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R025  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** xgrammar; XGrammar constrained decoding

## R025:C01 — conceito

XGrammar implementa geração estruturada por restrições durante a decodificação. A biblioteca compila descrições como JSON Schema ou gramáticas e calcula quais tokens podem continuar a saída. Ela atua no processo de amostragem, não apenas na validação do texto pronto. A estrutura admitida continua diferente da correção factual e das regras de negócio.

Como funciona:
- A gramática compilada depende da configuração de tokenização e pode ser compartilhada entre solicitações compatíveis.
- Cada solicitação mantém seu próprio GrammarMatcher; uma máscara remove tokens inválidos dos logits antes da amostragem.
- Após aceitar o token escolhido, o matcher avança; a condição de término precisa respeitar o estado da geração estruturada.

Nota de nomenclatura: Não promete suporte a toda construção de schema ou a qualquer checkpoint. Nenhum backend foi configurado ou testado nesta entrega.

## R025:C02 — aplicacao

Quando usar:
- Extração, contratos de ferramentas e respostas estruturadas quando o runtime oferece integração compatível.

Quando não usar:
- Para comprovar verdade, autorização ou relações semânticas que não estão expressas e verificadas no contrato.

Implementação proposta:
- Proposta: escolher um schema pequeno e registrar sua versão junto ao tokenizer e ao modelo.
- Usar a integração do backend ou conectar compilação, máscara e atualização de estado a cada passo de geração.
- Manter estado separado por solicitação, rejeitar gramáticas incompatíveis e validar o objeto completo com um validador independente.

Aplicação LAI proposta:
Proposta LAI: avaliar XGrammar para contratos estruturados do executor e extrações do RAG; verificar conteúdo, identificadores e evidências após a geração.

## R025:C03 — riscos_validacao

Armadilhas:
- Compartilhar um matcher mutável entre usuários pode contaminar o estado; compartilhar somente a gramática compilada apropriada.
- Interromper pelo limite de tokens pode deixar um prefixo válido e uma saída incompleta; não tratá-la como objeto final aceito.

Métricas sugeridas:
- Validade sintática, conformidade ao schema, conclusão íntegra, latência de compilação e impacto no tempo por token.

Testes propostos:
- Proposta: testar objetos aninhados, Unicode, campos obrigatórios, restrições impossíveis e orçamento insuficiente de saída.
- Misturar solicitações com schemas diferentes no mesmo lote e verificar isolamento, término e rejeição de tokens inadmissíveis.

## R025:C04 — perguntas_proveniencia

Pergunta: JSON válido significa resposta correta?
Resposta: Não. O objeto pode cumprir a estrutura e ainda conter valores falsos ou incompatíveis com a evidência.

Pergunta: Basta escrever uma gramática no prompt?
Resposta: Não. A restrição precisa ser implementada pelo backend durante a decodificação; o prompt também deve explicar o conteúdo esperado.

Pergunta: Posso compartilhar o mesmo matcher entre pedidos?
Resposta: Não como estado mutável único: cada sequência precisa de seu próprio progresso gramatical.

Pergunta: JSON válido prova resposta correta?
Resposta: Não. Sintaxe, regras de domínio e correspondência com evidência precisam de verificações distintas.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R025:C05 — mecanismo_avancado

Na integração do XGrammar, informação do tokenizer, compilador e gramática compilada podem ser preparados para reúso apropriado. O estado do matcher acompanha a sequência de cada requisição: gerar máscara, aplicá-la aos logits antes de amostrar e aceitar o token escolhido são etapas distintas. Em lotes, a linha da máscara precisa corresponder à requisição correta. Rollback especulativo exige manter estado gramatical e sequência de tokens coerentes.

Condição de contorno:
Restringir tokens à linguagem aceita não verifica fatos, autorização ou regras de negócio externas. Uma saída interrompida por orçamento pode continuar incompleta mesmo com prefixo gramatical válido.

Contrato proposto:
- Entradas: Tokenizer compatível, gramática ou schema suportado, logits da etapa e estado de cada sequência ativa.
- Saídas: Máscara de tokens permitidos, decisão amostrada e estado atualizado ou término reconhecido.
- Estado: Artefato compilado reutilizável e matcher específico por sequência, com associação estável à posição do lote.
- Invariante: Cada token confirmado deve avançar exatamente o matcher correspondente; token descartado por rollback não pode permanecer aceito.

Compromissos de projeto:
- Compilação reutilizável amortiza custo, mas requer chave que identifique gramática e tokenizer.
- Restrições reduzem saídas malformadas, enquanto schemas complexos ou incompatíveis ampliam custo e risco de integração.

## R025:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: permutar requisições no lote e rejeitar um ramo especulativo; verificar que máscaras e histórico do matcher acompanham a sequência correta, sem contaminar a vizinha.

Plano de avaliação proposto:
Comparar geração livre com validação posterior e geração restrita, mantendo modelo e tarefas. Medir validade completa, acerto semântico, latência de compilação, latência por token e interrupções. Separar primeira compilação de uso aquecido.

Comparações:
- T196 (specializes): Implementa restrição gramatical durante a decodificação.
- T197 (complements): Validação posterior continua verificando o objeto completo e regras adicionais.

Afirmação rastreável:
A integração usa máscara antes da amostragem e estado de matcher associado à sequência.
Suporte: direct; fontes: V3D-S013
Limite: A documentação de integração não garante suporte irrestrito a todo schema ou backend.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R025:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou matcher por sequência e rollback. A nova camada usa structural tags e modos de chamada de ferramenta para desenhar contratos mistos, com testes de fronteiras e custos de compilação.

Programa de saída
Structural tags permitem especificar regiões livres e estruturadas no fluxo. Modele transições entre explicação e objeto de ferramenta, em vez de aplicar uma restrição genérica a toda a resposta. Delimitadores precisam corresponder ao template do modelo e às regras do consumidor.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

Modos de ferramenta
A documentação distingue escolhas como automático, obrigatório, ferramenta forçada e ausência de chamada, conforme integração. O contrato deve refletir o modo realmente solicitado. Forçar uma ferramenta não demonstra que ela é apropriada para a intenção; seleção semântica e autorização continuam externas.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

Compilação e reúso
Gramáticas compiladas podem ser reutilizadas quando tokenizer e contrato são compatíveis, mas matcher continua pertencendo à sequência. Meça compilação e cache em schemas dinâmicos. Um catálogo com muitas variações pode consumir memória e introduzir latência inicial que não aparece em benchmark com gramática já pronta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

USO AVANÇADO — API de domínio
Cenário: O agente deve escolher uma ferramenta e preencher argumentos.
Estratégia: Use modo e tags compatíveis, compile schemas conhecidos e valide objeto completo antes de executar. Teste quando a resposta correta é não chamar ferramenta.
Papel do modelo pequeno: Um 3–7B pode preencher contratos estreitos com menos erros de sintaxe.
Aceite proposto: Medir escolha correta, argumentos corretos e validade estrutural separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

USO AVANÇADO — Texto com trecho estruturado
Cenário: A aplicação precisa exibir explicação e consumir um objeto.
Estratégia: Defina fronteiras inequívocas e teste tokens que incluem vários caracteres estruturais. Confirme conclusão e parser antes de liberar o objeto ao consumidor.
Papel do modelo pequeno: Um 8–14B pode produzir resposta mista mantendo o controle do fluxo.
Aceite proposto: Nenhum fragmento livre interpretado como ação e nenhuma estrutura parcial aceita.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S013, V4B-S015, V4B-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Schemas simples tornam a restrição útil sem sobrecarregar contexto ou compilação.
8–14B: Teste tags e modos próprios do checkpoint; o mesmo desenho textual pode tokenizar diferente.
15–30B: Modelos maiores não eliminam necessidade de matcher correto em lotes e especulação.
Requisitos de treino/runtime: Biblioteca integrada ao loop de amostragem; exige suporte do engine e do tokenizer, sem treino obrigatório.
Não aplicar quando: Não supor suporte integral a todo JSON Schema nem equivalência de templates entre famílias.

## R025:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: É a implementação XGrammar documentada.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013.

## R025:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R025 → T196 [feeds]
Como combinar: XGrammar implementa máscaras e estados para geração restringida.
Interface: Gramática compilada, matcher e logits.
Condição: Integração respeita sequência e rollback.
Aceite proposto: Testar prefixos, conclusão e tokens proibidos.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4B-S015, V4B-S016. Casos: V4B-C014.

2. R025 → T197 [complements]
Como combinar: Validação final cobre contrato completo e diferenças de recursos suportados.
Interface: Objeto e schema versionado.
Condição: Dialeto e limites conhecidos.
Aceite proposto: Rejeitar saída truncada e campos semanticamente inválidos em camada própria.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S013, V4B-S015, V4B-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não compartilhar matcher mutável entre sequências concorrentes.
- Invalidar cache de gramática quando tokenizer ou contrato muda.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
XGrammar pode melhorar confiabilidade de interface de um modelo pequeno. Compare campos corretos e decisões de ferramenta; estrutura garantida não equivale a competência geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T140, T141, T196, T197, R009, R011, R023, R026

## Fontes primárias associadas

### V2B-S022 — XGrammar — Quick Start

[https://xgrammar.mlc.ai/docs/latest/start/quick_start.html](https://xgrammar.mlc.ai/docs/latest/start/quick_start.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compilação de gramáticas, JSON Schema, tokenizer e integração de geração restrita.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V2B-S023 — XGrammar — Integration with LLM Engine

[https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html](https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramática compartilhável, matcher por solicitação, máscaras de tokens, aceitação e término.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V3D-S013 — XGrammar — Engine integration

[https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html](https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos de tokenizer, compilação, matcher por sequência e máscara antes da amostragem.

Limite: Integração exige sincronização com a sequência; restrição sintática não comprova correção semântica.

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
