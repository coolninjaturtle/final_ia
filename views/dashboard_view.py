import flet as ft
from views.recipe_card import RecipeCard


class DashboardView(ft.View):
    def __init__(
        self,
        page: ft.Page,
        supabase,
        user_id: str = None,
    ):
        super().__init__(route=f"/dashboard/{user_id}")
        self.supabase = supabase
        self.page = page
        self.appbar = ft.AppBar(
            bgcolor=ft.colors.TRANSPARENT,
            automatically_imply_leading=False,
            title=ft.Container(
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text("Hello,", font_family="Polly-Light", size=20),
                        ft.Text(
                            f"{self.supabase.current_user.email}!",
                            font_family="Polly-Bold",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
                padding=10,
            ),
            actions=[
                ft.IconButton(
                    icon=ft.icons.DOWNLOAD,
                    tooltip="Load Recipe",
                    on_click=self.load_recipe,
                )
            ]
        )
        self.scroll = ft.ScrollMode.HIDDEN
        self.padding = ft.padding.only(bottom=10, top=10)
        self.vertical_alignment = (ft.MainAxisAlignment.START,)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True

        self.user_id = user_id

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, shape=ft.CircleBorder(), on_click=lambda e: self.page.go("/new_recipe")
        )
        self.floating_action_button_location = (
            ft.FloatingActionButtonLocation.CENTER_DOCKED
        )

        all_recipes = self.supabase.get_all_recipes(user_id=self.user_id)

        for recipe in all_recipes:
            recipe = recipe["recipes"]

            recipe_id = recipe["recipe_id"]
            title = recipe["recipe_name"]
            ingredients = recipe["recipe_ingredients"]
            time = recipe["recipe_time"]
            image_url = recipe["recipe_picture"]

            self.controls.append(
                RecipeCard(
                    data=recipe_id,
                    page=self.page,
                    title=title,
                    time=time,
                    image_url=image_url,
                    number_of_ingredients=len(ingredients),
                    supabase=self.supabase,
                )
            )

        self.bottom_appbar = ft.BottomAppBar(
            shape=ft.NotchShape.CIRCULAR,
            height=100,
            bgcolor=ft.colors.BLUE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, tooltip="Home", on_click=self.home_tab, icon_color=ft.colors.WHITE),
                    ft.IconButton(icon=ft.icons.FAVORITE, tooltip="Favourites", on_click=self.favorites_tab),
                    ft.IconButton(icon=ft.icons.PERSON, tooltip="Profile", on_click=self.profile_tab),
                ],
            ),
        )

    def home_tab(self, e):
        self.controls.clear()
        self.bottom_appbar.content.controls[0].icon_color = ft.colors.WHITE
        self.bottom_appbar.content.controls[1].icon_color = None
        self.bottom_appbar.content.controls[2].icon_color = None
        all_recipes = self.supabase.get_all_recipes(user_id=self.user_id)

        for recipe in all_recipes:
            recipe = recipe["recipes"]

            recipe_id = recipe["recipe_id"]
            title = recipe["recipe_name"]
            ingredients = recipe["recipe_ingredients"]
            time = recipe["recipe_time"]
            image_url = recipe["recipe_picture"]

            self.controls.append(
                RecipeCard(
                    data=recipe_id,
                    page=self.page,
                    title=title,
                    time=time,
                    image_url=image_url,
                    number_of_ingredients=len(ingredients),
                    supabase=self.supabase,
                )
            )

        self.update()

    def favorites_tab(self, e):
        self.controls.clear()
        self.bottom_appbar.content.controls[0].icon_color = None
        self.bottom_appbar.content.controls[1].icon_color = ft.colors.WHITE
        self.bottom_appbar.content.controls[2].icon_color = None
        favorite_recipes = self.supabase.get_favorite_recipes(user_id=self.user_id)

        for recipe in favorite_recipes:
            recipe = recipe["recipes"]

            recipe_id = recipe["recipe_id"]
            title = recipe["recipe_name"]
            ingredients = recipe["recipe_ingredients"]
            time = recipe["recipe_time"]
            image_url = recipe["recipe_picture"]

            self.controls.append(
                RecipeCard(
                    data=recipe_id,
                    page=self.page,
                    title=title,
                    time=time,
                    image_url=image_url,
                    number_of_ingredients=len(ingredients),
                    supabase=self.supabase,
                )
            )

        self.update()

    def profile_tab(self, e):
        pass

    def load_recipe(self, e):
        def load_function(e):
            if self.page.dialog.content.value != "":
                self.page.dialog.open = False
                self.page.update()
                self.page.go(f"/recipe/{self.page.dialog.content.value}")
                self.supabase.set_relationship(user_id=self.user_id, recipe_id=self.page.dialog.content.value)
            else:
                self.page.dialog.content.error_text = "Please enter a time"
                self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Load Recipe"),
            modal=True,
            content=ft.TextField(
                border_color=ft.colors.TRANSPARENT,
                text_align=ft.TextAlign.CENTER,
                hint_text="Enter Code",
            ),
            open=True,
            actions=[ft.TextButton("Load", on_click=load_function)],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.update()
