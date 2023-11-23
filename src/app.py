import streamlit as st
from PIL import Image
import cv2
import numpy as np
import zipfile
import os
import time


def detect_blur_spot(image, threshold=100):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Laplacian filter for edge detection
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Calculate maximum intensity and variance
    laplacian_variance = laplacian.var()

    # Initialize result variables
    blur_text = "Normal"
    text_color = (0, 255, 0)

    # Check blur condition based on variance of Laplacian image
    if laplacian_variance < threshold:
        blur_text = "Blurry"
        text_color = (255, 0, 0)
    # Add labels to the image
    cv2.putText(image, "{}: {:.2f}".format(blur_text, laplacian_variance), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                text_color, 3)

    return image


def detect_blur(upload_path, col1, col2, threshold):
    # Update an original image
    with col1:
        image = Image.open(upload_path)
        col1.write("Original Image :camera:")
        st.image(upload_path, caption="Uploaded Image", use_column_width=True)

    # Detect blur and confidence
    with col2:
        img_array = np.array(image)
        detected_image = detect_blur_spot(img_array, threshold)
        col2.write("Blur Detector :male-detective:")
        st.image(detected_image, caption="Processed Image", use_column_width=True)


def main():
    st.set_page_config(layout="wide", page_title="Image Background Remover")

    st.write("## Blur Detector")
    st.sidebar.header("Upload and download :gear:")
    st.sidebar.markdown('------')
    source_radio = st.sidebar.radio(
        "Select Modes:",
        ["Image File", "Image Folder"]
    )
    st.sidebar.markdown('------')
    threshold = st.sidebar.slider('Select threshold:', 0, 1000, 100)

    # Process Image
    if source_radio == "Image File":
        col1, col2 = st.columns(2)
        my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

        if my_upload is not None:
            detect_blur(upload_path=my_upload, col1=col1, col2=col2, threshold=threshold)
        else:
            detect_blur(upload_path="./datasets/blurry/img_3.png", col1=col1, col2=col2, threshold=threshold)

    # Process Image Folder
    elif source_radio == "Image Folder":
        st.info("To be completed!")
        # Created a file uploader widget to upload a ZIP file
        uploaded_file = st.file_uploader("Uploaded a ZIP file containing the folder:")
        if uploaded_file:
            progress_text = "Operation in progress. Please wait..."
            my_bar = st.progress(0, text=progress_text)
            unzip_file_name = uploaded_file.name.split(".")[0]
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall("temp")
                files = os.listdir(f"temp/{unzip_file_name}/")
                for i, file in enumerate(files):
                    percentage = i / len(files)
                    my_bar.progress(percentage, text=f"Operation in progress: {i+1}/{len(files)}. Please wait...")
                    time.sleep(0.1)
            my_bar.empty()


if __name__ == "__main__":
    main()
