import pandas as pd
import numpy as np
import os
import yaml
from datetime import datetime
import time
import random
import os

current_path = os.getcwd()

with open(f"{current_path}/house_profiles.yaml", "r") as f:
    config = yaml.safe_load(f)

houses = config["houses"]
profiles = config["profiles"]
error_prob = config.get("error_probability", 0.05)
interval = config.get("interval_seconds", 30)

def inject_error(value):
    # Randomly return None, string, or absurd number
    choices = [None, "error", -9999, 9999, "NaN"]
    return random.choice(choices)

def generate_batch():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    rows = []
    
    for house in houses:
        profile = house["profile"]
        r = profiles[profile]["consumption_range"]

        row = {
            "timestamp": datetime.now().isoformat(),
            "house_id": house["id"],
            "consumption_kWh": round(np.random.uniform(*r), 2),
            "temperature": round(np.random.uniform(15, 35), 1),
            "voltage": round(np.random.normal(220, 5), 1),
        }

        # Inyectar errores aleatoriamente
        for key in ["consumption_kWh", "temperature", "voltage"]:
            if random.random() < error_prob:
                row[key] = inject_error(row[key])

        rows.append(row)

    df = pd.DataFrame(rows)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(f"data/raw/batch_{now}.csv", index=False)
    print(f"✅ Lote generado: batch_{now}.csv")

# Ejecutar en loop
if __name__ == "__main__":
    while True:
        generate_batch()
        time.sleep(interval)