import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load the dataset
df = pd.read_csv(r'survey-app/dummydata2.csv', sep='\t')

# Title of the Streamlit app
st.title('Dummy Dashboard')

# Sidebar with filtering options
st.sidebar.title('Filters')

# Add filter widgets in the sidebar
apply_province_filter = st.sidebar.checkbox('Province')
if apply_province_filter:
    selected_province = st.sidebar.selectbox('Select Province', [''] + df['Provinsi'].unique())
else:
    selected_province = ''

apply_city_filter = st.sidebar.checkbox('City')
if apply_city_filter:
    selected_city = st.sidebar.selectbox('Select City', [''] + df['Kota_Kabupaten'].unique())
else:
    selected_city = ''

apply_education_filter = st.sidebar.checkbox('Education')
if apply_education_filter:
    selected_education = st.sidebar.selectbox('Select Education', [''] + df['Pendidikan'].unique())
else:
    selected_education = ''

apply_gender_filter = st.sidebar.checkbox('Gender')
if apply_gender_filter:
    selected_gender = st.sidebar.selectbox('Select Gender', [''] + df['Jenis_Kelamin'].unique())
else:
    selected_gender = ''

apply_party_filter = st.sidebar.checkbox('Party')
if apply_party_filter:
    selected_party = st.sidebar.selectbox('Select Party', [''] + df['Preferensi_Partai'].unique())
else:
    selected_party = ''

apply_profession_filter = st.sidebar.checkbox('Profession')
if apply_profession_filter:
    selected_profession = st.sidebar.selectbox('Select Profession', [''] + df['Profesi'].unique())
else:
    selected_profession = ''
    
# Apply filters to the DataFrame
filtered_df = df

# Apply the 'Province' filter if selected
if apply_province_filter and selected_province:
    filtered_df = filtered_df[filtered_df['Provinsi'] == selected_province]

# Apply the 'City' filter if selected
if apply_city_filter and selected_city:
    filtered_df = filtered_df[filtered_df['Kota_Kabupaten'] == selected_city]

# Apply the 'Education' filter if selected
if apply_education_filter and selected_education:
    filtered_df = filtered_df[filtered_df['Pendidikan'] == selected_education]

# Apply the 'Gender' filter if selected
if apply_gender_filter and selected_gender:
    filtered_df = filtered_df[filtered_df['Jenis_Kelamin'] == selected_gender]

# Show the filtered DataFrame if needed
st.subheader('Filtered Data')
st.write(filtered_df)

# Add a download button for the filtered data
st.download_button('Download Filtered Data as CSV', filtered_df.to_csv(index=False), key='download_filtered_data')

# Bar chart for Age Distribution
st.subheader('Age Distribution')
age_counts = filtered_df['Umur'].value_counts()
fig = px.bar(x=age_counts.index, y=age_counts.values, labels={'x': 'Age Distribution', 'y': 'Count'})
st.plotly_chart(fig)

# Countplot for Education Level using Plotly
st.subheader('Education Level Distribution')
education_counts = filtered_df['Pendidikan'].value_counts()
fig = px.bar(x=education_counts.index, y=education_counts.values, labels={'x': 'Education Level', 'y': 'Count'})
st.plotly_chart(fig)

# Top Important Issues Bar Chart
st.subheader('Issues')
top_issues_df = pd.concat([filtered_df['Isu_Penting1'], filtered_df['Isu_Penting2'], filtered_df['Isu_Penting3']], axis=1)
top_issues_counts = top_issues_df.apply(pd.Series.value_counts).sum(axis=1).sort_values(ascending=False).head(6)
fig_top_issues = px.bar(x=top_issues_counts.index, y=top_issues_counts.values, labels={'x': 'Issue', 'y': 'Count'})
st.plotly_chart(fig_top_issues)

# Party Affiliation Pie Chart
st.subheader('Party Affiliation Distribution')
party_affiliation_counts = filtered_df['Afiliasi_Partai'].value_counts()

# Define a blue gradient color scale
blue_gradient = px.colors.sequential.dense

