from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


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
