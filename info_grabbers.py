from invokeai.invocation_api import (
	BaseInvocation,
	invocation,
    UNetField,
    InputField,
    InvocationContext,
    StringOutput,
    AnyModelConfig
)
from typing import Literal

INFO_TYPE = Literal[
    "name",
    "path"
]

@invocation("info_grabber_unet_invocation", title="UNet Info Grabber", tags=["unet", "info"], category="info", version="1.0.1")
class InfoGrabberUNetInvocation(BaseInvocation):
    """Outputs different info from a UNet"""

    unet: UNetField = InputField(title="UNet")
    info_type: INFO_TYPE = InputField(title="Info Type", description="The kind of info to retrieve")

    def invoke(self, context: InvocationContext) -> StringOutput:
        result: str = ""
        if self.info_type == "name":
            result = self.unet.unet.name
        elif self.info_type == "path":
            config: AnyModelConfig = context.models.get_config(self.unet.unet)
            result = config.source
        return StringOutput(value=result)