fig_party_affiliation = px.bar(party_affiliation_counts, x=party_affiliation_counts.index, y=party_affiliation_counts.values,
                               color=party_affiliation_counts.index, color_discrete_sequence=blue_gradient)

st.plotly_chart(fig_party_affiliation)

# Bar chart for Profession Distribution
st.subheader('Profession')
profession_counts = filtered_df['Profesi'].value_counts()
st.bar_chart(profession_counts)

# Political Ideology Pie Chart
st.subheader('Political Ideology Distribution')
political_ideology_counts = filtered_df['Ideologi_Politik'].value_counts()

# Define a blue gradient color scale
blue_gradient = px.colors.sequential.dense

# Create a stacked horizontal bar chart
fig_political_ideology = px.bar(political_ideology_counts, x=political_ideology_counts.values, y=political_ideology_counts.index,
                                 color=political_ideology_counts.index, color_discrete_sequence=blue_gradient,
                                 orientation='h')  # Set the orientation to horizontal

st.plotly_chart(fig_political_ideology)

# Bar Chart for Media Source
st.subheader('Media Source Distribution')
media_source_counts = filtered_df['Sumber_Media'].value_counts()
fig_media_source = px.bar(x=media_source_counts.index, y=media_source_counts.values,
                           labels={'x': 'Media Source', 'y': 'Count'})
st.plotly_chart(fig_media_source)

# Bar Chart for Balanced Reporting
st.subheader('Balanced Reporting Distribution')
balanced_reporting_counts = filtered_df['Pemberitaan_Berimbang'].value_counts()
fig_balanced_reporting = px.bar(x=balanced_reporting_counts.index, y=balanced_reporting_counts.values,
                                 labels={'x': 'Balanced Reporting', 'y': 'Count'})
st.plotly_chart(fig_balanced_reporting)

# Bar Chart for Electoral Integrity
st.subheader('Electoral Integrity Distribution')
electoral_integrity_counts = filtered_df['Integritas_Pemilu'].value_counts()
fig_electoral_integrity = px.bar(x=electoral_integrity_counts.index, y=electoral_integrity_counts.values,
                                 labels={'x': 'Electoral Integrity', 'y': 'Count'})
st.plotly_chart(fig_electoral_integrity)

# Histogram for Likelihood to Vote
st.subheader('Likelihood to Vote Distribution')
fig = px.histogram(filtered_df, x='Kemungkinan_Menggunakan_Hak_Pilih', nbins=10,
                   labels={'Kemungkinan_Menggunakan_Hak_Pilih': 'Likelihood to Vote', 'count': 'Count'},
                   histnorm='percent')
fig.update_traces(marker_line=dict(width=3, color='black'))
st.plotly_chart(fig)

# Plot for Likelihood to Vote vs. Electoral Integrity
st.subheader('Likelihood to Vote vs. Electoral Integrity Distribution')
box_fig = px.box(filtered_df, x='Kemungkinan_Menggunakan_Hak_Pilih', y='Integritas_Pemilu',
                 labels={'Kemungkinan_Menggunakan_Hak_Pilih': 'Likelihood to Vote',
                         'Integritas_Pemilu': 'Electoral Integrity'})
box_fig.update_layout()
st.plotly_chart(box_fig)    

# Bar Chart for Party Preference
st.subheader('Party Preference')
party_preference_counts = filtered_df['Preferensi_Partai'].value_counts()

# Sort party_preference_counts by value in descending order
party_preference_counts = party_preference_counts.sort_values(ascending=True)

# Create a horizontal bar chart
fig_party_preference = go.Figure(data=[go.Bar(
    y=party_preference_counts.index,  # Use 'y' to set the labels on the y-axis
    x=party_preference_counts.values,  # Use 'x' to set the values on the x-axis
    orientation='h'  # Set orientation to 'h' for horizontal bars
)])

fig_party_preference.update_layout(
    title='Party Preference (Sorted by Count)',
    xaxis_title='Count',
    yaxis_title='Party Preference'
)

st.plotly_chart(fig_party_preference)

# Footer
st.sidebar.text('Created with Streamlit')
