import matplotlib.pyplot as plt

from integration_module.analysis import EXACT_VALUE



def plot_monte_carlo_values(results, exact_value=EXACT_VALUE):
    n_values = list(results.keys())
    values = [results[n]["value"] for n in n_values]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(n_values, values, marker="o", label="Monte Carlo")
    ax.axhline(exact_value, linestyle="--", label="Точное значение")

    ax.set_xscale("log")
    ax.set_xlabel("Количество испытаний N")
    ax.set_ylabel("Значение интеграла")
    ax.set_title("Сходимость метода Монте-Карло")
    ax.grid(True, which="both", linestyle=":")
    ax.legend()

    fig.tight_layout()
    fig.savefig("images/monte_carlo_values.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_monte_carlo_errors(results):
    n_values = list(results.keys())
    errors = [results[n]["error"] for n in n_values]

    points = [
        (n, error)
        for n, error in zip(n_values, errors)
        if error > 0
    ]

    if not points:
        raise ValueError(
            "Нет положительных погрешностей для логарифмического графика"
        )

    n_plot, errors_plot = zip(*points)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.loglog(n_plot, errors_plot, marker="o", label="Абсолютная погрешность")

    reference = [
        errors_plot[0] * (n / n_plot[0]) ** (-0.5)
        for n in n_plot
    ]

    ax.loglog(
        n_plot,
        reference,
        linestyle="--",
        label=r"Ориентир $N^{-1/2}$",
    )

    ax.set_xlabel("Количество испытаний N")
    ax.set_ylabel("Абсолютная погрешность")
    ax.set_title("Погрешность метода Монте-Карло")
    ax.grid(True, which="both", linestyle=":")
    ax.legend()

    fig.tight_layout()
    fig.savefig("images/monte_carlo_errors.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_deterministic_convergence(results):
    fig, ax = plt.subplots(figsize=(10, 6))

    for name, data in results.items():
        points = [
            (n, error)
            for n, error in zip(data["n"], data["errors"])
            if n > 0 and error > 0
        ]

        if not points:
            continue

        n_values, errors = zip(*points)

        ax.loglog(n_values, errors, marker="o", label=name)

    ax.set_xlabel("Число разбиений n")
    ax.set_ylabel("Абсолютная погрешность")
    ax.set_title("Сходимость детерминированных методов")
    ax.grid(True, which="both", linestyle=":")
    ax.legend()

    fig.tight_layout()
    fig.savefig("images/deterministic_convergence.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
