# T068 — Memory-Augmented Generation

**Nome canônico:** Memory-Augmented Generation  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** family  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T068  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** geração aumentada por memória; MAG

## T068:C01 — conceito

Família de geração apoiada por memória externa ou componentes de memória específicos. Pode usar texto recuperado por ferramentas ou arquiteturas treinadas para ler representações armazenadas, como LongMem. O nome precisa vir acompanhado da forma de memória e da interface de leitura.

Como funciona:
- Persistir informação em representação adequada.
- Selecionar memória relevante durante a tarefa.
- Condicionar a geração ao conteúdo ou estado recuperado.

## T068:C02 — aplicacao

Quando usar:
- Tarefas que exigem histórico maior que o contexto ativo.
- Reutilização de experiências e conhecimento entre sessões.

Quando não usar:
- Não presumir que qualquer modelo aceita diretamente estados de memória de outra arquitetura.

Implementação proposta:
- Proposta: começar por memória textual com proveniência e ferramentas claras.
- Separar escrita, consolidação e leitura em componentes observáveis.
- Se experimentar memória integrada ao modelo, verificar treinamento, versões e custo adicional.

Aplicação LAI proposta:
Proposta LAI: combinar memória externa auditável e geração pelo modelo configurado; LongMem é referência de pesquisa, não um recurso automaticamente habilitado no Qwen.

## T068:C03 — riscos_validacao

Armadilhas:
- Memória antiga pode ser incompatível com fatos atuais.
- Falhas de recuperação podem parecer falhas de raciocínio e dificultar diagnóstico.

Métricas sugeridas:
- Qualidade com memória correta, irrelevante e ausente.
- Recall, latência e custo total de manutenção da memória.

Testes propostos:
- Comparar o mesmo problema com e sem um episódio relevante.
- Injetar uma memória contraditória com fonte fraca e exigir tratamento de conflito.

## T068:C04 — perguntas_proveniencia

Pergunta: Memory-Augmented Generation é sempre RAG?
Resposta: Há sobreposição, mas arquiteturas com memória integrada podem operar de forma diferente de um pipeline textual de RAG.

Pergunta: Sempre exige treinamento?
Resposta: Não. Memória via ferramentas pode ser engenharia de runtime; arquiteturas especializadas podem exigir adaptação do modelo.

Pergunta: Uma resposta melhor prova que a memória foi usada?
Resposta: Não. Faça ablações com memória removida, trocada ou corrigida e observe o comportamento. Acerto isolado pode vir do conhecimento paramétrico.

Pergunta: Como evitar que o gerador ignore correções recuperadas?
Resposta: Inclua status e versões, teste conflitos entre conhecimento anterior e evidência atual e avalie se a resposta respeita o escopo atualizado.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T068:C05 — mecanismo_avancado

O ponto de integração da memória muda o experimento. Recuperar texto adiciona tokens a um gerador comum; recuperar estados neurais exige componentes capazes de lê-los. Em LongMem, o backbone congelado codifica memória e uma rede lateral adaptativa aprende recuperação e leitura. Avaliar essas opções exige contabilizar treinamento e construção da memória, além da latência de consulta, sem tratar ambas como simples troca de banco vetorial.

Condição de contorno:
Uma memória neural não pode ser conectada a qualquer modelo apenas porque ele aceita texto, e memória textual não corrige um recuperador incapaz de encontrar a evidência.

Contrato proposto:
- Entradas: Memória identificada, consulta ou estado gerador e interface de leitura explicitamente definida.
- Saídas: Resposta condicionada e registro das memórias efetivamente fornecidas ao componente leitor.
- Estado: Versões do escritor, índice, representação, leitor e políticas de atualização.
- Invariante: A avaliação separa erro de recuperação, incompatibilidade de representação e interpretação incorreta pelo gerador.

Compromissos de projeto:
- Texto recuperado facilita auditoria e consome espaço na janela.
- Representações especializadas podem reduzir esse consumo aparente e acrescentam dependências de arquitetura, treinamento e reconstrução do índice.

## T068:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: trocar a representação da memória sem atualizar seu leitor. O sistema deve detectar incompatibilidade ou a avaliação revelar degradação, mesmo que a busca retorne candidatos com pontuação alta.

Plano de avaliação proposto:
Avaliação proposta: comparar ausência de memória, memória textual e interface neural somente em condições compatíveis. Medir sustentação, recuperação, custo de construção, latência e atualização; reporte separadamente treinamento amortizado e custo por consulta.

Comparações:
- T047 (complements): Memória longa define persistência e escopo; geração aumentada especifica como essa informação influencia a saída.
- T052 (complements): Interfaces latentes são uma forma de representação possível, cuja interpretação precisa de consumidor compatível.

Afirmação rastreável:
LongMem separa backbone congelado como codificador de uma rede lateral adaptativa para recuperar e ler memória.
Suporte: direct; fontes: A-S013
Limite: O mecanismo é arquitetural e treinado; o artigo não demonstra compatibilidade direta com APIs arbitrárias de modelos fechados.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T068:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou memória textual e neural. Aqui o uso da memória é testado por intervenção para distinguir acesso de influência real.

Projeto e decomposição
Encontrar e inserir memória não prova que o gerador a utilizou. Compare resposta com memória correta, removida e trocada por versão incompatível, mantendo pergunta igual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

Controle adaptativo
Defina política para conflito entre memória e conhecimento paramétrico. Para tarefas sobre documentos privados, o modelo deve citar a evidência fornecida e sinalizar conflito, não substituir silenciosamente por lembrança.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

