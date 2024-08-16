import streamlit as st
import requests
from io import BytesIO
from docxtpl import DocxTemplate
from zipfile import ZipFile, BadZipFile

def get_template_from_github(repo_owner, repo_name, file_path, branch='main'):
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Check if the content type is correct for a Word document
        if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' not in response.headers.get('Content-Type', ''):
            raise ValueError("Downloaded file is not a valid Word document")
        
        # Try to open the file as a zip (Word documents are zip files)
        try:
            ZipFile(BytesIO(response.content))
        except BadZipFile:
            raise ValueError("Downloaded file is not a valid Word document (not a zip file)")
        
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
