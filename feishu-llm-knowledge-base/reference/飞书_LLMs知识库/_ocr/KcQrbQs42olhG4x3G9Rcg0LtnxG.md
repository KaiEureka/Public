**公式**：

$$
\mathrm{FFN}(x) = \mathrm{down\_proj}(\mathrm{SiLU}(\mathrm{gate\_proj}(x)) \odot \mathrm{up\_proj}(x))
$$

其中 $\mathrm{SiLU}(z) = z \cdot \sigma(z)$。

这种门控机制让模型能够动态选择特征，中间维度通常设为 $\frac{8}{3}d_{model}$ 以平衡参数量。
