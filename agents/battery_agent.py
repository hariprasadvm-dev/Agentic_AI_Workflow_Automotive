import pandas as pd

class BatteryInsightAgent:
    def __init__(self, state, data_path):
        self.state = state
        self.data_path = data_path
    
    # Load battery data from CSV (instance method)
    ## Instance methods are functions defined in a class 
    ## that operate on an instance of that class. 
    ## They always take self as the first parameter,
    ## which refers to the object itself.
    def load_data(self):
        df = pd.read_csv(self.data_path)
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        df['SoH_drop'] = df['SoH'].shift(1) - df['SoH']
        return df
    
    def detect_anomalies(self, df, threshold=30.0):
        anomalies = df[df['SoH_drop'] > threshold]
        return anomalies['date'].tolist()
    
    def calculate_average_loss(self, df):
        avg_drop = df['SoH_drop'].mean()
        return avg_drop
    
    def fast_slow_decline(self, df, fast_threshold=0.5):
        fast = df[df['charge_type'] =="fast"]
        slow = df[df['charge_type'] =="slow"]
        return {
            'fast_avg_drop': fast['SoH_drop'].mean(),
            'slow_avg_drop': slow['SoH_drop'].mean()
        }
    
    def analyze(self):
        battery_data = self.load_data()
        anomalies = self.detect_anomalies(battery_data)
        avg_loss = self.calculate_average_loss(battery_data)
        decline_types = self.fast_slow_decline(battery_data)

        high_degradation = battery_data[battery_data['SoH_drop'] > 0.3]
        highlight_dates = high_degradation['date'].tolist()

        if avg_loss > 0.2:
            status = "rapid degradation"
            recommendation = "Schedule battery inspection immediately."
        elif avg_loss > 0.1:
            status = "moderate degradation"
            recommendation = "Monitor battery health closely."
        else:
            status = "normal degradation"
            recommendation = "No immediate action required."
            
        insights = {
            "status": status,
            "recommendation": recommendation,
            "anomalies": anomalies,
            "average_loss_per_cycle": avg_loss,
            "decline_types": decline_types,
            "anomalies_count": anomalies,
            "highlight_dates": highlight_dates,
            "latest_soh": round(battery_data['SoH'].iloc[-1], 2)
        }

        # Update state with results
        self.state["battery_insight"] = insights
        return self.state
    
    # Example use
if __name__ == "__main__":
    initial_state = {}
    agent = BatteryInsightAgent(state=initial_state, 
                                data_path='battery_logs.csv')
    updated_state = agent.analyze()
    for key, value in updated_state["battery_insight"].items():
        print(f"{key}: {value}")