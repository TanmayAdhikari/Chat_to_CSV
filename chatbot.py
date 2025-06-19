# Import Libraries
import streamlit as st
import pandas as pd
import os
from io import StringIO
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
api_key = os.getenv("AZURE_API_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")
api_version = os.getenv("AZURE_API_VERSION", "2023-05-15")  # Default if not specified
model_name = os.getenv("AZURE_MODEL_NAME", "gpt-35-turbo")  # Default if not specified

# Check if required environment variables are set
if not all([deployment_name, api_key, endpoint]):
    st.error("❌ Missing required environment variables. Please check your .env file.")
    st.info("Required variables: AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, AZURE_ENDPOINT")
    st.stop()

# Set up the Azure OpenAI model
llm = AzureChatOpenAI(
    azure_deployment=deployment_name,
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version,
    model_name=model_name,
)

# Define a reusable prompt
prompt = PromptTemplate.from_template("""
You are a Python pandas expert. Given a DataFrame `df` and a human instruction, write the exact Python code (no comments, no explanations) to modify it.

Instruction: {instruction}
""")
chain = prompt | llm | StrOutputParser()

# Streamlit UI
st.set_page_config(page_title="Smart CSV Editor", layout="wide")
st.title("🧠 LLM-Powered CSV Editor")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Original Data")
        st.dataframe(df, use_container_width=True)
        
        instruction = st.text_area("Enter a command (e.g., 'Add a column with all 1s' or 'Change value in row 2 column B to 100')")
        
        # Define python_code variable at a higher scope
        python_code = ""
        
        if st.button("Run Command"):
            with st.spinner("Interpreting with Azure OpenAI..."):
                try:
                    python_code = chain.invoke({"instruction": instruction})
                    st.code(python_code, language="python")
                    st.info("Generated code above ☝️ - Now executing...")
                    
                    exec_globals = {"df": df.copy()}
                    exec(python_code, exec_globals)
                    df = exec_globals["df"]
                    st.success("✅ Command executed successfully!")
                    st.dataframe(df, use_container_width=True)
                    
                    # Allow download
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Modified CSV",
                        data=csv,
                        file_name="modified.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"⚠️ Error while executing: {e}")
                    if python_code:
                        st.code(python_code, language="python")
                    st.error(f"Generated code encountered an error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error reading CSV file: {str(e)}")
