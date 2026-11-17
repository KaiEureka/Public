**插入方式**：

对于每一层 Transformer，我们会将可训练的前缀参数 $P\in\mathbb{R}^{L\times d}$ 切分为两部分：$P_K$ 和 $P_V$，分别作为 Key 和 Value 的前缀。假设原始输入的 Key 和 Value 矩阵为 $K_{\mathrm{input}}$ 和 $V_{\mathrm{input}}$，则在计算自注意力时，新的 Key 和 Value 矩阵变为：

$$
K'=[P_K;K_{\mathrm{input}}],\quad V'=[P_V;V_{\mathrm{input}}]
$$

而 Query 矩阵 $Q_{\mathrm{input}}$ 保持不变。模型通过注意力机制 $Q_{\mathrm{input}}\cdot K'^T$，使得真实输入中的每个 token 都能“看到”这些额外的前缀 Key，并通过其 Value 来聚合信息。
