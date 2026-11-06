# T196 — Constrained Decoding / Grammar-Constrained Decoding

**Nome canônico:** Decodificação restrita por gramática  
**Grupo:** Verificação, treinamento e especialização  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T196  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Constrained Decoding; decodificação restrita; grammar-guided decoding; Grammar-Constrained Decoding; grammar-constrained generation

## T196:C01 — conceito

Constrained Decoding restringe tokens durante a geração para manter o prefixo dentro de uma linguagem permitida. Grammar-Constrained Decoding é sua forma orientada por gramática, útil para JSON, DSLs e estruturas de chamadas. Pode reduzir erros de sintaxe, mas não demonstra verdade factual, autorização ou correção de domínio. Um JSON válido ainda pode conter valores incorretos.

Como funciona:
- Compilar gramática ou restrições suportadas em um estado que acompanha o prefixo emitido.
- A cada passo, calcular continuações permitidas e mascarar tokens que tornariam a conclusão inválida.
- Permitir término somente em estado aceitável, ou retornar falha/incompletude quando orçamento e restrições impedirem a conclusão.

## T196:C02 — aplicacao

Quando usar:
- Interfaces que exigem saída parseável, enumerações limitadas ou linguagem formal com contrato previamente conhecido.

Quando não usar:
- Como único verificador de cálculos, fatos, permissões ou efeitos de uma ação externa.

Implementação proposta:
- Proposta: declarar a gramática e o subconjunto de JSON Schema aceito pelo engine; nem toda restrição semântica vira gramática.
- Testar compatibilidade com tokenizer, tokens especiais, Unicode e escapes; reservar orçamento para encerrar a estrutura.
- Versionar schema e gramática juntos, invalidando artefatos compilados quando mudarem.
- Após decodificar, executar parser, validação de schema e regras de domínio; registrar recusa, truncamento e ausência de continuação admissível como estados distintos.

Aplicação LAI proposta:
Proposta LAI: restringir formato de comandos candidatos e exigir verificações externas antes da execução; a gramática compõe o contrato de saída, sem substituir o controlador de integridade.

## T196:C03 — riscos_validacao

Armadilhas:
- Uma gramática inconsistente pode bloquear a geração; uma excessivamente permissiva pode aceitar estruturas inúteis.
- Aplicar uma sequência de parada antes do fechamento da estrutura pode produzir prefixo válido, porém documento incompleto.

Métricas sugeridas:
- Taxa de parse válido, violações de domínio, latência de compilação, overhead de decodificação e saídas sem término válido.

Testes propostos:
- Teste proposto: gerar strings com aspas, barras, Unicode e valores enumerados, incluindo casos próximos dos limites.
- Forçar truncamento e gramática incompatível e verificar que o consumidor não executa argumentos parciais.

## T196:C04 — perguntas_proveniencia

Pergunta: Grammar-Constrained Decoding valida só depois da geração?
Resposta: Não. Restringe escolhas durante a geração; validação posterior permanece útil para integridade final e regras de domínio.

Pergunta: Uma gramática garante um identificador real e autorizado?
Resposta: Não. Pode garantir a forma do identificador; existência e autorização precisam de consulta e verificação externas.

Pergunta: Token estruturalmente permitido pode estar errado?
Resposta: Sim. Um número ou identificador pode obedecer à gramática e designar um valor incorreto.

Pergunta: EOS sempre significa JSON completo?
Resposta: Somente se o protocolo de término exige completude; truncamento e políticas de parada externas precisam ser tratados separadamente.

Escopo das fontes:
XGrammar fundamenta restrição por gramática; JSON Schema fundamenta validação estrutural. Contrato LAI e testes são propostas.

## T196:C05 — mecanismo_avancado

Uma gramática válida para caracteres precisa ser relacionada aos tokens reais do modelo, que podem conter fragmentos ou vários símbolos estruturais. O estado do matcher deve avançar pelo token escolhido e produzir a máscara da etapa seguinte. Tamanho de vocabulário do tokenizer e dimensão dos logits também podem diferir por padding. Um prefixo ainda extensível não é uma estrutura concluída quando o orçamento termina.

Condição de contorno:
Restrições incompatíveis podem deixar nenhum token permitido; remover a máscara silenciosamente violaria o contrato estrutural.

Contrato proposto:
- Entradas: Gramática ou schema suportado, tokenizer, dimensão dos logits e estado de geração.
- Saídas: Tokens permitidos e resultado com estado de conclusão explícito.
- Estado: Gramática compilada, matcher por sequência e máscaras alinhadas ao vocabulário.
- Invariante: A máscara corresponde exatamente ao prefixo confirmado daquela sequência.

Compromissos de projeto:
- Restringir tokens reduz erros estruturais e adiciona custo de compilação ou matching.
- Gramáticas rígidas podem excluir representações válidas que o contrato não descreveu.

