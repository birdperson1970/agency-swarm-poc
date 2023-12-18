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
        # Clean up the test file
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

if __name__ == '__main__':
    unittest.main()