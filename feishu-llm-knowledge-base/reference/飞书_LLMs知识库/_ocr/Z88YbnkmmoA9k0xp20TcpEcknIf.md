假设原 MHA 有 $h$ 个查询头，对应的 $h$ 个键权重 $W_K^{\mathrm{MHA}(1)},\ldots,W_K^{\mathrm{MHA}(h)}$ 和值权重 $W_V^{\mathrm{MHA}(1)},\ldots,W_V^{\mathrm{MHA}(h)}$，每个形状 $\mathbb{R}^{d_{\text{model}}\times d_k}$。选择目标分组数 $g$，并将 $h$ 个头划分为 $g$ 组，每组 $h/g$ 个头（通常采用简单的顺序分组，因为头间没有内在顺序，平均效果良好）。对于第 $j$ 组，组内包含索引集合 $\mathcal{S}_j$，初始化 GQA 的键和值权重为组内均值：

$$
W_K^{\mathrm{GQA}(j)}=\frac{1}{|\mathcal{S}_j|}\sum_{i\in\mathcal{S}_j}W_K^{\mathrm{MHA}(i)},\quad W_V^{\mathrm{GQA}(j)}=\frac{1}{|\mathcal{S}_j|}\sum_{i\in\mathcal{S}_j}W_V^{\mathrm{MHA}(i)}
$$

查询权重 $W_Q$ 和输出投影 $W_O$ 完全保留原样。这样我们就得到了一个可以直接运行的 GQA 模型，此时它的困惑度通常仅有轻微上升（例如在 C4 上从 9.0 升到 9.2）。
