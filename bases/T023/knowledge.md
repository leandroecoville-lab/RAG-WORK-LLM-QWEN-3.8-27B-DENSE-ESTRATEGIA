# T023 — Recursive Summarization Tree

**Nome canônico:** Recursive Summarization Tree  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T008  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** árvore recursiva de resumos

## T023:C01 — conceito

Árvore de resumos recursivos em que folhas representam trechos originais e nós internos sintetizam seus descendentes. É uma forma estrutural de sumarização hierárquica, preservada aqui como entrada própria do inventário, sem contabilizá-la como mecanismo independente.

Como funciona:
- Criar folhas com referências exatas às fontes.
- Agrupar folhas e gerar resumos com ligações aos filhos.
- Repetir até um nível de visão geral que caiba no orçamento.

Nota de nomenclatura: Representação estrutural da sumarização hierárquica; não deve ser contada como tecnologia independente.

## T023:C02 — aplicacao

Quando usar:
- Navegação de acervos extensos por nível de detalhe.
- Perguntas amplas que precisam descer a documentos específicos para comprovação.

Quando não usar:
- Não confiar em um nó superior para citar literalmente texto que só existe nas folhas.

Implementação proposta:
- Proposta: armazenar parent_id, child_ids, hash dos filhos e versão do resumidor.
- Limitar profundidade e tamanho de nó de acordo com a distribuição dos documentos.
- Ao atualizar conteúdo, invalidar o caminho até a raiz e reconstruir somente a parte afetada.

Aplicação LAI proposta:
Proposta LAI: manter uma árvore por domínio de software e ligações entre domínios; fontes originais continuam acessíveis para auditoria.

## T023:C03 — riscos_validacao

Armadilhas:
- Profundidade excessiva amplia perdas de detalhe.
- Agrupamento instável pode mudar toda a árvore após pequenas alterações.

Métricas sugeridas:
- Profundidade média de navegação até a evidência.
- Custo de atualização e fidelidade de cada nível.

Testes propostos:
- Pedir uma afirmação do resumo raiz e localizar sua folha de origem.
- Alterar uma folha e verificar que nenhum ancestral antigo é servido como atual.

## T023:C04 — perguntas_proveniencia

Pergunta: A árvore precisa ser binária?
Resposta: Não. A ramificação deve refletir orçamento, estrutura e qualidade de agregação.

Pergunta: Qual diferença para sumarização em cadeia?
Resposta: Na cadeia, cada versão acumula a anterior; na árvore, ramos podem ser sintetizados e atualizados separadamente.

Pergunta: Como manter uma citação precisa no resumo superior?
Resposta: Preserve o caminho até a folha e cite a evidência original quando ela sustentar a afirmação. Citar apenas outro resumo pode esconder erro intermediário.

Pergunta: A raiz pode ser recalculada sem todas as folhas?
Resposta: Pode usar filhos já válidos. Depois de mudanças, é necessário reconstruir os dependentes afetados, mantendo uma revisão consistente da árvore.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T023:C05 — mecanismo_avancado

Uma árvore permite localizar a primeira camada em que uma afirmação desapareceu ou foi alterada. Para isso, cada nó deve conservar seus filhos e a versão do processo que o gerou. A estrutura também distingue cobertura e abstração: visitar um nó ancestral cobre uma síntese de seus descendentes, não prova que o leitor examinou cada folha nem preservou cada detalhe.

Condição de contorno:
Se a síntese não reduz informação suficiente, a profundidade aumenta sem benefício; se reduz demais, perguntas locais exigem voltar às folhas.

Contrato proposto:
- Entradas: Folhas identificadas, regra de agrupamento e condição de término.
- Saídas: Árvore com níveis, resumos e ligações verificáveis aos filhos.
- Estado: Versões dos nós, dependências e estado de reconstrução.
- Invariante: Nenhum nó interno é apresentado como fonte independente dos descendentes que sintetiza.

Compromissos de projeto:
- Árvores balanceadas limitam profundidade, mas podem agrupar unidades pouco relacionadas.
- Agrupamento semântico melhora coerência local e pode produzir tamanhos irregulares e manutenção mais complexa.

## T023:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: inserir uma exceção numa folha e acompanhar sua passagem por cada nível. Quando houver perda, a consulta deve expandir o nó relevante ou registrar insuficiência, sem inventar a exceção no topo.

Plano de avaliação proposto:
Avaliação proposta: comparar cadeia incremental e árvore sob igual orçamento de saída. Medir profundidade, custo de reconstrução, localização de erros e recuperação de detalhes; variar ordem dos documentos e distribuição de tamanho das folhas.

