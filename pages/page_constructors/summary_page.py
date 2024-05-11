import flet as ft
import flet_core
import pandas as pd

from data_process import data_is_loaded, load_csv, get_data, set_data, summary
from modules.data import Data
from pages.page import Page


summary_data = {}


def get_summary_page(page: Page):
    global summary_data
    page.clean_controls()

    def get_full_info(event: flet_core.control_event.ControlEvent):
        list_name = event.control.data
        if isinstance(summary_data[list_name], dict):
            for i in summary_data[list_name].keys():
                if isinstance(summary_data[list_name][i], dict):
                    summary_data[list_name][i] = \
                        "\n".join([f"{key}: {value}" for key, value in summary_data[list_name][i].items()])

            data = "\n".join([f"{key}: {value}" for key, value in summary_data[list_name].items()])
        else:
            data = str(summary_data[list_name])

        dlg = ft.AlertDialog(
            title=ft.Text('Данные'),
            content=ft.Text(data),
            open=True
        )

        page.body.dialog = dlg
        page.body.update()

    def get_summary_rows(data: dict):
        rows = []
        for i in data.keys():
            rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(i)), ft.DataCell(ft.Text(
                    'раскрыть список...' if (isinstance(data[i], dict) or isinstance(data[i], list))
                    else 'раскрыть строку...' if len(str(data[i])) > 50 else data[i]
                ), on_tap=get_full_info, data=i)]
            ))

        return rows

    if data_is_loaded():
        summary_data = summary()
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Наименование")),
                ft.DataColumn(ft.Text("Значение"))
            ],
            rows=get_summary_rows(summary_data),
            border=ft.border.all(2, 'black')
        )

        lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        lv.controls.append(ft.IconButton(ft.icons.CLOSE, icon_color='black', on_click=lambda _: set_data(None)))
        lv.controls.append(table)

        page.add_control(lv)

    return page
