import random
from typing import Literal, Union

from fastapi import HTTPException

from invokeai.app.services.model_records import UnknownModelException
from invokeai.invocation_api import (
    AnyModelConfig,
    BaseInvocation,
    BaseInvocationOutput,
    BaseModelType,
    FieldDescriptions,
    Input,
    InputField,
    InvocationContext,
    LoadedModel,
    LoRAField,
    ModelFormat,
    ModelIdentifierField,
    OutputField,
    invocation,
    invocation_output,
)

MODEL_TYPE_LABELS = Literal[
    BaseModelType.StableDiffusion1,
    BaseModelType.StableDiffusion2,
    BaseModelType.StableDiffusionXL,
    BaseModelType.StableDiffusionXLRefiner,
]

RLM_START_MESSAGE = "\033[1;38;5;16;43m  #REPLACE#  \033[0m"
RLM_LORA_MESSAGE = "\033[33m#REPLACE#\033[0m"


class MinimumLoRANotSuppliedException(Exception):
    """Raised when there were not enough LoRAs supplied in the input Collection to honour the requirements of RandomLoRAMixer node."""

    def __init__(self, supplied: int, needed: int):
        super().__init__(
            f"RandomLoRAMixer node was not provided enough LoRAs [{supplied}] in the input Collection to honour the mininum LoRAs value [{needed}]"
        )


@invocation_output("lora_collection_from_path_output")
class LoRACollectionFromPathOutput(BaseInvocationOutput):
    """Filtered LoRA Colleciton Output"""

    loras: list[LoRAField] = OutputField(description="A collection of LoRAs.", title="LoRAs")


@invocation(
    "lora_collection_from_path_invocation",
    title="LoRA Collection From Path",
    tags=["model", "lora", "collection"],
    category="model",
    version="1.0.1",
)
class LoRACollectionFromPathInvocation(BaseInvocation):
    """Loads a collection of LoRAs filtered based on their path on disk."""

    model_type: MODEL_TYPE_LABELS = InputField(
        title="LoRA Type",
        default=BaseModelType.StableDiffusionXL,
        description="The type of LoRAs that will be retrieved.",
        input=Input.Direct,
    )
    path_filter: str = InputField(
        title="Path Filter", description="The path for the lora must contain the filter string"
    )
    default_weight: float = InputField(
        title="Default Weight",
        description="The weight to apply to each lora. This can be changed after using a Reapply LoRA Weight node.",
        default=0.75,
    )

    def invoke(self, context: InvocationContext) -> LoRACollectionFromPathOutput:
        try:
            # Get a list of all the installed models
            model_config_list: list[AnyModelConfig] = context.models.search_by_attrs(
                format=ModelFormat.LyCORIS, base=self.model_type
            )

            # Handle windows paths
            escaped_path_filter = self.path_filter.replace("\\", "/")

            # Filter the list down to only those which have a partial path match to our path_filter input
            filtered_list = [item for item in model_config_list if escaped_path_filter in item.source]
            new_list = []
            for item in filtered_list:
                model_identifier = ModelIdentifierField(
                    key=item.key, hash=item.hash, name=item.name, base=item.base, type=item.type
                )
                new_list.append(LoRAField(lora=model_identifier, weight=0.75))
            return LoRACollectionFromPathOutput(loras=new_list)
        except UnknownModelException as e:
            raise HTTPException(status_code=404, detail=str(e))


@invocation_output("merge_lora_collections_output")
class MergeLoRACollectionsOutput(BaseInvocationOutput):
    """Join LoRA Collections output"""

    collection: list[LoRAField] = OutputField(description="The merged collection", title="Collection")


