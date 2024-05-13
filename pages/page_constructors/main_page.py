import flet as ft
import flet_core
import pandas as pd

from data_process import data_is_loaded, load_csv, get_data, set_data, get_dataframe, set_target, get_target, summary
from modules.data import Data

from pages.page import Page
from pages.page_constructors.corr_page import get_corr_page
from pages.page_constructors.graphs_page import get_graphs_page
from pages.page_constructors.reg_page import get_reg_page
from pages.page_constructors.summary_page import get_summary_page


def get_main_page(page: Page):
    page.clean_controls()
    dataframe_name = ft.Text('...', width=1200)

    if not data_is_loaded():
        def upload_file(e: ft.FilePickerResultEvent):
            load_csv(e.files[0].path)

            dataframe_name.value = e.files[0].name
            dataframe_name.update()
            page.update(get_main_page(page).body)

        pick_files_dialog = ft.FilePicker(on_result=upload_file)
        upload_button = ft.IconButton(ft.icons.UPLOAD, on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=False,
            allowed_extensions=['csv'],
            dialog_title='Select dataset'
        ), icon_color='black', tooltip='Загрузить')

        page.add_control(
            ft.Row([
                upload_button, pick_files_dialog,
                dataframe_name
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ))
    else:
        new_sum_page = Page(page.body, [])
        new_sum_page.set_parent(page.parent)
        page.parent.pages[1] = get_summary_page(new_sum_page)

        new_graphs_page = Page(page.body, [])
        new_graphs_page.set_parent(page.parent)
        page.parent.pages[2] = get_graphs_page(new_graphs_page)

        new_corr_page = Page(page.body, [])
        new_corr_page.set_parent(page.parent)
        page.parent.pages[3] = get_corr_page(new_corr_page)

        new_reg_page = Page(page.body, [])
        new_reg_page.set_parent(page.parent)
        page.parent.pages[4] = get_reg_page(new_reg_page)

        drop_column_name = ft.TextField(label='Удалить')

        def normalize_dataframe(event):
            get_dataframe().normalize()
            page.update(get_main_page(page).body)

        def close_dataframe(event):
            set_data(None)
            dataframe_name.value = '...'
            page.update(get_main_page(page).body)

        def get_headers(df: pd.DataFrame) -> list:
            return [ft.DataColumn(
                ft.Text(header + f'\n{"Цель" if header is get_target() else ""}')
            ) for header in df.columns]

        def reload_data(event: flet_core.control_event.ControlEvent):
            set_target(event.control.data)

            sum_page = Page(page.body, [])
            sum_page.set_parent(page.parent)
            page.parent.pages[1] = get_summary_page(sum_page)

            reg_page = Page(page.body, [])
            reg_page.set_parent(page.parent)
            page.parent.pages[4] = get_reg_page(reg_page)

            page.update(get_main_page(page).body)

        def get_rows(df: pd.DataFrame) -> list:
            df_rows = []
            for index, row in df.iterrows():
                df_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(row[header]), data=header, on_tap=reload_data
                            ) for header in df.columns
                        ]
                    )
                )

            return df_rows

        def drop_column(event):
            set_data(Data(get_data().drop(columns=[drop_column_name.value], axis=1)))
            page.update(get_main_page(page).body)

        save_data = ""

        def save_file(event: ft.FilePickerResultEvent):
            global save_data
            path = event.path
            if path:
                try:
                    if save_data == "data":
                        get_dataframe().data_body.to_csv(path)
                        return

                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(save_data)
                except Exception as e:
                    print(f'Save error [{e}]')

            return 0

        save_dialog = ft.FilePicker(on_result=save_file)

        def save_file_dialog(event):
            global save_data
            if event.control.data == 'data':
                save_data = "data"
            else:
                save_data = str(summary())

            save_dialog.save_file()

        table = ft.DataTable(
            columns=get_headers(get_data()),
            rows=get_rows(get_data()),
            border=ft.border.all(2, 'black')
        )

        drop_column_row = ft.Row(
            [
                ft.IconButton(icon=ft.icons.DELETE, icon_color='black', on_click=drop_column, tooltip='Удалить'),
                drop_column_name
            ]
        )

        lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        lv.controls.append(ft.IconButton(ft.icons.CLOSE, icon_color='black', on_click=close_dataframe, tooltip='Закрыть'))

        lv.controls.append(drop_column_row)
        lv.controls.append(
            ft.Row(
                [
                    ft.TextButton('Нормализовать', style=ft.ButtonStyle(color='black'), on_click=normalize_dataframe),
                    ft.TextButton('Сохранить датасет', style=ft.ButtonStyle(color='black'), on_click=save_file_dialog, data='data'),
                    ft.TextButton('Сохранить отчёт', style=ft.ButtonStyle(color='black'), on_click=save_file_dialog, data='report')
                ]
            )
        )
        lv.controls.append(table)

        page.body.overlay.append(save_dialog)
        page.add_control(lv)

    return page
