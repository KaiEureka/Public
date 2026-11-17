$$
r_\theta(x,y)=\beta\cdot\log\frac{\pi_\theta(y|x)}{\pi_{\mathrm{ref}}(y|x)}
$$

然后，KTO 不再比较 $y_w$ 和 $y_l$ 的奖励谁高谁低，而是将单个回复的奖励与一个预设的**参考点（reference point）** $z_{\mathrm{ref}}$ 进行比较：
