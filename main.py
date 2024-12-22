import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor

# Load data
data_path = "C:/Users/rites/Downloads/Rape Violation In INDIA.unknown"
df = preprocessor.load_data(data_path)

# Title for dashboard
st.title("Rape Violation Data Dashboard")

# Sidebar for filters
st.sidebar.title("Filters")

# Filters
select_year = preprocessor.multiselect("Select Year", df["YEAR"].unique())
select_state = preprocessor.multiselect("Select State", df["State"].unique())
select_pie_year = st.sidebar.selectbox('Select Year for Pie Chart', df['YEAR'].unique())

filtered_df = df[(df["YEAR"].isin(select_year)) & (df["State"].isin(select_state))]

# Aggregate data to avoid duplicate entries
aggregated_df = filtered_df.groupby(['YEAR', 'State']).sum().reset_index()

# KPI - Key Performance Indicator
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Known Cases", value=int(filtered_df["No. Of Cases In Which Offenders Were Known To The Victims"].sum()))

with col2:
    st.metric(label="Total Parents/C. Family Members Cases", value=int(filtered_df["No. Of Cases In Which Offenders Were Parents / Close Family Members"].sum()))

with col3:
    st.metric(label="Total Relatives Cases", value=int(filtered_df["No. Of Cases In Which Offenders Were Relatives"].sum()))

with col4:
    st.metric(label="Total Neighbours Cases", value=int(filtered_df["No. Of Cases In Which Offenders Were Neighbours"].sum()))

# Visualization 1: Total Cases Over Years
st.write("### Total Cases Over Years")
st.line_chart(aggregated_df.pivot(index='YEAR', columns='State', values='No. Of Cases In Which Offenders Were Known To The Victims'))

# Visualization in two columns

st.write("### Cases By Offender Type")
fig, ax = plt.subplots(figsize =(12,8))
sns.barplot(data=filtered_df.melt(id_vars=['State', 'YEAR'], value_vars=[
        'No. Of Cases In Which Offenders Were Parents / Close Family Members',
        'No. Of Cases In Which Offenders Were Relatives',
        'No. Of Cases In Which Offenders Were Neighbours',
        'No. Of Cases In Which Offenders Were Other Known Persons'
]), x='value', y='variable', hue='State', ax=ax)
ax.set_xlabel("Number of Cases")
ax.set_ylabel("Offender Type")
st.pyplot(fig)

# Visualization of Cases By States
st.write("### Cases By State")
fig, ax = plt.subplots(figsize =(12,8))
sns.barplot(data=filtered_df, x='State', y='No. Of Cases In Which Offenders Were Known To The Victims', hue='YEAR', ax=ax)
ax.set_xlabel("State")
ax.set_ylabel("Number of Cases")
st.pyplot(fig)


# Heatmap for offenders Types 
st.write("### Heatmap of Offender Types")
heatmap_data = filtered_df.groupby(['State', 'YEAR']).sum().reset_index()
heatmap_data = heatmap_data.melt(id_vars=['State', 'YEAR'], value_vars=[
        'No. Of Cases In Which Offenders Were Parents / Close Family Members',
        'No. Of Cases In Which Offenders Were Relatives',
        'No. Of Cases In Which Offenders Were Neighbours',
        'No. Of Cases In Which Offenders Were Other Known Persons'
])
heatmap_data_pivot = heatmap_data.pivot_table(index="variable", columns="State", values="value", aggfunc='sum')
fig, ax = plt.subplots(figsize =(12,8))
sns.heatmap(heatmap_data_pivot, cmap="YlGnBu",annot =True, ax=ax)
st.pyplot(fig)


# Visualization in Pie -Chart 
st.write("### Pie Chart for Offender Types in a Specific Year")
df_pie_year = df[df['YEAR'] == select_pie_year].melt(id_vars=['State'], value_vars=[
        'No. Of Cases In Which Offenders Were Parents / Close Family Members',
        'No. Of Cases In Which Offenders Were Relatives',
        'No. Of Cases In Which Offenders Were Neighbours',
        'No. Of Cases In Which Offenders Were Other Known Persons'
])
pie_data = df_pie_year.groupby('variable').sum().reset_index()
fig, ax = plt.subplots(figsize =(12,8))
ax.pie(pie_data['value'], labels=pie_data['variable'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
ax.axis('equal')
st.pyplot(fig)

# Insights
st.write("### Insights")
st.write("""
- The number of cases in which offenders were known to the victims has generally increased over the years.
- The highest number of cases involve other known persons as the offenders.
- There are significant variations in crime data across different states.
- Visualization helps in identifying patterns and trends, making it easier to target specific areas for intervention.
""")
