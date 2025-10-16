from invokeai.invocation_api import (
	SchedulerOutput,
	SCHEDULER_NAME_VALUES,
	BooleanOutput,
	BooleanCollectionOutput,
	ConditioningField,
	ConditioningOutput,
	ConditioningCollectionOutput,
	FluxConditioningField,
	FluxConditioningOutput,
	FluxConditioningCollectionOutput,
	IntegerOutput,
	IntegerCollectionOutput,
	FloatOutput,
	FloatCollectionOutput,
	StringOutput,
	StringCollectionOutput,
	ImageOutput,
	ImageCollectionOutput,
	InvocationContext,
	InputField,
	OutputField,
	ImageField,
	BaseInvocation,
	BaseInvocationOutput,
	invocation,
	invocation_output,
	ModelIdentifierField,
	UNetField,
	CLIPField,
	VAEField,
	FieldDescriptions,
	LoRAField
)
from invokeai.app.invocations.sdxl import (
	SDXLModelLoaderOutput
)

#region Bool
@invocation("bool_toggle", title="Bool Toggle", tags=["bool", "toggle"], category="toggle", version="1.0.0")
class BoolToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate boolean inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	bool1: bool = InputField(default=False, description="First Bool Input")
	bool2: bool = InputField(default=False, description="Second Bool Input")

	def invoke(self, context: InvocationContext) -> BooleanOutput:
		return BooleanOutput(value=(self.bool2 if self.use_second else self.bool1))

@invocation("bool_collection_toggle", title="Bool Collection Toggle", tags=["bool", "collection", "toggle"], category="toggle", version="1.0.0")
class BoolCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate boolean collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[bool] = InputField(description="First Bool Collection Input")
	col2: list[bool] = InputField(description="Second Bool Collection Input")

	def invoke(self, context: InvocationContext) -> BooleanCollectionOutput:
		return BooleanCollectionOutput(collection=(self.col2 if self.use_second else self.col1))
#endregion Bool

#region Int
@invocation("int_toggle", title="Integer Toggle", tags=["int", "integer", "toggle"], category="toggle", version="1.0.0")
class IntToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate integer inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	int1: int = InputField(default=0, description="First Integer Input")
	int2: int = InputField(default=0, description="Second Integer Input")

	def invoke(self, context: InvocationContext) -> IntegerOutput:
		return IntegerOutput(value=self.int2 if self.use_second else self.int1)

@invocation("int_collection_toggle", title="Integer Collection Toggle", tags=["int", "integer", "collection", "toggle"], category="toggle", version="1.0.0")
class IntCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate integer collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[int] = InputField(description="First Int Collection Input")
	col2: list[int] = InputField(description="Second Int Collection Input")

	def invoke(self, context: InvocationContext) -> IntegerCollectionOutput:
		return IntegerCollectionOutput(collection=(self.col2 if self.use_second else self.col1))
#endregion int

#region Float
@invocation("float_toggle", title="Float Toggle", tags=["float", "toggle"], category="toggle", version="1.0.0")
class FloatToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate float inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	float1: float = InputField(default=0, description="First Float Input")
	float2: float = InputField(default=0, description="Second Float Input")

	def invoke(self, context: InvocationContext) -> FloatOutput:
		return FloatOutput(value=(self.float2 if self.use_second else self.float1))

@invocation("float_collection_toggle", title="Float Collection Toggle", tags=["float", "collection", "toggle"], category="toggle", version="1.0.0")
class FloatCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate float collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[float] = InputField(description="First Float Collection Input")
	col2: list[float] = InputField(description="Second Float Collection Input")

	def invoke(self, context: InvocationContext) -> FloatCollectionOutput:
		return FloatCollectionOutput(collection=(self.col2 if self.use_second else self.col1))
#endregion Float

#region String
@invocation("string_toggle", title="String Toggle", tags=["str", "string", "toggle"], category="toggle", version="1.0.0")
class StringToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate string inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	str1: str = InputField(title="String 1", description="First String Input")
	str2: str = InputField(title="String 2", description="Second String Input")

	def invoke(self, context: InvocationContext) -> StringOutput:
		return StringOutput(value=self.str2 if self.use_second else self.str1)

