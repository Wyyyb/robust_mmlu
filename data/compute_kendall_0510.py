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
    # print("tau", tau)
    return tau


def compute_0510():
    # mmlu_pro hybrid
    mmlu_pro_standard = [0.252, 0.306, 0.279]
    # mmlu_pro symbol
    # mmlu_pro_standard = [0.195, 0.303, 0.311]

    # mmlu hybrid
    # mmlu_standard = [0.392, 0.484, 0.439]
    # mmlu symbol
    mmlu_standard = [0.458, 0.625, 0.634]

    mmlu_pro = [
        [0.195, 0.303, 0.311],
        [0.191, 0.297, 0.305],
        [0.188, 0.3, 0.316],
        [0.466, 0.379, 0.463],
        [0.2, 0.438, 0.273],
        [0.145, 0.299, 0.258],
        [0.252, 0.306, 0.279],
        [0.25, 0.31, 0.278],
        [0.254, 0.308, 0.284],
        [0.293, 0.357, 0.329],
        [0.266, 0.33, 0.306],
        [0.278, 0.338, 0.311]
    ]

    mmlu = [
        [0.458, 0.625, 0.634],
        [0.447, 0.624, 0.628],
        [0.433, 0.63, 0.63],
        [0.615, 0.684, 0.665],
        [0.454, 0.659, 0.575],
        [0.381, 0.586, 0.623],
        [0.392, 0.484, 0.439],
        [0.387, 0.489, 0.438],
        [0.392, 0.49, 0.441],
        [0.41, 0.49, 0.447],
        [0.389, 0.489, 0.446],
        [0.397, 0.48, 0.446]
    ]
    mmlu_pro_score = 0
    mmlu_score = 0
    # compute mmlu pro ken
    for each in mmlu_pro:
        mmlu_pro_score += kendalls_tau(mmlu_pro_standard, each)
    print("mmlu-pro kendalls score", mmlu_pro_score/12)
    for each in mmlu:
        mmlu_score += kendalls_tau(mmlu_standard, each)
    print("mmlu kendalls score", mmlu_score/12)


if __name__ == "__main__":
    compute_0510()


