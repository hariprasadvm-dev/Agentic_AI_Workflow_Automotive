import pandas as pd
import os
from typing import Dict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
class ServicePlannerAgent:

    def __init__(self, state):
        """
        Initializes the Service Planner Agent with shared workflow state.
        Requires 'battery_insight' key in the state.
        """
        self.state = state
        self.insight = self.state.get('battery_insight', {})
        self.rag_enabled = False
    
    def plan_service(self):

        status = self.insight.get("status", "unknown")

        if status == "rapid degradation":
            action = "Immediate service required. Prioritize battery inspection and replacement."
            urgency = "high"
            source_status = status
        elif status == "moderate degradation":
            action = "Schedule service within the next month. Focus on battery health monitoring."
            urgency = "medium"
            source_status = status
        elif status == "normal degradation":
            action = "Routine service as per schedule. No immediate action needed."
            urgency = "low"
            source_status = status
        else:
            action = "Unable to determine action due to missing status."
            urgency = "unknown"
            source_status = status
        service_plan = {
            "action": action,
            "urgency": urgency,
            "source_status": source_status
        }
        return service_plan
    def plan(self):
        # Step 1: Create baseline plan (rule-based)
        decision = self.plan_service()
        print("Baseline Service Plan:")
        print(decision)

        # Step 2: Augment with service manual (RAG)
        rag_find = self.query_service_manual(self.insight)
        print("RAG Findings:")
        print(rag_find)

        # Step 3: Enhance plan with RAG insights
        enhanced_plan = self.enhance_plan_with_rag(decision, rag_find)
        print("Enhanced Service Plan:")

        # Step 4: Update state
        self.state["service_plan"] = enhanced_plan
        self.state["rag_insights"] = rag_find
        
        return self.state
    
    def query_service_manual(self, battery_analysis: Dict) -> Dict:
        """Query Tesla service manual using RAG"""
        
        # Build query from battery analysis
        soh = battery_analysis.get('latest_soh', 100)
        anomalies = battery_analysis.get('anomalies', [])
        
        query = f"""
        Tesla battery at {soh}% State of Health.
        Issues: {', '.join(anomalies) if anomalies else 'None'}.
        What service procedures and ODIN routines are recommended?
        """
        
        try:
            # Define embeddings
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            # Retrieve relevant manual sections
            vector_store = FAISS.load_local(
                    "vector_index", 
                    embeddings,
                    allow_dangerous_deserialization=True
                )
            docs = vector_store.similarity_search(query, k=3)
            
            # Extract key information
            procedures = []
            odin_routines = []
            manual_content = []
            
            for doc in docs:
                content = doc.page_content
                manual_content.append(content[:200])  # First 200 chars of each doc
                
                # Extract ODIN routines (Tesla diagnostic commands)
                import re
                routines = re.findall(r'PROC_[A-Z0-9_-]+', content)
                odin_routines.extend(routines)
                
            # Extract procedures (look for common patterns)
            if "procedure" in content.lower() or "step" in content.lower():
                procedures.append(content[:100])  # Extract relevant snippet
                
            # Extract ODIN routines
            if "odin" in content.lower() or "diagnostic" in content.lower():
                odin_routines.append(content[:100])  # Extract relevant snippet
            
            return {
                'procedures': procedures[:2],  # Top 2 relevant procedures
                'odin_routines': list(set(odin_routines))[:3],  # Top 3 unique routines
                'manual_sections_found': len(docs),
                'raw_content': manual_content
            }
            
        except Exception as e:
            print(f"⚠️  RAG query failed: {e}")
            return {
                'procedures': ["Standard battery inspection"],
                'odin_routines': ["Basic diagnostic check"],
                'manual_sections_found': 0,
                'raw_content': []
                }

    def enhance_plan_with_rag(self, baseline_plan: Dict, rag_insights: Dict) -> Dict:
        """Enhance baseline plan with RAG insights"""
        
        # Create a copy to avoid modifying original
        enhanced_plan = baseline_plan.copy()

        # Add RAG information to plan
        enhanced_plan.update({
            'rag_enhanced': True,
            'tesla_procedures': rag_insights.get('procedures', []),
            'odin_routines': rag_insights.get('odin_routines', []),
            'manual_sections_referenced': rag_insights.get('manual_sections_found', 0)
        })

        return enhanced_plan

if __name__ == "__main__":
    mock_state = {
        "battery_insight": {
            "status": "moderate degradation",
            "recommendation": "Monitor battery health closely.",
            "anomalies": ["2023-01-15", "2023-03-22"],
            "average_loss_per_cycle": 0.15,
            "decline_types": {
                "fast_avg_drop": 0.25,
                "slow_avg_drop": 0.1
            },
            "anomalies_count": 2,
            "highlight_dates": ["2023-02-10", "2023-04-05"],
            "latest_soh": 85.5
        }
    }
    agent = ServicePlannerAgent(mock_state)
    updated_state = agent.plan()
    print("Service Plan")
    for key, value in updated_state["service_plan"].items():
        print(f"{key}: {value}")


    
        