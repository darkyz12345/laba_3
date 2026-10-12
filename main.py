from pathlib import Path

from integration_module.analysis import (
    EXACT_VALUE,
    compare_methods,
    convergence_deterministic,
    convergence_monte_carlo,
    convergence_order,
    create_comparison_table,
    create_convergence_table,
)
from integration_module.plotting import (
    plot_monte_carlo_values,
    plot_monte_carlo_errors,
    plot_deterministic_convergence,
)


A = 0.0
B = 2.0
COMPARISON_N = 100

DETERMINISTIC_N = [
    2, 4, 8, 16, 32, 64, 128, 256, 512, 1024
]

MONTE_CARLO_N = [
    1_000,
    5_000,
    10_000,
    50_000,
    100_000,
    500_000,
    1_000_000,
    2_000_000,
    5_000_000,
    10_000_000,
    50_000_000,
    100_000_000
]


def print_comparison(results, exact_value):
    print("\nСРАВНЕНИЕ МЕТОДОВ")
    print(f"Точное значение: {exact_value:.12f}")
    print("-" * 100)
    print(
        f"{'Метод':<38}"
        f"{'Результат':>22}"
        f"{'Абсолютная погрешность':>28}"
    )
    print("-" * 100)

    for name, data in results.items():
        print(
            f"{name:<38}"
            f"{data['value']:>22.12f}"
            f"{data['error']:>28.6e}"
        )

    print("-" * 100)


def print_convergence_orders(results):
    print("\nЭКСПЕРИМЕНТАЛЬНЫЙ ПОРЯДОК СХОДИМОСТИ")
    print("-" * 90)

    for name, data in results.items():
        orders = convergence_order(data["errors"], data["n"])
        valid_orders = [
            order for order in orders
            if order == order and abs(order) != float("inf")
        ]

        print(f"\n{name}")

        for i, order in enumerate(orders):
            if order == order and abs(order) != float("inf"):
                print(
                    f"n = {data['n'][i]:>4} -> "
                    f"n = {data['n'][i + 1]:>4}: "
                    f"p = {order:.4f}"
                )
            else:
                print(
                    f"n = {data['n'][i]:>4} -> "
                    f"n = {data['n'][i + 1]:>4}: "
                    f"p не определён"
                )

        if valid_orders:
            print(
                "Средний экспериментальный порядок: "
                f"{sum(valid_orders) / len(valid_orders):.4f}"
            )


def main():
    images_dir = Path(__file__).resolve().parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    comparison_results = compare_methods(
        A,
        B,
        COMPARISON_N,
        EXACT_VALUE,
    )

    deterministic_results = convergence_deterministic(
        A,
        B,
        DETERMINISTIC_N,
        EXACT_VALUE,
    )

    monte_carlo_results = convergence_monte_carlo(
        A,
        B,
        MONTE_CARLO_N,
        EXACT_VALUE,
    )

    print_comparison(comparison_results, EXACT_VALUE)
    print_convergence_orders(deterministic_results)

    create_comparison_table(
        comparison_results,
        EXACT_VALUE,
        filename=str(images_dir / "comparison_table.png"),
    )

    create_convergence_table(
        deterministic_results,
        filename=str(images_dir / "deterministic_convergence_table.png"),
    )

    create_convergence_table(
        monte_carlo_results,
        filename=str(images_dir / "monte_carlo_convergence_table.png"),
        monte_carlo=True,
    )

    plot_monte_carlo_values(
        monte_carlo_results,
        exact_value=EXACT_VALUE,
    )

    plot_monte_carlo_errors(monte_carlo_results)

    plot_deterministic_convergence(deterministic_results)

    print("\nВсе вычисления завершены.")
    print(f"Таблицы и графики сохранены в: {images_dir}")


if __name__ == "__main__":
    main()