## T196:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: reutilizar matcher de outra sequência e encerrar a geração antes do fechamento de um objeto. Esperar detecção do estado incompatível e indicação de estrutura incompleta, sem fallback irrestrito.

Plano de avaliação proposto:
Plano proposto: comparar geração livre e restrita sob o mesmo schema e modelo. Medir validade completa, conteúdo correto, latência e casos sem continuação; exigir validação final independente e separar sucesso sintático de factualidade.

Comparações:
- T197 (complements): Schema validation examina o objeto produzido; constrained decoding restringe o caminho enquanto ele é produzido.

Afirmação rastreável:
O workflow XGrammar vincula compilação ao tokenizer e mantém um matcher que aceita tokens e gera máscaras subsequentes.
Suporte: direct; fontes: V3B-S025
Limite: O suporte de grammar/schema e término depende da implementação; estrutura permitida não prova fatos externos.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T196:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 explicou matcher e alinhamento de tokens. O aprofundamento trata regiões livres e estruturadas, interação com ferramentas e especulação e confirmação do objeto completo antes de uso.

Estrutura por regiões
XGrammar documenta structural tags para combinar texto livre e regiões com formato restrito. Isso permite tratar raciocínio, texto e chamada de ferramenta com estados distintos, mas exige delimitadores compatíveis com o formato do modelo. Não aplique uma gramática de um template a outro apenas porque ambos parecem JSON.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

Conclusão e entrega
Um prefixo permitido pode terminar por limite de tokens antes de formar objeto completo. O serviço deve comunicar término, validar estrutura final e impedir que fragmentos sejam executados como chamada de ferramenta. Streaming pode exibir progresso, mas não autoriza tratar uma chamada incompleta como ação confirmada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

Especulação e máscara
Propostas especulativas precisam respeitar o estado correto da gramática durante verificação e rollback. A Apple descreve combinação de geração guiada e especulação no framework local. Essa evidência sustenta a combinação naquela pilha, sem garantir suporte de qualquer runtime, tokenizer ou versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

USO AVANÇADO — Chamada de ferramenta tipada
Cenário: O modelo precisa produzir nome e argumentos válidos.
Estratégia: Compile restrições compatíveis, mantenha matcher por sequência e valide argumentos completos antes da autorização. Regras de negócio e permissões continuam externas.
Papel do modelo pequeno: Um 3–7B pode preencher contratos estreitos com menos falhas sintáticas.
Aceite proposto: Medir validade estrutural, campos semanticamente corretos e chamadas indevidas separadamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

USO AVANÇADO — Saída mista
Cenário: A resposta contém explicação e um objeto que será consumido por software.
Estratégia: Use regiões estruturadas explícitas e mantenha o parser alinhado ao template. Teste delimitadores dentro de strings e encerramento prematuro.
Papel do modelo pequeno: Um 8–14B pode explicar e estruturar, sem que texto livre seja interpretado como comando.
Aceite proposto: Nenhum objeto parcial aceito e nenhuma confusão entre texto e ação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Restringir formato ajuda utilização prática, mas não ensina o significado dos campos.
8–14B: Schemas complexos podem reduzir liberdade útil ou elevar custo de compilação; medir.
15–30B: Maior porte não dispensa gramática quando a interface exige estrutura exata.
Requisitos de treino/runtime: Runtime com integração de logits e tokenizer; treino não é obrigatório para a restrição, mas o modelo precisa compreender a tarefa.
Não aplicar quando: Não confundir saída sintaticamente válida com dados verdadeiros ou autorização de ação.

## T196:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4D-C001 — Apple / Foundation Models / Apple Intelligence OS 26
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Framework do modelo local disponibilizado no OS 26 e utilizado por aplicativos citados pela Apple.
Mecanismo documentado: A descrição técnica associa modelo de cerca de 3B, quantização, adaptadores, ferramentas e combinação de geração guiada com especulação.
Correspondência com esta base: Geração guiada compila restrições sobre a saída.
Transferência proposta para modelo pequeno: Proposta: restringir o pequeno modelo a extrair ou produzir objetos de domínio, validar conteúdo após a gramática e medir latência com especulação ligada/desligada.
Limite: Classificação conservadora de produto disponível: não há telemetria pública de uso de cada mecanismo nem demonstração de equivalência com fronteira. Aplicativos externos não são contados como implantações próprias da Apple.
Fontes: V4D-S002, V4D-S006, V4D-S011.

V4B-C015 — Guidance / Guidance — geração programática
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.
Mecanismo documentado: Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.
Correspondência com esta base: Restrições são aplicadas durante geração em backends compatíveis.
Transferência proposta para modelo pequeno: Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.
Limite: Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.
Fontes: V4B-S030, V3D-S015, V3D-S014.

