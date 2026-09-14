from src.jobmaxxer.filtering import match_job
from src.jobmaxxer.models import Job


def profile():
    return {
        "target_roles": ["AI Engineer", "Python Backend Engineer"],
        "skills": ["Python", "FastAPI", "RAG"],
        "preferred_locations": ["India", "Remote"],
        "max_years_experience": 2,
        "exclude_keywords": ["senior", "staff", "principal", "lead", "manager", "director", "architect"],
        "entry_keywords": ["junior", "graduate", "fresher", "0-2 years", "entry-level"],
    }


def test_entry_level_ai_job_matches():
    job = Job("Example", "Junior AI Engineer", "Bengaluru, India", "https://example.com/job/1", "https://example.com/careers", "Python, FastAPI, RAG. 0-2 years experience.")
    result = match_job(job, profile())
    assert result is not None
    assert result.score > 0


def test_senior_job_is_rejected():
    job = Job("Example", "Senior AI Engineer", "Remote", "https://example.com/job/2", "https://example.com/careers", "Python and RAG. 5+ years experience.")
    assert match_job(job, profile()) is None


def test_unrelated_job_is_rejected():
    job = Job("Example", "Graphic Designer", "India", "https://example.com/job/3", "https://example.com/careers", "Adobe Creative Cloud.")
    assert match_job(job, profile()) is None
