import flet as ft

import supabase_wrapper


class LoginView(ft.View):
    def __init__(self, page: ft.Page, supabase: supabase_wrapper.SupaBaseWrapper):
        super().__init__(route="/login")
        self.appbar = ft.AppBar(
            bgcolor=ft.colors.TRANSPARENT,
        )
        self.page = page
        self.padding = ft.padding.only(bottom=40, left=20, right=20, top=10)
        self.supabase = supabase

        self.email_bar = ft.TextField(
            height=50,
            label="Email",
            label_style=ft.TextStyle(color="#50C878"),
            autofocus=True,
            hint_text="Enter Your Email",
            border_color="#50C878",
        )

        self.password_bar = ft.TextField(
            height=50,
            label="Password",
            label_style=ft.TextStyle(color="#50C878"),
            password=True,
            hint_text="Enter Your Password",
            can_reveal_password=True,
            border_color="#50C878",
        )

        self.login_content = ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Text(
                    "Log In",
                    font_family="Polly Bold",
                    theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                    color="#50C878",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(color=ft.colors.TRANSPARENT, height=10),
                self.email_bar,
                self.password_bar,
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            expand=True,
                            height=50,
                            content=ft.Text(
                                "Log In",
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                                font_family="Polly Bold",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            on_click=self.__login,
                            style=ft.ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                                    ft.MaterialState.PRESSED: ft.StadiumBorder(),
                                },
                                bgcolor="#50C878",
                                padding=10,
                            )
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text("Don't Have an Account?"),
                        ft.Text(
                            spans=[ft.TextSpan(
                                text="Sign Up!",
                                on_click=lambda _: self.page.go("/signup"),
                                style=ft.TextStyle(color="#50C878", font_family="Polly Bold"),
                            )]
                        )
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        self.controls = [self.login_content]

    def __login(self, e):
        self.controls[0].disabled = True
        self.update()
        login_message = self.supabase.sign_in(self.email_bar.value, self.password_bar.value)
        if login_message == "success":
            self.page.go(f"/dashboard/{self.supabase.current_user.id}")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(login_message), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            self.controls[0].disabled = False
            self.update()
