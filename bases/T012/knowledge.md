# T012 — Recursive Chunking

**Nome canônico:** Recursive Chunking  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** technique  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T012  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** segmentação recursiva

## T012:C01 — conceito

Aplica uma sequência de separadores, começando por unidades amplas e refinando apenas blocos grandes demais. Uma estratégia comum tenta parágrafos, linhas, espaços e, por último, caracteres. Recursivo descreve a divisão, não raciocínio recursivo do agente.

Como funciona:
- Tentar o separador de maior unidade disponível.
- Dividir novamente somente os blocos que ultrapassam o limite.
- Combinar fragmentos compatíveis e registrar sobreposições e offsets.

## T012:C02 — aplicacao

Quando usar:
- Textos gerais com parágrafos e linhas razoavelmente estruturados.
- Baseline de ingestão que exige simplicidade e previsibilidade.

Quando não usar:
- Não esperar reconhecimento completo de tabelas, AST de código ou relações entre documentos.

Implementação proposta:
- Proposta: adaptar separadores ao idioma e tipo de arquivo.
- Medir tamanho com tokenizer quando o limite relevante é em tokens.
- Preservar títulos como metadados e versionar a lista de separadores.

Aplicação LAI proposta:
Proposta LAI: adotar como divisão textual padrão inicial; encaminhar schemas e arquivos de código a parsers conscientes da estrutura.

## T012:C03 — riscos_validacao

Armadilhas:
- Medir caracteres enquanto o embedder limita tokens pode causar truncamento.
- Separadores mal escolhidos geram muitos fragmentos minúsculos.

Métricas sugeridas:
- Quantidade de trechos vazios ou acima do limite.
- Recall de evidência e tamanho médio efetivo.

Testes propostos:
- Usar textos com poucas quebras e garantir término e cobertura completa.
- Testar pontuação portuguesa e listas com quebras de linha para detectar fragmentação.

## T012:C04 — perguntas_proveniencia

Pergunta: Recursivo é igual a hierárquico?
Resposta: Não necessariamente. Um splitter recursivo pode produzir somente uma lista plana de trechos.

Pergunta: A ordem dos separadores importa?
Resposta: Sim. Ela define quais unidades o algoritmo tenta preservar antes de usar cortes mais finos.

Pergunta: A sobreposição configurada sempre aparece exatamente?
Resposta: Não se deve presumir. A preservação de unidades e a estratégia de junção podem alterar a sobreposição efetiva; inspecione offsets resultantes.

Pergunta: Quando usar parser em vez de separadores?
Resposta: Quando a semântica estrutural importa, como funções e tabelas. Um parser fornece relações que uma lista de caracteres não reconhece.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T012:C05 — mecanismo_avancado

A ordem dos separadores funciona como uma prioridade estrutural. Um bloco só desce para uma regra mais fina quando permanece grande demais. A configuração padrão de um divisor por caracteres não impõe automaticamente limite em tokens; trocar apenas o nome do parâmetro não muda a função de comprimento. Para línguas sem espaços, a lista de separadores deve considerar sua pontuação e convenções.

Condição de contorno:
Arquivos minificados, tabelas densas e unidades sem separadores reconhecidos podem chegar ao fallback mais fino e perder fronteiras úteis.

Contrato proposto:
- Entradas: Texto, separadores ordenados, função de comprimento e sobreposição alvo.
- Saídas: Segmentos com offsets e unidade de tamanho declarada.
- Estado: Versão da configuração, normalização aplicada e metadados de documento.
- Invariante: Cada fallback reduz uma unidade excessiva ou encerra com erro explícito, sem recursão improdutiva.

Compromissos de projeto:
- Regras simples tornam a ingestão reproduzível, mas não identificam relações semânticas implícitas.
- Mais separadores específicos preservam estrutura e também exigem testes por tipo de documento.

## T012:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: processar texto sem espaços e um bloco de código muito longo. Confirmar término, respeito ao limite medido e registro de cortes que atravessam uma unidade sintática.

Plano de avaliação proposto:
Avaliação proposta: comparar separadores genéricos e específicos por linguagem mantendo função de comprimento e índice iguais. Medir unidades quebradas, quantidade de chunks, custo e recuperação de evidências; escolher configuração por corpus, não por preferência nominal.

