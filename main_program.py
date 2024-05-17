import flet as ft

from pages.menu import Menu
from pages.page import Page
from pages.page_constructors.corr_page import get_corr_page
from pages.page_constructors.graphs_page import get_graphs_page
from pages.page_constructors.info_page import get_info_page
from pages.page_constructors.main_page import get_main_page
from pages.page_constructors.reg_page import get_reg_page
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
        get_graphs_page(Page(page, [])), get_corr_page(Page(page, [])),
        get_reg_page(Page(page, [])), get_info_page(Page(page, []))
    ],
        ft.Row([
            ft.IconButton(ft.icons.HOME, on_click=lambda _:program.show_page(0), tooltip='Главная'),
            ft.IconButton(ft.icons.SUMMARIZE, on_click=lambda _:program.show_page(1), tooltip='Выборочная статистика'),
            ft.IconButton(ft.icons.AUTO_GRAPH, on_click=lambda _:program.show_page(2), tooltip='Графики'),
            ft.IconButton(ft.icons.DATA_ARRAY, on_click=lambda _:program.show_page(3), tooltip='Корреляция'),
            ft.IconButton(ft.icons.GRAPHIC_EQ, on_click=lambda _:program.show_page(4), tooltip='Регрессионный анализ'),
            ft.IconButton(ft.icons.INFO, on_click=lambda _: program.show_page(5), tooltip='Авторы'),
        ],
    ))
    # endregion

    program.show_page(0)


ft.app(target=main, assets_dir="assets")
