# T061 — Content-Addressable Storage

**Nome canônico:** Content-Addressable Storage  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** architecture  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T061  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** armazenamento endereçado por conteúdo; CAS

## T061:C01 — conceito

Endereça objetos pelo hash de seu conteúdo em vez de depender apenas de nome ou localização. Conteúdo idêntico produz o mesmo identificador sob o mesmo esquema; alteração produz outro. O hash verifica identidade dos bytes, mas não prova a verdade nem a autoria do que eles dizem.

Como funciona:
- Definir serialização ou bytes canônicos.
- Calcular o identificador e persistir o objeto.
- Verificar o hash ao recuperar e ligar referências à versão imutável.

## T061:C02 — aplicacao

Quando usar:
- Evidências e artefatos reutilizados em muitas missões.
- Deduplicação e rastreio de alterações de documentos.

Quando não usar:
- Não usar o hash como autorização de acesso nem como certificado de que um teste foi executado.

Implementação proposta:
- Proposta: usar algoritmo declarado e manifestos com tamanho e tipo.
- Separar objetos imutáveis de aliases como versão atual.
- Controlar coleta de lixo por referências para não apagar conteúdo ainda necessário.

Aplicação LAI proposta:
Proposta LAI: identificar logs e contratos por conteúdo para ligar cada achado à evidência examinada; preservar controles de acesso separados.

## T061:C03 — riscos_validacao

Armadilhas:
- Mesmo conteúdo serializado de forma diferente pode produzir hashes distintos.
- Deduplicação pode criar compartilhamento indevido se permissões não forem verificadas.

Métricas sugeridas:
- Falhas de integridade e taxa de deduplicação.
- Referências quebradas após retenção ou limpeza.

Testes propostos:
- Modificar um byte e exigir falha de verificação contra o identificador antigo.
- Apagar objeto ainda referenciado e detectar inconsistência do manifesto.

## T061:C04 — perguntas_proveniencia

Pergunta: Um hash comprova que a afirmação do arquivo é verdadeira?
Resposta: Não. Comprova identidade ou alteração dos bytes em relação ao hash esperado.

Pergunta: É preciso usar Git?
Resposta: Não. Git exemplifica esse modelo, mas ele pode ser implementado em bancos ou armazenamento de objetos.

Pergunta: Mesmo CID garante que o objeto estará disponível?
Resposta: Não. O identificador permite conferir o conteúdo encontrado, mas alguém ainda precisa armazenar e servir os blocos necessários.

Pergunta: Posso usar latest num store por conteúdo?
Resposta: Pode manter um alias mutável separado. Para reproduzir uma decisão, registre também o identificador imutável para o qual o alias foi resolvido.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T061:C05 — mecanismo_avancado

O endereço por conteúdo depende da representação efetivamente hasheada. Em IPFS, um CID inclui informações de codec e hash, e um arquivo pode ser dividido em blocos ligados por um DAG. Portanto, o CID raiz não é simplesmente o SHA-256 dos bytes do arquivo completo. Configurações de chunking e codificação podem mudar o identificador sem mudar o conteúdo lógico interpretado pelo usuário.

Condição de contorno:
Identidade por bytes não resolve equivalência semântica, disponibilidade, autenticidade do produtor ou permissão de acesso ao objeto compartilhado.

Contrato proposto:
- Entradas: Bytes ou estrutura serializada, algoritmo de hash, codec e parâmetros de segmentação.
- Saídas: Identificador verificável, manifesto de representação e objeto recuperável conforme a política de retenção.
- Estado: Objetos, referências vivas, aliases mutáveis e configuração de produção dos identificadores.
- Invariante: A verificação usa exatamente a representação e o esquema declarados, sem confundir um checksum simples com outro tipo de identificador.

Compromissos de projeto:
- Deduplicação economiza armazenamento de objetos iguais e exige rastrear referências antes de coletá-los.
- Representações estruturadas permitem reutilizar partes e tornam a reprodução do identificador dependente de mais parâmetros.

## T061:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: ingerir o mesmo arquivo com dois esquemas de blocos e comparar os identificadores. O sistema deve reconhecer a diferença de representação e verificar cada objeto segundo seu contrato, sem acusar corrupção apenas por IDs distintos.

