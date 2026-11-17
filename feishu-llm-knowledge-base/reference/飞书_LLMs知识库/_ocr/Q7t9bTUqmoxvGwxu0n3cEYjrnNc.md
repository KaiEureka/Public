ORPO 被称为“无参考”（reference-free）的对齐方法，其根本原因在于，它的损失函数中**不存在一个独立的、需要被冻结的参考模型（$\pi_{\text{ref}}$）**。

在 DPO 和 RLHF (PPO) 中，参考模型是必不可少的组件：

- **在 DPO 中**，参考模型用来计算隐式奖励 $r = \beta \cdot \log \frac{\pi_\theta}{\pi_{\text{ref}}}$，为策略模型的更新提供基准。
- **在 RLHF 中**，参考模型（$\pi_{\text{ref}}$）被用来计算 KL 散度惩罚项，防止策略模型偏离太远。
