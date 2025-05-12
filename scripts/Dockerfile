FROM bitnami/spark:3.5.5

WORKDIR /app

COPY . /app

# Descargar el driver JDBC de PostgreSQL (versión 42.7.5)
RUN curl -o /opt/bitnami/spark/jars/postgresql-42.7.5.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.5.jar

# Comando por defecto (puedes sobrescribir en compose si quieres)
CMD ["spark-submit", "--master", "local[*]", "insert_clean_data.py"]