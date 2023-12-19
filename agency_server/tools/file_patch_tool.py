import os
from typing import Optional

from pydantic import Field

from agency_swarm.tools.base_tool import BaseTool


class FilePatchTool(BaseTool):
    # Define the fields with descriptions using Pydantic Field
    file_path: str = Field(
        ...,
        description="Specify the absolute path to the file that you want to make changes to. This should be the absolute path starting from the root directory. It is important to ensure the path entered here is correct to avoid errors when applying your changes.",
    )
    snippet: str = Field(
        ...,
        description="Enter the exact portion of the code or text that you want to use for comparison or to replace, delete, or insert into the file. Ensure that this snippet accurately reflects the changes you intend to implement including whitespace formating. Missing or extra characters could cause unexpected results.",
    )

    start_line: int = Field(
        None,
        description="This is a line number marking the beginning of the section in the file where the changes should start.",
    )

    end_line: Optional[int] = Field(
        None,
        description="This is a line number marking the end of the section to 'replace' or 'delete' lines.",
    )
    mode: Optional[str] = Field(
        None,
        description="Choose the operation mode from 'create', 'delete', 'replace', or 'insert'. Select 'delete' if you want to remove the text between the start and end lines. Choose 'replace' to substitute this text with the snippet provided, and 'insert' to add the snippet directly after the start line, preserving any existing content.",
    )

    def run(self):
        if self.mode == "create":
            # Create a new file with the snippet
            with open(self.file_path, "w") as file:
                file.writelines([line + "\n" for line in self.snippet.split("\n")])
            return "File created successfully."

        else:
            # Read the original file content
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            if self.start_line is None:
                return "Start line not found."
            start_index = (
                self.start_line - 1
            )  # Adjusting because list index starts at 0
            if self.end_line is not None:
                end_index = self.end_line

            if self.mode == "replace":
                # Replace the range of lines with the snippet
                snippet_lines = self.snippet.split("\n")
                lines[start_index : end_index] = [
                    line + "\n" for line in snippet_lines
                ]
            elif self.mode == "insert":
                # Insert the snippet at the start_index
                snippet_lines = self.snippet.split("\n")
                for i, snippet_line in enumerate(snippet_lines):
                    lines.insert(start_index + i + 1, snippet_line + "\n")
            elif self.mode == "delete":
                del lines[start_index:end_index]

        # Write the updated content back to the file
        with open(self.file_path, "w") as file:
            file.writelines(lines)

        return "Code changes successfully applied."
