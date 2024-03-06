import flet as ft


class OpeningView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        self.padding = 0
        self.bg_image = ft.Row(
            expand=True,
            controls=[ft.ShaderMask(
                ft.Image(src="assets/bg_image.jpg", fit=ft.ImageFit.FILL, height=1155),
                blend_mode=ft.BlendMode.DST_IN,
                expand=True,
                shader=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.colors.BLACK, ft.colors.TRANSPARENT],
                    stops=[0.3, 1.0],
                ),
            )],
        )

        self.text_and_button_container = ft.Container(
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=90, left=5, right=5),
            content=ft.Column(
                expand=True,
                spacing=35,
                controls=[
                    ft.Text(
                        "Document Your Favorite Recipes!",
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                        style=ft.TextStyle(
                            color=ft.colors.WHITE,
                            size=30,
                            shadow=ft.BoxShadow(color=ft.colors.BLACK, offset=ft.Offset(2, 3)),
                            font_family="Polly Bold",
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                    ft.ElevatedButton(
                        width=200,
                        height=70,
                        on_click=lambda _: page.go("/login"),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Container(bgcolor=ft.colors.WHITE, width=50, height=50, border_radius=100,
                                             content=ft.Icon(ft.icons.ARROW_RIGHT, color="#50C878", size=50),
                                             alignment=ft.alignment.center),
                                ft.Text("Get Started", color=ft.colors.WHITE, font_family="Polly Bold",
                                        weight=ft.FontWeight.BOLD, size=19),
                            ]
                        ),
                        style=ft.ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT: ft.StadiumBorder(),
                                ft.MaterialState.PRESSED: ft.RoundedRectangleBorder(radius=20),
                            },
                            bgcolor="#50C878",
                            padding=ft.padding.only(left=10, top=10, bottom=10),
                        )
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.END,
            )
        )

        self.background_container = ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Stack(
                expand=True,
                controls=[
                    self.bg_image,
                    self.text_and_button_container,
                ]
            ),
        )

        self.controls = [self.background_container]
