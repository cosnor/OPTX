import numpy as np
import time
import sympy as sp
import math
from sympy.parsing.sympy_parser import parse_expr
from sympy import diff
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Union

router = APIRouter()

class NewtonRequest(BaseModel):
    function: str  # Función a optimizar
    initial_point: float  # Punto inicial
    tolerance: float = 1e-6  # Tolerancia para la convergencia
    max_iterations: int = 100  # Número máximo de iteraciones

class NewtonResponse(BaseModel):
    function_string: str
    iteration_points: List[float]  # Puntos iterados
    convergence_data: Dict[str, List[float]]  # Datos de convergencia
    result: Dict[str, Any]  # Resultado final

class GradientDescentRequest(BaseModel):
    function: str
    initial_point: float
    learning_rate: float = 0.01
    tolerance: float = 1e-6
    max_iterations: int = 1000

class GradientDescentResponse(BaseModel):
    function_string: str
    convergence_data: Dict[str, List[float]]
    result: Dict[str, Any]

class SARequest(BaseModel):
    function: str
    initial_point: float = 0.0  # Punto inicial proporcionado por el usuario
    initial_temperature: float = 1000.0  # Temperatura inicial
    cooling_rate: float = 0.95  # Tasa de enfriamiento
    max_iterations: int = 1000  # Número máximo de iteraciones
    tolerance: float = 1e-6  # Tolerancia para la convergencia

class SAResponse(BaseModel):
    function_string: str
    convergence_data: Dict[str, List[float]]
    result: Dict[str, Any]

# Nueva función para verificar la naturaleza del punto crítico mediante el criterio de la segunda derivada
def check_critical_point(f_prime_val, f_double_prime_val):
    # Verificar si es un punto crítico y su naturaleza
    # Tolerancia para considerar un valor como cero
    tol = 1e-10
    
    # Si la primera derivada no es cercana a cero, no es un punto crítico
    if abs(f_prime_val) > tol:
        return {
            "type": "not_critical", 
            "description": "No es un punto crítico (gradiente ≠ 0)",
            "is_minimum": False
        }
    
    # Verificar la segunda derivada (matriz Hessiana en 1D)
    if f_double_prime_val > tol:
        return {
            "type": "minimum", 
            "description": "Mínimo local (f''(x) > 0, Hessiana definida positiva)",
            "is_minimum": True
        }
    elif f_double_prime_val < -tol:
        return {
            "type": "maximum", 
            "description": "Máximo local (f''(x) < 0, Hessiana definida negativa)",
            "is_minimum": False
        }
    else:
        return {
            "type": "saddle_or_inflection", 
            "description": "Punto de silla o inflexión (f''(x) ≈ 0, Hessiana indefinida)",
            "is_minimum": False
        }

# Función para manejar valores infinitos en JSON
def safe_float(value):
    """Convierte valores float a valores seguros para JSON"""
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        return [safe_float(v) for v in value]
    
    try:
        float_val = float(value)
        if math.isnan(float_val):
            return "NaN"
        if math.isinf(float_val):
            return 1e308 if float_val > 0 else -1e308
        return float_val
    except:
        return str(value)

