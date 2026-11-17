- $f_e$ = 分配给专家 $e$ 的 token 的比例（实际路由到该专家的 token 数 / 总 token 数）。
- $P_e$ = 专家 $e$ 的平均门控概率（对分配到它的 token 的 softmax 概率取平均）。

负载均衡损失通常为：

$$
\mathcal{L}_{\mathrm{aux}} = \alpha \cdot E \cdot \sum_{e=1}^{E} f_e \cdot P_e
$$

其中 $\alpha$ 是一个超参数（例如 0.01），$E$ 为专家数。这个损失惩罚那些门控概率高且分配 token 多的专家，促使它们降低集中度。优化目标是最小化该损失，让 $f_e$ 和 $P_e$ 的分布更均匀。
