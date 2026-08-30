from models import Vacancy, VacancyStatus
from tracker import JobTracker
from storage import load_vacancies,save_vacancies

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

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()