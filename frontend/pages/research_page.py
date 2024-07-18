import streamlit as st
import requests


RESEARCH_START_URL = "http://localhost:9000/research/start"

def research_report():
    st.title("Research Report")
    st.write("This is the research report page.")