# Files Reader Project

Small project to automatically read all the lines from a file without taking into account resources context and the new lines symbol.

## Usage

```
reader = FileReader("path/of/the_file.txt")
lines = reader.read_all_lines()
```

The resources context is already managed inside the constructor. An FileNotFoundError will be thrown if the file doesn't exist. The returned lines won't have the special characters `\n` or `\r`.

