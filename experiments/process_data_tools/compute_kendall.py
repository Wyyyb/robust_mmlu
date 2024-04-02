import time


def kendalls_tau(rank1, rank2):
    n = len(rank1)
    if n != len(rank2):
        raise ValueError("两个列表必须具有相同的长度")

    # 计算一致对和不一致对的数量
    concordant = 0
    discordant = 0
    for i in range(n-1):
        for j in range(i+1, n):
            # 一致对 (concordant pair)
            if (rank1[i] - rank1[j]) * (rank2[i] - rank2[j]) > 0:
                concordant += 1
            # 不一致对 (discordant pair)
            elif (rank1[i] - rank1[j]) * (rank2[i] - rank2[j]) < 0:
                discordant += 1

    # 计算Kendall's tau值
    tau = (concordant - discordant) / ((n * (n - 1)) / 2)
    return tau


def compute_0328():
    # 7b, 7b_chat, 13b, 13b_chat

    # # ori_dataset
    # ori = [3, 4, 1, 2]
    # fix_B = [4, 1, 2, 3]
    # fix_C = [4, 3, 2, 1]
    # rare = [4, 3, 1, 2]
    #
    # # exp_10_dataset
    # exp_10_ori = [4, 3, 1, 2]
    # exp_10_fix_B = [2, 1, 4, 3]
    # exp_10_fix_C = [3, 4, 2, 1]
    # exp_10_rare = [4, 3, 2, 1]

    # ori_dataset
    ori = [45.1, 47.5, 54.5, 53.0]
    fix_B = [51.6, 67.8, 61.0, 58.0]
    fix_C = [41.3, 47.6, 61.8, 63.2]
    rare = [42.5, 44.0, 52.5, 52.2]

    # exp_10_dataset
    exp_10_ori = [26.8, 28.3, 35.5, 34.8]
    exp_10_fix_B = [48.8, 53.7, 45.9, 46.2]
    exp_10_fix_C = [48.0, 47.5, 51.1, 54.6]
    exp_10_rare = [18.0, 20.4, 30.0, 32.2]



    ori_dataset = []
    ori_dataset.append(kendalls_tau(ori, fix_B))
    ori_dataset.append(kendalls_tau(ori, fix_C))
    ori_dataset.append(kendalls_tau(ori, rare))

    exp_10_dataset = []
    exp_10_dataset.append(kendalls_tau(exp_10_ori, exp_10_fix_B))
    exp_10_dataset.append(kendalls_tau(exp_10_ori, exp_10_fix_C))
    exp_10_dataset.append(kendalls_tau(exp_10_ori, exp_10_rare))

    print("sum(ori_dataset)", sum(ori_dataset), "ori_dataset", ori_dataset)
    print("sum(exp_10_dataset)", sum(exp_10_dataset), "exp_10_dataset", exp_10_dataset)


if __name__ == "__main__":
    compute_0328()


