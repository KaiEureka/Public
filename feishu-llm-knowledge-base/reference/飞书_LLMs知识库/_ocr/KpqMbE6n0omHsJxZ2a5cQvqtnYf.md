$$
\mathcal{L}_{\mathrm{MLM}} = -\sum_{i \in \mathcal{M}} \log P_\theta(x_i \mid \tilde{\mathbf{x}}).
$$

实际训练中通常取平均损失：$\mathcal{L} = -\frac{1}{|\mathcal{M}|}\sum_{i \in \mathcal{M}} \log P_\theta(x_i \mid \tilde{\mathbf{x}})$。

**交叉熵损失推导**：对于单个被掩码位置 $i$，模型输出一个 logits 向量 $\mathbf{z}_i = \mathbf{W}\mathbf{h}_i + \mathbf{b}$。经过 softmax 得到概率分布 $\hat{\mathbf{y}}_i = \mathrm{softmax}(\mathbf{z}_i)$，其中 $\hat{y}_{i,v} = \exp(z_{i,v}) / \sum_{v'} \exp(z_{i,v'})$。真实标签为 $x_i$（一个 one-hot 向量，在索引 $x_i$ 处为 1）。该位置的交叉熵损失为：

$$
\ell_i = -\log \hat{y}_{i,x_i}.
$$
