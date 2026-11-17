具体做法是，对于每个生成的 token $y_t$，其调整后的奖励 $\tilde{r}_t$ 定义为：

$$
\tilde{r}_t = r_t - \beta \cdot \left( \log \pi_\theta(y_t|x, y_{<t}) - \log \pi_{ref}(y_t|x, y_{<t}) \right)
$$

然后将 $\tilde{r}_t$ 作为新的奖励值，用于后续 GAE 优势函数的计算中。这种方法在数学上与方式一等价，因为它改变了奖励，进而改变了优势估计，最终的梯度更新方向是一致的。在一些 RLHF 的实现中，这种方式更便于与现有的 PPO 代码库集成。
