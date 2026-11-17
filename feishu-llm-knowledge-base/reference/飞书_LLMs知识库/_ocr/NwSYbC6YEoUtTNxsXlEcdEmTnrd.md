1. **计算总显存预算**
   - GPU 总显存 $M_{\text{total}}$。
   - 减去模型权重占用 $M_{\text{weights}}$（例如 FP16 下：参数量 × 2 bytes，若使用量化则按量化后大小）。
   - 减去其他固定开销（如 CUDA context、中间激活缓冲区等）$M_{\text{other}}$（通常预留 1~3 GB）。
   - 可用于 KV Cache 的显存预算 $M_{\text{kv}}=M_{\text{total}}-M_{\text{weights}}-M_{\text{other}}$。
2. **计算单个 token 的 KV Cache 大小**

每个 token 每层的 KV 缓存为 $2\times\text{num\_kv\_heads}\times\text{head\_dim}\times\text{dtype\_size}$。

总大小 $C_{\text{token}}=L\times2\times\text{num\_kv\_heads}\times\text{head\_dim}\times\text{dtype\_size}$。

例如 LLaMA-2 7B：L=32, num_kv_heads=32, head_dim=128, FP16 → $32\times2\times32\times128\times2=524,288$ bytes $\approx0.5$ MB/token。
3. **设定平均序列长度**

需要预估平均每个请求的序列长度 $L_{\text{avg}}$（prompt + 生成）。这是经验值，例如在线服务中平均可能为 500 token。同时考虑最大长度 $L_{\max}$ 用于安全边界。
4. **计算最大并发序列数**
   - 若使用 PagedAttention（块大小为 $B$），需要考虑内部碎片。简单估算：每个请求占用的平均块数 $=\lceil L_{\text{avg}}/B\rceil$，每块大小 $C_{\text{block}}=B\times C_{\text{token}}$。
   - 则 $\text{max\_seqs}\approx M_{\text{kv}}/(C_{\text{block}}\times\lceil L_{\text{avg}}/B\rceil)$。
   - 更保守：直接按最大允许长度 $L_{\max}$ 计算，保证任何请求都不会因显存不足而失败，但会大幅限制并发数。更好的方式是允许超配，依靠抢占来动态平衡，因此 `max_num_seqs` 可设置得比保守估算更高。
5. **实际调优**
   - 初始设定一个经验值，运行典型负载，监控峰值显存使用率。逐步提高 `max_num_seqs` 直到接近显存上限，并设置一定余量（如使用率不超过 90%）。
   - 许多框架会动态管理，实际并发数受实时可用块数限制，`max_num_seqs` 只是一个硬顶。
