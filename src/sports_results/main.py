import time
from sports_results.data import athletes_data
from sports_results.processors import (
    get_unique_sports,
    create_athlete_index,
    group_by_sport,
    count_athletes_by_sport,
    track_recent_results
)
from sports_results.analytics import (
    calculate_average_result,
    find_best_athlete,
    build_rating,
    calculate_multi_average,
    create_athlete_record,
    create_result_filter
)

def run_benchmark():
    """Експериментальна частина: порівняння часу лінійного пошуку в list vs пошуку за dict-index."""
    print("\n" + "=" * 50)
    print("ЕКСПЕРИМЕНТАЛЬНА ЧАСТИНА (BENCHMARK)")
    print("=" * 50)
    
    sizes = [1000, 10000, 100000]
    for size in sizes:
        # 1. Генерація тестового набору
        big_data = [{"id": i, "name": f"Athlete_{i}", "sport_type": "Run", "result": 10.0 + (i % 100)} for i in range(size)]
        target_id = size - 1  # Пошук останнього елемента (найгірший випадок для лінійного пошуку)

        # 2. Лінійний пошук у list O(n)
        start = time.perf_counter()
        _ = next((item for item in big_data if item["id"] == target_id), None)
        list_time = time.perf_counter() - start

        # 3. Пошук у dict O(1)
        index = {item["id"]: item for item in big_data}
        start = time.perf_counter()
        _ = index.get(target_id)
        dict_time = time.perf_counter() - start

        print(f"Записи: {size:6d} | List Search O(n): {list_time:.8f} s | Dict Search O(1): {dict_time:.8f} s")

def main() -> None:
    print("=== АНАЛІЗ СИСТЕМИ ОБЛІКУ СПОРТИВНИХ РЕЗУЛЬТАТІВ ===")
    
    # 1. Множина унікальних видів спорту (Set Comprehension)
    sports = get_unique_sports(athletes_data)
    print(f"\n1. Унікальні види спорту (set): {sports}")
    
    # 2. Dict Index (Dict Comprehension)
    idx = create_athlete_index(athletes_data)
    print(f"2. Пошук за ID=3 (dict-index O(1)): {idx.get(3)}")
    
    # 3. Обчислення середнього (Decorators & Generator Expressions)
    avg_res = calculate_average_result(athletes_data)
    print(f"3. Загальний середній результат: {avg_res:.2f}")
    
    # 4. Найкращий результат (Lambda)
    best = find_best_athlete(athletes_data)
    if best:
        print(f"4. Найкращий спортсмен (lambda): {best['name']} з результатом {best['result']}")
        
    # 5. Сортування та рейтинг
    rating = build_rating(athletes_data)
    print("\n5. Рейтинг спортсменів (sorted):")
    for rank, item in enumerate(rating, 1):
        print(f"   {rank}. {item['name']} ({item['sport_type']}) — {item['result']}")
        
    # 6. Collections: Counter & defaultdict
    counts = count_athletes_by_sport(athletes_data)
    print(f"\n6. Кількість спортсменів за видами (Counter): {dict(counts)}")
    
    grouped = group_by_sport(athletes_data)
    print(f"   Групування (defaultdict): {list(grouped.keys())}")
    
    # 7. Closure (Замикання)
    filter_above_20 = create_result_filter(20.0)
    high_results = [r for r in athletes_data if filter_above_20(r)]
    print(f"\n7. Фільтрація >= 20.0 (Closure): {[r['name'] for r in high_results]}")
    
    # 8. Аргументи *args та **kwargs
    demo_args = calculate_multi_average(10.5, 11.2, 10.8)
    print(f"\n8. Середне через *args: {demo_args:.2f}")
    
    new_record = create_athlete_record(id=7, name="Василь Ломаченко", sport_type="Бокс", result=95.0, category="Професіонали")
    print(f"   Запис створено через **kwargs: {new_record}")

    # 9. Запуск бенчмаркінгу
    run_benchmark()

if __name__ == "__main__":
    main()