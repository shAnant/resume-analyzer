from pypdf import PdfReader
import re



def extract_text(path):
    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def extract_skil(text):

    skills = {}

    match = re.search(
        r"Skills(.*?)(Projects|Certifications|Education)",
        text,
        re.S | re.I
    )

    if not match:
        return []

    skills_text = match.group(1)

    lines = skills_text.split("\n")

    for line in lines:

        if ":" in line:

            category, values = line.split(":", 1)

            items = [
                v.strip()
                for v in values.split(",")
                if v.strip()
            ]

            skills[category.strip()] = items

    skills_list = []

    for category in skills:
        skills_list.extend(skills[category])

    return skills_list


