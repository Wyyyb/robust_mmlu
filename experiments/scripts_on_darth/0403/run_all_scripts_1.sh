#!/bin/bash

# 启动每个脚本并将其放入后台执行
export PYTHONWARNINGS="ignore"
./eval_13b_fixA.sh &
./eval_13b_fixB.sh &
./eval_13b_fixC.sh &
./eval_13b_fixD.sh &
./eval_13b_ori.sh &
./eval_13b_rare_symbol.sh &

# 等待所有后台进程结束
wait

echo "所有脚本执行完毕。"