import unittest
import os

from agency_server.tools.code_changes_tool import apply_code_changes

class TestCodeChanges(unittest.TestCase):

    def setUp(self):
        # Create a sample file to test against
        self.test_file_path = 'test_file.py'
        with open(self.test_file_path, 'w') as f:
            f.write("def hello_world():\n")
            f.write("    print('Hello, world!')\n\n")
            f.write("# End of function\n")

    def test_insert_snippet(self):
        # Arrange
        snippet = "    print('Inserted line')"
        start_pattern = "# End of function"
        apply_code_changes(self.test_file_path, snippet, start_pattern, mode="insert")
        
        # Act
        with open(self.test_file_path, 'r') as f:
            content = f.readlines()

        # Assert
        self.assertIn(snippet + "\n", content)

    def test_delete_lines(self):
        # Arrange
        start_pattern = "def hello_world():"
        end_pattern = "# End of function"
        apply_code_changes(self.test_file_path, '', start_pattern, end_pattern, mode="delete")
        
        # Act
        with open(self.test_file_path, 'r') as f:
            content = f.readlines()

        # Assert
        self.assertEqual(len(content), 1)

    def test_replace_lines(self):
        # Arrange
        snippet = "    print('Replaced line')"
        start_pattern = "def hello_world():"
        end_pattern = "# End of function"
        apply_code_changes(self.test_file_path, snippet, start_pattern, end_pattern, mode="replace")
        
        # Act
        with open(self.test_file_path, 'r') as f:
            content = f.readlines()

        # Assert
        self.assertIn(snippet + "\n", content)
        self.assertNotIn("    print('Hello, world!')\n", content)
        
    def tearDown(self):

    def test_create_mode(self):
        # Arrange
        snippet = "print('New file created')"
        test_file_path = 'new_test_file.py'

        # Act
        result = apply_code_changes(test_file_path, snippet, mode="create")

        # Assert
        self.assertTrue(os.path.exists(test_file_path))
        with open(test_file_path, 'r') as f:
            content = f.read().strip()
        self.assertEqual(content, snippet)

        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

    def test_error_handling_patterns_not_found(self):
        # Arrange
        snippet = ""
        start_pattern = "non_existent_start_pattern"
        end_pattern = "non_existent_end_pattern"

        # Act
        result = apply_code_changes(self.test_file_path, snippet, start_pattern, end_pattern, mode="replace")

        # Assert
        self.assertIn("pattern not found", result.lower())

    def test_error_handling_invalid_mode(self):
        # Arrange
        snippet = ""
        mode = "invalid_mode"

        # Act
        result = apply_code_changes(self.test_file_path, snippet, mode=mode)

        # Assert
        self.assertIn("invalid mode", result.lower())

        # Clean up the test file
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

if __name__ == '__main__':
    unittest.main()