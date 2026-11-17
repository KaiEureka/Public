2. **Chosen 回复的双重身份**：chosen 回复 $y_w$ 在这个样本中扮演着双重角色。在计算 $\mathcal{L}_{SFT}$ 时，它是模型要去模仿学习的“标准答案”；在计算 $\mathcal{L}_{OR}$ 时，它又是偏好对中的“正样本”。
3. **Rejected 回复的惩罚对象**：rejected 回复 $y_l$ 只参与 $\mathcal{L}_{OR}$ 的计算，作为“负样本”被惩罚。
