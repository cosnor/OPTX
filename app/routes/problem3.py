from fastapi import APIRouter
from pydantic import BaseModel
from sympy import symbols, exp, sin, cos, log, factorial, diff, latex

router = APIRouter()

class TaylorRequest(BaseModel):
    n_terms: int  # Número de términos de la serie de Taylor
    a: float  # Punto a evaluar
    function: int  # Función a aproximar

# Definimos la variable simbólica
x = symbols('x')

# Diccionario de funciones simbólicas disponibles
functions = {
    1: ("e^x", exp(x)),
    2: ("sin(x)", sin(x)),
    3: ("cos(x)", cos(x)),
    4: ("ln(1 + x)", log(1 + x)),
    5: ("1 / (1 - x)", 1 / (1 - x)),
}

# Función para calcular la serie de Taylor
def taylor_series(func_expr, a, n_terms):
    taylor_approx = 0
    for n in range(n_terms):
        derivative = diff(func_expr, x, n).subs(x, a)  # Derivada en x = a
        taylor_approx += derivative * (x - a)**n / factorial(n)  # Término de la serie
    return taylor_approx

@router.post("/taylor")
async def taylor_series_approximation(request: TaylorRequest):
    n_terms = request.n_terms
    a = request.a
    function = request.function

    if function not in functions:
        return {"error": "Función no válida. Las opciones son: 1 (e^x), 2 (sin(x)), 3 (cos(x)), 4 (ln(1 + x)), 5 (1 / (1 - x))"}

    func_name, func_expr = functions[function]
    taylor_poly = taylor_series(func_expr, a, n_terms)  # Calcula el polinomio de Taylor
    latex_taylor = latex(taylor_poly, mode='plain')  # Polinomio de Taylor en formato LaTeX sin left/right
    latex_function = latex(func_expr)  # Función original
    latex_taylor = latex_taylor.replace(r"\left", "").replace(r"\right", "")
    latex_function = latex_function.replace(r"\left", "").replace(r"\right", "")

    return {
        "function": f"${latex_function}",
        "latex": f"${latex_taylor}$"  # Formato LaTeX
    }
