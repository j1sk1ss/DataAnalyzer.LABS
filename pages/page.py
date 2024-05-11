import flet as ft

from pages.menu import Menu


class Page:
    def __init__(self, page: ft.Page, components: list):
        self.body = page
        self.body_components = components
        self.parent = None

    def set_parent(self, parent: Menu):
        self.parent = parent

    def update(self, page: ft.Page):
        self.body = page
        if self.parent is not None:
            self.parent.update_page(self)
        else:
            print('[Error] Page without parent')

    def load(self):
        self.body.controls.clear()
        for c in self.body_components:
            self.body.add(c)

        self.body.update()

    def add_control(self, control):
        self.body_components.append(control)

    def add_temp_control(self, control):
        self.body.add(control)
        self.body.update()

    def delete_control(self, control_data):
        for control in self.body.controls:
            if control.data == control_data:
                self.body_components.remove(control)
                break

    def delete_temp_control(self, control_data):
        for control in self.body.controls:
            if control.data == control_data:
                self.body.controls.remove(control)
                break

        self.body.update()

    def clean_controls(self):
        self.body_components.clear()
