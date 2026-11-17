$$
\mathcal{L}_{total} = \mathcal{L}_{\text{SimPO}}(D_{help}) + \lambda_{safe} \cdot \mathcal{L}_{\text{SimPO}}(D_{safe})
$$

其中：

- $\mathcal{L}_{\text{SimPO}}(D_{help})$ 是在有用性数据上计算的标准 SimPO 损失。
- $\mathcal{L}_{\text{SimPO}}(D_{safe})$ 是在安全性数据上计算的 SimPO 损失，它会鼓励模型提升安全回复（如拒答）的生成概率，并降低不安全回复的概率。
- $\lambda_{safe}$ 是我们为安全性维度设定的权重。通过增大 $\lambda_{safe}$，我们可以显著增强模型的安全对齐行为，即使这可能会稍微牺牲一些在其他任务上的有用性。
