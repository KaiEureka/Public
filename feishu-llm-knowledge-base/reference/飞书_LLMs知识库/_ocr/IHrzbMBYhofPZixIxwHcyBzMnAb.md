PPO 的优化目标是最大化 $\mathbb{E}[r(x,y)]-\beta\cdot\mathrm{KL}(\pi_\theta||\pi_{\mathrm{ref}})$。其代理目标函数的梯度形式（简化）为：

$$
\nabla_\theta\mathcal{L}_{\mathrm{PPO}}\propto\mathbb{E}\left[\nabla_\theta\log\pi_\theta(y|x)\cdot A(x,y)\right]-\beta\cdot\nabla_\theta\mathrm{KL}(\pi_\theta||\pi_{\mathrm{ref}})
$$

其中，KL 散度的梯度 $\nabla_\theta\mathrm{KL}\approx\nabla_\theta\log\pi_\theta(y|x)$（忽略常数项）。因此，在 PPO 的每个更新步中，都会从奖励的梯度中**减去**一个由 $\beta$ 控制的、指向 $\nabla_\theta\log\pi_\theta(y|x)$ 的梯度项。这是一个**显式的、加法性的惩罚**，直接作用于参数更新。

**DPO 的隐式 KL 约束与梯度**：

DPO 的损失函数为 $-\log\sigma\left(\beta\cdot\log\frac{\pi_\theta(y_w)}{\pi_{\mathrm{ref}}(y_w)}-\beta\cdot\log\frac{\pi_\theta(y_l)}{\pi_{\mathrm{ref}}(y_l)}\right)$。其梯度形式为：

$$
\nabla_\theta\mathcal{L}_{\mathrm{DPO}}\propto-\mathbb{E}\left[w(x,y_w,y_l)\cdot\left(\nabla_\theta\log\pi_\theta(y_w|x)-\nabla_\theta\log\pi_\theta(y_l|x)\right)\right]
$$
