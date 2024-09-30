import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st
import re

# Set the path to Tesseract on your Windows machine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to preprocess and extract text from an image
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)

        # Optional: Enhance the image for better OCR results
        image = image.convert('L')  # Convert to grayscale
        image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image

        # Perform OCR with English and Hindi languages
        extracted_text = pytesseract.image_to_string(image, lang='eng+hin')
        return extracted_text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit Web Application
st.title("OCR and Document Search Web Application")

# Upload an image file (JPEG, PNG)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        # Save the uploaded image temporarily to disk
        with open("uploaded_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text from the uploaded image
        extracted_text = extract_text_from_image("uploaded_image.jpg")

        # Display the extracted text
        st.write("### Extracted Text:")
        st.write(extracted_text)

        # Keyword search functionality
        search_query = st.text_input("Enter a keyword to search in the extracted text:")

        if search_query:
            # Convert both extracted text and search query to lowercase for case-insensitive search
            if search_query.lower() in extracted_text.lower():
                st.success(f"Keyword '{search_query}' found!")

                # Highlight the found keyword in the extracted text (case-insensitive)
                # Using Markdown formatting for simple highlighting (bold)
                highlighted_text = extracted_text.replace(
                    search_query, f"**{search_query}**", flags=re.IGNORECASE
                )
                st.markdown(highlighted_text)
            else:
                st.warning(f"Keyword '{search_query}' not found in the extracted text.")

    except Exception as e:
        st.error(f"Failed to process the image. Error: {str(e)}")
