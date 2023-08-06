# Jsonl2json

A Python library for converting data in the JSON Lines (.jsonl) format to the standard JSON (.json) format

## Installation

You can install `jsonl2json` using `pip`:
<br>

```shell
pip install jsonl2json
```

## Usage

You can use `jsonl2json` in your Python code like this:

```python
from jsonl2json import JsonlToJsonFormatter

jsonl = JsonlToJsonFormatter('input.jsonl', 'output.json')
jsonl.to_json()
```

This will read the input file input.jsonl and write a JSON array to the output file output.json.

# License

jsonltojson is released under the MIT `License.txt`. See LICENSE for more information.
