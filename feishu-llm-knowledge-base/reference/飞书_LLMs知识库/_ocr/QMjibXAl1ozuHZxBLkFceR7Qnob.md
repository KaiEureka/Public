$$
\text{Peak Activation} \approx L \times \text{size\_of\_input\_tensor} + A_{\mathrm{layer}}
$$

其中输入张量大小为 $2BSH$ 字节 (FP16)，远比层内部激活小。原无检查点激活为 $L \times A_{\mathrm{layer}}$，所以**缩放因子**近似为：

$$
\frac{\text{Peak with checkpoint}}{\text{Original}} \approx \frac{2BSH + A_{\mathrm{layer}}/L}{A_{\mathrm{layer}}} \approx \frac{1}{L} \quad (\text{当 } A_{\mathrm{layer}} \gg 2BSH)
$$
