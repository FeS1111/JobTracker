from http.client import HTTPException

from fastapi import FastAPI, HTTPException

from job_tracker.schemas import VacancyResponse, VacancyCreate, VacancyStatusUpdate
from job_tracker.storage import load_vacancies, save_vacancies
from job_tracker.tracker import JobTracker
from job_tracker.models import Vacancy, VacancyStatus

app = FastAPI(
    title="JobTracker API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Job Tracker API is running"}

vacancies = load_vacancies()
tracker = JobTracker(vacancies)

@app.get(
    "/vacancies",
    response_model=list[VacancyResponse]
)

def get_vacancies(status: VacancyStatus | None = None):
    if status is None:
        return tracker.get_all_vacancies()
    return tracker.filter_by_status(status)

@app.post(
    "/vacancies",
    response_model=VacancyResponse,
    status_code= 201
)

def create_vacancy(vacancy_data: VacancyCreate):
    existing_vacancy = tracker.find_vacancy(
        vacancy_data.company,
        vacancy_data.title
    )

    vacancy = Vacancy(
        **vacancy_data.model_dump(),
        status=VacancyStatus.NEW
    )

    if existing_vacancy is not None:
        raise HTTPException(
            status_code=409,
            detail="Вакансия уже существует"
        )
    tracker.add_vacancy(vacancy)
    save_vacancies(tracker.get_all_vacancies())
    return vacancy

@app.get(
    "/vacancies/search",
    response_model=VacancyResponse
)

def get_vacancy(company:str, title:str):
    vacancy = tracker.find_vacancy(company, title)
    if vacancy is None:
        raise HTTPException(
            status_code=404,
            detail="Вакансия не найдена"
        )
    return vacancy

@app.patch(
    "/vacancies/status",
    response_model=VacancyResponse
)

def vacancy_status_update(company: str, title: str, status_data: VacancyStatusUpdate):
    try:
        updated_vacancy = tracker.update_status(
            company,
            title,
            status_data.status
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    save_vacancies(tracker.get_all_vacancies())

    return updated_vacancy

@app.delete(
    "/vacancies",
    response_model=VacancyResponse
)

def delete_vacancy(company:str, title:str):
    try:
        deleted_vacancy = tracker.remove_vacancy(
            company,
            title
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    save_vacancies(tracker.get_all_vacancies())

    return deleted_vacancy

@app.get(
    "/statistics/technologies"
)

def get_technologies() -> dict[str, int]:
    return tracker.technology_statistics()