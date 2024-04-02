import flet as ft


class NewRecipeView(ft.View):
    def __init__(self, supabase, page):
        super().__init__()
        self.padding = 0

        self.page = page
        self.supabase = supabase

        self.title_bar = ft.TextField(
            text_align=ft.TextAlign.CENTER,
            border_color=ft.colors.TRANSPARENT,
            hint_text="Title Here",
        )
        self.appbar = ft.AppBar(
            title=self.title_bar,
            center_title=True,
            automatically_imply_leading=False,
        )
        self.bottom_appbar = ft.BottomAppBar(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.TextButton("Confirm", on_click=self.confirm),
                    ft.VerticalDivider(thickness=2),
                    ft.TextButton("Cancel", on_click=self.cancel),
                ],
            )
        )

        self.ingredients_tab = ft.Tab(
            text="Ingredients",
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.TextField(
                                border_color=ft.colors.TRANSPARENT,
                                hint_text="Ingredient Name"
                            ),
                            ft.TextField(
                                border_color=ft.colors.TRANSPARENT,
                                hint_text="Quantity",
                            ),
                            ft.TextField(
                                border_color=ft.colors.TRANSPARENT,
                                hint_text="Unit",
                            )
                        ]
                    ),
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_color=ft.colors.WHITE,
                        on_click=self.add_ingredient
                    )
                ]
            ),
        )

        tabs = ft.Tabs(
            tab_alignment=ft.TabAlignment.CENTER,
            selected_index=0,
            tabs=[
                self.ingredients_tab,
                ft.Tab(
                    text="Instructions",
                ),
            ],
        )

        self.controls = [tabs]

    def confirm(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)

    def cancel(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)

    def add_ingredient(self, e):
        pass
