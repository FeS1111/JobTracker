from job_tracker.database import SessionLocal
from job_tracker.repository import (
    create_vacancy,
    find_vacancy,
    get_all_vacancies,
)

with SessionLocal() as session:
    vacancy = create_vacancy(
        session=session,
        company="Ozon",
        title="Python Backend Developer",
        salary=200000,
        technologies=[
            "Python",
            "PostgreSQL",
            "FastAPI",
        ],
    )
    print("Вакансия создана: ")
    print(vacancy.id, vacancy.company, vacancy.title)

with SessionLocal() as session:
    vacancy = find_vacancy(
        session=session,
        company='Yandex',
        title='ML Engineer',
    )
    print("Вакансия найдена: ")
    print(vacancy)

with SessionLocal() as session:
    vacancies = get_all_vacancies(session=session)
    print("Все вакансии: ")
    for vacancy in vacancies:
        print(vacancy.id, vacancy.company, vacancy.title, vacancy.status)
