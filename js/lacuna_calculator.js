function generateSparseMatrix(n) {

    let matrix = Array.from({ length: n }, () => Array(n).fill(0));
    let nonZeroElements = Math.floor(n * n * 0.1); // 10% non-zero elements

    for (let i = 0; i < nonZeroElements; i++) {
        let row = Math.floor(Math.random() * n);
        let col = Math.floor(Math.random() * n);
        let value = Math.floor(Math.random() * 100) + 1; // Random value between 1 and 100
        matrix[row][col] = value;
    }
    return matrix;
}

// Define la matriz en JavaScript
let matrix = generateSparseMatrix(8);

  // Genera la representación en LaTeX de la matriz
const generarMatrizLaTeX = (matrix) => {
let latex = "\\begin{bmatrix}";
matrix.forEach((fila, index) => {
    latex += fila.join(" & "); // Une los elementos de la fila con &
    if (index < matrix.length - 1) {
    latex += " \\\\ "; // Salto de línea en LaTeX
    }
});
latex += "\\end{bmatrix}";
return latex;
};

// Inserta la matriz en el DOM
const divMatriz = document.getElementById("matrix");
divMatriz.innerHTML = `$$${generarMatrizLaTeX(matrix)}$$`;

// Randomizar matriz

const randomizeBttn = document.getElementById("randomizeButton");
randomizeBttn.onclick = () => {
    matrix = generateSparseMatrix(8);
    divMatriz.innerHTML = `$$${generarMatrizLaTeX(matrix)}$$`;
    MathJax.typeset();
}

// Obtener los valores de los parámetros al presionar el botón

const calcularBttn = document.getElementById("calculateButton");

calcularBttn.onclick = () => {
    // fetch
    // URL del servidor
    let url = "http://127.0.0.1:8000/api/matrix/";

    // Matriz a enviar al servidor
    let matrixtoSend = matrix; 
    // Método usado para el formato en el radio del formulario
    let method = document.querySelector('input[name="methodOption"]:checked').value;
    let operation = document.querySelector('input[name="operationOption"]:checked').value;
    
    // Objeto con los datos a enviar al servidor
    let data = {
        matrix: matrixtoSend,
        method: method,
        operation: operation
    };

    // Realizar el fetch con POST
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Aquí puedes manejar la respuesta del servidor}
        // Insertar la respuesta en el DOM

    })
    .catch((error) => {
        console.error('Error:', error);
    });
    


}
