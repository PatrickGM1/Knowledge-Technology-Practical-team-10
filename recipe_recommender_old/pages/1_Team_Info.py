import streamlit as st

st.set_page_config(
    page_title="Team Info",
    layout="wide"

)

st.title("Team Information")

st.write("### Team 10")
st.write("Knowledge Technology Practical")

st.write("**Team Members:**")
st.write("- **Ana Maria Izbas** – S5575974 – *Analyst / Documentation Lead*")
st.write("- **George Radu Tutui** – S5515610 – *Knowledge Engineer (Chef Interviewer)*")
st.write("- **Mihai Patrick Gheba** – S5560535 – *Developer*")


st.write("---")

st.write("**Project:** Recipe Recommendation System")
st.write("A system that recommends recipes based on user preferences, available ingredients, and expert chef knowledge.")

st.write("---")

st.markdown("""
    <style>
    .stButton > button[kind="primary"] {
        background-color: #FF6B35 !important;
        border-color: #FF6B35 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #E55A2B !important;
        border-color: #E55A2B !important;
    }
    </style>
""", unsafe_allow_html=True)
