# batch-energy-monitoring
 # ⚡ Batch Energy Monitoring

Simulación y procesamiento batch de consumo energético residencial usando PySpark, PostgreSQL, y herramientas modernas de Data Engineering.

![Banner](https://raw.githubusercontent.com/TomasFuentesA/batch-energy-monitoring/main/assets/banner_energy.gif)

---

## 📌 Descripción

Este proyecto simula el consumo energético de distintas viviendas en un vecindario y ejecuta un pipeline batch completo:

- Simulación de datos sintéticos y realistas
- Limpieza y validación de datos en Spark
- Ingesta a PostgreSQL mediante Spark Structured Streaming
- Análisis exploratorio con Jupyter y modelado con scikit-learn
- Contenerización completa usando Docker

---

```markdown
## 🏗️ Arquitectura

```mermaid
flowchart LR
    A[simulate_batch.py] --> B[data/raw]

    B --> C[preprocess.py (Spark)]
    C --> D[data/clean]
    C --> E[PostgreSQL: energy_data_raw]
    C --> F[PostgreSQL: energy_data_cleaned]

    F --> G[Jupyter/EDA]
    F --> H[ML models (scikit-learn)]
    E --> G
