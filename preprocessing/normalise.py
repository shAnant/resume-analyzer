import re

def normalise(skill):

    return re.sub(
        r"[^\w\s]",
        "",
        skill.lower()
    ).strip()