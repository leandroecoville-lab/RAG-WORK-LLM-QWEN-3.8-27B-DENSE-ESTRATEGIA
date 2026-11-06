# T041 — Last-N Messages Window

**Nome canônico:** Last-N Messages Window  
**Grupo:** Contexto, compressão e recuperação  
**Escopo:** inventario  
**Natureza:** pattern  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T041  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** janela das últimas mensagens

## T041:C01 — conceito

Mantém as últimas N mensagens, preservando separadamente instruções obrigatórias. É a forma mais simples de janela móvel. N mede mensagens, não tokens: uma única resposta de ferramenta pode ser maior que dezenas de mensagens de conversa.

Como funciona:
- Definir o que conta como mensagem ou turno.
- Selecionar o sufixo recente sem quebrar interações estruturadas.
- Anexar estado essencial e referências ao histórico arquivado.

## T041:C02 — aplicacao

Quando usar:
- Protótipos e conversas de mensagens curtas.
- Baseline para comparar políticas de contexto mais sofisticadas.

Quando não usar:
- Não é suficiente para limitar tokens quando o tamanho das mensagens varia muito.

Implementação proposta:
- Proposta: definir janela em turnos completos quando houver ferramentas.
- Aplicar um teto de tokens adicional.
- Persistir decisões que continuam válidas fora da janela e recuperar detalhes antigos quando referenciados.

Aplicação LAI proposta:
Proposta LAI: usar como componente de histórico recente, sem confundir com memória durável ou política de planejamento da Helena.

## T041:C03 — riscos_validacao

Armadilhas:
- Uma mensagem longa pode ultrapassar o limite sozinha.
- N mensagens podem cortar uma pergunta, mantendo apenas sua resposta.

Métricas sugeridas:
- Tokens máximos por chamada.
- Esquecimento de fatos anteriores à janela.

Testes propostos:
- Gerar uma mensagem de ferramenta muito longa e exigir proteção por orçamento.
- Colocar uma decisão no turno N+1 anterior e confirmar preservação no estado essencial.

## T041:C04 — perguntas_proveniencia

Pergunta: N=20 significa vinte trocas completas?
Resposta: Só se o runtime definiu assim. É necessário distinguir mensagens individuais e turnos.

Pergunta: É melhor aumentar N sempre?
Resposta: Não. Isso aumenta custo e pode adicionar ruído; a escolha deve seguir avaliação de qualidade e orçamento.

Pergunta: Reexecutar o corte deve produzir o mesmo resultado?
Resposta: Sim, se histórico, N e regras forem iguais. Novas mensagens ou mudanças de agrupamento devem explicar qualquer diferença.

Pergunta: Como detectar exclusão persistente acidental?
Resposta: Compare o histórico armazenado antes e depois da montagem. Uma política de apresentação não deveria apagar eventos sem contrato explícito.

Escopo das fontes:
As fontes sustentam os conceitos relacionados. Implementação, aplicação LAI e critérios de teste abaixo são propostas editoriais; não são resultados executados nem garantia de desempenho.

## T041:C05 — mecanismo_avancado

O tamanho N depende da serialização da conversa. Uma resposta do assistente pode conter várias chamadas paralelas, seguidas por resultados em mensagens separadas; outro backend pode agrupar resultados. Assim, N constante não preserva a mesma interação entre provedores. A política deve operar sobre unidades conversacionais definidas e gerar uma visão para a chamada, distinguindo esse corte de uma exclusão persistente no estado.

Condição de contorno:
Se o histórico é altamente assimétrico ou ferramentas produzem muitas mensagens intermediárias, contar mensagens passa a refletir detalhes do protocolo mais que contexto útil.

Contrato proposto:
- Entradas: Histórico ordenado, definição de turno e vínculos entre chamadas e resultados de ferramentas.
- Saídas: Sufixo válido para o provedor, acompanhado de decisão explícita sobre arquivamento e persistência.
- Estado: Sequência de eventos, IDs de mensagens e política de agrupamento de interações.
- Invariante: Aplicar uma visão limitada não elimina o histórico original por consequência não declarada.

Compromissos de projeto:
- Contagem de mensagens é simples de explicar e pouco estável diante de mudanças de protocolo.
- Agrupar interações evita pares quebrados e faz o tamanho efetivo variar em relação ao N nominal.

## T041:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: emitir três chamadas paralelas no mesmo turno e cortar entre seus resultados. O montador deve manter a unidade necessária ou indicar a impossibilidade de caber no orçamento.

