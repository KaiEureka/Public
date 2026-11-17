1. **隐式奖励** $r_\theta$：$r_\theta(x,y)=\beta\cdot\log\frac{\pi_\theta(y|x)}{\pi_{\mathrm{ref}}(y|x)}$。它衡量的是，相较于参考模型 $\pi_{\mathrm{ref}}$，当前策略模型 $\pi_\theta$ 在多大程度上“更偏好”生成这个回复 $y$。
2. **参考点** $z_{\mathrm{ref}}$：这是一个核心参数，代表“中性”奖励的基准。通常，$z_{\mathrm{ref}}$ 被设置为数据集中所有回复的平均隐式奖励，或者简单地设为 0。它的作用是为“好/坏”的判断提供一个“锚点”。
3. **对 Desirable 样本的处理**：损失函数 $\mathcal{L}_D$ 的形式是 $-\log\sigma(\beta(r_\theta-z_{\mathrm{ref}}))$。我们希望最小化这个损失，就需要最大化 $\sigma(\beta(r_\theta-z_{\mathrm{ref}}))$，即最大化 $r_\theta-z_{\mathrm{ref}}$。换句话说，模型被鼓励去**提升好回复的隐式奖励，使其远高于参考点**。
4. **对 Undesirable 样本的处理**：损失函数 $\mathcal{L}_U$ 的形式是 $-\log\sigma(-\beta(r_\theta-z_{\mathrm{ref}}))$。我们希望最小化它，就需要最大化 $\sigma(-\beta(r_\theta-z_{\mathrm{ref}}))$，即最小化 $r_\theta-z_{\mathrm{ref}}$。换句话说，模型被鼓励去**降低坏回复的隐式奖励，使其远低于参考点**。
5. **不对称权重** $\lambda_D,\lambda_U$：这两个超参数允许我们对 desirable 和 undesirable 样本施加不同强度的优化。根据前景理论的“损失厌恶”，我们通常会设置 $\lambda_U>\lambda_D$，这意味着模型因为生成一个“坏回复”而受到的惩罚，要大于它因为生成一个“好回复”而获得的奖励。这能更有效地塑造模型的“底线”。
