# synthetic_soh_data.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_soh_data(days=90, seed=42):
    """
    Generates synthetic EV battery data over a specified number of days.
    Includes SoH degradation influenced by fast and slow charging patterns.
    """
    np.random.seed(seed)

    start_date = datetime(2025, 6, 1)
    data = []
    soh = 100.0  # Start with full battery health

    for i in range(days):
        date = start_date + timedelta(days=i)
        temperature = np.random.normal(25, 5)  # Simulate ambient temperature
        is_fast_charge = np.random.rand() < 0.3  # 30% chance of fast charging
        charge_type = 'fast' if is_fast_charge else 'slow'

        # Apply different degradation rates based on charge type
        if is_fast_charge:
            degradation = np.random.uniform(0.02, 0.06)
        else:
            degradation = np.random.uniform(0.005, 0.02)
        
        soh = max(soh - degradation, 60.0)  # Cap minimum SoH at 60%

        # Append daily record
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': round(temperature, 2),
            'charge_type': charge_type,
            'SoH': round(soh, 2),
            'charge_cycles': np.random.randint(1, 3)  # Simulate 1-2 cycles/day
        })

    # Create and export DataFrame
    df = pd.DataFrame(data)
    df.to_csv('battery_logs.csv', index=False)
    print("✅ Synthetic SoH data generated and saved to 'battery_logs.csv'")

if __name__ == "__main__":
    generate_synthetic_soh_data()

# Note: The above script can be run independently to generate the synthetic data.