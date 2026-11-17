- **残差分支缩放**：在残差连接中加入一个固定的小缩放参数 $\alpha$（如 $\alpha = (2N)^{-1/2}$，其中 $N$ 为层数），公式变为：

$$
\mathrm{Output} = \mathrm{LayerNorm}(x + \alpha \cdot \mathrm{Sublayer}(x))
$$
