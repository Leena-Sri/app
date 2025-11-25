from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Temporary "database"
users = {}

# HTML Templates
login_page = """
<!doctype html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; background:#f0f4f7; }
        .container {
            width: 350px; margin:80px auto; background:white; padding:25px;
            border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);
        }
        input, button, select {
            width:100%; padding:10px; margin-top:10px; border-radius:5px; border:1px solid #ccc;
        }
        button { background:#4287f5; color:white; border:none; cursor:pointer; }
        button:hover { background:#2f6bd9; }
        a { text-decoration:none; color:#4287f5; }
    </style>
</head>
<body>

<div class="container">
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Enter Username" required>
        <input type="password" name="password" placeholder="Enter Password" required>
        <button type="submit">Login</button>
        <p>Don't have an account? <a href="/register">Register</a></p>
    </form>
</div>

</body>
</html>
"""

register_page = """
<!doctype html>
<html>
<head>
    <title>Register</title>
    <style>
        body { font-family: Arial; background:#f7f0f5; }
        .container {
            width: 350px; margin:80px auto; background:white; padding:25px;
            border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);
        }
        input, button {
            width:100%; padding:10px; margin-top:10px; border-radius:5px; border:1px solid #ccc;
        }
        button { background:#e64398; color:white; border:none; cursor:pointer; }
        button:hover { background:#c83283; }
        a { text-decoration:none; color:#e64398; }
    </style>
</head>
<body>

<div class="container">
    <h2>Register</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Create Username" required>
        <input type="password" name="password" placeholder="Create Password" required>
        <button type="submit">Register</button>
        <p>Already have an account? <a href="/login">Login</a></p>
    </form>
</div>

</body>
</html>
"""

calculator_page = """
<!doctype html>
<html>
<head>
    <title>Calculator</title>
    <style>
        body { font-family: Arial; background:#eef2f3; }
        .container {
            width: 400px; margin:60px auto; background:white; padding:30px;
            border-radius:12px; box-shadow:0 0 12px rgba(0,0,0,0.2);
        }
        input, select, button {
            width:100%; padding:12px; margin-top:15px; border-radius:6px; border:1px solid #ccc;
        }
        button { background:#28a745; color:white; border:none; cursor:pointer; }
        button:hover { background:#218838; }
        .logout {
            text-align:right; margin-bottom:10px;
        }
        a { color:#e60b46; text-decoration:none; }
    </style>
</head>
<body>

<div class="container">

<div class="logout">
<a href="/logout">Logout</a>
</div>

<h2>Simple Calculator</h2>

<form method="POST">
    Number 1: 
    <input type="number" step="any" name="num1" required>

    Number 2:
    <input type="number" step="any" name="num2" required>

    Operation:
    <select name="operation" required>
        <option value="add">Addition (+)</option>
        <option value="subtract">Subtraction (−)</option>
        <option value="multiply">Multiplication (×)</option>
        <option value="divide">Division (÷)</option>
    </select>

    <button type="submit">Calculate</button>
</form>

{% if result is not none %}
  <h3>Result: {{ result }}</h3>
{% endif %}

</div>

</body>
</html>
"""


# ---------------- ROUTES ---------------- #
@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/calculator")
        else:
            return render_template_string(login_page + "<p style='color:red;text-align:center;'>Invalid login</p>")

    return render_template_string(login_page)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users:
            return render_template_string(register_page + "<p style='color:red;text-align:center;'>User already exists</p>")

        users[u] = p
        return redirect("/login")

    return render_template_string(register_page)


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if "user" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            result = num1 / num2 if num2 != 0 else "Error: Cannot divide by zero"

    return render_template_string(calculator_page, result=result)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route('/', methods=['GET','POST'])
def register():
    name = None
    email = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
    return render_template_string(FORM_HTML, name=name, email=email)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

