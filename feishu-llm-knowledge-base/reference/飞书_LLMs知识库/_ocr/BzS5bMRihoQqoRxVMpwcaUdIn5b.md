可以替换为：$\Delta = \beta \cdot \left( \log \frac{P_\theta(y_w|x)}{P_{\text{freezed\_old}}(y_w|x)} - \log \frac{P_\theta(y_l|x)}{P_{\text{freezed\_old}}(y_l|x)} \right)$，其中分母是一个冻结的旧模型。
