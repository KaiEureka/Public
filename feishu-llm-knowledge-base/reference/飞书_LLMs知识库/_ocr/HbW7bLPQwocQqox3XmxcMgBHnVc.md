1. **累积注意力分数的维护（逐头）**

对于每一个注意力头，维护一个与当前序列长度 $t$ 同步增长的累积分数向量 $\mathbf{a}\in\mathbb{R}^t$，初始化为全零。每一步（每生成一个新 token），当前查询 $Q$ 与所有历史键 $K$ 计算得到原始注意力权重 $\alpha\in\mathbb{R}^t$（softmax 之后）。将 $\alpha$ 直接累加到历史累积分数上：

$$
\mathbf{a}\leftarrow\mathbf{a}+\alpha
$$
