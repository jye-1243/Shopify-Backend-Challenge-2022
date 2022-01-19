from flask import Flask, g, render_template, redirect, url_for, request, flash
import sqlite3 as sql

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = '12345654321'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    # Modify search_query based on if search exists
    sqlite_query = """SELECT id, title, quantity, descript, warehouses.warehouse_id, warehouse_name, warehouse_address FROM entries
                    LEFT JOIN warehouses ON entries.warehouse_id = warehouses.warehouse_id"""
    cursor.execute(sqlite_query)

    # Get database query results
    entries = cursor.fetchall()
    records = {}

    for entry in entries:
        warehouse = entry[5]
        records[warehouse] = records.get(entry[5], [])
        records[warehouse].append(entry)

    return render_template("index.html", list=records)

@app.route('/add',  methods=['GET', 'POST'])
def add():
    db = get_db()
    cursor = db.cursor()

    # POST request
    if request.method == 'POST':
        # Convert data into tuple format
        name = request.form.get('name')
        amount = request.form.get('amount')
        description = request.form.get('description')
        data_tuple = (name, amount, description,)

        # Modify search_query based on if search exists
        check_query = """SELECT title FROM entries WHERE title=? """
        cursor.execute(check_query, (name,))

        # Get database query results
        entry = cursor.fetchone()
        if not entry:
            sqlite_insert_query = """ INSERT INTO entries (title, quantity, descript) VALUES (?, ?, ?)"""

            # Insert into database
            cursor.execute(sqlite_insert_query, data_tuple)

            db.commit()
        else: 
            flash("Item already exists")

        return redirect(url_for('index'))

    query = """SELECT warehouse_id, warehouse_name FROM warehouses"""
    cursor.execute(query)
    warehouses = cursor.fetchall()

    return render_template("add.html", warehouses=warehouses)

@app.route('/delete', methods=['GET', 'POST'])
def remove():
    
    db = get_db()
    cursor = db.cursor()

    # Post request
    if request.method == "POST":
        deletes=request.form.getlist("deletes")

        # If no photos selected to delete, return request url
        if not deletes:
            return(redirect(request.url))

        # Delete selected images if they exist 
        sqlite_delete_query = """ DELETE FROM entries WHERE title = ? """
        for item in deletes:
            cursor.execute(sqlite_delete_query, (item,))
            db.commit()

        return redirect(url_for('index'))


    # Modify search_query based on if search exists
    sqlite_query = """SELECT DISTINCT title, quantity, descript FROM entries"""
    cursor.execute(sqlite_query)

    # Get database query results
    records = cursor.fetchall()


    return render_template("delete.html", records=records)

    
@app.route('/edit',  methods=['GET', 'PUT', 'POST'])
def edit():
    db = get_db()
    cursor = db.cursor()

    args = request.args
    if args.get('id'):
        id = args.get('id')[:-1]
        # Modify search_query based on if search exists
        sqlite_query = """SELECT id, title, quantity, descript, entries.warehouse_id, warehouse_name FROM entries
                        LEFT JOIN warehouses ON entries.warehouse_id=warehouses.warehouse_id WHERE id=?"""
        cursor.execute(sqlite_query, (id,))

        # Get database query results
        entry = cursor.fetchone()

        # Modify search_query based on if search exists
        warehouse_query = """SELECT * FROM warehouses"""
        cursor.execute(warehouse_query)

        # Get database query results
        warehouses = cursor.fetchall()

        return render_template("edit.html", data=entry, warehouses=warehouses)
    
    if request.method == "POST":
        # Convert data into tuple format
        id = request.form.get('id')
        name = request.form.get('name')
        amount = request.form.get('amount')
        description = request.form.get('description')
        warehouse_id = request.form.get('warehouse')
        data_tuple = (name, amount, description, warehouse_id, id,)
        sqlite_insert_query = """ UPDATE entries SET title = ?, quantity = ?, descript = ?, warehouse_id = ? WHERE id = ?"""

        # Insert into database
        cursor.execute(sqlite_insert_query, data_tuple)

        db.commit()

    return redirect(url_for('index'))

    
@app.route('/warehouses', methods=['GET', 'POST'])
def warehouses():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
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

            # Modify search_query based on if search exists
            check_query = """SELECT warehouse_name FROM warehouses WHERE warehouse_name=? """
            cursor.execute(check_query, (name,))

            # Get database query results
            entry = cursor.fetchone()
            if not entry:
                sqlite_insert_query = """ INSERT INTO warehouses (warehouse_name, warehouse_address) VALUES (?, ?)"""

                # Insert into database
                cursor.execute(sqlite_insert_query, data_tuple)

                db.commit()
            else: 
                flash("Warehouse already exists")

    # Modify search_query based on if search exists
    sqlite_query = """SELECT * FROM warehouses"""
    cursor.execute(sqlite_query)

    # Get database query results
    records = cursor.fetchall()
   
    return render_template("warehouses.html", list=records)