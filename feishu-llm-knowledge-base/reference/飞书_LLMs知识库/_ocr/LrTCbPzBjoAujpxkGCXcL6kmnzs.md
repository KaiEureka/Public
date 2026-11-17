$$
\mathcal{L}_{\mathrm{MLM}} = -\frac{1}{|\mathcal{M}|}\sum_{i \in \mathcal{M}}\log P_\theta(x_i \mid x_{\setminus\mathcal{M}})
$$

其中 $\mathcal{M}$ 是被掩码位置的集合，$x_{\setminus\mathcal{M}}$ 是未掩码的上下文。
