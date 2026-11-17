$$
\begin{cases}
PE_{(pos,2i)} = \sin\left(\dfrac{pos}{10000^{2i/d_{\mathrm{model}}}}\right) \\
PE_{(pos,2i+1)} = \cos\left(\dfrac{pos}{10000^{2i/d_{\mathrm{model}}}}\right)
\end{cases}
$$

其中：

- $pos$ 是 token 在序列中的位置，从 0 开始。
- $i$ 是维度的索引，取值范围 $0, 1, \ldots, \frac{d_{\mathrm{model}}}{2} - 1$，即每个维度对应一个正弦和一个余弦函数。
- $d_{\mathrm{model}}$ 是模型的嵌入维度（例如 512）。
- $10000^{2i/d_{\mathrm{model}}}$ 是频率控制项，它随维度 $i$ 的增加而指数衰减，从而在不同维度上使用不同的波长。
