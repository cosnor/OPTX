const calculator = Desmos.GraphingCalculator(
    document.getElementById('calculator'),
    {keypad: false, expressions: false}
);

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

function getPoint(){
    let xinput = document.getElementById('xInput');
    let yinput = document.getElementById('yInput');
    let x = parseFloat(xinput.value);
    let y = parseFloat(yinput.value);
    return [x, y];
}

bttn.addEventListener("click", () => {
    message.textContent = "";
    calculator.setBlank();
    const radius = getRadius();
    if (radius <= 0 || isNaN(radius)) {
        return;
    } else {
        let point = getPoint();
        let data = {
            "r": radius,
            "point": point
        };
        fetch("http://127.0.0.1:8000/api/area", {
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
            
            if (data.is_point_inside){
                let x = data.axis_limits["x"]
                // Converting the string to a array
                x = JSON.parse(x);
                let x1 = x[0];
                let x2 = x[1];
                let y = data.axis_limits["y"]
                y = JSON.parse(y);
                let y1 = y[0];
                let y2 = y[1];

                let point = data.points;
                let x_point = point[0];
                let y_point = point[1];
                console.log(x_point, y_point);
                calculator.setExpression({id: 'point', latex: `(${x_point},${y_point})`});
                calculator.setExpression({id: 'graph1', latex: `x=${x1}`});
                calculator.setExpression({id: 'graph2', latex: `x=${x2}`});
                calculator.setExpression({id: 'graph3', latex: `y=${y1}`});
                calculator.setExpression({id: 'graph4', latex: `y=${y2}`});
                calculator.setExpression({id: 'graph5', latex: data.function});
                message.textContent = "The point is inside the circle and the rectangle area is: " + data.rectangle_area;
                message.style.color = "yellow";
            }  else {
                message.textContent = data.error;
                message.style.color = "yellow";
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        
    }
});

