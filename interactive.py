import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import statsmodels.api as sm
# Load the dataset
data = pd.read_csv('data_revised.csv')

# App Title and Description
st.title("Interactive Data")
st.write("Explore patterns in the data ")


# Sidebar Filters
st.sidebar.header("Filter")   #give a title for the sidebar menu


# Sidebar Filters for Numerical Variables

experience_range = st.sidebar.slider("Experience (years)", int(data['experience'].min()), int(data['experience'].max()), (8, 20))
whrswk_range = st.sidebar.slider("Work Hours per Week", int(data['whrswk'].min()), int(data['whrswk'].max()), (5, 60))
# create a slider, and tentatively show a range from 5 to 35



# Sidebar Filters for Categorical Variables
region = st.sidebar.multiselect("Region", options=data['region'].unique(), default=data['region'].unique())
hispanic = st.sidebar.multiselect("Hispanic", options=data['hispanic'].unique(), default="no")
career = st.sidebar.multiselect("Career Stage", options=data['career_stage'].unique(), default=data['career_stage'].unique())




# Filter data based on selections
filtered_data = data[
    (data['experience'].between(*experience_range)) &
    (data['whrswk'].between(*whrswk_range)) &
    (data['region'].isin(region)) &
    (data['hispanic'].isin(hispanic)&
    (data['career_stage'].isin(career)))
]



# .between(*experience_range): checks whether each value in the experience column falls within the range
# experience_range  is a tuple
# * operator unpacks the tuple
# & acts as an AND operator




# Show filtered data if user selects the option
if st.sidebar.checkbox("Show Filtered Data"):
    st.write(filtered_data)

# st.sidebar places the checkbox in the sidebar section of the Streamlit app.
# checkbox("Show Filtered Data") creates a checkbox with the label "Show Filtered Data"
# st.write(filtered_data):



## Add a histogram
# Section: Distribution of Hours Worked per Week
st.header("Distribution of Hours Worked per Week")
st.write("This histogram shows the distribution of hours worked per week in the filtered data.")



# Plot histogram
fig, ax = plt.subplots()
sns.histplot(filtered_data['whrswk'], bins=20, color='skyblue', kde=False, ax=ax)
ax.set_title("Histogram of Hours Worked per Week")
ax.set_xlabel("Hours Worked per Week")
ax.set_ylabel("Frequency")
st.pyplot(fig)


# Adding a Scatter Plot
# Section: Scatter Plot - Experience vs. Hours Worked per Week
st.header("Scatter Plot: Experience  vs. Hours Worked per Week")
st.write("Check the box below to add a trendline to the scatter plot.")
show_trendline = st.checkbox("Show Trendline", value=False)

fig = px.scatter(filtered_data, x='experience', y='whrswk', title="Experience vs. Work Hours",
                 labels={"experience": "Experience (years)", "whrswk": "Hours Worked per Week"},
                 trendline="ols" if show_trendline else None)
st.plotly_chart(fig)






## Add a correlation matrix

# Section: Correlation Matrix
st.header("Correlation Matrix")
st.write("Check the box to view the correlation matrix for numerical variables.")

continuous_vars = ['whrswk', 'experience','kidslt6','kids618','husby', 'adjusted_experience', 
                   'experience_education', 'family_responsibility_index', 
                  'experience_squared','education_level']

# Show correlation matrix
if st.checkbox("Show Correlation Matrix"):
    corr_matrix = filtered_data[continuous_vars].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
