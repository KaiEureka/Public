4. **总损失函数**：将注意力转移损失 $L_{AT}$ 与标准的logits蒸馏损失 $L_{KD}$ 和任务损失 $L_{CE}$ 结合：

$$
L_{total} = \alpha L_{KD} + \beta L_{CE} + \gamma L_{AT}
$$
