import streamlit as st
import requests
import os
import pandas as pd
from io import BytesIO
from docxtpl import DocxTemplate
from zipfile import ZipFile, BadZipFile

def get_template_from_github(repo_owner, repo_name, file_path, branch='main'):
    url = f"https://github.com/{repo_owner}/{repo_name}/raw/{branch}/{file_path}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        content_length = response.headers.get('Content-Length', 'Unknown')
        
        # Check file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension != '.docx':
            raise ValueError(f"File does not have .docx extension. Extension: {file_extension}")
        
        # Accept both specific Word document type and generic binary type
        valid_types = [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/octet-stream'
        ]
        if content_type not in valid_types:
            raise ValueError(f"Unexpected content type. Got: {content_type}, Expected one of: {', '.join(valid_types)}")
        
        if int(content_length) < 1000:  # Arbitrary small size, adjust as needed
            raise ValueError(f"Downloaded file is too small to be a valid Word document. Size: {content_length} bytes")
        
        return BytesIO(response.content)
    except requests.RequestException as e:
        st.error(f"Failed to download template from GitHub: {str(e)}")
        return None
    except ValueError as e:
        st.error(str(e))
        return None

def generate_training_plan(user_data, template_file):
    try:
        doc = DocxTemplate(template_file)
    except Exception as e:
        st.error(f"Error processing template file: {str(e)}")
        return None
    
    context = user_data.to_dict()
    
    # Ensure all values are strings to avoid issues with nan
    for key, value in context.items():
        if pd.isna(value):
            context[key] = ""
        else:
            context[key] = str(value)
    
    try:
        doc.render(context)
    except Exception as e:
        st.error(f"Error generating document: {str(e)}")
        return None
    
    output = BytesIO()
    try:
        doc.save(output)
    except Exception as e:
        st.error(f"Error saving document: {str(e)}")
        return None
    
    output.seek(0)
    return output