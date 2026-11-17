1. 对于一个提示，**Actor** 生成回复。
2. 将回复分别送给 **Reward Model** 和 **Reference Model**，计算 $R_{total} = \text{Reward} - \beta \times \text{KL}(\pi_\theta, \pi_{ref})$。
3. **Critic** 模型根据生成的 token 序列，估计每一步的状态价值 $V(s_t)$。
4. 利用 $R_{total}$ 和 $V(s_t)$，计算出优势函数 $A_t$。
5. 最后，用 $A_t$ 和 PPO-clip 目标函数，**同时更新 Actor 模型和 Critic 模型的参数**。
