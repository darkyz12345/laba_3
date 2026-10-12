from integration_module import *
import math
import matplotlib.pyplot as plt


EXACT_VALUE = 1 - math.exp(-2)


def absolute_error(value, exact_value):
    return abs(value - exact_value)


DETERMINISTIC_METHODS = {
    "Метод левых прямоугольников": left_rectangle,
    "Метод правых прямоугольников": right_rectangle,
    "Метод средних прямоугольников": middle_rectangle,
    "Метод трапеций": trapezoid,
    "Метод Симпсона": simpson,
}


def compare_methods(a, b, n, exact_value):
    results = {}

    for name, method in DETERMINISTIC_METHODS.items():
        value = method(a, b, n)

        results[name] = {
            "value": value,
            "error": absolute_error(value, exact_value),
        }

    return results


def convergence_deterministic(a, b, n_values, exact_value):
    n_values = list(n_values)
    results = {}

    for name, method in DETERMINISTIC_METHODS.items():
        values = []
        errors = []

        for n in n_values:
            value = method(a, b, n)

            values.append(value)
            errors.append(absolute_error(value, exact_value))

        results[name] = {
            "n": n_values,
            "values": values,
            "errors": errors,
        }

    return results


def convergence_monte_carlo(a, b, n_values, exact_value):
    results = {}

    for n in n_values:
        value = monte_carlo(a, b, n)

        results[n] = {
            "value": value,
            "error": absolute_error(value, exact_value),
        }

    return results

def convergence_order(errors, n_values):
    if len(errors) != len(n_values):
        raise ValueError("Количество погрешностей и значений n не совпадает")
    orders = []
    for i in range(len(errors) - 1):
        e_c = errors[i]
        e_n = errors[i + 1]
        n_c = n_values[i]
        n_n = n_values[i + 1]
        if e_c <= 0 or e_n <= 0 or n_c <= 0 or n_n <= n_c:
            orders.append(float('nan'))
            continue
        p = math.log(e_c / e_n) / math.log(n_n / n_c)
        orders.append(p)
    return orders

def create_comparison_table(results, exact_value, filename='images/comparison_table.png'):
    rows = []
    for name, data in results.items():
        rows.append([
            name,
            f"{data['value']:.10f}",
            f"{data['error']:.6e}",
        ])
    fig, ax = plt.subplots(figsize=(11, 3 + 0.45 * len(rows)))
    ax.axis('off')
    table = ax.table(
        cellText=rows,
        colLabels=[
            'Метод',
            'Значение интеграла',
            'Абсолютная погрешность'
        ],
        cellLoc="center",
        loc="center",
        colWidths=[0.42, 0.27, 0.31]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.6)
    ax.set_title(f"Сравнение методов\nТочное значение: {exact_value:.10f}", pad=20)
    fig.tight_layout()
    fig.savefig(filename, dpi=500, bbox_inches="tight")
    plt.close(fig)


def create_convergence_table(results, filename="images/convergence_table.png", monte_carlo=False):
    rows = []

    if monte_carlo:
        for n, data in results.items():
            rows.append([
                f"{n:,}".replace(",", " "),
                f"{data['value']:.10f}",
                f"{data['error']:.6e}",
            ])

        title = "Сходимость метода Монте-Карло"
        headers = [
            "Количество испытаний N",
            "Значение интеграла",
            "Абсолютная погрешность",
        ]

    else:
        for name, data in results.items():
            for n, value, error in zip(
                data["n"],
                data["values"],
                data["errors"],
            ):
                rows.append([
                    name,
                    str(n),
                    f"{value:.10f}",
                    f"{error:.6e}",
                ])

        title = "Исследование сходимости детерминированных методов"
        headers = [
            "Метод",
            "Число разбиений n",
            "Значение интеграла",
            "Абсолютная погрешность",
        ]

    height = max(3, 0.35 * len(rows) + 1.5)

    fig, ax = plt.subplots(figsize=(13, height))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=headers,
        cellLoc="center",
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.4)

    ax.set_title(title, pad=18)

    fig.tight_layout()
    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
