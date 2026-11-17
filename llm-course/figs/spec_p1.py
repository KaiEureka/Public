import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from insert import insert
insert([
 ("ch00.md", "前向加反向，每个参数每个 token 共 6 FLOP", "fig-ch00-6nd", "ch00_6nd.svg",
  "训练计算量为什么是 6ND：一个线性层在前向和反向中各做一次同样规模的矩阵乘法", "就是 $C \\approx 6ND$"),
 ("ch00.md", "所以一个 7B 模型光是这些就要", "fig-ch00-mem16", "ch00_mem16.svg",
  "用 bf16 混合精度加 Adam 训练时，每个参数约占 16 字节；7B 模型仅这一项就超出了一张 H100 的显存", None),
 ("ch00.md", "举例（估算）：Llama 3 8B 用 bf16 存储约 16 GB", "fig-ch00-decode", "ch00_decode.svg",
  "decode 阶段的瓶颈：每生成一个 token，都要把全部权重从显存读一遍（以 Llama 3 8B、一张 H100 为例）", None),
 ("ch01.md", "的方式叫**自回归**", "fig-ch01-autoreg", "ch01_autoreg.svg",
  "自回归生成：模型给出下一个 token 的分布，从中抽样，把结果接到前文后面，再预测下一个", "叫**自回归**（autoregressive）"),
 ("ch01.md", "^#### 换到真实世界", "fig-ch01-tree", "ch01_tree.svg",
  "玩具世界的前缀树。从左到右读出一篇文档；每条边上的数是给定前缀时下一个 token 的条件概率，沿路径相乘就是文档的概率", None),
 ("ch01.md", "- **能降下去的只有 KL 这一项**", "fig-ch01-loss", "ch01_loss.svg",
  "交叉熵 loss = 数据的熵 H(p) + KL 散度。训练只能压低 KL 那一段", None),
 ("ch01.md", "这个公式值得记住，它有很直观的含义", "fig-ch01-grad", "ch01_grad.svg",
  "loss 对 logits 的梯度 softmax(z) − onehot(y)：正确答案被往上推，每个错误答案按它当前的概率被往下推", None),
 ("ch01.md", "所有 GPT 类模型的预训练损失都是这样写的。", "fig-ch01-teacher", "ch01_teacher.svg",
  "teacher forcing：输入是真实序列，目标是它右移一位；一次前向同时得到每个位置的预测", None),
 ("ch01.md", "- $\\tau > 1$：分布被拉平，抽样更随机。", "fig-ch01-temp", "ch01_temp.svg",
  "温度的作用：τ 越小，分布越集中在最可能的字符上；τ 越大，分布越平", None),
 ("ch01.md", "^#### 为什么先变好、后变差", "fig-ch01-ngram", "ch01_ngram.svg",
  "n-gram 的两难（数据同上表）：n 越大，上下文的信息越多，但没见过的上下文也越多，loss 先降后升", None),
])
