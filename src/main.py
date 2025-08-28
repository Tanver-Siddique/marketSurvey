import flet as ft
from Title_animation import GradientAnimatedTextContainer


class Survey(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            bgcolor=ft.Colors.BLACK,
            expand=True,
            padding=5,
        )
        self.page = page

        self.title_text = GradientAnimatedTextContainer(
            value="Desires After Duties",
            font_family="title_font",
            no_wrap=False
        )

        self.main_content_container = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            bgcolor="#fdf6e3",
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        value="Welcome",
                                        size=25,
                                        font_family="Arial",
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_GREY_900
                                    ),
                                    ft.Text(
                                        value="Request for Your Opinion",
                                        size=20,
                                        color=ft.Colors.BLUE_GREY_500
                                    ),
                                    ft.Text(
                                        value="We're conducting a brief survey to understand how people spend their money once their essential needs are met. Your insights are incredibly important as they help us understand evolving consumer priorities and lifestyle trends. This information can guide businesses in developing products and services that truly align with what people want beyond their basic needs.",
                                        size=12,
                                        color=ft.Colors.BLACK,
                                        text_align=ft.TextAlign.JUSTIFY
                                    ),
                                    ft.Container(
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        content=ft.Row(
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Icon(
                                                            name=ft.Icons.TIMER_ROUNDED,
                                                            color=ft.Colors.BLACK
                                                        ),
                                                        ft.Text(
                                                            value="5-7 Minutes",
                                                            weight=ft.FontWeight.BOLD,
                                                            size=12,
                                                            color=ft.Colors.BLACK
                                                        )
                                                    ]
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.Icon(
                                                            name=ft.Icons.ENHANCED_ENCRYPTION_ROUNDED,
                                                            color=ft.Colors.BLACK
                                                        ),
                                                        ft.Text(
                                                            value="Anonymous",
                                                            weight=ft.FontWeight.BOLD,
                                                            size=12,
                                                            color=ft.Colors.BLACK
                                                        )
                                                    ]
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                        )
                                    ),
                                    ft.Divider(),
                                    ft.ElevatedButton(
                                        text="Start Survey",
                                        bgcolor=ft.Colors.BLUE_GREY_200,
                                        color=ft.Colors.BLACK,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(
                                                radius=5
                                            )
                                        )
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=ft.padding.all(10)
                        )
                    ],
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 4},
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.content = ft.Column(
            expand=True,
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Column(
                            controls=[self.title_text],
                            col={"xs": 12},
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),

                ft.Column(
                    controls=[self.main_content_container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            ],
        )

    def on_view_change(self, e):
        if self.page.width < 600:
            self.title_text.text_control.size = 25
        elif self.page.width < 900:
            self.title_text.text_control.size = 40
        else:
            self.title_text.text_control.size = 50
        self.page.update()


def main(page: ft.Page):
    page.title = "Survey"
    page.spacing = 0
    page.padding = 0

    survey_container = Survey(page)

    # Use the relative path for the font
    page.fonts = {
        "title_font": "ZenDots-Regular.ttf",
        "fancy": "CherryBombOne-Regular.ttf"
    }

    page.on_resized = survey_container.on_view_change

    page.add(survey_container)

    page.run_task(survey_container.title_text.animate_gradient_task)

    survey_container.on_view_change(None)
    page.update()


# This is a crucial line for hosting. It tells Flet where to find the assets.
if __name__ == "__main__":
    ft.app(main, assets_dir="assets")