// Obtén los elementos necesarios del DOM
const input = document.getElementById('source_code');
const buttons = document.querySelectorAll('button');
const calculator = document.querySelector('.Calculadora');
const lexicalResultContainer = document.getElementById('lexical_result');

let string = '';
const arr = Array.from(buttons);

arr.forEach((button) => {
    button.addEventListener('click', (e) => {
        if (e.target.innerHTML === '=') {
            // Obtén el valor actualizado de la cadena de entrada
            string = input.value.trim();
            console.log('Input value:', string); // Verifica si la cadena de entrada se está capturando correctamente

            try {
                if (string !== '') {
                    // Evalúa la expresión matemática
                    const result = evaluateExpression(string);
                    input.value = result;
                }

                // Realiza una solicitud para obtener el análisis léxico
                fetchLexicalAnalysis(string);
            } catch (error) {
                input.value = 'Error';
                console.error('Error:', error);
            }

            // Reinicia la cadena de entrada
            string = '';
        } else if (e.target.innerHTML === 'C') {
            input.value = '';
        } else if (e.target.innerHTML === 'DEL') {
            input.value = input.value.slice(0, -1);
        } else {
            input.value += e.target.innerHTML;
        }
    });
});
// Función para evaluar la expresión matemática respetando la jerarquía de operaciones
function evaluateExpression(expression) {
    // Utiliza una pila (stack) para evaluar la expresión
    const operands = [];
    const operators = [];

    let currentNumber = '';

    // Función auxiliar para evaluar operaciones y actualizar la pila de operandos
    const evaluateOperation = () => {
        const operator = operators.pop();
        const rightOperand = operands.pop();
        const leftOperand = operands.pop();

        switch (operator) {
            case '+':
                operands.push(leftOperand + rightOperand);
                break;
            case '-':
                operands.push(leftOperand - rightOperand);
                break;
            case '*':
                operands.push(leftOperand * rightOperand);
                break;
            case '/':
                if (rightOperand === 0) {
                    throw new Error('División por cero');
                }
                operands.push(leftOperand / rightOperand);
                break;
            default:
                throw new Error('Operador no válido');
        }
    };

    // Itera sobre cada carácter de la expresión
    for (let i = 0; i < expression.length; i++) {
        const char = expression[i];

        if (!isNaN(char) || char === '.') {
            // Si es un dígito o un punto decimal, agrégalo al número actual
            currentNumber += char;
        } else {
            if (currentNumber !== '') {
                // Si el número actual no está vacío, conviértelo en un número y agrégalo a la lista de operandos
                operands.push(parseFloat(currentNumber));
                currentNumber = ''; // Reinicia el número actual
            }

            if (char === '+' || char === '-') {
                // Si es un operador de suma o resta
                while (operators.length > 0 && (operators[operators.length - 1] === '+' || operators[operators.length - 1] === '-' || operators[operators.length - 1] === '*' || operators[operators.length - 1] === '/')) {
                    evaluateOperation();
                }
                operators.push(char);
            } else if (char === '*' || char === '/') {
                // Si es un operador de multiplicación o división
                while (operators.length > 0 && (operators[operators.length - 1] === '*' || operators[operators.length - 1] === '/')) {
                    evaluateOperation();
                }
                operators.push(char);
            } else if (char === '(') {
                // Paréntesis izquierdo, simplemente agrégalo a la lista de operadores
                operators.push(char);
            } else if (char === ')') {
                // Paréntesis derecho, evalúa las operaciones dentro del paréntesis
                while (operators.length > 0 && operators[operators.length - 1] !== '(') {
                    evaluateOperation();
                }
                if (operators.length === 0 || operators[operators.length - 1] !== '(') {
                    throw new Error('Paréntesis desequilibrados');
                }
                operators.pop(); // Elimina el paréntesis izquierdo de la pila de operadores
            }
        }
    }

    // Agrega el último número a la lista de operandos si existe
    if (currentNumber !== '') {
        operands.push(parseFloat(currentNumber));
    }

    // Evalúa cualquier operación restante en la pila de operadores
    while (operators.length > 0) {
        evaluateOperation();
    }

    // El resultado final debe ser el único elemento en la lista de operandos
    if (operands.length === 1) {
        return operands.pop();
    } else {
        throw new Error('Expresión inválida');
    }
}
function fetchLexicalAnalysis(sourceCode) {
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ source_code: sourceCode }),
    })
    .then((response) => response.json())
    .then((data) => {
        // Muestra los resultados léxicos en el contenedor adecuado
        let html = '<ul>';
        data.lexical_result.forEach((token) => {
            html += `<li>${token[0]}: ${token[1]}</li>`;
        });
        html += '</ul>';
        lexicalResultContainer.innerHTML = html;
    })
    .catch((error) => console.error('Error:', error));
}


//numero:0-9
//decimales 0-9.0-9
//operadores: +,-,/,*
//parentesis_a: (
// parentesis_c)
// punto.
// igual: =