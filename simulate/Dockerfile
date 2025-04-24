FROM bitnami/python:3.9

USER root
RUN python3 -m pip install pandas numpy pyyaml

COPY simulate/simulate_batch.py ./app
COPY simulate/house_profiles.yaml ./app

WORKDIR /app
CMD ["python3", "simulate_batch.py"]