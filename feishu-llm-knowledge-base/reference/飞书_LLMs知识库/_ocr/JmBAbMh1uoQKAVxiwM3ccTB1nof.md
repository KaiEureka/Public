**融合 Dropout 思想**：

GELU 的设计灵感来源于将 Dropout 与激活函数结合。标准 Dropout 以固定概率 $p$ 随机将神经元置零。GELU 则可视为一种"自适应 Dropout"：对于输入 $x$，它被乘以一个伯努利随机变量 $m \sim \mathrm{Bernoulli}(\Phi(x))$，然后输出 $m \cdot x$。期望值就是 $\mathbb{E}[m \cdot x] = \Phi(x) \cdot x = \mathrm{GELU}(x)$。换句话说，GELU 在期望下等效于根据输入的大小随机丢弃神经元：输入 $x$ 越大，保留概率 $\Phi(x)$ 越接近 1；输入越小（尤其是负值），保留概率越小（接近 0）。这比固定丢弃概率的 Dropout 更灵活，因为它使得正则化强度与输入本身相关，有利于保护强信号并抑制弱噪声。
