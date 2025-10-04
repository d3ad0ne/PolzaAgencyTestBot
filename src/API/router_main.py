from fastapi import APIRouter, Body
from . import resume_scraper


router = APIRouter(prefix='/api')


@router.post('/resume')
async def resume(body: str = Body(media_type="text/plain")):
    skills = [ 
    "python", "java", "c++", "javascript", "html", "css", "sql", "excel",  
    "tableau", "power bi", "aws", "docker", "kubernetes", "git", "bash",  
    "linux", "pandas", "numpy", "scikit-learn", "tensorflow", "keras",  
    "pytorch", "nlp", "machine learning", "data analysis", "data visualization",  
    "project management", "communication", "leadership", "teamwork",  
    "problem solving", "analytical thinking", "agile", "scrum",  
    "powerpoint", "presentation", "cloud", "design patterns"  
    ]
    doc_text = body
    resume_skills = await resume_scraper.skillsFinder(doc_text, skills)
    return {'skills': resume_skills}
