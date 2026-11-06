# T230 — Unified Diff

**Nome canônico:** Unified Diff  
**Grupo:** Continuidade, programação e controle operacional  
**Escopo:** inventario  
**Natureza:** format  
**Estado da evidência:** Conceito sustentado pelas fontes associadas  
**ID canônico:** T230  
**Data da curadoria:** 2026-11-05

**Nomes de busca:** diff unificado

## T230:C01 — conceito

Formato textual de diferenças organizado por arquivos e blocos chamados hunks. Cada hunk informa intervalos na versão anterior e na nova e apresenta linhas mantidas, removidas e adicionadas. Git produz e consome variantes com metadados adicionais; esses detalhes precisam ser interpretados pelo aplicador correto.

Como funciona:
- Cabeçalhos identificam os arquivos anterior e posterior.
- Um cabeçalho de hunk descreve posição e extensão dos intervalos antigos e novos.
- Prefixos distinguem contexto, remoção e adição; o contexto ajuda a localizar a região afetada.

## T230:C02 — aplicacao

Quando usar:
- Revisão de código, transporte de alterações textuais e aplicação controlada em ferramentas que aceitam o formato.

Quando não usar:
- Usar um parser simplista para qualquer saída de Git ou tratar o formato textual básico como representação completa de binários e renomeações.

Implementação proposta:
- Proposta: gerar patches com ferramenta confiável, preservando conteúdo literal e quebras de linha.
- Registrar separadamente a revisão-base ou hashes quando a integridade da base for necessária.
- Usar um aplicador compatível com os metadados emitidos e validar caminhos antes da gravação.
- Inspecionar alterações de modo, renomeação e marcadores de fim de arquivo quando presentes.
- Após aplicar, comparar o resultado esperado ao diff efetivamente produzido e verificar o comportamento afetado.

Aplicação LAI proposta:
Proposta LAI: adotar unified diff como um formato possível de entrega de mudanças, acompanhado de identidade da base e validação independente do conteúdo.

## T230:C03 — riscos_validacao

Armadilhas:
- Os números de linha ficam desatualizados após mudanças concorrentes.
- Tabs, finais de linha e ausência de newline final podem ser relevantes.
- Um patch sintaticamente válido pode alterar o arquivo errado se o mapeamento de caminhos for incorreto.

Métricas sugeridas:
- Hunks aplicados e rejeitados; divergência de contexto; mudanças de caminho; diferenças inesperadas após aplicação.

Testes propostos:
- Aplicar um exemplo com múltiplos hunks e conferir exatamente as linhas resultantes.
- Testar arquivo sem newline final e preservação do estado esperado.
- Introduzir caminho fora do escopo e verificar rejeição pelo aplicador autorizado.

## T230:C04 — perguntas_proveniencia

Pergunta: Unified Diff inclui sempre o hash da base?
Resposta: Não. Cabeçalhos de hunk e linhas de contexto não fornecem, sozinhos, uma garantia criptográfica. Algumas variantes Git incluem informações adicionais, mas a política deve verificar o que está presente.

Pergunta: Aplicar sem erro prova correção?
Resposta: Não. Prova apenas que o aplicador aceitou as alterações nas condições observadas. Correção semântica exige revisão e verificações do comportamento.

Pergunta: Uma linha +++ sempre representa conteúdo adicionado?
Resposta: Não. Pode ser o cabeçalho do arquivo novo; a interpretação depende do estado do parser.

Pergunta: As posições tornam o patch independente da base?
Resposta: Não. Contexto e conteúdo esperado ainda precisam corresponder à revisão em que a alteração será aplicada.

Escopo das fontes:
As fontes apoiam o conceito ou padrões relacionados. A implementação, a aplicação LAI e os testes descritos são propostas editoriais, sem execução ou benchmark na infraestrutura do usuário.

## T230:C05 — mecanismo_avancado

