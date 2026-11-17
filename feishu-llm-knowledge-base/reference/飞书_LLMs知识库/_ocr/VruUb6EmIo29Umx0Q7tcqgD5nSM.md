RoPE 通过旋转变换对 Q 和 K 施加位置编码，即先计算 $\tilde{q}=R_mq,\ \tilde{k}=R_nk$，再做点积。FlashAttention 需要在计算 $\tilde{q}$ 和 $\tilde{k}$ 时应用旋转，但直接在 SRAM 内逐块旋转会占用计算资源。
