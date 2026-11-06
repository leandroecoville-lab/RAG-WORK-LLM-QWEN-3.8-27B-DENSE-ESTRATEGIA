# T015 — Reference Passing

**Nome canônico:** Reference Passing  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T015  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** passagem por referência; artifact references

## T015:C01 — conceito

Passa identificadores recuperáveis de artefatos entre etapas ou agentes em vez de transmitir todo o conteúdo. A referência só é útil se um resolvedor puder abrir a versão correta com acesso autorizado. Um ponteiro curto não contém implicitamente o conhecimento do arquivo.

Como funciona:
- Persistir um artefato com ID, versão e metadados.
- Transmitir referência mais descrição mínima do conteúdo.
- Resolver a referência e carregar a parte necessária no ponto de uso.

Nota de nomenclatura: Padrão de engenharia aplicado a agentes; não identifica um método científico exclusivo.

## T015:C02 — aplicacao

Quando usar:
- Resultados grandes de ferramentas ou subagentes.
- Missões com muitos arquivos e evidências reutilizadas.

Quando não usar:
- Não serve quando o consumidor não tem acesso ao mesmo armazenamento ou precisa agir sem ler o conteúdo.

Implementação proposta:
- Proposta: adotar IDs opacos e resolver no serviço, sem concatenar caminhos recebidos.
- Incluir hash, tamanho e tipo para validar a leitura.
- Retornar estado explícito para referência inexistente, versão antiga ou conteúdo parcial.

Aplicação LAI proposta:
Proposta LAI: transportar referências de logs, contratos e relatórios entre especialistas; o executor lê a evidência necessária antes de aplicar uma decisão.

## T015:C03 — riscos_validacao

Armadilhas:
- O produtor pode transmitir referência antes de concluir a escrita.
- Um alias mutável pode resolver para conteúdo diferente daquele usado na decisão original.

Métricas sugeridas:
- Referências resolvidas corretamente por versão.
- Bytes ou tokens transferidos por etapa e falhas de acesso.

Testes propostos:
- Alterar o objeto após criar a referência e exigir detecção de versão divergente.
- Tentar uma referência de namespace diferente e rejeitar acesso indevido.

## T015:C04 — perguntas_proveniencia

Pergunta: O modelo conhece o arquivo ao receber seu caminho?
Resposta: Não. Ele precisa de conteúdo recuperado ou de uma ferramenta que o leia.

Pergunta: Devo usar apenas o nome do arquivo?
Resposta: Prefira ID e versão; nomes podem colidir, mudar ou apontar para conteúdo diferente.

Pergunta: Uma URL prova que o conteúdo foi lido?
Resposta: Não. Ela prova apenas que uma localização foi fornecida. O relato deve distinguir referência recebida, leitura bem-sucedida e conteúdo efetivamente utilizado.

Pergunta: Como evitar referências que perdem validade?
Resposta: Defina retenção e versões recuperáveis compatíveis com a tarefa; registre falhas e preserve uma representação autorizada quando o contrato exigir continuidade.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T015:C05 — mecanismo_avancado

Uma referência precisa distinguir identidade lógica de identidade de versão. Um caminho que aponta para a versão mais recente pode resolver conteúdo diferente entre planejamento e execução. Para continuidade verificável, transfira também revisão, tipo e descrição do que o destinatário deve ler. O custo evitado no envio pode reaparecer como latência de resolução ou indisponibilidade do recurso.

Condição de contorno:
Passar apenas um identificador é insuficiente quando o próximo agente não possui resolvedor, acesso ou capacidade para interpretar o artefato referenciado.

Contrato proposto:
- Entradas: Referência, versão esperada, finalidade e escopo da leitura.
- Saídas: Conteúdo autorizado ou erro classificado de ausência, versão ou acesso.
- Estado: Mapeamento de identificadores, revisões e leituras realizadas.
- Invariante: O destinatário não afirma conhecer o conteúdo antes de resolvê-lo ou receber evidência explícita suficiente.

Compromissos de projeto:
- Referências diminuem duplicação de conteúdo, mas introduzem dependência de disponibilidade.
- Versões fixadas favorecem reprodução, enquanto referências móveis facilitam atualização e exigem revalidação.

## T015:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: alterar um arquivo entre a emissão e a resolução da referência. Um consumidor que exigiu a versão antiga deve receber essa versão ou erro claro, nunca substituição silenciosa.

Plano de avaliação proposto:
Avaliação proposta: comparar conteúdo embutido e referência resolvida sob diferentes tamanhos e taxas de reutilização. Medir tokens, tempo total, referências quebradas e divergências de versão; escolher por custo completo da troca.

Comparações:
- T066 (complements): O resolvedor aplica o contrato de leitura e versão usado na passagem.
- T061 (complements): Um hash de conteúdo pode identificar uma versão, mantendo localização e acesso como problemas separados.

Afirmação rastreável:
MCP identifica recursos por URI e define operações distintas de listagem e leitura.
Suporte: direct; fontes: V3A-S019
Limite: A especificação não torna toda URI imutável nem fornece automaticamente o versionamento editorial proposto.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T015:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 separou referência e leitura. Aqui referências transportam prova de disponibilidade e uma política de resolução por tarefa.

Projeto e decomposição
Uma referência entregue a outro agente deve declarar conteúdo disponível, recorte permitido e custo de abertura. O receptor pode planejar sem fingir que já leu.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

