- **内部分数**：$\log \frac{\text{odds}_\theta(y_w|x)}{\text{odds}_\theta(y_l|x)}$ 计算了模型对 chosen 回复的“发生比”相对于 rejected 回复的“发生比”的比值，再取对数。如果模型更倾向于生成 chosen（即其 odds 更高），这个差值就为正且越大越好。
- **损失优化**：通过最小化 $-\log \sigma(\cdot)$，等价于最大化这个内部分数。因此，$\mathcal{L}_{OR}$ 的物理意义就是**最大化模型对 chosen 回复的相对偏好，同时最小化模型生成 rejected 回复的可能性。**

**总损失**：

$$
\mathcal{L}_{ORPO} = \mathcal{L}_{SFT} + \lambda \cdot \mathcal{L}_{OR}
$$
