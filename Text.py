import streamlit as st
from PIL import Image
import pytesseract

# Streamlit app title
st.title("Text Extraction from Image")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Extract text from image
    text = pytesseract.image_to_string(image)
    
    # Display extracted text
    st.subheader("Extracted Text")
    st.text(text)
  
