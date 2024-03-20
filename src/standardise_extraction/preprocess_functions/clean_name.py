import re


def remove_titles(name: str):
    """

    Args:
        name (str): An entity that has been extracted from the model.

    Returns:
        (str) : Returns a name that has had titles removed.
    """

    titles = ["Mrs", "Mr", "Ms", "Dr", "Prof", "Miss", "Doctor", "Patient"]
    pattern = r"^(?:" + "|".join(titles) + r")(?:\.\s)?(?:\.)?"
    cleaned_name = re.sub(pattern, "", name, flags=re.IGNORECASE)

    return cleaned_name
