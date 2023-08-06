#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/28 23:56
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
import flet

if TYPE_CHECKING:
    from typing import Union, Callable, Type

    from flet import OptionalNumber
    from flet import Control

register_db = {}


class Registrable:
    id: str


def register(cls: Registrable):
    d = register_db
    keys = cls.id.split(".")
    for k in keys[:-1]:
        d[k] = {}
        d = d[k]
    d[keys[-1]] = cls
    return cls


@dataclass
class Requirements:
    screens: list[str] = None
    actions: list[str] = None
    events: list[str] = None


@dataclass
class Supplies:
    screens: dict[str, Type[Screen]] = None
    actions: dict[str, Type[Action]] = None
    events: dict[str, Type[Event]] = None


@register
class Action(Registrable):
    id = "action.base"

    def __call__(self):
        raise NotImplementedError


@register
class Event(Registrable):
    id = "event.base"

    def __init__(self, actions):
        self.actions = actions

    def __call__(self):
        for action in self.actions:
            action()


@dataclass
class ScreenState:
    visible: bool = True


@register
class Screen(Registrable):
    id = "screen.base"

    def __init__(self, state: ScreenState=None):
        self.state = state

    def build(self):
        raise NotImplementedError


class Plugin:
    id = "base"

    def __init__(self, supplies: Supplies, requirements: Requirements):
        self.supplies = supplies
        self.requirements = requirements
        self.instructions = []

    def get_screens(self) -> dict[str, Type[Screen]]:
        return self.supplies.screens

    def get_main_screen(self) -> Type[Screen]:
        return self.get_screens()["screen.main"]

    def add_instruction(self, event, actions):
        register_db["event"][event](actions)


@register
class CopyAction(Action):
    id = "action.copy"

    def __call__(self, *args, **kwargs):
        import pyperclip
        pyperclip.waitForNewPaste()
        pyperclip.copy("Hello World!")
        print(f"copy {pyperclip.paste()} completed")


@register
class DemoScreen(Screen):
    id = "screen.main"

    def build(self):
        return flet.Text(self.id)


demo_plugin = Plugin(
    Supplies(
        screens={DemoScreen.id: DemoScreen},
        actions={CopyAction.id: CopyAction}
    ),
    Requirements()
)

if __name__ == '__main__':
    requirements = Requirements()
    supplies = Supplies(
        screens={DemoScreen.id: DemoScreen},
        actions={CopyAction.id: CopyAction}
    )
    p = Plugin(supplies, requirements)
    main_screen_cls = p.get_main_screen()
    main_screen_cls()
    # p.instructions.append({
    #     "id": "command-screenshot",
    #     "event": "base",
    #     "action": ["screenshot"]
    # })
    # import pyautogui
    #
    # pyautogui.screenshot()
    # requirements = {
    #     "events": [],
    #     "actions": [],
    # }
    # supplies = {
    #     "events": ["screenshot-end"],
    #     "actions": ["screenshot"],
    # }
    # p = Plugin(requirements, supplies)
    # p.instructions.append({
    #     "id": "command-screenshot",
    #     "event": "base",
    #     "action": ["screenshot"]
    # })
