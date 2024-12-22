import pandas as pd
import streamlit as st

def multiselect(title, option_list):
    selected = st.sidebar.multiselect(title, option_list)
    select_all = st.sidebar.checkbox("Select all", value=True, key=title)
    if select_all:
        selected_options = option_list
    else:
        selected_options = selected
    return selected_options

# Offender statistics
def fetch_offender_statistics(df):
    offender_types = [
        'No. Of Cases In Which Offenders Were Known To The Victims',
        'No. Of Cases In Which Offenders Were Parents / Close Family Members',
        'No. Of Cases In Which Offenders Were Relatives',
        'No. Of Cases In Which Offenders Were Neighbours',
        'No. Of Cases In Which Offenders Were Other Known Persons'
    ]
    
    offender_stats = df[offender_types].sum().reset_index()
    offender_stats.columns = ['Offender Type', 'Count']
    return offender_stats

# Top states by cases
def fetch_top_states_by_cases(df):
    state_cases = df.groupby("State")['No. Of Cases In Which Offenders Were Known To The Victims'].sum().reset_index().sort_values(by='No. Of Cases In Which Offenders Were Known To The Victims', ascending=False)
    return state_cases

# Load data from a CSV file
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

