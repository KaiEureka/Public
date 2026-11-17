对 SimPO 损失函数 $\mathcal{L}_{SimPO}=-\log\sigma\left(\beta(\bar{p}_w-\bar{p}_l)-\gamma\right)$ 求关于策略模型参数 $\theta$ 的梯度，可以清晰地揭示其学习机制。

其梯度形式为：

$$
\nabla_\theta\mathcal{L}_{SimPO}=-\underbrace{\left[1-\sigma\left(\beta(\bar{p}_w-\bar{p}_l)-\gamma\right)\right]}_{\text{权重 }w}\cdot\beta\cdot\left(\nabla_\theta\bar{p}_w-\nabla_\theta\bar{p}_l\right)
$$
