LoRA 基于一个关键假设：大模型在适应下游任务时，其权重的更新量 $\Delta W$ 虽然形状和原始权重 $W \in \mathbb{R}^{d \times k}$ 相同，但其**本质上是低秩的**。因此，这个更新量可以用两个小矩阵的乘积来近似表示：

$$
\Delta W = BA
$$

其中 $A \in \mathbb{R}^{d \times r}, B \in \mathbb{R}^{r \times k}$，且秩 $r \ll \min(d, k)$。例如，$r$ 可以设为 8 或 16。