No cabeçalho @@ -l,s +l,s @@, os intervalos descrevem posição e quantidade de linhas das versões antiga e nova; contagens omitidas representam casos unitários do formato. Linhas de contexto participam dos dois lados, remoções somente do antigo e adições somente do novo. Metadados Git podem incluir modos, renomes e IDs de blobs. Combined diff de merges possui outra estrutura e não deve ser tratado como patch comum de dois lados.

Condição de contorno:
Um parser que reconhece apenas linhas iniciadas por mais e menos pode confundir cabeçalhos, conteúdo e mudanças de metadados.

Contrato proposto:
- Entradas: Diff, dialeto de formato, base e convenção de caminhos.
- Saídas: Hunks interpretados, mudanças de arquivo e diagnóstico de inconsistência.
- Estado: Contagens por lado, arquivo corrente e metadados de versão.
- Invariante: As contagens do hunk correspondem às linhas que cada lado realmente contém.

Compromissos de projeto:
- Metadados adicionais melhoram identificação e exigem parser compatível.
- Contexto mínimo reduz tamanho e aumenta fragilidade diante de alterações próximas.

## T230:C06 — experimento_comparacao

Falha a injetar e resultado esperado — proposta:
Teste proposto: incluir criação, remoção, renome e marcador de ausência de newline; conferir que o parser distingue metadados de linhas editáveis e preserva conteúdo final.

Plano de avaliação proposto:
Comparar parser simples e aplicador oficial sobre patches com casos-limite. Medir rejeição de hunks malformados, equivalência dos bytes produzidos e tratamento de modos. Usar a base exata para não atribuir conflito legítimo a defeito do formato.

Comparações:
- T229 (complements): Patch-based coding escolhe a estratégia de edição; Unified Diff fornece uma representação específica.
- T231 (distinct_from): Search/replace identifica texto literal e usa outro contrato de localização.

Afirmação rastreável:
A documentação Git distingue patch de dois lados e combined diff, além de cabeçalhos estendidos.
Suporte: direct; fontes: V2A-S013
Limite: Nem todo texto visualmente parecido com diff é aceito pelo mesmo aplicador ou representa os mesmos metadados.

Nota de pesquisa:
Mecanismos referenciados em fontes primárias; contratos e verificação descritos são propostas, não ensaios executados.

## T230:C07 — estrategia_3_30b

NOVA CAMADA v4 — A v3 descrevia hunks e diferenças de metadados. A ampliação trata Unified Diff como linguagem de entrada não confiável, com parsing completo, política de caminhos e verificação de que a aplicação produziu o delta pretendido.

Parser antes de aplicação
Valide cabeçalhos, contagens e sequência de hunks antes de modificar arquivos. Linhas que parecem metadados podem fazer parte do conteúdo, e mensagens extras de um modelo não pertencem ao patch. Defina quais extensões do formato o aplicador aceita; rejeitar explicitamente um formato não suportado é melhor que interpretar parcialmente e continuar.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V2A-S013.

Caminhos e tipos de objeto
Normalize caminhos segundo a semântica do aplicador e confira escopo permitido. Renome, symlink, permissão executável e arquivo binário não são simples mudanças de linhas. Uma tarefa de texto pode proibir essas operações; se forem necessárias, devem ter contrato próprio. O validador precisa examinar tanto cabeçalho quanto resultado no filesystem.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V3C-S037.

Aplicação observada
Depois de aplicar, recalcule o diff da árvore resultante e compare com intenção e escopo. Contexto deslocado, normalização de quebras de linha ou tolerância do aplicador podem alterar a interpretação. Se a base divergiu, faça merge suportado ou gere novo candidato com leitura atual; não trate números de linha como endereço absoluto independente de versão.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034.

