$$
\text{Perplexity}(PPL) = 2^{H(P,Q)} = 2^{-\frac{1}{N}\sum_{i=1}^{N} \log_2 P_\theta(w_i|w_{<i})}
$$

其中 $P_\theta(w_i|w_{<i})$ 是模型在给定历史序列 $w_{<i}$ 的情况下预测下一个词 $w_i$ 的概率。