@invocation(
    "merge_lora_collections_invocation",
    title="Merge LoRA Collections",
    tags=["collection", "lora"],
    category="collection",
    version="1.0.0",
)
class MergeLoRACollectionsInvocation(BaseInvocation):
    """Merges two Collections of LoRAs into a single Collection."""

    collection1: Union[LoRAField, list[LoRAField]] = InputField(
        title="Collection 1", description="A collection of LoRAs or a single LoRA from a LoRA Selector node."
    )
    collection2: Union[LoRAField, list[LoRAField]] = InputField(
        title="Collection 2", description="A collection of LoRAs or a single LoRA from a LoRA Selector node."
    )

    def invoke(self, context: InvocationContext) -> MergeLoRACollectionsOutput:
        new_collection: list[LoRAField] = []
        new_collection.extend(
            self.collection1 if self.collection1 == list[LoRAField] else list[LoRAField](self.collection1)
        )
        new_collection.extend(
            self.collection2 if self.collection2 == list[LoRAField] else list[LoRAField](self.collection2)
        )
        return MergeLoRACollectionsOutput(collection=new_collection)


@invocation_output("lookup_lora_triggers_output")
class LookupLoRATriggersOutput(BaseInvocationOutput):
    """Lookup LoRA Triggers Output"""

    trigger_words: list[str] = OutputField(description="A collection of the LoRAs trigger words", title="Trigger Words")


@invocation(
    "lookup_lora_triggers_invocation",
    title="Lookup LoRA Triggers",
    tags=["model, lora"],
    category="model",
    version="1.0.0",
)
class LookupLoRATriggersInvocation(BaseInvocation):
    """Retrieves a LoRA's trigger words from the Model Manager"""

    lora: LoRAField = InputField(title="LoRA", description="The LoRA to look up")

    def invoke(self, context: InvocationContext) -> LookupLoRATriggersOutput:
        try:
            # Get the input LoRA's data from the Model Manager
            loaded_model: LoadedModel = context.models.load(identifier=self.lora.lora.key)

            # Extract trigger words in to a new list
            trigger_list = list(loaded_model.config.trigger_phrases) if loaded_model.config.trigger_phrases else [""]

            return LookupLoRATriggersOutput(trigger_words=trigger_list)
        except UnknownModelException as e:
            raise HTTPException(status_code=404, detail=str(e))


@invocation_output("lookup_lora_collection_triggers_output")
class LookupLoRACollectionTriggersOutput(BaseInvocationOutput):
    """Lookup LoRA Collection Triggers Output"""

    trigger_words: list[str] = OutputField(
        description="A collection of all the LoRAs trigger words", title="Trigger Words"
    )


@invocation(
    "lookup_lora_collection_triggers_invocation",
    title="Lookup LoRA Collection Triggers",
    tags=["model, lora, collection"],
    category="model",
    version="1.0.0",
)
class LookupLoRACollectionTriggersInvocation(BaseInvocation):
    """Retrieves trigger words from the Model Manager for all LoRAs in the collection"""

    lora_collection: list[LoRAField] = InputField(title="LoRA Collection", description="The LoRAs to look up")

    def invoke(self, context: InvocationContext) -> LookupLoRATriggersOutput:
        try:
            trigger_list: list[str] = []

            for lora in self.lora_collection:
                # Get the input LoRA's data from the Model Manager
                loaded_model: LoadedModel = context.models.load(identifier=lora.lora.key)

                # Extract trigger words in to a new list
                lora_trigger_list = (
                    list(loaded_model.config.trigger_phrases) if loaded_model.config.trigger_phrases else [""]
                )

                # Merge
                if isinstance(lora_trigger_list, list):
                    trigger_list.extend(lora_trigger_list)

            print("=============================================")
            print(trigger_list)
            print("=============================================")
            return LookupLoRACollectionTriggersOutput(trigger_words=trigger_list)
        except UnknownModelException as e:
            raise HTTPException(status_code=404, detail=str(e))


@invocation_output("random_lora_mixer_output")
class RandomLoRAMixerOutput(BaseInvocationOutput):
    """Random LoRA Mixer Output"""

    loras: list[LoRAField] = OutputField(
        title="LoRAs", description="A random selection of the input LoRAs with random weights"
    )
    trigger_words: str = OutputField(
        title="Trigger Words", description="A string with delimited trigger words for the random LoRAs"
    )
    lora_names: str = OutputField(
        title="Lora Names", description="A string with the names and weights of all applied LoRAs"
    )


