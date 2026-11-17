[[图]] 多头并行计算流程图：(B,n,dmodel)经reshape变为(B·h,n,dk)，送入多GPU批量矩阵乘（Batch MatMul All head），得到Output。
