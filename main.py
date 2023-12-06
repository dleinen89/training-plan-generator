import datetime
import pandas as pd
from docxtpl import DocxTemplate
import streamlit as st
from coldata import col_names, date_cols
import base64
from io import BytesIO

# Ensure openpyxl is installed, needed for pd.read_excel to work with .xlsx files
try:
    import openpyxl
except ImportError:
    st.error("Missing optional dependency 'openpyxl'. Use pip or conda to install openpyxl.")
    raise

# Streamlit page configuration
st.set_page_config(page_title="Final Training Plan Generator", layout="wide")

def convert_dates_in_row(row, date_columns):
    """Converts date columns in a row to the desired format."""
    for col in date_columns:
        if pd.notnull(row[col]):
            if isinstance(row[col], datetime.datetime):
                row[col] = row[col].strftime("%d/%m/%y")
            else:
                row[col] = str(row[col])
        else:
            row[col] = ""
    return row

def generate_training_plan(excel_file, template_file, rego_num):
    try:
        # Read the Excel file into a Pandas DataFrame
        studentdata = pd.read_excel(excel_file)
        studentdata.columns = col_names
        
        matching_row = studentdata[studentdata["RegoNum"] == int(rego_num)].iloc[0]
        matching_row = convert_dates_in_row(matching_row, date_cols)
        
        context = matching_row.to_dict()

        doc = DocxTemplate(template_file)
        doc.render(context)
        
        # Save to BytesIO object instead of file system
        output_stream = BytesIO()
        doc.save(output_stream)
        
        # Prepare output stream for download
        output_stream.seek(0)
        b64 = base64.b64encode(output_stream.read()).decode()
        
        # Prepare download link
        first_name = matching_row["StudentFirstName"]
        last_name = matching_row["StudentLastName"]
        output_file_name = f"{first_name}_{last_name}_Training_Plan.docx"
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{output_file_name}">Download Word file</a>'
        
        return href # Return the download link directly
    
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI elements
st.title("Final Training Plan Generator")

excel_file = st.file_uploader("Upload Excel File (*.xlsx):", type=["xlsx"])
template_file = st.file_uploader("Upload Word Template File (*.docx):", type=["docx"])
rego_num = st.text_input("Enter Student Registration Number:")

if excel_file and template_file and rego_num:
    if st.button("Generate Training Plan"):
        download_link = generate_training_plan(excel_file, template_file, rego_num)
        if download_link.startswith('Error'):
            st.error(download_link)
        else:
            st.success("Training plan created successfully!")
            st.markdown(download_link, unsafe_allow_html=True)