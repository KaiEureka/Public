**关键公式验证**：假设损失缩放因子 $S$，各GPU本地放大梯度为 $g_i' = S \cdot g_i$。All-Reduce（平均）后得到 $\bar{g}' = S \cdot \bar{g}$。再unscale得到 $\bar{g} = \bar{g}'/S$，结果与在FP32下通信完全一致。
