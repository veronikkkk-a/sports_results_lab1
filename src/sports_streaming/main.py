import time
import random
import tracemalloc
from pathlib import Path
from itertools import islice, pairwise
from sports_streaming.pipeline import build_pipeline
from sports_streaming.analytics import (
    streaming_average_result,
    find_best_result,
    streaming_min_max
)
from sports_streaming.batches import batched_records

def generate_test_file(path: Path, count: int) -> None:
    """Генерація тестового CSV файлу з великою кількістю записів."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sports = ["Біг 100м", "Плавання 50м", "Стрибки у довжину", "Важка атлетика"]
    categories = ["Професіонали", "Дорослі", "Юніори"]
    
    import csv
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["athlete", "sport", "result", "category", "timestamp"])
        for i in range(1, count + 1):
            writer.writerow([
                f"Спортсмен {i}",
                random.choice(sports),
                round(random.uniform(9.5, 120.0), 2),
                random.choice(categories),
                f"2026-10-{random.randint(1, 30):02d} 12:00:00"
            ])

def measure_memory_and_time(func, *args):
    """Вимірювання пікового споживання пам'яті та часу виконання."""
    tracemalloc.start()
    start_time = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, elapsed, peak

def run_benchmarks():
    """Проведення бенчмаркінгу для eager та lazy підходів."""
    data_dir = Path("data")
    sizes = [10_000, 100_000, 500_000]
    
    print("\n" + "="*80)
    print("ЕКСПЕРИМЕНТАЛЬНА ЧАСТИНА (BENCHMARK: EAGER VS LAZY)")
    print("="*80)
    print(f"{'Records':<10} | {'Eager Time (s)':<15} | {'Lazy Time (s)':<15} | {'Eager Peak (MB)':<16} | {'Lazy Peak (MB)':<16}")
    print("-" * 80)
    
    for size in sizes:
        file_path = data_dir / f"sports_{size}.csv"
        if not file_path.exists():
            generate_test_file(file_path, size)
            
        def eager_run(path):
            with path.open("r", encoding="utf-8") as f:
                import csv
                rows = list(csv.DictReader(f))
            processed = [r for r in rows if float(r.get("result", 0)) > 0]
            return len(processed)
            
        _, eager_time, eager_peak = measure_memory_and_time(eager_run, file_path)
        
        def lazy_run(path):
            pipeline = build_pipeline(path)
            return sum(1 for _ in pipeline)
            
        _, lazy_time, lazy_peak = measure_memory_and_time(lazy_run, file_path)
        
        print(f"{size:<10} | {eager_time:<15.4f} | {lazy_time:<15.4f} | {eager_peak / 1024**2:<16.2f} | {lazy_peak / 1024**2:<16.2f}")
    print("="*80)

def main():
    data_path = Path("data/sports_100k.csv")
    if not data_path.exists():
        print("Генерація тестового файлу на 100 000 записів...")
        generate_test_file(data_path, 100_000)
        
    print("=== АНАЛІЗ СИСТЕМИ ОБЛІКУ СПОРТИВНИХ РЕЗУЛЬТАТІВ (ЛАБОРАТОРНА РОБОТА №3) ===")
    
    pipeline = build_pipeline(data_path)
    first_5 = list(islice(pipeline, 5))
    print("\n1. Перші 5 спортивних результатів (із використанням islice):")
    for r in first_5:
        print(f"   - {r.athlete} | {r.sport} | Результат: {r.result} | Категорія: {r.category}")
        
    avg = streaming_average_result(build_pipeline(data_path))
    min_res, max_res = streaming_min_max(build_pipeline(data_path))
    best = find_best_result(build_pipeline(data_path))
    
    print(f"\n2. Потокова агрегація даних:")
    print(f"   - Загальний середній результат: {avg:.2f}")
    print(f"   - Мінімальний результат: {min_res}")
    print(f"   - Максимальний результат: {max_res}")
    if best:
        print(f"   - Найкращий результат: {best.athlete} ({best.sport}) з показником {best.result}")
        
    results_sample = [r.result for r in islice(build_pipeline(data_path, sport="Біг 100м"), 5)]
    print("\n3. Pairwise аналіз зміни послідовних результатів (Біг 100м):")
    for prev, curr in pairwise(results_sample):
        diff = round(curr - prev, 2)
        print(f"   - Перехід від {prev} до {curr}: різниця = {diff:+f}")
        
    print("\n4. Приклад Batch Processing (перші 2 батчі по 3 записи):")
    for b_idx, batch in enumerate(batched_records(build_pipeline(data_path), 3), 1):
        if b_idx > 2:
            break
        print(f"   - Батч #{b_idx} (містить записів: {len(batch)})")
        for rec in batch:
            print(f"     * {rec.athlete} ({rec.sport}) -> {rec.result}")
            
    run_benchmarks()

if __name__ == "__main__":
    main()