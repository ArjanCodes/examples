from sympy import Eq, solve, symbols


def main():
    x = symbols("x")
    equation = Eq(x**2 + 2 * x - 8, 0)

    # Solve the equation
    solutions = solve(equation, x)
    print(solutions)


if __name__ == "__main__":
    main()
