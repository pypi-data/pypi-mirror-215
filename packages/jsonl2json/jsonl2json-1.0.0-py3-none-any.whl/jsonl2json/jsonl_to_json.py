import json
from .utils import is_jsonl_file

class JsonlToJsonFormatter:
    """
    A class for formatting JSONL files to a single JSON array.

    Attributes:
        input_file_path (str): The path to the input JSONL file.
        output_file_path (str): The path to the output JSON file.
    """
    def __init__(self, input_file_path: str, output_file_path: str):
        """
        Constructs a new JsonlToJsonFormatter instance with the given input and output file paths.

        Args:
            input_file_path (str): The path to the input JSONL file.
            output_file_path (str): The path to the output JSON file.
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def to_json(self, pretty_print=False):
        """
        Reads the input JSONL file and writes a JSON array to the output JSON file.

        Args:
            pretty_print (bool): Whether to pretty-print the output JSON. Defaults to False.
        """
        if not is_jsonl_file(self.input_file_path):
            print(f"Error: {self.input_file_path} is not a valid JSONL file")
            return

        try:
            with open(self.input_file_path, 'r', encoding='utf-8') as input_file, open(self.output_file_path, 'w') as output_file:
                # Write the opening bracket for the JSON array
                output_file.write('[')

                # Load and write each JSON object to the output file
                for line in input_file:
                    obj = json.loads(line)
                    if pretty_print:
                        json.dump(obj, output_file, indent=4)
                    else:
                        json.dump(obj, output_file)
                    output_file.write(',')

                # Remove the trailing comma and write the closing bracket for the JSON array
                output_file.seek(output_file.tell() - 1)
                output_file.write(']')

        except FileNotFoundError:
            print(f"Error: File not found at {self.input_file_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON object in {self.input_file_path}")
        except:
            print("Error: Unknown error occurred")