# T073 — Immutable Evidence Store

**Nome canônico:** Immutable Evidence Store  
**Grupo:** Memória, persistência e conhecimento  
**Escopo:** inventario  
**Natureza:** component  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T073  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** repositório imutável de evidências; evidence store

## T073:C01 — conceito

Armazena evidências de modo que versões confirmadas não sejam alteradas silenciosamente. Imutabilidade depende de permissões, retenção e implementação; um arquivo chamado imutável não oferece essa garantia. O registro deve separar conteúdo, identificação e prova de origem.

Como funciona:
- Capturar evidência com metadados de origem e integridade.
- Persistir uma versão protegida conforme a política definida.
- Criar novas versões ou registros de correção sem sobrescrever a evidência anterior.

## T073:C02 — aplicacao

Quando usar:
- Logs de testes, contratos examinados e relatórios de auditoria.
- Necessidade de reconstruir o suporte de uma decisão.

Quando não usar:
- Não reter indiscriminadamente dados sensíveis ou temporários sem finalidade e política de retenção.

Implementação proposta:
- Proposta: usar IDs e hashes com controle de escrita e exclusão.
- Definir retenção e quem pode administrar o armazenamento.
- Verificar periodicamente integridade e possibilidade real de recuperar os objetos.

Aplicação LAI proposta:
Proposta LAI: guardar saídas originais de testes e snapshots usados em auditorias; conclusões derivadas ficam em registros separados e corrigíveis.

## T073:C03 — riscos_validacao

Armadilhas:
- Hash guardado ao lado de arquivo alterável pode ser substituído junto com ele.
- Imutabilidade não prova que o conteúdo foi produzido pela ferramenta alegada.

Métricas sugeridas:
- Integridade dos objetos e referências acessíveis.
- Tentativas de alteração detectadas e cobertura de origem.

Testes propostos:
- Tentar modificar uma versão protegida e exigir rejeição.
- Inserir evidência nova contraditória e preservar ambas com relação explícita de correção.

## T073:C04 — perguntas_proveniencia

Pergunta: Um commit Git é imutabilidade absoluta?
Resposta: Não. Objetos podem ter hashes estáveis, mas referências e retenção dependem do controle do repositório.

Pergunta: WORM comprova a veracidade do arquivo?
Resposta: Não. Protege contra determinadas alterações; qualidade, autoria e contexto da evidência continuam exigindo validação.

Pergunta: Um objeto protegido pode ter informação errada?
Resposta: Sim. Guarde correção separada com vínculo à evidência e impeça que a consulta atual use o registro errado sem seu status.

Pergunta: Guardar o hash no mesmo local resolve autenticidade?
Resposta: Não. Um administrador que controla ambas as partes pode substituir a narrativa de origem. A cadeia de confiança exige controles apropriados ao produtor e ao armazenamento.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T073:C05 — mecanismo_avancado

Imutabilidade deve ser descrita por versão, duração e autoridade capaz de alterar a política. No S3 Object Lock, retenção se aplica a versões de objeto e os modos têm poderes administrativos diferentes. Proteger bytes não impede publicar uma versão nova ou alterar um alias para apontar a outra evidência. Um consumidor precisa fixar a versão protegida e verificar a cadeia de origem, não apenas confiar no nome do bucket.

Condição de contorno:
Armazenamento WORM não prova que o conteúdo inicial era verdadeiro, completo ou produzido pelo agente alegado; integridade e autenticidade são propriedades diferentes.

Contrato proposto:
- Entradas: Evidências, identificadores de versão, política de retenção e informação sobre o produtor.
- Saídas: Versões protegidas e recuperáveis com manifesto de integridade e proveniência associada.
- Estado: Retenção vigente, permissões administrativas, aliases e verificações de disponibilidade.
- Invariante: Uma nova versão ou mudança de ponteiro não substitui silenciosamente a evidência citada numa decisão anterior.

Compromissos de projeto:
- Proteção contra alteração reduz risco de reescrita e limita correções destrutivas.
- Retenção prolongada preserva auditabilidade e aumenta custo; informações derivadas podem ser corrigidas sem apagar o original.

## T073:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: manter uma versão protegida e trocar o alias para outro objeto. A auditoria da decisão anterior deve recuperar a versão original e detectar a mudança de referência.

Plano de avaliação proposto:
Avaliação proposta: avaliar controles com versões de teste e permissões distintas. Medir resistência à sobrescrita, detecção de ponteiros trocados e recuperação por versão; verificar também proveniência, pois um hash correto pode acompanhar uma evidência falsa.

