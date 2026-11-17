3. **人类标注**：将这些（提示，回复A，回复B）对交给人类标注员，标注员根据"HHH"标准指出哪个更好。最终得到的数据集为 $\mathcal{D} = \{(x, y_w, y_l)\}$，其中 $y_w$ 是胜出的较好回复，$y_l$ 是失败的较差回复。

**Bradley-Terry 模型下的排序损失**：

奖励模型的训练目标是，让奖励模型 $r_\phi(x, y)$ 给出的分数，能够正确反映人类的偏好排序。Bradley-Terry 模型将人类偏好概率建模为：

$$
P(y_w \succ y_l | x) = \frac{\exp(r_\phi(x, y_w))}{\exp(r_\phi(x, y_w)) + \exp(r_\phi(x, y_l))}
$$
