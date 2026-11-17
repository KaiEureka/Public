在 MQA 中，所有查询头共享同一个 $K$ 和同一个 $V$。设批次大小为 $b$，序列长度分别为 $s_q$（查询）和 $s_{kv}$（键值），查询头数 $h$，每个头的维度 $d$。输入张量：

- $Q\in\mathbb{R}^{b\times s_q\times h\times d}$
- $K\in\mathbb{R}^{b\times s_{kv}\times1\times d}$（单头）
- $V\in\mathbb{R}^{b\times s_{kv}\times1\times d}$
