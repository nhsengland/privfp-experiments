import re


def remove_titles(name):
    # Define a list of common titles to remove
    titles = ["Mrs", "Mr", "Ms", "Dr", "Prof", "Miss", "Doctor"]

    # Create a regular expression pattern to match any title followed by an optional dot and space.
    pattern = r"^(?:" + "|".join(titles) + r")(?:\.\s)?(?:\.)?"

    # Replace all occurrences of titles with an empty string
    cleaned_name = re.sub(pattern, "", name, flags=re.IGNORECASE)

    return cleaned_name
