from pypdf import PdfReader
import re

# path = "Arpit Chudhary DL.pdf"
# text = ""

# for page in reader.pages:
#     text += page.extract_text()
    
def extract_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        textr += page.extract_text()
    return text

def extract_skills(text):
    skills = {}
    match = re.search(r"Skills(.*?)(Projects|Certifications|Education)", text, re.S | re.I)
    
    if not match:
        return {}
    
    skills_text = match.group(1)
    
    lines = skills_text.split("\n")
    
    for line in lines :
        if ":" in line :
            category, values = line.split(":",1)
            
            category = category.strip()
            
            items = [v.strip() for v in values.split(",") if v.strip()]
            skills[category] = items
            
    skills_list = []
    for skill in skills:
        skills_list += skills[skill]
    return skills_list

def dict_of_skills_to_list(skills):
    skills_list = []
    for skill in skills:
        skills_list += skills[skill]
    return skills_list


# skills = extract_skills(text)
# list_of_skills = dict_of_skills_to_list(skills)
# print(list_of_skills)