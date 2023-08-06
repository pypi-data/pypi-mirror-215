"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from pcconfig import config

import reflex as rf

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rf.State):
    """The app state."""

    pass


def index() -> rf.Component:
    return rf.fragment(
        rf.color_mode_button(rf.color_mode_icon(), float="right"),
        rf.vstack(
            rf.heading("Welcome to Reflex!", font_size="2em"),
            rf.box("Get started by editing ", rf.code(filename, font_size="1em")),
            rf.link(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": rf.color_mode_cond(
                        light="rgb(107,99,246)",
                        dark="rgb(179, 175, 255)",
                    )
                },
            ),
            spacing="1.5em",
            font_size="2em",
            padding_top="10%",
        ),
    )


# Add state and page to the app.
app = rf.App(state=State)
app.add_page(index)
app.compile()
