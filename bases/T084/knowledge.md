# T084 — Session-Based Caching

**Nome canônico:** Session-Based Caching  
**Grupo:** Inferência, atenção, GPU e cache  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Padrão editorial apoiado em conceitos relacionados  
**ID canônico:** T084  
**Data da curadoria:** 2026-11-05

## T084:C01 — conceito

Padrão de aplicação que associa estados reutilizáveis a uma sessão de conversa. Pode reter KV, resultados ou ambos, mas cada tipo possui validade diferente. Aqui o foco é a continuidade computacional do diálogo; a sessão deve continuar recuperável mesmo que o cache desapareça.

Como funciona:
- Identificar sessão, revisão do histórico e versão do modelo.
- Verificar se a nova entrada realmente continua o prefixo anterior.
- Reusar estados válidos ou reconstruí-los a partir do histórico persistido.

## T084:C02 — aplicacao

Quando usar:
- Conversas com muitos turnos que acrescentam conteúdo ao final.
- Sessões frequentes cujo custo de prefill domina o tempo de resposta.

Quando não usar:
- Usar a sessão como única chave mesmo quando o histórico foi editado ou compactado.

Implementação proposta:
- Separar armazenamento durável da conversa e armazenamento descartável dos estados.
- Adicionar TTL, limite de memória e política de invalidação por revisão.
- Serializar atualizações concorrentes ou usar revisão otimista para impedir bifurcações acidentais.

Aplicação LAI proposta:
Proposta LAI: manter a conversa e o estado de missão fora do cache e usar a sessão apenas como domínio de continuidade e isolamento.

## T084:C03 — riscos_validacao

Armadilhas:
- Afinidade rígida a um worker pode desequilibrar carga.
- Reuso após resumo da conversa é inválido quando os tokens de entrada mudaram.

Métricas sugeridas:
- Acerto por sessão e custo de reconstrução depois de expiração.
- Consumo de memória por sessão ociosa e tempo até primeiro token.

Testes propostos:
- Expirar o cache entre turnos e exigir continuação correta a partir dos dados persistidos.
- Enviar turnos concorrentes e confirmar que revisões não se misturam.

## T084:C04 — perguntas_proveniencia

Pergunta: Fechar o servidor deve apagar a conversa?
Resposta: Não. A conversa deve sobreviver na persistência; somente a aceleração computacional pode ser perdida.

Pergunta: Uma sessão autoriza reuso após edição?
Resposta: Não. A revisão do histórico e a identidade dos tokens também precisam coincidir.

Pergunta: Pode salvar apenas o cache como memória?
Resposta: Isso dificulta auditoria e migração; preserve também o histórico necessário para reconstruir estados compatíveis.

Pergunta: O cancelamento apaga todos os tokens gerados?
Resposta: O contrato precisa distinguir tokens já confirmados dos provisórios e definir precisamente qual revisão permanece válida.

Escopo das fontes:
A fonte cobre objetos de cache e reuso; gestão de sessão, revisões e TTL são arquitetura editorial proposta.

## T084:C05 — mecanismo_avancado

O estado de sessão precisa distinguir histórico confirmado de geração em andamento. Uma edição de mensagem ou ramificação muda a ancestralidade, enquanto uma resposta atrasada ainda pode tentar gravar no cache antigo. Um contrato editorial robusto associa sessão, revisão e identidade do modelo, confirmando atualizações apenas quando a revisão esperada permanece válida. Mensagens persistidas são a fonte de reconstrução; o cache é descartável.

Condição de contorno:
Persistência de conversa não implica persistência de tensores; reinícios e mudanças de configuração podem exigir reconstrução integral.

Contrato proposto:
- Entradas: Identificador da sessão, revisão esperada, histórico tokenizado e extensão solicitada.
- Saídas: Nova revisão confirmada ou conflito explícito, com continuação correspondente.
- Estado: Histórico durável separado dos estados de atenção e operações pendentes.
- Invariante: Uma operação atrasada nunca sobrescreve silenciosamente uma ramificação mais recente.

