# Política de casos, correspondência e contagem

## Produção não é uma palavra promocional

Um caso é `production_documented` quando uma fonte primária do operador/autores descreve implantação ou uso real. `operational_product` significa recurso/produto documentado, sem comprovar a implantação ou escala específica. `research_only` significa pesquisa ou benchmark. Uma publicação acadêmica pode descrever uma implantação real; nesse caso, o conteúdo e seu recorte justificam a classe, não o formato do documento.

Uma afirmação de produção vale para o mecanismo documentado. Disponibilizar uma biblioteca com várias opções não demonstra que todas as opções estejam ativas em cada usuário da biblioteca. Um changelog recente não reescreve retroativamente a configuração de um deployment antigo.

## Correspondência por base

- `exact`: a fonte sustenta especificamente o mecanismo da entrada.
- `family`: a fonte sustenta somente uma família relacionada; não se assume o algoritmo exato.
- `analogy`: aplicação comparável, sem adoção literal do componente.

Resumo não comprova sumarização em cadeia. Cache geral não comprova cache semântico. Um banco transacional não comprova memória episódica de agente. Treinar adaptador contra pesos quantizados não comprova todos os detalhes do método QLoRA original. Essas diferenças permanecem nos mapeamentos.

As entradas P são nomes de propostas arquiteturais. Seus mapeamentos são sempre `analogy`; não se atribui à Big Tech um produto LAI que ela não declarou utilizar.

## Recorte organizacional explícito

Para a meta estrita, a curadoria usa o núcleo de grandes plataformas e fabricantes representados por Apple, Alphabet/Google/DeepMind, Microsoft/GitHub/LinkedIn, Amazon/AWS, Meta/Facebook, NVIDIA, Alibaba, Baidu, Tencent, ByteDance, IBM, Salesforce e Oracle, quando presentes nos registros. A classificação não afirma que exista uma definição mundial única de Big Tech.

OpenAI, Anthropic, DeepSeek, Moonshot AI e Thinking Machines são identificados como `ai_lab` e contados separadamente. Uber, Netflix, Perplexity, Cloudflare, Snowflake, Letta, Coinbase e outros operadores recebem `technology_operator` quando presentes. Autores universitários ou grupos sem um operador corporativo identificado recebem `research_group`.

Essa separação é conservadora: não reclassifica um operador apenas para aumentar a contagem pedida. O catálogo mantém seus casos úteis, inclusive integrações que podem inspirar sistemas 3–30B.

## Regra de dez exemplos

Um caso conta na meta de uma base somente se cumprir os três requisitos:

1. `evidence_level = production_documented`.
2. O mapeamento da base é `exact`.
3. `organization_class = bigtech`.

Uma implantação canônica conta uma vez por base. Quando fontes diferentes descrevem o mesmo sistema, `canonical_case_id` mantém a identidade e evita inflação. O mesmo caso pode sustentar várias entradas distintas, sem se transformar em várias implantações no total de casos únicos.

A lacuna é `max(0, 10 − casos estritos)`. Não significa ausência mundial da aplicação. Consultas, recortes e limites estão em `pesquisa/CONSULTAS_V4.jsonl`. A tabela de cobertura inclui também labs, outros operadores, produtos, pesquisas e correspondências aproximadas.

O campo `deployment_domain` distingue aplicação, serving e treino de LLM, pesquisa/ferramenta para LLM e sistemas sem LLM demonstrada. `verified_bigtech_llm_production_exact` é o subconjunto estrito dos três primeiros domínios. A contagem geral de mecanismos pode incluir MapReduce, bancos e filas em infraestrutura tradicional; não deve ser apresentada como contagem de implantações de LLM. Nem o subconjunto LLM implica porte 3–30B: tamanho e versão precisam de evidência adicional individual.

## Grafos

O grafo caso→base expressa correspondência, não co-uso automático entre todos os temas do caso. O grafo de conexões entre bases exige uma relação individualizada.

Uma conexão `source_documented` deve citar caso operacional, fonte em comum e correspondência exata dos dois mecanismos. A descrição deve indicar o que a fonte efetivamente conecta. O estágio do caso continua visível: produto disponível não vira produção porque a linha é documentada.

O rótulo documenta a combinação delimitada; interfaces sugeridas e testes de aceite são contratos editoriais para adaptação. Eles não se tornam APIs oficiais, configurações exatas da empresa ou ganhos medidos apenas por aparecerem na mesma aresta.

Uma conexão `engineering_proposal` registra ordem, interface, condição e critério de aceite. Ela pode ser sensata e útil sem ainda ter sido implantada. Ausência de linha significa falta de vínculo incluído neste recorte, não incompatibilidade universal.

## Transferência a modelos pequenos

Casos históricos de filas, bancos, compiladores e controle de versão comprovam mecanismos desses sistemas. Sua utilização em agentes 3–30B é apresentada como proposta, exceto quando a fonte documenta explicitamente essa implantação e porte.

Não se infere o número de parâmetros de um modelo a partir do produto. Parâmetros totais e ativos, versão, hardware, adaptador e configuração de decodificação precisam de suporte próprio. Ganho do operador não é ganho medido neste pacote ou no ambiente do usuário.
