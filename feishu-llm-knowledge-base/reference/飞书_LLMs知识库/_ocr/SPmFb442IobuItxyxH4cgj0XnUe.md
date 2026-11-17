FlashAttention 的加速效果在 prefill 和 decode 阶段有明显差异，根源在于**注意力计算的形状和瓶颈性质不同。**

- **Prefill 阶段**：一次性处理整个输入序列（长度为 $N_p$）。查询和键值序列长度相同，注意力矩阵为 $[N_p,N_p]$，计算是平方复杂度，且因矩阵大，**内存瓶颈严重**。FlashAttention 通过避免写出 $N_p\times N_p$ 的中间矩阵，极大减少了 HBM 读写，加速显著，通常可以比标准实现快 2-8 倍，且显存节省明显（线性于 N 而非 N²）。
- **Decode 阶段**：自回归生成，每次仅处理一个 token（查询长度 $N_q=1$），但键值缓存长度 $N_{kv}$ 逐渐增大。注意力矩阵形状为 $[1,N_{kv}]$，是一个**向量-矩阵乘法**。此时计算量本身很小（$O(N_{kv}d)$），操作强度（FLOP/Byte）极低，**内存带宽是绝对瓶颈**。标准实现中，需要从 KV Cache 读取所有的 K 和 V，与单个 Q 计算，然后写入输出。FlashAttention 在 decode 时，依然采用分块：将 K, V 分成块逐一与 Q 块计算。由于 Q 只有 1 个 token，分块带来的好处不是避免写出注意力矩阵（它本来就极小），而是通过分块来**更好地利用 SRAM 数据复用**，减少对 HBM 的读取次数？但实际上，decode 时标准实现已经不需要写回注意力矩阵，主要成本就是读取整个 KV Cache。FlashAttention 在 decode 的加速相对较小，往往只有 20%-50% 的改善，远不如 prefill 显著。甚至在某些实现中，标准 PyTorch 的 `scaled_dot_product_attention` 在 decode 时调用的优化 kernel 与 FlashAttention 性能相似。

**总结差异原因**：

- Prefill 是计算密集且内存巨大，FlashAttention 消除 N² 中间量，是决定性的。
