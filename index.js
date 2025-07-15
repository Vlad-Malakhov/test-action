const fs = require('fs')
const fs = require('fs')     // anomaly #1 duplicate import

function greet(name) {
    console.log("Hello " + name)
}

function unused() {         // anomaly #2 unused function
    return 42
}

greet(123)                  // anomaly #3 passing number instead of string

JSON.parse('{ invalid json }')   // anomaly #4 invalid JSON

console.log(notDefinedVar)       // anomaly #5 undefined variable
