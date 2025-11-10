from langchain_deepseek import ChatDeepSeek
from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tools.farm_sensor_tool import fetch_farm_sensor_data
import os
from dotenv import load_dotenv
import json # Import json

# Load environment variables
load_dotenv()

# --- MODIFIED: Updated AgentState (removed device_address) ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    device_id: str
    sensor_data: str
    current_advisor: str
    next_action: str

# Initialize LLM with DeepSeek
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    temperature=0.7,
    model_kwargs={}
)
# ═══════════════════════════════════════════════════════════════
#                         ROUTER NODE
# ═══════════════════════════════════════════════════════════════

def router_node(state: AgentState) -> AgentState:
    """
    Intelligently routes farmer queries to the appropriate specialist advisor
    """
    system_prompt = """You are a routing agent for an apple orchard AI advisory system.

Analyze the farmer's query and route to the appropriate specialist:

1. data_analyzer - Current conditions, sensor readings, "what's my current...?"
2. irrigation_advisor - Watering, soil moisture, irrigation scheduling
3. risk_advisor - Pests, diseases, weather threats, warnings
4. fertilizer_pesticide - Fertilization, nutrients, pest control products
5. general_advisor - Pruning, varieties, harvesting, general apple farming
6. off_topic - Any question NOT about farming, agriculture, or sensor data (e.g., "who is the prime minister", "what is a computer")

Respond with ONLY the advisor name (e.g., "irrigation_advisor"), nothing else."""
    
    user_message = state["messages"][-1].content
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Farmer's question: {user_message}")
    ]
    
    response = llm.invoke(messages)
    advisor = response.content.strip().lower().replace(" ", "_")
    
    valid_advisors = ["data_analyzer", "irrigation_advisor", "risk_advisor", 
                      "fertilizer_pesticide", "general_advisor", "off_topic"]
    
    if advisor not in valid_advisors:
        advisor = "general_advisor"  # Default fallback
    
    state["current_advisor"] = advisor
    state["next_action"] = advisor
    
    return state

# ═══════════════════════════════════════════════════════════════
#                  ADVISOR NODES (Updated)
# ═══════════════════════════════════════════════════════════════

# --- REMOVED get_data_footer function ---

def data_analyzer_node(state: AgentState) -> AgentState:
    """
    Analyzes current sensor data and provides interpretations
    """
    sensor_data = fetch_farm_sensor_data.invoke({"device_id": state["device_id"], "limit": 5})
    state["sensor_data"] = sensor_data
    
    # --- MODIFIED PROMPT (footer removed) ---
    system_prompt = f"""You are a data analyst. You MUST follow these rules:
1. Use limited, relevant emojis (like 🌡️, 💧).
2. NEVER use markdown or any symbols like *, -, or #.
3. Answer in English, Hindi or Hinglish.
4. Always add time and date of when was data recorded.

Here is the sensor data:
{sensor_data}

Based on the data, give the full data, related to the farmer's question."""
    
    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]
    
    response = llm.invoke(messages)
    state["messages"].append(AIMessage(content=response.content))
    state["next_action"] = "end"
    
    return state

def irrigation_advisor_node(state: AgentState) -> AgentState:
    """
    Provides irrigation recommendations based on real-time sensor data
    """
    sensor_data = fetch_farm_sensor_data.invoke({"device_id": state["device_id"], "limit": 10})
    state["sensor_data"] = sensor_data
    
    # --- MODIFIED PROMPT (footer removed) ---
    system_prompt = f"""You are an irrigation advisor. You MUST follow these rules:
1. Use limited, relevant emojis (like 💧, ☀️).
2. NEVER use markdown or any symbols like *, -, or #.
3. Answer in English, Hindi or Hinglish.
4. Always add time and date of when was data recorded.

Here is the sensor data:
{sensor_data}
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]
    
    response = llm.invoke(messages)
    state["messages"].append(AIMessage(content=response.content))
    state["next_action"] = "end"
    
    return state

def risk_advisor_node(state: AgentState) -> AgentState:
    """
    Assesses disease and pest risks based on environmental conditions
    """
    sensor_data = fetch_farm_sensor_data.invoke({"device_id": state["device_id"], "limit": 10})
    state["sensor_data"] = sensor_data
    
    # --- MODIFIED PROMPT (footer removed) ---
    system_prompt = f"""You are a risk advisor. You MUST follow these rules:
1. Use limited, relevant emojis (like 🦠, 🐛).
2. NEVER use markdown or any symbols like *, -, or #.
3. Answer in English, Hindi or Hinglish.
4. Always add time and date of when was data recorded.

Here is the sensor data:
{sensor_data}

