const calculator = Desmos.GraphingCalculator(
    document.getElementById('calculator'),
    {keypad: false, expressions: false}
);
calculator.setExpression({id: 'graph1', latex: 'y=x^2+3x-4'});
calculator.setExpression({id: 'graph2', latex: 'y=\\cos(x)', color: '#00ff00'});

const bttn = document.getElementById("calculateButton");
bttn.disabled = true;
const message = document.getElementById("message");
const input = document.getElementById('numberInput');

function validateNumber() {
    const value = parseFloat(input.value);
    if (value <= 0 || isNaN(value)) {
        message.textContent = "Please choose a number greater than 0";
        message.style.color = "yellow";
        // Deactivate bttn
        bttn.disabled = true;
    } else {
        bttn.disabled = false;
        message.textContent = "";
    }
}

function getRadius(){
    const input = document.getElementById('numberInput');
    return parseFloat(input.value);
}

bttn.addEventListener("click", () => {
    const radius = getRadius();
    if (radius <= 0 || isNaN(radius)) {
        return;
    } else {
        //! Insertar Código Aquí
        
    }
});

