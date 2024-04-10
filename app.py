from db_sqlite import db_creation, open_file , export_csv

localidades = "localidades.csv"

# * Llamado a las funciones
db_creation()
open_file(localidades)
export_csv()