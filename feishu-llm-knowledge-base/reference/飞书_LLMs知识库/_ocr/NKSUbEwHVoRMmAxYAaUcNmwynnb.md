- $Q, K, V$：每个 $b \times s \times d$，3 个，约 $3 \times 2048 \times 12288 \times 2 = 144$ MB（FP16）。
- 注意力分数矩阵 $S$：$b \times h \times s \times s = 96 \times 2048 \times 2048 \approx 4 \times 10^8$ 元素，FP16 约 0.8 GB。
- Softmax 输出 $A$：同 $S$，约 0.8 GB。

注意力部分小计约 1.7 GB。
