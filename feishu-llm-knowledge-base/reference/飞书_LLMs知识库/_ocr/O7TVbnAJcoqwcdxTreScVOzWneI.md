2. **更新 Actor 模型**：将经验 batch 中的数据输入 Actor 模型，让它计算当前策略下的 $\log \pi_{new}$。结合之前保存的 $\log \pi_{old}$ 和 $\hat{A}_t$，计算 PPO-clip 损失。同时，可以加入预训练数据的交叉熵损失（PPO-ptx）。用这个总损失更新 Actor 的参数。这个步骤也会进行多个 epoch。
