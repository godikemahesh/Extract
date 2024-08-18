import streamlit as st
import requests
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np

# Function to call the ocr.space API
def extract_text_from_image(image, api_key):
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={'image': image},
        data={'apikey': api_key}
    )
    result = response.json()
    return result['ParsedResults'][0]['ParsedText']

# Video transformer for webcam capture
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.image = None

    def transform(self, frame):
        self.image = frame.to_ndarray(format="bgr24")
        return frame

    def get_image(self):
        return self.image

# Streamlit app
def main():
    st.title("OCR Text Extraction")
    st.write("Upload an image or use your webcam to capture and extract text.")

    # API Key input
    api_key = "K81821207288957"

    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Webcam capture
    st.write("Or click a photo with your webcam:")
    webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

    if st.button("Capture Image"):
        if webrtc_ctx.video_transformer and webrtc_ctx.video_transformer.get_image() is not None:
            image = webrtc_ctx.video_transformer.get_image()
            st.image(image, channels="BGR")
            if st.button("Extract Text from Captured Image"):
                _, encoded_image = cv2.imencode('.jpg', image)
                text = extract_text_from_image(encoded_image.tobytes(), api_key)
                st.write("Extracted Text:")
                st.text_area("Text", text, height=200)
        else:
            st.error("Failed to capture image")

    if uploaded_file and api_key:
        text = extract_text_from_image(uploaded_file, api_key)
        st.write("Extracted Text:")
        st.text_area("Text", text, height=200)


if __name__ == "__main__":
    main()
