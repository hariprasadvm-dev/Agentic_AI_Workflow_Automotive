from datetime import datetime
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_api_key():
    """Get Groq API key from Streamlit secrets or environment variables"""
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


def get_client():
    """Create Groq client"""
    return OpenAI(
        api_key=get_api_key(),
        base_url="https://api.groq.com/openai/v1"
    )


class CommunicationAgent:
    def __init__(self, state):
        self.state = state
        self.insight = self.state.get("battery_insight", {})
        self.plan = self.state.get("service_plan", {})
        self.appointment = self.state.get("appointment", {})
        self.rag_insights = self.state.get("rag_insights", {})

    def summary_insight(self):
        soh = self.insight.get("latest_soh", "Unknown")
        anomalies = self.insight.get("anomalies", [])
        avg_loss = self.insight.get("average_loss_per_cycle", "Unknown")

        return (
            f"Battery State of Health (SoH): {soh}%.\n"
            f"The system detected {len(anomalies)} anomalies "
            f"and an average SoH decline of {avg_loss} per cycle."
        )

    def summarize_plan(self):
        return self.plan.get(
            "action",
            "No clear service recommendation found."
        )

    def summarize_appointment(self):
        if self.appointment.get("status") == "scheduled":
            dealer = self.appointment.get("dealer", "Unknown Dealer")
            slot = self.appointment.get("slot", "Unknown Slot")
            method = self.appointment.get("method", "Unknown Method")

            return (
                f"Appointment scheduled with {dealer} "
                f"on {slot} via {method}."
            )

        return "No appointment scheduled."

    def summarize_rag_content(self, raw_content):
        """Summarize service manual findings"""
        if not raw_content:
            return "No specific procedures found in manual."

        try:
            client = get_client()

            content_text = " ".join(raw_content[:3])

            prompt = f"""
            Summarize these Tesla service manual excerpts into
            2-3 actionable recommendations:

            {content_text}

            Focus on:
            - Specific procedures
            - ODIN diagnostic codes
            - Maintenance steps

            Keep it under 100 words.
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:
            print("RAG summary failed:", e)
            return "Manual procedures available - consult service documentation."

    def get_tesla_recommendations(self):
        raw_content = self.rag_insights.get("raw_content", [])

        if not raw_content:
            return "No specific Tesla service procedures found."

        summary = self.summarize_rag_content(raw_content)

        return f"""
Tesla Service Manual Recommendations:
📖 Based on {len(raw_content)} relevant manual sections:

{summary}

💡 These recommendations are extracted from service documentation.
"""

    def curate_email_with_llm(self, raw_content):
        """Improve email using Groq"""
        try:
            client = get_client()

            prompt = f"""
            Improve this vehicle maintenance email:

            {raw_content}

            Make it:
            - clear
            - concise
            - professional
            - friendly
            - easy for car owners to understand
            - include clear next steps
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            print("LLM curation failed:", e)
            return raw_content

    def email_summary(self):
        if self.appointment.get("status") != "scheduled":
            self.state["user_message"] = (
                "No appointment scheduled, email summary not generated."
            )
            return self.state

        insight_summary = self.summary_insight()
        plan_summary = self.summarize_plan()
        appointment_summary = self.summarize_appointment()

        raw_email = f"""
Subject: Battery Health and Service Summary

Dear User,

Here is the summary of your vehicle's battery health and service plan.

Battery Insight:
{insight_summary}

Service Plan:
{plan_summary}

Appointment Details:
{appointment_summary}

Best regards,
Vehicle Maintenance Team
"""

        final_email = self.curate_email_with_llm(raw_email)

        self.state["user_message"] = final_email
        return self.state