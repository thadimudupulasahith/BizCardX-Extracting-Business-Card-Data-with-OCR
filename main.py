import streamlit as st
from m2 import upload_database, extracted_data, show_database

# Setting page configuration in Streamlit
st.set_page_config(page_title='Bizcardx Extraction', layout="wide")

# Displaying title and balloons animation
st.balloons()
st.title(':violet[Bizcardx Data Extraction]')

# Creating tabs for data extraction and database side
data_extraction, database_side = st.tabs(['Data uploading and Viewing', 'Database side'])
file_name = 'thiru'

with data_extraction:
    # Uploading file to Streamlit app
    uploaded = st.file_uploader('Choose an image file')

    if uploaded is not None:
        with open(f'{file_name}.png', 'wb') as f:
            f.write(uploaded.getvalue())

        # Extracting data from image (Image view)
        st.subheader(':violet[Image view of Data]')
        if st.button('Extract Data from Image'):
            extracted = extracted_data(f'{file_name}.png')
            st.image(extracted)

        # Uploading data to the database
        st.subheader(':violet[Upload extracted to Database]')
        if st.button('Upload data'):
            upload_database(f'{file_name}.png')
            st.success('Data uploaded to Database successfully!', icon="✅")

# Getting data from the database and storing it in the 'df' variable
df = show_database()

with database_side:
    st.title(':violet[All Data in Database]')

    # Showing all data from the database
    if st.button('Show All'):
        st.dataframe(df)

    # Searching data in the database by column
    st.subheader(':violet[Search Data by Column]')
    column = str(st.radio('Select column to search', ('Name', 'Designation', 'Company_name', 'Address', 'Contact_number', 'Mail_id', 'Website_link'), horizontal=True))
    value = str(st.selectbox('Please select value to search', df[column]))

    if st.button('Search Data'):
        st.dataframe(df[df[column] == value])
