import math

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict

# Creates a FastAPI application object
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --- Pydantic Models ---

class Numbers(BaseModel):
    """Two-number input for operations like add, subtract, multiply, divide."""
    a: float
    b: float


class Number(BaseModel):
    """Single-number input. Ignores extra fields (e.g. 'mode') sent from JS."""
    model_config = ConfigDict(extra="ignore")
    value: float


class QuadraticEquation(BaseModel):
    """Coefficients for a quadratic equation: ax² + bx + c = 0."""
    a: float
    b: float
    c: float


class PowerInput(BaseModel):
    """Input for x raised to the power y."""
    x: float
    y: float


class RootInput(BaseModel):
    """Input for the yth root of x."""
    x: float
    y: float


class ExpInput(BaseModel):
    """Input for scientific notation: x × 10^exp."""
    x: float
    exp: float


class AngleInput(BaseModel):
    """Angle value with its mode: 'deg' for degrees, 'rad' for radians."""
    value: float
    mode: str


# --- Home Route ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# --- Basic Arithmetic ---

@app.post("/add")
def add(data: Numbers):
    """Add two numbers."""
    return {
        "operation": "addition",
        "result": data.a + data.b
    }


@app.post("/subtract")
def subtract(data: Numbers):
    """Subtract b from a."""
    return {
        "operation": "subtraction",
        "result": data.a - data.b
    }


@app.post("/multiply")
def multiply(data: Numbers):
    """Multiply two numbers."""
    return {
        "operation": "multiplication",
        "result": data.a * data.b
    }


@app.post("/divide")
def divide(data: Numbers):
    """Divide a by b. Returns error if b is zero."""
    if data.b == 0:
        return {"error": "Cannot divide by zero"}
    return {
        "operation": "division",
        "result": data.a / data.b
    }


# --- Roots & Powers ---

@app.post("/sqrt")
def sqrt(data: Number):
    """Square root. Returns error for negative input."""
    if data.value < 0:
        return {"error": "Square root of a negative number is not allowed"}
    return {
        "operation": "square root",
        "result": math.sqrt(data.value)
    }


@app.post("/square")
def square(data: Number):
    """Square a number (x²)."""
    return {
        "operation": "square",
        "result": data.value ** 2
    }


@app.post("/cube")
def cube(data: Number):
    """Cube a number (x³)."""
    return {
        "operation": "cube",
        "result": data.value ** 3
    }


@app.post("/cube-root")
def cube_root(data: Number):
    """Cube root. Handles negative numbers correctly."""
    if data.value < 0:
        result = -((-data.value) ** (1 / 3))
    else:
        result = data.value ** (1 / 3)
    return {
        "operation": "cube root",
        "result": result
    }


@app.post("/power")
def power(data: PowerInput):
    """Raise x to the power y (xʸ)."""
    return {
        "operation": "x^y",
        "result": data.x ** data.y
    }


@app.post("/nth-root")
def nth_root(data: RootInput):
    """Calculate the yth root of x. Handles negative base correctly."""
    if data.y == 0:
        return {"error": "Root degree cannot be zero"}
    if data.x < 0:
        result = -((-data.x) ** (1 / data.y))
    else:
        result = data.x ** (1 / data.y)
    return {
        "operation": "nth root",
        "result": result
    }


# --- Exponentials & Logarithms ---

@app.post("/exp")
def exponential(data: Number):
    """Calculate e raised to the power x (eˣ)."""
    return {
        "operation": "e^x",
        "result": math.exp(data.value)
    }


@app.post("/power10")
def power10(data: Number):
    """Calculate 10 raised to the power x (10ˣ)."""
    return {
        "operation": "10^x",
        "result": 10 ** data.value
    }


@app.post("/log")
def logarithm(data: Number):
    """Base-10 logarithm. Returns error for non-positive input."""
    if data.value <= 0:
        return {"error": "Logarithm is only defined for positive numbers"}
    return {
        "operation": "logarithm",
        "result": math.log10(data.value)
    }


@app.post("/ln")
def natural_log(data: Number):
    """Natural logarithm (base e). Returns error for non-positive input."""
    if data.value <= 0:
        return {
            "error": "Natural logarithm is only defined for positive numbers"
        }
    return {
        "operation": "natural logarithm",
        "result": math.log(data.value)
    }


@app.post("/scientific-exp")
def scientific_exp(data: ExpInput):
    """Scientific notation: returns x × 10^exp."""
    return {
        "operation": "scientific notation",
        "result": data.x * (10 ** data.exp)
    }


# --- Miscellaneous ---

@app.post("/reciprocal")
def reciprocal(data: Number):
    """Calculate 1/x. Returns error if x is zero."""
    if data.value == 0:
        return {"error": "Cannot divide by zero"}
    return {
        "operation": "reciprocal",
        "result": 1 / data.value
    }


@app.post("/factorial")
def factorial(data: Number):
    """Factorial of a non-negative integer."""
    if data.value < 0:
        return {"error": "Factorial is not defined for negative numbers"}
    return {
        "operation": "factorial",
        "result": math.factorial(int(data.value))
    }


@app.post("/percentage")
def percentage(data: Number):
    """Convert a percentage to its decimal form (e.g. 50 → 0.5)."""
    return {
        "operation": "percentage",
        "result": data.value / 100
    }


# --- Trigonometry ---

