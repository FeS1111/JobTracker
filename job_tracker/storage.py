import json
from pathlib import Path
from dataclasses import asdict
from job_tracker.models import Vacancy, VacancyStatus

STORAGE_PATH = Path(__file__).with_name("vacancies.json")

def vacancy_to_dict(vacancy: Vacancy) -> dict:
    data = asdict(vacancy)
    data['status'] = vacancy.status.value
    return data

def vacancy_from_dict(data: dict) -> Vacancy:
    vacancy_data = data.copy()
    vacancy_data['status'] = VacancyStatus(vacancy_data['status'])
    return Vacancy(**vacancy_data)

def save_vacancies(vacancies: list[Vacancy]) -> None:
    storage = []
    for vacancy in vacancies:
        storage.append(vacancy_to_dict(vacancy))

    with open(STORAGE_PATH, "w", encoding="utf-8") as file:
        json.dump(storage, file, ensure_ascii=False, indent=4)

def load_vacancies() -> list[Vacancy]:
    try:
        with open(STORAGE_PATH, encoding="utf-8") as file:
            storage = json.load(file)

    except FileNotFoundError:
        return []

    except json.decoder.JSONDecodeError:
        return []

    vacancies = []
    for vacancy_data in storage:
        vacancies.append(vacancy_from_dict(vacancy_data))

    return vacancies

