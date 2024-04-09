import sqlite3
import csv

# ? Creacion y conexion a la base de datos
def db_functions():
    connection = sqlite3.connect('tp2_py.db')
    # * Creacion de un cursor para ejecutar comandos SQL
    cursor = connection.cursor()
    # * Eliminar la tabla si ya existe
    cursor.execute("DROP TABLE IF EXISTS provincias")
    # * Crear la tabla
    cursor.execute("CREATE TABLE provincias (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, localidad TEXT, id_provincia INTEGER, codigo_postal INTEGER, id_prov_mstr INTEGER)")

    connection.commit()
    # * Cerrar el cursor, no la conexión
    cursor.close()  
    # * Cerrar la conexión
    connection.close()  


# ? Funcion para abrir el archivo CSV y cargar los datos en la base de datos
def open_file(file):
    #* coneccion a la DB
    connectDB = sqlite3.connect('tp2_py.db')
    cursor = connectDB.cursor()

    try:
        # * intentar leer el archivo CSV
        with open(file, "r", newline='') as local_csv:
            
            reader = csv.reader(local_csv)

            # * guardar en variables los datos de cada fila para insertar en la base de datos
            for fila in reader:
                provincia = fila[0]
                id_provincia = fila[1]
                localidad = fila[2]
                codigo_postal = fila[3]
                id_prov_mstr = fila[4]
                cursor.execute("INSERT INTO provincias (nombre, id_provincia, localidad, codigo_postal, id_prov_mstr) VALUES (?, ?, ?, ?, ?)", (provincia, id_provincia, localidad, codigo_postal, id_prov_mstr))

            # * cerrar la conexion a la base de datos
            connectDB.commit()
            cursor.close()
            connectDB.close()

    # * manejo de excepciones
    except FileNotFoundError:
        print(f"El archivo '{file}' no existe.")
    except Exception as e:
        print(f"Error: {e}")

# ? Funcion para exportar los datos de la base de datos a diferentes archivos CSV
def export_csv():
    connectDB = sqlite3.connect('tp2_py.db')
    cursor = connectDB.cursor()

    # * obtener todos los datos de la tabla provincias
    cursor.execute("SELECT * FROM provincias WHERE provincia = ")
    table_data = cursor.fetchall()

    # * guardar los datos en un archivo CSV por provincia
    for row in table_data:
         with open(f"{row[0]}.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["nombre", "id_provincia", "localidad", "codigo_postal", "id_prov_mstr"])
            writer.writerows(row)

    cursor.close()
    connectDB.close()
