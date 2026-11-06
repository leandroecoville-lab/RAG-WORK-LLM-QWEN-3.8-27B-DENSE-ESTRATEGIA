# Lista completa atualizada — 243 entradas

206 entradas anteriores + 37 acréscimos. IDs anteriores preservados. São itens de um inventário, não tecnologias independentes: há técnicas, variantes, componentes e formatos.

## Contexto, compressão e recuperação — 46

1. Map-Reduce
2. Prompt Caching
3. Sliding Window de contexto — incluindo descarte FIFO
4. Summarization em cadeia
5. Semantic Caching
6. Context Compression
7. Response Caching por Hash
8. Hierarchical Summarization
9. RAG — Retrieval-Augmented Generation; incluindo RAG temporal
10. Fixed-Size Chunking
11. Semantic Chunking
12. Recursive Chunking
13. Long-Context Models
14. Progressive Disclosure
15. Reference Passing
16. Tool Result Truncation
17. Context Folding
18. Context Pruning
19. Few-Shot Pruning
20. Learned Prompt Compression
21. Context Compression On-the-Fly
22. Instruction Compression
23. Recursive Summarization Tree
24. Context Broker e Context Builder
25. Adaptive RAG
26. Hierarchical Retrieval
27. Hybrid Retrieval — BM25 + vetores
28. Reranking
29. GraphRAG
30. RAPTOR
31. Semantic Cache Invalidation
32. Parent-Child Retrieval / Parent-Child Chunking
33. Structure-Aware Chunking
34. Agentic Chunking
35. Contextual Chunking
36. Query-Aware RAG
37. Query-Aware Compression
38. Selective Context Pruning
39. Importance-Aware Window
40. State-Aware Window
41. Last-N Messages Window
42. Token-Based Window
43. Context Compaction
44. Progressive Context Expansion
45. Tool Retrieval
46. Dynamic Few-Shot Selection

## Memória, persistência e conhecimento — 32

47. Long-Term Memory — memória de longo prazo
48. Memory Management
49. Episodic Memory
50. Working Memory Window
51. Graph-Based Memory
52. Latent Context
53. Scratchpad em arquivo
54. Semantic Memory
55. Procedural Memory
56. Bitemporal Memory
57. Causal Memory
58. Memory Consolidation
59. Event Sourcing
60. Agent Checkpointing / Checkpoint & Resume — incluindo checkpoints transacionais
61. Content-Addressable Storage
62. Hierarchical Memory
63. Virtual Context Management — memória virtual de contexto, estilo MemGPT
64. Persistent Agent State
65. Transactional State Manager
66. Memory Resolver / Reference Resolver
67. Active Memory Retrieval
68. Memory-Augmented Generation
69. Consolidação por resumos — anteriormente chamada de “Context Distillation”
70. Episodic Store
71. Memory Promotion
72. Versioned Memory
73. Immutable Evidence Store
74. Memory Eviction
75. Memory Reconciliation
76. Git-Backed Memory
77. Temporal Knowledge Graphs
78. Semantic Page Fault

**Correção T069:** consolidar sessões em um resumo externo não é destilar contexto nos pesos. A destilação paramétrica permanece em T179.

## Inferência, atenção, GPU e cache — 54

79. Speculative Decoding
80. Adaptive Speculative Decoding
81. KV Cache Reuse
82. Prefix Caching
83. Advanced Prefix Caching
84. Session-Based Caching
85. Quantization
86. Quantized KV Cache
87. Batching — Static Batching e Dynamic Batching
88. Continuous Batching
89. Early Stopping — EOS, stop sequences, limites e parada semântica
90. FlashAttention
91. FlashAttention-2
92. FlashAttention-3
93. PagedAttention
94. Chunked Prefill
95. Sliding Window Attention
96. Sparse Attention
97. Block-Sparse Attention
98. Memory-Efficient Attention
99. Multi-Query Attention — MQA
100. Grouped-Query Attention — GQA
101. Ring Attention
102. Disaggregated Inference / Disaggregated Prefill-Decode
103. Prefix Tree / Trie de prefixos
104. Radix Attention
105. KV Cache Eviction
106. Otimização de KV com MQA/GQA
107. Roofline Analysis
108. Multi-Head Attention — MHA
109. Local / Window Attention
110. Global Token Attention
111. Dynamic Sparse Attention
112. Retrieval-Based Attention
113. FlashAttention Tiling
114. Online Softmax
115. Activation Checkpointing
116. KV Cache Recomputation
117. Context Parallelism
118. Tensor Parallelism
119. Pipeline Parallelism
120. KV Cache Routing
121. GPU Scheduling
122. RDMA para inferência distribuída
123. FP8 Quantization
124. INT4 / W4A16 Quantization
125. GPTQ
126. AWQ
127. GGUF — formato de modelos, não método único de quantização
128. EAGLE / EAGLE-3
129. MTP — Multi-Token Prediction
130. N-Gram Speculative Decoding
131. Suffix Decoding
132. Draft-Model Speculation

## Orquestração, execução e resiliência — 44

