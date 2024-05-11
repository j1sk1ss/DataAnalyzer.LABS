from collections import Counter

import flet as ft
import flet_core.control_event
from flet.matplotlib_chart import MatplotlibChart

from matplotlib import pyplot as plt
import pingouin as pg
import pandas as pd
import seaborn as sns

from data_process import load_csv, data_is_loaded, get_data, set_data, summary
from modules.data import Data
from pages.menu import Menu
from pages.page import Page
from pages.page_constructors.graphs_page import get_graphs_page
from pages.page_constructors.main_page import get_main_page
from pages.page_constructors.summary_page import get_summary_page


def main(page: ft.Page):

    # region [Startup settings]
    page.title = 'Cordell Data Analyzer'
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.window_width = 1200
    page.window_height = 600
    page.window_resizable = False
    # endregion

    # region [Page bodies]
    program = Menu(page, [
        get_main_page(Page(page, [])), get_summary_page(Page(page, [])),
        get_graphs_page(Page(page, []))
    ],
        ft.Row([
            ft.IconButton(ft.icons.HOME, on_click=lambda _:program.show_page(0)),
            ft.IconButton(ft.icons.SUMMARIZE, on_click=lambda _:program.show_page(1)),
            ft.IconButton(ft.icons.AUTO_GRAPH, on_click=lambda _:program.show_page(2)),
            ft.IconButton(ft.icons.DATA_ARRAY, on_click=lambda _:program.show_page(3)),
            ft.IconButton(ft.icons.GRAPHIC_EQ, on_click=lambda _:program.show_page(4)),
        ],
    ))

    # endregion

    program.show_page(0)

    # region [Main Page]
    # Main page ===========

    def open_main_page(event):
        return

    # endregion

    # region [Summary Page]
    # Summary page ===========

    def open_summary_page(event):
        return

    # endregion

    # region [Graphs Page]
    # Graphs page ===========

    min_field = ft.TextField(hint_text="Нижний предел", value="0", label="Минимум")
    max_field = ft.TextField(hint_text="Верхний предел", value="1000000", label="Максимум")

    def reload_graph_page(page_number, row):
        page_reload(3)
        button_headers = [ft.TextButton(
            x, style=ft.ButtonStyle(color='grey' if (row == 1 and page_number == i) else 'black'),
            on_click=draw_default_graph
        ) for i, x in enumerate(get_data().columns)]
        page.add(
            ft.Row(
                [*button_headers, ft.Text("Все данные")]
            )
        )

        button_headers = [
            ft.TextButton(x, style=ft.ButtonStyle(color='grey' if (row == 2 and page_number == i) else 'black'),
                          on_click=draw_freq_graph) for i, x in enumerate(get_data().columns)]
        page.add(
            ft.Row(
                [*button_headers, ft.Text("Частота")]
            ),
            ft.Row(
                [min_field, max_field], alignment=ft.MainAxisAlignment.END
            )
        )

    def draw_default_graph(e: flet_core.control_event.ControlEvent):
        column_name = e.control.text
        column_data = []

        reload_graph_page(list(get_data().columns).index(column_name), 1)

        bottom_axis = [
            ft.ChartAxisLabel(
                value=x,
                label=ft.Text(str(x), size=10, weight=ft.FontWeight.NORMAL),
            ) for x in range(len(column_data))
        ]

        left_axis = [
            ft.ChartAxisLabel(
                value=x,
                label=ft.Text(str(x), size=10, weight=ft.FontWeight.NORMAL),
            ) for x in range(int(max(get_data()[column_name])), 0,
                             max(int(max(get_data()[column_name]) / 10000), 1))
        ]

        column = get_data()[column_name]
        for i in range(len(column)):
            if int(min_field.value) < i < int(max_field.value):
                column_data.append(ft.LineChartDataPoint(i, column[i]))

        chart_data = [ft.LineChartData(
            data_points=column_data,
            stroke_width=2,
            color=ft.colors.LIGHT_GREEN,
            curved=False,
            stroke_cap_round=True,
        )]

        chart = ft.LineChart(
            data_series=chart_data,
            left_axis=ft.ChartAxis(
                labels=left_axis
            ),
            bottom_axis=ft.ChartAxis(
                labels=bottom_axis
            ),
            border=ft.Border(
                bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))
            )
        )

        page.add(chart)
        page.update()

    def draw_freq_graph(e: flet_core.control_event.ControlEvent):
        data = get_data()
        column_name = e.control.text
        column = data[column_name]

        reload_graph_page(list(get_data().columns).index(column_name), 2)

        value_counts = sorted(Counter(column).items(), key=lambda x: x[0])
        column_values = []
        for i in value_counts:
            column_values.append(i[1])

        chart_data = [ft.BarChartGroup(
            x=i,
            bar_rods=[
                ft.BarChartRod(
                    from_y=1,
                    to_y=column_values[i],
                    width=6,
                    color=ft.colors.BLUE,
                    border_radius=0,
                ),
            ],
        ) for i in range(len(column_values)) if int(min_field.value) < value_counts[i][0] < int(max_field.value)]

        bottom_axis = [
            ft.ChartAxisLabel(
                value=value_counts[x][0],
                label=ft.Text(str(value_counts[x][0]), size=10, weight=ft.FontWeight.NORMAL),
            ) for x in range(0, len(value_counts), 5)
        ]

        left_axis = [
            ft.ChartAxisLabel(
                value=x,
                label=ft.Text(str(x), size=10, weight=ft.FontWeight.NORMAL),
            ) for x in range(int(max(get_data()[column_name])), 0,
                             max(int(max(get_data()[column_name]) / 10000), 1))
        ]

        page.add(ft.BarChart(
            bar_groups=chart_data,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels=left_axis),
            bottom_axis=ft.ChartAxis(labels=bottom_axis)
        ))
        page.update()

    def open_graphs_page(event):
        return
        reload_graph_page(1, 1)
        page.update()

    # endregion

    # region [Corr Page]
    # Corr page ===========

    def draw_corr(event):
        reload_corr_page(1)

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

        page.add(MatplotlibChart(fig, expand=True))

        page.update()

    def draw_pcorr(event):
        reload_corr_page(2)

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

        page.add(MatplotlibChart(fig, expand=True))

        page.update()

    def reload_corr_page(page_number):
        page_reload(4)
        button_headers = [
            ft.TextButton('Парная корреляция', style=ft.ButtonStyle(color='grey' if page_number == 1 else 'black'),
                          on_click=draw_corr),
            ft.TextButton('Частная корреляция', style=ft.ButtonStyle(color='grey' if page_number == 2 else 'black'),
                          on_click=draw_pcorr)
        ]

        page.add(
            ft.Row(
                [*button_headers]
            )
        )

    def open_corr_page(event):
        reload_corr_page(1)
        page.update()

    # endregion

    def open_regression_page(event):
        page_reload(5)

        page.update()

    def page_reload(page_number):
        page.controls.clear()

        page.add(
            ft.Row(
                [
                    ft.IconButton(ft.icons.HOME, icon_color='grey' if page_number == 1 else 'black',
                                  on_click=open_main_page),
                    ft.IconButton(ft.icons.SUMMARIZE, icon_color='grey' if page_number == 2 else 'black',
                                  on_click=open_summary_page),
                    ft.IconButton(ft.icons.AUTO_GRAPH, icon_color='grey' if page_number == 3 else 'black',
                                  on_click=open_graphs_page),
                    ft.IconButton(ft.icons.DATA_ARRAY, icon_color='grey' if page_number == 4 else 'black',
                                  on_click=open_corr_page),
                    ft.IconButton(ft.icons.GRAPHIC_EQ, icon_color='grey' if page_number == 5 else 'black',
                                  on_click=open_regression_page),
                ],
            )
        )

        page.update()

    # open_main_page(None)


ft.app(target=main)
