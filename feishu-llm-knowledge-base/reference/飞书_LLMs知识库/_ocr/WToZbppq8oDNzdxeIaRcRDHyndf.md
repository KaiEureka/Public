$$
y = x + \mathrm{Dropout}(\mathrm{Sublayer}(x))
$$

或更完整地（Post-Norm）：

$$
y = \mathrm{LayerNorm}(x + \mathrm{Dropout}(\mathrm{Sublayer}(x)))
$$