@app.post("/sin")
def sine(data: AngleInput):
    """Sine of an angle in degrees or radians."""
    if data.mode == "deg":
        result = math.sin(math.radians(data.value))
    else:
        result = math.sin(data.value)
    return {
        "operation": "sine",
        "result": result
    }


@app.post("/cos")
def cosine(data: AngleInput):
    """Cosine of an angle in degrees or radians."""
    if data.mode == "deg":
        result = math.cos(math.radians(data.value))
    else:
        result = math.cos(data.value)
    return {
        "operation": "cosine",
        "result": result
    }


@app.post("/tan")
def tangent(data: AngleInput):
    """Tangent of an angle in degrees or radians."""
    if data.mode == "deg":
        result = math.tan(math.radians(data.value))
    else:
        result = math.tan(data.value)
    return {
        "operation": "tangent",
        "result": result
    }


@app.post("/trig-all")
def trig_all(data: AngleInput):
    """Return all six trig values for a given angle."""
    angle = data.value
    if data.mode == "deg":
        angle = math.radians(angle)

    sin_val = math.sin(angle)
    cos_val = math.cos(angle)
    tan_val = math.tan(angle)

    EPSILON = 1e-10

    # Snap near-zero values to exactly 0
    if abs(sin_val) < EPSILON:
        sin_val = 0
    if abs(cos_val) < EPSILON:
        cos_val = 0
    if abs(tan_val) < EPSILON:
        tan_val = 0

    return {
        "sin": sin_val,
        "cos": cos_val,
        "tan": (
            "Undefined" if abs(cos_val) < EPSILON
            else sin_val / cos_val
        ),
        "cot": (
            "Undefined" if abs(sin_val) < EPSILON
            else cos_val / sin_val
        ),
        "sec": (
            "Undefined" if abs(cos_val) < EPSILON
            else 1 / cos_val
        ),
        "csc": (
            "Undefined" if abs(sin_val) < EPSILON
            else 1 / sin_val
        ),
    }


# --- Inverse Trigonometry ---

@app.post("/asin")
def arcsine(data: Number):
    """Inverse sine. Input must be between -1 and 1."""
    if data.value < -1 or data.value > 1:
        return {"error": "Input must be between -1 and 1"}
    return {
        "operation": "inverse sine",
        "result": math.degrees(math.asin(data.value))
    }


@app.post("/acos")
def arccosine(data: Number):
    """Inverse cosine. Input must be between -1 and 1."""
    if data.value < -1 or data.value > 1:
        return {"error": "Input must be between -1 and 1"}
    return {
        "operation": "inverse cosine",
        "result": math.degrees(math.acos(data.value))
    }


@app.post("/atan")
def arctangent(data: Number):
    """Inverse tangent."""
    return {
        "operation": "inverse tangent",
        "result": math.degrees(math.atan(data.value))
    }


@app.post("/inverse-trig-all")
def inverse_trig_all(data: AngleInput):
    """Return all six inverse trig values in degrees or radians."""
    value = data.value
    mode = data.mode
    result = {}

    def convert(angle):
        """Convert radians to degrees if mode is 'deg', else return as-is."""
        if mode == "deg":
            return math.degrees(angle)
        return angle

    # asin and acos (defined only for input in [-1, 1])
    if -1 <= value <= 1:
        result["asin"] = convert(math.asin(value))
        result["acos"] = convert(math.acos(value))
    else:
        result["asin"] = "Undefined"
        result["acos"] = "Undefined"

    # atan (defined for all real numbers)
    result["atan"] = convert(math.atan(value))

    # acot
    if value == 0:
        result["acot"] = 90 if mode == "deg" else math.pi / 2
    else:
        acot = convert(math.atan(1 / value))
        if value < 0:
            acot += 180 if mode == "deg" else math.pi
        result["acot"] = acot

    # asec and acosec (defined only for |input| >= 1)
    if abs(value) >= 1:
        result["asec"] = convert(math.acos(1 / value))
        result["acosec"] = convert(math.asin(1 / value))
    else:
        result["asec"] = "Undefined"
        result["acosec"] = "Undefined"

    return result


# --- Quadratic Equation Solver ---

@app.post("/solve-quadratic")
def solve_quadratic(data: QuadraticEquation):
    """
    Solve ax² + bx + c = 0.

    Returns two real roots, one real root, or complex roots
    depending on the discriminant (b² - 4ac).
    """
    a, b, c = data.a, data.b, data.c

    if a == 0:
        return {"error": "a cannot be 0 for a quadratic equation"}

    # discriminant determines the nature of the roots
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return {
            "equation_type": "Two Real Roots",
            "root1": root1,
            "root2": root2
        }
    elif discriminant == 0:
        root = -b / (2 * a)
        return {
            "equation_type": "One Real Root",
            "root": root
        }
    else:
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-discriminant) / (2 * a)
        return {
            "equation_type": "Complex Roots",
            "root1": f"{real_part}+{imaginary_part}i",
            "root2": f"{real_part}-{imaginary_part}i"
        }

# --- Request Flow ---
# Client sends JSON
#       ↓
# FastAPI receives request
#       ↓
# Pydantic validates data
#       ↓
# Function executes logic
#       ↓
# Return Python dictionary
#       ↓
# FastAPI converts it to JSON
#       ↓
# Client receives response

# Run with: uvicorn main:app --reload
