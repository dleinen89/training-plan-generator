import streamlit as st
import pandas as pd
from src.data_processing import load_excel_data, search_users, display_completion_rate, display_user_profile
from src.document_generation import generate_training_plan, get_template_from_github

# Set page config
st.set_page_config(page_title="Final Training Plan Generator", page_icon="📚", layout="wide", initial_sidebar_state="expanded", menu_items=None)

# Define colors
HEADER_COLOR = "#eb8f3c"

# Apply custom theme
st.markdown(f"""
    <style>
    /* Main background */
    .stApp {{
        background-color: #07154b;
    }}

    /* Headings */
    h1, h2, h3 {{
        color: {HEADER_COLOR} !important;
        font-weight: bold;
    }}

    /* Text color */
    body, p, .stTextInput label, .stSelectbox label {{
        color: #e0e0e0 !important;
    }}

    /* Buttons */
    .stButton > button, .stDownloadButton > button {{
        background-color: {HEADER_COLOR};
        color: #0e1117;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background-color: #2ac1de;
        color: #ffffff;
    }}

    /* Input fields */
    .stTextInput > div > div > input, .stSelectbox > div > div > input {{
        background-color: #ffffff;
        color: #000000 !important;
        border-radius: 5px;
    }}

    /* Completion rate bar */
    .completion-rate-bar {{
        background-color: #1e2530;
        border-radius: 10px;
        padding: 3px;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, .2);
    }}
    .completion-rate-bar > div {{
        border-radius: 7px;
        height: 20px;
        text-align: center;
        line-height: 20px;
        color: #ffffff;
        transition: width 0.5s ease-in-out;
    }}

    /* User profile */
    .user-profile {{
        background-color: #1e2530;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .user-profile h3 {{
        margin-bottom: 10px;
    }}
    .user-profile p {{
        margin: 5px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("Final Training Plan Generator")

    # GitHub repository details
    repo_owner = "dleinen89"
    repo_name = "training-plan-generator"
    template_path = "templates/training_plan_template.docx"

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        with st.spinner("Loading Excel file..."):
            df = load_excel_data(uploaded_file)
        
        if df is not None:
            st.success("Excel file loaded successfully!")
            search_term = st.text_input("Search by Registration Number, Employee Number, Last Name, or First Name")
            if search_term:
                results = search_users(df, search_term)
                if not results.empty:
                    st.write(f"Found {len(results)} results:")
                    selected_user = st.selectbox(
                        "Select a user:",
                        options=results.index,
                        format_func=lambda x: f"{results.loc[x, 'StudentFirstName']} {results.loc[x, 'StudentLastName']} - RegoNum: {results.loc[x, 'RegoNum']}, EmployeeNum: {results.loc[x, 'EmployeeNum']}"
                    )

                    user_data = results.loc[selected_user]
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        display_user_profile(user_data)

                    with col2:
                        st.subheader("Completion Rate:")
                        display_completion_rate(user_data['CompletionRate'])
                    
                    if st.button("Generate Training Plan"):
                        if pd.isna(user_data['CompletionRate']) or float(user_data['CompletionRate']) < 1:
                            st.error("Cannot generate final training plan. Completion rate is not 100%.")
                        else:
                            with st.spinner("Generating training plan..."):
                                template_file = get_template_from_github(repo_owner, repo_name, template_path)
                                if template_file:
                                    doc_output = generate_training_plan(user_data, template_file)
                                    
                                    if doc_output:
                                        st.success("Training plan generated successfully!")
                                        st.download_button(
                                            label="Download Training Plan",
                                            data=doc_output,
                                            file_name=f"{user_data['StudentFirstName']} {user_data['StudentLastName']} Training Plan final.docx",
                                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                            key="download_button"
                                        )
                                    else:
                                        st.error("Failed to generate training plan.")
                                else:
                                    st.error("Failed to retrieve template from GitHub.")

                    # Display additional user information
                    with st.expander("View All User Data"):
                        st.write(user_data)
                else:
                    st.info("No results found.")
            else:
                st.info("Enter a search term to find users.")
        else:
            st.error("Failed to load Excel file. Please check the file and try again.")
    else:
        st.info("Please upload an Excel file to begin.")

if __name__ == "__main__":
    main()