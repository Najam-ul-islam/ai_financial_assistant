from financial_assistant import FinancialAssistant as fa
from typing import Any
import streamlit as st
import time

# Streamlit UI for sidebar configuration
with st.container():
    st.sidebar.title("Financial Assistant Configuration")
    st.sidebar.info("""
        This is a demo application for the Financial Assistant. 
        Please enter your OpenAI API key in the sidebar to initialize the assistant.
    """)
# st.sidebar.title("Financial Assistant Menu")
entered_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Initialize the FinancialAssistant
financial_assistant = None

if entered_api_key:
    with st.spinner('Initializing Financial Assistant...'):
        try:
            financial_assistant = fa(apikey=entered_api_key)
        except Exception as e:
            st.error(f"Error initializing Financial Assistant: {e}")

# Streamlit UI for selecting the assistant
assistant_option = st.sidebar.selectbox("Select an Assistant", ("Financial Assistant",))

if assistant_option == "Financial Assistant":
    st.title("Financial Assistant Application")

    # Description
    # st.info("""
    #     This assistant is your go-to resource for financial insights and advice. 
    #     Simply enter your financial query below and let the assistant guide you with actionable insights.
    # """)

    # User input for financial query
    user_query = st.text_input("Enter your financial query:")

    # Example usage:
    if st.button('Run Financial Assistant', disabled=financial_assistant is None):
        with st.spinner('Running Financial Assistant...'):
            try:
                # Check if financial assistant is initialized
                if financial_assistant:
                    create_thread: Any = financial_assistant.create_thread()
                    run: Any = financial_assistant.submit_message(assistant_id=financial_assistant.assistant.id, thread=create_thread, user_message=user_query)
                    run: Any = financial_assistant.wait_on_run(run=run, thread=create_thread)
                    response_messages: Any = financial_assistant.get_response(thread=create_thread)
                    response: Any = financial_assistant.pretty_print_response(response_messages)
                    st.text_area("Response:", value=response, height=400)
                else:
                    st.warning("Financial Assistant is not initialized. Please enter your API key.")
            except Exception as e:
                st.error(f"Error running Financial Assistant: {e}")
