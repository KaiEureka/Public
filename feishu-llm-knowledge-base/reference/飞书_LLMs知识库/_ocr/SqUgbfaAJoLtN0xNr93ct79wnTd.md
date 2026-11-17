$$
\nabla_\theta \mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\beta \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ w(x, y_w, y_l) \cdot \left( \nabla_\theta \log \pi_\theta(y_w|x) - \nabla_\theta \log \pi_\theta(y_l|x) \right) \right]
$$

其中 $w(x, y_w, y_l)$ 是权重项，它本身就依赖于 $\pi_\theta$ 和 $\pi_{\text{ref}}$ 的差值。这个梯度项表明，DPO 的更新方向是同时“提升” $\pi_\theta(y_w|x)$ 和“降低” $\pi_\theta(y_l|x)$。而参考模型 $\pi_{\text{ref}}$ 隐式地出现在权重 $w$ 中，从而影响每次更新的强度。当策略模型试图偏离参考模型太远时，权重项会自适应地调整，形成一个软性的、动态的约束，这比 PPO 中显式的 KL 惩罚更为优雅。
