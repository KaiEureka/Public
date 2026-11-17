3. **从概率到无偏估计**：

上述证明表明，对于一次随机排列 $\pi$，比较两个 MinHash 值是否相等这个**伯努利试验**，其成功的概率就是 Jaccard 相似度。

要得到一个稳定的、准确的 Jaccard 估计值，我们使用 $k$ 个**独立**的随机排列 $\pi_1, \pi_2, ..., \pi_k$。

对每个排列 $\pi_i$，我们计算两个集合的 MinHash 值 $h_i(A)$ 和 $h_i(B)$。

定义一个指示变量 $I_i$：

$$
I_i = \begin{cases} 1, & \text{if } h_i(A) = h_i(B) \\ 0, & \text{otherwise} \end{cases}
$$
