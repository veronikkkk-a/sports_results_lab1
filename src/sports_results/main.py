from sports_results.exceptions import SportsError
from sports_results.models import AthleteResult
from sports_results.services import (
    add_result,
    calculate_average_result,
    find_by_sport,
    get_all_results,
    get_best_result,
    get_rating,
)


def create_demo_data() -> list[AthleteResult]:
    """Демонстраційні дані для тестування."""
    return [
        AthleteResult(1, "Андрій Шевченко", "Біг 100м", 10.5, "Професіонали"),
        AthleteResult(2, "Олена Олексієнко", "Біг 100м", 11.2, "Дорослі"),
        AthleteResult(3, "Максим Бондар", "Плавання 50м", 22.8, "Професіонали"),
        AthleteResult(4, "Ірина Мельник", "Плавання 50м", 24.1, "Юніори"),
        AthleteResult(5, "Дмитро Коваль", "Біг 100м", 10.8, "Дорослі"),
    ]


def print_results(records: list[AthleteResult], title: str = "Результати") -> None:
    """Форматоване відображення списку у вигляді таблиці."""
    if not records:
        print(f"\n{title}: Список порожній.")
        return

    print(f"\n=== {title.upper()} ===")
    print(f"{'ID':<5} {'Ім\'я спортсмена':<22} {'Вид спорту':<18} {'Результат':<12} {'Категорія':<15}")
    print("-" * 75)
    for r in records:
        print(f"{r.athlete_id:<5} {r.name:<22} {r.sport_type:<18} {r.result:<12.2f} {r.category:<15}")
    print("=" * 75)


def get_float_input(prompt: str) -> float | None:
    """Валідація введення дійсних чисел."""
    try:
        val = float(input(prompt).strip())
        return val
    except ValueError:
        print("Помилка: введіть коректне число.")
        return None


def print_menu() -> None:
    print("\n--- СИСТЕМА ОБЛІКУ СПОРТИВНИХ РЕЗУЛЬТАТІВ ---")
    print("1. Показати всі результати")
    print("2. Додати новий результат")
    print("3. Пошук за видом спорту")
    print("4. Визначити найкращий результат")
    print("5. Обчислити середній результат")
    print("6. Сформувати рейтинг спортсменів")
    print("0. Вихід")


def run_menu(records: list[AthleteResult]) -> None:
    while True:
        print_menu()
        choice = input("Оберіть опцію: ").strip()

        if choice == "1":
            print_results(get_all_results(records), "Усі спортивні результати")

        elif choice == "2":
            name = input("Введіть ім'я спортсмена: ").strip()
            sport_type = input("Введіть вид спорту: ").strip()
            result = get_float_input("Введіть результат (число): ")
            category = input("Введіть категорію (Юніори/Дорослі/Професіонали): ").strip()

            if name and sport_type and result is not None and category:
                try:
                    new_rec = add_result(records, name, sport_type, result, category)
                    print(f"\nУспіх: Додано результат для {new_rec.name}!")
                except SportsError as e:
                    print(f"\nПомилка: {e}")
            else:
                print("\nПомилка: Усі поля мають бути заповнені коректно.")

        elif choice == "3":
            sport = input("Введіть вид спорту для пошуку: ").strip()
            if sport:
                res = find_by_sport(records, sport)
                print_results(res, f"Результати за видом спорту '{sport}'")
            else:
                print("\nЗапит не може бути порожнім.")

        elif choice == "4":
            sport = input("Введіть вид спорту (або натисніть Enter для всіх): ").strip()
            try:
                best = get_best_result(records, sport if sport else None)
                print(f"\nНайкращий результат: {best.name} — {best.result:.2f} ({best.sport_type}, {best.category})")
            except SportsError as e:
                print(f"\nПомилка: {e}")

        elif choice == "5":
            sport = input("Введіть вид спорту (або натисніть Enter для всіх): ").strip()
            avg = calculate_average_result(records, sport if sport else None)
            target = f"за видом спорту '{sport}'" if sport else "за всіма видами"
            print(f"\nСередній результат {target}: {avg:.2f}")

        elif choice == "6":
            sport = input("Введіть вид спорту для рейтингу (або Enter для загального): ").strip()
            rating = get_rating(records, sport if sport else None)
            print_results(rating, "Рейтинг спортсменів (за спаданням)")

        elif choice == "0":
            print("Дякуємо за використання системи. До побачення!")
            break
        else:
            print("Некоректна команда. Спробуйте ще раз.")


def main() -> None:
    records = create_demo_data()
    run_menu(records)


if __name__ == "__main__":
    main()