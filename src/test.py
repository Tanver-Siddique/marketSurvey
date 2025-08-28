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
                            bgcolor=ft.Colors.BLACK,
                            content=ft.Text(
                                value="""Hello, my name is tanver, i am from gazipur. I completed my graduation from Gopalgonj Science and Technology University.
                                Now, after each full back-and-forth animation, the gradient will shift to a brand new set of random colors, making the effect even more visually interesting.""",
                                color="white",
                                size=12,
                                font_family="Arial",
                                no_wrap=False
                            ),
                            padding=ft.padding.all(15)
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
        "title_font": "ZenDots-Regular.ttf"
    }

    page.on_resized = survey_container.on_view_change

    page.add(survey_container)

    page.run_task(survey_container.title_text.animate_gradient_task)

    survey_container.on_view_change(None)
    page.update()


# This is a crucial line for hosting. It tells Flet where to find the assets.
if __name__ == "__main__":
    ft.app(main, assets_dir="assets")