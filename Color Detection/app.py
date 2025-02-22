import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #FADADD; /* Pale Pink Background */
        }
        .stApp {
            background-color: #FADADD;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #333333;
        }
        .image-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }
        .color-title {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Function to detect colors in an image
def detect_colors(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color_ranges = {
        "Red": [(np.array([0, 120, 70]), np.array([10, 255, 255])),
                (np.array([170, 120, 70]), np.array([180, 255, 255]))],
        "Orange": [(np.array([11, 150, 150]), np.array([19, 255, 255]))],
        "Yellow": [(np.array([20, 100, 100]), np.array([30, 255, 255]))],
        "Green": [(np.array([36, 50, 70]), np.array([89, 255, 255]))],
        "Blue": [(np.array([90, 50, 70]), np.array([128, 255, 255]))],
        "Pink": [(np.array([140, 50, 70]), np.array([169, 255, 255]))],
        "Purple": [(np.array([129, 50, 70]), np.array([139, 255, 255]))]
    }

    detected_images = {}
    detected_colors = []

    for color, ranges in color_ranges.items():
        mask = np.zeros_like(hsv_image[:, :, 0])
        for lower, upper in ranges:
            mask |= cv2.inRange(hsv_image, lower, upper)

        result = cv2.bitwise_and(image, image, mask=mask)
        
        # If a color is found, store it
        if np.any(mask):
            detected_images[color] = result
            detected_colors.append(color)

    return detected_images, detected_colors

# 🎨 Streamlit UI
st.markdown("<h1 class='title'>🎨 Color Detection App</h1>", unsafe_allow_html=True)
st.write("Upload an image, and I'll detect and separate different colors!")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Display Original Image
    st.subheader("Original Image")
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), channels="RGB")

    # Process Image
    detected_images, detected_colors = detect_colors(image)

    if detected_images:
        # Display Detected Colors Side by Side
        st.subheader("Detected Colors")
        image_cols = st.columns(len(detected_images))  # Create columns dynamically

        for idx, (color, img) in enumerate(detected_images.items()):
            with image_cols[idx]:  # Place each image in a separate column
                st.markdown(f"<p class='color-title'>{color}</p>", unsafe_allow_html=True)
                st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), channels="RGB")

        # Show list of detected colors
        st.subheader("Colors detected:")
        st.write(", ".join(detected_colors))
    else:
        st.write("No colors detected in the image.")
