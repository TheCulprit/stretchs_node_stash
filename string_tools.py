from invokeai.invocation_api import (
	BaseInvocation,
	BaseInvocationOutput,
	invocation,
	invocation_output,
	InputField,
	InvocationContext,
	OutputField,
	StringCollectionOutput
)
import os
from typing import Union

@invocation_output("string_collection_joiner_output")
class StringCollectionJoinerOutput(BaseInvocationOutput):
	"""String Collection Joiner Output"""

	result: str = OutputField(description="The joined string", title="Result")


@invocation("string_collection_joiner_invocation", title="String Collection Joiner", tags=["string"], category="string", version="1.0.1")
class StringCollectionJoinerInvocation(BaseInvocation):
	"""Takes a collection of strings and returns a single string with all the collections items, separated by the input delimiter."""

	delimiter: str = InputField(title="Delimiter", description="The character to place between each string.", default=", ")
	collection: list[str] = InputField(title="Collection", description="The string collection to join.")
	escape_delimiter: bool = InputField(title="Escape Delimiter", description="Wehter we should escape the delimiter", default=False)
	
	def join_with_delimiter(self, items, delimiter) -> str:
		# Replace delimiter with escaped version in all items
		escaped_delimiter = '\\' + delimiter.replace('\\', '\\\\')
		escaped_items = [item.replace(delimiter, escaped_delimiter) for item in items]

		# Join items with the delimiter
		return delimiter.join(escaped_items)

	def invoke(self, context: InvocationContext) -> StringCollectionJoinerOutput:
		result = self.collection
		if self.escape_delimiter:
			result = self.join_with_delimiter(self.collection, self.delimiter)
		else:
			result = self.delimiter.join(result)
		return StringCollectionJoinerOutput(result=result)


@invocation_output("load_text_file_to_string_output")
class LoadTextFileToStringOutput(BaseInvocationOutput):
	"""Load Text File To String Output"""

	result: str = OutputField(title="Result")


@invocation("load_text_file_to_string_invocation", title="Load Text File to String", tags=["string"], category="string", version="1.0.0", use_cache=False)
class LoadTextFileToStringInvocation(BaseInvocation):
	"""Loads a text from a provided path and outputs it as a string"""

	file_path: str = InputField(title="Path", description="The full path to the text file.")

	def invoke(self, context: InvocationContext) -> LoadTextFileToStringOutput:
		with open(self.file_path, 'r', encoding="utf-8") as file:
			# Read the entire file content into a string
			file_content = file.read()
		return LoadTextFileToStringOutput(result=file_content)



@invocation_output("load_all_text_files_in_folder_output")
class LoadAllTextFilesInFolderOutput(BaseInvocationOutput):
	"""Load Text Files In Folder Output"""

	result: list[str] = OutputField(title="Results")


@invocation("load_all_text_files_in_folder_output", title="Load All Text Files In Folder", tags=["string"], category="string", version="1.0.1", use_cache=False)
class LoadAllTextFilesInFolderInvocation(BaseInvocation):
	"""Loads all text files in a folder and its subfolders recursively, returning them as a Collection of strings"""

	extension_to_match: str = InputField(title="File Extension", description="Only files with the given extension will be loaded. For example: json")
	folder_path: str = InputField(title="Folder Path", description="The path to load files from.")

	def invoke(self, context: InvocationContext) -> LoadAllTextFilesInFolderOutput:
		if not os.path.isdir(self.folder_path):
			raise OSError(f"The path '{self.folder_path}' is either not a directory or does not exist.")
		
		files_content = []
		
		# Walk through all subdirectories and files in the folder
		for root, dirs, files in os.walk(self.folder_path):
			for filename in files:
				if filename.endswith(self.extension_to_match):
					file_path = os.path.join(root, filename)
					with open(file_path, 'r', encoding="utf-8") as file:
						files_content.append(file.read())
	
		return LoadAllTextFilesInFolderOutput(result=files_content)


@invocation_output("merge_string_collections_output")
class MergeStringCollectionsOutput(BaseInvocationOutput):
	"""Merge String Collections output"""

	collection: list[str] = OutputField(description="The merged collection", title="Collection")


@invocation("merge_string_collections_invocation", title="Merge String Collections", tags=["collection", "string"], category="collection", version="1.0.0")
class MergeStringCollectionsInvocation(BaseInvocation):
	"""Merges two Collections of LoRAs into a single Collection."""

	collection1: Union[str, list[str]] = InputField(title="Collection 1", description="A collection of strings or a single string.")
	collection2: Union[str, list[str]] = InputField(title="Collection 2", description="A collection of strings or a single string.")

	def invoke(self, context: InvocationContext) -> MergeStringCollectionsOutput:
		new_collection: list[str] = []
		new_collection.extend(self.collection1 if self.collection1 == list[str] else list[str](self.collection1))
		new_collection.extend(self.collection2 if self.collection2 == list[str] else list[str](self.collection2))
		return MergeStringCollectionsOutput(collection=new_collection)


@invocation("string_to_collection_splitter_invocation", title="String to Collection Splitter", tags=["string"], category="string", version="1.0.0")
class StringToCollectionSplitterInvocation(BaseInvocation):
    """Takes a delimited string and splits it into a collection."""

    delimiter: str = InputField(title="Delimiter", description="The character dividing each string.", default=", ")
    string: str = InputField(title="String", description="The string to split.")
    unescape_delimiter: bool = InputField(title="Escape Delimiter", description="Whether we should unescape the delimiter", default=False)

    def split_with_delimiter(self, joined_string, delimiter) -> list[str]:
        # First split by unescaped delimiter
        parts = []
        current_part = ""
        i = 0

        while i < len(joined_string):
            # Check if we've hit the delimiter
            if joined_string[i:i+len(delimiter)] == delimiter:
                parts.append(current_part)
                current_part = ""
                i += len(delimiter)
            else:
                # Check for escaped delimiter
                if (i < len(joined_string) - 1 and
                    joined_string[i] == '\\' and
                    joined_string[i+1:i+1+len(delimiter)] == delimiter):
                    current_part += delimiter
                    i += len(delimiter) + 1
                else:
                    current_part += joined_string[i]
                    i += 1

        # Add the last part
        parts.append(current_part)

        return parts

    def invoke(self, context: InvocationContext) -> StringCollectionOutput:
        result = self.string
        if self.unescape_delimiter:
            result = self.split_with_delimiter(self.string, self.delimiter)
        else:
            result = result.split(self.delimiter)
        return StringCollectionOutput(collection=result)