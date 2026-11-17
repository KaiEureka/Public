1. 将序列输入模型，得到每个时间步的 logits $\mathbf{z}_t \in \mathbb{R}^V$。
2. 使用 softmax 计算概率：$\hat{y}_t = \mathrm{softmax}(\mathbf{z}_t)$。
3. 提取目标 token $x_t$ 的概率 $p_t = \hat{y}_{t,x_t}$。
4. 计算平均负对数似然：$\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log p_t$。
5. 困惑度 $\mathrm{PPL} = \exp(\mathcal{L})$。
