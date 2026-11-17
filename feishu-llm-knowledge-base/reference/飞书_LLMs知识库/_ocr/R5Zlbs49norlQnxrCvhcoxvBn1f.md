$$
\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V,
$$

其中 $Q, K, V \in \mathbb{R}^{T \times d_k}$ 分别是查询、键、值矩阵，$M$ 是掩码矩阵，$T$ 为序列长度。掩码 $M$ 的作用是：对于位置 $i$（查询），它只能关注位置 $j \le i$（键）。因此，对于 $j > i$ 的位置，我们希望注意力权重为 0。
