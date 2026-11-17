ORPO 的总损失是 $\mathcal{L}_{ORPO} = \mathcal{L}_{SFT} + \lambda \cdot \mathcal{L}_{OR}$。其中 $\mathcal{L}_{SFT}$ 部分，正是标准的指令微调交叉熵损失。这个损失的存在，为模型提供了一个强大且持续的梯度信号，强制模型去最大化 chosen 回复（即“好回复”）中每个 token 的生成概率。
