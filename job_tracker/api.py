from http.client import HTTPException

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from job_tracker.database import get_db
from job_tracker import repository
from job_tracker.schemas import VacancyResponse, VacancyCreate, VacancyStatusUpdate
from job_tracker.storage import load_vacancies, save_vacancies
from job_tracker.tracker import JobTracker
from job_tracker.models import Vacancy, VacancyStatus
from job_tracker.db_models import VacancyORM
app = FastAPI(
    title="JobTracker API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Job Tracker API is running"}

#vacancies = load_vacancies()
#tracker = JobTracker(vacancies)

def vacancy_orm_to_response(vacancy: VacancyORM) -> VacancyResponse:
    return VacancyResponse(
        company=vacancy.company,
        title=vacancy.title,
        salary=vacancy.salary,
        status=vacancy.status,
        technologies=[technology.name for technology in vacancy.technologies],
    )

@app.get(
    "/vacancies",
    response_model=list[VacancyResponse]
)

def get_vacancies(session: Session = Depends(get_db), status: VacancyStatus | None = None):

    if status is None:
        vacancies = repository.get_all_vacancies(session)
    else:
        vacancies = repository.get_vacancies_by_status(session, status)

    return [vacancy_orm_to_response(vacancy) for vacancy in vacancies]

@app.post(
    "/vacancies",
    response_model=VacancyResponse,
    status_code= 201
)

def create_vacancy(vacancy_data: VacancyCreate, session: Session = Depends(get_db)):
    existing_vacancy = repository.find_vacancy(
        session,
        vacancy_data.company,
        vacancy_data.title
    )

    if existing_vacancy is not None:
        raise HTTPException(
            status_code=409,
            detail="Вакансия уже существует"
        )

    vacancy = repository.create_vacancy(
        session=session,
        company=vacancy_data.company,
        title=vacancy_data.title,
        salary=vacancy_data.salary,
        technologies=vacancy_data.technologies,
    )

    return vacancy_orm_to_response(vacancy)

@app.get(
    "/vacancies/search",
    response_model=VacancyResponse
)

def get_vacancy(company:str, title:str, session: Session = Depends(get_db)):
    vacancy = repository.find_vacancy(session, company, title)
    if vacancy is None:
        raise HTTPException(
            status_code=404,
            detail="Вакансия не найдена"
        )
    return vacancy_orm_to_response(vacancy)

@app.patch(
    "/vacancies/status",
    response_model=VacancyResponse
)

def vacancy_status_update(
        company: str,
        title: str,
        status_data: VacancyStatusUpdate,
        session: Session = Depends(get_db)
):
    try:
        updated_vacancy = repository.update_status(
            session,
            company,
            title,
            status_data.status
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    return vacancy_orm_to_response(updated_vacancy)

@app.delete(
    "/vacancies",
    response_model=VacancyResponse
)

def delete_vacancy(company:str, title:str, session: Session = Depends(get_db)):
    try:
        deleted_vacancy = repository.delete_vacancy(
            session,
            company,
            title
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    return vacancy_orm_to_response(deleted_vacancy)



@app.get(
    "/statistics/technologies"
)

def get_technologies(session: Session = Depends(get_db)) -> dict[str, int]:
    return repository.get_technology_statistics(session)