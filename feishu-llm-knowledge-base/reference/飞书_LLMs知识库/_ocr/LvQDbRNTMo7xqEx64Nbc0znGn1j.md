**KL 散度（Kullback-Leibler Divergence）** 测量两个概率分布之间的差异。在知识蒸馏中，它被用来衡量学生模型的软输出分布 $P_S$ 与教师模型的软输出分布 $P_T$ 之间的距离。蒸馏损失通常定义为两者的 KL 散度：

$$
\mathcal{L}_{\mathrm{KD}} = \mathrm{KL}(P_T \parallel P_S) = \sum_i P_T(i) \log \frac{P_T(i)}{P_S(i)}
$$

其中 $P_T$ 和 $P_S$ 都是在相同温度 $T$ 下经过 softmax 得到的概率分布：

$$
P(i) = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}
$$
