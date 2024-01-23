import sqlite3

conexion = sqlite3.connect("Pagos.db")
cursor = conexion.cursor()

# Crear la tabla de pagos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagos (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    id_multa INTEGER
)
""")

conexion.commit()
conexion.close()
