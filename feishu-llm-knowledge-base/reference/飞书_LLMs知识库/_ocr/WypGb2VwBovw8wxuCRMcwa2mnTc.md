**通信量**：Reduce-Scatter 的通信量与 All-Reduce 相同（均为 $2\Psi \times \frac{N_d - 1}{N_d} \approx 2\Psi$），但由于只保留部分梯度，节省了显存。
