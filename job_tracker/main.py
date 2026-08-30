from job_tracker.models import Vacancy, VacancyStatus
from job_tracker.tracker import JobTracker
from job_tracker.storage import load_vacancies,save_vacancies

def print_menu() -> None:
    print("\n===== Job Tracker =====")
    print("1. Показать все вакансии")
    print("2. Добавить вакансию")
    print("3. Найти по компании")
    print("4. Изменить статус")
    print("5. Удалить вакансию")
    print("6. Статистика технологий")
    print("0. Выход")

def print_vacancy(vacancy: Vacancy) -> None:
    technologies = ", ".join(vacancy.technologies)

    salary = (
        f"{vacancy.salary:,} ₽".replace(",", " ")
        if vacancy.salary is not None
        else "Не указана"
    )

    print("-" * 40)
    print(f"Компания:     {vacancy.company}")
    print(f"Вакансия:     {vacancy.title}")
    print(f"Зарплата:     {salary}")
    print(f"Статус:       {vacancy.status.value}")
    print(f"Технологии:   {technologies}")
    print("-" * 40)

def print_technology_statistics(technology_statistics: dict[str, int]) -> None:
    print("\n" + "-" * 40)
    print("Статистика технологий:")
    print("-" * 40)

    sorted_statistics = sorted(technology_statistics.items(), key=lambda item: item[1], reverse=True)

    for technology, count in sorted_statistics:
        print(f"{technology}: {count}")
    print("-" * 40)

def main() -> None:
    vacancies = load_vacancies()
    tracker = JobTracker(vacancies)

    while True:
        print_menu()

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            data = tracker.get_all_vacancies()
            if not data:
                print("Список вакансий пуст.")
            else:
                for vacancy in data:
                    print_vacancy(vacancy)

        elif choice == "2":
            company = input("Введите название компании: ").strip()
            title = input("Введите название вакансии: ").strip()
            salary = int(input("Введите ЗП: ").strip())

            technologies_input = input(
                "Введите технологии через запятую: "
            )

            technologies = [
                technology.strip()
                for technology in technologies_input.split(",")
            ]

            vacancy = Vacancy(company, title, salary, VacancyStatus.NEW, technologies)
            tracker.add_vacancy(vacancy)
            save_vacancies(tracker.get_all_vacancies())

        elif choice == "3":
            company = input("Введите название компании: ").strip()
            data = tracker.find_by_company(company)
            if not data:
                print("Список вакансий пуст.")
            else:
                for vacancy in data:
                    print_vacancy(vacancy)

        elif choice == "4":
            company = input("Введите название компании: ").strip()
            title = input("Введите название акансии: ").strip()

            print("Доступные статусы:\n", "1. new\n", "2. applied\n", "3. interview\n", "4. rejected")
            status_input = input("Выберите новый статус: ").strip()

            status_map = {
                "1": VacancyStatus.NEW,
                "2": VacancyStatus.APPLIED,
                "3": VacancyStatus.INTERVIEW,
                "4": VacancyStatus.REJECTED,
            }

            new_status = status_map.get(status_input)
            if new_status is None:
                print("Введен неверный статус!")
            else:
                try:
                    updated_vacancy = tracker.update_status(company, title, new_status)
                    save_vacancies(tracker.get_all_vacancies())
                    print(
                        f"Статус вакансии '{updated_vacancy.title}' "
                        f"изменён на '{updated_vacancy.status.value}'"
                    )
                except ValueError as error:
                    print(error)

        elif choice == "5":
            company = input("Введите название компании: ").strip()
            title = input("Введите название акансии: ").strip()
            try:
                deleted_vacancy = tracker.remove_vacancy(company, title)
                save_vacancies(tracker.get_all_vacancies())
                print(
                    f"Вакансия '{deleted_vacancy.title}' "
                    f"в компании '{deleted_vacancy.company}' удалена."
                )
            except ValueError as error:
                print(error)

        elif choice == "6":
            data = tracker.technology_statistics()
            if not data:
                print("Список технологий пуст.")
            else:
                print_technology_statistics(data)


        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()