Compromissos de projeto:
- Manter várias ramificações aumenta memória, mas evita reconstruções frequentes.
- Serializar todas as operações simplifica consistência e pode reduzir concorrência útil.

## T084:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: iniciar duas continuações, editar a mensagem anterior e concluir a primeira por último. Esperar conflito de revisão ou cache isolado, sem associar sua resposta à nova conversa.

Plano de avaliação proposto:
Plano proposto: comparar execução sem cache e cache por revisão em sessões lineares e ramificadas. Medir reconstruções, bytes residentes, latência e conflitos; aceitar apenas respostas equivalentes para o mesmo histórico confirmado.

Comparações:
- T081 (complements): A consistência de sessão controla quando o estado incremental pode ser reutilizado.

Afirmação rastreável:
O cache armazena estados derivados de tokens processados, permitindo continuação sem refazer suas projeções.
Suporte: related; fontes: V3B-S005
Limite: A documentação sustenta o mecanismo de cache; revisão transacional de sessão é proposta de integração, não API padronizada.

Nota de pesquisa:
Síntese técnica com fontes; contratos, testes e critérios de avaliação são propostas editoriais, não resultados executados.

## T084:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 vinculou cache à revisão do histórico. A nova proposta explicita leases, tentativas concorrentes e políticas de mobilidade, evitando que afinidade de sessão se torne dependência permanente de um worker ou uma fonte de resultados atrasados.

Lease de continuação
Associe a execução em andamento a uma revisão esperada e a um lease de duração limitada. A conclusão só confirma o novo estado se ambos continuarem válidos. Um pedido lento que retorna depois de edição do usuário deve ser registrado como tentativa obsoleta, sem sobrescrever a ramificação atual da conversa.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

Afinidade com saída de emergência
Afinidade melhora a chance de encontrar KV, mas precisa poder ceder a indisponibilidade ou fila excessiva. Guarde o histórico confirmado fora do worker e defina quando vale reconstruir em outro destino. Uma sessão pode manter identidade estável enquanto seu estado computacional muda de localização.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

Contabilidade de sessão ociosa
Faça retenção depender do intervalo de revisita, do tamanho do cache e da prioridade da sessão. Sessões curtas e frequentes podem ser baratas de manter; uma conversa longa abandonada pode expulsar várias sessões úteis. Registre retomadas e reconstruções para ajustar a política, preservando a possibilidade de voltar sem o cache.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

USO AVANÇADO — Assistente interrompido pelo usuário
Cenário: O usuário cancela uma resposta e envia correção imediatamente.
Estratégia: Cancele a tentativa antiga, confirme somente tokens que a política de conversa considera aceitos e abra nova revisão. Não reutilize automaticamente o trecho gerado e não entregue uma conclusão tardia como se respondesse à correção.
Papel do modelo pequeno: Um modelo 3–14B pode manter interação rápida com estado lógico pequeno e explícito.
Aceite proposto: Testar corridas entre cancelamento, fim da geração e nova mensagem sem mistura de revisões.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

USO AVANÇADO — Sessão móvel entre máquinas
Cenário: Um serviço precisa drenar workers para atualização.
Estratégia: Pare novas admissões no worker antigo, preserve estados confirmados e escolha transferência suportada ou replay dos tokens. Permita concluir requisições em voo ou cancelar com razão explícita; nunca tratar cache ausente como perda da sessão.
Papel do modelo pequeno: Um modelo 15–30B pode exigir reconstrução planejada para manter a cauda aceitável.
Aceite proposto: Medir sucesso de retomada, duplicação de respostas e tempo de drenagem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3B-S005, V4B-S004, V3D-S016.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Em 3–7B, replay de uma conversa curta pode ser mais simples que infraestrutura de migração de KV.
8–14B: Em 8–14B, manter cache de sessões ativas e externalizar histórico permite mobilidade com custo previsível.
15–30B: Em 15–30B, planejar retenção e drenagem por bytes KV, não somente por quantidade de sessões.
Requisitos de treino/runtime: Runtime fornece cache e cancelamento; aplicação fornece revisão, histórico durável e semântica de confirmação.
Não aplicar quando: Não presumir afinidade garantida pelo balanceador nem usar ID de sessão como autorização suficiente.