@router.post("/newton", response_model=NewtonResponse)
def newton_method_optimization(request: NewtonRequest):
    try:
        # Obtener parámetros del request
        func_str = request.function
        x0 = request.initial_point
        tol = request.tolerance
        max_iter = request.max_iterations
        
        # Configurar cálculo simbólico
        x = sp.symbols('x')
        
        try:
            # Convertir a expresión de sympy
            func = parse_expr(func_str)
            
            # Verificar que la función es válida evaluándola en un punto
            test_value = float(func.subs(x, 1.0))
            
            # Calcular la primera y segunda derivada
            func_prime = diff(func, x)
            func_double_prime = diff(func_prime, x)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al parsear la función: {str(e)}")
        
        # Ejecutar el método de Newton
        start_time = time.time()
        
        x_values = [x0]
        f_values = [float(func.subs(x, x0))]
        
        # Función para convertir expresiones simbólicas a funciones numéricas
        f = lambda val: float(func.subs(x, val))
        f_prime = lambda val: float(func_prime.subs(x, val))
        f_double_prime = lambda val: float(func_double_prime.subs(x, val))
        
        x_current = x0
        converged = False
        error_message = None
        
        for i in range(max_iter):
            # Verificar que la segunda derivada no sea cero para evitar división por cero
            f_double_prime_val = f_double_prime(x_current)
            
            if abs(f_double_prime_val) < 1e-10:
                error_message = f"Segunda derivada cercana a cero en x = {x_current}. El método de Newton puede no ser adecuado para este punto o función."
                break
            
            # Calcular el siguiente valor usando la fórmula de Newton para minimización:
            # x_{n+1} = x_n - f'(x_n) / f''(x_n)
            x_next = x_current - f_prime(x_current) / f_double_prime_val
            
            # Guardar los valores
            x_values.append(x_next)
            f_values.append(f(x_next))
            
            # Verificar convergencia
            if abs(x_next - x_current) < tol:
                converged = True
                break
                
            x_current = x_next
        
        end_time = time.time()
        execution_time = end_time - start_time
        iterations_used = len(x_values) - 1  # Restar 1 porque incluimos el punto inicial
        
        # Verificar la naturaleza del punto crítico encontrado
        final_f_prime_val = f_prime(x_values[-1])
        final_f_double_prime_val = f_double_prime(x_values[-1])
        critical_point_info = check_critical_point(final_f_prime_val, final_f_double_prime_val)
        
        # Crear datos para la respuesta
        result = {
            "converged": converged,
            "iterations": iterations_used,
            "minimum_x": safe_float(x_values[-1]),
            "minimum_f": safe_float(f_values[-1]),
            "execution_time": execution_time,
            "error_message": error_message,
            "critical_point_type": critical_point_info["type"],
            "critical_point_description": critical_point_info["description"],
            "is_minimum": critical_point_info["is_minimum"],
            "first_derivative": safe_float(final_f_prime_val),
            "second_derivative": safe_float(final_f_double_prime_val)
        }
        
        # Crear datos de convergencia
        convergence_data = {
            "f_values": f_values
        }
        
        # Combinar los datos en un solo objeto de respuesta
        response = {
            "function_string": func_str,
            "iteration_points": x_values,
            "convergence_data": convergence_data,
            "result": result
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el cálculo: {str(e)}")
    
@router.post("/gradient", response_model=GradientDescentResponse)
def gradient_descent_optimization(request: GradientDescentRequest):
    try:
        # Obtener parámetros del request
        func_str = request.function
        x0 = request.initial_point
        learning_rate = request.learning_rate
        tol = request.tolerance
        max_iter = request.max_iterations
        
        # Configurar cálculo simbólico
        x = sp.symbols('x')
        
        try:
            # Convertir a expresión de sympy
            func = parse_expr(func_str)
            
            # Verificar que la función es válida evaluándola en un punto
            test_value = float(func.subs(x, 1.0))
            
            # Calcular la primera derivada (gradiente)
            func_prime = diff(func, x)
            
            # Calcular la segunda derivada (Hessiana) para análisis del punto crítico
            func_double_prime = diff(func_prime, x)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al parsear la función: {str(e)}")
        
        # Ejecutar el método de Gradiente Descendiente
        start_time = time.time()
        
        x_values = [x0]
        f_values = [float(func.subs(x, x0))]
        gradient_values = [float(func_prime.subs(x, x0))]
        
        # Función para convertir expresiones simbólicas a funciones numéricas
        f = lambda val: float(func.subs(x, val))
        f_prime = lambda val: float(func_prime.subs(x, val))
        f_double_prime = lambda val: float(func_double_prime.subs(x, val))
        
        x_current = x0
        converged = False
        error_message = None
        
        for i in range(max_iter):
            try:
                # Calcular el gradiente en el punto actual
                grad = f_prime(x_current)
                
                # Limitar el tamaño del gradiente para evitar pasos demasiado grandes
                max_step = 10.0  # valor máximo de paso
                step_size = learning_rate * grad
                if abs(step_size) > max_step:
                    step_size = max_step * (1 if step_size > 0 else -1)
                
                # Actualizar el punto usando la regla de gradiente descendiente limitada
                x_next = x_current - step_size
                
                # Guardar los valores (asegurándose de que sean seguros para JSON)
                x_values.append(safe_float(x_next))
                f_val = f(x_next)
                f_values.append(safe_float(f_val))
                gradient_values.append(safe_float(f_prime(x_next)))
                
                # Verificar convergencia
                if abs(x_next - x_current) < tol or abs(grad) < tol:
                    converged = True
                    break
                    
                x_current = x_next
                
                # Decay del learning rate cada 100 iteraciones
                if i > 0 and i % 100 == 0:
                    learning_rate *= 0.9  # Reducir el learning rate un 10%
                    
            except Exception as e:
                error_message = f"Error en la iteración {i}: {str(e)}"
                break
        
        end_time = time.time()
        execution_time = end_time - start_time
        iterations_used = len(x_values) - 1  # Restar 1 porque incluimos el punto inicial
        
        # Verificar la naturaleza del punto crítico encontrado
        try:
            final_f_prime_val = safe_float(f_prime(x_values[-1]))
            final_f_double_prime_val = safe_float(f_double_prime(x_values[-1]))
            critical_point_info = check_critical_point(final_f_prime_val, final_f_double_prime_val)
        except Exception as e:
            critical_point_info = {
                "type": "unknown", 
                "description": f"No se pudo determinar el tipo de punto crítico: {str(e)}",
                "is_minimum": False
            }
            final_f_prime_val = None
            final_f_double_prime_val = None
        
        # Crear datos para la respuesta
        result = {
            "converged": converged,
            "iterations": iterations_used,
            "minimum_x": safe_float(x_values[-1]),
            "minimum_f": safe_float(f_values[-1]),
            "final_gradient": safe_float(gradient_values[-1]),
            "execution_time": execution_time,
            "error_message": error_message,
            "critical_point_type": critical_point_info["type"],
            "critical_point_description": critical_point_info["description"],
            "is_minimum": critical_point_info["is_minimum"],
            "first_derivative": safe_float(final_f_prime_val),
            "second_derivative": safe_float(final_f_double_prime_val)
        }
        
        # Crear datos de convergencia
        convergence_data = {
            "x_values": safe_float(x_values),
            "f_values": safe_float(f_values)
        }
        
        # Combinar los datos en un solo objeto de respuesta
        response = {
            "function_string": func_str,
            "convergence_data": convergence_data,
            "result": result
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el cálculo: {str(e)}")
    
@router.post("/sa", response_model=SAResponse)
def sa_optimization(request: SARequest):
    try:
        # Obtener parámetros del request
        func_str = request.function
        initial_point = request.initial_point
        initial_temperature = request.initial_temperature
        cooling_rate = request.cooling_rate
        max_iter = request.max_iterations
        tol = request.tolerance
        
        # Configurar cálculo simbólico
        x = sp.symbols('x')
        
        try:
            # Convertir a expresión de sympy
            func = parse_expr(func_str)
            
            # Verificar que la función es válida evaluándola en un punto
            test_value = float(func.subs(x, 1.0))
            
            # Calcular la primera y segunda derivada para análisis del punto crítico
            func_prime = diff(func, x)
            func_double_prime = diff(func_prime, x)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al parsear la función: {str(e)}")
        
        # Convertir la función simbólica a una función numérica para evaluación
        f_lambda = sp.lambdify(x, func, "numpy")
        f_prime_lambda = sp.lambdify(x, func_prime, "numpy")
        f_double_prime_lambda = sp.lambdify(x, func_double_prime, "numpy")
        
        # Función objetivo para SA con manejo seguro de valores
        def objective_function(pos):
            try:
                val = f_lambda(pos)
                if math.isnan(val) or math.isinf(val):
                    return 1e100  # Un valor muy grande pero finito
                return val
            except:
                return 1e100  # Un valor muy grande pero finito
        
        # Ejecutar el algoritmo de Recocido Simulado
        start_time = time.time()
        
        # Inicializar variables
        current_position = initial_point  # Usar el punto inicial proporcionado por el usuario
        current_value = objective_function(current_position)
        best_position = current_position
        best_value = current_value
        temperature = initial_temperature
        
        # Historial de convergencia
        positions_history = [current_position]
        values_history = [current_value]
        
        for iteration in range(max_iter):
            # Generar un nuevo candidato aleatorio
            new_position = current_position + np.random.uniform(-1, 1) * temperature
            new_value = objective_function(new_position)
            
            # Calcular la diferencia de energía
            delta = new_value - current_value
            
            # Aceptar el nuevo candidato con probabilidad basada en la temperatura
            if delta < 0 or np.random.rand() < np.exp(-delta / temperature):
                current_position = new_position
                current_value = new_value
                
                # Actualizar el mejor valor encontrado
                if current_value < best_value:
                    best_position = current_position
                    best_value = current_value
            
            # Reducir la temperatura
            temperature *= cooling_rate
            
            # Guardar historial
            positions_history.append(current_position)
            values_history.append(current_value)
            
            # Verificar convergencia
            if temperature < tol:
                break
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verificar la naturaleza del punto crítico encontrado
        try:
            final_f_prime_val = safe_float(f_prime_lambda(best_position))
            final_f_double_prime_val = safe_float(f_double_prime_lambda(best_position))
            critical_point_info = check_critical_point(final_f_prime_val, final_f_double_prime_val)
        except Exception as e:
            critical_point_info = {
                "type": "unknown", 
                "description": f"No se pudo determinar el tipo de punto crítico: {str(e)}",
                "is_minimum": False
            }
            final_f_prime_val = None
            final_f_double_prime_val = None
        
        # Crear datos para la respuesta
        result = {
            "converged": temperature < tol,
            "iterations": iteration + 1,
            "minimum_x": safe_float(best_position),
            "minimum_f": safe_float(best_value),
            "execution_time": execution_time,
            "critical_point_type": critical_point_info["type"],
            "critical_point_description": critical_point_info["description"],
            "is_minimum": critical_point_info["is_minimum"],
            "first_derivative": safe_float(final_f_prime_val),
            "second_derivative": safe_float(final_f_double_prime_val)
        }
        
        # Crear datos de convergencia
        convergence_data = {
            "positions": safe_float(positions_history),
            "values": safe_float(values_history)
        }
        
        # Combinar los datos en un solo objeto de respuesta
        response = {
            "function_string": func_str,
            "convergence_data": convergence_data,
            "result": result
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el cálculo: {str(e)}")