Comparações:
- T010 (complements): O limite de tamanho continua útil como restrição, embora os cortes tentem preservar unidades maiores.
- T033 (distinct_from): Recursão por delimitadores não equivale a interpretar uma árvore estrutural do documento.

Afirmação rastreável:
A documentação do RecursiveCharacterTextSplitter separa lista de separadores, função de comprimento e sobreposição.
Suporte: direct; fontes: A-S004
Limite: A configuração consultada é de uma biblioteca específica; outros divisores podem ter contratos diferentes.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T012:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descreveu separadores e contagem. A novidade é preservar âncoras estáveis e limitar propagação de mudanças no particionamento recursivo.

Projeto e decomposição
Associe fragmentos a caminhos estruturais antes de aplicar separadores. Tamanho ainda governa fallback, mas o caminho permite localizar continuidade após inserções.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

Controle adaptativo
Registre qual nível de separador produziu cada fronteira. Muitos cortes no último nível indicam conteúdo incompatível ou parser ausente, não apenas chunk pequeno.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

Validação contrafactual
Avalie reindexação após inserções no início e no meio do arquivo. Meça referências preservadas e necessidade real de recomputar embeddings. Unidade de avaliação: arquivo versionado. Teste inserção de uma seção antes de todas as demais e alteração interna num bloco protegido. Referências por caminho e revisão devem continuar localizando conteúdo sem depender do número ordinal do chunk. Se o bloco ficar grande demais, a saída precisa indicar oversize e oferecer estratégia de leitura; cortar silenciosamente não é fallback aceitável.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

USO AVANÇADO — Manuais em Markdown
Cenário: Seções mudam sem reorganização total.
Estratégia: Dividir por cabeçalhos, depois parágrafos e sentenças; conservar caminho da seção e número da revisão.
Papel do modelo pequeno: 3–7B extrai campos dentro do fragmento.
Aceite proposto: Citações devem resolver seção correta após edição.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

USO AVANÇADO — Arquivos mistos
Cenário: Texto contém comandos longos e exemplos.
Estratégia: Reconhecer blocos protegidos e encaminhar oversize para leitura específica em vez de quebrar comando arbitrariamente.
Papel do modelo pequeno: 8–14B explica bloco protegido.
Aceite proposto: Nenhum exemplo executável pode ser alterado pelo splitter.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S004, V4A-S013.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de unidades finais pequenas com contexto de cabeçalho.
8–14B: Comparador de fragmentos que compartilham uma seção.
15–30B: Síntese entre seções, pedindo bloco completo quando necessário.
Requisitos de treino/runtime: Separadores versionados, metadados de caminho e tratamento explícito de oversize.
Não aplicar quando: A estrutura depende de layout visual que os separadores textuais perderam.

## T012:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q009.

## T012:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T012 → T015 [feeds]
Como combinar: Emitir referência independente do índice ordinal.
Interface: Caminho, revisão, offsets e digest.
Condição: Âncora representar conteúdo identificável.
Aceite proposto: Inserir parágrafo e verificar referências preservadas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S004, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T012 → T033 [requires]
Como combinar: Detectar unidades protegidas antes do fallback.
Interface: Tipo de bloco e limites permitidos.
Condição: Parser reconhecer estrutura relevante.
Aceite proposto: Testar bloco longo sem corte em ponto inválido.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S004, V4A-S013. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Evitar IDs baseados somente na posição na lista.
- Não ocultar trecho excessivo descartando o restante.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar localização e leitura após edições; a profundidade da recursão não mede qualidade semântica.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T010, T011, T033

## Fontes primárias associadas

### A-S004 — Splitting recursively

[https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Separadores ordenados, limite de tamanho e sobreposição na divisão recursiva de texto.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S013 — Is Semantic Chunking Worth the Computational Cost?

[https://arxiv.org/abs/2410.13070](https://arxiv.org/abs/2410.13070)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação de segmentação semântica e tamanho fixo em recuperação de documentos, evidência e respostas; ganhos não universais.

Limite: Consulta de fonte primária; não houve reprodução experimental. Resultados e APIs são limitados ao trabalho ou documentação citados, consultados em 2026-11-05.

### V4A-S013 — How content chunking works for knowledge bases

[https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/kb-chunking.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Chunking fixo, semântico e hierarquia filho-pai como recursos do Bedrock.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
