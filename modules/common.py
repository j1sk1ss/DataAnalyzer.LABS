import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def show_correlation(matrix, size=(10, 10), name='default'):
    plt.figure(figsize=size)
    sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title(name)
    plt.show()


def get_lists(dataframe):
    temp_list = []
    for i in range(len(dataframe.iloc[0])):
        lst = []
        for j in range(len(dataframe)):
            lst.append(dataframe.iloc[j].iloc[i])

        temp_list.append(lst)

    return temp_list


def get_dispersion(n, x, m):
    answer_sum = 0
    for i in range(1, n):
        answer_sum += (x[i] - m) ** 2

    return (1 / (n - 1)) * answer_sum


def cdf(x):
    x = x / 1.414213562
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    s = np.sign(x)
    t = 1 / (1 + s * p * x)
    b = np.exp(-x * x)
    y = (s * s + s) / 2 - \
        s * (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * b / 2

    return y
