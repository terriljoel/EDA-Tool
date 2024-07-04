import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pydantic_settings import BaseSettings
# from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def home():
    st.set_page_config(page_title="EDA Tool",
    page_icon ="📈")
    st.title("Welcome to the EDA Tool")

    st.write("""
    ### An exploratory analysis tool that provides various summaries and visualizations on the uploaded data.
             

## Features
### Basic Exploratory Analysis
- Viewing the raw, head, tail and datatypes of the data
- Displaying the summary statistics
- Showing the unique and missing values in the data
- Handling missing values 

### Data Visualizations
- Relational plots (scatter, line)
- Categorical plots (strip, swarm, box, violin, boxen, point, bar)
- Count plots
- Distribution plots
- Scatter plot
- Correlation heatmaps
- Pair plots
### Pandas Profiling
    """)

    # Developer Information
    st.header("About the Developers")
    st.write("""
    This EDA tool was developed by:
- *Ansh Kapoor*: [GitHub Profile](https://github.com/AnshKapoor)
- *Hitesh Bhardwaj*: [GitHub Profile](https://github.com/)
- *Hafiz M Usman Hameed Khan*: [GitHub Profile](https://github.com/)
- *Terril Joel Nazareth*: [GitHub Profile](https://github.com/terriljoel/)

Click the button below to navigate to the EDA tool.
    """)


#     st.write(""" 
#             Developed By 
# - *Ansh Kapoor*   
# - *Hitesh Bhardwaj*     
# - *Hafiz M Usman Hameed Khan*   
# - *Terril Joel Nazareth*


# ### An exploratory analysis tool that provides various summaries and visualizations on the uploaded data.
             

# ## Features
# ### Basic Exploratory Analysis
# - Viewing the raw, head, tail and datatypes of the data
# - Displaying the summary statistics
# - Showing the unique and missing values in the data
# - Handling missing values 

# ### Data Visualizations
# - Relational plots (scatter, line)
# - Categorical plots (strip, swarm, box, violin, boxen, point, bar)
# - Count plots
# - Distribution plots
# - Scatter plot
# - Correlation heatmaps
# - Pair plots
# ### Pandas Profiling
        
# Click the button below to navigate to the EDA tool.
#                """)
    if st.button('Go to EDA Tool'):
        st.session_state.page = 'eda'
        st.rerun() 

def eda():
# Page layout
    st.set_page_config(page_title="EDA Tool",
    initial_sidebar_state="expanded",
    page_icon ="📈")
    # st.set_option("deprecation.showPyplotGlobalUse", False)

