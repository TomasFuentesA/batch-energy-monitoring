FROM bitnami/spark:3.5.5

USER root
RUN install_packages python3 python3-pip
RUN pip3 install pyspark pandas sqlalchemy scikit-learn

COPY spark_jobs/preprocess.py ./app

# Copia los datos desde el contexto raíz
COPY data/raw /app/data/raw

WORKDIR /app