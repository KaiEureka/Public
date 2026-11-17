- 根据即时奖励 $r_t$ 和 Critic 的价值估计 $V(s_t)$，使用 GAE 算法计算出每个 token 的优势函数 $\hat{A}_t$。
- 计算每个 token 的 KL 散度惩罚值。
- 计算出用于 PPO 更新的总目标值：$R_{total} = \hat{A}_t - \beta \cdot \text{KL}$。
- Actor 模型在生成时的对数概率 $\log \pi_{old}$ 会被保存下来，作为计算概率比 $r_t(\theta)$ 的基准。

至此，我们已经构建了一个完整的经验 batch，它包含了：提示、回复、$\log \pi_{old}$、$\hat{A}_t$、以及 Critic 的 $V(s_t)$ 估计等所有信息。
