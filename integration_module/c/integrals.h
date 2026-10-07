#ifndef INTEGRALS_H
#define INTEGRALS_H

double func(double x);

double left_rectangle_integral(double a, double b, double (*funct)(double), int n);

double right_rectangle_integral(double a, double b, double (*funct)(double), int n);

double middle_rectangle_integral(double a, double b, double (*funct)(double), int n);

double trapezoid_integral(double a, double b, double (*funct)(double), int n);

double simpson_integral(double a, double b, double (*funct)(double), int n, int *code);

double monte_carlo_integrals(double a, double b, double (*funct)(double), long long int n);

void initialize_random(void);

#endif