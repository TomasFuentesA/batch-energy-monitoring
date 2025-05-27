import pandas as pd
import numpy as np
import os
import yaml
from datetime import datetime, timedelta
import time
import random

current_path = os.getcwd()

with open(f"{current_path}/house_profiles.yaml", "r") as f:
    config = yaml.safe_load(f)

houses = config["houses"]
profiles = config["profiles"]
error_prob = config.get("error_probability", 0.05)

# Simulación: avanzar 1 minuto por lote
time_step = timedelta(minutes=15)

# Velocidad real: cada 0.01 segundos
real_interval = 15

# Archivo de estado (solo simulated_time)
state_file = os.path.join(current_path, "simulation_state.yaml")

# Cargar estado si existe
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        saved = yaml.safe_load(f)
        simulated_time = datetime.fromisoformat(saved["simulated_time"])
    print(f"▶️ Reanudando desde {simulated_time}")
else:
    simulated_time = datetime(2024, 1, 1, 0, 0, 0)
    print("🆕 Iniciando desde 2024-01-01")

def inject_error(value):
    return random.choice([None, "error", -9999, 9999, "NaN"])

def generate_batch():
    global simulated_time
    rows = []

    for house in houses:
        profile = house["profile"]
        base_range = profiles[profile]["consumption_range"]
        base_consumption = np.random.uniform(*base_range)

        # Temperatura según estación con picos aleatorios
        month = simulated_time.month
        if month in [12, 1, 2]:  # Verano
            temperature = np.random.uniform(25, 35)
        elif month in [6, 7, 8]:  # Invierno
            temperature = np.random.uniform(5, 15)
        elif month in [3, 4, 5]:  # Otoño
            temperature = np.random.uniform(25, 35) if random.random() < 0.2 else np.random.uniform(15, 25)
        else:  # Primavera
            temperature = np.random.uniform(5, 10) if random.random() < 0.2 else np.random.uniform(15, 25)

        voltage = np.random.normal(220, 5)
        temp_effect = np.interp(temperature, [5, 35], [+0.2, -0.2])
        volt_effect = np.interp(voltage, [210, 230], [+0.1, -0.1])

        adjusted_consumption = base_consumption * (1 + temp_effect + volt_effect)
        final_consumption = round(adjusted_consumption * np.random.normal(1, 0.1), 2)

        row = {
            "timestamp": datetime.now().isoformat(),
            "simulated_timestamp": simulated_time.isoformat(),
            "house_id": house["id"],
            "consumption_kWh": final_consumption,
            "temperature": round(temperature, 1),
            "voltage": round(voltage, 1)
        }

        for key in ["consumption_kWh", "temperature", "voltage"]:
            if random.random() < error_prob:
                row[key] = inject_error(row[key])

        rows.append(row)

    df = pd.DataFrame(rows)
    os.makedirs("data/raw", exist_ok=True)
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"data/raw/batch_{now_str}.csv"
    df.to_csv(filepath, index=False)
    print(f"✅ {simulated_time.date()} | {filepath} con {len(rows)} filas.")

    # Guardar nuevo estado
    with open(state_file, "w") as f:
        yaml.dump({"simulated_time": simulated_time.isoformat()}, f)

    # Avanzar tiempo simulado
    simulated_time += time_step

if __name__ == "__main__":
    while True:
        generate_batch()
        time.sleep(real_interval)


