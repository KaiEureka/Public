**完全正确，前提是 $d_k=d_{model}/h$ 不变。**

**推导**：

- 对于单个头 $i$：$W_Q^{(i)},W_K^{(i)},W_V^{(i)}$ 都是 $d_{model}\times d_k$ 的矩阵。
- 单个头的参数量 = $3\times d_{model}\times d_k$。
- 所有 $h$ 个头的参数量 = $h\times3\times d_{model}\times d_k$。
- 由于 $d_k=d_{model}/h$，代入得：$h\times3\times d_{model}\times(d_{model}/h)=3\times d_{model}^2$。

**结论**：投影矩阵部分的总参数量是常数 $3d_{model}^2$，与 $h$ 无关。输出投影 $W_O$ 的大小是 $d_{model}\times d_{model}$，也与 $h$ 无关。
