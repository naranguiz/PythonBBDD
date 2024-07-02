import mysql.connector
import csv

# Credenciales de la base de datos (reemplazar con los valores reales)
db_config = {
    'host': '54.219.2.160',
    'user': 'postulante',
    'password': 'HB<tba!Sp6U2j5CN',
    'database': 'prueba_postulantes'
}

# Nombre de la tabla
table_name = 'encuesta'

# Nombre del archivo CSV de salida
csv_filename = 'datos_encuesta.csv'

try:
    # Establecer conexión con la base de datos
    connection = mysql.connector.connect(**db_config)

    # Crear un cursor
    cursor = connection.cursor()

    # Consulta SQL para obtener todas las columnas y filas de la tabla
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Obtener los resultados de la consulta
    results = cursor.fetchall()

    # Obtener los nombres de las columnas
    column_names = [desc[0] for desc in cursor.description]

    # Escribir los resultados en un archivo CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Escribir la cabecera (nombres de columnas)
        csv_writer.writerow(column_names)

        # Escribir las filas de datos
        csv_writer.writerows(results)

    print(f"Los datos se han exportado exitosamente a '{csv_filename}'")

except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")

finally:
    # Cerrar el cursor y la conexión
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()
        