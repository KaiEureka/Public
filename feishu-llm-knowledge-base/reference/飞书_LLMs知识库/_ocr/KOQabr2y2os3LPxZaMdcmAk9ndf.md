LayerNorm（层归一化）对单个样本的特征维度进行归一化，即对每个 token 的嵌入向量单独归一化。假设输入为 $x \in \mathbb{R}^d$（一个 token 的向量，维度为 $d$），LayerNorm 计算如下：

$$
\mu = \frac{1}{d}\sum_{i=1}^{d} x_i, \quad \sigma^2 = \frac{1}{d}\sum_{i=1}^{d}(x_i - \mu)^2
$$

$$
\hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

$$
y_i = \gamma_i \hat{x}_i + \beta_i
$$

其中 $\mu$ 和 $\sigma^2$ 是沿**特征维度**（即整个向量的所有元素）计算的均值与方差，$\epsilon$ 是防止除零的小常数。$\gamma$ 和 $\beta$ 是与输入同维度的可学习参数，用于恢复变换的表达能力。
