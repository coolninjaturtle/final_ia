import flet as ft
from views.recipe_card import RecipeCard


class LikedView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page


class ProfileView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page


class DashboardView(ft.View):
    def __init__(self, page: ft.Page, supabase, user_id: str = None,):
        super().__init__(route=f"/dashboard/{user_id}")
        self.supabase = supabase
        self.page = page
        self.appbar = ft.AppBar(
            bgcolor=ft.colors.TRANSPARENT,
            automatically_imply_leading=False,
            title=ft.Container(padding=ft.padding.only(bottom=10, left=5, top=10),
                               content=ft.Text(f"Hello, \n{self.supabase.current_user.email}!",
                                               theme_style=ft.TextThemeStyle.TITLE_LARGE
                                               )
                               ),
        )
        self.scroll = ft.ScrollMode.HIDDEN
        self.padding = ft.padding.only(bottom=10, top=10)
        self.vertical_alignment = ft.MainAxisAlignment.START,
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True

        self.user_id = user_id

        self.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, shape=ft.CircleBorder(),
                                                              on_click=self.new_recipe)
        self.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

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
                    supabase=self.supabase
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
                    ft.IconButton(icon=ft.icons.HOME, tooltip="Home", icon_color=ft.colors.WHITE,
                                  on_click=lambda e: self.page.update()),
                    ft.IconButton(icon=ft.icons.FAVORITE, tooltip="Favourites"),
                    ft.IconButton(icon=ft.icons.PERSON, tooltip="Profile"),
                ]
            )
        )

    def new_recipe(self, e):
        self.page.go("/new_recipe")
