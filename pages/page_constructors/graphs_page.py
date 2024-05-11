from collections import Counter

import flet as ft
import flet_core
import pandas as pd

from data_process import data_is_loaded, load_csv, get_data, set_data, summary
from modules.data import Data
from pages.menu import Menu
from pages.page import Page


min_field = ft.TextField(hint_text="Нижний предел", value="0", label="Минимум")
max_field = ft.TextField(hint_text="Верхний предел", value="1000000", label="Максимум")


def reload_graph_page(page: Page, page_number, row):
    page.clean_controls()

    def draw_default_graph(e: flet_core.control_event.ControlEvent):
        column_name = e.control.text
        column_data = []

        reload_graph_page(page, list(get_data().columns).index(column_name), 1)

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

        page.add_control(ft.LineChart(
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
        ))

        page.update(page.body)

    def draw_freq_graph(e: flet_core.control_event.ControlEvent):
        data = get_data()
        column_name = e.control.text
        column = data[column_name]

        reload_graph_page(page, list(get_data().columns).index(column_name), 2)

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

        page.add_control(ft.BarChart(
            bar_groups=chart_data,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels=left_axis),
            bottom_axis=ft.ChartAxis(labels=bottom_axis)
        ))

        page.update(page.body)

    button_headers = [ft.TextButton(
        x, style=ft.ButtonStyle(color='grey' if (row == 1 and page_number == i) else 'black'),
        on_click=draw_default_graph
    ) for i, x in enumerate(get_data().columns)]

    page.add_control(
        ft.Row(
            [*button_headers, ft.Text("Все данные")]
        )
    )

    button_headers = [
        ft.TextButton(x, style=ft.ButtonStyle(color='grey' if (row == 2 and page_number == i) else 'black'),
                      on_click=draw_freq_graph) for i, x in enumerate(get_data().columns)]

    page.add_control(
        ft.Row(
            [*button_headers, ft.Text("Частота")]
        )
    )

    page.add_control(
        ft.Row(
            [min_field, max_field], alignment=ft.MainAxisAlignment.END
        )
    )


def get_graphs_page(page: Page):
    if data_is_loaded():
        reload_graph_page(page, 1, 1)

    return page
