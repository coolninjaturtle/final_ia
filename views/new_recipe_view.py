import flet as ft


class NewRecipeView(ft.View):
    def __init__(self, supabase, page):
        super().__init__()
        self.padding = 0

        self.page = page
        self.supabase = supabase

        self.scroll = ft.ScrollMode.AUTO

        self.title_bar = ft.TextField(
            text_align=ft.TextAlign.CENTER,
            border_color=ft.colors.TRANSPARENT,
            hint_text="Title Here",
            text_size=20,
            text_style=ft.TextStyle(
                font_family="Polly Bold",
                weight=ft.FontWeight.BOLD,
            ),
            hint_style=ft.TextStyle(
                font_family="Polly Bold",
                weight=ft.FontWeight.BOLD,
            ),
            autofocus=True,
        )
        self.appbar = ft.AppBar(
            title=self.title_bar,
            center_title=True,
            automatically_imply_leading=False,
        )
        self.bottom_appbar = ft.BottomAppBar(
            elevation=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.TextButton("Cancel", on_click=self.cancel),
                    ft.VerticalDivider(thickness=2),
                    ft.TextButton("Confirm", on_click=self.confirm),
                ],
            )
        )

        self.lv = ft.Column(
            spacing=0,
            auto_scroll=True,
            controls=[
                ft.Container(
                    padding=ft.padding.all(10),
                    content=ft.ResponsiveRow(
                        controls=[
                            ft.TextField(
                                hint_text="Ingredient",
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                col={"xs": 4},
                            ),
                            ft.TextField(
                                hint_text="Quantity",
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                col={"xs": 4},
                            ),
                            ft.TextField(
                                hint_text="Unit",
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                col={"xs": 4},
                            ),
                        ],
                    ),
                ),
            ],
        )

        self.ingredients_tab = ft.Tab(
            text="Ingredients",
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.lv,
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_color=ft.colors.WHITE,
                        on_click=self.add_ingredient,
                    ),
                ],
            ),
        )

        self.instruction_tab = ft.Tab(
            text="Instructions",
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Container(
                            height=self.page.height,
                            border_radius=10,
                            bgcolor=ft.colors.TRANSPARENT,
                            border=ft.border.all(5, color="#50C878"),
                            padding=10,
                            content=ft.TextField(
                                hint_text="Enter Instruction",
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                multiline=True,
                                autofocus=True,
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
                        image_src=None,
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
            on_change=self.tab_change,
        )

        self.controls = [self.tabs]

    def confirm(self, e):

        def dialog_trick(e):
            if time_dialog.content.value != "":
                self.page.dialog.open = False
                self.page.update()
                act_process()
            else:
                time_dialog.content.error_text = "Pstop being a bbitch"
                self.page.update()

        def act_process():
            ingredients = {}
            for val in self.lv.controls:
                item = val.content.controls[0].value
                quantity = val.content.controls[1].value
                unit = val.content.controls[2].value
                ingredients[item] = f"{quantity} {unit}"
            try:
                self.supabase.insert_new_recipe(
                    title=self.title_bar.value,
                    ingredients=ingredients,
                    process=self.instruction_tab.content.controls[0].content.content.value,
                    time=time_dialog.content.value,
                    photo=self.photo_tab.content.controls[0].image_src
                )
                print(f"/dashboard/{self.supabase.current_user.id}")
                self.page.views.pop()
                self.page.go(self.page.views[-1].route)
            except Exception as e:
                self.page.snack_bar = ft.SnackBar(ft.Text(str(e)), bgcolor=ft.colors.RED)
                self.page.snack_bar.open = True
                self.page.update()

        time_dialog = ft.AlertDialog(
            title=ft.Text("Time Required to Complete Recipe"),
            modal=True,
            content=ft.TextField(
                border_color=ft.colors.TRANSPARENT,
                text_align=ft.TextAlign.CENTER,
                hint_text="Enter Time",
            ),
            open=True,
            actions=[ft.TextButton("Confirm", on_click=dialog_trick)],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.dialog = time_dialog
        self.page.update()

    def cancel(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)

    def add_ingredient(self, e):
        self.lv.controls.append(
            ft.Container(
                padding=ft.padding.all(10),
                content=ft.ResponsiveRow(
                    controls=[
                        ft.TextField(
                            hint_text="Ingredient",
                            border_color=ft.colors.TRANSPARENT,
                            text_align=ft.TextAlign.CENTER,
                            col={"xs": 4},
                        ),
                        ft.TextField(
                            hint_text="Quantity",
                            border_color=ft.colors.TRANSPARENT,
                            text_align=ft.TextAlign.CENTER,
                            col={"xs": 4},
                        ),
                        ft.TextField(
                            hint_text="Unit",
                            border_color=ft.colors.TRANSPARENT,
                            text_align=ft.TextAlign.CENTER,
                            col={"xs": 4},
                        ),
                    ],
                ),
            ),
        )
        self.update()

    def tab_change(self, e):
        if self.tabs.selected_index == 2:
            self.floating_action_button = ft.FloatingActionButton(
                shape=ft.CircleBorder(),
                icon=ft.icons.CAMERA,
                on_click=self.pick_photo,
            )
            self.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT
        else:
            self.floating_action_button = None
        self.update()

    def pick_photo(self, e):
        def photo_picked(result):
            if result.files:
                image = result.files[0]
                self.photo_tab.content.controls[0].image_src = image.path
                self.update()
            else:
                print("Photo picking was cancelled.")

        file_picker = ft.FilePicker(on_result=photo_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)

