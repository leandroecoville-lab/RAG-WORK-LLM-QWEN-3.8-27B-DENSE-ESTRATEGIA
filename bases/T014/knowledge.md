# T014 — Progressive Disclosure

**Nome canônico:** Progressive Disclosure  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T014  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** divulgação progressiva; carregamento por camadas

## T014:C01 — conceito

Expõe informação em camadas conforme a necessidade: primeiro um catálogo enxuto, depois instruções e finalmente fontes completas. O recurso permanece acessível, mas somente a parte necessária entra na chamada. É um padrão de interface e contexto, não um mecanismo de memória paramétrica.

Como funciona:
- Publicar metadados que permitam descobrir a capacidade ou documento.
- Carregar instruções essenciais após a seleção.
- Abrir exemplos, arquivos e fontes detalhadas apenas quando a tarefa exigir.

## T014:C02 — aplicacao

Quando usar:
- Catálogos grandes de ferramentas, skills e documentação.
- Agentes com muitas capacidades especializadas usadas raramente.

Quando não usar:
- Não ocultar restrições obrigatórias nem dados cuja ausência impede perceber que uma busca é necessária.

Implementação proposta:
- Proposta: criar índice por objetivo, entradas e saídas de cada recurso.
- Preservar referências estáveis e indicar quando há conteúdo adicional.
- Medir descoberta com solicitações sem o nome exato da ferramenta e manter fallback de pesquisa.

Aplicação LAI proposta:
Proposta LAI: manter no contexto da Helena um catálogo compacto de capacidades e carregar contratos completos antes de qualquer execução dependente deles.

## T014:C03 — riscos_validacao

Armadilhas:
- Descrições vagas tornam recursos invisíveis.
- O agente pode confundir o resumo do recurso com sua instrução completa.

Métricas sugeridas:
- Taxa de descoberta da capacidade correta.
- Tokens carregados até resolver a tarefa, incluindo buscas adicionais.

Testes propostos:
- Pedir uma tarefa por paráfrase e conferir seleção correta da skill.
- Remover o documento detalhado e exigir aviso de leitura incompleta.

## T014:C04 — perguntas_proveniencia

Pergunta: Preciso colocar as 218 entradas no prompt inicial?
Resposta: Não. Um índice de descoberta pode selecionar as entradas pertinentes e seus trechos.

Pergunta: Progressive disclosure reduz conhecimento disponível?
Resposta: Reduz informação imediatamente carregada; o acervo continua acessível por recuperação.

Pergunta: Posso resumir todas as regras no catálogo?
Resposta: Pode aumentar custo e ambiguidade. Inclua condições discriminativas e mantenha a instrução completa acessível, identificando o resumo como resumo.

Pergunta: Carregar uma skill concede autorização para executar tudo nela?
Resposta: Não. Descoberta e leitura disponibilizam instruções; autorização continua vinculada à tarefa e aos controles do ambiente, sem expansão automática de escopo.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T014:C05 — mecanismo_avancado

O catálogo inicial funciona como um mecanismo de roteamento: se a descrição não expõe a condição de uso de um recurso, o agente pode nunca abrir o conteúdo que resolveria a tarefa. Assim, economizar tokens na primeira camada exige preservar informação discriminativa. A versão dos metadados também deve corresponder à versão das instruções e recursos carregados depois.

Condição de contorno:
O padrão falha quando detalhes essenciais à escolha ficam escondidos atrás de uma decisão que depende justamente desses detalhes.

Contrato proposto:
- Entradas: Catálogo resumido, objetivo atual e resolvedor das camadas seguintes.
- Saídas: Conjunto de recursos expandidos com justificativa e versão.
- Estado: Recursos já lidos, dependências e orçamento disponível para expansão.
- Invariante: Metadados orientam descoberta, mas não são tratados como conteúdo completo ou evidência de execução.

Compromissos de projeto:
- Descrições compactas reduzem custo inicial, porém podem aumentar falsos negativos de descoberta.
- Mais camadas preservam seletividade, mas acrescentam latência e risco de referências quebradas.

## T014:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: criar dois recursos com nomes semelhantes e condições de uso diferentes. Verificar se os metadados permitem selecionar o correto antes de ler instruções extensas.

