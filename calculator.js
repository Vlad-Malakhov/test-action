function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) {
        console.log("Error: Cannot divide by zero.");
        return null;
    }
    return a / b;
}

console.log("Simple Calculator");

const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

readline.question("Enter first number: ", (num1) => {
    readline.question("Enter second number: ", (num2) => {
        readline.question("Enter operation (+, -, *, /): ", (operation) => {
            num1 = parseFloat(num1);
            num2 = parseFloat(num2);

            let result;

            if (operation === "+") {
                result = add(num1, num2);
            } else if (operation === "-") {
                result = subtract(num1, num2);
            } else if (operation === "*") {
                result = multiply(num1, num2);
            } else if (operation === "/") {
                result = divide(num1, num2);
            } else {
                console.log("Invalid operation.");
                result = null;
            }

            if (result !== null) {
                console.log("Result: " + result);
            }

            readline.close();
        });
    });
});