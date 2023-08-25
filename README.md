# Fruit Basket
#### Video Demo:  https://youtu.be/FaSGAGpLqi4
#### Description:
#### Fruit Basket - Flask E-commerce Web Application
Fruit Basket is a Flask-based web application designed to provide an online platform for users to buy a variety of fresh and delicious fruits. With a user-friendly interface and powerful features, users can easily browse, select, and purchase their favorite fruits.

##### Features:
* User Registration and Authentication: Users can create accounts, log in, and manage their profiles to access personalized features.
* Product Catalog: Display a wide range of fruits with detailed descriptions and prices
* Shopping Cart: Users can add fruits to their cart, view the items and remove products.
* Search Functionality: Users can search for fruits based on name making it easier to find products.

##### Technologies Used:
* Flask: A lightweight web framework used for building the backend of the application.
* Python: The programming language used for server-side logic, data processing, and database integration.
* HTML: Markup language used for creating the structure and content of web pages.
* CSS: Cascading Style Sheets used for styling the HTML elements and enhancing the visual appearance.
* JavaScript: A scripting language used to implement interactivity and dynamic behavior on the client-side.
* SQLite: A lightweight relational database management system used to store product information, user data, and orders.

##### Usage:
Browse through the Fruit Basket catalog to discover a wide variety of fresh fruits.
Click on a fruit to view detailed information, including price.
Add fruits to your shopping cart by specifying the quantity.
Review your selected items in the cart and make any necessary adjustments.
Proceed to the checkout process.
Your order has been succesfully placed.

##### app.py
* @app.route("/", methods = ["GET","POST"]):
    This is home page. It contains the nav bar, search bar and all the fruits available for sale. For method = "POST" I implemented the search bar and displayed the results
 of the search. Else it displays all the fruits without any search filter.
* @app.route("/login", methods = ["GET","POST"]):
  This is login page. It displays login page for method = "GET". Else it takes in the user input and logs the user in if all values entered are appropriate.
* @app.route("/register", methods = ["GET","POST"]):
  This is login page. It displays register page for method = "GET". Else it takes in the user input and registers the user in if all values entered are appropriate.
* @app.route("/logout"):
  It logs the user out of the session and takes them back to the login page.
* @app.route("/product/<int:product_id>"):This displays product details page. From the page you can select the desired quantity and add the item to cart.It also contains the description of products.
* @app.route("/Addtocart", methods = ["GET","POST"]):
  Adds the selected item to the cart. This displays cart page with all the items selected in the cart with their respective images, prices, quantities and such including the new one.
* @app.route("/cart"):
  It will show the products present in the cart.
* @app.route("/remove_from_cart/<int:product_id>"):
  This takes the product id and removes that particular product from the cart.
* @app.route("/checkout", methods = ["GET","POST"]):
  If method = "POST" it deletes all the products from the cart and places the order. Else it redirects the user back to the home page
