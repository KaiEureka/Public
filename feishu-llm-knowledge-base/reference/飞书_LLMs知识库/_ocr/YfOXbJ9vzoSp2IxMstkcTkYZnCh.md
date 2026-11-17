**数学推导**：设真实损失函数 $L(w)$，缩放后 $\tilde{L}(w) = S \cdot L(w)$，则梯度 $\nabla \tilde{L} = S \cdot \nabla L$。参数更新：$w_{t+1} = w_t - \eta \cdot (\nabla \tilde{L}/S) = w_t - \eta \cdot \nabla L$，完全等价。
