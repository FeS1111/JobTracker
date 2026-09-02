from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from job_tracker.db_models import VacancyORM, TechnologyORM, vacancy_technologies
from job_tracker.models import VacancyStatus


def get_all_vacancies(session: Session) -> list[VacancyORM]:
    statement = select(VacancyORM).options(selectinload(VacancyORM.technologies))

    vacancies = session.scalars(statement).all()
    return list(vacancies)

def find_vacancy(session: Session, company: str, title: str) -> VacancyORM | None:
    statement = (
        select(VacancyORM)
        .options(
            selectinload(VacancyORM.technologies)
        )
        .where(
            VacancyORM.company == company,
            VacancyORM.title == title,
        )
    )
    return session.scalar(statement)

def create_vacancy(
        session: Session,
        company: str,
        title: str,
        salary: int | None,
        technologies: list[str]
) -> VacancyORM:

    vacancy = VacancyORM(
        company=company,
        title=title,
        salary=salary,
        status=VacancyStatus.NEW,
    )

    for technology in technologies:
        vacancy.technologies.append(
            get_or_create_technology(session, technology)
        )

    session.add(vacancy)
    session.commit()
    session.refresh(vacancy)
    return vacancy

def get_or_create_technology(
        session: Session,
        name: str
) -> TechnologyORM:
    statement = select(TechnologyORM).where(TechnologyORM.name == name)

    technology = session.scalar(statement)
    if technology is not None:
        return technology

    technology = TechnologyORM(name=name)
    session.add(technology)
    return technology

def update_status(
        session: Session,
        company: str,
        title: str,
        status: VacancyStatus,
) -> VacancyORM:
    vacancy = find_vacancy(session, company, title)

    if vacancy is None:
        raise ValueError(
            f"Did not find vacancy {title} in {company}"
        )

    vacancy.status = status
    session.commit()
    session.refresh(vacancy)
    return vacancy

def delete_vacancy(session: Session, company: str, title: str) -> VacancyORM:
    vacancy = find_vacancy(session, company, title)
    if vacancy is None:
        raise ValueError(
            f"Did not find vacancy {title} in {company}"
        )
    session.delete(vacancy)
    session.commit()
    return vacancy

def get_vacancies_by_status(session: Session, status: VacancyStatus) -> list[VacancyORM]:
    statement = (select(VacancyORM)
                 .options(selectinload(VacancyORM.technologies))
                 .where(VacancyORM.status == status)
                 )
    vacancies = session.scalars(statement).all()
    return list(vacancies)

def get_technology_statistics(session: Session) -> dict[str, int]:
    statement =(
        select(
            TechnologyORM.name,
            func.count(
                vacancy_technologies.c.vacancy_id
            )
        )
        .join(
            vacancy_technologies,
            TechnologyORM.id == vacancy_technologies.c.technology_id,
        )
        .group_by(
            TechnologyORM.id,
            TechnologyORM.name
        )
    )

    result = session.execute(statement)
    rows = result.all()
    statistics = {}
    for technology, count in rows:
        statistics[technology] = count
    return statistics