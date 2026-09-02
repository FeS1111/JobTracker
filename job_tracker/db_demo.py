from sqlalchemy import inspect, select

from job_tracker.database import SessionLocal
from job_tracker.db_models import VacancyORM
from job_tracker.models import VacancyStatus

vacancy = VacancyORM(
    company='Ozon',
    title='Python Backend Developer',
    salary=250000,
    status=VacancyStatus.NEW,
)

state = inspect(vacancy)

print("После создания объекта:")
print("transient:", state.transient)
print("pending:", state.pending)
print("persistent:", state.persistent)

with SessionLocal() as session:
    session.add(vacancy)
    state = inspect(vacancy)
    print("\nПосле session.add():")
    print("transient:", state.transient)
    print("pending:", state.pending)
    print("persistent:", state.persistent)

    session.flush()
    state = inspect(vacancy)

    print("\nПосле flush():")
    print("transient:", state.transient)
    print("pending:", state.pending)
    print("persistent:", state.persistent)

    print("ID:", vacancy.id)

    session.commit()
    print("\nПосле commit:")
    print("ID:", vacancy.id)

with SessionLocal() as session:
    statement = select(VacancyORM).where(VacancyORM.company == 'Ozon')
    res = session.execute(statement)
    vacancies = res.scalars().all()

    for vacancy in vacancies:
        print(vacancy.id,vacancy.company,vacancy.title,vacancy.salary,vacancy.status)