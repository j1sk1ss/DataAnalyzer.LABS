import flet as ft
import pandas as pd

from main import load_csv, data_is_loaded, get_data, set_data, summary


def main(page: ft.Page):
    page.title = 'Cordell Data Analyzer'
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.START

    # region [Main Page]
    # Main page ===========

    dataframe_name = ft.Text('...', width=1200)

    def get_headers(df: pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

    def get_rows(df: pd.DataFrame) -> list:
        df_rows = []
        for index, row in df.iterrows():
            df_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(row[header])) for header in df.columns]))
        return df_rows

    def open_main_page(e):
        page_reload()
        if not data_is_loaded():
            pick_files_dialog = ft.FilePicker(on_result=upload_file)
            upload_button = ft.IconButton(ft.icons.UPLOAD, on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False
            ), icon_color='black')

            page.add(
                ft.Row([
                        upload_button, pick_files_dialog,
                        dataframe_name
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        else:
            table = ft.DataTable(
                columns=get_headers(get_data()),
                rows=get_rows(get_data()),
                border=ft.border.all(2, 'black')
            )

            lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
            lv.controls.append(ft.IconButton(ft.icons.CLOSE, icon_color='black', on_click=lambda _: set_data(None)))
            lv.controls.append(table)

            page.add(lv)

        page.update()

    def upload_file(e: ft.FilePickerResultEvent):
        load_csv(e.files[0].path)

        dataframe_name.value = e.files[0].name
        dataframe_name.update()

    # endregion

    # region [Summary Page]
    # Summary page ===========
    def get_summary_rows(data: dict):
        rows = []
        for i in data.keys():
            rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(i)), ft.DataCell(ft.Text(data[i]))]))

        return rows

    def open_summary_page(e):
        page_reload()

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

            lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
            lv.controls.append(ft.IconButton(ft.icons.CLOSE, icon_color='black', on_click=lambda _: set_data(None)))
            lv.controls.append(table)

            page.add(lv)

        page.update()

    # endregion

    # Graphs page ===========
    def open_graphs_page(e):
        page.update()

    # Corr page ===========
    def open_corr_page(e):
        page.update()

    def page_reload():
        page.clean()

        page.add(
            ft.Row(
                [
                    ft.IconButton(ft.icons.HOME, icon_color='black', on_click=open_main_page),
                    ft.IconButton(ft.icons.SUMMARIZE, icon_color='black', on_click=open_summary_page),
                    ft.IconButton(ft.icons.AUTO_GRAPH, icon_color='black', on_click=open_graphs_page),
                    ft.IconButton(ft.icons.DATA_ARRAY, icon_color='black', on_click=open_corr_page)
                ],
            )
        )

        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.HOME, icon_color='black', on_click=open_main_page),
                ft.IconButton(ft.icons.SUMMARIZE, icon_color='black', on_click=open_summary_page),
                ft.IconButton(ft.icons.AUTO_GRAPH, icon_color='black', on_click=open_graphs_page),
                ft.IconButton(ft.icons.DATA_ARRAY, icon_color='black', on_click=open_corr_page)
            ],
        )
    )


ft.app(target=main)
