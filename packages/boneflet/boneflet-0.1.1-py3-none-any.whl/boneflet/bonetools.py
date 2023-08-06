from __future__ import annotations
from typing import TYPE_CHECKING
import flet
from flet import colors, icons, theme
from flet import RoundedRectangleBorder, UserControl, Border, BorderSide, BorderRadius
from flet import ButtonStyle
from boneflet.button import BoneButton
from boneflet.tab import BoneTabs, BoneTab

if TYPE_CHECKING:
    from typing import Union, Callable

    from flet import OptionalNumber
    from flet import Control

    OptionalStr = Union[None, str]


class HeaderBar(UserControl):
    def build(self):
        tabs = flet.Container(
            BoneTabs([
                BoneTab(text="icons.SETTINGS_OUTLINED"),
                BoneTab(text="Tab 2"),
                BoneTab(text="Tab 3"),
            ], height=34),
            margin=flet.Margin(0, 6, 0, 0),
        )
        items = flet.Row([
            flet.WindowDragArea(flet.Container(width=100, height=40)),
            # flet.Draggable(content = btn),
            tabs,
            BoneButton(flet.icons.WB_SUNNY_OUTLINED),
            BoneButton(flet.icons.FILTER_3)
        ], height=40, alignment=flet.MainAxisAlignment.START)
        return flet.Container(items, bgcolor=colors.BLACK12, padding=0, margin=0)


class SideBar(UserControl):
    def build(self):
        items = flet.Column([
            BoneButton(icon=icons.SETTINGS_OUTLINED, size=24),
            BoneButton(icon=icons.SETTINGS_OUTLINED, size=24),
            BoneButton(icon=icons.SETTINGS_OUTLINED, size=24),
            # flet.TextField(icon=icons.SETTINGS_OUTLINED, size=24),
        ])
        return flet.Container(items, padding=4, margin=0,
                              border=Border(None, BorderSide(2, colors.PRIMARY), None, None))


class Body(UserControl):

    def build(self):
        return flet.Stack(self.controls)


def main(page: flet.Page):
    page.title = "BoneFlet"
    page.window_title_bar_hidden = True
    page.spacing = 0
    page.theme_mode = "light"
    # page.event_handlers()
    # page.bgcolor = "red"
    # page.show_semantics_debugger=True
    page.padding = 0
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.theme = theme.Theme(color_scheme_seed=colors.BLACK)

    app_bar = HeaderBar()
    side_bar = SideBar()
    body = Body([
        flet.Container(content=flet.TextButton(text="faf"), bgcolor="blue", expand=True),
        flet.TextButton(text="fa2f"),
        flet.TextButton(text="f43a2f"),
        flet.Container(bgcolor="blue"),
    ])

    page.add(
        app_bar,
        flet.Row([
            side_bar,
            body,
        ], expand=True),
    )


flet.app(
    target=main
)
