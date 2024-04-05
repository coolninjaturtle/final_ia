import flet as ft


class RecipeView(ft.View):
    def __init__(self, supabase, page, recipe_id):
        super().__init__()
        self.padding = 0

        self.page = page
        self.supabase = supabase
        self.recipe_id = recipe_id

        self.scroll = ft.ScrollMode.AUTO

        recipe_details = self.supabase.get_recipe_by_id(recipe_id=recipe_id)[0]
        self.title = recipe_details["recipe_name"]
        self.ingredients = recipe_details["recipe_ingredients"]
        self.time = recipe_details["recipe_time"]
        self.process = recipe_details["recipe_process"]
        self.image_url = recipe_details["recipe_picture"]
        self.creator = recipe_details["creator"]

        self.appbar = ft.AppBar(
            title=ft.Text(f"{self.title}", font_family="Polly-Bold", size=25, weight=ft.FontWeight.BOLD),
            center_title=True,
        )

        self.ingredients_tab = ft.Tab(
            text="Ingredients",
            content=ft.Container(
                padding=10,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[]
                )
            )
        )

        for ingredient, quantity in self.ingredients.items():
            self.ingredients_tab.content.content.controls.append(
                ft.Text(
                    f"- {ingredient}: {quantity}",
                    weight=ft.FontWeight.NORMAL,
                    font_family="Polly-Regular",
                    size=20,
                    selectable=True
                )
            )

        self.instruction_tab = ft.Tab(
            text="Instructions",
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Container(
                            border_radius=10,
                            bgcolor=ft.colors.TRANSPARENT,
                            border=ft.border.all(5, color="#50C878"),
                            padding=10,
                            content=ft.TextField(
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                multiline=True,
                                value=self.process,
                                disabled=True,
                                border_width=0,
                                text_style=ft.TextStyle(color=ft.colors.WHITE)
                            ),
                        )
                    )
                ]
            ),
        )

        self.photo_tab = ft.Tab(
            text="Photo",
            content=ft.Column(
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        image_src=self.image_url,
                        image_fit=ft.ImageFit.FILL,
                        width=self.page.width,
                        height=self.page.height,
                    )
                ]
            ),
        )

        self.tabs = ft.Tabs(
            indicator_tab_size=True,
            tab_alignment=ft.TabAlignment.CENTER,
            selected_index=0,
            tabs=[self.ingredients_tab, self.instruction_tab, self.photo_tab],
        )

        self.function_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color=ft.colors.WHITE,
                    on_click=self.edit_recipe,
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.WHITE,
                    on_click=self.delete_recipe,
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.SHARE,
                    icon_color=ft.colors.WHITE,
                    on_click=self.share_recipe,
                    icon_size=20,
                )
            ]
        )

        self.controls = [self.function_row, self.tabs]

    def edit_recipe(self, e):
        if self.supabase.current_user.id != self.creator:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("You did not create this recipe, so you cannot edit it"),
                bgcolor=ft.colors.RED,
                open=True,
            )
            self.page.update()
        else:
            pass

    def delete_recipe(self, e):
        self.supabase.sever_relationship(recipe_id=self.recipe_id)
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)

    def share_recipe(self, e):
        self.page.set_clipboard(self.recipe_id)
        self.page.snack_bar = ft.SnackBar(
            ft.Text("Recipe ID copied to clipboard, please share with friends"),
            bgcolor=ft.colors.GREEN,
            open=True,
        )
        self.page.update()