Based on the data, what is the biggest risk right now and what should farmer do?"""
    
    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]
    
    response = llm.invoke(messages)
    state["messages"].append(AIMessage(content=response.content))
    state["next_action"] = "end"
    
    return state

def fertilizer_pesticide_node(state: AgentState) -> AgentState:
    """
    Provides fertilization schedules and pest control recommendations
    """
    sensor_data = fetch_farm_sensor_data.invoke({"device_id": state["device_id"], "limit": 5})
    state["sensor_data"] = sensor_data
    
    # --- MODIFIED PROMPT (footer removed) ---
    system_prompt = f"""You are an agronomist. You MUST follow these rules:
1. Use limited, relevant emojis (like 🌿).
2. NEVER use markdown or any symbols like *, -, or #.
3. Answer in English, Hindi or Hinglish.
4. Always add time and date of when was data recorded.

Here is the sensor data:
{sensor_data}

Based on the data, give a simple fertilizer or pesticide tip related to the farmer's question."""
    
    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]
    
    response = llm.invoke(messages)
    state["messages"].append(AIMessage(content=response.content))
    state["next_action"] = "end"
    
    return state

def general_advisor_node(state: AgentState) -> AgentState:
    """
    Handles general apple orchard management questions
    """
    # --- MODIFIED PROMPT (footer removed) ---
    system_prompt = f"""You are a general farm advisor. You MUST follow these rules:
1. Use limited, relevant emojis.
2. NEVER use markdown or any symbols like *, -, or #.
3. Answer in English, Hindi or Hinglish.
4. Always add time and date of when was data recorded.

Answer the farmer's question simply."""
    
    messages = [
        SystemMessage(content=system_prompt),
        *state["messages"]
    ]
    
    response = llm.invoke(messages)
    state["messages"].append(AIMessage(content=response.content))
    state["next_action"] = "end"
    
    return state

# --- "Off Topic" Node (Guardrail) ---
def off_topic_node(state: AgentState) -> AgentState:
    """
    Handles questions that are not related to farming.
    """
    response_text = "I am KeSAN, your apple farm assistant 🍎. I can only help with questions about apple farming and your sensor data. How can I assist you with your orchard today?"
    
    state["messages"].append(AIMessage(content=response_text))
    state["next_action"] = "end"
    
    return state

# ═══════════════════════════════════════════════════════════════
#                         ROUTING LOGIC
# ═══════════════════════════════════════════════════════════════

def route_to_advisor(state: AgentState) -> Literal["data_analyzer", "irrigation_advisor", "risk_advisor", "fertilizer_pesticide", "general_advisor", "off_topic", "end"]:
    """Routes to the appropriate advisor based on current state"""
    next_action = state.get("next_action", "end")
    
    if next_action == "end":
        return "end"
    
    return next_action

# ═══════════════════════════════════════════════════════════════
#                         BUILD THE GRAPH
# ═══════════════════════════════════════════════════════════════

def create_orchard_agent():
    """Creates and compiles the LangGraph agent"""
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("router", router_node)
    workflow.add_node("data_analyzer", data_analyzer_node)
    workflow.add_node("irrigation_advisor", irrigation_advisor_node)
    workflow.add_node("risk_advisor", risk_advisor_node)
    workflow.add_node("fertilizer_pesticide", fertilizer_pesticide_node)
    workflow.add_node("general_advisor", general_advisor_node)
    workflow.add_node("off_topic", off_topic_node)
    
    # Define edges
    workflow.add_edge(START, "router")
    
    workflow.add_conditional_edges(
        "router",
        route_to_advisor,
        {
            "data_analyzer": "data_analyzer",
            "irrigation_advisor": "irrigation_advisor",
            "risk_advisor": "risk_advisor",
            "fertilizer_pesticide": "fertilizer_pesticide",
            "general_advisor": "general_advisor",
            "off_topic": "off_topic",
            "end": END 
        }
    )
    
    # All advisors end the workflow
    workflow.add_edge("data_analyzer", END)
    workflow.add_edge("irrigation_advisor", END)
    workflow.add_edge("risk_advisor", END)
    workflow.add_edge("fertilizer_pesticide", END)
    workflow.add_edge("general_advisor", END)
    workflow.add_edge("off_topic", END)
    
    return workflow.compile()

# ═══════════════════════════════════════════════════════════════
#                       INVOCATION FUNCTION
# ═══════════════════════════════════════════════════════════════

# --- MODIFIED: Removed device_address ---
def invoke_agent(device_id: str, message: str):
    """
    Main function to invoke the agent
    """
    agent = create_orchard_agent()
    
    result = agent.invoke({
        "messages": [HumanMessage(content=message)],
        "device_id": device_id,
        "sensor_data": "",
        "current_advisor": "",
        "next_action": ""
    })
    
    return {
        "response": result["messages"][-1].content,
        "advisor_used": result["current_advisor"],
        "sensor_data_used": bool(result.get("sensor_data")),
        "all_messages": result["messages"]
    }