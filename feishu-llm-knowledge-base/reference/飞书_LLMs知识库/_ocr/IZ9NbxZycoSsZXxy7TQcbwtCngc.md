$$
\mathcal{L}(\phi) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( r_\phi(x, y_w) - r_\phi(x, y_l) \right) \right]
$$

其中 $\sigma$ 是 sigmoid 函数。这个损失函数直观地告诉我们：让较好回复 $y_w$ 的分数比 $y_l$ 越高越好。当两者分数差距很小时，损失大；差距足够大时，损失趋近于零。
