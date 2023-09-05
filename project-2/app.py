import math
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Custom expression parser
def custom_eval(expression):
    # Define a safe dictionary for evaluating expressions
    safe_dict = {"math": math}

    # Replace "^" with "**" for exponentiation
    expression = expression.replace("^", "**")

    # Replace trigonometric functions with degree conversion
    expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expression)
    expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expression)
    expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expression)
    
    # Replace sqrt with math.sqrt
    expression = expression.replace("sqrt(", "math.sqrt(")

    # Handle additional functions and constants
    expression = expression.replace("log(", "math.log10(")
    expression = expression.replace("ln(", "math.log(")
    expression = expression.replace("e", str(math.e))
    expression = expression.replace("pi", str(math.pi))

    try:
        # Evaluate the modified expression
        result = eval(expression, {"__builtins__": None}, safe_dict)
        return round(result, 2)  # Round the result to 2 decimal places
    except (TypeError, ValueError, NameError, SyntaxError):
        return "Invalid input"

# Rest of your Flask code...

@app.route("/", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        data = request.get_json()
        expression = data.get("expression", "")
        result = custom_eval(expression)
        return jsonify({"result": result})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
