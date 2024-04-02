import flet as ft


class RecipeCard(ft.UserControl):
    def __init__(self, supabase, page, title, time, number_of_ingredients, data, image_url=None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.title = title
        self.data = title
        self.time = time
        self.number_of_ingredients = number_of_ingredients
        self.image_url = image_url
        self.data = data
        self.supabase = supabase

        self.text_content = ft.Column(
            controls=[
                ft.Text(
                    self.title,
                    style=ft.TextStyle(
                        color=ft.colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        shadow=ft.BoxShadow(color="black", offset=ft.Offset(1.5, 3.5)),
                    ),
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            self.time,
                            style=ft.TextStyle(
                                color=ft.colors.WHITE,
                                size=14,
                                shadow=ft.BoxShadow(color="black", offset=ft.Offset(1.5, 3.5)),
                                weight=ft.FontWeight.W_500,
                            )
                        ),
                        ft.Container(width=2, height=15, bgcolor=ft.colors.WHITE),
                        ft.Text(
                            f"{self.number_of_ingredients} ingredients",
                            style=ft.TextStyle(
                                color=ft.colors.WHITE,
                                size=14,
                                shadow=ft.BoxShadow(color="black", offset=ft.Offset(1.5, 3.5)),
                                weight=ft.FontWeight.W_500,
                            )
                        ),
                    ]
                ),
            ]
        )

        self.card = ft.Card(
            width=250,
            height=300,
            content=ft.Container(
                image_src=image_url if image_url else "./assets/recipe-placeholder.jpg",
                border_radius=14,
                image_fit=ft.ImageFit.FILL,
                padding=ft.padding.all(10),
                content=ft.Container(content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    alignment=ft.MainAxisAlignment.END,
                    controls=[self.text_content],
                ),
                    on_click=lambda e: print("balls"),
                ),
            ),
        )

        self.fav_button = ft.FloatingActionButton(
            icon=ft.icons.FAVORITE if self.supabase.is_favorite(data, self.supabase.current_user.id) else ft.icons.FAVORITE_BORDER,
            bgcolor=ft.colors.PINK_300,
            on_click=self.toggle_favorite,
            tooltip="Favorite",
            shape=ft.CircleBorder(),
            height=35,
            width=35,
        )

    def build(self):
        return ft.Stack(
            controls=[
                self.card,
                self.fav_button
            ]
        )

    def toggle_favorite(self, e):
        if self.fav_button.icon == ft.icons.FAVORITE_BORDER:
            self.fav_button.icon = ft.icons.FAVORITE
            self.supabase.set_favorite(recipe_id=self.data, user_id=self.supabase.current_user.id, value=True)
        elif self.fav_button.icon == ft.icons.FAVORITE:
            self.fav_button.icon = ft.icons.FAVORITE_BORDER
            self.supabase.set_favorite(recipe_id=self.data, user_id=self.supabase.current_user.id, value=False)
        self.fav_button.update()
