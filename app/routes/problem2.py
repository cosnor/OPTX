from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix, dok_matrix
import time

router = APIRouter()

class MatrixRequest(BaseModel):
    matrix: list[list[float]]  # Matriz enviada desde el frontend
    method: str  # "LIL", "DOK" o "CSR"
    operation: str  # "multiply" o "add"

class MatrixRequest2(BaseModel):
    matrix: list[list[float]]  # Matriz enviada desde el frontend
    operation: str  # "multiply" o "add"

class CSRMatrix:
    def __init__(self, matrix):
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
        self.data = []
        self.indices = []
        self.indptr = [0]
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix[i][j] != 0:
                    self.data.append(matrix[i][j])
                    self.indices.append(j)
            self.indptr.append(len(self.data))

    def to_dense(self):
        dense = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.indptr[i], self.indptr[i+1]):
                dense[i][self.indices[j]] = self.data[j]
        return dense

# ✅ Funciones de operaciones
def matrix_multiply(matrix1, matrix2):
    return np.dot(matrix1, matrix2)

def matrix_add(matrix1, matrix2):
    return matrix1 + matrix2

@router.post("/matrix")
async def process_matrix(request: MatrixRequest):
    method = request.method.upper()
    operation = request.operation.lower()
    matrix = request.matrix  # Recibimos la matriz desde el frontend

    # Convertimos la matriz a formato CSR
    csr_matrix_custom = CSRMatrix(matrix)

    # Medimos el tiempo de ejecución de la implementación propia
    start_time = time.perf_counter()
    if operation == "multiply":
        result = matrix_multiply(csr_matrix_custom.to_dense(), csr_matrix_custom.to_dense())
    elif operation == "add":
        result = matrix_add(csr_matrix_custom.to_dense(), csr_matrix_custom.to_dense())
    else:
        return {"error": "Operación no válida"}
    end_time = time.perf_counter()
    custom_time = end_time - start_time

    # Medimos el tiempo de ejecución con scipy.sparse
    start_time = time.perf_counter()
    if method == "LIL":
        scipy_matrix = lil_matrix(matrix)
    elif method == "DOK":
        scipy_matrix = dok_matrix(matrix)
    elif method == "CSR":
        scipy_matrix = csr_matrix(matrix)
    else:
        return {"error": "Método no válido"}

    if operation == "multiply":
        result_scipy = scipy_matrix.dot(scipy_matrix).toarray()
    elif operation == "add":
        result_scipy = (scipy_matrix + scipy_matrix).toarray()
    end_time = time.perf_counter()
    scipy_time = end_time - start_time

    return {
        "custom_implementation_time": round(custom_time, 6),
        "scipy_time": round(scipy_time, 6)
    }

@router.post("/matrix/comparison")
async def compare_matrix_operations(request: MatrixRequest2):
    operation = request.operation.lower()
    matrix = np.array(request.matrix)

    # Implementación con CSRMatrix
    csr_matrix_custom = CSRMatrix(matrix.tolist())
    start_time = time.perf_counter()
    if operation == "multiply":
        result_custom = matrix_multiply(csr_matrix_custom.to_dense(), csr_matrix_custom.to_dense())
    elif operation == "add":
        result_custom = matrix_add(csr_matrix_custom.to_dense(), csr_matrix_custom.to_dense())
    else:
        return {"error": "Operación no válida"}
    end_time = time.perf_counter()
    custom_time = end_time - start_time

    # Implementación con matrices densas normales
    start_time = time.perf_counter()
    if operation == "multiply":
        result_dense = matrix_multiply(matrix, matrix)
    elif operation == "add":
        result_dense = matrix_add(matrix, matrix)
    end_time = time.perf_counter()
    dense_time = end_time - start_time

    return {
        "custom_sparse_time": round(custom_time, 6),
        "dense_matrix_time": round(dense_time, 6)
    }