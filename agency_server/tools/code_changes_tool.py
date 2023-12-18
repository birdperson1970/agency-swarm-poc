# Function to apply a code snippet to an existing file with options to insert, delete, or replace lines
def apply_code_changes(file_path, snippet, start_pattern, end_pattern=None, mode="insert"):
    # Read the original file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Identify the start and end points for modification
    start_index = end_index = None
    for i, line in enumerate(lines):
        if start_pattern in line:
            start_index = i
        if end_pattern and end_pattern in line:
            end_index = i
            break
    
    if start_index is None:
        return "Start pattern not found."

    if mode == "delete":
        # Delete the range of lines from start_index up to but not including end_index
        del lines[start_index:end_index]
    elif mode == "replace":
        # Replace the range of lines with the snippet
        snippet_lines = snippet.split("\n")
        lines[start_index:end_index+1] = [line + "\n" for line in snippet_lines]
    elif mode == "insert":
        # Insert the snippet at the start_index
        snippet_lines = snippet.split("\n")
        for i, snippet_line in enumerate(snippet_lines):
            lines.insert(start_index + i + 1, snippet_line + "\n")
    else:
        return "Invalid mode specified."

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
    
    return "Code changes successfully applied."

