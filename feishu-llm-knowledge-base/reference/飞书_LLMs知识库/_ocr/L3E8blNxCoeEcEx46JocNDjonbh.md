这是最直接、最标准的方法。在 Actor 模型生成的 token 序列上，分别计算参考模型 $\pi_{ref}$ 和当前策略模型 $\pi_\theta$ 的对数概率。然后，直接计算这两个对数概率的差值的数学期望，作为 KL 散度的无偏估计。

$$
\text{KL}(\pi_\theta \| \pi_{ref}) = \mathbb{E}_{y \sim \pi_\theta} \left[ \log \pi_\theta(y|x) - \log \pi_{ref}(y|x) \right]
$$
