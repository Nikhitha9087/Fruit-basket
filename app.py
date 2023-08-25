import os
from werkzeug.utils import secure_filename
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods = ["GET","POST"])
@login_required
def index():
    if request.method == "GET":
     products = db.execute("SELECT * FROM products")
     return render_template("index.html",products = products)
    else:
     nproducts = db.execute("SELECT * FROM products WHERE name LIKE ?","%"+request.form.get("search")+"%")
     return render_template("index.html",nproducts = nproducts,search = request.form.get("search"))

@app.route("/product/<int:product_id>")
@login_required
def product_detail(product_id):
    # get the data of the item
    product = db.execute("SELECT * FROM products WHERE product_id = ?", product_id)
    # render a template to display the item details
    return render_template("product_detail.html", product = product)

@app.route("/Addtocart", methods = ["GET","POST"])
@login_required
def add():
    if request.method == "POST":
        product_id = int(request.form.get("product_id"))
        sold_quantity = int(request.form.get("sold_quantity"))
        if sold_quantity <= 0:
         return apology("Invalid quantity",400)
        else:
         products = db.execute("SELECT * FROM products WHERE product_id = ?",product_id)
         db.execute("INSERT INTO cart (product_id,name,price,quantity,session_id) VALUES (?,?,?,?,?)",product_id,products[0]["name"],products[0]["price"],sold_quantity,session["user_id"])
         cart = db.execute("SELECT cart.name,cart.price,SUM(quantity) AS total_quantity,cart.product_id FROM cart JOIN users ON users.id = cart.session_id WHERE session_id = ? GROUP BY product_id",session["user_id"] )
         total = 0
         for i in cart:
          total += i["price"]*i["total_quantity"]
         return render_template("cart.html",cart = cart,total = total)
    else:
        return redirect("/")

@app.route("/cart")
@login_required
def cart():
        cart = db.execute("SELECT cart.name,cart.price,SUM(quantity) AS total_quantity,cart.product_id FROM cart JOIN users ON users.id = cart.session_id WHERE session_id = ? GROUP BY product_id",session["user_id"] )
        total = 0
        for i in cart:
          total += i["price"]*i["total_quantity"]
        return render_template("cart.html",cart = cart,total = total)
@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    db.execute("DELETE FROM cart WHERE product_id = ?",product_id)
    cart = db.execute("SELECT cart.name,cart.price,SUM(quantity) AS total_quantity,cart.product_id FROM cart JOIN users ON users.id = cart.session_id WHERE session_id = ? GROUP BY product_id",session["user_id"] )
    total = 0
    for i in cart:
     total += i["price"]*i["total_quantity"]
    return render_template("cart.html",cart = cart,total = total)

@app.route("/checkout", methods = ["GET","POST"])
@login_required
def checkout():
   if request.method == "POST":
      db.execute("DELETE FROM cart WHERE session_id = ?",session["user_id"])
      return render_template("success.html")
   else:
      return redirect("/")

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
        rows = db.execute(
           "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html",classy = 'bg-img')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        copy = request.form.get("confirmation")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if not username or len(rows) != 0:
            return apology("Invalid username or Username already exists", 400)
        if not password or not copy:
            return apology("Missing password", 400)
        elif password != copy:
            return apology("Passwords don't match", 400)
        else:
            db.execute(
                "INSERT INTO users(username,hash) VALUES(?,?)",
                username,
                generate_password_hash(password),
            )
        return redirect("/")
    else:
        return render_template("register.html")


