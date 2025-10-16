from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    invocation,
    invocation_output,
    ModelIdentifierField,
    InputField,
    OutputField,
    InvocationContext,
    LoRAField
)

@invocation_output("lora_name_grabber_output")
class LoRANameGrabberOutput(BaseInvocationOutput):
    """LoRA Name Grabber output"""

    name: str = OutputField(description="Name of the LoRA", title="Name")


@invocation("lora_name_grabber_invocation", title="LoRA Name Grabber", tags=["model, lora, string"], category="model", version="1.0.0")
class LoRANameGrabberInvocation(BaseInvocation):
    """Outputs the LoRA's name as a string. Use a Lora Selector node as input."""

    lora: LoRAField = InputField(title="LoRA", description="The LoRA whose name you wish to grab. Get this from a LoRA Selector node.")

    def invoke(self, context: InvocationContext) -> LoRANameGrabberOutput:
        return LoRANameGrabberOutput(name=self.lora.lora.name)




@invocation_output("model_name_grabber_output")
class ModelNameGrabberOutput(BaseInvocationOutput):
    """Model Name Grabber output"""

    name: str = OutputField(description="Name of the Model", title="Name")

@invocation("model_name_grabber_invocation", title="Model Name Grabber", tags=["model, string"], category="model", version="1.0.0")
class ModelNameGrabberInvocation(BaseInvocation):
    """Outputs the Model's name as a string. Use the Model Identifier node as input."""

    model: ModelIdentifierField = InputField(title="Model", description="Get this input from a Model Identifier node.")

    def invoke(self, context: InvocationContext) -> ModelNameGrabberOutput:
        return ModelNameGrabberOutput(name=self.model.name)