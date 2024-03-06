import flet as ft


class DashboardView(ft.View):
    def __init__(self, page: ft.Page, user_id: str = None,):
        super().__init__()
        self.user_id = user_id
        self.appbar = ft.AppBar(
            bgcolor=ft.colors.TRANSPARENT,
        )

        self.controls = []
