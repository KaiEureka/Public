一个65B（650亿）参数的模型，标准FP16存储需要 $65\times10^9\times2\text{ bytes}\approx130\text{ GB}$。使用QLoRA的NF4+双重量化后，每个参数约占4.2-bit（约0.525字节）。因此，模型本身的显存占用降至 $65\times10^9\times0.525\text{ bytes}\approx34\text{ GB}$。
