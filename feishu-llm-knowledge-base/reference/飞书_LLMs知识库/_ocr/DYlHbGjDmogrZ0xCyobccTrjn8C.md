MHA 为每个头 $i$ 都有独立的 $W_K^i,W_V^i$（形状 $[d_{\text{model}},d_k]$）。若要将它们转换为 GQA 的 $g$ 个 KV 头，需要把原始的 $h$ 个 KV 头划分为 $g$ 组，每组包含 $h/g$ 个原始的 KV 头。对于第 $j$ 组，其对应的 GQA 权重就是组内所有原始权重的均值：

$$
W_K^{\mathrm{GQA}(j)}=\frac{1}{h/g}\sum_{i\in\mathrm{Group}_j}W_K^{\mathrm{MHA}(i)},\quad W_V^{\mathrm{GQA}(j)}=\frac{1}{h/g}\sum_{i\in\mathrm{Group}_j}W_V^{\mathrm{MHA}(i)}
$$

查询权重 $W_Q^i$ 保持不变，因为 GQA 仍然保持原有的 $h$ 个查询头。输出投影 $W_O$ 也原样保留。
