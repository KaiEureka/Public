$$
\frac{\partial\mathcal{L}_U}{\partial r}=\lambda_U\cdot\beta\cdot\sigma(-\beta(r-z))
$$

这个梯度始终为**正**。一个正的梯度意味着会**减少**隐式奖励 $r$。同样，梯度大小由 $\sigma(-\beta(r-z))$ 决定：当 $r$ 远高于 $z$ 时，$\sigma$ 接近 1，惩罚力度最大；当 $r$ 远低于 $z$ 时，$\sigma$ 接近 0，模型认为安全，停止惩罚。
