**Implicit Reward（隐式奖励）** 是 DPO 推导中自然产生的一个关键概念。它指的是利用策略模型 $\pi_\theta$ 和参考模型 $\pi_{\text{ref}}$ 的对数概率比，可以隐式地表示出当前策略认为一个回复有多“好”。其定义公式为：

$$
\hat{r}_\theta(x, y) = \beta \cdot \log \frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)}
$$
