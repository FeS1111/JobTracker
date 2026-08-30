from job_tracker.models import VacancyStatus
from models import Vacancy

class JobTracker:
    def __init__(self, vacancies: list[Vacancy] | None = None):
        if vacancies is None:
            self.vacancies: list[Vacancy] = []
        else:
            self.vacancies = vacancies.copy()

    def  add_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)

    def remove_vacancy(self, company: str, title: str) -> Vacancy:
        for vacancy in self.vacancies:
            if vacancy.company == company and vacancy.title == title:
                self.vacancies.remove(vacancy)
                return vacancy
        raise ValueError(
            f"Вакансия '{title}' в компании '{company}' не найдена"
        )

    def find_by_company(self, company: str) -> list[Vacancy]:
        search_results = []
        for vacancy in self.vacancies:
            if vacancy.company == company:
                search_results.append(vacancy)
        return search_results

    def find_vacancy(self, company: str, title: str) -> Vacancy | None :
        for vacancy in self.vacancies:
            if vacancy.company == company and vacancy.title == title:
                return vacancy

        return None

    def filter_by_status(self, status: VacancyStatus) -> list[Vacancy]:
        search_results = []
        for vacancy in self.vacancies:
            if vacancy.status == status:
                search_results.append(vacancy)
        return search_results

    def update_status(self, company: str, title: str, status: VacancyStatus) -> Vacancy:
        vacancy = self.find_vacancy(company, title)
        if vacancy is None:
            raise ValueError(
                f"Вакансия '{title}' в компании '{company}' не найдена"
            )
        vacancy.status = status
        return vacancy


    def get_all_vacancies(self) -> list[Vacancy]:
        return self.vacancies.copy()

    def technology_statistics(self) -> dict[str, int]:
        dictionary = {}
        for vacancy in self.vacancies:
            for technology in vacancy.technologies:
                if technology in dictionary:
                    dictionary[technology] += 1
                else:
                    dictionary[technology] = 1
        return dictionary


