from typing import Literal

from invokeai.invocation_api import BaseInvocation, BooleanOutput, InputField, InvocationContext, invocation

NUMBER_COMPARISION_METHODS = Literal["<", "<=", ">", ">=", "==", "!="]


@invocation(
    "compare_ints_invocation", title="Compare Ints", tags=["int", "compare"], category="compare", version="1.0.0"
)
class CompareIntsInvocation(BaseInvocation):
    """Compares two integers based on input criteria and ouputs a boolean."""

    comparison_method: NUMBER_COMPARISION_METHODS = InputField(
        title="Comparison Method", description="The comparision method to use"
    )
    int1: int = InputField(title="Int 1", description="The first integer.")
    int2: int = InputField(title="Int 2", description="The second integer.")

    def invoke(self, context: InvocationContext) -> BooleanOutput:
        result: bool = False
        if self.comparison_method == "<":
            result = self.int1 < self.int2
        elif self.comparison_method == "<=":
            result = self.int1 <= self.int2
        elif self.comparison_method == ">":
            result = self.int1 > self.int2
        elif self.comparison_method == ">=":
            result = self.int1 >= self.int2
        elif self.comparison_method == "==":
            result = self.int1 == self.int2
        elif self.comparison_method == "!=":
            result = self.int1 != self.int2
        return BooleanOutput(value=result)


@invocation(
    "compare_floats_invocation", title="Compare Floats", tags=["floats", "compare"], category="compare", version="1.0.0"
)
class CompareFloatsInvocation(BaseInvocation):
    """Compares two floats based on input criteria and ouputs a boolean."""

    comparison_method: NUMBER_COMPARISION_METHODS = InputField(
        title="Comparison Method", description="The comparision method to use"
    )
    float1: float = InputField(title="Float 1", description="The first float")
    float2: float = InputField(title="Float 2", description="The second float")

    def invoke(self, context: InvocationContext) -> BooleanOutput:
        result: bool = False
        if self.comparison_method == "<":
            result = self.float1 < self.float2
        elif self.comparison_method == "<=":
            result = self.float1 <= self.float2
        elif self.comparison_method == ">":
            result = self.float1 > self.float2
        elif self.comparison_method == ">=":
            result = self.float1 >= self.float2
        elif self.comparison_method == "==":
            result = self.float1 == self.float2
        elif self.comparison_method == "!=":
            result = self.float1 != self.float2
        return BooleanOutput(value=result)


STRING_COMPARISON_METHODS = Literal["equals", "contains", "starts with", "ends with"]


@invocation(
    "compare_strings_invocation",
    title="Compare Strings",
    tags=["string", "str", "compare"],
    category="compare",
    version="1.0.0",
)
class CompareStringsInvocation(BaseInvocation):
    """Compares two strings based on input criteria and ouputs a boolean."""

    comparison_method: STRING_COMPARISON_METHODS = InputField(
        title="Comparison Method", description="The comparision method to use"
    )
    ignore_case: bool = InputField(
        title="Ignore Case",
        description="If true the node will ignore the case of the strings in all comparison methods",
    )
    str1: str = InputField(title="String 1", description="The first float")
    str2: str = InputField(title="String 2", description="The second float")

    def invoke(self, context: InvocationContext) -> BooleanOutput:
        result: bool = False
        if self.comparison_method == "equals":
            if self.ignore_case:
                result = self.str1.casefold() == self.str2.casefold()
            else:
                result = self.str1 == self.str2
        elif self.comparison_method == "contains":
            if self.ignore_case:
                result = self.str2.lower() in self.str1.lower()
            else:
                result = self.str2 in self.str1
        elif self.comparison_method == "starts with":
            if self.ignore_case:
                result = self.str1.lower().startswith(self.str2.lower())
            else:
                result = self.str1.startswith(self.str2)
        elif self.comparison_method == "ends with":
            if self.ignore_case:
                result = self.str1.lower().endswith(self.str2.lower())
            else:
                result = self.str1.endswith(self.str2)
        return BooleanOutput(value=result)
