import unittest
import os
from agency_server.tools.file_patch_tool import FilePatchTool


class TestFilePatchTool(unittest.TestCase):

    def setUp(self):
        # Setup a dummy file for testing
        self.dummy_file_path = 'dummy_file.txt'
    

    def tearDown(self):
        # Remove the dummy file after testing
        os.remove(self.dummy_file_path)

    def test_create_snippet_valid(self):
        # Test creating a snippet in a file
# Test creating a snippet in a file
        result = FilePatchTool(file_path=self.dummy_file_path, snippet='Line 1\n\tLine 2\n\t\tLine 3\n', mode='create').run()
# Test deleting a snippet in a file

        result = FilePatchTool(file_path=self.dummy_file_path, snippet='\t\t\tReplaced Line 2', start_line=2, end_line=2, mode='replace').run()
# Test inserting a snippet in a file
        result = FilePatchTool(file_path=self.dummy_file_path, snippet='Replaced Line 2', start_line=2, end_line=2, mode='replace').run()
        result = FilePatchTool(file_path=self.dummy_file_path, snippet='\tInserted Line 3', start_line=2, mode='insert').run()
        with open(self.dummy_file_path, 'r') as dummy_file:
            content = dummy_file.readlines()
            self.assertEqual(content[3], '\t\tLine 3\n', "Snippet Inserted Line should be inserted after line 2.")
        result = FilePatchTool(file_path=self.dummy_file_path, snippet='Inserted Line', start_line=2, mode='insert').run()
        # Test replacing a snippet in a file
        result = FilePatchTool(file_path=self.dummy_file_path, snippet='Line 2\n', start_line=2, end_line=2, mode='delete').run()
        result = FilePatchTool(file_path=self.dummy_file_path, snippet='Line 2\n', start_line=2, end_line=2, mode='delete').run()

    # def test_insert_snippet_valid(self):
        # Test inserting a snippet in a file
#        file_patch_tool = FilePatchTool()
        # TODO: implement insert snippet logic and assertions

    # Additional tests for edge cases can be added here

if __name__ == '__main__':
    unittest.main()
