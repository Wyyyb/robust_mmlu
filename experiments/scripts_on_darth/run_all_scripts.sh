#!/bin/bash

# 启动每个脚本并将其放入后台执行

./eval_7b_fixA.sh &
./eval_7b_fixB.sh &
./eval_7b_fixC.sh &
./eval_7b_fixD.sh &
./eval_7b_ori.sh &
./eval_7b_rare_symbol.sh &

# 等待所有后台进程结束
wait

echo "所有脚本执行完毕。"