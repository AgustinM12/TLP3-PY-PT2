from db_sqlite import db_functions, open_file , export_csv
localidades = "localidades.csv"

# * Crear la base de datos
db_functions()
open_file(localidades)
export_csv()