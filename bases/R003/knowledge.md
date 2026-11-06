# R003 — LongMem

**Nome canônico:** LongMem — Augmenting Language Models with Long-Term Memory  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R003  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** Long-Term Memory augmented language model; memória neural de longo prazo

## R003:C01 — conceito

Arquitetura de pesquisa que usa a LLM base congelada como codificador de memória e uma rede lateral adaptável como recuperador e leitor. Seu mecanismo aprende a utilizar representações de contextos passados. É diferente de simplesmente conectar uma API de chat a arquivos ou a um índice textual.

Como funciona:
- Codificar contextos anteriores com o backbone congelado.
- Armazenar representações recuperáveis em um banco de memória.
- Treinar a adaptação para que a rede lateral recupere e utilize essa informação.

## R003:C02 — aplicacao

Quando usar:
- Pesquisa em arquiteturas de memória com acesso ao modelo e ao treinamento.
- Comparação controlada entre memória neural e recuperação textual em tarefas longas.

Quando não usar:
- Como configuração imediata de um servidor arbitrário que só expõe chat/completions.

Implementação proposta:
- Proposta: identificar implementação e checkpoint compatíveis antes de escolher o experimento.
- Reproduzir um caso pequeno com e sem acesso à memória mantendo dados e orçamento comparáveis.
- Medir armazenamento, latência e ganho na tarefa; incluir episódios antigos e dados fora do domínio.

Aplicação LAI proposta:
Proposta LAI: tratar LongMem como linha de pesquisa; para integração inicial da Helena com APIs, avaliar primeiro recuperação textual e estado persistente.

## R003:C03 — riscos_validacao

Armadilhas:
- Trocar o codificador pode invalidar a compatibilidade das representações armazenadas.
- A capacidade do banco de memória não significa atenção exata a todo o histórico em cada passo.

Métricas sugeridas:
- Qualidade na tarefa com memória versus sem memória.
- Custo de codificação, leitura e manutenção por quantidade de contexto armazenado.

Testes propostos:
- Proposta: alterar uma informação histórica relevante e observar se a recuperação responde à alteração.
- Remover a memória e exigir queda específica nas tarefas dependentes dela, evitando atribuir ganhos a outros fatores.

## R003:C04 — perguntas_proveniencia

Pergunta: LongMem é apenas RAG textual?
Resposta: Não. O trabalho inclui arquitetura neural, representações armazenadas e treinamento de adaptação.

Pergunta: Posso assumir compatibilidade com meu Qwen?
Resposta: Não. Ela depende de implementação, arquitetura, checkpoint e treinamento, que precisam ser examinados.

Pergunta: A palavra staleness significa informação factual vencida?
Resposta: No argumento arquitetural, refere-se à compatibilidade de representações quando redes mudam. Validade temporal dos fatos exige controle adicional.

Pergunta: É uma biblioteca intercambiável com RAG textual?
Resposta: Não diretamente. Ela depende de componentes internos e treinamento; a documentação do repositório apresenta uma implementação específica baseada em fairseq.

Escopo das fontes:
A-S013 sustenta o backbone congelado e a rede lateral treinável. Não foi reproduzido o sistema nem extrapolado o resultado do artigo ao ambiente LAI.

## R003:C05 — mecanismo_avancado

O código de LongMem armazena chaves e valores por cabeça de atenção. Para buscar, indexa uma média das chaves de cada chunk e recupera os estados dos chunks selecionados, separando unidade de busca da unidade lida. O backbone congelado mantém estável a representação codificada enquanto a rede lateral aprende a utilizá-la. Essa estabilidade reduz incompatibilidade por deriva do codificador; não torna fatos antigos automaticamente atuais.

Condição de contorno:
A memória continua limitada por capacidade, custo de busca e interface neural; transportar esse banco para outro backbone pode invalidar seu significado mesmo com dimensões iguais.

Contrato proposto:
- Entradas: Contextos anteriores, backbone e tokenizer compatíveis, configuração de banco e rede lateral adaptada.
- Saídas: Estados recuperados e geração condicionada pela arquitetura de leitura de memória.
- Estado: Chaves e valores, índice por cabeça, configuração de chunks e versões dos pesos.
- Invariante: Memórias codificadas sob uma versão não são reutilizadas com outro consumidor apenas por passarem na validação de forma.

Compromissos de projeto:
- Buscar representantes de chunks reduz a unidade de indexação e pode diluir um detalhe importante dentro da média.
- Congelar o codificador facilita reutilização do banco e restringe liberdade de atualizar o backbone sem reconstrução.

## R003:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar o backbone mantendo o banco anterior e comparar com recodificação completa. A experiência deve detectar deriva de compatibilidade, sem atribuir qualquer queda apenas ao tamanho da memória.

Plano de avaliação proposto:
Avaliação proposta: comparar backbone sem memória, arquitetura com banco e banco recodificado após mudança controlada. Medir uso de contexto passado, latência de busca, memória computacional e preservação de detalhes; contabilizar adaptação e construção do índice.

Comparações:
- T052 (specializes): LongMem usa uma interface neural específica para contexto passado, dentro da família ampla de representações latentes.
- R001 (distinct_from): MemGPT controla texto e funções externamente; LongMem modifica a arquitetura de leitura e requer adaptação treinada.

