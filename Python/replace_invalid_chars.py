# Replace forward slash with underscore
filename = "my/document.txt"
new_filename = filename.replace("/", "_")
print(new_filename) # my_document.txt

# Replace only the first colon with a dash
time = "12:34:56"
new_time = time.replace(":", "-", 1)
print(new_time) # 12-34:56

# Replace all invalid characters with underscore using a loop
filename = "my*document?.txt"
invalid_chars = "<>:\"/\\|?*"
for char in invalid_chars:
    filename = filename.replace(char, "_")
print(filename) # my_document_.txt

# Replace all invalid characters with underscore using a regular expression
import re
filename = "my*document?.txt"
invalid_chars = "<>:\"/\\|?*"
pattern = "[" + re.escape(invalid_chars) + "]"
filename = re.sub(pattern, "_", filename)
print(filename) # my_document_.txt

