import random
from invokeai.invocation_api import (
     BaseInvocation,
     BaseInvocationOutput,
     InvocationContext,
     invocation,
     invocation_output,
     InputField,
     OutputField
)
import math
from typing import Tuple
from invokeai.app.invocations.constants import LATENT_SCALE_FACTOR

@invocation_output("random_image_size")
class RandomImageSizeOutput(BaseInvocationOutput):
    """Random Image Size Output"""

    width: int = OutputField(title="Width")
    height: int = OutputField(title="Height")

@invocation("random_image_size_invocation", title="Random Image Size", tags=["size", "image", "dimensions"], category="size", version="1.0.0")
class RandomImageSizeInvocation(BaseInvocation):
	"""Outputs a random size from a list of sizes."""

	seed: int = InputField(title="Seed", description="A seed for the randomness. Use -1 for non-deterministic.", default=-1)
	size_list: str = InputField(title="Size List", description="", default="1024x1024,888x1184,1184x888,840x1256,1256x840,768x1368,1368x768")
	multiples_of_32: bool = InputField(title="Multiples of 32", description="", default=False)

	def invoke(self, context: InvocationContext) -> RandomImageSizeOutput:
		if self.seed != -1:
			random.seed(self.seed)

		# Split the sizes
		stripped: str = self.size_list.replace(" ", "")
		split: list[str] = stripped.split(",")
		
		# select a random size
		ran_size: str = random.choice(split)
		
		# Split
		width_str, height_str = ran_size.split("x")
		width = int(width_str)
		height = int(height_str)

		# Multiples of 32
		if self.multiples_of_32:
			def round_to_32(n: int) -> int:
				return round(n / 32) * 32
			width = round_to_32(width)
			height = round_to_32(height)
		
		return RandomImageSizeOutput(width=width, height=height)