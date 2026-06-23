let lastAnswer = 0;
let memory = 0;
let angleMode = "deg";

function appendValue(value) {

    document.getElementById("display").value += value;

}

function clearDisplay() {

    document.getElementById("display").value = "";

    let results =
        document.getElementById("trigResults");

    if (results) {

        results.innerHTML = "";
    }

}

function safeEval(expression) {
    // Allow only safe math characters: digits, operators, parentheses, decimals, spaces
    if (!/^[\d\s\+\-\*\/\.\(\)]+$/.test(expression)) {
        throw new Error("Invalid characters in expression");
    }
    // Use Function constructor to evaluate in isolated scope (no access to global vars)
    return Function('"use strict"; return (' + expression + ')')();
}

function calculateResult() {

    let expression =
        document.getElementById("display").value;

    try {

        let result = safeEval(expression);

        if (!isFinite(result)) {
            throw new Error("Result is not finite");
        }

        lastAnswer = result;

        document.getElementById("display").value =
            result;

    }

    catch(error) {

        document.getElementById("display").value =
            "Error";

    }

}

function backspace() {

    let display =
        document.getElementById("display");

    display.value =
        display.value.slice(0, -1);

}

function appendPi() {

    document.getElementById("display").value +=
        Math.PI;

}

function useAns() {

    document.getElementById("display").value +=
        lastAnswer;

}

function memoryAdd() {

    memory += Number(
        document.getElementById("display").value
    );

}

function memorySubtract() {

    memory -= Number(
        document.getElementById("display").value
    );

}

function memoryRecall() {

    document.getElementById("display").value =
        memory;

}

function memoryClear() {

    memory = 0;

    // Brief visual feedback on the display
    let display = document.getElementById("display");
    let prev = display.value;
    display.value = "MC: Memory Cleared";
    setTimeout(() => { display.value = prev; }, 800);

}

function appendE() {

    document.getElementById("display").value +=
        Math.E;

}


async function callNumberAPI(endpoint) {

    let value = Number(
        document.getElementById("display").value
    );

    let response = await fetch(
        `http://127.0.0.1:8000/${endpoint}`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                value: value,
                mode: angleMode      
            })
        }
    );

    let data = await response.json();

    if (data.error) {

        document.getElementById("display").value =
            data.error;

        return;
    }

    document.getElementById("display").value =
        data.result;
}

async function calculatePower() {

    let x =
        Number(prompt("Enter x"));

    let y =
        Number(prompt("Enter y"));

    let response = await fetch(
        "http://127.0.0.1:8000/power",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                x: x,
                y: y
            })
        }
    );

    let data = await response.json();

    document.getElementById("display").value =
        data.result;
}

async function calculateNthRoot() {

    let x =
        Number(prompt("Enter x"));

    let y =
        Number(prompt("Enter root degree"));

    let response = await fetch(
        "http://127.0.0.1:8000/nth-root",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                x: x,
                y: y
            })
        }
    );

    let data = await response.json();

    document.getElementById("display").value =
        data.result;
}

function setDegreeMode() {

    angleMode = "deg";

    document.getElementById("degBtn")
        .classList.add("active-mode");

    document.getElementById("radBtn")
        .classList.remove("active-mode");

}

function setRadianMode() {

    angleMode = "rad";

    document.getElementById("radBtn")
        .classList.add("active-mode");

    document.getElementById("degBtn")
        .classList.remove("active-mode");

}

async function calculateEXP() {

    let x =
        Number(prompt("Enter number"));

    let exp =
        Number(prompt("Enter exponent"));

    let response = await fetch(
        "http://127.0.0.1:8000/scientific-exp",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                x: x,
                exp: exp
            })
        }
    );

    let data = await response.json();

    document.getElementById("display").value =
        data.result;
}

document.addEventListener(
    "DOMContentLoaded", 
    function () {
        document.getElementById("degBtn")
        .classList.add("active-mode");

        showNormalMode();

});


function showNormalMode() {

    document.getElementById("normalModeBtn")
        .classList.add("active-mode");

    document.getElementById("trigModeBtn")
        .classList.remove("active-mode");

    document.getElementById("normalMode")
        .style.display = "block";

    document.getElementById("trigModeContainer")
        .style.display = "none";

    document.getElementById("degBtn")
        .style.display = "none";

    document.getElementById("radBtn")
        .style.display = "none";
}

function showTrigMode() {

    document.getElementById("trigModeBtn")
        .classList.add("active-mode");

    document.getElementById("normalModeBtn")
        .classList.remove("active-mode");

    document.getElementById("normalMode")
        .style.display = "none";

    document.getElementById("trigModeContainer")
        .style.display = "block";

    document.getElementById("degBtn")
        .style.display = "block";

    document.getElementById("radBtn")
        .style.display = "block";
}

async function calculateTrigDirect() {

    let angle =
        safeEval(
            document.getElementById("display")
            .value
        );

    let response = await fetch(
        "http://127.0.0.1:8000/trig-all",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                value:angle,
                mode:angleMode
            })
        }
    );

    let data =
        await response.json();

    document.getElementById(
        "trigResults"
    ).innerHTML = `

    <h3>Trigonometric Values</h3>

    <table class="trig-table">

        <tr>
            <th>Function</th>
            <th>Value</th>
        </tr>

        <tr>
            <td>sin</td>
            <td>${Number(data.sin).toFixed(6)}</td>
        </tr>

        <tr>
            <td>cos</td>
            <td>${Number(data.cos).toFixed(6)}</td>
        </tr>

        <tr>
            <td>tan</td>
            <td>${
                data.tan === "Undefined"
                ? "Undefined"
                : Number(data.tan).toFixed(6)
            }</td>
        </tr>

        <tr>
            <td>cot</td>
            <td>${
                data.cot === "Undefined"
                ? "Undefined"
                : Number(data.cot).toFixed(6)
            }</td>
        </tr>

        <tr>
            <td>sec</td>
            <td>${
                data.sec === "Undefined"
                ? "Undefined"
                : Number(data.sec).toFixed(6)
            }</td>
        </tr>

        <tr>
            <td>cosec</td>
            <td>${
                data.csc === "Undefined"
                ? "Undefined"
                : Number(data.csc).toFixed(6)
            }</td>
        </tr>

    </table>
    `;
}

async function calculateInverseTrigDirect() {

    let value =
        Number(
            document.getElementById("display")
            .value
        );

    console.log({
        value: value,
        mode: angleMode
    });

    let response =
        await fetch(
            "http://127.0.0.1:8000/inverse-trig-all",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    value: value,
                    mode: angleMode
                })
            }
        );

    let data =
        await response.json();

    document.getElementById(
        "trigResults"
    ).innerHTML = `

    <h3>Inverse Trigonometric Values</h3>

    <table class="trig-table">

        <tr>
            <th>Function</th>
            <th>Value (${angleMode === "deg" ? "Degrees" : "Radians"})</th>
        </tr>

        <tr>
            <td>sin⁻¹</td>
            <td>${data.asin}</td>
        </tr>

        <tr>
            <td>cos⁻¹</td>
            <td>${data.acos}</td>
        </tr>

        <tr>
            <td>tan⁻¹</td>
            <td>${data.atan}</td>
        </tr>

        <tr>
            <td>cot⁻¹</td>
            <td>${data.acot}</td>
        </tr>

        <tr>
            <td>sec⁻¹</td>
            <td>${data.asec}</td>
        </tr>

        <tr>
            <td>cosec⁻¹</td>
            <td>${data.acosec}</td>
        </tr>

    </table>
    `;
}