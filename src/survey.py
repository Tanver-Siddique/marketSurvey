# survey.py
import flet as ft
from data import general_info


class QuestionManager:
    def __init__(self, page, language="en", on_complete=None):
        self.page = page
        self.language = language
        self.questions = list(general_info[language].items())
        self.current_index = 0
        self.answers = {}
        self.on_complete = on_complete

        # Next and previous button controls
        self.next_button_controls = ft.ElevatedButton(
            text="Next",
            on_click=self.go_next,
            disabled=True,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )

        self.previous_button_controls = ft.ElevatedButton(
            text="Previous",
            on_click=self.go_previous,
            disabled=True,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )

        # Create the UI container
        self.container = ft.Column(
            spacing=10,
            expand=True,
            controls=[
                # The question controls will be added here dynamically
            ]
        )

        # Progress bar with responsive width
        self.progress_bar = ft.ProgressBar(
            value=0,
            expand=True,
            color=ft.Colors.BLUE,
            bgcolor=ft.Colors.GREY_300
        )

        # Main container with progress bar and questions
        self.main_container = ft.Column([
            self.progress_bar,
            self.container,
        ])

        # Render first question
        self.show_question()

    def update_language(self, new_language):
        """Update the language without resetting progress"""
        self.language = new_language
        self.questions = list(general_info[new_language].items())
        # Only show the question if not at the end
        if self.current_index < len(self.questions):
            self.show_question()
        else:
            self.show_end()

    def update_button_states(self):
        """Updates the disabled state of the next and previous buttons."""
        # Previous button logic
        self.previous_button_controls.disabled = self.current_index == 0

        # Next button logic
        qid, qdata = self.questions[self.current_index]
        q_type = qdata["type"]

        if q_type == "checkbox":
            # For checkbox, next is enabled if at least one is checked
            is_any_checked = any(cb.value for cb in self.checkboxes)
            self.next_button_controls.disabled = not is_any_checked
        else:
            # For radio, next is enabled if an option is selected
            has_answer = qid in self.answers and self.answers[qid] is not None
            self.next_button_controls.disabled = not has_answer

        self.page.update()

    def show_question(self):
        """Render the current question UI"""
        # Update progress bar
        self.progress_bar.value = self.current_index / len(self.questions)

        self.container.controls.clear()
        qid, qdata = self.questions[self.current_index]

        question_text = qdata["question"]
        options = qdata["options"]
        q_type = qdata["type"]

        # Add question text
        self.container.controls.append(
            ft.Markdown(
                value=question_text,
                md_style_sheet=ft.MarkdownStyleSheet(
                    p_text_style=ft.TextStyle(
                        color=ft.Colors.BLACK, size=18, weight=ft.FontWeight.BOLD
                    )
                )
            )
        )

        # Render based on question type
        if q_type == "checkbox":
            current_values = self.answers.get(qid, [])
            self.checkboxes = []
            for opt_id, opt_text in options.items():
                checkbox = ft.Checkbox(
                    label=opt_text,
                    label_style=ft.TextStyle(color=ft.Colors.BLACK),
                    value=opt_id in current_values,
                    data=opt_id,
                    on_change=lambda e: self.update_button_states()  # Update state on change
                )
                self.checkboxes.append(checkbox)
            self.container.controls.append(ft.Column(controls=self.checkboxes))

        else:  # Assumes "radio" type
            current_value = self.answers.get(qid, None)
            radio_group = ft.RadioGroup(
                value=current_value,
                content=ft.Column(
                    controls=[ft.Radio(value=opt_id, label=opt_text, label_style=ft.TextStyle(color=ft.Colors.BLACK))
                              for opt_id, opt_text in options.items()]
                ),
                on_change=lambda e: self.record_answer_and_next(e)  # Auto advance on change
            )
            self.container.controls.append(radio_group)

        # Add the button row at the end
        self.container.controls.append(ft.Divider(color=ft.Colors.TRANSPARENT))
        self.container.controls.append(
            ft.Row(
                controls=[
                    self.previous_button_controls,
                    self.next_button_controls
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

        self.update_button_states()
        self.page.update()

    def record_answer_and_next(self, e):
        """Save radio answer and move forward"""
        qid, qdata = self.questions[self.current_index]
        self.answers[qid] = e.control.value

        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.show_question()
        else:
            self.progress_bar.value = 1.0
            self.show_end()

    def go_next(self, e):
        """Handle next button click for checkbox questions"""
        qid, qdata = self.questions[self.current_index]

        if qdata["type"] == "checkbox":
            value = [cb.data for cb in self.checkboxes if cb.value]
            self.answers[qid] = value

        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.show_question()
        else:
            self.progress_bar.value = 1.0
            self.show_end()

    def go_previous(self, e):
        """Go back to previous question"""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()

    def show_end(self):
        """End of survey message"""
        self.container.controls.clear()

        self.end_message_control = ft.Text(
            "Thank you for completing the survey!" if self.language == "en" else "জরিপটি সম্পূর্ণ করার জন্য আপনাকে ধন্যবাদ!",
            size=22,
            color=ft.Colors.GREEN
        )
        self.container.controls.append(self.end_message_control)

        self.container.controls.append(
            ft.Text("Final Answers:", size=16, color=ft.Colors.BLACK)
        )
        for qid, ans in self.answers.items():
            self.container.controls.append(
                ft.Text(f"{qid}: {ans}", size=14, color=ft.Colors.GREY_700)
            )

        self.page.update()

        if self.on_complete:
            self.on_complete()


def general_info_questions(page, language, on_complete=None):
    manager = QuestionManager(page, language, on_complete)
    return manager
