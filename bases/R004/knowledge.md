# R004 — Generative Agents

**Nome canônico:** Generative Agents: Interactive Simulacra of Human Behavior  
**Grupo:** Pesquisas, projetos e tecnologias de referência  
**Escopo:** referencia  
**Natureza:** paper  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** R004  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** agentes generativos; memory stream; reflexão episódica

## R004:C01 — conceito

Pesquisa sobre agentes que simulam comportamentos humanos em um ambiente interativo. A arquitetura registra experiências em linguagem natural, produz reflexões de nível mais alto e recupera memórias para planejamento. Sua avaliação de comportamento plausível não demonstra que um agente empresarial tomará decisões corretas ou seguras.

Como funciona:
- Registrar observações e experiências do agente em um fluxo de memória.
- Sintetizar reflexões que relacionam experiências anteriores.
- Recuperar conteúdo relevante para planejar e ajustar ações no ambiente.

## R004:C02 — aplicacao

Quando usar:
- Estudo de memória episódica e planejamento em simulações.
- Prototipação de exercícios de interação com personagens e cenários controlados.

Quando não usar:
- Como evidência de leitura real de intenção humana ou validação científica de um cliente específico.

Implementação proposta:
- Proposta: começar com simulação pequena e registrar todas as observações com sua origem.
- Separar observação literal de reflexão inferida para não transformar uma interpretação em fato.
- Comparar memória completa, memória sem reflexão e memória sem recuperação mantendo os cenários iguais.

Aplicação LAI proposta:
Proposta LAI: usar a separação entre experiência, reflexão e plano para treinos simulados de vendas; validar resultados reais por evidências externas à simulação.

## R004:C03 — riscos_validacao

Armadilhas:
- Um comportamento convincente pode encobrir uma decisão factual incorreta.
- Reflexões geradas pelo próprio modelo podem retroalimentar uma interpretação falsa.

Métricas sugeridas:
- Consistência com observações e objetivos declarados do cenário.
- Frequência de inferências indevidas promovidas a fatos e custo por episódio.

Testes propostos:
- Proposta: inserir uma observação ambígua e confirmar que a inferência permanece identificada.
- Corrigir uma informação do personagem e medir se o planejamento usa a atualização.

## R004:C04 — perguntas_proveniencia

Pergunta: Comportamento plausível prova competência comercial?
Resposta: Não. Plausibilidade em uma simulação e resultado comercial real são critérios diferentes.

Pergunta: Reflexão deve virar memória comprovada?
Resposta: Somente após critérios de validação adequados. Inicialmente, é uma interpretação do agente.

Pergunta: A importância usada no artigo é confiança factual?
Resposta: Não. Ela destaca a relevância percebida do evento para o agente simulado. Um item importante ainda pode conter interpretação equivocada.

Pergunta: Refletir sobre reflexões aumenta evidência disponível?
Resposta: Aumenta organização e abstração, não o número de observações independentes. A cadeia deve continuar apontando às origens que realmente sustentam a conclusão.

Escopo das fontes:
A-S008 sustenta os componentes de observação, reflexão, planejamento e recuperação na simulação. Os controles de evidência e critérios comerciais acima são propostas editoriais.

## R004:C05 — mecanismo_avancado

Generative Agents calcula recuperação combinando recência de acesso, importância atribuída e relevância à situação. Reflexões entram novamente no mesmo fluxo e podem sustentar reflexões posteriores por referências. Isso cria uma estrutura de derivação útil à coerência, mas também um caminho de autorreforço: uma interpretação incorreta pode reaparecer com aparência de conhecimento consolidado se não for distinguida da observação original.

Condição de contorno:
Plausibilidade de comportamento numa simulação não mede a verdade de afirmações, capacidade causal ou confiabilidade de decisões num ambiente empresarial.

Contrato proposto:
- Entradas: Observações da simulação, situação atual, memórias anteriores e regras de planejamento.
- Saídas: Ações planejadas, reflexões derivadas e memórias selecionadas para a próxima inferência.
- Estado: Fluxo de memória, tempos de criação e acesso, escores e referências das reflexões.
- Invariante: Reflexão mantém status de inferência e não é confundida com nova observação independente do ambiente.

Compromissos de projeto:
- Reflexões permitem abstrair padrões e podem amplificar interpretações erradas.
- Recência por acesso mantém continuidade e pode privilegiar lembranças já usadas, reduzindo exposição a evidência esquecida.

## R004:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: introduzir uma observação ambígua que gere inferência incorreta e depois apresentar correção direta. O sistema deve revisar derivados relevantes, sem contar reflexões repetidas como várias confirmações.

Plano de avaliação proposto:
Avaliação proposta: comparar arquitetura completa com remoção de reflexão ou variação do recuperador. Medir coerência, fidelidade às observações, propagação de correções e custo; mantenha plausibilidade e precisão factual como dimensões separadas.

