| 特性 | GQA | MLA |
| --- | --- | --- |
| **压缩机制** | 减少 KV 头数，组内共享 | 低秩压缩 KV 向量维度 |
| **缓存大小** | $2 \times L \times G \times S \times d_k$ | $2 \times L \times S \times d_{latent}$（远小于 GQA 在 G 较小的情况） |
| **多样性保留** | 组数越多，多样性越高 | 潜在空间设计得当可保留丰富语义，且不受头数限制 |
| **训练与实现复杂度** | 相对简单，已广泛支持 | 较复杂，需要对现有注意力内核进行深度定制 |
| **代表模型** | LLaMA-2/3, Mixtral, Qwen2.5 | DeepSeek-V2/V3 |
