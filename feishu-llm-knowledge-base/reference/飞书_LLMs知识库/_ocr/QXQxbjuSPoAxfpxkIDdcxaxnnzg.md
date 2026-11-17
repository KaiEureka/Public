1. **RLHF 的 PPO 目标函数**：在 RLHF 中，我们的目标是最大化奖励模型给出的分数，同时最小化与参考模型 $\pi_{\text{ref}}$ 的 KL 散度。

$$
\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(y|x)} \left[ r_\phi(x, y) \right] - \beta \cdot \text{KL} \left( \pi_\theta(y|x) \| \pi_{\text{ref}}(y|x) \right)
$$

2. **该目标函数存在解析解**：通过变分法可以证明，这个带 KL 约束的奖励最大化问题，其最优策略 $\pi^*(y|x)$ 具有以下封闭形式：

$$
\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp \left( \frac{1}{\beta} r_\phi(x, y) \right)
$$
