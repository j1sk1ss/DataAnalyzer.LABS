import flet as ft
from pages.page import Page


def get_info_page(page: Page):
    page.clean_controls()

    page.add_control(
        ft.Row(
            [
                ft.Text('Авторы:\nРуководитель: Щудро Игорь Анатольевич\nРазработчик: Фот Николай Сергеевич\n'
                        'Описание: Программа для работы со статистическими данными. '
                        'Программа для корреляционного и регрессионного анализа')
            ]
        )
    )

    return page
