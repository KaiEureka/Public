$$
Y=(X\cdot\mathrm{diag}(s)^{-1})\cdot(\mathrm{diag}(s)\cdot W)=\hat{X}\hat{W}
$$

通过选择合适的 $s$（如 $s_j=\max(|X_j|)^\alpha/\max(|W_j|)^{1-\alpha}$），将激活的离群值“平滑”到更均衡的分布，而权重相应被放大，二者相乘结果不变。平滑后 $X$ 和 $W$ 均更易于量化。这是目前解决激活离群值的最有效方案之一，被集成到多个推理框架中。
