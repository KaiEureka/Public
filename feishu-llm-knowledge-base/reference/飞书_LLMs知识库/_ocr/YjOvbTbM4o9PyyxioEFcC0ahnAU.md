- **作用**：这是 PPO 目标函数中的一个正则化项。它衡量当前策略模型 $\pi_\theta$ 与参考模型 $\pi_{\mathrm{ref}}$ 之间的差异。
- **为什么是减号**：我们希望在最大化 PPO 目标（获得高奖励）的同时，最小化 KL 散度（保持在参考模型附近）。因此，在总目标函数中，KL 散度项前面有一个负号（或者说，我们加上一个负的KL散度）。系数 $\beta$ 用于控制惩罚的强度。这个惩罚防止了模型过度优化奖励而偏离太远。

**3. 预训练梯度（$\mathcal{L}_{PTX}$）**

$$
\mathcal{L}_{PTX} = \mathbb{E}_{(x,y) \sim \mathcal{D}_{pretrain}}\left[\log \pi_\theta(y|x)\right]
$$
