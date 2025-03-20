from fastapi import APIRouter
from pydantic import BaseModel
from sympy import symbols, sqrt, latex

# Crear un router
router = APIRouter()

# Definir la variable simbólica
x_sym = symbols('x')

# Definir el modelo de solicitud
class RectangleRequest(BaseModel):
    r: float  # Radio del círculo
    point: tuple[float, float]  # Punto (x, y) para verificar

# Definir el endpoint
@router.post("/area")
async def area(request: RectangleRequest):
    r = request.r
    x_point, y_point = request.point

    # Verificar si x está dentro del dominio [0, 2r]
    if 0 <= x_point <= 2 * r:
        # Verificar si el punto está dentro del círculo completo
        if x_point**2 + y_point**2 <= (2 * r)**2:
            # Verificar si el punto está dentro del semicírculo (y <= sqrt(4r^2 - x^2))
            if y_point <= sqrt(4 * r**2 - x_point**2):
                area_rectangle = 2 * r**2  # Área del rectángulo más grande
                area_from_point = x_point * y_point  # Área desde el punto

                # Calcular el punto óptimo (esquina del rectángulo)
                sqrt_2 = sqrt(2)  # Raíz cuadrada de 2
                x = float((sqrt_2 * r).evalf())  # Convertir a float
                y = float((sqrt_2 * r).evalf())

                # Función de la semicircunferencia en formato LaTeX
                function_expr = sqrt(4 * r**2 - x_sym**2)
                function_latex = latex(function_expr)

                # Retornar directamente los valores
                return {
                    "points": [x, y],  # Punto óptimo en formato numérico
                    "function": f"y = {function_latex}",  # Función en LaTeX
                    "axis_limits": {
                        "x": f"[0, {round(2 * r, 4)}]",
                        "y": f"[0, {round(2 * r, 4)}]",
                    },
                    "rectangle_area": round(area_rectangle, 4),
                    "area_from_point": round(area_from_point, 4),
                    "is_point_inside": True,
                }
            else:
                # El punto está dentro del círculo pero fuera del semicírculo
                return {
                    "error": "El punto está dentro del círculo pero fuera del semicírculo.",
                    "is_point_inside": False,
                }
        else:
            # El punto está fuera del círculo
            return {
                "error": "El punto está fuera del círculo.",
                "is_point_inside": False,
            }
    else:
        # El punto está fuera del dominio de x
        return {
            "error": f"El valor de x = {x_point} está fuera del dominio [0, {2 * r}].",
            "is_point_inside": False,
        }