Controle adaptativo
Use leases ou verificação equivalente para artefatos temporários. Se a validade expirar, renovar acesso ou materializar cópia identificada antes da etapa dependente.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

Validação contrafactual
Compare transporte integral e referências em tarefas com reuso desigual. Medir leituras evitadas, referências quebradas e conclusões sem abertura. Unidade de avaliação: cadeia de referências. Inclua referência válida no momento da delegação e indisponível na retomada. O receptor deve produzir diagnóstico de indisponibilidade, não reconstruir conteúdo a partir do título ou de um resumo antigo. Compare materialização antecipada e leitura tardia segundo prazo e probabilidade de uso; referências economizam transporte, mas podem aumentar risco operacional quando a origem é temporária.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

USO AVANÇADO — Delegação de análise
Cenário: Subagente produz relatório extenso.
Estratégia: Retornar índice de afirmações e referências a evidências; líder abre somente suportes que usará no texto final.
Papel do modelo pequeno: 3–7B produz índice; 15–30B integra.
Aceite proposto: Nenhuma citação final pode apontar conteúdo não verificado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

USO AVANÇADO — Resultados grandes de ferramenta
Cenário: Tabela excede a janela.
Estratégia: Persistir resultado, devolver schema e referência; consultas posteriores pedem colunas ou linhas necessárias.
Papel do modelo pequeno: 8–14B escolhe projeções pequenas.
Aceite proposto: Resposta deve preservar filtro e versão da tabela.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3A-S019, V4A-S025.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Consumidor de identificadores e schemas, com resolução determinística.
8–14B: Seletor de recortes e projeções por pergunta.
15–30B: Integrador que compara fontes grandes por aberturas direcionadas.
Requisitos de treino/runtime: Resolver com identidade, versão e status de disponibilidade; validade de acesso deve ser verificável.
Não aplicar quando: A origem não ficará acessível até o fim da tarefa e não há cópia durável.

## T015:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C020 — Google / NotebookLM com fontes multimodais
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: aplicação com LLM.
Uso observado: Produto oferece análise de documentos, áudio e vídeo com citações.
Mecanismo documentado: Conteúdo de fontes e transcrições fundamenta respostas referenciadas.
Correspondência com esta base: Citações retornam às fontes; formato de Reference Passing não é especificado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Conservar timestamp e locutor ao fornecer excertos para leitor compacto.
Limite: Não importar limites comerciais históricos como atuais; não é prova de parser infalível. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S025.

V4A-C016 — Google Cloud / Gemini context caching
Evidência: produto/recurso disponível; somente família relacionada. Organização: Big Tech — núcleo definido nesta curadoria.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Manual disponibiliza caches implícitos e explícitos de contexto.
Mecanismo documentado: Reuso de prefixos, referências a objetos de cache e contabilidade de tokens.
Correspondência com esta base: Nome de recurso referencia conteúdo cacheado, não referência semântica genérica.
Transferência proposta para modelo pequeno: Proposta de engenharia: Agrupar chamadas pequenas com prefixo estável quando runtime suportar e medir custo líquido.
Limite: Modelos e condições de serviço variam; caching não aumenta janela nem reduz obrigação de evidência. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: V4A-S015.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002, V4A-Q019, V4A-Q022.

## T015:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T015 → T066 [requires]
Como combinar: Resolver identidade antes de interpretar o conteúdo.
Interface: URI lógica, revisão, hash e seletor.
Condição: Resolver não substituir versão silenciosamente.
Aceite proposto: Testar expiração e versão inexistente.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V4A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T015 → T061 [complements]
Como combinar: Vincular artefato recuperado ao digest esperado.
Interface: Bytes, codec e digest.
Condição: Hash representar o artefato efetivamente lido.
Aceite proposto: Alterar objeto e impedir aceitação pelo identificador antigo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3A-S019, V4A-S025. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não resumir referência como se fosse evidência lida.
- Conservar limite de acesso quando a referência atravessar agentes.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar custo de transporte e qualidade das citações, não presumir que referência curta melhora entendimento.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T053, T061, T066

## Fontes primárias associadas

### A-S006 — Effective context engineering for AI agents

[https://www.anthropic.com/research/effective-context-engineering-for-ai-agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Gestão seletiva de contexto, recuperação sob demanda e técnicas de continuidade de agentes.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### A-S010 — MemFS

[https://docs.letta.com/concepts/memfs](https://docs.letta.com/concepts/memfs)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Memória em repositório Git, projeção em arquivos e carregamento por índices.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V3A-S019 — Model Context Protocol: Resources, specification 2025-11-25

[https://modelcontextprotocol.io/specification/2025-11-25/server/resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Recursos identificados por URI; listagem, leitura e capacidades opcionais de notificação.

Limite: Fonte primária consultada. Sem reprodução de resultados, instalação ou verificação de servidor; detalhes operacionais propostos são inferências editoriais.

### V4A-S025 — NotebookLM adds audio and YouTube support, plus easier sharing of Audio Overviews

[https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/](https://blog.google/innovation-and-ai/products/notebooklm-audio-video-sources/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Produto fundamentado em fontes com citações e transcrições; recursos disponíveis.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

### V4A-S015 — Context caching overview

[https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Caching implícito e explícito, metadados de uso e duração; recurso disponível.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
