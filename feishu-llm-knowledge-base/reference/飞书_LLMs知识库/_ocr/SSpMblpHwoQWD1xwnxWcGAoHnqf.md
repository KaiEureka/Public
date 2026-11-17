$$
\mathcal{L}_{\mathrm{CE}} = -\frac{1}{L}\sum_{t=1}^{L} \log P_S(y_t^*|x_{<t})
$$

总损失为两者的加权和：$\mathcal{L} = \alpha \cdot \mathcal{L}_{\mathrm{KD}} + (1-\alpha) \cdot \mathcal{L}_{\mathrm{CE}}$，其中 $\alpha$ 通常取0.5~0.9。
