import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import io

# Streamlit UI
st.title("Digital Image Forgery Detection")

def ela_analysis(image, quality=90):
    """
    Perform Error Level Analysis (ELA) on an image to detect tampered regions.
    """
    # Save uploaded image as a temporary file
    compressed = io.BytesIO()
    image.save(compressed, "JPEG", quality=quality)
    
    # Reopen the compressed image
    compressed = Image.open(compressed)

    # Compute the difference between original and compressed images
    diff = ImageChops.difference(image, compressed)

    # Enhance the difference to make discrepancies more visible
    extrema = diff.getextrema()
    max_diff = max([value for channel in extrema for value in channel])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    diff = ImageEnhance.Brightness(diff).enhance(scale)

    return diff

# File uploader in Streamlit
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file).convert('RGB')

    # Perform ELA
    ela_result = ela_analysis(image)

    # Display images
    st.image(image, caption="Original Image", use_column_width=True)
    st.image(ela_result, caption="ELA Result (Forgery Detection)", use_column_width=True)
