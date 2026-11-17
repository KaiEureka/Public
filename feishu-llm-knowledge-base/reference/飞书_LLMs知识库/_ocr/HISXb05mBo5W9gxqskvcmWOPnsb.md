$$
\mathcal{L}(\theta) = -\frac{1}{T}\sum_{t=1}^{T} \log P_\theta(x_t \mid x_{<t}),
$$

其中 $P_\theta(x_t \mid x_{<t})$ 是模型在参数 $\theta$ 下，给定历史 $x_{<t}$ 预测 $x_t$ 的条件概率。通常我们会累加整个批次的损失并取平均。在实现中，模型最后一层输出 logits $\mathbf{z}_t \in \mathbb{R}^V$（$V$ 为词汇量大小），经过 softmax 得到概率分布 $\hat{y}_t = \mathrm{softmax}(\mathbf{z}_t)$，则 $P_\theta(x_t \mid x_{<t}) = \hat{y}_{t,x_t}$。损失函数等价于：

$$
\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log \hat{y}_{t,x_t},
$$
