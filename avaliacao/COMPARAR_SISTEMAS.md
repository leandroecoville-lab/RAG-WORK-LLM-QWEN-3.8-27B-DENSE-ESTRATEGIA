# Avaliar um sistema 3–30B frente a um baseline

O programa `runtime/compare_systems.py` analisa **observações já coletadas**. Ele não chama LLMs, não avalia a verdade das respostas e não preenche resultados ausentes. Nenhum benchmark real de modelo foi executado na criação deste pacote.

## Desenho antes da coleta

Escolha tarefas representativas do seu tráfego. Separe treino, desenvolvimento e avaliação final por origem, tempo e família quando houver dependência. Congele os critérios de sucesso, o baseline e a margem aceitável antes de examinar o conjunto final. Documente exceções e recursos adicionais usados por cada sistema.

O candidato declara **3–30B parâmetros totais**. Parâmetros ativos de MoE são registrados separadamente. A designação de fronteira do baseline é uma decisão externa: o script não determina qual modelo é o melhor do mercado.

Pareie a mesma tarefa e repetição entre candidato e baseline. `cluster_id` representa uma unidade de dependência, como documento de origem ou família de problema; variações muito semelhantes não devem ser apresentadas como amostras independentes. O bootstrap por cluster preserva essas dependências declaradas. Sua validade ainda depende de desenho de amostragem adequado.

## Configuração

Copie `configuracao_exemplo.json` e substitua todas as identidades ilustrativas. Os números de limite são **exemplos de configuração**, não recomendação universal ou resultado observado. `quality_margin=0.02`, por exemplo, significa aceitar uma perda de até dois pontos percentuais no critério de sucesso declarado; pode ser inadequado para sua tarefa.

Os custos amortizados por requisição devem vir de uma hipótese explícita de volume. Registre treino, professor, engenharia recorrente e infraestrutura conforme a contabilidade adotada, evitando comparar uma GPU já paga com um serviço de nuvem como se a primeira fosse gratuita.

## Uma linha por execução observada

O arquivo JSONL contém exatamente estes campos:

| Campo | Conteúdo |
|---|---|
| `task_id` | Identidade estável da tarefa |
| `trial_id` | Identidade da repetição, pareada entre sistemas |
| `cluster_id` | Grupo de dependência da amostra |
| `system_id` | ID declarado para candidato ou baseline |
| `success` | Booleano resultante da regra de aceite previamente definida |
| `critical_failure` | Booleano; não pode coexistir com `success=true` |
| `latency_ms` | Latência de ponta a ponta, incluindo espera e retries |
| `runtime_cost_usd` | Custo variável total da execução, incluindo ferramentas e escaladas |
| `input_tokens`, `output_tokens` | Contagens inteiras, sob convenção declarada |
| `evidence_uri` | Referência ao trace/resultado que permite auditar o rótulo |

Não elimine timeouts, respostas abstidas ou tentativas caras. Se a tarefa não cumpriu seu contrato, preserve a falha no conjunto. Tokens de tokenizers diferentes não são uma medida universal de trabalho; o script apenas os agrega, sem convertê-los em preço.

```bash
python3 runtime/compare_systems.py \
  --config avaliacao/minha_configuracao.json \
  --observations avaliacao/minhas_observacoes.jsonl \
  --out avaliacao/meu_resultado.json
```

## O que o relatório calcula

- Taxa de sucesso e falhas críticas observadas por sistema.
- Latência p50 e p95 pelo método de posto mais próximo.
- Custo total e custo por resultado aceito; o segundo é indefinido se não houve aceites.
- Diferença pareada de sucesso, candidato menos baseline.
- Intervalo aproximado de 95% por bootstrap dos clusters declarados, com semente reproduzível.
- Verificação dos limites de amostra, margem de qualidade, custo, latência e falhas.

O estado `criteria_met_on_this_dataset` significa apenas que os limites declarados foram atendidos nos dados fornecidos. Não significa equivalência geral, ganho causal de um componente, segurança estatística de toda subpopulação ou produção já validada. Os hashes identificam configuração e observações, mas não provam que o protocolo foi registrado antes da coleta.

## Revisões necessárias fora do script

Audite uma amostra dos rótulos e estime divergência entre avaliadores. Examine resultados por idioma, tarefa, tamanho do contexto e dificuldade. Compare a arquitetura completa e suas ablações. Um intervalo agregado pode esconder um subgrupo com regressão grave.

Não há intervalo de confiança para as razões de custo e p95 nesta versão. Poucos clusters tornam o bootstrap instável. Ausência de falhas críticas observadas não demonstra risco zero. O número mínimo de clusters da configuração é um bloqueio operacional, não um cálculo universal de poder estatístico.

Os testes do programa usam dados sintéticos temporários para verificar fórmulas, validação e pareamento. Esses testes não entram no catálogo de exemplos de produção.
