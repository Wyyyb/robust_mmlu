export CUDA_VISIBLE_DEVICES=1
python my_evaluate_llama.py -k 5 -g 1 -d ../test_data/test -s ../test_data/test_result -m mistralai/Mistral-7B-Instruct-v0.2

# python my_evaluate_llama.py -k 5 -g 1 -d ../test_data/test -s ../test_data/test_result -m google/gemma-7b

