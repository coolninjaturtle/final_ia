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

        self.appbar = ft.AppBar(
            title=ft.Text(f"{self.title}", font_family="Polly-Bold", size=20, weight=ft.FontWeight.BOLD),
        )

