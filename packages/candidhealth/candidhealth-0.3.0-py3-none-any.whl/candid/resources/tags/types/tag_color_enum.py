# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class TagColorEnum(str, enum.Enum):
    BLACK = "black"
    WHITE = "white"
    GRAY = "gray"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    INDIGO = "indigo"
    PURPLE = "purple"
    PINK = "pink"

    def visit(
        self,
        black: typing.Callable[[], T_Result],
        white: typing.Callable[[], T_Result],
        gray: typing.Callable[[], T_Result],
        red: typing.Callable[[], T_Result],
        yellow: typing.Callable[[], T_Result],
        green: typing.Callable[[], T_Result],
        blue: typing.Callable[[], T_Result],
        indigo: typing.Callable[[], T_Result],
        purple: typing.Callable[[], T_Result],
        pink: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is TagColorEnum.BLACK:
            return black()
        if self is TagColorEnum.WHITE:
            return white()
        if self is TagColorEnum.GRAY:
            return gray()
        if self is TagColorEnum.RED:
            return red()
        if self is TagColorEnum.YELLOW:
            return yellow()
        if self is TagColorEnum.GREEN:
            return green()
        if self is TagColorEnum.BLUE:
            return blue()
        if self is TagColorEnum.INDIGO:
            return indigo()
        if self is TagColorEnum.PURPLE:
            return purple()
        if self is TagColorEnum.PINK:
            return pink()
