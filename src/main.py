# test.py
import flet as ft
import asyncio
from Title_animation import GradientAnimatedTextContainer
from data import start_text


class Survey(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(bgcolor=ft.Colors.BLACK, expand=True, padding=5)
        self.page = page
        self.language = "en"
        self.current_page = "intro"
        self.question_manager = None
        self.is_completed = False

        self.title_text = GradientAnimatedTextContainer(
            value="Desires After Duties",
            font_family="title_font",
            no_wrap=False
        )

        self.language_slider = ft.SegmentedButton(
            selected={"0"},
            allow_multiple_selection=False,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            segments=[
                ft.Segment(value="0", label=ft.Text("Eng")),
                ft.Segment(value="1", label=ft.Text("বাংলা")),
            ],
            on_change=self.change_language,
            col={"xs": 6, "sm": 2, "md": 2, "lg": 2},
        )

        self.main_content_controls = ft.Column(
            spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.main_content_container_column = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            col={"xs": 12, "sm": 6, "md": 4, "lg": 4},
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    bgcolor="#fdf6e3",
                                    padding=ft.padding.all(10),
                                    content=self.main_content_controls,
                                )
                            ],
                        )
                    ],
                )
            ],
        )

        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Divider(color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            col={"xs": 12},
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[self.title_text],
                        )
                    ],
                ),
                ft.Divider(color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow(
                    controls=[self.language_slider],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=False,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.main_content_container_column,
            ],
        )

        self._refresh_content()

    def _create_intro_controls(self):
        """Intro page content based on current language"""
        t = start_text[self.language]
        return [
            ft.Text(
                value=t["welcome"],
                size=25,
                font_family="Arial",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_900,
            ),
            ft.Text(value=t["request"], size=20, color=ft.Colors.BLUE_GREY_500),
            ft.Text(
                value=t["description"],
                size=12,
                color=ft.Colors.BLACK,
                text_align=ft.TextAlign.JUSTIFY,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(name=ft.Icons.TIMER_ROUNDED, color=ft.Colors.BLACK),
                            ft.Text(
                                value=t["time"],
                                weight=ft.FontWeight.BOLD,
                                size=12,
                                color=ft.Colors.BLACK,
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(
                                name=ft.Icons.ENHANCED_ENCRYPTION_ROUNDED,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Text(
                                value=t["anonymous"],
                                weight=ft.FontWeight.BOLD,
                                size=12,
                                color=ft.Colors.BLACK,
                            ),
                        ],
                    ),
                ],
            ),
            ft.Divider(),
            ft.ElevatedButton(
                text=t["button"],
                bgcolor=ft.Colors.BLUE_GREY_200,
                color=ft.Colors.BLACK,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                on_click=self.clicked_start_survey,
            ),
        ]

    def _create_questionnaire_controls(self):
        """Survey questions page based on current language"""
        from survey import general_info_questions

        if self.question_manager is None:
            self.question_manager = general_info_questions(self.page, self.language,
                                                           on_complete=self.on_survey_complete)
            return [self.question_manager.main_container]
        else:
            self.question_manager.update_language(self.language)
            return [self.question_manager.main_container]

    def _refresh_content(self):
        """Rebuilds UI depending on current_page and language"""
        self.main_content_controls.controls.clear()

        if self.current_page == "intro":
            self.main_content_controls.controls.extend(self._create_intro_controls())
        elif self.current_page == "questionnaire":
            self.main_content_controls.controls.extend(self._create_questionnaire_controls())

        self.page.update()

    def on_survey_complete(self):
        """Set a flag when the survey is fully completed"""
        self.is_completed = True

    def change_language(self, e):
        """Handles language toggle globally"""
        selected_value = list(e.control.selected)[0]
        if selected_value == "0":
            self.language = "en"
        else:
            self.language = "bn"

        if self.is_completed:
            # If the survey is completed, just update the end message
            self.question_manager.end_message_control.value = "Thank you for completing the survey!" if self.language == "en" else "জরিপটি সম্পূর্ণ করার জন্য আপনাকে ধন্যবাদ!"
            self.page.update()
        else:
            # If not completed, refresh the whole content
            self._refresh_content()

    def on_view_change(self, e):
        """Responsive title size adjustment"""
        if self.page.width < 600:
            self.title_text.text_control.size = 25
        elif self.page.width < 900:
            self.title_text.text_control.size = 40
        else:
            self.title_text.text_control.size = 50
        self.page.update()

    def clicked_start_survey(self, e):
        """Switch to questionnaire"""
        self.current_page = "questionnaire"
        self._refresh_content()


# --------- LOADING LOGIC ----------
async def load_survey(page: ft.Page):
    page.update()
    await asyncio.sleep(0.1)

    page.controls.clear()
    survey_container = Survey(page)
    page.on_resized = survey_container.on_view_change
    page.add(survey_container)

    page.run_task(survey_container.title_text.animate_gradient_task)
    survey_container.on_view_change(None)

    page.update()


async def main(page: ft.Page):
    page.title = "Survey"
    page.spacing = 0
    page.padding = 0
    page.fonts = {
        "title_font": "ZenDots-Regular.ttf",
        "fancy": "CherryBombOne-Regular.ttf",
    }

    loading_screen = ft.Column(
        [
            ft.ProgressRing(),
            ft.Text("Loading survey...", size=20, color=ft.Colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    page.controls.clear()
    page.add(loading_screen)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    await load_survey(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")