# Main title
    st.header("Python Lab Project")
    if st.sidebar.button('Back'):
        st.session_state.page = 'home'
        st.rerun() 
    st.title("Exploratory Data Analysis Tool 📈")
    # st.sidebar.title("Exploratory Data Analysis (EDA) Tool 📈")
    # st.sidebar.markdown("## Upload a CSV file to get started")
    # App description
    # st.markdown("### An exploratory analysis tool that provides various summaries and visualizations on the uploaded data.")

    # Upload file
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type="csv")

    st.info("Upload a CSV file to get started")
    if uploaded_file is not None:
        st.success("File sucessfully uploaded!")
        df = pd.read_csv(uploaded_file)
        numerical_col = df.select_dtypes(include=np.number).columns.tolist()
        categorical_col = df.drop(numerical_col, axis=1).columns

        # categorical_col = df.select_dtypes(include=['object', 'category']).columns.tolist()
        # st.info(numerical_col)
        # st.info(categorical_col)
        # Show raw data
        if st.sidebar.checkbox("Show raw data", False):
            st.write(df)

        activity_list = ["Basic Exploratory Analysis", "Data Visualizations", "Pandas Profiling"]
        activity = st.sidebar.selectbox("Choose activity", activity_list)

        if activity == "Basic Exploratory Analysis":
            # Show head
            if st.sidebar.checkbox("Head", key="head"):
                st.subheader("DataFrame's Head")
                st.write(df.head())

            # Show tail
            if st.sidebar.checkbox("Tail", key="tail"):
                st.subheader("DataFrame's Tail")
                st.write(df.tail())

            # Show description
            if st.sidebar.checkbox("Describe", key="desc"):
                st.subheader("Data Description")
                st.write(df.describe())

             # # Show unique values
            if st.sidebar.checkbox("Unique Values", key="unique"):
                col = st.sidebar.selectbox("Choose a column", df.columns)
                st.subheader(f"{col}'s Unique Values")
                st.write(df[col].value_counts())

             # Show data types
            if st.sidebar.checkbox("Data types", key="datatype"):
                st.subheader("DataFrame's datatypes")
                data_types = df.dtypes.apply(lambda x: x.name).to_frame(name='Data Type').reset_index()
                data_types.columns = ['Column', 'Data Type']
                st.write(data_types)
            # Show missing values
            if st.sidebar.checkbox("Missing Values", key="mv"):
                st.subheader("DataFrame's Missing Values")
                missing_values = df.isnull().sum()
                missing_values_df = missing_values.reset_index()
                missing_values_df.columns = ['ColumnName', 'Count']
                missing_values_df=missing_values_df[missing_values_df['Count']>0]
                if missing_values_df.empty:
                    st.info('There are no missing values')
                else:
                    # st.dataframe(missing_values_df)
                    # st.dataframe(missing_values_df.set_index(df.columns[0]))
                    st.write(missing_values_df)
                    if st.sidebar.checkbox("Handle Missing Values"):
                        st.sidebar.info('Choose columns')
                        for col in missing_values_df.ColumnName:
                            if st.sidebar.checkbox(col):
                                # print('hello')
                                # if col in df.select_dtypes(include=['number']).columns:
                                method = st.sidebar.radio("Fill or Drop?", ["Fill", "Drop"])
                                if method == "Fill":
                                    detailed_output = []
                                    # fill_value = st.sidebar.text_input("Fill value or method (mean/median)", "mean")
                                    
                                    fill_value = st.sidebar.selectbox("Choose a method",["None","mean", "median","custom value"]) if col in numerical_col else st.sidebar.selectbox("Choose a method",["None","custom value"])
                                   

                                    if fill_value in ["mean", "median"]:
                                        fill_values = round(df.loc[:, col].mean(),2) if fill_value == "mean" else round(df.loc[:, col].median(),2)
                                        # for col in df.columns:
                                        # if col in fill_values:
                                        missing_indices = df[df[col].isna()].index
                                        for i in missing_indices:
                                            detailed_output.append(f"The missing value at index {i} in column '{col}' was replaced with {fill_values}.")
                                        df[col] = df[col].fillna(fill_values)
                                        st.write(df)
                                        
                                    elif fill_value=="custom value":
                                        value=""
                                        value=st.sidebar.text_input("Custom Value")
                                        if value:
                                            # for col in df.columns:
                                            missing_indices = df[df[col].isna()].index
                                            for i in missing_indices:
                                                detailed_output.append(f"The missing value at index {i} in column '{col}' was replaced with '{value}'.")
                                            df = df.fillna(value)
                                            st.write(df)
                                    for message in detailed_output:
                                        st.text(message)
                                    download(df)
                                else:
                                    missing_indices = df[df.isna().any(axis=1)].index
                                    detailed_output = []
                                    for i in missing_indices:
                                        detailed_output.append(f"Row at index {i} with missing values was dropped.")
                                    df = df.dropna(subset=[col])
                                    st.write(df)
                                    for message in detailed_output:
                                        st.text(message)
                                    download(df)
                                    

        elif activity == "Data Visualizations":
            st.set_option('deprecation.showPyplotGlobalUse', False)
            # Relation plot
            if st.sidebar.checkbox("Relational Plot", key="rel"):
                st.subheader("Relational Plot")
                if len(numerical_col) > 1:
                    x = st.sidebar.selectbox("Choose a column", numerical_col)
                    del numerical_col[numerical_col.index(x)]
                    y = st.sidebar.selectbox("Choose another column", numerical_col)
                    kind = st.sidebar.radio("Kind", ["scatter", "line"])
                    hue = st.sidebar.selectbox("Hue (Optional)", categorical_col.insert(0, None),key="rel_1")
                    fig, ax = plt.subplots()    
                    sns.relplot(x=x, y=y, data=df, kind=kind, hue=hue)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Categorical plot
            if st.sidebar.checkbox("Categorical Plot", key="cat"):
                if (len(numerical_col) and len(categorical_col)) > 1:
                    x = st.sidebar.selectbox("Choose a column", categorical_col, key="cat_1")
                    y = st.sidebar.selectbox("Choose another column", numerical_col, key="cat_2")
                    kind_list = ["strip", "swarm", "box", "violin", "boxen", "point", "bar"]
                    kind = st.sidebar.selectbox("Kind", kind_list, key="cat_3")
                    st.subheader(f"{kind.capitalize()} Plot")
                    hue = st.sidebar.selectbox("Hue (Optional)", categorical_col.insert(0, None), key="cat_4")
                    sns.catplot(x=x, y=y, data=df, kind=kind, hue=hue)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Count plot
            if st.sidebar.checkbox("Count Plot", False, key="count"):
                if len(categorical_col) > 1:
                    col = st.sidebar.selectbox("Choose a column", categorical_col, key="count_1")
                    st.subheader(f"{col}'s Count Plot")
                    sns.countplot(x=col, data=df)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Distribution plot
            if st.sidebar.checkbox("Distribution Plot", False, key="dist"):
                if len(numerical_col) > 1:
                    col = st.sidebar.selectbox("Choose a column", numerical_col,  key="dist_1")
                    st.subheader(f"{col}'s Distribution Plot")
                    sns.histplot(df[col],kde=True)
                    plt.grid(True)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Heatmap
            if st.sidebar.checkbox("Correlation Heatmap", False, key="heatmap"):
                st.subheader(f"Correlation Heatmap")
                sns.heatmap(df[numerical_col].corr(), annot=True)
                st.pyplot()

            
            # Pairplot
            if st.sidebar.checkbox("Pairplot", False, key="pairplot"):
                st.subheader(f"Pairplot")
                hue = st.sidebar.selectbox("Hue (Optional)", categorical_col,key="Pairplot_1")
                sns.pairplot(df, hue=hue,diag_kind='kde')
                st.pyplot()
        elif activity == "Pandas Profiling":
            pr = ProfileReport(df, explorative=True)
            st_profile_report(pr)

def download(df):
    csv=df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )

# Main function to control the app flow
def main():
    st.logo("cd-basis-siegel.png",)
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'eda':
        eda()

if __name__ == "__main__":
    main()
