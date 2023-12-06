import datetime
import pandas as pd
from docxtpl import DocxTemplate
import streamlit as st
from coldata import col_names, date_cols
import io
import base64
from tempfile import NamedTemporaryFile

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

def load_docx_template(template_file):
    """Loads the docx template from the uploaded file."""
    with NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        tmp_file.write(template_file.read())
        tmp_filepath = tmp_file.name
    doc = DocxTemplate(tmp_filepath)
    return doc, tmp_filepath

def generate_download_link(docx_filepath):
    """Generates a download link for the DOCX file."""
    with open(docx_filepath, "rb") as file:
        byte_data = file.read()
    b64 = base64.b64encode(byte_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{docx_filepath.split("/")[-1]}">Download Word file</a>'
    return href

def generate_training_plan(excel_file, template_file, rego_num):
    try:
        # Read the Excel file into a Pandas DataFrame
        studentdata = pd.read_excel(excel_file)
        studentdata.columns = col_names
        
        matching_row = studentdata[studentdata["RegoNum"] == int(rego_num)].iloc[0]
        matching_row = convert_dates_in_row(matching_row, date_cols)
        
        context = matching_row.to_dict()
        
        doc, docx_filepath = load_docx_template(template_file)
        doc.render(context)
        
        first_name = matching_row["StudentFirstName"]
        last_name = matching_row["StudentLastName"]
        output_file_name = f"{first_name}_{last_name}_Training_Plan.docx"
        doc.save(output_file_name)
        
        return output_file_name, docx_filepath
    except Exception as e:
        return None, str(e)

# Streamlit UI elements
st.title("Final Training Plan Generator")

excel_file = st.file_uploader("Upload Excel File (*.xlsx):", type=["xlsx"])
template_file = st.file_uploader("Upload Word Template File (*.docx):", type=["docx"])

rego_num = st.text_input("Enter Student Registration Number:")

if excel_file and template_file and rego_num:
    if st.button("Generate Training Plan"):
        output_file_name, error_or_file_path = generate_training_plan(excel_file, template_file, rego_num)
        if output_file_name:
            st.success(f"Training plan created successfully: {output_file_name}")
            st.markdown(generate_download_link(output_file_name), unsafe_allow_html=True)
        else:
            st.error(f"Error: {error_or_file_path}")