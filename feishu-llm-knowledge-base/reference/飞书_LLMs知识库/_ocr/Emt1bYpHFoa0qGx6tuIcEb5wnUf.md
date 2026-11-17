设输入序列为 $X\in\mathbb{R}^{n\times d_{model}}$，头数为 $h$，每个头的维度 $d_k=d_{model}/h$。

对于第 $i$ 个头：

- 有三个可学习的投影矩阵 $W_Q^{(i)},W_K^{(i)},W_V^{(i)}\in\mathbb{R}^{d_{model}\times d_k}$。
- 投影得到查询、键、值：

$$
Q_i=XW_Q^{(i)},\quad K_i=XW_K^{(i)},\quad V_i=XW_V^{(i)}
$$

- 计算该头的注意力输出：

$$
\text{head}_i=\text{Attention}(Q_i,K_i,V_i)=\text{softmax}\left(\frac{Q_iK_i^T}{\sqrt{d_k}}\right)V_i
$$

所有 $h$ 个头并行计算后，将结果在特征维度上拼接：

$$
\text{MultiHead}(X)=\text{Concat}(\text{head}_1,\ldots,\text{head}_h)W_O
$$

其中 $W_O\in\mathbb{R}^{d_{model}\times d_{model}}$ 是最终的输出投影矩阵。

**工程实现上的等价写法**：
实际代码中通常将 $W_Q,W_K,W_V$ 分别合并为三个大的矩阵 $\in\mathbb{R}^{d_{model}\times hd_k}$，一次性算出所有头的 Q、K、V，再通过 reshape 和 transpose 拆成 $(B,h,n,d_k)$ 的形状，批量进行注意力计算。这样可以利用高度优化的矩阵乘法，所有头完全并行。
