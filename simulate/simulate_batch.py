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
interval = config.get("interval_seconds", 30)

# Control interno para simular el avance del tiempo
fake_now = datetime.now()

def inject_error(value):
    return random.choice([None, "error", -9999, 9999, "NaN"])

def generate_batch():
    global fake_now
    rows = []

    for house in houses:
        profile = house["profile"]
        base_range = profiles[profile]["consumption_range"]
        base_consumption = np.random.uniform(*base_range)

        # Simular temperatura y voltaje
        temperature = np.random.uniform(10, 35)
        voltage = np.random.normal(220, 5)

        # Introducir correlaciones
        temp_effect = np.interp(temperature, [10, 35], [+0.2, -0.2])  # más calor → menos consumo
        volt_effect = np.interp(voltage, [210, 230], [+0.1, -0.1])    # menos voltaje → más consumo

        adjusted_consumption = base_consumption * (1 + temp_effect + volt_effect)

        # Variabilidad realista (pequeños picos)
        spike = np.random.normal(1, 0.1)  # media=1, std=0.1
        final_consumption = round(adjusted_consumption * spike, 2)

        row = {
            "timestamp": fake_now.isoformat(),
            "house_id": house["id"],
            "consumption_kWh": final_consumption,
            "temperature": round(temperature, 1),
            "voltage": round(voltage, 1),
        }

        # Inyectar errores ocasionalmente
        for key in ["consumption_kWh", "temperature", "voltage"]:
            if random.random() < error_prob:
                row[key] = inject_error(row[key])

        rows.append(row)

    df = pd.DataFrame(rows)
    os.makedirs("data/raw", exist_ok=True)
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f"data/raw/batch_{now_str}.csv", index=False)
    print(f"✅ Lote generado: batch_{now_str}.csv con {len(rows)} filas.")

    # Simular avance del tiempo
    fake_now += timedelta(seconds=interval)

if __name__ == "__main__":
    while True:
        generate_batch()
        time.sleep(interval)
