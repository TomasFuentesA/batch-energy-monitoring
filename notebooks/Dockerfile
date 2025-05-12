FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear carpeta base y subcarpeta de notebooks
WORKDIR /app
RUN mkdir -p /app/notebooks

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar bibliotecas de ciencia de datos y ML
RUN pip install --no-cache-dir \
    jupyterlab notebook \
    pandas numpy matplotlib seaborn \
    scikit-learn \
    sqlalchemy psycopg2-binary

# Exponer puerto
EXPOSE 8888

# Comando de inicio con ruta apuntando a /app/notebooks
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''", "--notebook-dir=/app/notebooks"]
