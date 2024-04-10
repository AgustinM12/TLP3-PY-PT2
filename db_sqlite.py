import sqlite3
import csv
import os

# ? Creacion y conexion a la base de datos
def db_creation():
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

            # * guardar en variables los datos de cada columna para insertar en la base de datos
            for columna in reader:
                provincia = columna[0]
                id_provincia = columna[1]
                localidad = columna[2]
                codigo_postal = columna[3]
                id_prov_mstr = columna[4]

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
    try:
        # * verificar si la carpeta csv_files existe, si no, crearla
        if not os.path.exists("csv_files"):
            os.makedirs("csv_files")

        # * conexion a la base de datos
        connectDB = sqlite3.connect('tp2_py.db')
        cursor = connectDB.cursor()

        # * obtener todos los nombres diferentes de la tabla provincias
        cursor.execute("SELECT DISTINCT nombre FROM provincias")
        lista_provincia = cursor.fetchall()

        # * eliminar la primer posicion que contiene el nombre de la columna
        lista_provincia = lista_provincia[1:]

        # * buscar los datos de las provincias
        for provincia in lista_provincia:
            cursor.execute("SELECT * FROM provincias WHERE nombre = ?", provincia)

            # * formatear el nombre del archivo CSV
            provincia = str(provincia)
            provincia = provincia[2:-3]

            provincia_data = cursor.fetchall()

            # * escribir los datos de cada provincia en un archivo CSV en el directorio csv_files
            with open(f"./csv_files/{provincia}.csv", "w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "nombre", "id_provincia", "localidad", "codigo_postal", "id_prov_mstr"])
                writer.writerows(provincia_data)

        cursor.close()
        connectDB.close()
    except Exception as e:
        print(f"Error: {e}")
