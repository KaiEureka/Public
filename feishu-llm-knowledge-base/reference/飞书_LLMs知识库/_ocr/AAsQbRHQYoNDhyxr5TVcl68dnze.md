$$
y = x + \mathrm{Sublayer}(\mathrm{LayerNorm}(x))
$$

两种形式中，核心都是 `x + Sublayer(...)`，即残差加法。该加法是逐元素的，要求输入和输出的维度一致（均为 $d_{model}$），这由子层内部的投影保证。
