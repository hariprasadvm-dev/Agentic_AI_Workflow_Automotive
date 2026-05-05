import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from langgraph.graph import StateGraph, END
from .state import initial_state

from agents.battery_agent import BatteryInsightAgent
from agents.service_planner_agent import ServicePlannerAgent
from agents.scheduler_agent import SchedulerAgent
from agents.communicator_agent import CommunicationAgent

def battery_node(state):
    return  BatteryInsightAgent(state=state, 
                                data_path='battery_logs.csv').analyze()

def service_plan_node(state):
    return ServicePlannerAgent(state=state).plan()

def schedule_node(state):
    return SchedulerAgent(state=state).schedule()

def communicate_node(state):
    return CommunicationAgent(state=state).email_summary()

def build_graph(state=None):
    if state is None:
        state = initial_state()
    
    workflow = StateGraph(dict)
    workflow.add_node("battery_insight", battery_node)
    workflow.add_node("service_plan", service_plan_node)
    workflow.add_node("schedule_appointment", schedule_node)
    workflow.add_node("communicate", communicate_node)

    workflow.set_entry_point("battery_insight")
    workflow.add_edge("battery_insight", "service_plan")
    workflow.add_edge("service_plan", "schedule_appointment")
    workflow.add_edge("schedule_appointment", "communicate")
    workflow.add_edge("communicate", END)

    #workflow.compile().draw("agentic_workflow_dag.png")
    #print("✅ DAG diagram saved as 'agentic_workflow_dag.png'")

    app = workflow.compile()
    #app.draw("agentic_workflow_compiled_dag.png")
    #print("✅ Compiled DAG diagram saved as 'agentic_workflow_compiled_dag.png'")
    final_state = app.invoke(state)
    return final_state

if __name__ == "__main__":
    state = initial_state()
    state["battery_insight"] = {}
    final = build_graph(state)
    print("\nFinal State:")
    print(final)