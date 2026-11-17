$$
\mathcal{L}_{total} = \mathcal{L}_{SFT} + \lambda_{help} \cdot \mathcal{L}_{OR}^{help} + \lambda_{safe} \cdot \mathcal{L}_{OR}^{safe} + \lambda_{concise} \cdot \mathcal{L}_{OR}^{concise}
$$

通过调整各个维度的 $\lambda$ 权重，我们可以精确地控制模型在这些维度上的表现。例如，提高 $\lambda_{safe}$ 可以增强模型的安全性，即使这可能会稍微降低有用性的优化强度。
