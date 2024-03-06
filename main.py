import flet as ft
from views.opening_view import OpeningView
from views.login_view import LoginView
from views.signup_view import SignupView
from views.dashboard_view import DashboardView
from views.recipe_view import RecipeView
from supabase_wrapper import SupaBaseWrapper


def main(page: ft.Page):
    page.title = "Recipe App"
    page.theme_mode = ft.ThemeMode.DARK

    supabase = SupaBaseWrapper()

    page.fonts = {
        "Polly Bold": "assets/fonts/Polly-Bold.ttf",
        "Polly Light": "assets/fonts/Polly-Light.ttf",
        "Polly Regular": "assets/fonts/Polly-Regular.ttf",
        "Polly Thin": "assets/fonts/Polly-Thin.ttf",
    }

    def route_change(e):
        troute = ft.TemplateRoute(page.route)
        if troute.match("/"):
            page.views.append(OpeningView(page=page))
        elif troute.match("/login"):
            if page.views[-1].route == "/login":
                page.views.pop()
            page.views.append(LoginView(page=page))
        elif troute.match("/signup"):
            if page.views[-1].route == "/signup":
                page.views.pop()
            page.views.append(SignupView(page=page, supabase=supabase))
        elif troute.match("/dashboard"):
            if page.views[-1].route == "/dashboard":
                page.views.pop()
            page.views.append(DashboardView(page=page))
        page.update()

    def view_pop(e):
        page.views.pop()
        page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")


ft.app(target=main, view=ft.AppView.FLET_APP, assets_dir="assets")
