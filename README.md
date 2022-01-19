# Shopify-Backend-Challenge-2022
Shopify Summer 2022 Backend and Production Internship Challenge

This web app is for a basic database for a logistics company with CRUD functionality, and an added function of being able to add warehouses and assign items to various warehouses.

## Getting Started

### Prerequisites
This project was built using Python3, which can be installed [here](https://www.python.org/downloads/). Once Python is installed, also install [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/).
This project also requires SQLite, which can be installed pursuant to these [instructions](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm)

### Installation and Deployment
1. Clone this [github repository](https://github.com/jye-1243/Shopify-Backend-Challenge-2022)
2. Navigate to your local folder for the repository in your command line.
3. Run `set FLASK_APP=main` and `set FLASK_ENV=development` in the aforementioned directory on CMD. Alternatively, the `set` keyword may be replaced with `export` in Bash. Other similar keywords may be found [here](https://flask.palletsprojects.com/en/2.0.x/config/)
4. Run the command `flask run` in the directory. This will run the app with the default app with some placeholder item names and quantities already included in the database.
5. The web app should open in Flask's provided address, usually [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
6. To reset the database, run `python init_db.py` and reload the app.

## Built With
This project was built with:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
- [Bootstrap Navbar](https://getbootstrap.com/docs/4.0/components/navbar/) - Bootstrap components
- [SQLite](https://www.sqlite.org/index.html) - Database
