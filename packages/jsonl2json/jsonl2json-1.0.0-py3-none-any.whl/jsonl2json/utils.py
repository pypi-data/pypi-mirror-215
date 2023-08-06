import json

def is_jsonl_file(file_path):
    """
    Checks if the given file path is a valid JSONL file.

    Args:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file is a valid JSONL file, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Check if each line is a valid JSON object
            for line in file:
                json.loads(line)
        return True
    except (json.JSONDecodeError, FileNotFoundError):
        return False