Comparações:
- T008 (specializes): A árvore explicita uma implementação estrutural da sumarização hierárquica.
- T030 (distinct_from): RAPTOR acrescenta procedimentos de embeddings, agrupamento e busca; uma árvore de resumos isolada não o reproduz.

Afirmação rastreável:
O trabalho sobre livros resume pequenas seções e depois resume recursivamente essas sínteses.
Suporte: direct; fontes: V3A-S021
Limite: O treinamento com feedback humano do estudo não está implícito em qualquer árvore construída por prompts.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T023:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 examinou erro recursivo. Aqui a árvore pode ser materializada sob demanda e manter níveis orientados a perguntas distintas.

Projeto e decomposição
Crie nós apenas quando houver utilidade de consulta, evitando resumir todos os níveis antecipadamente. Popularidade da região e custo de atualização orientam materialização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Controle adaptativo
Separe resumo descritivo e índice de perguntas respondíveis pelo nó. O índice melhora roteamento; o resumo sozinho pode ocultar detalhe que seria necessário.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

Validação contrafactual
Compare árvore completa e parcial sob carga com consultas frequentes e raras. Meça tempo inicial, atualização e custo acumulado. Unidade de avaliação: árvore de sínteses. Inclua uma consulta rara sobre folha recém-adicionada e uma consulta frequente sobre ramo já materializado. A árvore parcial deve responder ambas sem apresentar nó pendente como vazio. Medir tempo de primeira consulta e custo acumulado distingue trabalho adiado de trabalho eliminado, evitando atribuir economia a uma construção simplesmente incompleta.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Acervo crescente
Cenário: Novos documentos chegam continuamente.
Estratégia: Adicionar folhas e materializar ancestrais de regiões consultadas; marcar nós pendentes para que o leitor não trate ausência como resumo vazio.
Papel do modelo pequeno: 3–7B extrai índice de perguntas.
Aceite proposto: Consulta rara deve chegar à folha mesmo sem ancestral pronto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

USO AVANÇADO — Relatórios em múltiplos níveis
Cenário: Diretoria e operação exigem detalhes diferentes.
Estratégia: Construir vistas por granularidade usando as mesmas folhas; manter divergências disponíveis em ambos os níveis.
Papel do modelo pequeno: 15–30B redige síntese executiva.
Aceite proposto: Conclusão executiva não pode contrariar evidência operacional.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S021, V4A-S024.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Gerador de descritores de folha e perguntas possíveis.
8–14B: Resumidor de conjuntos pequenos com teste de cobertura.
15–30B: Integrador de vistas com escopos e granularidades diferentes.
Requisitos de treino/runtime: Catálogo de nós materializados, custo de geração e dependências de origem; política de atualização explícita.
Não aplicar quando: Cada consulta exige combinação inédita que atravessa quase toda a árvore.

## T023:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q021, V4A-Q022.

## T023:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T023 → T026 [feeds]
Como combinar: Usar índice de perguntas para navegar até evidências.
Interface: node_id, temas, perguntas cobertas e filhos.
Condição: Índice não for tratado como resposta comprovada.
Aceite proposto: Testar pergunta cuja resposta está em folha pouco popular.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T023 → T007 [complements]
Como combinar: Cachear síntese por conjunto de filhos e política.
Interface: Digest dos filhos, prompt e versão do leitor.
Condição: Dependências completas comporem a chave.
Aceite proposto: Modificar folha e exigir regeneração do ancestral consultado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S021, V4A-S024. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não apresentar nó não materializado como ausência de conteúdo.
- Evitar circularidade entre síntese e sua própria evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar amortização por perfil de consulta; síntese hierárquica não deve substituir evidência de detalhe.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T004, T008, T026, T030

## Fontes primárias associadas

### A-S014 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

[https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Árvore construída por embeddings, agrupamento e resumos recursivos; recuperação em níveis de abstração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S021 — Recursively Summarizing Books with Human Feedback

[https://arxiv.org/abs/2109.10862](https://arxiv.org/abs/2109.10862)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Decomposição recursiva de sumarização e treinamento com feedback humano; avaliação em níveis distintos.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S024 — Project GraphRAG

[https://www.microsoft.com/en-us/research/project/graphrag/](https://www.microsoft.com/en-us/research/project/graphrag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Projeto de pesquisa reúne extração, análise de redes, prompts e resumo.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