USO AVANÇADO — Editor restrito por protocolo
Cenário: Um modelo pequeno retorna somente um patch para alteração local.
Estratégia: Forneça exemplo mínimo do formato aceito e proíba prosa dentro da saída consumida. Faça parsing e aplicação em sandbox, valide contagens e arquivo alvo e devolva erro estruturado em caso de rejeição. O reparo recebe a causa específica, sem executar fragmentos de patch válidos isoladamente.
Papel do modelo pequeno: 3–7B emite hunks pequenos; 8–14B corrige representação a partir do erro.
Aceite proposto: Proposta: nenhuma aplicação parcial silenciosa e alta taxa de formato válido sem reduzir teste semântico.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V2A-S013, V3C-S034.

USO AVANÇADO — Mudança com vários arquivos
Cenário: Um patch inclui renome e edição de conteúdo.
Estratégia: Declare previamente se o fluxo aceita renomes e modos. Verifique que o destino não colide com arquivo existente e que o diff final corresponde à movimentação esperada. Rode testes sobre a árvore inteira resultante, não sobre cada hunk isolado.
Papel do modelo pequeno: 15–30B pode planejar relações; aplicador determinístico executa operação validada.
Aceite proposto: Proposta: caminhos corretos, metadados preservados e nenhuma alteração fora do conjunto autorizado.
Natureza: proposta de engenharia; não medida neste pacote; fontes: V3C-S034, V3C-S037.

ADEQUAÇÃO A MODELOS PEQUENOS — hipóteses de projeto, não ranking universal
3–7B: Hunks curtos e exemplos consistentes são mais tratáveis que patches extensos com metadados mistos.
8–14B: Reparo de formato e identificação de conflito de contexto em múltiplos arquivos.
15–30B: Planejamento de mudanças maiores, mantendo parsing e aplicação fora da LLM.
Requisitos de treino/runtime: Aplicador versionado, política de extensões, normalização conhecida e validação em árvore isolada.
Não aplicar quando: Não confundir Aider diff, udiff adaptado e Unified Diff padrão nem aceitar combined diff como patch comum.

## T230:C08 — casos_producao

META: 10 exemplos de produção de Big Tech para esta base. Comprovados com correspondência exata nesta curadoria: 0. Lacuna: 10. Laboratórios de IA, contados separadamente: 0; outros operadores com produção exata: 0.
Subconjunto estrito aplicado a LLMs (aplicação, serving ou treino): 0. Os demais podem documentar o mecanismo em infraestrutura sem LLM.
A lacuna registra o que esta pesquisa não comprovou; não afirma inexistência mundial. A referência a um sistema não prova que ele utilize toda a ficha.

V4C-C028 — Aider / Architect/editor e formatos de edição
Evidência: produto/recurso disponível; somente família relacionada. Organização: outro operador de tecnologia.
Domínio observado: ferramenta/framework para LLM.
Uso observado: Documentação disponibiliza modo architect e formatos whole, diff e udiff.
Mecanismo documentado: Uma chamada propõe a solução e outra traduz em edições; formatos têm contratos diferentes e podem usar o mesmo modelo.
Correspondência com esta base: Formato udiff documentado é baseado em diffs, com convenção própria; não é edição AST.
Transferência proposta para modelo pequeno: Proposta: testar 3–7B como tradutor de edições curtas e 15–30B como arquiteto, sem presumir que dividir melhora acerto.
Limite: Recurso disponível não comprova adoção empresarial nem desempenho nesta instalação. Mesma fonte reaproveitada da v3, reaberta nesta pesquisa.
Fontes: V3C-S042, V2A-S008.

Metadados completos dos casos: production_cases.json desta base.
Pesquisa: Documentação Git e Aider apoia formatos e distinções. Não foi inferida produção de Unified Diff apenas porque uma empresa usa controle de versões. Consulta complementar específica registrada na consolidação; ver limites da busca e da correspondência, sem criar casos não comprovados.
Consultas registradas: V4C-Q023, V4C-Q015, V4D-Q024.

## T230:C09 — conexoes_aceite

CONEXÕES INDIVIDUAIS — ordem, interface, condição e teste

