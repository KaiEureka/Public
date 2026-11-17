1. **温度采样（Temperature Sampling）**：这是最主流、最有效的方法。如 XLM-R 对 CommonCrawl 中 100 多种语言进行采样时，使用公式 $p_i \propto (N_i)^\alpha$，$\alpha$ 取 0.3。这极大地提升了低资源语言的采样概率，使得即便是数据量极小的语言也能获得足够多的训练机会。
