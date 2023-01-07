import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    cash = rows[0]["cash"]
    user_id = rows[0]["id"]

    stocks = db.execute("SELECT * FROM wallet WHERE user_id = ? AND shares != 0", user_id)
    grand_total = 0 + float(cash)

    for i in range(len(stocks)):
        stock = lookup(stocks[i]["symbol"])
        stocks[i]["price"] = stock["price"]
        stocks[i]["name"] = stock["name"]
        stocks[i]["total"] = int(stocks[i]['shares']) * float(stock["price"])
        grand_total += stocks[i]["total"]

    return render_template("index.html", stocks=stocks, grand_total=grand_total, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("The stock is not found", 400)

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        user = rows[0]
        user_id = user["id"]
        cash = user["cash"]
        time = str(datetime.datetime.now())
        symbol = stock["symbol"]
        price = stock["price"]
        shares = request.form.get("shares")

        if not str(shares).isnumeric():
            return apology("Shares cannot be non-numeric", 400)
        elif not float(shares).is_integer():
            return apology("Shares cannot be fractional", 400)

        cash_left = float(cash) - (float(price) * int(shares))

        if cash_left < 0:
            return apology("Not enough money", 400)

        db.execute("INSERT INTO history (user_id, symbol, price, shares, time) VALUES (?,?,?,?,?)",
            user_id, symbol, price, shares, time
            )

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_left, user_id)

        old_shares = db.execute("SELECT shares FROM wallet WHERE user_id = ? AND symbol = ?", user_id, symbol)
        if len(old_shares) == 0:
            db.execute("INSERT INTO wallet (user_id, symbol, shares) VALUES (?,?,?)", user_id, symbol, shares)
        else:
            new_shares = int(old_shares[0]["shares"]) + int(shares)
            db.execute("UPDATE wallet SET shares = ? WHERE user_id = ? AND symbol = ?",new_shares , user_id, symbol)

        return redirect("/")

    else: #if request method is "GET"
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY time DESC", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("The stock is not found", 400)

        return render_template("quoted.html", stock = stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        #check for valid username
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("username already exists", 400)

        #check for valid password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]

        return redirect("/")

    else: #if request.method == "GET"
        return render_template("register.html")


    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM wallet WHERE user_id = ? AND shares != 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)

    symbol = request.form.get("symbol")

    if symbol == None:
        return apology("Stock not selected")

    wallet = db.execute("SELECT * FROM wallet WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]

    shares_sell = request.form.get("shares")
    if int(wallet["shares"]) - int(shares_sell) < 0 :
        return apology("Not enough shares", 400)

    stock = lookup(symbol)
    price = stock["price"]
    shares = int(shares_sell) * (-1)
    time = str(datetime.datetime.now())

    db.execute("INSERT INTO history (user_id, symbol, price, shares, time) VALUES (?,?,?,?,?)",
        session["user_id"], symbol, price, shares, time
        )

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    db.execute("UPDATE users SET cash = ? WHERE id = ?", float(cash) + int(shares_sell) * float(price), session["user_id"])

    db.execute("UPDATE wallet SET shares = ? WHERE user_id = ? AND symbol = ?",
        int(wallet["shares"]) - int(shares_sell) , session["user_id"], symbol
        )

    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
