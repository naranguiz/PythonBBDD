import mysql.connector
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Configuración de la conexión a la base de datos
config = {
    'user': 'postulante',
    'password': 'HB<tba!Sp6U2j5CN',
    'host': '54.219.2.160',
    'database': 'prueba_postulantes'
}

# 1. Conexión a la base de datos
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

try:
    # 2. Consultas y cálculos de métricas

    # 2.1. SNG de satisfacción general
    query1 = "SELECT COUNT(*) AS total_satisfaccion FROM encuesta WHERE satisfeccion_general IN (6, 7);"
    query2 = "SELECT COUNT(*) AS total_insatisfaccion FROM encuesta WHERE satisfeccion_general IN (1, 2, 3, 4);"
    query3 = "SELECT COUNT(*) AS total_respuestas FROM encuesta WHERE satisfeccion_general IN (1,2,3,4,5,6,7);"

    cursor.execute(query1)
    total_satisfaccion = cursor.fetchone()[0]
    cursor.execute(query2)
    total_insatisfaccion = cursor.fetchone()[0]
    cursor.execute(query3)
    total_respuestas = cursor.fetchone()[0]

    porcentaje_satisfaccion = round((total_satisfaccion / total_respuestas) * 100)
    porcentaje_insatisfaccion = round((total_insatisfaccion / total_respuestas) * 100)
    sng = porcentaje_satisfaccion - porcentaje_insatisfaccion

    # 2.2. Total de personas que conocían a la empresa
    query = "SELECT COUNT(*) FROM encuesta WHERE conocia_empresa = 'Sí';"
    cursor.execute(query)
    total_conocedores = cursor.fetchone()[0]

    # 2.3. SNG de la recomendación (usando la misma lógica que 1.a)
    query_recomendacion_satisfaccion = "SELECT COUNT(*) AS total_recomendacion_satisfaccion FROM encuesta WHERE recomendacion IN (6, 7);"
    query_recomendacion_insatisfaccion = "SELECT COUNT(*) AS total_recomendacion_insatisfaccion FROM encuesta WHERE recomendacion IN (1,2,3,4);"
    query_total_recomendaciones = "SELECT COUNT(*) AS total_recomendaciones FROM encuesta WHERE recomendacion IN  (1,2,3,4,5,6,7);"

    cursor.execute(query_recomendacion_satisfaccion)
    total_recomendacion_satisfaccion = cursor.fetchone()[0]
    cursor.execute(query_recomendacion_insatisfaccion)
    total_recomendacion_insatisfaccion = cursor.fetchone()[0]
    cursor.execute(query_total_recomendaciones)
    total_recomendaciones = cursor.fetchone()[0]

    porcentaje_recomendacion_satisfaccion = round((total_recomendacion_satisfaccion / total_recomendaciones) * 100)
    porcentaje_recomendacion_insatisfaccion = round((total_recomendacion_insatisfaccion / total_recomendaciones) * 100)
    sng_recomendacion = porcentaje_recomendacion_satisfaccion - porcentaje_recomendacion_insatisfaccion


    # 2.4. Nota promedio de recomendación
    query = "SELECT AVG(recomendacion) FROM encuesta;"
    cursor.execute(query)
    nota_promedio_recomendacion = cursor.fetchone()[0]

    # 2.5. Total de personas que hicieron un comentario
    query = "SELECT COUNT(*) FROM encuesta WHERE recomendacion_abierta IS NOT NULL AND recomendacion_abierta != '';"
    cursor.execute(query)
    total_comentarios = cursor.fetchone()[0]

    # 2.6. Días y meses que llevó la encuesta
    query = "SELECT MIN(fecha), MAX(fecha) FROM encuesta;"
    cursor.execute(query)
    fecha_inicio_str, fecha_fin_str = cursor.fetchone()

    formato_fecha = "%Y-%m-%d %H:%M:%S" 
    fecha_inicio = datetime.strptime(fecha_inicio_str, formato_fecha)
    fecha_fin = datetime.strptime(fecha_fin_str, formato_fecha)

    dias_totales = (fecha_fin - fecha_inicio).days
    meses_encuesta = dias_totales // 30
    dias_restantes = dias_totales % 30


    # 3. Extracción de respuestas abiertas para análisis de sentimiento para posterior análisis en IA-Generativa.
  
    query = "SELECT recomendacion_abierta FROM encuesta WHERE recomendacion_abierta IS NOT NULL AND recomendacion_abierta != '';"
    cursor.execute(query)
    respuestas_abiertas = cursor.fetchall()

    with open('respuestas_abiertas.txt', 'w', encoding='utf-8') as f:
        for i, respuesta in enumerate(respuestas_abiertas, start=1):
            f.write(f"{i}. {respuesta[0]}\n\n")  # Enumeración y doble salto de línea

    # 4. Presentación de resultados
    print(f'SNG de satisfacción general: {sng}')
    print(f'Total de personas que conocían a la empresa: {total_conocedores}')
    print(f'SNG de recomendación: {sng_recomendacion}') 
    print(f'Nota promedio de recomendación: {nota_promedio_recomendacion:.2f}')
    print(f'Total de personas que hicieron un comentario: {total_comentarios}')
    print(f'Duración de la encuesta: {meses_encuesta} meses y {dias_restantes} días')

    # GRAFICAS

    # 5.1. Gráfico de barras para SNG de satisfacción general
    labels = ['Satisfacción', 'Insatisfacción']
    sizes = [porcentaje_satisfaccion, porcentaje_insatisfaccion]
    colors = ['#4CAF50', '#F44336']  # Verde (satisfacción), Rojo (insatisfacción)

    plt.figure(figsize=(10, 6))  # Tamaño más grande
    plt.bar(labels, sizes, color=colors)
    plt.title('SNG de Satisfacción General', fontsize=14)  # Título más grande
    plt.ylabel('Porcentaje', fontsize=12)  # Etiqueta más grande
    plt.xticks(fontsize=10)  # Etiquetas del eje X más grandes
    plt.ylim(0, 100)  # Límites del eje Y
    for i, v in enumerate(sizes):
        plt.text(i, v + 1, str(v) + '%', ha='center', fontsize=10)  # Etiquetas de datos
    plt.grid(axis='y', alpha=0.5)  # Cuadrícula en el eje Y

    plt.savefig('sng_satisfaccion_general.pdf')  # Guardar figura como PDF
    plt.close()

    # 5.2. Gráfico de pastel para conocían vs. no conocían a la empresa
    total_encuestados = total_respuestas
    total_no_conocedores = total_encuestados - total_conocedores
    labels = ['Conocían', 'No conocían']
    sizes = [total_conocedores, total_no_conocedores]

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=['#673AB7', '#FFC107'], explode=(0.05, 0))  # Colores y explosión
    plt.title('Conocimiento Previo de la Empresa', fontsize=14)

    plt.savefig('conocimiento_previo_empresa.pdf')  # Guardar figura como PDF
    plt.close()

    # 5.3. Gráfico de barras para SNG de recomendación
    labels = ['Satisfacción (Recomendación)', 'Insatisfacción (Recomendación)']  # Etiquetas claras
    sizes = [porcentaje_recomendacion_satisfaccion, porcentaje_recomendacion_insatisfaccion]
    colors = ['#2196F3', '#FF9800']  # Azul (satisfacción), Naranja (insatisfacción)

    plt.figure(figsize=(10, 6))
    plt.bar(labels, sizes, color=colors)
    plt.title('SNG de Recomendación', fontsize=14)
    plt.ylabel('Porcentaje', fontsize=12)
    plt.xticks(fontsize=10, rotation=15)  # Rotación de etiquetas
    plt.ylim(0, 100)
    for i, v in enumerate(sizes):
        plt.text(i, v + 1, str(v) + '%', ha='center', fontsize=10)
    plt.grid(axis='y', alpha=0.5)  # Cuadrícula en el eje Y

    plt.savefig('sng_recomendacion.pdf')  # Guardar figura como PDF
    plt.close()

    # 5.4. Histograma de distribución de las notas de recomendación
    query = "SELECT recomendacion FROM encuesta WHERE recomendacion IS NOT NULL;" # Consulta corregida
    cursor.execute(query)
    notas_recomendacion = [row[0] for row in cursor.fetchall()]  # Declaración dentro del try

    plt.figure(figsize=(10, 6))
    plt.hist(notas_recomendacion, bins=7, range=(1, 8), rwidth=0.8, color='#00BCD4')
    plt.title('Distribución de Notas de Recomendación', fontsize=14)
    plt.xlabel('Nota', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.xticks(range(1, 8))
    plt.grid(axis='y', alpha=0.5)

    plt.savefig('distribucion_notas_recomendacion.pdf')  # Guardar figura como PDF
    plt.close()

except mysql.connector.Error as err:
    print(f"Error en la base de datos: {err}")

finally:
    # Cerrar conexión
    if cnx.is_connected():
        cursor.close()
        cnx.close()

