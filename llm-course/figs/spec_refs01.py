"""Add in-text references for the chapter 0-4 figures (added in the first figure round without references)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from insert import addref
addref([
 ("ch00.md", "一张 80 GB 的 H100 放不下", "一张 80 GB 的 H100 放不下（{{fig-ch00-mem16}}）"),
 ("ch00.md", "举例（估算）：Llama 3 8B 用 bf16", "举例（估算，见{{fig-ch00-decode}}）：Llama 3 8B 用 bf16"),
 ("ch01.md", "也就是模型与真实分布之间的差距。", "也就是模型与真实分布之间的差距（{{fig-ch01-loss}}）。"),
 ("ch01.md", "这个公式值得记住，它有很直观的含义：", "这个公式值得记住，它有很直观的含义（{{fig-ch01-grad}}）："),
 ("ch01.md", "所有 GPT 类模型的预训练损失都是这样写的。", "所有 GPT 类模型的预训练损失都是这样写的（{{fig-ch01-teacher}}）。"),
 ("ch01.md", "**温度** $\\tau$：", "**温度** $\\tau$（{{fig-ch01-temp}}）："),
 ("ch01.md", "这里有两股力量在互相拉扯：", "这里有两股力量在互相拉扯（{{fig-ch01-ngram}}）："),
 ("ch02.md", "这就是一个最简单的**线性层**。", "这就是一个最简单的**线性层**（{{fig-ch02-onehot}}）。"),
 ("ch02.md", "解决办法是在线性层之间插入一个**激活函数**", "解决办法（{{fig-ch02-xor}}）是在线性层之间插入一个**激活函数**"),
 ("ch02.md", "一个记忆技巧：", "一个记忆技巧（{{fig-ch02-matgrad}}）："),
 ("ch02.md", "本章模型的反向传播，完整代码就是下面这些：", "本章模型的反向传播，完整代码就是下面这些（数据流见{{fig-ch02-backflow}}）："),
 ("ch02.md", "### 2.6 结果\n", "### 2.6 结果\n\n训练过程见下表和{{fig-ch02-curve}}。\n"),
 ("ch02.md", "原因有两个：", "原因有两个（{{fig-ch02-context}}）："),
 ("ch03.md", "逐行解读：", "逐行解读（{{fig-ch03-signal}}）："),
 ("ch03.md", "Post-norm 把恒等路径也包进了 Norm 里", "Post-norm（{{fig-ch03-residual}}）把恒等路径也包进了 Norm 里"),
 ("ch03.md", "**关键在 $\\hat m/\\sqrt{\\hat v}$ 这一项。**", "**关键在 $\\hat m/\\sqrt{\\hat v}$ 这一项**（{{fig-ch03-optim}}）。"),
 ("ch03.md", "**WSD**（Warmup–Stable–Decay）：", "**WSD**（Warmup–Stable–Decay，三种调度的对比见{{fig-ch03-sched}}）："),
 ("ch03.md", "#### 梯度累积\n", "#### 梯度累积\n\n梯度累积和下面的梯度裁剪见{{fig-ch03-accum}}。\n"),
 ("ch04.md", "先区分两个概念：", "先区分两个概念（{{fig-ch04-cpugpu}}）："),
 ("ch04.md", "### 4.3 存储层级：越近越快，越快越小\n", "### 4.3 存储层级：越近越快，越快越小\n\n{{fig-ch04-memhier}} 是下表的直观版本。\n"),
 ("ch04.md", "**实验 B**：", "**实验 B**（{{fig-ch04-batch}}）："),
 ("ch04.md", "为例（GELU 是一种激活函数，第 6 章介绍）：", "为例（GELU 是一种激活函数，第 6 章介绍；见{{fig-ch04-fusion}}）："),
 ("ch04.md", "解决办法是**批处理**：", "解决办法是**批处理**（{{fig-ch04-batching}}）："),
])
print("ok")
