import flet as ft
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

    def draw_corr(event):
        try:
            reload_corr_page(page, 1)

            corr_matrix = get_data().corr()
            fig, ax = plt.subplots()
            im = ax.imshow(corr_matrix, cmap='hot', interpolation='nearest')
            fig.colorbar(im)

            ax.set_xticks(range(len(corr_matrix.columns)))
            ax.set_yticks(range(len(corr_matrix.index)))

            ax.set_xticklabels(corr_matrix.columns)
            ax.set_yticklabels(corr_matrix.index)

            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title('Парная корреляция')

            page.add_control(MatplotlibChart(fig, expand=True))
            page.update(None)
        except ValueError:
            print('[Error] Corr error')

    def draw_pcorr(event):
        try:
            reload_corr_page(page, 2)

            pcorr_matrix = get_data().pcorr()
            fig, ax = plt.subplots()
            im = ax.imshow(pcorr_matrix, cmap='hot', interpolation='nearest')
            fig.colorbar(im)

            ax.set_xticks(range(len(pcorr_matrix.columns)))
            ax.set_yticks(range(len(pcorr_matrix.index)))

            ax.set_xticklabels(pcorr_matrix.columns)
            ax.set_yticklabels(pcorr_matrix.index)

            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title('Частная корреляция')

            page.add_control(MatplotlibChart(fig, expand=True))
            page.update(None)
        except ValueError:
            print('[Error] Pcorr error')

    button_headers = [
        ft.TextButton('Парная корреляция', style=ft.ButtonStyle(color='grey' if page_number == 1 else 'black'),
                      on_click=draw_corr),
        ft.TextButton('Частная корреляция', style=ft.ButtonStyle(color='grey' if page_number == 2 else 'black'),
                      on_click=draw_pcorr)
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
