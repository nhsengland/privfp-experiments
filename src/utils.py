import os
import json


def write(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(data)


def load_json(from_variable, from_path):
    if not from_variable and not from_path:
        raise ValueError("Either from_variable or from_path must be provided.")

    elif from_variable and from_path:
        raise ValueError(
            "Both from_variable and from_path cannot be provided at the same time."
        )

    elif from_variable:
        output = json.loads(from_variable)

    else:
        with open(from_path) as file:
            output = json.load(file)

    return output
