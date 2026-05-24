import streamlit as st
import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# 1. UI Configuration
st.set_page_config(page_title="EPL Nerd", page_icon="⚽", layout="wide")
st.title("⚽ EPL Nerd")

# 2. Visualization Tool Definition
@tool
def visualize_data(sql_query: str):
    """
    Executes a SQL query, stores the result as a DataFrame, 
    and prepares it for rendering as a chart. 
    Use this only when the user explicitly asks for a graph or chart.
    """
    try:
        df = pd.read_sql(sql_query, st.secrets["DATABASE_URL"])
        st.session_state.last_df = df
        return f"Data retrieved successfully. I have created a chart with {len(df)} rows."
    except Exception as e:
        return f"Error executing query: {e}"

# 3. Agent Initialization
@st.cache_resource
def initialize_agent():
    db = SQLDatabase.from_uri(st.secrets["DATABASE_URL"])
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=st.secrets["GROQ_API_KEY"]
    )
    
    # We use PREFIX instead of a full PromptTemplate so we don't overwrite the built-in SQL rules.
    prefix = """You are an expert SQL analyst for Premier League data.
- IMPORTANT: If the user asks for a 'chart', 'graph', 'plot', or 'visualization', you MUST use the 'visualize_data' tool. Do not just answer with text.
- IMPORTANT: When filtering by season, use the format 'YYYY-YY' (e.g., '2023-24', '2024-25').
- Do NOT use 'YYYY-YYYY' (e.g., do not use '2023-2024').
- answer in casual indonesian language.
- If you are unsure of the exact season string, use 'SELECT DISTINCT season FROM epl_player_stats' first.
- Always use SUM(goals_scored) when calculating total goals for a season.
- If you don't know a table name, first use 'sql_db_list_tables' to see what is available."""
    
    # Add visualization tool to the agent
    tools = [visualize_data]
    
    return create_sql_agent(
        llm=llm, 
        db=db, 
        agent_type="tool-calling", 
        prefix=prefix,             # <--- We use prefix here
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )

agent = initialize_agent()

# 4. Session State Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I'm connected to your EPL database! Ask me for stats or to build a chart."}]
if "last_df" not in st.session_state:
    st.session_state.last_df = None

# 5. Render Chat Interface
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 6. Handle User Input
if prompt := st.chat_input("Ask a question about the EPL data..."):
    # Display user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Process response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                # Invoke agent
                response = agent.invoke({
                    "input": prompt,
                    "chat_history": st.session_state.chat_history
                })
                
                answer = response["output"]
                st.write(answer)
                
                # Update history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.chat_history.append(("human", prompt))
                st.session_state.chat_history.append(("ai", answer))
                
                # Render chart if the tool was used
                if st.session_state.last_df is not None:
                    st.bar_chart(st.session_state.last_df)
                    # Clear last_df after rendering
                    st.session_state.last_df = None
                    
            except Exception as e:
                st.error(f"Error: {e}")
