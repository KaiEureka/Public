$$
\mathrm{Attention}(Q_i, K, V) = \mathrm{softmax}\left(\frac{Q_i K_{i-W+1:i}^T}{\sqrt{d_k}}\right)V_{i-W+1:i}
$$

- 这种局部自注意力将复杂度从 $O(n^2)$ 降至 $O(n \cdot W)$，并极大压缩了 KV 缓存。
