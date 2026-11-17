KL 散度衡量了两个概率分布之间的差异。在这里，它衡量的是 Actor 模型当前的策略分布 $\pi_\theta$ 与 Reference 模型原有的策略分布 $\pi_{\mathrm{ref}}$ 之间的差异。

$$
KL\left(\pi_\theta \| \pi_{\mathrm{ref}}\right) = \mathbb{E}_{y \sim \pi_\theta}\left[\log \pi_\theta(y|x) - \log \pi_{\mathrm{ref}}(y|x)\right]
$$