@invocation("string_collection_toggle", title="String Collection Toggle", tags=["str", "string", "collection", "toggle"], category="toggle", version="1.0.0")
class StringCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate string collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[str] = InputField(description="First String Collection Input")
	col2: list[str] = InputField(description="Second String Collection Input")

	def invoke(self, context: InvocationContext) -> StringCollectionOutput:
		return StringCollectionOutput(collection=(self.col2 if self.use_second else self.col1))
#endregion String

#region Image
@invocation("image_toggle", title="Image Toggle", tags=["image", "toggle"], category="toggle", version="1.0.0")
class ImageToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate image inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	img1: ImageField = InputField(description="First Image Input")
	img2: ImageField = InputField(description="Second Image Input")

	def invoke(self, context: InvocationContext) -> ImageOutput:
		image_dto = context.images.get_dto(self.img2.image_name if self.use_second else self.img1.image_name)
		return ImageOutput.build(image_dto=image_dto)

@invocation("image_collection_toggle", title="Image Collection Toggle", tags=["image", "collection", "toggle"], category="toggle", version="1.0.0")
class ImageCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate Image collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[ImageField] = InputField(description="First Image Collection Input")
	col2: list[ImageField] = InputField(description="Second Image Collection Input")

	def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
		return ImageCollectionOutput(collection=self.col2 if self.use_second else self.col1)
#endregion Image

#region LoRA
@invocation_output("lora_toggle_output")
class LoRAToggleOutput(BaseInvocationOutput):
	lora: LoRAField = OutputField(description="LoRA model and weight", title="LoRA")

@invocation("lora_toggle", title="LoRA Toggle", tags=["lora", "toggle"], category="toggle", version="1.0.0")
class LoRAToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate LoRA inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	lora1: LoRAField = InputField(description="First LoRA Input")
	lora2: LoRAField = InputField(description="Second LoRA Input")

	def invoke(self, context: InvocationContext) -> LoRAToggleOutput:
		return LoRAToggleOutput(lora=self.lora2 if self.use_second else self.lora1)

@invocation_output("lora_collection_toggle_output")
class LoRACollectionToggleOutput(BaseInvocationOutput):
	collection: list[LoRAField] = OutputField(description="Collection of LoRA models and weights", title="LoRA Collection")

@invocation("lora_collection_toggle", title="LoRA Collection Toggle", tags=["lora", "collection", "toggle"], category="toggle", version="1.0.0")
class LoRACollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate LoRA collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[LoRAField] = InputField(description="First LoRA Collection Input")
	col2: list[LoRAField] = InputField(description="Second LoRA Collection Input")

	def invoke(self, context: InvocationContext) -> LoRACollectionToggleOutput:
		return LoRACollectionToggleOutput(collection=self.col2 if self.use_second else self.col1)
#endregion LoRA

#region Scheduler
@invocation("scheduler_toggle", title="Scheduler Toggle", tags=["scheduler", "toggle"], category="toggle", version="1.0.0")
class SchedulerToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate scheduler inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	scheduler1: SCHEDULER_NAME_VALUES = InputField(description="First Scheduler Input")
	scheduler2: SCHEDULER_NAME_VALUES = InputField(description="Second Scheduler Input")

	def invoke(self, context: InvocationContext) -> SchedulerOutput:
		return SchedulerOutput(scheduler=self.scheduler2 if self.use_second else self.scheduler1)
#endregion

#region Main Model
@invocation_output("model_toggle_output")
class ModelToggleOutput(BaseInvocationOutput):
    """Model Toggle output"""

    model: ModelIdentifierField = OutputField(description="Model identifier", title="Model")

