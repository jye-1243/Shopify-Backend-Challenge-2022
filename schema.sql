DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS warehouses;

CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    descript TEXT NOT NULL,
    warehouse_id INTEGER,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

CREATE TABLE warehouses (
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_name TEXT NOT NULL,
    warehouse_address TEXT NOT NULL
)