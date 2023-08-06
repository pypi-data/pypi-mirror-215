#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/18 18:14
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations
from typing import TYPE_CHECKING
import flet
from flet import colors, icons, theme
from flet import RoundedRectangleBorder, UserControl, Border, BorderSide, BorderRadius
from flet import ButtonStyle
from boneflet.button import BoneButton

if TYPE_CHECKING:
    from typing import Union, Callable, Optional
    from flet import OptionalNumber
    from flet import Control

    OptionalStr = Union[None, str]


class BoneTab(flet.Container):
    def __init__(
            self,
            text: str | None = None,
            selected: bool = False,
            width: int = 100,
            on_click: Callable = lambda _: None
    ):
        self.title = flet.Text(text, width=width - 30, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
        self.close = BoneButton(icon=icons.CLOSE, height=20, width=20, size=16)
        super().__init__(flet.TextButton(content=flet.Row([
            self.title,
            self.close
        ], spacing=0), on_click=on_click, width=width))
        self.padding = flet.Padding(4, 0, 4, 4)
        self.border_radius = BorderRadius(5, 5, 0, 0)
        self.selected = selected

    @property
    def selected(self) -> bool:
        return self.__selected

    @selected.setter
    def selected(self, value: bool):
        if value:
            self.bgcolor = colors.BACKGROUND

            self.content.style = flet.ButtonStyle(
                bgcolor=colors.BACKGROUND,
                overlay_color=colors.TRANSPARENT,
                shadow_color=colors.TRANSPARENT,
                surface_tint_color=colors.TRANSPARENT,
                color=colors.BLACK38,
                padding=flet.Padding(5, 0, 0, 0),
                shape=RoundedRectangleBorder(radius=BorderRadius(5, 5, 0, 0))
            )
        else:
            self.bgcolor = colors.TRANSPARENT
            self.content.style = flet.ButtonStyle(
                bgcolor={
                    flet.MaterialState.DEFAULT: colors.TRANSPARENT,
                    flet.MaterialState.HOVERED: colors.BLACK12,
                },
                overlay_color=colors.TRANSPARENT,
                shadow_color=colors.TRANSPARENT,
                color=colors.BLACK38,
                padding=flet.Padding(5, 0, 0, 0),
                shape=RoundedRectangleBorder(radius=5)
            )
        self.__selected = value

    @property
    def on_click(self):
        return self.content.on_click

    @on_click.setter
    def on_click(self, handler):
        self.content.on_click = handler

    @property
    def on_close(self):
        return self.close.on_click

    @on_close.setter
    def on_close(self, handler):
        self.close.on_click = handler


class BoneTabs(UserControl):
    def __init__(
            self,
            tabs: list[BoneTab],
            height: int = 90,
            selected_index: int = 0,
            show_add_tab: bool = True,
            add_event: bool = True,
            on_change: Callable = lambda _: None
    ):
        super().__init__()
        self.__selected_index = selected_index
        self.on_change = on_change
        self.tabs = tabs
        if show_add_tab:
            self.add_tab = flet.Container(BoneButton(icon=icons.ADD, width=28, height=28, size=20),
                                          padding=flet.Padding(6, 0, 0, 6))
        else:
            self.add_tab = flet.Container()

        self.content = flet.Row([*self.tabs, self.add_tab], spacing=0, expand=True)
        self.index2tab: dict[int, BoneTab] = {}
        self.tab2index: dict[BoneTab, int] = {}

        def gen_tab_event(control: BoneTab, on_click: Optional[Callable] = None):

            def tab_on_click(e: flet.ControlEvent):
                self.selected_index = self.tab2index[control]
                if on_click:
                    on_click(e)
                self.on_change(e)

            def tab_on_close(e: flet.ControlEvent):
                index = self.tab2index[control]
                self.tabs.pop(index)
                for _i, _tab in enumerate(self.tabs[index:]):
                    _i += index
                    self.index2tab[_i] = _tab
                    self.tab2index[_tab] = _i
                self.selected_index = index
                self.on_change(e)

            return tab_on_click, tab_on_close

        def add_tab_on_click(e):
            index = len(self.tabs)
            new_tab = BoneTab(text="tab")
            new_tab.on_click, new_tab.on_close = gen_tab_event(new_tab)
            self.tabs.append(new_tab)
            self.index2tab[index] = new_tab
            self.tab2index[new_tab] = index
            self.content.controls = [*self.tabs, self.add_tab]
            self.selected_index = index
            self.on_change(e)

        for i, tab in enumerate(self.tabs):
            tab.height = height
            if add_event:
                tab.on_click, tab.on_close = gen_tab_event(tab, tab.on_click)
            self.index2tab[i] = tab
            self.tab2index[tab] = i
            if i == selected_index:
                tab.selected = True
            else:
                tab.selected = False

        self.add_tab.on_click = add_tab_on_click

    def __len__(self):
        return len(self.tabs)

    @property
    def selected_index(self):
        return self.__selected_index

    @selected_index.setter
    def selected_index(self, value: int):
        old = self.index2tab[self.__selected_index]
        new = self.index2tab[value]
        old.selected = False
        new.selected = True
        self.__selected_index = value

    @property
    def on_change(self):
        return self.__on_change

    @on_change.setter
    def on_change(self, handler):
        def _on_change(e):
            handler(e)
            self.update()

        self.__on_change = _on_change

    def update(self):
        self.content.controls = [*self.tabs, self.add_tab]
        super().update()

    async def update_async(self):
        self.content.controls = [*self.tabs, self.add_tab]
        await super().update_async()

    def build(self):
        return self.content
