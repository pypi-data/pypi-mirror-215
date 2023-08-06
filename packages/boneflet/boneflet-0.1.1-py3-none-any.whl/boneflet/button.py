#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/18 18:13
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from typing import TYPE_CHECKING
import flet
from flet import colors, icons, theme
from flet import RoundedRectangleBorder, UserControl, Border, BorderSide, BorderRadius
from flet import ButtonStyle

if TYPE_CHECKING:
    from typing import Union, Callable

    from flet import OptionalNumber
    from flet import Control
    from flet_core import types

    OptionalStr = Union[None, str]

button_style = flet.ButtonStyle(
    shape=RoundedRectangleBorder(radius=5)
)


class BoneButton(UserControl):
    def __init__(
            self,
            text: str | None = None,
            icon: str | None = None,

            scale: OptionalNumber = None,
            size: OptionalNumber = None,
            height: OptionalNumber = None,
            width: OptionalNumber = None,
            padding: types.PaddingValue = 0,
            on_click: Callable = lambda _: None
    ):
        super().__init__()
        self.icon = icon
        self.text = text
        self.size = size

        if self.text is None:
            self.control = flet.IconButton(content=flet.Icon(self.icon, size=size), scale=scale)
        elif self.icon is None:
            self.control = flet.TextButton(content=flet.Text(self.text, size=size), scale=scale)
        else:
            raise ValueError("You should use ElevatedButton")
        self.control.height = height
        self.control.width = width

        self.on_click = on_click
        self.style = flet.ButtonStyle(
            bgcolor={
                flet.MaterialState.DEFAULT: colors.TRANSPARENT,
                flet.MaterialState.HOVERED: colors.BLACK12,
            },
            overlay_color=colors.TRANSPARENT,
            color=colors.BLACK38,
            padding=padding,
            shape=RoundedRectangleBorder(radius=5),
        )

    def build(self):
        return self.control

    @property
    def style(self) -> ButtonStyle:
        return self.control.style

    @style.setter
    def style(self, value: ButtonStyle):
        self.control.style = value

    @property
    def on_click(self):
        return self.control.on_click

    @on_click.setter
    def on_click(self, handler):
        self.control.on_click = handler
