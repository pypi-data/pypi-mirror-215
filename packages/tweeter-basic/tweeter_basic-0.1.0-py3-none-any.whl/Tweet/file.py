import json

def write(file_path, contents):
    with open(file_path, "w") as f:
        json.dump(contents, f)

def read(file_path):
    with open(file_path, "r") as f:
        output = json.load(f)
    return output
