# T035 — Contextual Chunking

**Nome canônico:** Contextual Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T035  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** contextualização de chunks; Contextual Retrieval

## T035:C01 — conceito

Expressão usada de forma variável para preservar contexto ao segmentar ou para enriquecer cada trecho antes da indexação. Neste pacote, refere-se principalmente a contextualização de chunks: adicionar uma descrição curta que situa o trecho no documento, mantendo separado o texto original.

Como funciona:
- Identificar documento, seção e entidades relevantes ao trecho.
- Gerar ou extrair um pequeno contexto explicativo.
- Indexar contexto e trecho sem perder a fronteira entre fonte e texto derivado.

Nota de nomenclatura: O nome original é amplo; o mecanismo específico documentado pela Anthropic é Contextual Retrieval, não um splitter universal.

## T035:C02 — aplicacao

Quando usar:
- Trechos com pronomes ou nomes abreviados que ficam ambíguos isoladamente.
- Coleções de relatórios semelhantes de produtos ou versões distintas.

Quando não usar:
- Não adicionar resumo inventado ou informações externas como se fizessem parte da fonte.

Implementação proposta:
- Proposta: preferir metadados determinísticos quando suficientes.
- Se usar LLM, validar contexto produzido contra o documento original.
- Preservar campos separados original_text e contextual_prefix para auditoria e citações.

Aplicação LAI proposta:
Proposta LAI: acrescentar software, versão e seção em cada fragmento técnico antes de buscar descrições geradas mais elaboradas.

## T035:C03 — riscos_validacao

Armadilhas:
- Contextualização errada contamina simultaneamente busca lexical e vetorial.
- Um prefixo grande pode dominar o embedding e reduzir discriminação do trecho.

Métricas sugeridas:
- Recall de perguntas com entidades implícitas.
- Taxa de contextos adicionados sem apoio no documento.

Testes propostos:
- Usar relatórios de dois produtos com os mesmos termos e exigir distinção correta.
- Trocar o documento pai e verificar invalidação da contextualização derivada.

## T035:C04 — perguntas_proveniencia

Pergunta: Contextual Retrieval muda necessariamente as fronteiras?
Resposta: Não. Pode manter os mesmos chunks e acrescentar informação que os situa no documento.

Pergunta: A descrição adicionada pode ser citada como fonte primária?
Resposta: Não por si só. A citação deve apontar para o trecho original que a sustenta.

Pergunta: Late Chunking produz uma explicação textual adicional?
Resposta: Não necessariamente. A informação contextual entra nas representações dos tokens antes do agrupamento que forma o embedding do trecho.

Pergunta: O prefixo precisa conter um resumo completo?
Resposta: Não. O objetivo é resolver o que torna aquele trecho ambíguo. Resumo amplo pode ocupar espaço e reduzir sua especificidade.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T035:C05 — mecanismo_avancado

A contextualização altera a representação de busca antes da consulta: termos de entidade, período e escopo passam a integrar o texto indexado. Isso pode elevar a recuperação de um trecho ambíguo, mas também contaminar dois caminhos simultaneamente quando o prefixo é usado em embeddings e BM25. A atualização documental deve considerar dependências além do chunk: o prefixo pode depender de outra seção.

Condição de contorno:
Quando metadados determinísticos já resolvem a ambiguidade, gerar uma descrição pode adicionar custo e erro sem melhorar a discriminação entre trechos.

Contrato proposto:
- Entradas: Chunk original, contexto documental autorizado e revisão consistente da fonte.
- Saídas: Anotação contextual separada do texto citado, com dependências documentais registradas.
- Estado: Modelo contextualizador, template, versões do índice e associação entre prefixo e original.
- Invariante: Termos acrescentados para busca permanecem identificáveis como anotação, sem se tornarem evidência primária.

Compromissos de projeto:
- Contexto específico resolve referências locais, mas prefixos semelhantes podem aproximar artificialmente todos os chunks.
- Gerar anotações na ingestão amortiza custo de consulta e exige reprocessamento quando as dependências mudam.

## T035:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: mudar a entidade descrita na introdução sem alterar o chunk. A indexação deve invalidar o prefixo dependente e impedir recuperação que ainda atribua o trecho à entidade antiga.