## T084:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4B-C004 — Cloudflare / Workers AI
Evidência: produção documentada; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: infraestrutura de inferência de LLM.
Uso observado: Cloudflare descreve prefix caching já utilizado no Workers AI e a exposição de tokens em cache, além de afinidade de sessão para alcançar a mesma instância.
Mecanismo documentado: Reuso de tensores do prefill em prefixos idênticos; encaminhamento com identificador de afinidade e fila assíncrona que aproveita capacidade.
Correspondência com esta base: Afinidade por sessão aumenta chance de cache, mas não demonstra todo o contrato de revisão de sessão da ficha.
Transferência proposta para modelo pequeno: Proposta: em serviço 3–30B, testar afinidade com limite de espera e fallback, e medir tokens reutilizados sem confundir desconto comercial com economia de hardware.
Limite: A página destaca modelos grandes; não fixa aplicabilidade nem SLO para todos os modelos. Cloudflare é classificada como operador tecnológico, não contada automaticamente como bigtech estrita.
Fontes: V4B-S004.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca de família e fontes oficiais consultadas em 05/11/2026. Ausência de caso exato significa não encontrado neste recorte; recursos documentados e propostas não contam como implantação.
Consultas registradas: V4B-Q002.

## T084:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T084 → T064 [requires]
Como combinar: Persistir histórico confirmado e artefatos antes de depender do cache de sessão.
Interface: ID estável, revisão e resultados aceitos.
Condição: Estado durável pode reconstruir a entrada exata.
Aceite proposto: Excluir todo KV e retomar sem repetir ferramentas concluídas.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, V4B-S004, V3D-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T084 → T120 [complements]
Como combinar: Escolher destino com afinidade enquanto fila e saúde permanecem adequadas.
Interface: Localização preferida, validade do lease e atraso previsto.
Condição: Roteador dispõe de fallback e não confunde afinidade com exclusividade.
Aceite proposto: Derrubar o destino preferido e verificar retomada controlada.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3B-S005, V4B-S004, V3D-S016. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Rejeitar commit de tentativa com revisão vencida.
- Testar perda de worker durante streaming e não publicar fragmentos obsoletos.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Avaliar continuidade de uma missão em condições de falha frente a uma baseline de fronteira. Cache reduz recomputação; qualidade da recuperação depende dos contratos de estado e não do número de parâmetros.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T081, T082, T154, T064

## Fontes primárias associadas

### B-S003 — Cache strategies

[https://huggingface.co/docs/transformers/main/en/kv_cache](https://huggingface.co/docs/transformers/main/en/kv_cache)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Reuso de estados KV; caches dinâmico, estático e quantizado; controle de past_key_values.

Limite: Documentação consultada nesta data; compatibilidade depende da versão, modelo e hardware. Sem ensaio no ambiente LAI.

### V3B-S005 — How caching works

[https://huggingface.co/docs/transformers/main/en/cache_explanation](https://huggingface.co/docs/transformers/main/en/cache_explanation)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Semântica causal de reutilização KV, máscara cobrindo passado e presente, estado por camada.

Limite: Documentação dinâmica main consultada em 2026-11-05; contrato de sessão é inferência editorial, não API documentada.

### V4B-S004 — Powering the agents: Workers AI now runs large models, starting with Kimi K2.5

[https://blog.cloudflare.com/workers-ai-large-models/](https://blog.cloudflare.com/workers-ai-large-models/)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Workers AI descreve prefix caching, afinidade por sessão, métricas de cache e fila assíncrona orientada por capacidade.

Limite: Disponibilidade por modelo e contexto temporal; política de preço e ganhos não extrapolados.

### V3D-S016 — LangGraph — Persistence: checkpointers and stores

[https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Checkpointers persistem estado de thread; stores mantêm dados entre threads.

Limite: A antiga rota durable-execution redireciona para esta página; não usada como prova de replay determinístico.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
