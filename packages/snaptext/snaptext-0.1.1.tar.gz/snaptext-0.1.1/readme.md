# Snaptext

**Snaptext** is a Python package that provides tools for manipulating strings while retaining source positions in the resulting object.


## Installation

```sh
$ pip install snaptext
```


## Usage

### Indexing, concatenation and stripping

```py
from snaptext import Source

source = Source("123 / 456")

source[0:4].area.format()
# =>
# 123 / 456
# ^^^^

source[0:4].strip().area.format()
# =>
# 123 / 456
# ^^^

(source[0:3] + source[-3:]).area.format()
# =>
# 123 / 456
# ^^^   ^^^
```

### Regular expression matching

```py

text = Source("Pi is about 3.1415.")
match = text.transform_match(text.search(r"(\d+)\.(\d+)"))

match.group().area.format()
# =>
# Pi is about 3.1415.
#             ^^^^^^

match.group(2).area.format()
# =>
# Pi is about 3.1415.
#               ^^^^
```

### Regular expression substitution

```py

text = Source("The sum of 3.02 and 12.8 is 15.82")

result = text.sub(r"(\d+)\.(\d+)", r"\1,\2")
# => 'The sum of 3,02 and 12,8 is 15,82'

result.area.format()
# =>
# The sum of 3.02 and 12.8 is 15.82
# ^^^^^^^^^^^^ ^^^^^^^^^ ^^^^^^^ ^^
```

### Example: JSON parser

```py

from snaptext.json import loads

result = loads("""
{
  "a": "x",
  "b": [13, 14, 15],
  "c": true
}
""")

result.value['b'].value[1].area.format()
# =>
#    "b": [13, 14, 15],
#              ^^
```
