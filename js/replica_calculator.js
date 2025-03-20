const calculator = Desmos.GraphingCalculator(
    document.getElementById('calculator'),
    {keypad: false, expressions: true, expressionsCollapsed: true}
);

let functionChosen = document.querySelector('input[name="functionOption"]:checked').value;
const inputTerms = document.getElementById("numberInput");
const message = document.getElementById("message");
const inputA = document.getElementById("pointInput");
const bttn = document.getElementById("calculateButton");

function validateNumber() {
    const value = parseFloat(inputTerms.value);
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

function validateNumber2() {
    const value = parseFloat(inputA.value);
    if (value < 0 || isNaN(value)) {
        message.textContent = "Please choose a number greater or equal to 0";
        message.style.color = "yellow";
        // Deactivate bttn
        bttn.disabled = true;
    } else {
        bttn.disabled = false;
        message.textContent = "";
    }
}

bttn.addEventListener("click", () => {
    message.textContent = "";
    calculator.setBlank();
    const terms = parseInt(inputTerms.value);
    const a = parseFloat(inputA.value);
    if (terms <= 0 || isNaN(terms) || a < 0 || isNaN(a)) {
        return;
    } else {
        let functionChosen = document.querySelector('input[name="functionOption"]:checked').value;
        const data = {
            "n_terms": terms,
            "a": a,
            "function": parseInt(functionChosen)
        };
        fetch("http://127.0.0.1:8000/api/taylor",
        {
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
            let real_function = data.function;
            let taylor_function = data.latex;
            // quito $ de los strings
            real_function = real_function.replace(/\$/g, '');
            taylor_function = taylor_function.replace(/\$/g, '');
            console.log(real_function);
            console.log(taylor_function);
            calculator.setExpression({id: 'graph1', latex: `y=${real_function}`});
            calculator.setExpression({id: 'graph2', latex: `y=${taylor_function}`});
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    
    }
}
);