Comparações:
- T049 (complements): O fluxo registra experiências situadas que podem ser recuperadas para orientar comportamento.
- T058 (complements): Reflexões sintetizam memórias em abstrações, exigindo rastreabilidade das derivações.

Afirmação rastreável:
O artigo combina relevância, recência e importância na recuperação e armazena reflexões com referências às memórias utilizadas.
Suporte: direct; fontes: A-S008
Limite: Pesos e limiares ilustrados pertencem à simulação estudada; não são recomendações universais para memória operacional.

Nota de pesquisa:
Síntese técnica com fontes primárias; contratos, cenários de falha e critérios de decisão são propostas editoriais, não execução na LAI.

## R004:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 distinguiu plausibilidade e verdade. Aqui Generative Agents é usado para estudar crenças divergentes e transferência de memória em simulação controlada.

Projeto e decomposição
Separe estado verdadeiro do ambiente e crenças de cada agente. Reflexões podem ser coerentes com observações incompletas e ainda estar erradas; isso deve ser mensurável no experimento.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

Controle adaptativo
Controle quais eventos cada agente presencia e quais recebe por relato. A memória precisa preservar origem para distinguir experiência direta, rumor e inferência.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

Validação contrafactual
Compare agentes com reflexão, somente episódios e memória fornecida por controlador. Meça fidelidade ao que foi observado, propagação de rumores e ações compatíveis com crenças, sem confundir realismo narrativo com acerto. Unidade de avaliação: agente em simulação.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

USO AVANÇADO — Simulação de colaboração
Cenário: Agentes precisam coordenar tarefas com informação parcial.
Estratégia: Distribuir observações diferentes, registrar mensagens e verificar como crenças convergem após evidência nova.
Papel do modelo pequeno: 3–7B atua em papéis estreitos.
Aceite proposto: Agente não pode usar informação que nunca recebeu.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

USO AVANÇADO — Treino de recuperação episódica
Cenário: É preciso testar memória sob ruído.
Estratégia: Criar ambiente sintético próprio com eventos identificados e mudanças de preferência; comparar recência, relevância e importância.
Papel do modelo pequeno: 8–14B recupera; 15–30B planeja.
Aceite proposto: Correção explícita deve alterar comportamento sem apagar histórico de crença.
Natureza: proposta de engenharia; não medida neste pacote; fontes: A-S008.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Agente simulado com vocabulário e ações limitadas.
8–14B: Agente com memória episódica e reflexão em ambiente controlado.
15–30B: Planejador social experimental, sem extrapolar para comportamento humano real.
Requisitos de treino/runtime: Simulador com estado conhecido, logs e controle de observações; não usar comportamento plausível como único avaliador.
Não aplicar quando: A intenção é prever pessoas reais ou validar causalidade social sem desenho empírico apropriado.

## R004:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4A-C030 — Autores Generative Agents / Generative Agents / Smallville
Evidência: pesquisa; não comprova produção; correspondência exata do mecanismo. Organização: grupo de pesquisa.
Domínio observado: pesquisa sobre LLM.
Uso observado: Estudo constrói agentes simulados que registram experiências e refletem.
Mecanismo documentado: Memórias episódicas, recuperação, reflexão e planejamento em ambiente simulado.
Correspondência com esta base: Trabalho identificado.
Transferência proposta para modelo pequeno: Proposta de engenharia: Usar simulação restrita para estudar recuperação com 3–14B, distinguindo crenças de fatos.
Limite: Simulação e plausibilidade não comprovam produção, causalidade ou confiabilidade empresarial. Não comprova resultado no ambiente do usuário nem equivalência geral de modelos 3–30B.
Fontes: A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Busca por família; produtos e pesquisas separados de produção. Correspondência aproximada não satisfaz a meta de dez. Estratégia proposta, sem execução local.
Consultas registradas: V4A-Q023.

## R004:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. R004 → T049 [requires]
Como combinar: Registrar experiências com origem e observador.
Interface: Evento, agente, percepção e tempo.
Condição: Store distinguir observação de relato.
Aceite proposto: Introduzir rumor e rastrear sua propagação.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. R004 → T051 [complements]
Como combinar: Separar perspectivas e crenças no grafo.
Interface: Relação, agente que acredita e evidência.
Condição: Crença não ser promovida a fato do ambiente.
Aceite proposto: Consultar perspectiva individual e comparar com estado verdadeiro.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não chamar simulação de prova de produção empresarial.
- Não inferir personalidade humana real a partir de agente textual.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Comparar memória e coordenação dentro do simulador; realismo de personagens não demonstra inteligência social geral.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T049, T054, T058, T071

## Fontes primárias associadas

### A-S008 — Generative Agents: Interactive Simulacra of Human Behavior

[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Experiências em linguagem natural, reflexões e recuperação para orientar agentes simulados.

Limite: Leitura da página indicada; não equivale à reprodução experimental nem à auditoria integral do projeto.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
