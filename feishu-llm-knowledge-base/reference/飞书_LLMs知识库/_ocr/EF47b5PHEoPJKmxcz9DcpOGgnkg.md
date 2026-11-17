$$
\mathcal{L} = \mathcal{L}_{PPO} - \beta \cdot \mathcal{L}_{KL} + \gamma \cdot \mathcal{L}_{PTX}
$$

下面详细解释每一项：

**1. PPO 损失（$\mathcal{L}_{PPO}$）**

这是 PPO 算法的核心，驱动策略模型去获得更高的奖励。

$$
\mathcal{L}_{PPO} = \mathbb{E}_{(x,y) \sim \pi_\theta}\left[\min\left(r(\theta) \cdot A_t, \mathrm{clip}(r(\theta), 1-\epsilon, 1+\epsilon) \cdot A_t\right)\right]
$$

- **优势函数 $A_t$**：衡量在状态 $t$ 下，采取动作 $y_t$ 相比当前策略平均水平的优势。它由 Critic 模型和 Reward Model 共同计算。$A_t > 0$ 表示该动作优于平均水平，应该鼓励。
- **概率比 $r(\theta)$**：新策略 $\pi_\theta$ 与旧策略 $\pi_{\theta_{old}}$ 在生成 token $y_t$ 的概率之比。$r(\theta) = \frac{\pi_\theta(y_t|x, y_{<t})}{\pi_{\theta_{old}}(y_t|x, y_{<t})}$。
- **裁剪（Clip）机制**：这是 PPO 的精髓。通过 `clip` 函数和 `min` 函数，算法确保了当 $A_t > 0$ 时，不会让概率比 $r(\theta)$ 无限制增大（防止步子迈得太大）；当 $A_t < 0$ 时，不会让概率比无限制减小。这种保守的更新策略保证了训练的稳定性。
