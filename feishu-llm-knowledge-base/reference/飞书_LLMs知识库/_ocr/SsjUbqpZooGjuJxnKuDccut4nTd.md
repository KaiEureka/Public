$$
h=W_0x+\frac{\alpha}{r}BAx
$$

其中，$x$ 是输入向量，$W_0$ 是冻结的预训练权重矩阵，$A\in\mathbb{R}^{r\times k}$ 和 $B\in\mathbb{R}^{d\times r}$ 是 LoRA 的可训练矩阵，$\alpha$ 是缩放因子，$r$ 是秩。
