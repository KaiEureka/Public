对于一个长度为 $T$ 的文本序列 $x = (x_1, x_2, \ldots, x_T)$，模型要学习条件概率 $P(x_t | x_{<t})$，并最小化负对数似然损失：

$$
\mathcal{L}(\theta) = -\frac{1}{T}\sum_{t=1}^{T}\log P_\theta(x_t \mid x_{<t})
$$

其中 $P_\theta(x_t \mid x_{<t})$ 由模型最后一层输出经过 softmax 得到。

在训练时，因果掩码确保每个位置 $t$ 只能利用 $x_1, \ldots, x_{t-1}$ 的信息来预测 $x_t$。损失通常只在非填充 token 上计算。
