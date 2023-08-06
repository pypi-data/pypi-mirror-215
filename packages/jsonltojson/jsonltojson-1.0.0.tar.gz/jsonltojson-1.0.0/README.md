# jsonltojson

A Python package for formatting JSONL files to a single JSON array.

## Installation

#### Unix-based systems (macOS, Linux)

You can install `jsonltojson` using `pip`:
```pip3 install jsonltojson```

#### Other operating systems
```pip install jsonltojson```
## Usage

You can use `jsonltojson` in your Python code like this:

```
from jsonltojson import JsonlToJsonFormatter

formatter = JsonlToJsonFormatter('input.jsonl', 'output.json')
formatter.format()
```
This will read the input file input.jsonl and write a JSON array to the output file output.json.

# License
jsonltojson is released under the MIT ```License.txt```. See LICENSE for more information.