Conexão documentada confirma o uso combinado delimitado pela fonte. Os contratos de interface, condições de adaptação e aceites abaixo são orientações de engenharia; não constituem uma API oficial ou ganho já medido, salvo atribuição factual explícita.

1. T230 → T229 [complements]
Como combinar: Unified Diff pode representar o delta de uma estratégia de edição por patch, conforme o aplicador escolhido.
Interface: Hunks, metadados e revisão base.
Condição: Formato e extensões são explicitamente suportados.
Aceite proposto: Delta aplicado corresponde à intenção e ao escopo.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S034, V2A-S008. Casos: nenhum caso operacional comprova esta conexão proposta.

2. T230 → T233 [feeds]
Como combinar: Entregar a árvore candidata e a identidade da base para validação antes de publicação.
Interface: Patch parseado, árvore resultante e hashes.
Condição: Nenhum erro de aplicação foi ignorado.
Aceite proposto: Verificação final incide sobre o artefato exato a ser publicado.
Natureza: proposta de engenharia; não medida neste pacote. Fontes: V3C-S037. Casos: nenhum caso operacional comprova esta conexão proposta.

CONTROLES DE FALHA
- Não usar extração ingênua de linhas com mais ou menos como parser.
- Marcadores de ausência de newline e mudanças CRLF precisam de tratamento conforme o aplicador real.

COMPARAÇÃO COM FRONTEIRA — protocolo proposto
Compare aderência ao formato, sucesso de aplicação e correção separadamente. Modelos pequenos podem emitir diffs bons em casos curtos; isso não garante competência em mudanças arquiteturais.

Os parâmetros totais, a arquitetura, o treino, a quantização, o contexto e o hardware devem ser registrados. Mais mecanismos podem elevar custo e falhas. Escolher por ablação e sucesso por tarefa; não presumir paridade geral.

## Relações

T229, T233

## Fontes primárias associadas

### V2A-S013 — diff-format

[https://git-scm.com/docs/diff-format](https://git-scm.com/docs/diff-format)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Estrutura de diferenças produzidas pelo Git; cabeçalhos e hunks de alterações.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V2A-S014 — git-apply

[https://git-scm.com/docs/git-apply](https://git-scm.com/docs/git-apply)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Verificação e aplicação de patches; contexto, índice e tratamento de caminhos.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S034 — Git — git-diff

[https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Comparação entre revisões, índice e árvore de trabalho; formatos de diferenças e identificação dos objetos comparados.

Limite: Diff é evidência textual e estrutural da mudança, não teste de comportamento nem captura de estado externo.

### V3C-S037 — Git — git-update-ref

[https://git-scm.com/docs/git-update-ref](https://git-scm.com/docs/git-update-ref)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Atualização condicional de ref compara old-oid; transações bloqueiam e validam refs antes de aplicar mudanças.

Limite: Atomicidade de cada ref não significa snapshot simultâneo garantido a todo leitor concorrente de várias refs.

### V2A-S008 — Edit formats

[https://aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Formatos de edição incluindo substituição e diffs; o formato exato depende do executor.

Limite: Consulta documental primária. Não houve reprodução de experimentos, instalação do produto nem validação de disponibilidade na infraestrutura LAI. Receitas e testes das entradas são propostas editoriais.

### V3C-S042 — Chat modes — Architect mode and the editor model

[https://aider.chat/docs/usage/modes.html](https://aider.chat/docs/usage/modes.html)

Consulta: 2026-11-05; estado: `opened`.

Sustenta: Modo architect divide a solicitação em proposta e edição; papéis podem usar o mesmo modelo; editor usa formato próprio de alterações.

Limite: Documentação primária consultada, sem execução do Aider. Exemplos de modelos da página não são recomendações atuais; a separação em duas chamadas não demonstra ganho universal.

As seções de aplicação, implementação e validação são propostas de engenharia. Esta ficha não comprova que a técnica foi implementada, treinada ou testada na LAI.
