
from typing import Optional

from pydantic import Field

from agency_swarm.tools.base_tool import BaseTool


class FilePatchTool(BaseTool):
    # Define the fields with descriptions using Pydantic Field
    file_path: str = Field(
        ..., description="The target file path."
    )
    snippet: str = Field(
        ..., description="The modified content to compare with the original file."
    )
    start_pattern: Optional[str] = Field(
        None, description="The start pattern."
    )
    end_pattern: Optional[str] = Field(
        None, description="The end pattern."
    )
    mode: Optional[str] = Field(
        None, description="delete, replace, insert"
    )

    def run(self):     
        # Read the original file content
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        # Identify the start and end points for modification
        start_index = end_index = None
        for i, line in enumerate(lines):
            if self.start_pattern in line:
                start_index = i
            if self.end_pattern and self.end_pattern in line:
                end_index = i
                break
        
        if start_index is None:
            return "Start pattern not found."

        if self.mode == "delete":
            # Delete the range of lines from start_index up to but not including end_index
            del lines[start_index:end_index]
        elif self.mode == "replace":
            # Replace the range of lines with the snippet
            snippet_lines = self.snippet.split("\n")
            lines[start_index:end_index+1] = [line + "\n" for line in snippet_lines]
        elif self.mode == "insert":
            # Insert the snippet at the start_index
            snippet_lines = self.snippet.split("\n")
            for i, snippet_line in enumerate(snippet_lines):
                lines.insert(start_index + i + 1, snippet_line + "\n")
        else:
            return "Invalid mode specified."

        # Write the updated content back to the file
        with open(self.file_path, 'w') as file:
            file.writelines(lines)
        
        return "Code changes successfully applied."

