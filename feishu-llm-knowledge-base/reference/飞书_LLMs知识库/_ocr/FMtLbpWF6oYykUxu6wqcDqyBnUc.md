实现上，它把标准的键值投影矩阵 $W_K$ 和 $W_V$ 分解为两个低秩矩阵的乘积：

$$
W_K = W_{down} \cdot W_{up}^K, \quad W_V = W_{down} \cdot W_{up}^V
$$

其中 $W_{down} \in \mathbb{R}^{d_{model} \times d_{latent}}$ 将输入压缩到极低维的潜在向量 $c_{kv}$，$d_{latent} \ll H \times d_k$。推理时只需缓存 $c_{kv}$，而非完整的 K、V。需要使用时，通过上投影 $W_{up}^K, W_{up}^V$ 实时恢复。由于上投影矩阵参数量大（$d_{latent} \times H \times d_k$），表达能力被保留在参数中，缓存则被极限压缩。
