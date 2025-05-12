FROM bitnami/spark:3.5.5

USER root

# Instalar curl
RUN install_packages curl

# Descargar el driver JDBC de PostgreSQL
RUN curl -o /opt/bitnami/spark/jars/postgresql-42.7.5.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.5.jar

WORKDIR /app
COPY . /app
