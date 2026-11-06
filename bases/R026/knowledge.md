# R026 — Guidance

**Nome canônico:** Guidance — programação controlada de geração  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** project  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R026  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** guidance Python; Guidance library

## R026:C01 — conceito

Guidance é uma biblioteca para combinar texto de prompt, geração e controle de fluxo em programas Python. Ela permite construir saídas por partes e impor restrições conforme o backend, incluindo seleção entre alternativas e geração JSON. O suporte efetivo depende do provedor e da integração; a biblioteca não transforma qualquer endpoint em um decodificador plenamente controlável.

Como funciona:
- Um objeto de modelo acumula contexto e campos gerados que o programa pode consultar por nome.
- select restringe a escolha a alternativas; gen produz segmentos conforme opções disponíveis; o código Python decide as próximas operações.
- guidance.json aceita schema ou modelos compatíveis, mas sua documentação informa suporte parcial a construções de JSON Schema.

Nota de nomenclatura: Limitações de JSON Schema são atribuídas à API documentada, não à impossibilidade teórica de representar toda restrição em qualquer sistema.

## R026:C02 — aplicacao

Quando usar:
- Classificação com rótulos fechados, extração estruturada e fluxos pequenos que combinam geração com lógica determinística.

Quando não usar:
- Quando as restrições necessárias não são suportadas pelo backend ou quando um parser determinístico já resolve a tarefa.

Implementação proposta:
- Proposta: selecionar o backend e verificar suas capacidades antes de definir a gramática ou formato esperado.
- Começar por uma seleção pequena, incluindo opção para evidência insuficiente; capturar campos gerados sem depender de posições textuais frágeis.
- Adicionar schema e validação semântica externa; registrar prompt, modelo, programa e parâmetros para reproduzir os testes.

Aplicação LAI proposta:
Proposta LAI: comparar Guidance com geração estruturada nativa em uma rotina de classificação ou extração da Helena, mantendo critérios de negócio fora do texto gerado.

## R026:C03 — riscos_validacao

Armadilhas:
- Um exemplo funcional com modelo local não demonstra os mesmos recursos em uma API remota.
- Um campo bem formatado ainda pode representar decisão errada; suporte parcial de schema exige verificar cada restrição usada.

Métricas sugeridas:
- Acurácia dos rótulos, conformidade estrutural, rejeições semânticas, latência e tokens usados por decisão aceita.

Testes propostos:
- Proposta: testar alternativas parecidas, ausência de evidência e entradas que tentam induzir rótulos fora do conjunto.
- Validar strings com escapes, objetos aninhados, limites de saída e regras numéricas no validador externo, identificando falhas de conteúdo separadamente.

## R026:C04 — perguntas_proveniencia

Pergunta: Guidance tem as mesmas capacidades em todos os modelos?
Resposta: Não. A documentação distingue o suporte por backend; cada combinação precisa ser verificada.

Pergunta: Uma escolha forçada entre rótulos garante classificação correta?
Resposta: Não. Ela garante um formato admissível quando suportada, mas ainda exige avaliar se o rótulo corresponde à entrada.

Pergunta: Se o programa aceitou o schema, todas as regras foram garantidas?
Resposta: Não presuma isso; confira suporte documentado e valide o objeto final com o contrato da aplicação.

Pergunta: Como tratar uma captura interrompida?
Resposta: Preserve o estado de incompletude, descarte uso operacional e decida entre retry limitado ou erro explícito.

Escopo das fontes:
Fontes sustentam a descrição e os mecanismos documentados. Implementação, métricas, validação e aplicação LAI abaixo são propostas editoriais; nenhuma implantação ou avaliação no servidor do usuário foi executada.

## R026:C05 — mecanismo_avancado

Guidance combina fluxo de programa e geração controlada, com capacidades que variam conforme o backend. A documentação de JSON explicita limitações de suporte a recursos do schema; não se deve presumir equivalência integral entre uma restrição declarada e a validação completa do objeto. O contrato da aplicação precisa verificar a saída terminada, inclusive regras que o mecanismo de geração não consegue impor naquele provedor.

Condição de contorno:
Um programa que funciona com controle local de logits pode não ter as mesmas capacidades numa API remota. Compatibilidade deve ser testada no backend realmente selecionado.

Contrato proposto:
- Entradas: Programa Guidance, backend, modelo, schema ou escolhas permitidas e limite de geração.
- Saídas: Capturas nomeadas, texto produzido, estado final e resultado de validação posterior do objeto completo.
- Estado: Modelo e configuração de execução, progresso das capturas e artefatos necessários ao programa.
- Invariante: Uma captura parcial ou uma restrição não suportada não pode ser promovida silenciosamente a resultado validado.

Compromissos de projeto:
- Controle programático torna o formato mais previsível, mas adiciona acoplamento às capacidades do provedor.
- Validar novamente custa trabalho, porém detecta lacunas de schema e regras de negócio que a geração não cobre.

## R026:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Proposta: exigir uma restrição de schema fora do subconjunto suportado e interromper outra geração no limite; confirmar que ambos os casos recebem diagnóstico explícito antes de qualquer consumo transacional.

Plano de avaliação proposto:
Fixar modelo, backend e tarefas. Comparar geração livre, Guidance e restrição nativa do servidor quanto a validade completa, semântica, tempo e custo. Incluir casos numéricos, objetos aninhados e truncamento, sem considerar apenas exemplos que terminam corretamente.

Comparações:
- T196 (complements): Pode utilizar restrições de geração conforme o backend.
- R025 (alternative): São ferramentas distintas; comparar capacidade concreta, não apenas o objetivo de estruturação.

