缩放因子 $\alpha$ 及其与秩 $r$ 结合使用的缩放规则 $\frac{\alpha}{r}$，是 LoRA 能够在不同秩下保持稳定、减少重调参的关键设计。

**1. α 的作用：一个独立于 r 的学习率调节器**

LoRA 的前向传播为 $h=W_0x+\frac{\alpha}{r}BAx$。这里的 $\alpha$ 可以看作是一个**作用于 LoRA 分支的独立学习率缩放因子**。当我们调整秩 $r$ 时，如果不引入 $\alpha$，那么 $BAx$ 的输出范数会随着 $r$ 的变化而剧烈波动。这是因为 $B\in\mathbb{R}^{d\times r}$ 和 $A\in\mathbb{R}^{r\times k}$ 的矩阵乘积的期望范数与 $r$ 直接相关。
