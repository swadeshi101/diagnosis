import os
import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# Milestone 1: Initialize API and Models
# Activity 1.1: Set up Google GenAI API credentials
genai.configure(api_key='AIzaSyC57ekJI6-i1S6MjxMMYi2nDOH2Rh9gyP0')

# Activity 1.2: Print available models for verification
model = genai.list_models()
for model in model:
    print(model)

# Activity 1.3: Initialize the Google Generative AI model
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", google_api_key='AIzaSyC57ekJI6-i1S6MjxMMYi2nDOH2Rh9gyP0', temperature=1.0)

# Milestone 3: Define Prompt Templates
# Activity 3.1: Create prompt template for differential diagnosis
prompt_templates = {
    "1": PromptTemplate(
        input_variables=["symptoms", "history", "test_results"],
        template="""Based on the patient's symptoms: {symptoms},
medical history: {history}, and test results: {test_results},
provide a differential diagnosis list prioritizing the most 
likely conditions. Include potential risks, complications, 
and recommended additional tests for further evaluation."""
    )
}

# Milestone 4: Collect User Inputs
# Activity 4.1: Collect diagnostic support input from the user
def get_diagnosis_input():
    with st.form("diagnosis_form"):
        symptoms = st.text_area("Patient's Symptoms:", "")
        history = st.text_area("Medical History:", "")
        test_results = st.text_area("Test Results (if any):", "")
        submitted = st.form_submit_button("Get Diagnosis")
        if submitted:
            return {"symptoms": symptoms, "history": history, "test_results": test_results}

# Milestone 5: Generate AI Responses
# Activity 5.1: Generate a differential diagnosis list
def get_prognosis_ai_response(prompt_type, input_data):
    """Generates a response based on the prompt type and input data."""
    if input_data is None:
        return "Error: Insufficient information provided."

    prompt = prompt_templates[prompt_type].format(**input_data)
    response = llm(prompt)
    return response

# Milestone 6: Build Streamlit User Interface
# Activity 6.1: Create main Streamlit application title and sidebar
st.title("PrognosisAI - Differential Diagnosis Support")

# Activity 6.2: Implement diagnostic support interface
input_data = get_diagnosis_input()
if input_data:
    with st.spinner("Analyzing..."):
        response = get_prognosis_ai_response("1", input_data)
        st.subheader("Possible Diagnoses:")
        st.write(response)
