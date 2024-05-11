import flet as ft
from events import Events


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

        self.body.add(self.navigation)

        for c in self.pages[index].body_components:
            self.body.add(c)

        self.body.update()
