$$
\text{Perplexity} = 2^{\text{Cross-Entropy}}
$$

或者，在使用自然对数时：

$$
\text{Perplexity} = e^{\text{Cross-Entropy}}
$$

其中，交叉熵的定义为：

$$
\text{Cross-Entropy} = -\frac{1}{N}\sum_{i=1}^{N} \log P_\theta(w_i|w_{<i})
$$

这里 $P_\theta(w_i|w_{<i})$ 是语言模型分配给真实词 $w_i$ 的概率。交叉熵衡量了真实数据分布 $P$ 与模型分布 $Q$ 之间的差异。当模型分布 $Q$ 完全等于真实分布 $P$ 时，交叉熵取得最小值，即真实数据的信息熵。