Plano de avaliação proposto:
Avaliação proposta: comparar endereçamento por nome e conteúdo em revisões, deduplicação e recuperação. Medir integridade detectada, reprodução dos IDs, custo de manifestos e objetos órfãos; testar indisponibilidade separadamente de alteração de bytes.

Comparações:
- T007 (complements): Canonicalização define quais bytes representam uma requisição; CAS endereça o objeto resultante pelo conteúdo.
- T073 (distinct_from): Endereço verificável detecta alteração; retenção imutável controla possibilidade de sobrescrever ou excluir versões.

Afirmação rastreável:
A documentação IPFS explica que CIDs incluem hash e codec e não equivalem necessariamente ao hash do arquivo inteiro.
Suporte: direct; fontes: V3A-S038
Limite: A descrição é específica do esquema IPFS; outros stores podem usar um hash direto sobre bytes canônicos.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T061:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu CID e hash bruto. Aqui CAS sustenta deduplicação verificável, coleta de lixo e manifestos de proveniência.

Projeto e decomposição
Armazene manifesto que liga bytes, interpretação e origem. Conteúdos iguais podem ter proveniências distintas; deduplicar armazenamento não deve fundir automaticamente autoridade ou identidade documental.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

Controle adaptativo
Faça coleta de lixo por referências alcançáveis a partir de raízes declaradas. Um artefato não acessado recentemente pode continuar necessário para auditoria ou reconstrução de memória.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

Validação contrafactual
Compare armazenamento por caminho e CAS com manifestos. Meça deduplicação, referências quebradas e recuperação após limpeza; hash correto não comprova autoria nem verdade. Unidade de avaliação: artefato endereçado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

USO AVANÇADO — Evidências compartilhadas
Cenário: Vários agentes usam o mesmo documento.
Estratégia: Guardar bytes uma vez, criar referências de proveniência separadas e transportar digest para verificar leituras.
Papel do modelo pequeno: 3–7B consome trechos; código verifica hash.
Aceite proposto: Cada citação deve preservar origem mesmo quando bytes forem iguais.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

USO AVANÇADO — Índices reconstruíveis
Cenário: Embeddings e resumos derivam de arquivos.
Estratégia: Registrar DAG de dependências e manter raízes da versão ativa; remover apenas artefatos sem dependentes protegidos.
Papel do modelo pequeno: 8–14B explica linhagem.
Aceite proposto: Reconstrução da versão ativa deve continuar possível após limpeza.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S038, A-S028.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de manifestos e referências, sem responsabilidade pelo cálculo criptográfico.
8–14B: Analista de dependências de artefatos e falhas de resolução.
15–30B: Integrador de evidências de múltiplas origens com identidade física compartilhada.
Requisitos de treino/runtime: Hash/codec definidos, armazenamento disponível e raízes de retenção; autenticação da origem é camada separada.
Não aplicar quando: Conteúdo precisa ser mutável sob o mesmo identificador ou política de retenção não distingue raízes protegidas.

## T061:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q006, V4A-Q026.

## T061:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T061 → T073 [complements]
Como combinar: Vincular evidência preservada a bytes verificáveis.
Interface: Digest, origem, retenção e manifestação de autoria.
Condição: Imutabilidade e autenticidade serem avaliadas separadamente.
Aceite proposto: Substituir conteúdo sob caminho e detectar divergência.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S038, A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T061 → T072 [feeds]
Como combinar: Versionar manifesto de artefatos derivados.
Interface: Raiz, dependências e versões de produtores.
Condição: Manifesto declarar conjunto completo da revisão.
Aceite proposto: Eliminar objeto referenciado e exigir falha explícita de integridade.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S038, A-S028. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar consistent hashing de endereçamento por conteúdo.
- Não deduplicar direitos ou proveniência apenas porque bytes coincidem.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar verificabilidade e recuperação; CAS melhora identidade dos artefatos, não entendimento semântico do leitor.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T007, T015, T073

## Fontes primárias associadas

### A-S028 — Git Internals — Git Objects

[https://git-scm.com/book/en/v2/Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Objetos endereçados por conteúdo e composição de árvores e commits.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S038 — Content Identifiers (CIDs)

[https://docs.ipfs.tech/concepts/content-addressing/](https://docs.ipfs.tech/concepts/content-addressing/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: CIDs combinam hash e informações de codec; identidade de conteúdo depende da representação e parâmetros de blocos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
