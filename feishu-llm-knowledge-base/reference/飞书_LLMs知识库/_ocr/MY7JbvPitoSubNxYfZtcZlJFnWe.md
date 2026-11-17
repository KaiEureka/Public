$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
$$

其中，$r_t$ 是奖励，$\gamma$ 是折扣因子，$V(s)$ 是 Critic 模型估计的状态价值。

那么，GAE 优势 $\hat{A}_t^{GAE(\gamma,\lambda)}$ 的计算公式如下：

$$
\hat{A}_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}
$$

其中，$\lambda \in [0, 1]$ 是 GAE 的关键参数。当 $\lambda = 0$ 时，$\hat{A}_t = \delta_t$，就是一步 TD 误差，方差最小但偏差最大。当 $\lambda = 1$ 时，$\hat{A}_t = \sum_{l=0}^{\infty} \gamma^l \delta_{t+l} = \sum_{l=0}^{\infty} \gamma^l r_{t+l} - V(s_t)$，这是蒙特卡洛回报，偏差最小但方差最大。在实践中，$\lambda$ 通常取值在 0.95 左右，通过对未来 TD 误差进行衰减加权，显著降低了蒙特卡洛估计的方差，使训练更加稳定高效。
