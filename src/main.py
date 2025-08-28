import flet as ft
import asyncio
import random


def get_random_color():
    """Generates a random hex color string."""
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"


def main(page: ft.Page):
    page.title = "Animated Gradient Text"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK

    text_content = ft.Text(
        "Flet Animation",
        size=70,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
    )

    animated_gradient_text = ft.ShaderMask(
        content=text_content,
        blend_mode=ft.BlendMode.SRC_IN,
        shader=ft.LinearGradient(
            # Initial colors and gradient setup
            begin=ft.alignment.Alignment(-1.5, 0),
            end=ft.alignment.Alignment(0.5, 0),
            colors=[ft.Colors.CYAN_700, ft.Colors.ORANGE_300, ft.Colors.CYAN_700],
            stops=[0.0, 0.5, 1.0]
        )
    )

    page.add(animated_gradient_text)

    async def animate_gradient():
        begin_x = -1.5
        end_x = 0.5
        step = 0.02
        moving_right = True

        while True:
            if moving_right:
                begin_x += step
                end_x += step
                if begin_x >= 1.5:
                    moving_right = False
            else:  # Moving left
                begin_x -= step
                end_x -= step
                if end_x <= -0.5:
                    moving_right = True

                    # --- NEW: Generate and apply new random colors
                    animated_gradient_text.shader.colors = [
                        get_random_color(),
                        get_random_color(),
                        get_random_color()
                    ]

            animated_gradient_text.shader.begin = ft.alignment.Alignment(begin_x, 0)
            animated_gradient_text.shader.end = ft.alignment.Alignment(end_x, 0)

            page.update()
            await asyncio.sleep(0.016)

    page.run_task(animate_gradient)


if __name__ == "__main__":
    ft.app(target=main)