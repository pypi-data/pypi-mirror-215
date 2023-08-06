import json

class JsonlToJsonFormatter:
    """
    A class for formatting JSONL files to a single JSON array.

    Attributes:
        input_file_path (str): The path to the input JSONL file.
        output_file_path (str): The path to the output JSON file.
    """
    def __init__(self, input_file_path, output_file_path):
        """
        Constructs a new JsonlToJsonFormatter instance with the given input and output file paths.

        Args:
            input_file_path (str): The path to the input JSONL file.
            output_file_path (str): The path to the output JSON file.
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def format(self):
        """
        Reads the input JSONL file and writes a JSON array to the output JSON file.
        """
        with open(self.input_file_path, 'r', encoding='utf-8') as input_file, open(self.output_file_path, 'w') as output_file:
            # Load all the JSON objects from the input file
            objects = [json.loads(line) for line in input_file]
            
            # Write the objects to the output file
            output_file.write('[')
            json.dump(objects[0], output_file)
            for obj in objects[1:]:
                output_file.write(',')
                json.dump(obj, output_file)
            
            # Close the array in the output file
            output_file.write(']')