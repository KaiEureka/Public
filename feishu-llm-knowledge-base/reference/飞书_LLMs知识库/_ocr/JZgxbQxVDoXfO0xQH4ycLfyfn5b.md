$$
\min_\theta \max_{\alpha \in \Delta_k} \sum_{i=1}^{k} \alpha_i \cdot \mathcal{L}_i(\theta)
$$

其中 $\mathcal{L}_i$ 是模型在第 $i$ 个领域上的损失，$\alpha$ 是动态调整的域权重。
