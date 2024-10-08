import pandas as pd
import streamlit as st
from coldata import col_names, date_cols, str_cols, int_cols, float_cols
from datetime import datetime, time

def process_date_column(series):
    def process_value(value):
        if pd.isna(value):
            return ""
        try:
            return pd.to_datetime(value).strftime('%d/%m/%Y')
        except ValueError:
            return str(value)  # Keep original string if it's not a valid date
    
    return series.apply(process_value)

def process_date_column(series):
    def process_value(value):
        if pd.isna(value):
            return ""
        if isinstance(value, time):
            return value.strftime('%H:%M:%S')
        try:
            if isinstance(value, datetime):
                return value.strftime('%d/%m/%Y')
            return pd.to_datetime(value).strftime('%d/%m/%Y')
        except ValueError:
            return str(value)  # Keep original string if it's not a valid date
    
    return series.apply(process_value)

def load_excel_data(uploaded_file):
    try:
        # Create a dictionary of column data types
        dtypes = {col: 'object' for col in col_names}  # Start with all columns as 'object'
        for col in str_cols:
            dtypes[col] = str
        
        # Read the Excel file
        df = pd.read_excel(
            uploaded_file,
            header=None,
            skiprows=7,
            names=col_names,
            usecols=col_names,
            dtype=dtypes
        )
        
        # Process date columns
        for col in date_cols:
            df[col] = process_date_column(df[col])
        
        # Convert numeric columns to appropriate types
        for col in int_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        for col in float_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Ensure all specified columns are present
        missing_cols = set(col_names) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing columns in Excel file: {', '.join(missing_cols)}")
        
        df = df[col_names]
        
        # Drop specific columns
        df = df.drop(columns=['AU', 'AK', 'AP', 'BB'], errors='ignore')
        
        # Convert all remaining object columns to string
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str)
        
        # Convert any remaining numeric columns to string
        for col in df.select_dtypes(include=['float64', 'int64', 'Int64']):
            df[col] = df[col].astype(str)
        
        return df
    except ValueError as ve:
        st.error(f"Error in Excel file structure: {str(ve)}")
    except Exception as e:
        st.error(f"Failed to load Excel file: {str(e)}")
        st.error("Please check if the Excel file has the expected structure and column names.")
    return None

def search_users(df, search_term):
    return df[
        df['RegoNum'].astype(str).str.contains(search_term, case=False, na=False) |
        df['EmployeeNum'].astype(str).str.contains(search_term, case=False, na=False) |
        df['StudentLastName'].astype(str).str.contains(search_term, case=False, na=False) |
        df['StudentFirstName'].astype(str).str.contains(search_term, case=False, na=False)
    ]

def display_completion_rate(completion_rate):
    if pd.isna(completion_rate):
        st.warning("Completion rate is not available.")
        return
    
    completion_rate = float(completion_rate)
    display_percentage = completion_rate * 100 if completion_rate <= 1 else completion_rate

    color = "#4CAF50" if completion_rate == 1 else "#FFA500"
    st.markdown(f"""
    <div class="completion-rate-bar">
        <div style="width: {min(display_percentage, 100)}%; background-color: {color};">
            {display_percentage:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    if completion_rate < 1:
        st.warning("Warning: Completion rate is less than 100%.")
    else:
        st.success("Completion rate is 100%. Ready for final training plan.")

def display_user_profile(user_data):
    # Create a container for the profile
    profile_container = st.container()
    
    with profile_container:
        # Display user information
        st.subheader(f"{user_data['StudentFirstName']} {user_data['StudentLastName']}")
        st.write(f"**Registration Number:** {user_data['RegoNum']}")
        st.write(f"**Employee Number:** {int(user_data['EmployeeNum'])}")
        st.write(f"**Branch:** {user_data['BranchName']}")
