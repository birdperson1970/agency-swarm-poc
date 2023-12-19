import unittest
from unittest.mock import MagicMock, mock_open, patch
from agency_server.tools.file_patch_tool import FilePatchTool


class TestFilePatchTool(unittest.TestCase):
    def setUp(self):
        # Initialize the FilePatchTool with a sample file path and content
        self.file_path = "test.txt"
        self.snippet = "Test snippet"
        self.start_pattern = "## Start"
        self.end_pattern = "## End"
        self.sample_file_content = """
            Line 1

            ## Start

            Line to be replaced

            ## End

            Line 5 

        """

    def test_replace_mode_with_patterns(self, mock_file):
        # Set up a FilePatchTool instance with the replace mode and patterns
        tool = FilePatchTool(
            file_path=self.file_path,
            snippet=self.snippet,
            start_pattern=self.start_pattern,
            end_pattern=self.end_pattern,
            mode="replace",
        )
        result = tool.run()
        mock_file.assert_called_with(self.file_path, "r")
        self.assertEqual(result, "Code changes successfully applied.")

    # Test case for delete mode with line numbers
    def test_delete_mode_with_line_numbers(self, mock_file):
        # Set up a FilePatchTool instance with the delete mode and line numbers
        tool = FilePatchTool(
            file_path=self.file_path,
            snippet=self.snippet,
            start_line=2,
            end_line=4,
            mode="delete",
        )
        result = tool.run()
        mock_file.assert_called_with(self.file_path, "r")
        self.assertEqual(result, "Code changes successfully applied.")

    # Test case for insert mode with start pattern
    def test_insert_mode_with_start_pattern(self, mock_file):
        # Set up a FilePatchTool instance with the insert mode and a start pattern
        tool = FilePatchTool(
            file_path=self.file_path,
            snippet=self.snippet,
            start_pattern=self.start_pattern,
            mode="insert",
        )
        result = tool.run()
        mock_file.assert_called_with(self.file_path, "r")
        self.assertEqual(result, "Code changes successfully applied.")

    # Test case for invalid mode error handling
    def test_invalid_mode(self, mock_file):
        # Set up a FilePatchTool instance with an invalid mode
        tool = FilePatchTool(
            file_path=self.file_path, snippet=self.snippet, mode="invalid_mode"
        )
        result = tool.run()
        self.assertEqual(result, "Invalid mode specified.")

    # Test case for pattern not found error handling
    @patch("builtins.open", new_callable=mock_open, read_data="Line without patterns")
    def test_pattern_not_found(self, mock_file):
        # Set up a FilePatchTool instance with patterns that don't exist in the file content
        tool = FilePatchTool(
            file_path=self.file_path,
            snippet=self.snippet,
            start_pattern="Nonexistent start pattern",
            end_pattern="Nonexistent end pattern",
            mode="replace",
        )
        result = tool.run()
        self.assertEqual(result, "Start or end pattern/line not found.")

    # Test case for creating a new file with the 'create' mode
    @patch("builtins.open", new_callable=mock_open)
    def test_create_mode(self, mock_file):
        # Set up a FilePatchTool instance with the 'create' mode
        tool = FilePatchTool(
            file_path=self.file_path, snippet=self.snippet, mode="create"
        )
        mock_file.return_value = MagicMock()
        result = tool.run()
        mock_file.assert_called_with(self.file_path, "w")
        mock_file.return_value.write.assert_called_with(self.snippet + "")
        self.assertEqual(result, "Code changes successfully applied.")
