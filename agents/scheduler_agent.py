from datetime import datetime, timedelta
import pandas as pd
import random

class SchedulerAgent:
    def __init__(self, state):
        """
        Initialize the SchedulerAgent with the current state.

        Args:
            state (dict): The current state containing battery insights and other relevant information.
        """
        self.state = state
        self.insight = self.state.get('battery_insight', {})
        self.recommendation = self.state.get('service_plan', {}).get('action', "")
        self.dealers = {
            "Dealer_A": self._generate_slots(),
            "Dealer_B": self._generate_slots(),
            "Dealer_C": self._generate_slots()}

    # internal method to generate mock available slots for dealers    
    def _generate_slots(self):
        
        slots = []
        base_date = datetime.now()
        for i in range(1, 15):  # Next two weeks
            day = base_date + timedelta(days=i)
            for hour in [9, 11, 13, 15]:  # Four slots per day
                slots.append(day.replace(hour=hour, minute=0, second=0, microsecond=0))
        return slots
    
    def select_slot(self):
        dealer = random.choice(list(self.dealers.keys()))
        slots = random.choice(self.dealers[dealer])
        dealer_slot = {"dealer": dealer, "slot": slots}
        return dealer_slot
    
    def schedule(self):
        if "schedule" not in self.recommendation.lower():
            self.state["appointment"] = {
                "status": "no schedule needed",
                "details": "No scheduling action required based on current battery status."
            }
            return self.state  # No scheduling needed
        
        selection = self.select_slot()
        self.state["appointment"] = {
            "status": "scheduled",
            "dealer": selection["dealer"],
            "slot": selection["slot"],
            "method": "auto-selected by scheduler agent"
        }
        return self.state
    
if __name__ == "__main__":
    mock_state = {
        "service_plan": {
            "action": "Schedule service within the next month. Focus on battery health monitoring.",
            "urgency": "medium",
            "source_status": "moderate degradation"
        }
    }
    agent = SchedulerAgent(mock_state)
    updated_state = agent.schedule()

    for key, value in updated_state["appointment"].items():
        print(f"{key}: {value}")