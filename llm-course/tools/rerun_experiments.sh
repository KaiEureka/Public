#!/bin/bash
# Re-run every experiment of the book in a scratch copy of code/, logging output and wall time
# (the logs in code/rerun_logs/ and appendix C came from this script).
#
#   cp -r code /tmp/rerun && bash tools/rerun_experiments.sh /tmp/rerun
#   python3 fill_appC.py /tmp/rerun/logs/times.tsv     # optional: regenerate appendix C from the new timings
R=$(cd "${1:?usage: rerun_experiments.sh <copy of code/>}" && pwd); D=$R/data/shakespeare.txt
mkdir -p "$R/logs"
[ -d "$R/ch06_train" ] || cp -r "$R/ch06" "$R/ch06_train"  # retrain in a copy; ch32-34 load the original ch06 checkpoint
run() {  # run <chapter> <label> <command...>
  local ch=$1 label=$2; shift 2
  cd "$R/$ch" || return
  local t0=$(date +%s%N)
  "$@" > "$R/logs/${ch}_${label}.log" 2>&1; local rc=$?
  local t1=$(date +%s%N)
  printf "%s\t%s\t%d\t%d\n" "$ch" "$label" "$(( (t1 - t0) / 1000000000 ))" "$rc" >> "$R/logs/times.tsv"
}
: > "$R/logs/times.tsv"
run ch01 bigram python3 -I bigram.py $D
run ch01 examples python3 -I examples.py $D
run ch02 micrograd python3 -I micrograd.py
run ch02 mlp_K8 python3 -I mlp_lm.py $D 60000 8
run ch02 mlp_K4 python3 -I mlp_lm.py $D 60000 4
run ch02 mlp_K16 python3 -I mlp_lm.py $D 60000 16
run ch03 check python3 -I check.py $D
run ch03 e1 python3 -I e1_init_stats.py $D
run ch03 e3 python3 -I e3_depth.py $D 0.1 6000
run ch03 erest python3 -I e_rest.py $D
run ch04 roofline python3 -I roofline.py
run ch04 roofline3 python3 -I roofline3.py
run ch05 run python3 -I run.py $D ../data/zh
run ch06_train gpt python3 -I gpt.py $D 1000 128 128 4 4 32
run ch06_train eval_pos python3 -I eval_pos.py $D
run ch07 modern_block python3 -I modern_block.py
run ch08 balance python3 -I balance.py
run ch10 chinchilla python3 -I chinchilla.py
run ch11 mup python3 -I mup_demo.py $D
run ch12 muon python3 -I muon_ns.py
run ch13 precision python3 -I precision.py
run ch13 fp8 python3 -I fp8_outliers.py
run ch15 minhash python3 -I minhash.py $D
run ch17 collapse python3 -I collapse.py $D
run ch19 ring python3 ring_allreduce.py
run ch22 flash python3 -I flash_cpu.py
run ch22 triton env TRITON_INTERPRET=1 python3 -I triton_softmax.py
run ch25 goodhart python3 -I goodhart.py
run ch26 dpo python3 -I dpo_toy.py
run ch27 grpo python3 -I grpo_toy.py
run ch29 distill python3 -I distill_toy.py $D
run ch30 eval_noise python3 -I eval_noise.py
run ch32 sae_3e-3 python3 -I sae.py ../ch06 $D 3e-3
run ch32 sae_3e-2 python3 -I sae.py ../ch06 $D 3e-2
run ch32 steer python3 -I steer.py ../ch06 $D
run ch33 kvcache python3 -I kvcache.py ../ch06 $D
run ch34 quant python3 -I quant.py ../ch06 $D
run ch34 speculative python3 -I speculative.py ../ch06 $D
run ch35 mm python3 -I mm_toys.py
echo ALLDONE >> "$R/logs/times.tsv"