Afirmação rastreável:
A implementação oficial indexa médias das chaves por chunk e retorna chaves e valores dos grupos recuperados.
Suporte: direct; fontes: V3A-S047
Limite: Código consultado sem execução; detalhes são desta implementação de pesquisa e não demonstram prontidão para o servidor da LAI.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R003:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 detalhou memória KV e encoder congelado. Aqui LongMem é analisado como projeto de ciclo de vida de representações, incluindo atualização do consumidor.

Projeto e decomposição
Versione encoder, representação armazenada e módulo que a lê como conjunto. Alterar qualquer parte exige teste de compatibilidade; dimensão igual não preserva geometria nem significado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

Controle adaptativo
Separe renovação factual do texto e renovação representacional. Reindexar com encoder antigo pode atualizar fatos; trocar encoder exige reconstruir memória mesmo quando documentos não mudaram.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

Validação contrafactual
Compare memória atualizada, obsoleta e reconstruída após mudança de modelo. Meça recuperação e resposta separadamente, além do custo de treino e armazenamento; não atribuir falha neural a falta de documento. Unidade de avaliação: memória neural por revisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

USO AVANÇADO — Experimento de memória longa
Cenário: Equipe tem pesos e infraestrutura de treino.
Estratégia: Reproduzir interface em escala controlada, avaliar vantagem sobre RAG textual e ampliar somente se o ganho cobrir manutenção.
Papel do modelo pequeno: 15–30B consumidor experimental.
Aceite proposto: Exigir benefício além do mesmo modelo com evidência textual equivalente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

USO AVANÇADO — Corpus que muda
Cenário: Fatos antigos precisam ser substituídos.
Estratégia: Manter mapa texto-representação e reconstruir regiões afetadas; verificar que estados antigos não continuam acessíveis como atuais.
Papel do modelo pequeno: 8–14B pode servir como baseline textual.
Aceite proposto: Consulta deve acompanhar atualização factual sem misturar revisões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S013, V3A-S045, V3A-S047.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Baseline de leitura textual, sem presumir que LongMem se encaixa diretamente.
8–14B: Consumidor experimental apenas se arquitetura e treino forem adaptados e avaliados.
15–30B: Alvo de pesquisa com acesso a camadas, memória externa e recursos de treinamento.
Requisitos de treino/runtime: Código e arquitetura compatíveis, dados de treino e instrumentação de estados; não é ferramenta plug-and-play para modelo fechado.
Não aplicar quando: Não há acesso ao modelo ou custo de reconstruir representações domina benefício de contexto.

## R003:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C029 — Autores LongMem; Microsoft Research e colaboradores / LongMem
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Artigo e código estudam memória neural recuperável para contexto extenso.
Mecanismo documentado: Representações em memória e módulo adaptado de leitura são componentes treinados.
Correspondência com esta base: Projeto e código específicos.
Transferência proposta para modelo pequeno: Proposta de engenharia: Somente considerar 15–30B se houver acesso a treino e alinhamento de estados; iniciar com RAG textual controlado.
Limite: Não é plug-in universal nem uso bigtech demonstrado; portar requer treino e compatibilidade. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S013, V3A-S047.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q018, V4A-Q023.

## R003:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R003 → T052 [requires]
Como combinar: Declarar formato e versão da memória neural.
Interface: Camada, tensor, máscaras, encoder e consumidor.
Condição: Representações serem semanticamente compatíveis.
Aceite proposto: Trocar encoder sem reconstruir e medir degradação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S045, V3A-S047. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R003 → T009 [alternative]
Como combinar: Usar RAG textual como comparação operacional.
Interface: Mesmas fontes, consulta e orçamento de recursos.
Condição: Baseline receber evidência equivalente.
Aceite proposto: Separar ganho de memória neural de ganho de recuperação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S013, V3A-S045, V3A-S047. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não tratar encoder congelado como garantia de fatos atuais.
- Não transportar métricas do artigo para outro porte sem experimento.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar contexto longo em tarefa definida; resultados do LongMem não demonstram superioridade geral a modelos de fronteira.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T052, T068, T062

## Fontes primárias associadas

### A-S013 — Augmenting Language Models with Long-Term Memory

[https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: LongMem: backbone congelado como codificador e rede lateral treinada para recuperação e leitura.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S045 — LongMem official implementation

[https://github.com/Victorwz/LongMem](https://github.com/Victorwz/LongMem)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Organização de SideNetwork, banco de memória e atenção para fusão; dependências de implementação de pesquisa em fairseq.

Limite: Fonte primária dinâmica consultada; leitura de documentação ou código sem instalação, execução ou reprodução de resultados. Branch e documentação podem evoluir; fixar revisão antes de implementar.

### V3A-S047 — LongMem External_Memory implementation

[https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py](https://github.com/Victorwz/LongMem/blob/main/fairseq/fairseq/modules/dynamic_memory_with_chunk.py)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Banco de chaves e valores por cabeça, indexação da média das chaves em chunks e recuperação dos estados dos chunks selecionados.

Limite: Leitura do código na branch main, sem execução. Detalhes representam esta implementação de pesquisa e não garantem compatibilidade com qualquer modelo ou ambiente.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
