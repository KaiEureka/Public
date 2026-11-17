[[图]] MoE 前向流程图：Input Token 经 Gate Network 得到 logits z=Wg·x 并 Softmax，Top-k Selection 选出 Expert 1、Expert 2，再 Weighted Sum 得到 Output
