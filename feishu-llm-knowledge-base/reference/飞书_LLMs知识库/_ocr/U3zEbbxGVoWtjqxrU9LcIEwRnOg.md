$$
y_i=\frac{\phi(q_i^{(dec)})^T\sum_j\phi(k_j^{(enc)})v_j^{(enc)T}}{\phi(q_i^{(dec)})^T\sum_j\phi(k_j^{(enc)})}
$$

**独特优势**：

- **源序列的固定状态**：编码器的输出 `K_enc` 和 `V_enc` 是一次性生成的。在线性交叉注意力中，可以预先计算好一个固定大小的“源状态矩阵” $S_{enc}=\sum_j\phi(k_j)v_j^T$ 和归一化向量 $Z_{enc}=\sum_j\phi(k_j)$。无论源序列多长，解码器都只需访问这个固定的状态，解码复杂度与源长度无关。
