import streamlit as st
import easyocr
import mysql.connector
import pandas as pd
from PIL import Image

# Create a MySQL database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='GItamsai123$',
    database='bizcardx_db'
)
cursor = conn.cursor()

# Create a table to store business card information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS business_cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255),
        card_holder_name VARCHAR(255),
        designation VARCHAR(255),
        mobile_number VARCHAR(255),
        email VARCHAR(255),
        website VARCHAR(255),
        area VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        pin_code VARCHAR(255),
        image LONGBLOB
    )
''')
conn.commit()

# Create a function to insert business card data into the database
def insert_data(data, image):
    cursor.execute('''
        INSERT INTO business_cards (company_name, card_holder_name, designation, mobile_number, email, website, area, city, state, pin_code, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', data + (image,))
    conn.commit()

# Create a function to retrieve business card data from the database
def get_data():
    cursor.execute('SELECT * FROM business_cards')
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=[column[0] for column in cursor.description])
    return df

# Create a Streamlit application
def main():
    st.title("Business Card OCR")

    # File uploader for business card image
    uploaded_file = st.file_uploader("Upload a business card image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Business Card", use_column_width=True)

        # Extract text using easyOCR
        reader = easyocr.Reader(['en'])
        extracted_text = reader.readtext(image)

        # Extract relevant information from the extracted text
        data = {}
        for item in extracted_text:
            if 'company' in item[1].lower():
                data['company_name'] = item[0]
            elif 'name' in item[1].lower():
                data['card_holder_name'] = item[0]
            elif 'designation' in item[1].lower():
                data['designation'] = item[0]
            elif 'mobile' in item[1].lower():
                data['mobile_number'] = item[0]
            elif 'email' in item[1].lower():
                data['email'] = item[0]
            elif 'website' in item[1].lower():
                data['website'] = item[0]
            elif 'area' in item[1].lower():
                data['area'] = item[0]
            elif 'city' in item[1].lower():
                data['city'] = item[0]
            elif 'state' in item[1].lower():
                data['state'] = item[0]
            elif 'pin code' in item[1].lower():
                data['pin_code'] = item[0]

        # Display the extracted information
        st.subheader("Extracted Information:")
        for key, value in data.items():
            st.write(f"{key.capitalize()}: {value}")

        # Save the extracted information and image to the database
        if st.button("Save"):
            # Convert the image to binary
            image_binary = uploaded_file.read()

            # Insert the data into the database
            insert_data(tuple(data.values()), image_binary)

            st.success("Business card information saved successfully.")

    # Display the database records
    df = get_data()
    st.subheader("Saved Business Card Information:")
    st.dataframe(df)

if __name__ == '__main__':
    main()
