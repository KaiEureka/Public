对于一个预训练的权重矩阵 $W_0\in\mathbb{R}^{d\times k}$，LoRA 不直接去优化一个同样尺寸的 $\Delta W$，而是将 $\Delta W$ 分解为两个小矩阵的乘积：

$$
\Delta W=BA
$$

其中，$B\in\mathbb{R}^{d\times r}$，$A\in\mathbb{R}^{r\times k}$，且秩 $r\ll\min(d,k)$。这个 $r$ 就是 LoRA 最核心的超参数——秩（rank）。