133. Model Routing
134. Semantic Routing
135. Model Cascade
136. Fallback Chains
137. Rate Limiting
138. Circuit Breaker
139. Parallel Tool Calls
140. Tool Use / Function Calling
141. Structured Outputs
142. Agent Frameworks com Planning
143. Plan-Then-Act
144. ReAct Pattern
145. Adaptive Depth
146. Adaptive Compute
147. Parallel Fan-Out
148. Conditional Branching
149. Priority Queue
150. Request Coalescing / Singleflight
151. Lazy Loading de ferramentas
152. Token Budget Allocation
153. Output Streaming com interrupção
154. Multi-Turn Conversation Management
155. System Prompt Optimization / prompt de sistema enxuto
156. Temperature Tuning
157. Prefix Hashing
158. Tool Registry
159. Durable Execution
160. DAG Scheduling
161. Critical Path Analysis
162. Idempotência
163. Backoff exponencial com jitter
164. Retry-After
165. Half-open — estado do Circuit Breaker
166. Queue Fairness / Aging
167. Token Bucket
168. Soft Limit / Hard Limit de tokens
169. Multi-Agent com contextos isolados
170. Tool Schema Versioning
171. Cache-Aware Orchestration
172. Streaming Controller
173. Model Fallback Controlado
174. Priority-Based Scheduling
175. Rate Limiting com Fallback
176. Token-Aware Planning

## Verificação, treinamento e especialização — 30

177. Fine-Tuning
178. Knowledge Distillation
179. Context Distillation Paramétrica
180. Prompt Distillation
181. Agent Memory Distillation
182. LoRA
183. QLoRA
184. Mixture of Experts — MoE
185. Constitutional AI
186. Debate entre agentes
187. Ensemble Voting
188. Self-Consistency
189. Best-of-N Verification
190. Verifier Loop
191. Chain-of-Verification
192. Self-Refine
193. Guardrails
194. Process Supervision
195. Verificação baseada em execução
196. Constrained Decoding / Grammar-Constrained Decoding
197. JSON Schema Validation
198. Calibrated Confidence
199. Aprendizagem por avaliação
200. Independent Verification
201. Agent Test-Time Scaling
202. Uncertainty-Aware Planning
203. Correctness-Based Routing
204. Skills / Procedural Learning
205. Semantic Equivalence Testing
206. Process Verification

## Continuidade, programação e controle operacional — 37

207. Memory Stream
208. Planner–Executor / Plan-and-Execute
209. Reflexion
210. Session Rotation
211. Handoff File
212. Auto-Compact por gatilho
213. Task Decomposition em micro-missões
214. Tool Output Pruning
215. Observation Masking
216. Repo Map / mapa do repositório
217. Test-Driven Loop
218. Loop Detection / detecção de estagnação e ciclos
219. Limite de recursão / profundidade de execução
220. Tool Call Repair
221. Goal Reminder Injection
222. Context Budget Monitor
223. Constitutional Self-Check
224. Spec-Driven Loop
225. Watchdog com Auto-Restart
226. Heartbeat de progresso
227. Health Checks — liveness, readiness e progresso
228. Fila de retries com backoff exponencial
229. Diff-Only Editing / Patch-Based Coding
230. Unified Diff
231. Search/Replace Editing
232. AST Editing
233. Patch Validation — incluindo verificação de hash-base
234. Persistent Project Memory File — incluindo memória por módulo
235. Headless Mode em loop / Headless Controller
236. Git Commit por etapa
237. Subagent Offloading
238. Read On Demand com faixa de linhas
239. Git Worktrees
240. Snapshot de estado
241. Event Replay
242. Recuperação híbrida por Snapshot + Event Sourcing
243. Reconciliação de operações externas

## Pesquisas, projetos e tecnologias de referência — 27

Fora da contagem de 243 entradas principais.

- **R001** — MemGPT
- **R002** — Letta
- **R003** — LongMem
- **R004** — Generative Agents
- **R005** — LLMLingua
- **R006** — PRISM
- **R007** — SADA
- **R008** — LangGraph
- **R009** — vLLM
- **R010** — Hugging Face TGI
- **R011** — NVIDIA TensorRT-LLM
- **R012** — Tinker — Prompt Distillation
- **R013** — Letta MemFS
- **R014** — Letta Context Repositories
- **R015** — Learning by Distilling Context
- **R016** — Lost in the Middle
- **R017** — LangChain
- **R018** — Temporal
- **R019** — Aider
- **R020** — Claude Code
- **R021** — OpenAI Codex
- **R022** — Qwen
- **R023** — Hugging Face Transformers
- **R024** — llama.cpp
- **R025** — XGrammar
- **R026** — Guidance
- **R027** — Git

## Componentes arquiteturais propostos — 17

Fora da contagem de 243 entradas principais.

- **P001** — Context Engine
- **P002** — Context Manager
- **P003** — Virtual Context Manager
- **P004** — LAI Memory Runtime
- **P005** — Context & Memory Controller
- **P006** — Progressive Loader
- **P007** — Memory Retriever
- **P008** — Event Store / Event Log
- **P009** — Inference Engine
- **P010** — Routing Engine
- **P011** — Execution Engine / Execution Controller
- **P012** — Verification Engine / Verification Controller
- **P013** — Resilience Engine / Reliability Controller
- **P014** — Execution Resilience
- **P015** — Execution Integrity Controller
- **P016** — Evaluation Engine
- **P017** — Distillation Pipeline