Plano de avaliação proposto:
Avaliação proposta: comparar carregamento integral e progressivo com o mesmo acervo. Medir recursos necessários descobertos, leituras inúteis, tokens totais e tarefas abandonadas por descoberta insuficiente; revisar descrições que causam erros recorrentes.

Comparações:
- T015 (complements): Referências tornam possível adiar a transferência do conteúdo completo.
- T044 (complements): Expansão progressiva é a política que decide quando abrir a próxima camada.

Afirmação rastreável:
A especificação Agent Skills distingue carregamento de metadados, instruções e recursos sob demanda.
Suporte: direct; fontes: V3A-S018
Limite: O formato orienta organização; comportamento efetivo depende de como o executor implementa a descoberta.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T014:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 tratou descoberta por metadados. Aqui a camada nova é projetar descrições discriminativas e medir custo de escolhas erradas.

Projeto e decomposição
Descrições devem distinguir vizinhos, não resumir tudo igualmente. Inclua finalidade, exclusões e exemplo de decisão entre recursos parecidos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

Controle adaptativo
Faça carregamento em duas etapas: contrato mínimo para escolher e corpo necessário para agir. Se o contrato não desambiguar, ampliar metadados antes do conteúdo inteiro.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

Validação contrafactual
Compare catálogo integral e descoberta progressiva usando recursos raros. Medir seleção incorreta, cargas extras e conclusão, não somente tokens iniciais. Unidade de avaliação: catálogo de recursos. Monte um catálogo com dois recursos quase sinônimos, um frequente e outro raro, cuja diferença está numa pré-condição. O teste deve mostrar se o descritor permite escolher o raro sem abrir tudo. Depois remova a pré-condição da descrição e confirme degradação; essa ablação mede a utilidade real dos metadados de descoberta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

USO AVANÇADO — Biblioteca de procedimentos
Cenário: Centenas de rotinas compartilham termos.
Estratégia: Criar índice por intenção e pré-condições; testar pares confundíveis e revisar descrições que causam carga errada.
Papel do modelo pequeno: 3–7B escolhe entre candidatos curtos.
Aceite proposto: Procedimento selecionado deve satisfazer todas as pré-condições.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

USO AVANÇADO — Projeto com muitos módulos
Cenário: Agente precisa localizar documentação apropriada.
Estratégia: Expor mapa de responsabilidades e abrir módulo pelo problema observado; expandir vizinhos apenas se interface cruzar fronteira.
Papel do modelo pequeno: 8–14B resolve dependências locais.
Aceite proposto: Toda expansão deve responder a lacuna identificada.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S018, V4A-S023.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Roteador entre poucos descritores contrastivos.
8–14B: Planejador de carga em duas etapas com identificação de dependências.
15–30B: Integrador de recursos especializados, mantendo teto de expansão.
Requisitos de treino/runtime: Catálogo curado e versionado; exemplos negativos são mais úteis que descrições promocionais.
Não aplicar quando: Metadados não permitem descobrir o recurso correto com custo menor que leitura direta.

## T014:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019.

## T014:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T014 → T045 [complements]
Como combinar: Aplicar descritores contrastivos às ferramentas.
Interface: Intenção, restrições e tool_id.
Condição: Schema completo carregado antes da chamada.
Aceite proposto: Confundir ferramentas semelhantes deve gerar correção antes de executar.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T014 → T044 [feeds]
Como combinar: Abrir detalhe somente após identificar lacuna.
Interface: resource_id, motivo e limite de expansão.
Condição: A carga acrescentar informação necessária.
Aceite proposto: Medir utilidade marginal de cada abertura.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S018, V4A-S023. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Detectar ciclos de referências.
- Não conceder autoridade às instruções encontradas no conteúdo.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar descoberta de recursos raros; economia inicial que aumenta erros de seleção não é melhoria.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T015, T044, T045, T151

## Fontes primárias associadas

### A-S026 — Equipping agents for the real world with Agent Skills

[https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Skills descobertas por metadados, com instruções e recursos carregados sob demanda.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S018 — Agent Skills specification

[https://agentskills.io/specification](https://agentskills.io/specification)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Carregamento progressivo de metadados, instruções e recursos; estrutura e escopo de arquivos de skills.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S023 — Indexing repositories for GitHub Copilot

[https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Índice semântico de código e atualização; funcionalidade documentada do Copilot.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