Plano de avaliação proposto:
Avaliação proposta: comparar original, metadados determinísticos e contexto gerado, mantendo recuperador e orçamento iguais. Medir recuperação de referências implícitas, erros adicionados, custo de reindexação e diversidade dos candidatos; distinguir ganho lexical de ganho vetorial.

Comparações:
- T011 (distinct_from): Mudar fronteiras por similaridade não equivale a contextualizar a representação de um chunk existente.
- T027 (complements): Contextualização pode beneficiar busca lexical e vetorial; a fusão ainda precisa ser avaliada com candidatos equivalentes.

Afirmação rastreável:
Contextual Retrieval acrescenta contexto específico do trecho antes da indexação vetorial e lexical; Late Chunking contextualiza vetores antes do pooling.
Suporte: direct; fontes: A-S025, V3A-S014
Limite: São mecanismos distintos; resultados de um não demonstram eficácia do outro nem superioridade em qualquer acervo.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T035:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou contaminação do prefixo contextual. Aqui a expansão contextual é controlada por contrafactuais de identidade e granularidade.

Projeto e decomposição
Limite contexto adicionado a identificadores e localização que realmente desambiguam o trecho. Comentário explicativo longo pode dominar embedding e aproximar chunks diferentes indevidamente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

Controle adaptativo
Separe texto original, contexto gerado e campos estruturados. A busca pode usar todos; o leitor deve saber qual parte foi extraída e qual foi inferida na ingestão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

Validação contrafactual
Compare prefixos curtos, longos e ausência de prefixo. Troque entidades em documentos estruturalmente iguais para detectar vazamento de identidade e medir ranking de homônimos. Unidade de avaliação: chunk contextualizado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

USO AVANÇADO — Relatórios padronizados
Cenário: Trechos iguais pertencem a períodos distintos.
Estratégia: Adicionar organização, período e seção verificados; preservar esses atributos também como filtros, não apenas palavras no prefixo.
Papel do modelo pequeno: 3–7B gera contexto a partir de campos.
Aceite proposto: Consulta histórica não pode recuperar período errado por similaridade.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

USO AVANÇADO — Documentação de componentes
Cenário: Pronome referencia módulo distante.
Estratégia: Resolver referente pelo escopo documental e anexar identificação mínima; se houver ambiguidade, manter candidatos em vez de escolher silenciosamente.
Papel do modelo pequeno: 8–14B resolve referência local.
Aceite proposto: Toda identidade adicionada precisa de apoio no documento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S025, V3A-S014, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de prefixo determinístico verbalizado a partir de metadados.
8–14B: Resolvedor contextual para pronomes e escopo de seção.
15–30B: Revisor de casos ambíguos que atravessam vários documentos.
Requisitos de treino/runtime: Campos verificados, marcação de conteúdo gerado e reindexação quando escopo mudar.
Não aplicar quando: Contexto só pode ser obtido por especulação ou prefixo melhora similaridade mas piora precisão de evidências.

## T035:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009, V4A-Q019, V4A-Q022.

## T035:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T035 → T066 [requires]
Como combinar: Confirmar entidade e versão usadas no prefixo.
Interface: Identificador, escopo e evidência da resolução.
Condição: Resolver preservar ambiguidade não resolvida.
Aceite proposto: Testar duas entidades de mesmo nome.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S025, V3A-S014, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T035 → T027 [complements]
Como combinar: Aplicar contexto com avaliação separada por canal.
Interface: Texto original, prefixo e campos filtráveis.
Condição: Prefixo não apagar termos literais raros.
Aceite proposto: Medir contribuição lexical e vetorial independentemente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S025, V3A-S014, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não citar prefixo gerado como fonte primária.
- Evitar copiar título desatualizado para todos os chunks.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar desambiguação e precisão; contexto adicional pode ajudar indexação e prejudicar um leitor pequeno se não for rotulado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T033, T036, T027

## Fontes primárias associadas

### A-S025 — Introducing Contextual Retrieval

[https://www.anthropic.com/research/contextual-retrieval](https://www.anthropic.com/research/contextual-retrieval)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contextualização de trechos antes da indexação vetorial e lexical.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S014 — Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models

[https://arxiv.org/abs/2409.04701](https://arxiv.org/abs/2409.04701)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Contextualização antes da segmentação final e do mean pooling; distinta de gerar prefixos textuais para chunks.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
