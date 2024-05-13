import flet as ft
import numpy as np
from flet_core.matplotlib_chart import MatplotlibChart

from matplotlib import pyplot as plt
import matplotlib

import pingouin as pg
import pandas as pd
import seaborn as sns

from data_process import get_data, data_is_loaded
from pages.page import Page
matplotlib.use('agg')


def reload_corr_page(page: Page, page_number):
    page.clean_controls()

    def show_matrix(matrix, name):
        fig, ax = plt.subplots()
        im = ax.imshow(matrix, cmap='hot', interpolation='nearest')
        fig.colorbar(im)

        ax.set_xticks(range(len(matrix.columns)))
        ax.set_yticks(range(len(matrix.index)))

        ax.set_xticklabels(matrix.columns)
        ax.set_yticklabels(matrix.index)

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title(name)

        for i in range(len(matrix.index)):
            for j in range(len(matrix.columns)):
                ax.text(j, i, f'{matrix.iloc[i, j]:.2f}', ha='center', va='center', color='black')

        page.add_control(MatplotlibChart(fig, expand=True))
        page.update(None)

    def draw_corr(event):
        try:
            reload_corr_page(page, 1)
            show_matrix(get_data().corr(), 'Парная корреляция')
        except ValueError:
            print('[Error] Corr error')

    def draw_pcorr(event):
        try:
            reload_corr_page(page, 2)
            show_matrix(get_data().pcorr(), 'Частная корреляция')
        except ValueError:
            print('[Error] Pcorr error')

    def get_stud(matrix):
        n = matrix.shape[0]
        t_stat_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                if i != j:
                    correlation = matrix.iloc[i, j]
                    t_stat_matrix[i, j] = correlation * np.sqrt((n - 2) / (1 - correlation ** 2))

        return pd.DataFrame(t_stat_matrix, columns=matrix.columns, index=matrix.columns)

    def draw_stud_corr(event):
        try:
            reload_corr_page(page, 3)
            show_matrix(get_stud(get_data().corr()), 'Стьюдента парная')
        except ValueError:
            print('[Error] Stud corr error')

    def draw_stud_pcorr(event):
        try:
            reload_corr_page(page, 4)
            show_matrix(get_stud(get_data().pcorr()), 'Стьюдента частная')
        except ValueError:
            print('[Error] Stud pcorr error')

    button_headers = [
        ft.TextButton('Парная корреляция', style=ft.ButtonStyle(color='grey' if page_number == 1 else 'black'),
                      on_click=draw_corr),
        ft.TextButton('Частная корреляция', style=ft.ButtonStyle(color='grey' if page_number == 2 else 'black'),
                      on_click=draw_pcorr),
        ft.TextButton('Стьюдента парная', style=ft.ButtonStyle(color='grey' if page_number == 3 else 'black'),
                      on_click=draw_stud_corr),
        ft.TextButton('Стьюдента частная', style=ft.ButtonStyle(color='grey' if page_number == 4 else 'black'),
                      on_click=draw_stud_pcorr),
    ]

    page.add_control(
        ft.Row(
            [*button_headers]
        )
    )


def get_corr_page(page: Page):
    if data_is_loaded():
        reload_corr_page(page, 1)

    return page