Comparações:
- T061 (complements): Hash verifica identidade de conteúdo; retenção protege a existência e impossibilidade de alteração sob uma política.
- T072 (complements): Histórico versionado permite corrigir interpretação sem reescrever a evidência originalmente registrada.

Afirmação rastreável:
S3 Object Lock oferece retenção e legal holds por versão, com modos governance e compliance de proteção distinta.
Suporte: direct; fontes: A-S034
Limite: A garantia depende da configuração e do modo; não equivale a certificação factual ou a durabilidade de qualquer sistema chamado imutável.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T073:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu retenção WORM e autoridade. Aqui evidências imutáveis recebem verificação periódica de legibilidade e preservação de contexto.

Projeto e decomposição
Preserve artefato, metadados de captura e informação necessária para interpretá-lo. Bytes íntegros de uma tabela sem schema ou unidade podem ser inúteis na auditoria.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

Controle adaptativo
Verifique disponibilidade e legibilidade periodicamente, sem alterar o objeto original. Migrações de formato devem produzir novos derivados com vínculo explícito e comparação de conteúdo.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

Validação contrafactual
Compare armazenamento de arquivo isolado e pacote interpretável. Meça restauração, integridade e reprodução de extrações; retenção imutável não garante que o formato continue utilizável. Unidade de avaliação: pacote de evidência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

USO AVANÇADO — Auditoria de resposta
Cenário: É preciso comprovar o que foi consultado.
Estratégia: Guardar recorte e documento de origem com revisão, data de captura e parser; permitir reconstruir o contexto efetivamente enviado.
Papel do modelo pequeno: 3–7B lê manifesto; 8–14B explica.
Aceite proposto: Citação deve resolver exatamente a evidência usada na decisão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

USO AVANÇADO — Mudança de parser
Cenário: Novo extrator altera tabelas antigas.
Estratégia: Manter original, gerar extração nova e comparar células e relações antes de substituí-la na busca.
Papel do modelo pequeno: 15–30B revisa divergências sem alterar original.
Aceite proposto: Nenhuma conversão pode apagar evidência da interpretação anterior.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S034, V3A-S038, V3A-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Leitor de manifestos e verificações de integridade feitas por código.
8–14B: Comparador de extrações antigas e novas em blocos pequenos.
15–30B: Analista de divergências materiais entre interpretações do mesmo artefato.
Requisitos de treino/runtime: Retenção, hashes, metadados e leitores de formato; autenticidade exige evidência adicional à imutabilidade.
Não aplicar quando: A política impede correção de dados ativos e mistura evidência histórica com verdade vigente.

## T073:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q025, V4A-Q026.

## T073:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T073 → T061 [requires]
Como combinar: Verificar identidade física de cada artefato.
Interface: Digest, codec, tamanho e localização.
Condição: Verificação usar bytes efetivamente recuperados.
Aceite proposto: Corromper objeto e exigir falha antes da leitura pelo modelo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S034, V3A-S038, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T073 → T072 [feeds]
Como combinar: Versionar derivados e interpretações sem substituir origem.
Interface: Original, extração, parser e manifesto.
Condição: Relação de derivação permanecer rastreável.
Aceite proposto: Reproduzir resposta usando a versão histórica correta.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S034, V3A-S038, V3A-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar WORM como prova de que o conteúdo é verdadeiro.
- Não confundir exclusão da janela com eliminação do arquivo de evidência.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar auditabilidade das respostas; modelo de fronteira não recupera contexto que nunca foi preservado.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T059, T061, T072

## Fontes primárias associadas

### A-S034 — Locking objects with Object Lock

[https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Armazenamento WORM e proteção de versões de objetos contra alteração e exclusão.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S038 — Content Identifiers (CIDs)

[https://docs.ipfs.tech/concepts/content-addressing/](https://docs.ipfs.tech/concepts/content-addressing/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: CIDs combinam hash e informações de codec; identidade de conteúdo depende da representação e parâmetros de blocos.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

### V3A-S037 — PROV-DM: The PROV Data Model

[https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Entidades, atividades, agentes, derivação, atribuição e proveniência de registros derivados.

Limite: Fonte primária consultada. Desempenho não foi reproduzido, não foram usadas perguntas ou respostas dos benchmarks, e propostas de integração não representam execução na LAI.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
