$$
\mathcal{L}_{OR} = -\log \sigma \left( \log \frac{\text{odds}_\theta(y_w|x)}{\text{odds}_\theta(y_l|x)} \right)
$$

我们可以将其展开为：

$$
\mathcal{L}_{OR} = -\log \sigma \left( \log \text{odds}_\theta(y_w|x) - \log \text{odds}_\theta(y_l|x) \right)
$$

进一步，设 $A = \log P_\theta(y_w|x)$，$B = \log P_\theta(y_l|x)$。那么：

$$
\log \text{odds} = A - \log(1 - e^A)
$$
