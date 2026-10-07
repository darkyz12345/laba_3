#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>


double func(double x)
{
    return exp(-1.0 * x);
}


double left_rectangle_integral(double a, double b, double (*funct)(double), int n)
{
    double h = (b - a) / n;
    double x = a;
    double res = 0;
    for (int i = 0; i < n; ++i)
    {
        res += funct(x);
        x += h;
    }
    return res * h;
}

double right_rectangle_integral(double a, double b, double (*funct)(double), int n)
{
    double h = (b - a) / n;
    double x = a + h;
    double res = 0;
    for (int i = 0; i < n; ++i)
    {
        res += funct(x);
        x += h;
    }
    return res * h;
}

double middle_rectangle_integral(double a, double b, double (*funct)(double), int n)
{
    double h = (b - a) / n;
    double res = 0.0;
    for (int i = 0; i < n; ++i)
    {
        double x = a + (i + 0.5) * h;
        res += funct(x);
    }
    return res * h;
}

double trapezoid_integral(double a, double b, double (*funct)(double), int n)
{
    double h = (b - a) / n;
    double res = (funct(a) + funct(b)) / 2;
    for (int i = 1; i < n; ++i)
    {
        res += funct(a + i * h);
    }
    return res * h;
}

double simpson_integral(double a, double b, double (*funct)(double), int n, int *code)
{
    if (n % 2)
    {
        *code = 1;
        return 0;
    }
    double h = (b - a) / n;
    double res = (funct(b) + funct(a));
    for (int i = 1; i < n; ++i)
    {
        double x = a + i * h;
        if (i % 2)
        {
            res += 4 * funct(x);
        }
        else
        {
            res += 2 * funct(x);
        }
    }
    return res * h / 3;
}

double monte_carlo_integrals(double a, double b, double (*funct)(double), long long int n)
{
    double res = 0;
    for (long long int i = 0; i < n; ++i)
    {
        double rand_val = (double)rand() / RAND_MAX;
        double x = a + rand_val * (b - a);
        res += funct(x);
    }
    return (b - a) * res / n;
}

void initialize_random(void)
{
    srand((unsigned)time(NULL));
}