# OPTX

## Get Started

### 1. Ejecución Backend

Instalar todas las dependencias
pip install -r requirements.txt

Comando para inicializar proyecto
uvicorn app.main:app --reload

### 2. Ejecución Frontend

Se puede utilizar la extensión live server o en su defecto, acceder al "http://127.0.0.1:5500".

## Sobre OPTX

OPTX es una solución diseñada por Bella Mejía, María Camila Osorno, Alberto Sandoval y Yovany Zhu.

OPTX cuenta con varios módulos, cada módulo que representa un punto del laboratario de optimización. 

### Enigma

Enigma responde al punto 1

Escoge un problema de optimización de dos variables (o puedes crear uno también). Plantea su función de costo y las restricciones. Grafica la región factible con ayuda de Python. 
Desarrolla un programa que le permita al usuario:
a.	tener el valor de la función de costo a partir de un punto (x,y) 
b.	ver gráficamente cómo cambia la región factible ante un cambio en las restricciones.

El inciso a se puede conocer oprimiendo el punto resultante y el inciso b se observa en la gráfica.

### Lacuna

Lacuna responde al punto 2

Selecciona un método de representación de matrices sparse e impleméntalo en Python desde cero. Compara tus resultados con la función de las librerías de Python. La comparación debe incluir el tiempo de ejecución para una matriz sparse con los 2 métodos (propio vs Python) y el tiempo de ejecución de una operación con la matriz densa. Para la interfaz el usuario debe poder escoger entre 3 métodos de representación de matrices sparse (pueden ser librerías de Python), realizar al menos dos operaciones con matrices y visualizar el tiempo de ejecución.

El experimento se puede observar al final de la página, mientras que la comparación entre métodos de representación se encuentran en la parte superior.

### Replica

Replica responde al punto 3

Crea un programa para implementar la expansión en series de Taylor. El usuario debe ingresar la cantidad de términos de la expansión, el punto de expansión y la función a representar (debe tener al menos 5 funciones diferentes para escoger). Se debe mostrar en una gráfica la función original y la aproximación. 

### Eureka

Eureka responde al punto 4

Escoge 3 algoritmos de optimización sin restricciones. El usuario debe poder realizar cambios sobre sus parámetros y sobre el punto inicial. ¿Cómo afectan estos cambios los resultados? ¿Cómo afecta el tiempo de convergencia o cantidad de iteraciones? 






 