Afirmação rastreável:
A documentação Guidance informa diferenças entre backends e limitações de suporte a JSON Schema.
Suporte: direct; fontes: V3D-S014, V3D-S015
Limite: As limitações são dependentes da versão; valide o subconjunto necessário ao aplicativo.

Nota de pesquisa:
Contrato, teste de falha e plano de avaliação são recomendações editoriais; nenhuma implantação ou medição deste mecanismo foi executada neste pacote.

## R026:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou diferenças de backend e captura parcial. A nova camada explica token healing, composição de trechos e validação de programas que intercalam texto fixo com geração.

Fronteira de tokens
Token healing recua na fronteira de tokenização para permitir continuações compatíveis com o prefixo textual. Isso trata um efeito de segmentação, não autoriza alterar significado do texto fornecido. O mecanismo depende de controle do backend; não presuma que qualquer endpoint remoto permite a mesma operação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

Fluxo programático
Um programa Guidance mistura texto fixo, escolhas e capturas. Defina quais partes são dados e quais controlam o fluxo, mantendo valores externos sem reinterpretá-los como instruções do programa. A execução deve registrar capturas concluídas e interrupções para que um consumidor não use um objeto incompleto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

Portabilidade por capacidade
Backends locais e remotos oferecem graus diferentes de controle. Crie uma matriz das operações realmente suportadas, incluindo restrições JSON e geração por partes. Se um recurso não existe, escolha uma alternativa explícita e reavalie o contrato; não simule sucesso com prompting que apenas pede o formato.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

USO AVANÇADO — Formulário com campos controlados
Cenário: A aplicação alterna valores fixos e texto gerado.
Estratégia: Use capturas nomeadas, escolhas fechadas quando adequadas e validação final. Teste fronteiras de tokens e encerramento por orçamento, preservando campos já determinados.
Papel do modelo pequeno: Um 3–7B pode completar estruturas estreitas com controle programático.
Aceite proposto: Objeto completo, campos corretos e ausência de alterações indevidas em texto fixo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

USO AVANÇADO — Prototipar geração composta
Cenário: Há dúvida entre programa segmentado e resposta única.
Estratégia: Implemente ambas as alternativas no mesmo backend e compare custo, qualidade e clareza do contrato. Inclua o custo de chamadas adicionais e de prefixos repetidos.
Papel do modelo pequeno: Um 8–14B pode resolver tarefas compostas, se a segmentação não remover dependências necessárias.
Aceite proposto: Medir sucesso da tarefa e manutenção do programa, não só JSON válido.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3D-S014, V3D-S015, V4B-S030.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Programas curtos e escolhas explícitas podem reduzir exigência de geração livre.
8–14B: Segmentação ajuda controle, mas deve preservar contexto relevante entre partes.
15–30B: Em 15–30B, chamadas adicionais podem dominar custo; compare com geração única restrita.
Requisitos de treino/runtime: Biblioteca de controle em Python; capacidades dependem do backend e da versão, sem promessa universal de token healing remoto.
Não aplicar quando: Não confundir controle de fluxo com verificação de fatos ou com atualização dos pesos.

## R026:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C015 — Guidance / Guidance — geração programática
Evidência: produto/recurso disponível; correspondência exata do mecanismo. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação mostra composição de prompts e geração, com token healing nos backends locais indicados e suporte de restrições dependente do provedor.
Mecanismo documentado: Recuo na fronteira do prompt permite extensões de tokens compatíveis; comandos de geração e escolha definem estrutura e fluxo.
Correspondência com esta base: É o comportamento documentado da biblioteca Guidance.
Transferência proposta para modelo pequeno: Proposta: testar extração e DSLs em 3–14B com backend local, comparando estrutura, qualidade e custo frente a geração livre seguida de validação.
Limite: Exemplos de notebook não demonstram adoção em bigtech. Token healing não corrige erro factual nem garante eficiência em qualquer endpoint remoto.
Fontes: V4B-S030, V3D-S015, V3D-S014.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q021.

## R026:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R026 → T196 [complements]
Como combinar: Restrições de geração podem ser usadas onde o backend oferece controle suficiente.
Interface: Prefixo, captura e restrição suportada.
Condição: Contrato não depende de recurso indisponível.
Aceite proposto: Testar saídas impossíveis, término e fronteiras de tokens.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S014, V3D-S015, V4B-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R026 → T197 [requires]
Como combinar: Objeto gerado precisa de validação completa após a captura.
Interface: JSON concluído e schema do consumidor.
Condição: Dialeto e recursos conhecidos.
Aceite proposto: Distinguir erro de estrutura, regra de negócio e falta de conclusão.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3D-S014, V3D-S015, V4B-S030. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não promover uma captura parcial a resultado válido.
- Verificar que texto fixo permanece exatamente conforme o contrato após token healing.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Guidance pode organizar uma aplicação pequena e reduzir erros de interface. A comparação com fronteira deve avaliar a tarefa e o custo do programa completo, sem inferir inteligência do grau de controle.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T134, T140, T141, T196, T197, R023, R024, R025

## Fontes primárias associadas

### V2B-S024 — Introduction to guidance

[https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html](https://guidance.readthedocs.io/en/latest/example_notebooks/tutorials/intro_to_guidance.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Composição de contexto, select, captura de variáveis e controle Python; suporte de restrições depende do backend.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

### V2B-S025 — guidance.json

[https://guidance.readthedocs.io/en/latest/generated/guidance.json.html](https://guidance.readthedocs.io/en/latest/generated/guidance.json.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Geração JSON com schema ou modelos tipados e limites declarados de cobertura de JSON Schema.

Limite: Documentação primária consultada nesta data; nenhum teste de integração, geração real ou benchmark no ambiente LAI foi executado.

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

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
