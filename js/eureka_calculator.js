const calculator = Desmos.GraphingCalculator(
    document.getElementById('calculator'),
    {keypad: false, expressions: false}
);

let methodChosen = document.querySelector('input[name="functionOption"]:checked').value;
const inputPoint = document.getElementById("pointInput");
const message = document.getElementById("message");
const inputIter = document.getElementById("iterInput");
const bttn = document.getElementById("calculateButton");
const inputTolerance = document.getElementById("toleranceCombo");
const rateInput = document.getElementById("rateCombo");
const tempInput = document.getElementById("temperatureCombo");


function getTolerance () {
    return parseFloat(inputTolerance.value);
}

function getRate () {
    return parseFloat(rateInput.value);
}

function getTemperature () {
    return parseFloat(tempInput.value);
}

let actualTolerance = getTolerance();
let actualRate = getRate();
let actualTemperature = getTemperature();

function validateNumber() {
    const value = parseFloat(inputPoint.value);
    if (isNaN(value)) {
        message.textContent = "Please fill in the x-point";
        message.style.color = "yellow";
        // Deactivate bttn
        bttn.disabled = true;
    } else {
        bttn.disabled = false;
        message.textContent = "";
    }
}

function validateNumber2() {
    const value = parseFloat(inputIter.value);
    if (value < 2 || isNaN(value)) {
        message.textContent = "Please choose a number greater or equal to 2";
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
    const point = parseFloat(inputPoint.value);
    const iter = parseInt(inputIter.value);
    actualTolerance = getTolerance();
    actualRate = getRate();
    actualTemperature = getTemperature();
    if (isNaN(point) || isNaN(iter)) {
        return;
    } else {
        let methodChosen = document.querySelector('input[name="functionOption"]:checked').value;
        console.log(methodChosen);
        if (methodChosen == "1"){
            const data = {
                "function": "(x - 3)**2",
                "initial_point": point,
                "tolerance": actualTolerance,
                "max_iterations": iter
            };
            fetch("http://127.0.0.1:8000/api/newton",
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
                calculator.setExpression({id: 'graph1', latex: "y=(x-3)^2"});
                calculator.setExpression({id: 'graph2', latex: `${data.result.minimum_x},${data.result.minimum_f}`});
                message.textContent = `The mininum point is  (${data.result.minimum_x},${data.result.minimum_f}), found in ${data.result.iterations} iterations in ${data.result.execution_time} seconds`;
            })
        }
        if (methodChosen == "2"){
            const data = {
                "function": "(x - 3)**2",
                "initial_point": point,
                "learning_rate": actualRate,
                "tolerance": actualTolerance,
                "max_iterations": iter
            }
            fetch("http://127.0.0.1:8000/api/gradient",
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
                    calculator.setExpression({id: 'graph1', latex: "y=(x-3)^2"});
                    calculator.setExpression({id: 'graph2', latex: `${data.result.minimum_x},${data.result.minimum_f}`});
                    message.textContent = `The mininum point is  (${data.result.minimum_x},${data.result.minimum_f}), found in ${data.result.iterations} iterations in ${data.result.execution_time} seconds`;
                })
        }
        if (methodChosen == "3"){
            const data = {
                "function": "(x - 3)**2",
                "initial_point": point,
                "initial_temperature": actualTemperature,
                "cooling_rate": actualRate,
                "max_iterations": iter,
                "tolerance": actualTolerance
            }
            fetch("http://127.0.0.1:8000/api/sa",
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
                    calculator.setExpression({id: 'graph1', latex: "y=(x-3)^2"});
                    calculator.setExpression({id: 'graph2', latex: `${data.result.minimum_x},${data.result.minimum_f}`});
                    message.textContent = `Eureka! The mininum point is  (${data.result.minimum_x},${data.result.minimum_f}), found in ${data.result.iterations} iterations in ${data.result.execution_time} seconds`;
                })
        }


    }
});

