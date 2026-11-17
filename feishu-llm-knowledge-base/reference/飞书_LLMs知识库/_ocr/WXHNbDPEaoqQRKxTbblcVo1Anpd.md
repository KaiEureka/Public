$$
\mathrm{FFN}(x) = \mathrm{down\_proj}(\mathrm{SiLU}(\mathrm{gate\_proj}(x)) \odot \mathrm{up\_proj}(x))
$$

**中间层维度设置**：

设模型隐藏维度 $d_{model}$。LLaMA 的 FFN 中间维度（即 `gate_proj` 和 `up_proj` 的输出维度）设置为：

$$
d_{intermediate} = \frac{8}{3} \times d_{model}
$$