@invocation("model_toggle", title="Model Toggle", tags=["model", "toggle"], category="toggle", version="1.0.0")
class ModelToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate ModelIdentifier inputs"""
	
	use_second: bool = InputField(description="Use 2nd Input")
	model1: ModelIdentifierField = InputField(description="First Model Input")
	model2: ModelIdentifierField = InputField(description="First Model Input")

	def invoke(self, context: InvocationContext) -> ModelToggleOutput:
		return ModelToggleOutput(model=self.model2 if self.use_second else self.model1)

@invocation("sdxl_main_model_toggle", title="SDXL Main Model Toggle", tags=["model", "sdxl", "toggle"], category="toggle", version="1.0.0")
class SDXLMainModelToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate SDXL Main Model inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	unet1: UNetField = InputField(description=FieldDescriptions.unet, title="UNet 1")
	clip1: CLIPField = InputField(description=FieldDescriptions.clip, title="CLIP 1 1")
	clip21: CLIPField = InputField(description=FieldDescriptions.clip, title="CLIP 2 1")
	vae1: VAEField = InputField(description=FieldDescriptions.vae, title="VAE 1")
	unet2: UNetField = InputField(description=FieldDescriptions.unet, title="UNet 2")
	clip2: CLIPField = InputField(description=FieldDescriptions.clip, title="CLIP 1 2")
	clip22: CLIPField = InputField(description=FieldDescriptions.clip, title="CLIP 2 2")
	vae2: VAEField = InputField(description=FieldDescriptions.vae, title="VAE 2")

	def invoke(self, context: InvocationContext) -> SDXLModelLoaderOutput:
		return SDXLModelLoaderOutput(
			unet=self.unet2 if self.use_second else self.unet1,
			clip=self.clip2 if self.use_second else self.clip1,
			clip2=self.clip22 if self.use_second else self.clip21,
			vae=self.vae2 if self.use_second else self.vae1
		)
#endregion Main Model

#region Conditioning
@invocation("conditioning_toggle", title="Conditioning Toggle", tags=["conditioning", "toggle"], category="toggle", version="1.0.0")
class ConditioningToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate conditioning inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	cond1: ConditioningField = InputField(description="First Conditioning Input")
	cond2: ConditioningField = InputField(description="Second Conditioning Input")

	def invoke(self, context: InvocationContext) -> ConditioningOutput:
		return ConditioningOutput(conditioning=self.cond2 if self.use_second else self.cond1)

@invocation("conditioning_collection_toggle", title="Conditioning Collection Toggle", tags=["conditioning", "collection", "toggle"], category="toggle", version="1.0.0")
class ConditioningCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate conditioning collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[ConditioningField] = InputField(description="First Conditioning Collection Input")
	col2: list[ConditioningField] = InputField(description="Second Conditioning Collection Input")

	def invoke(self, context: InvocationContext) -> ConditioningCollectionOutput:
		return ConditioningCollectionOutput(collection=self.col2 if self.use_second else self.col1)
#endregion Conditioning

#region FLUX Conditioning
@invocation("flux_conditioning_toggle", title="FLUX Conditioning Toggle", tags=["conditioning", "toggle", "flux"], category="toggle", version="1.0.0")
class FLUXConditioningToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate FLUX conditioning inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	cond1: FluxConditioningField = InputField(description="First FLUX Conditioning Input")
	cond2: FluxConditioningField = InputField(description="Second FLUX Conditioning Input")

	def invoke(self, context: InvocationContext) -> FluxConditioningOutput:
		return FluxConditioningOutput(conditioning=self.cond2 if self.use_second else self.cond1)

@invocation("flux_conditioning_collection_toggle", title="FLUX Conditioning Collection Toggle", tags=["conditioning", "collection", "toggle", "flux"], category="toggle", version="1.0.1")
class FLUXConditioningCollectionToggleInvocation(BaseInvocation):
	"""Allows boolean selection between two separate FLUX conditioning collection inputs"""

	use_second: bool = InputField(default=False, description="Use 2nd Input")
	col1: list[FluxConditioningField] = InputField(description="First FLUX Conditioning Collection Input")
	col2: list[FluxConditioningField] = InputField(description="Second FLUX Conditioning Collection Input")

	def invoke(self, context: InvocationContext) -> FluxConditioningCollectionOutput:
		return FluxConditioningCollectionOutput(collection=self.col2 if self.use_second else self.col1)
#endregion FLUX Conditioning
