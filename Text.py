import streamlit as st
import requests
import cv2

# Function to call the ocr.space API
def extract_text_from_image(image, api_key):
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={'image': image},
        data={'apikey': api_key}
    )
    result = response.json()
    return result['ParsedResults'][0]['ParsedText']

# Streamlit app
def main():
    st.title("OCR Text Extraction")
    st.write("Upload an image to extract text from it.")

    # API Key input
    api_key ="K81821207288957"

    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    st.write("Or click a photo with your webcam:")

    if st.button("Open Camera and Capture Image"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cap.release()
            st.image(frame, channels="BGR")
            if st.button("Extract Text from Captured Image"):
                _, encoded_image = cv2.imencode('.jpg', frame)
                text = extract_text_from_image(encoded_image.tobytes(), api_key)
                st.write("Extracted Text:")
                st.text_area("Text", text, height=200)
        else:
            st.error("Failed to capture image")
            
    if uploaded_file and api_key:
        # Extract text from the uploaded image
        text = extract_text_from_image(uploaded_file, api_key)
        st.write("Extracted Text:")
        st.text_area("Text", text, height=200)

if __name__ == "__main__":
    main()
