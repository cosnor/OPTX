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
    // Matriz a enviar al servidor
    let matrixtoSend = matrix; 
    // Método usado para el formato en el radio del formulario
    let method = document.querySelector('input[name="opcion"]:checked').value;


}