@invocation(
    "random_lora_mixer_invocation",
    title="Random LoRA Mixer",
    tags=["model", "lora", "random"],
    category="model",
    version="1.0.2",
    use_cache=False,
)
class RandomLoRAMixerInvocation(BaseInvocation):
    """Returns a random Collection of LoRAs selected from an input Collection."""

    loras: list[LoRAField] = InputField(
        title="LoRAs", description="A random selection of the input LoRAs with random weights"
    )
    seed: int = InputField(
        title="Seed",
        description="A seed to use for the random number generator. This allows reproducability. Leave as -1 for non-deterministic",
        default=-1,
    )
    min_loras: int = InputField(title="Min LoRAs", description="The mininum number of LoRAs to output", default=1)
    max_loras: int = InputField(title="Max LoRAs", description="The maximum number of LoRAs to output", default=3)
    min_weight: float = InputField(
        title="Min Weight", description="The mininum weight to apply to a LoRA", default=0.05
    )
    max_weight: float = InputField(title="Max Weight", description="The maxinum weight to apply to a LoRA", default=1.0)
    trigger_word_delimiter: str = InputField(
        title="Trigger Word Delimiter",
        description="A character sequence to place between each trigger word",
        default=", ",
    )
    lora_names_delimiter: str = InputField(
        title="LoRA Names Delimiter", description="A character sequence to place between each LoRA name", default=", "
    )

    def invoke(self, context: InvocationContext) -> RandomLoRAMixerOutput:
        # Check that there are enough loras supplied in the loras list to honour the min_loras value.
        if len(self.loras) < self.min_loras:
            raise MinimumLoRANotSuppliedException(supplied=len(self.loras), needed=self.min_loras)

        # Seed the random number generator
        if self.seed != -1:
            random.seed(self.seed)

        # Randomly select loras and apply a random weight
        lora_count: int = random.randint(self.min_loras, self.max_loras)
        lora_list: list[LoRAField] = []
        name_list: list[str] = []
        for i in range(lora_count):
            ran_lora: LoRAField = random.choice(self.loras)
            ran_lora.weight = round(random.uniform(self.min_weight, self.max_weight), 2)
            lora_list.append(ran_lora)
            name_list.append(ran_lora.lora.name + ":" + str(ran_lora.weight))

        # Print
        print(RLM_START_MESSAGE.replace("#REPLACE#", "LoRAs selected by Random LoRA Mixer:"))
        for name in name_list:
            print("    " + RLM_LORA_MESSAGE.replace("#REPLACE#", name))

        # Retreive the selected LoRA's trigger words and the names
        trigger_list: list[str] = []
        for i in range(len(lora_list)):
            try:
                # Get the model information from model manager
                loaded_model: LoadedModel = context.models.load(identifier=lora_list[i].lora.key)
                # Extract trigger words to a new list
                if loaded_model.config.trigger_phrases != None and len(loaded_model.config.trigger_phrases) != 0:
                    trigger_list.extend(list(loaded_model.config.trigger_phrases))
            except UnknownModelException as e:
                raise HTTPException(status_code=404, detail=str(e))

        return RandomLoRAMixerOutput(
            loras=lora_list,
            trigger_words=self.trigger_word_delimiter.join(trigger_list),
            lora_names=self.trigger_word_delimiter.join(name_list),
        )


@invocation_output("reapply_lora_weight_output")
class ReapplyLoRAWeightOutput(BaseInvocationOutput):
    """Reapply LoRA Weight Output"""

    lora: LoRAField = OutputField(description="LoRA model from a LoRA Selector node", title="LoRA")


@invocation(
    "reapply_lora_weight_invocation",
    title="Reapply LoRA Weight",
    tags=["model, lora"],
    category="model",
    version="1.0.0",
)
class ReapplyLoRAWeightInvocation(BaseInvocation):
    """Allows specifying an alternate weight for a LoRA after it has been selected with a LoRA selector node"""

    lora: LoRAField = InputField(
        title="LoRA",
    )
    weight: float = InputField(default=0.75, description=FieldDescriptions.lora_weight)

    def invoke(self, context: InvocationContext) -> ReapplyLoRAWeightOutput:
        return ReapplyLoRAWeightOutput(lora=LoRAField(lora=self.lora.lora, weight=self.weight))
