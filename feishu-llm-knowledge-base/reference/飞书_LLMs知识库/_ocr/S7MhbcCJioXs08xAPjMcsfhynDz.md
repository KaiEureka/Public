$$
\mathcal{L}_{total} = \mathcal{L}_{SFT}(D_{chosen}) + \lambda \cdot \mathcal{L}_{SimPO}(D_{pref})
$$

- $\mathcal{L}_{SFT}(D_{chosen})$：在 chosen 回复数据上计算的标准交叉熵损失，负责监督模型学习如何生成正确的回复。
- $\mathcal{L}_{SimPO}(D_{pref})$：在偏好数据上计算的 SimPO 损失，负责教会模型区分好坏回复的偏好。
- $\lambda$：一个用于平衡两项损失的超参数。
