具体地，对于一个给定的文本序列 $w_1, w_2, ..., w_T$，语言模型给出概率 $P(w_1, ..., w_T)$，困惑度定义为：

$$
\mathrm{PPL} = \exp\left(-\frac{1}{T}\sum_{t=1}^{T} \log P(w_t \mid w_{<t})\right)
$$
