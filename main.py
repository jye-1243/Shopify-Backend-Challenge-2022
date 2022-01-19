from flask import Flask, g, render_template, redirect, url_for, request, flash
import sqlite3 as sql

DATABASE = 'database.db'

# Initialize app
app = Flask(__name__)
# Secret key needed for flash, not very important in this case
app.secret_key = '12345654321'

# Function to get database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

# Close database when closing app
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Default views items by warehouse
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    # Search query for all warehouses and entries
    sqlite_query = """SELECT id, title, quantity, descript, warehouses.warehouse_id, warehouse_name, warehouse_address FROM entries
                    LEFT JOIN warehouses ON entries.warehouse_id = warehouses.warehouse_id"""
    cursor.execute(sqlite_query)

    # Get database query results
    entries = cursor.fetchall()
    records = {}

    # Create dictionary where each key is each warehouse
    # Separate out everything by warehouse
    # Could have used ORDER BY in the SQL Query, but this way with the keys is probably easier to handle on the frontend display
    for entry in entries:
        warehouse = entry[5]
        records[warehouse] = records.get(entry[5], [])
        records[warehouse].append(entry)

    # Render index template
    return render_template("index.html", list=records)

# Route to add an item into the database
@app.route('/add',  methods=['GET', 'POST'])
def add():
    db = get_db()
    cursor = db.cursor()

    # POST request
    if request.method == 'POST':
        # Convert data from form into tuple format
        name = request.form.get('name')
        amount = request.form.get('amount')
        description = request.form.get('description')
        warehouse = request.form.get('warehouse')
        data_tuple = (name, amount, description, warehouse)

        # Query database to see if an item already exists in the database
        # Should only have one entry per item per warehouse
        check_query = """SELECT title FROM entries WHERE title=? AND warehouse_id=? """
        cursor.execute(check_query, (name, warehouse ))

        # Get database query results
        entry = cursor.fetchone()
        # If no entry already exists in the database, insert it
        if not entry:
            sqlite_insert_query = """ INSERT INTO entries (title, quantity, descript, warehouse_id) VALUES (?, ?, ?, ?)"""

            # Insert into database
            cursor.execute(sqlite_insert_query, data_tuple)

            db.commit()
        # Error message
        else: 
            flash("Item already exists")
        # Redirect to main page
        return redirect(url_for('index'))

    # Get warehouse info for dropdown and render add template
    query = """SELECT warehouse_id, warehouse_name FROM warehouses"""
    cursor.execute(query)
    warehouses = cursor.fetchall()

    return render_template("add.html", warehouses=warehouses)

# Route to delete an item from database
@app.route('/delete', methods=['GET', 'POST'])
def remove():
    
    db = get_db()
    cursor = db.cursor()

    # Post request
    if request.method == "POST":
        deletes=request.form.getlist("deletes")

        # If no items selected to delete, return request url
        if not deletes:
            return(redirect(request.url))

        # Delete selected items if they exist 
        sqlite_delete_query = """ DELETE FROM entries WHERE title = ? """
        for item in deletes:
            cursor.execute(sqlite_delete_query, (item,))
            db.commit()

        return redirect(url_for('index'))


    # Select all items and corresponding warehouses -> main identifiers
    sqlite_query = """SELECT DISTINCT title, warehouse_name FROM entries
                        LEFT JOIN warehouses ON entries.warehouse_id=warehouses.warehouse_id"""
    cursor.execute(sqlite_query)

    # Get database query results
    records = cursor.fetchall()


    return render_template("delete.html", records=records)

# Route to edit an existing item
@app.route('/edit',  methods=['GET', 'PUT', 'POST'])
def edit():
    db = get_db()
    cursor = db.cursor()

    # Check if URL has arguments that describe which item is being edited
    args = request.args
    if args.get('id'):
        # Convert ID to number, without end character
        id = args.get('id')[:-1]
        # Search query for all info on that item
        sqlite_query = """SELECT id, title, quantity, descript, entries.warehouse_id, warehouse_name FROM entries
                        LEFT JOIN warehouses ON entries.warehouse_id=warehouses.warehouse_id WHERE id=?"""
        cursor.execute(sqlite_query, (id,))

        # Get database query results for the selected item
        entry = cursor.fetchone()

        # Get warehouses as well for dropdown
        warehouse_query = """SELECT * FROM warehouses"""
        cursor.execute(warehouse_query)
        warehouses = cursor.fetchall()

        # Render template for that entry
        return render_template("edit.html", data=entry, warehouses=warehouses)
    
    # POST method
    # Case where an edit has been made
    if request.method == "POST":
        # Convert data into tuple format
        id = request.form.get('id')
        name = request.form.get('name')
        amount = request.form.get('amount')
        description = request.form.get('description')
        warehouse_id = request.form.get('warehouse')
        data_tuple = (name, amount, description, warehouse_id, id,)

        # Insert into database
        sqlite_insert_query = """ UPDATE entries SET title = ?, quantity = ?, descript = ?, warehouse_id = ? WHERE id = ?"""
        cursor.execute(sqlite_insert_query, data_tuple)

        db.commit()

    return redirect(url_for('index'))

# Route to manage warehouses
@app.route('/warehouses', methods=['GET', 'POST'])
def warehouses():
    db = get_db()
    cursor = db.cursor()
    # Case where a submission has been made via post request
    if request.method == 'POST':
        # If the post has an ID, it is a deletion
        if request.form.get('id'):
            id = request.form.get('id')
            id = int(id[:-1])
            # Delete selected images if they exist 
            sqlite_delete_query = """ DELETE FROM warehouses WHERE warehouse_id = ? """
            
            cursor.execute(sqlite_delete_query, (id,))
            db.commit()

        else:
            # Convert data into tuple format
            name = request.form.get('name')
            address = request.form.get('address')
            data_tuple = (name, address,)

            # Check if such a warehouse already exists
            check_query = """SELECT warehouse_name FROM warehouses WHERE warehouse_name=? """
            cursor.execute(check_query, (name,))
            entry = cursor.fetchone()

            # If no warehouse exists, insert into database
            if not entry:
                sqlite_insert_query = """ INSERT INTO warehouses (warehouse_name, warehouse_address) VALUES (?, ?)"""

                # Insert into database
                cursor.execute(sqlite_insert_query, data_tuple)

                db.commit()
            # Error if exists
            else: 
                flash("Warehouse already exists")

    # Get all warehouses and display
    sqlite_query = """SELECT * FROM warehouses"""
    cursor.execute(sqlite_query)
    records = cursor.fetchall()
   
    return render_template("warehouses.html", list=records)