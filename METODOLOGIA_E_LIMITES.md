# Método, evidência e limites — v4

## Unidade de trabalho

O inventário contém 243 entradas técnicas, variantes, componentes e formatos, preservados em T001–T243. R001–R027 são referências; P001–P017, nomes editoriais de componentes propostos. Total: 287 bases. Não são 287 tecnologias independentes nem 287 implementações prontas.

A v3 foi preservada como referência histórica. Esta edição acrescenta três camadas por base: estratégias para modelos pequenos, casos classificados e conexões com contratos. A comparação de novidade combina revisão editorial e diagnóstico textual; não é prova de novidade científica ou levantamento exaustivo de toda a literatura.

## Pesquisa e proveniência

As consultas executadas estão em `pesquisa/CONSULTAS_V4.jsonl`. Uma busca de família pode abranger vários IDs, quando isso é declarado. A ausência de caso indica que não foi comprovado neste recorte; não prova inexistência mundial.

Fontes técnicas são primárias: artigos dos autores, repositórios oficiais, documentação e relatos dos operadores. `opened` significa conteúdo aberto; `search_result`, resultado de busca examinado; `unverified`, referência ainda não confirmada. Abertura não é auditoria completa de toda afirmação do documento. Conteúdo externo não foi integralmente arquivado.

A consulta ocorreu em 2026-11-05. Datas de evento e de publicação são preservadas quando conhecidas; não se converte uma previsão futura em fato realizado. Documentação atual e descrição histórica de um produto podem tratar revisões diferentes. As fontes têm notas sobre essa limitação.

## Classes que não podem ser misturadas

| Campo | Significado |
|---|---|
| `production_documented` | Fonte do operador/autores descreve implantação ou uso real |
| `operational_product` | Produto ou recurso documentado, sem comprovar uso/escala específica |
| `research_only` | Pesquisa, protótipo ou benchmark; não prova implantação |
| `exact` | O mecanismo desta entrada está explicitamente sustentado |
| `family` | Só uma família próxima é sustentada |
| `analogy` | Comparação útil, sem adoção literal do componente |
| `source_documented` | Combinação descrita em caso operacional com fonte e correspondência |
| `engineering_proposal` | Composição sugerida, ainda não medida neste pacote |

Um caso pode sustentar vários temas sem ser uma implantação nova a cada mapeamento. Casos canônicos evitam dupla contagem quando diferentes relatos cobrem o mesmo sistema. Várias entradas no mesmo caso não geram automaticamente uma aresta de integração entre elas.

P001–P017 só recebem analogias de casos e conexões propostas. Nenhuma fonte comprova que uma empresa utiliza um produto LAI com esses nomes editoriais.

## Dez exemplos por base

A política estrita conta uma implantação canônica por base, com `production_documented`, correspondência `exact` e organização classificada como `bigtech`. Labs de IA e operadores adicionais aparecem separadamente. A classificação organizacional é um recorte explícito desta curadoria, não definição universal de Big Tech.

`producao/COBERTURA_10_POR_BASE.json` registra o total solicitado, os casos encontrados e a lacuna. Não são gerados exemplos fictícios nem preenchidas posições vazias com pesquisa. Uma técnica específica pode não ter dez implantações públicas verificáveis; um componente editorial P não tem adoção literal por definição.

Sistemas de bancos, filas e controle de versão podem comprovar um mecanismo geral em produção sem serem sistemas LLM. A adaptação ao agente e a modelos 3–30B continua identificada como proposta. Não se deduz treinamento, porte do modelo ou desempenho de um sistema a partir de seu fornecedor.

## Grafo e contratos

Cada conexão tem origem, destino, relação, ordem de uso, interface, condição, aceite, fontes e casos quando documentada. Uma relação `requires` vale no cenário descrito, não é dependência universal da técnica. `conflicts` registra uma condição de incompatibilidade, não impossibilidade permanente.

O grafo distingue produção documentada, produto disponível e proposta. Mesmo uma ligação documentada não demonstra que a integração local proposta tenha sido executada. O relatório de integridade verifica referências e classes; a revisão factual examina se a fonte realmente sustenta o vínculo.

## Recuperação sem confundir evidências

C01–C06 preservam o material anterior. C07–C09 são as novas camadas. Metadados e fontes acompanham cada seção; o conjunto de referências não é aplicado indiscriminadamente a todas as afirmações. O texto continua sendo uma síntese editorial, com propostas de engenharia identificadas.

O runtime padrão é lexical. A expansão por caracteres é uma heurística, não compreensão semântica ou confiança calibrada. Filtros de camada reduzem conteúdo irrelevante; o filtro `production` significa seção de evidências, não somente implantações confirmadas. Para estas, use `cases` com os filtros apropriados.

O construtor de contexto usa orçamento de caracteres, inclui somente blocos inteiros e informa omissões. Uma seção grande pode não caber. O usuário deve selecionar a base/camada, ampliar o orçamento quando adequado ou ingerir os arquivos em um pipeline com segmentação avaliada para seu modelo.

## Avaliação executada e avaliação proposta

As 90 perguntas históricas e as 40 perguntas reservadas da v3 já são conhecidas nesta edição. São **regressão local**; não constituem nova avaliação cega. Os parâmetros de busca da v3 foram mantidos. As perguntas didáticas não são usadas como benchmark independente.

Testes do código exercitam validação, filtragem, índices, fontes, citações, montagem e clientes externos simulados. O comparador de sistemas é testado com dados sintéticos temporários. Nenhum desses testes mede qualidade de uma LLM ou ganho GPU.

Protocolos por base, critérios de aceite e comparações com fronteira são propostas. Não houve treinamento, geração real, embeddings reais, instalação na Helena ou execução dos mecanismos descritos. Resultados efetivos ficam em `evidencias/` e no relatório da versão.

## Limites que permanecem

Uma fonte primária pode conter erro, recorte incompleto ou afirmação promocional. A curadoria registra limites e corrige generalizações identificadas; não promete ausência absoluta de erro. Ganhos reportados pelo operador não são ganhos medidos no ambiente do usuário.

A transferência para 3–30B depende de dados, arquitetura, hardware e distribuição das tarefas. Não há prova de paridade geral com modelos de fronteira, de superioridade mundial do acervo ou de que mais componentes necessariamente melhorem um sistema.

Hashes detectam mudanças em arquivos, não certificam verdade. O runtime é uma ferramenta local de consulta, não serviço multiusuário com autenticação e autorização. Texto recuperado é dado, não permissão para executar ações. Memória externa não treina pesos nem garante persistência fora da aplicação que efetivamente guarda os arquivos.

