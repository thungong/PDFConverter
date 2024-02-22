import streamlit as st
import pandas as pd
import tabula
from pdf2docx import Converter
import os
import tempfile
import shutil

# Version control
VERSION = "1.2.29"

# Contact information for the sidebar
CONTACT_INFO = """
**Contact Information:**

- Email: [mailme:aeytato@thatwhy.me] (aeytato@thatwhy.me)
- Website: [https://apps.thatwhy.me](https://apps.thatwhy.me)
"""

def convert_pdf_to_csv(pdf_file):
    # Use tabula library to extract tables from PDF and convert to DataFrame
    tables = tabula.read_pdf(pdf_file, pages="all", multiple_tables=True)
    # Concatenate all tables into a single DataFrame
    df = pd.concat(tables)
    return df

def convert_pdf_to_docx(pdf_file, output_docx):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Save the uploaded PDF file to the temporary directory
        temp_pdf_file = os.path.join(temp_dir, "uploaded_file.pdf")
        with open(temp_pdf_file, "wb") as f:
            f.write(pdf_file.read())

        # Use pdf2docx library to convert PDF to Word document
        cv = Converter(temp_pdf_file)
        cv.convert(output_docx)
        cv.close()

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

def main():
    st.sidebar.title("Aey Converter Tools")
    st.sidebar.markdown(f"Version: {VERSION}")
    st.sidebar.markdown(CONTACT_INFO)

    uploaded_file = st.file_uploader("Upload File for Conversion", type=["pdf"])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        st.write("Select conversion type:")
        conversion_type = st.radio("", ("CSV", "Word"))

        if st.button("Convert"):
            st.write(f"Converting {uploaded_file.name} to {conversion_type}...")

            try:
                if conversion_type == "CSV":
                    # Convert PDF to CSV
                    df = convert_pdf_to_csv(uploaded_file)
                    st.write("Conversion to CSV successful!")
                    st.write("Preview of CSV:")
                    st.write(df.head())

                    # Download CSV
                    csv_file = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_file,
                        file_name="converted_data.csv",
                        mime="text/csv"
                    )
                elif conversion_type == "Word":
                    # Convert PDF to Word document
                    output_docx = "converted_data.docx"
                    convert_pdf_to_docx(uploaded_file, output_docx)
                    st.write("Conversion to Word document successful!")

                    # Download Word document
                    st.download_button(
                        label="Download Word Document",
                        data=output_docx,
                        file_name=output_docx,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