V4B-C014 — MLC / XGrammar / XGrammar structural tags
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: A biblioteca documenta construção de gramáticas com regiões livres, delimitadores e envelopes de ferramentas específicos de famílias de modelos.
Mecanismo documentado: Tags estruturais e matcher restringem continuações; modos de tool choice controlam se chamadas são permitidas, exigidas ou forçadas.
Correspondência com esta base: Restringe geração por gramática durante decoding.
Transferência proposta para modelo pequeno: Proposta: usar com um pequeno modelo que domine a tarefa e validar argumentos contra regras de negócio antes de executar ferramentas.
Limite: Disponibilidade de biblioteca não é deployment comprovado. Gramática correta não prova fatos, autorização, intenção ou sucesso da ação.
Fontes: V4B-S015, V4B-S016.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q013.

## T196:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T196 → T079 [complements]
Como combinar: O framework Apple documenta geração guiada combinada com especulação.
Interface: Estado de restrição e tokens confirmados.
Condição: Suporte da pilha descrita, sem extrapolação para outros backends.
Aceite proposto: Testar aceitação e conclusão com gramática ativa.
Natureza: combinação descrita em fonte; ver estágio do caso. Fontes: V4D-S002. Casos: V4D-C001.

2. T196 → T197 [requires]
Como combinar: Validação final confirma o objeto no dialeto e regras adotados pelo consumidor.
Interface: Objeto completo e schema versionado.
Condição: Recursos do gerador e validador são compatíveis.
Aceite proposto: Testar limites de geração, campos extras e regras não suportadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S025, C-S008, V4B-S015, V4B-S016, V4D-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Invalidar matcher ao reiniciar uma sequência com outro prefixo.
- Não interpretar encerramento por limite como conclusão válida.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
A comparação com fronteira deve medir conteúdo correto dentro do contrato. Gramática pode equalizar parte da confiabilidade de interface, sem equalizar conhecimento ou capacidade de decisão.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T197, T195, P012, P015

## Fontes primárias associadas

### C-S008 — XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models

[https://arxiv.org/abs/2411.15100](https://arxiv.org/abs/2411.15100)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gramáticas e restrições de decodificação permitem saídas estruturadas.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### C-S049 — JSON Schema Validation: A Vocabulary for Structural Validation of JSON

[https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Vocabulário de tipos, valores, arrays e objetos valida estrutura; não valida veracidade factual.

Limite: Conteúdo consultado na data indicada; não houve reprodução experimental do trabalho.

### V3B-S025 — Workflow of XGrammar

[https://xgrammar.mlc.ai/docs/latest/start/workflow_of_xgrammar.html](https://xgrammar.mlc.ai/docs/latest/start/workflow_of_xgrammar.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Compilação vinculada ao tokenizer, máscara de vocabulário, avanço e término do matcher.

Limite: Documentação dinâmica consultada; gramática limita estrutura e não verifica fatos externos.

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

### V4D-S002 — Apple’s On-Device and Server Foundation Models: 2025 Updates

[https://machinelearning.apple.com/research/apple-foundation-models-2025-updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo local de cerca de 3B, QAT de pesos a 2 bits, KV a 8 bits e runtime que combina geração guiada e decodificação especulativa; adaptadores e ferramentas.

Limite: A arquitetura com compartilhamento de KV depende do modelo treinado. Recursos do modelo servidor, como PT-MoE e combinação de atenção local/global, não são automaticamente recursos do modelo local.

### V3D-S014 — Guidance — guidance.json

[https://guidance.readthedocs.io/en/latest/generated/guidance.json.html](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contrato da geração JSON e limitações de suporte a recursos de JSON Schema.

Limite: Suporte depende da versão; saída final e regras de domínio precisam de validação própria.

### V3D-S015 — Guidance — Introduction

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Fluxo programático e diferenças de capacidade entre backends locais e remotos.

Limite: Compartilhamento interno de recursos não implica fronteira de segurança ou equivalência de provedores.

### V4B-S030 — Token healing — Guidance

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/token_healing.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Tratamento de fronteiras de tokenização por recuo e prefixo restrito; integração documentada com LlamaCpp/Transformers.

Limite: Exemplos não comprovam qualidade de domínio nem implementação eficiente em todo provedor remoto.

### V4D-S006 — Apple’s Foundation Models framework unlocks new app experiences

[https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Framework disponível com OS 26; exemplos de aplicativos já usando o modelo local, inclusive SmartGym e Stoic.

Limite: Aplicativos citados são operadores distintos, não dez implantações próprias da Apple. Descrição do fornecedor sem benchmark independente do usuário.

### V4D-S011 — New Apple Intelligence features are available today

[https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/](https://www.apple.com/newsroom/2025/09/new-apple-intelligence-features-are-available-today/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Disponibilidade em OS 26, ações de Shortcuts e aplicativos que já utilizam Foundation Models.

Limite: Não atribui todos os recursos multimodais ao mesmo modelo textual de 3B. Private Cloud Compute e integrações externas possuem limites distintos.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
