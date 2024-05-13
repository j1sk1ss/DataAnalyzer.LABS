import flet as ft


class Menu:
    def __init__(self, page: ft.Page, pages: list, navigation: ft.Row):
        self.body = page
        self.pages = pages
        self.navigation = navigation

        for page in self.pages:
            if page is not None:
                page.set_parent(self)
            else:
                print('[Warn] Page is None')

    def update_page(self, page):
        self.show_page(self.pages.index(page))

    def show_page(self, index):
        self.body.controls.clear()
        for i in range(len(self.navigation.controls)):
            if i == index:
                self.navigation.controls[i].icon_color = 'grey'
            else:
                self.navigation.controls[i].icon_color = 'black'

        self.body.add(
            ft.Container(
                    content=self.navigation,
                    alignment=ft.alignment.center,
                    width=1200,
                    height=60,
                    bgcolor=ft.colors.BLUE_50,
                    border_radius=ft.border_radius.all(5),
                )
        )

        try:
            for c in self.pages[index].body_components:
                self.body.add(c)
        except AttributeError:
            print('NoneType')

        self.body.update()
