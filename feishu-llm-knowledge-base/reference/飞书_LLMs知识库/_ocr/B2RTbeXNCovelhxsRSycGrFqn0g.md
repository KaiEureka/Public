- 对第一层权重 $W_1 \in \mathbb{R}^{d \times 4d}$，将其沿列切成 $N$ 份（$N$ 为 TP 度），每张 GPU $i$ 持有 $W_1^{(i)} \in \mathbb{R}^{d \times (4d/N)}$。
- 输入 $X$（形状 $[b, s, d]$）对所有 GPU 可见，各 GPU 独立计算 $Y_i = XW_1^{(i)}$，得到形状 $[b, s, 4d/N]$ 的部分激活。**这一步无需通信**，因为每张卡拥有完整的 $X$，且 $Y_i$ 之间没有依赖。

**行切分（Row-wise）+ All-Reduce**

- 第二层权重 $W_2 \in \mathbb{R}^{4d \times d}$ 被行切成 $W_2^{(i)} \in \mathbb{R}^{(4d/N) \times d}$。
- 各 GPU 用自己持有的部分激活 $Y_i$ 与对应的部分权重相乘，得到形状 $[b, s, d]$ 的**部分和** $Z_i = Y_i W_2^{(i)}$。
- 完整的输出应为 $Z = \sum_{i=0}^{N-1} Z_i$。为了获得完整结果，必须对所有 GPU 的部分和做一次 **All-Reduce**（求和），最终每张卡都得到相同的最终输出 $Z$。
