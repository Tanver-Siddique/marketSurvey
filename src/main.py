import flet as ft
import asyncio
from Title_animation import GradientAnimatedTextContainer # Assuming this class exists and animate_gradient_task is async


class Survey(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            bgcolor=ft.Colors.BLACK,
            expand=True,
            padding=5,
        )
        self.page = page
        self.language = "bn"  # default English

        # Text values for bilingual support - these are loaded once
        self.texts = {
            "en": {
                "welcome": "Welcome",
                "request": "Request for Your Opinion",
                "description": (
                    "We're conducting a brief survey to understand how people spend their money "
                    "once their essential needs are met. Your insights are incredibly important "
                    "as they help us understand evolving consumer priorities and lifestyle trends. "
                    "This information can guide businesses in developing products and services that "
                    "truly align with what people want beyond their basic needs."
                ),
                "time": "5-7 Minutes",
                "anonymous": "Anonymous",
                "button": "Start Survey",
            },
            "bn": {
                "welcome": "স্বাগতম",
                "request": "আপনার মতামত প্রার্থনা করছি",
                "description": (
                    "আমরা একটি সংক্ষিপ্ত জরিপ পরিচালনা করছি, যাতে বোঝা যায় মানুষ তাদের মৌলিক "
                    "প্রয়োজন মেটানোর পর কীভাবে টাকা ব্যয় করে। আপনার মতামত আমাদের জন্য অত্যন্ত "
                    "গুরুত্বপূর্ণ কারণ এটি পরিবর্তিত ভোক্তা অগ্রাধিকার ও জীবনযাপনের প্রবণতা বুঝতে সাহায্য করে। "
                    "এই তথ্য ব্যবসাকে এমন পণ্য ও সেবা উন্নয়নে সহায়তা করবে যা মানুষের প্রকৃত চাহিদার সাথে সামঞ্জস্যপূর্ণ।"
                ),
                "time": "৫-৭ মিনিট",
                "anonymous": "গোপনীয়",
                "button": "জরিপ শুরু করুন",
            }
        }

        # Title control (initialized once, its value will be updated)
        self.title_text = GradientAnimatedTextContainer(
            value="Desires After Duties",
            font_family="title_font",
            no_wrap=False
        )

        # Language slider title control (initialized once, its value will be updated)
        self.language_slider_title = ft.Text(
            value="Select language:",
            color=ft.Colors.WHITE,
            size=20
        )

        # Language slider control (initialized once)
        self.language_slider = ft.SegmentedButton(
            selected={"1"},
            allow_multiple_selection=False,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            segments=[
                ft.Segment(value="0", label=ft.Text("Eng")),
                ft.Segment(value="1", label=ft.Text("বাংলা"))
            ],
            on_change=self.change_language
        )

        # Placeholder for the main content container. It will be built later.
        self.main_content_container_column = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[] # Initially empty
        )

        # Define the overall page layout with placeholders
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
                            controls=[self.title_text]
                        )
                    ]
                ),
                ft.Divider(color=ft.Colors.TRANSPARENT),
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            controls=[
                                self.language_slider_title,
                                self.language_slider
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                ),
                self.main_content_container_column # This column will hold the dynamically loaded content
            ],
        )

        # Initially build and load the main content
        self._load_main_content()


    def _create_main_content_controls(self):
        """
        Creates and returns a list of controls for the main survey introduction
        based on the current language. These controls are created "on demand."
        """
        t = self.texts[self.language]
        return ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 4},
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            bgcolor="#fdf6e3",
                            padding=ft.padding.all(10),
                            content=ft.Column(
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value=t["welcome"],
                                        size=25,
                                        font_family="Arial",
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_GREY_900
                                    ),
                                    ft.Text(
                                        value=t["request"],
                                        size=20,
                                        color=ft.Colors.BLUE_GREY_500
                                    ),
                                    ft.Text(
                                        value=t["description"],
                                        size=12,
                                        color=ft.Colors.BLACK,
                                        text_align=ft.TextAlign.JUSTIFY
                                    ),
                                    # Info row
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        controls=[
                                            ft.Row(
                                                spacing=4,
                                                controls=[
                                                    ft.Icon(
                                                        name=ft.Icons.TIMER_ROUNDED,
                                                        color=ft.Colors.BLACK
                                                    ),
                                                    ft.Text(
                                                        value=t["time"],
                                                        weight=ft.FontWeight.BOLD,
                                                        size=12,
                                                        color=ft.Colors.BLACK
                                                    )
                                                ]
                                            ),
                                            ft.Row(
                                                spacing=4,
                                                controls=[
                                                    ft.Icon(
                                                        name=ft.Icons.ENHANCED_ENCRYPTION_ROUNDED,
                                                        color=ft.Colors.BLACK
                                                    ),
                                                    ft.Text(
                                                        value=t["anonymous"],
                                                        weight=ft.FontWeight.BOLD,
                                                        size=12,
                                                        color=ft.Colors.BLACK
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    ft.Divider(),
                                    ft.ElevatedButton(
                                        text=t["button"],
                                        bgcolor=ft.Colors.BLUE_GREY_200,
                                        color=ft.Colors.BLACK,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=5)
                                        )
                                    )
                                ],
                            ),
                        )
                    ],
                )
            ],
        )

    def _load_main_content(self):
        """
        Loads (creates) the main content and places it into the main_content_container_column.
        This method replaces the entire content if it already exists.
        """
        # Clear existing content if any
        self.main_content_container_column.controls.clear()
        # Add the newly created content
        self.main_content_container_column.controls.append(self._create_main_content_controls())


    async def change_language(self, e):
        """Handles slider toggle between EN ("0") and BN ("1")"""
        selected_value = list(e.control.selected)[0]

        if selected_value == "0":
            self.language = "en"
            self.language_slider_title.value = "Select language:"
        else:  # selected_value == "1"
            self.language = "bn"
            self.language_slider_title.value = "ভাষা নির্বাচন করুনঃ"


        # Re-create and load the main content for the new language
        self._load_main_content()

        self.page.update() # Corrected: Removed await


    def on_view_change(self, e):
        # The title_text itself is a GradientAnimatedTextContainer, which likely
        # has a text_control property that holds the ft.Text object.
        # This part assumes your GradientAnimatedTextContainer correctly exposes it.
        if self.page.width < 600:
            self.title_text.text_control.size = 25
        elif self.page.width < 900:
            self.title_text.text_control.size = 40
        else:
            self.title_text.text_control.size = 50
        self.page.update()


# ---------LOADING LOGIC HERE ----------
async def load_survey(page: ft.Page):
    page.controls.clear()
    survey_container = Survey(page)
    page.on_resized = survey_container.on_view_change
    page.add(survey_container)

    # Start title animation (assuming animate_gradient_task is an async method)
    # The 'None' argument in on_view_change is standard for initial calls,
    # it simulates the event argument.
    page.run_task(survey_container.title_text.animate_gradient_task)
    survey_container.on_view_change(None)

    page.update() # Corrected: Removed await


async def main(page: ft.Page):
    page.title = "Survey"
    page.spacing = 0
    page.padding = 0
    page.fonts = {
        "title_font": "ZenDots-Regular.ttf",
        "fancy": "CherryBombOne-Regular.ttf"
    }

    # Show loading screen immediately
    loading_screen = ft.Column(
        [
            ft.ProgressRing(),
            ft.Text("Loading survey...", size=20, color=ft.Colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.controls.clear()
    page.add(loading_screen)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update() # Corrected: Removed await

    # Load survey after delay in the background
    await load_survey(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