Plano de avaliação proposto:
Avaliação proposta: comparar N mensagens, N turnos e orçamento por tokens no mesmo histórico lógico serializado de formas diferentes. Medir validade protocolar, contexto útil preservado e tokens reais; separar perda por corte de perda por persistência indevida.

Comparações:
- T003 (specializes): FIFO define a política de saída dos antigos; Last-N especifica uma medida particular da capacidade.
- T042 (complements): O limite em tokens pode impedir que um sufixo válido exceda a capacidade efetiva.

Afirmação rastreável:
LangChain distingue estratégias de corte, remoção de mensagens do estado e substituição por resumos.
Suporte: direct; fontes: A-S003
Limite: Exemplos de middleware podem modificar o estado; não se deve presumir que toda função chamada trim cria apenas uma visão temporária.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## T041:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 mostrou variabilidade de mensagens. Aqui Last-N é um baseline controlado e uma política por classe de interação.

Projeto e decomposição
Escolha N por classe de diálogo usando distribuição real de mensagens e densidade de informação. Uma conversa com ferramentas extensas não deve compartilhar configuração com chat curto.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Controle adaptativo
Reinicie a seleção recente após mudança confirmada de objetivo, conservando contratos ativos fora da fila. A janela não deve importar detalhes de assunto antigo só porque ainda estão entre os últimos turnos.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

Validação contrafactual
Compare N fixo, N por classe e janela por tokens com o mesmo teto máximo. Meça requisitos antigos esquecidos, custo médio e picos; não usar apenas conversas sem interrupções. Unidade de avaliação: conversa com mudança de tema.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Atendimento com questões independentes
Cenário: Usuário muda de assunto várias vezes.
Estratégia: Detectar mudança explícita, carregar identidade e preferências necessárias e limitar histórico do assunto anterior.
Papel do modelo pequeno: 3–7B classifica tema.
Aceite proposto: Não reutilizar resposta ou entidade do tema abandonado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

USO AVANÇADO — Fluxo de extração repetitiva
Cenário: Cada turno processa um item novo.
Estratégia: Manter instrução fixa e poucos exemplos recentes, arquivando resultados em tabela fora da janela.
Papel do modelo pequeno: 8–14B trata exceções.
Aceite proposto: Itens anteriores não podem contaminar campos do item atual.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S003, V4A-S002.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Classificador de tema com janela curta e instrução estável.
8–14B: Leitor de poucas interações que incluem correções locais.
15–30B: Supervisor de mudanças de objetivo, usando referências ao histórico quando necessário.
Requisitos de treino/runtime: Agrupamento por turnos lógicos e perfil de tamanho; ajuste de N não requer treino do modelo.
Não aplicar quando: Dependências antigas são frequentes e não existe mecanismo separado para obrigações ou recuperação.

## T041:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

Nenhum caso com mapeamento individualizado foi confirmado para esta base nesta curadoria. Não foram criados exemplos fictícios.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q002.

## T041:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T041 → T042 [complements]
Como combinar: Aplicar teto de tokens à seleção Last-N.
Interface: Turnos elegíveis, custo real e reserva.
Condição: Grupos de protocolo permanecerem completos.
Aceite proposto: Testar uma única mensagem maior que o orçamento.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T041 → T047 [requires]
Como combinar: Manter fatos duráveis fora da fila recente.
Interface: Preferência confirmada, escopo e origem.
Condição: Persistência não ser inferida da presença recente.
Aceite proposto: Retomar fato após ele sair dos últimos N turnos.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S003, V4A-S002. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não contar mensagens de sistema e ferramenta como unidades equivalentes.
- Não concluir que conteúdo arquivado será lembrado automaticamente.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Usar Last-N como controle simples; comparar retenção de obrigações e custo, sem atribuir ganho cognitivo ao tamanho N.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T003, T042, T050

## Fontes primárias associadas

### A-S003 — Short-term memory

[https://docs.langchain.com/oss/python/langchain/short-term-memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Histórico por thread, redução de mensagens e persistência do estado de curta duração.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

### V4A-S002 — Context engineering: memory, compaction, and tool clearing

[https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Distingue compactação, remoção de resultados e memória; explicita uso de estratégias no Claude Code.

Limite: Escopo limitado ao material aberto. Disponibilidade, resultados experimentais e implantação histórica são classes distintas; não demonstra desempenho de modelos 3–30B no ambiente do usuário.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
