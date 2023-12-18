from typing import Optional

from pydantic import Field

from agency_swarm.tools.base_tool import BaseTool


class FilePatchTool(BaseTool):
    # Define the fields with descriptions using Pydantic Field
    file_path: str = Field(
        ...,
        description="Specify the complete path to the file that you want to make changes to. This should be the absolute path starting from the root or a relative path from the current working directory. It is important to ensure the path entered here is correct to avoid errors when applying your changes.",
    )
    snippet: str = Field(
        ...,
        description="Enter the exact portion of the code or text that you want to use for comparison or to replace, delete, or insert into the file. Ensure that this snippet accurately reflects the changes you intend to implement including whitespace formating. Missing or extra characters could cause unexpected results.",
    )
    start_pattern: Optional[str] = Field(
        None,
        description="Provide a unique pattern or line of code that marks the beginning of the section in the file where the changes should start. This must uniquely identify the location within the file to start making changes, being specific helps to avoid applying changes in the wrong place.",
    )
    start_line: Optional[int] = Field(
        None,
        description="An alternative to 'start_pattern', this is a line number marking the beginning of the section in the file where the changes should start.",
    )
    end_pattern: Optional[str] = Field(
        None,
        description="Provide a corresponding pattern or line of code that marks the end of the section where the changes will stop. This is important for defining a precise area for modification and should immediately follow the area described by the start pattern.",
    )
    end_line: Optional[int] = Field(
        None,
        description="An alternative to 'end_pattern', this is a line number marking the end of the section where the changes will stop.",
    )
    mode: Optional[str] = Field(
        None,
        description="Choose the operation mode from 'delete', 'replace', or 'insert'. Select 'delete' if you want to remove the text between the start and end patterns. Choose 'replace' to substitute this text with the snippet provided, and 'insert' to add the snippet directly after the start pattern, preserving any existing content.",
    )

    def run(self):
        # Read the original file content
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        if self.start_line is not None and self.end_line is not None:
            start_index = (
                self.start_line - 1
            )  # Adjusting because list index starts at 0
            end_index = self.end_line
        else:
            # Identify the start and end points for modification based on patterns
            for i, line in enumerate(lines):
                if self.start_pattern and self.start_pattern in line:
                    start_index = i
                if self.end_pattern and self.end_pattern in line:
                    end_index = i
                    break

        if start_index is None or (self.end_pattern is not None and end_index is None):
            return "Start or end pattern/line not found."
            return "Start pattern not found."

        if self.mode == "delete":
            # Delete the range of lines from start_index up to but not including end_index
            del lines[start_index:end_index]
        elif self.mode == "replace":
            # Replace the range of lines with the snippet
            snippet_lines = self.snippet.split("\n")
            lines[start_index : end_index + 1] = [line + "\n" for line in snippet_lines]
        elif self.mode == "insert":
            # Insert the snippet at the start_index
            snippet_lines = self.snippet.split("\n")
            for i, snippet_line in enumerate(snippet_lines):
                lines.insert(start_index + i + 1, snippet_line + "\n")
        elif self.mode == "create":
            # Create a new file with the snippet
            with open(self.file_path, "w") as file:
                file.writelines([line + "\n" for line in self.snippet.split("\n")])
            return "Invalid mode specified."

        # Write the updated content back to the file
        with open(self.file_path, "w") as file:
            file.writelines(lines)

        return "Code changes successfully applied."
