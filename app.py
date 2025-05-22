import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from db_config import get_db_connection, release_db_connection, init_db, create_user
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize database
init_db()

# Initialize Groq client
if 'client' not in st.session_state:
    try:
        st.session_state.client = Groq(api_key=st.secrets["groq_api_key"])
    except Exception as e:
        st.error("Please set your GROQ_API_KEY in the Streamlit secrets")
        st.stop()

# Title and description
st.title("🤖 Groq Chatbot with Dual Summaries")
st.markdown("""
Yoliday Task/ Assignment - Shreeyans Arora
""")

# Function to save summaries to database
def save_to_db(user_id, original_text, casual_summary, formal_summary):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO summaries (user_id, original_text, casual_summary, formal_summary)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (user_id, original_text, casual_summary, formal_summary))
            summary_id = cur.fetchone()[0]
            conn.commit()
            return summary_id
    except Exception as e:
        st.error(f"Error saving to database: {str(e)}")
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Function to get recent summaries for a user
def get_recent_summaries(user_id, limit=5):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, original_text, casual_summary, formal_summary, created_at
                FROM summaries
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, limit))
            return cur.fetchall()
    except Exception as e:
        st.error(f"Error fetching from database: {str(e)}")
        return []
    finally:
        release_db_connection(conn)

# Function to generate summaries
def generate_summaries(text, style):
    try:
        if style == "casual":
            prompt = f"""Please provide a casual, friendly summary of the following text. 
            Use conversational language and make it sound natural and approachable:
            
            {text}"""
        else:
            prompt = f"""Please provide a formal, professional summary of the following text. 
            Use academic language and maintain a professional tone:
            
            {text}"""

        # Generate completion using Groq
        completion = st.session_state.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides clear and concise summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return "Sorry, there was an error generating the summary."

# Create tabs for different sections
tab1, tab2 = st.tabs(["Generate Summaries", "Recent Summaries"])

with tab1:
    # User ID input
    user_id = st.text_input("Enter your User ID:", key="user_id_input")
    
    if not user_id:
        st.warning("Please enter a User ID to continue.")
        st.stop()
    
    # Create user if they don't exist
    create_user(user_id)
    
    # Input area
    user_input = st.text_area("Enter your query:", height=150)

    # Generate summaries when button is clicked
    if st.button("Generate Summaries"):
        if user_input:
            # Create two columns for the summaries
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Casual Summary")
                with st.spinner('Generating casual summary...'):
                    casual_summary = generate_summaries(user_input, "casual")
                    st.write(casual_summary)
            
            with col2:
                st.subheader("📝 Formal Summary")
                with st.spinner('Generating formal summary...'):
                    formal_summary = generate_summaries(user_input, "formal")
                    st.write(formal_summary)
            
            # Save to database
            if casual_summary and formal_summary:
                summary_id = save_to_db(user_id, user_input, casual_summary, formal_summary)
                if summary_id:
                    st.success("Summaries saved successfully!")
        else:
            st.warning("Please enter a query first!")

with tab2:
    if not user_id:
        st.warning("Please enter a User ID in the Generate Summaries tab to view your history.")
    else:
        st.subheader(f"Recent Summaries for User: {user_id}")
        recent_summaries = get_recent_summaries(user_id)
        
        if recent_summaries:
            for summary in recent_summaries:
                with st.expander(f"Summary from {summary[4].strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.write("**Original Text:**")
                    st.write(summary[1])
                    st.write("**Casual Summary:**")
                    st.write(summary[2])
                    st.write("**Formal Summary:**")
                    st.write(summary[3])
        else:
            st.info("No summaries found for this user.")

# Add some styling
st.markdown("""
<style>
    .stTextArea textarea {
        font-size: 16px;
    }
    .stButton button {
        width: 100%;
        margin-top: 10px;
    }
    .stMarkdown {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True) 