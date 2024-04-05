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

        self.title_bar = ft.TextField(
            value=self.title,
            text_align=ft.TextAlign.CENTER,
            border_color=ft.colors.TRANSPARENT,
            text_size=20,
            text_style=ft.TextStyle(
                font_family="Polly Bold",
                weight=ft.FontWeight.BOLD,
            ),
            color=ft.colors.WHITE,
            disabled=True,
            border_width=0,
        )

        self.action_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color=ft.colors.WHITE,
                    tooltip="Edit",
                    on_click=self.edit_recipe,
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.SHARE,
                    icon_color=ft.colors.WHITE,
                    tooltip="Share",
                    on_click=self.share_recipe,
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.WHITE,
                    tooltip="Delete",
                    on_click=self.delete_recipe,
                    icon_size=20,
                ),
            ],
        )

        self.appbar = ft.AppBar(
            automatically_imply_leading=False,
            title=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                controls=[
                    self.title_bar,
                    self.action_row,
                ],
            ),
            center_title=True,
            toolbar_height=100,
            bgcolor=ft.colors.TRANSPARENT,
        )

        self.floating_action_button = ft.FloatingActionButton(
            shape=ft.CircleBorder(),
            icon=ft.icons.CANCEL,
            on_click=self.go_back,
        )
        self.floating_action_button_location = (
            ft.FloatingActionButtonLocation.CENTER_FLOAT
        )

        self.lv = ft.Column(
            spacing=0,
            auto_scroll=True,
            controls=[],
            disabled=True,
        )

        for ingredient, quantity in self.ingredients.items():
            self.lv.controls.append(
                ft.Container(
                    padding=ft.padding.all(10),
                    content=ft.ResponsiveRow(
                        controls=[
                            ft.TextField(
                                value=ingredient,
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                col={"xs": 4},
                                color=ft.colors.WHITE,
                                border_width=0,
                                hint_text="Ingredient",
                                multiline=True,
                            ),
                            ft.TextField(
                                value=quantity.split(" ")[0],
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                col={"xs": 4},
                                color=ft.colors.WHITE,
                                border_width=0,
                                hint_text="Quantity",
                                multiline=True,
                            ),
                            ft.TextField(
                                value=quantity.split(" ")[1],
                                border_color=ft.colors.TRANSPARENT,
                                text_align=ft.TextAlign.CENTER,
                                col={"xs": 4},
                                color=ft.colors.WHITE,
                                border_width=0,
                                hint_text="Unit",
                                multiline=True,
                            ),
                        ],
                    ),
                ),
            )

        self.add_recipe_button = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color=ft.colors.WHITE,
            tooltip="Add",
            on_click=self.add_ingredient,
        )

        self.ingredients_tab = ft.Tab(
            text="Ingredients",
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.lv,
                ],
            ),
        )

        self.instructions = ft.TextField(
            border_color=ft.colors.TRANSPARENT,
            text_align=ft.TextAlign.CENTER,
            multiline=True,
            value=self.process,
            disabled=True,
            border_width=0,
            color=ft.colors.WHITE,
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
                            content=self.instructions,
                        ),
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

        self.controls = [self.tabs]

    def go_back(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)

    def edit_recipe(self, e):
        if self.supabase.current_user.id != self.creator:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("You did not create this recipe, so you cannot edit it"),
                bgcolor=ft.colors.RED,
                open=True,
            )
            self.page.update()
        else:
            self.action_row.visible = False
            self.appbar.toolbar_height = 60
            self.lv.disabled = False
            self.instructions.disabled = False
            self.title_bar.disabled = False
            self.ingredients_tab.content.controls.append(self.add_recipe_button)
            self.tabs.on_change = self.tab_change
            self.floating_action_button = None
            self.bottom_appbar = ft.BottomAppBar(
                elevation=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton("Cancel", on_click=self.go_back),
                        ft.VerticalDivider(thickness=2),
                        ft.TextButton("Confirm", on_click=self.confirm),
                    ],
                )
            )
            self.update()

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

    def add_ingredient(self, e):
        self.lv.controls.append(
            ft.Container(
                padding=ft.padding.all(10),
                content=ft.ResponsiveRow(
                    controls=[
                        ft.TextField(
                            border_color=ft.colors.TRANSPARENT,
                            text_align=ft.TextAlign.CENTER,
                            col={"xs": 4},
                            color=ft.colors.WHITE,
                            border_width=0,
                            hint_text="Ingredient",
                            multiline=True,
                        ),
                        ft.TextField(
                            border_color=ft.colors.TRANSPARENT,
                            text_align=ft.TextAlign.CENTER,
                            col={"xs": 4},
                            color=ft.colors.WHITE,
                            border_width=0,
                            hint_text="Quantity",
                            multiline=True,
                        ),
                        ft.TextField(
                            border_color=ft.colors.TRANSPARENT,
                            text_align=ft.TextAlign.CENTER,
                            col={"xs": 4},
                            color=ft.colors.WHITE,
                            border_width=0,
                            hint_text="Unit",
                            multiline=True,
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

    def confirm(self, e):
        ingredients = {}
        for val in self.lv.controls:
            item = val.content.controls[0].value
            quantity = val.content.controls[1].value
            unit = val.content.controls[2].value
            ingredients[item] = f"{quantity} {unit}"
        try:
            if self.photo_tab.content.controls[0].image_src != self.image_url:
                self.supabase.edit_recipe(
                    title=self.title_bar.value,
                    ingredients=ingredients,
                    process=self.instruction_tab.content.controls[0].content.content.value,
                    photo=self.photo_tab.content.controls[0].image_src,
                    recipe_id=self.recipe_id
                )
            else:
                self.supabase.edit_recipe(
                    title=self.title_bar.value,
                    ingredients=ingredients,
                    process=self.instruction_tab.content.controls[0].content.content.value,
                    recipe_id=self.recipe_id
                )
            self.page.views.pop()
            self.page.go(self.page.views[-1].route)
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(e)), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()