Validação contrafactual
Meça fidelidade, sensibilidade à troca e abstenção quando memória fica insuficiente. Separar falha de recuperação, falha de leitura e adesão indevida a fonte errada evita atribuição enganosa de ganho. Unidade de avaliação: resposta condicionada à memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

USO AVANÇADO — Assistente de produto privado
Cenário: Fatos não aparecem no pré-treino.
Estratégia: Recuperar documentação versionada, exigir suporte por afirmação e testar nomes fictícios controlados que impedem acerto por familiaridade.
Papel do modelo pequeno: 8–14B leitor especializado.
Aceite proposto: Resposta deve acompanhar mudança documentada do atributo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

USO AVANÇADO — Memória neural experimental
Cenário: Modelo aberto lê estados externos.
Estratégia: Instrumentar contribuição da memória e comparar com RAG textual sob recursos equivalentes; não avaliar apenas perda de linguagem.
Papel do modelo pequeno: 15–30B consumidor treinável.
Aceite proposto: Memória errada deve ser detectável na avaliação, sem ocultar dependência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S047, V4A-S019.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor extrativo de texto recuperado com citações e campos ausentes.
8–14B: Leitor contextual especializado para integrar poucas memórias conflitantes.
15–30B: Consumidor neural ou integrador complexo quando houver treino e instrumentação.
Requisitos de treino/runtime: Interface de memória definida, versão do consumidor e testes contrafactuais próprios; texto e tensores exigem contratos distintos.
Não aplicar quando: O consumidor ignora memória ou segue conteúdo irrelevante sem capacidade de abster.

## T068:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C029 — Autores LongMem; Microsoft Research e colaboradores / LongMem
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo e código estudam memória neural recuperável para contexto extenso.
Mecanismo documentado: Representações em memória e módulo adaptado de leitura são componentes treinados.
Correspondência com esta base: Geração aumentada por memória neural.
Transferência proposta para modelo pequeno: Proposta de engenharia: Somente considerar 15–30B se houver acesso a treino e alinhamento de estados; iniciar com RAG textual controlado.
Limite: Não é plug-in universal nem uso bigtech demonstrado; portar requer treino e compatibilidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S013, V3A-S047.

V4A-C021 — Google DeepMind / DataGemma RIG/RAG
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Projeto publica variantes para fundamentar geração em Data Commons.
Mecanismo documentado: RIG troca números por dados; RAG usa modelo Gemma para preparar contexto de Gemini 1.5 Pro.
Correspondência com esta base: Geração é aumentada por dados externos.
Transferência proposta para modelo pequeno: Proposta de engenharia: Testar roteador pequeno para consulta estatística, mantendo unidade, período e população.
Limite: RAG citado não é pipeline integral 3–30B; não há implantação de usuário comprovada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S014.

V4A-C022 — Salesforce / SFR-RAG 9B
Evidência: pesquisa; não comprova produção; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: pesquisa sobre LLM.
Uso observado: Pesquisa apresenta modelo de nove bilhões especializado em fidelidade contextual.
Mecanismo documentado: Pós-treino privilegia leitura de evidência, citações e reconhecimento de insuficiência.
Correspondência com esta base: Uso de memória textual externa; não arquitetura neural LongMem.
Transferência proposta para modelo pequeno: Proposta de engenharia: Considerar leitor 8–14B especializado e comparar com modelo geral do mesmo porte.
Limite: Resultados experimentais publicados não garantem produção nem superioridade universal; nenhuma pergunta de benchmark foi incorporada. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S019.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q010, V4A-Q016, V4A-Q018, V4A-Q020, V4A-Q023.

## T068:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T068 → T009 [complements]
Como combinar: Separar busca de evidência e leitura gerativa.
Interface: Consulta, documentos, referências e status de cobertura.
Condição: Memória textual elegível estar disponível.
Aceite proposto: Trocar evidência mantendo consulta e medir dependência correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S047, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T068 → T052 [requires]
Como combinar: Especificar interface quando memória for latente.
Interface: Encoder, estados, máscaras e versão.
Condição: Consumidor treinado para a representação.
Aceite proposto: Testar incompatibilidade após troca de checkpoint.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S047, V4A-S019. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não atribuir ao componente memória acerto que ocorreria sem ele.
- Não tratar texto recuperado como autoridade de execução.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar fidelidade com a mesma evidência; sucesso num domínio privado não demonstra paridade geral com fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T009, T047, T052, T062, R003

## Fontes primárias associadas

### A-S013 — Augmenting Language Models with Long-Term Memory

[https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: LongMem: backbone congelado como codificador e rede lateral treinada para recuperação e leitura.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S023 — Memory overview

[https://docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distinções de escopo, memória semântica, episódica e procedural; gestão do histórico.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S047 — LongMem External_Memory implementation

[https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py](https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco de chaves e valores por cabeça, indexação da média das chaves em chunks e recuperação dos estados dos chunks selecionados.

Limite: Leitura do código na branch main, sem execução. Detalhes representam esta implementação de pesquisa e não garantem compatibilidade com qualquer modelo ou ambiente.

### V4A-S019 — Building Contextually Faithful RAG Applications with SFR-RAG

[https://www.salesforce.com/blog/sfr-rag/](https://www.salesforce.com/blog/sfr-rag/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modelo especializado de 9B para fidelidade contextual, citações e ausência de resposta; pesquisa.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S014 — DataGemma

[https://deepmind.google/models/gemma/datagemma/](https://deepmind.google/models/gemma/datagemma/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: RIG substitui números por dados; variante RAG prepara contexto consumido por Gemini 1.5 Pro.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
