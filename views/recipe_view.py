import flet as ft


class RecipeView(ft.View):
    def __init__(self):
        super().__init__()
        self.fullscreen_dialog = True
        self.appbar = ft.AppBar(
            title=ft.Text("Recipe"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(
                    icon=ft.icons.EDIT_OUTLINED,
                    icon_color=ft.colors.WHITE,
                    tooltip="Edit",)]
        )
