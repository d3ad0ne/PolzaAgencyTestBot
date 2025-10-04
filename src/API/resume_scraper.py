async def skillsFinder(doc_text: str, skills: list[str]):
    skills_in_resume = []
    for skill in skills:
        if skill in doc_text.lower():
            skills_in_resume.append(skill)
    return skills_in_resume
