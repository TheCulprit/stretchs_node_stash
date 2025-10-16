from invokeai.invocation_api import (
	BaseInvocation,
    BaseInvocationOutput,
    invocation,
    invocation_output,
    InputField,
    OutputField,
    InvocationContext
)
from typing import Literal
from enum import Enum

class Colours(str, Enum):
    """Colour codes"""
    BlackOnWhite = "Black on White"
    WhiteOnBlack = "White on Black"
    BlackOnGreen = "Black on Green"
    RedOnWhite = "Red on White"
    GreenOnRed = "Green on Red"
    YellowOnBlue = "Yellow on Blue"
    BlueOnYellow = "Blue on Yellow"
    MagentaOnCyan = "Magenta on Cyan"
    CyanOnMagenta = "Cyan on Magenta"
    BlackOnRed = "Black on Red"
    RedOnBlack = "Red on Black"
    YellowOnBlack = "Yellow on Black",
    BlackOnYellow = "Black on Yellow"
    
colours_dict = {
    Colours.BlackOnWhite: "\033[30;47m#REPLACE#\033[0m",
    Colours.WhiteOnBlack: "\033[37;40m#REPLACE#\033[0m",
    Colours.BlackOnGreen: "\033[30;42m#REPLACE#\033[0m",
    Colours.RedOnWhite: "\033[31;47m#REPLACE#\033[0m",
    Colours.GreenOnRed: "\033[32;41m#REPLACE#\033[0m",
    Colours.YellowOnBlue: "\033[33;44m#REPLACE#\033[0m",
    Colours.BlueOnYellow: "\033[34;43m#REPLACE#\033[0m",
    Colours.MagentaOnCyan: "\033[35;46m#REPLACE#\033[0m",
    Colours.CyanOnMagenta: "\033[36;45m#REPLACE#\033[0m",
    Colours.BlackOnRed: "\033[90;101m#REPLACE#\033[0m",
    Colours.RedOnBlack: "\033[91;100m#REPLACE#\033[0m",
    Colours.YellowOnBlack: "\x1b[33;40m#REPLACE#\x1b[0m",
    Colours.BlackOnYellow: "\x1b[30;43m#REPLACE#\x1b[0m"
}

COLOURS = Literal[
    Colours.BlackOnWhite,
    Colours.WhiteOnBlack,
    Colours.BlackOnGreen,
    Colours.RedOnWhite,
    Colours.GreenOnRed,
    Colours.YellowOnBlue,
    Colours.BlueOnYellow,
    Colours.MagentaOnCyan,
    Colours.CyanOnMagenta,
    Colours.BlackOnRed,
    Colours.RedOnBlack,
    Colours.YellowOnBlack,
    Colours.BlackOnYellow
]


@invocation_output("print_string_to_console_output")
class PrintStringToConsoleOutput(BaseInvocationOutput):
    """Debug Print String Output"""

    passthrough: str = OutputField(description="Passthrough", title="Passthrough")


@invocation("print_string_to_console_invocation", title="Print String to Console", tags=["debug", "string"], category="debug", version="1.0.1")
class PrintStringToConsoleInvocation(BaseInvocation):
    """Prints a string to the console."""

    print_colour: COLOURS = InputField(title="Print Colour", description="The colour to print the console output", default=Colours.WhiteOnBlack)
    input_str: str = InputField(title="Input string", description="The string to print to console.", default=", ")

    def invoke(self, context: InvocationContext) -> PrintStringToConsoleOutput:
        print(colours_dict[self.print_colour].replace("#REPLACE#", self.input_str))
        return PrintStringToConsoleOutput(passthrough=self.input_str)