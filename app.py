import streamlit as st
import pandas as pd
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

# Load the product data from CSV
@st.cache_data
def load_product_data():
    return pd.read_csv("products.csv")  # Replace "products.csv" with the actual path to your CSV file

product_data = load_product_data()

# Placeholder for actual skin type detection function
def predict_skin_type(image):
    # This function should be replaced with an actual model prediction
    return "Dry"  # Change this value for testing or implement a model for prediction

# Function to filter products based on skin type and selected concerns
def get_products(skin_type, selected_concerns):
    # Filter products based on skin type and selected concerns
    filtered_data = product_data[product_data['Skin_type'].str.contains(skin_type, case=False)]
    if selected_concerns:
        filtered_data = filtered_data[filtered_data['Concern'].apply(
            lambda x: any(concern in x for concern in selected_concerns))]
    return filtered_data

# Streamlit App

# Title
st.title("Skin Type Detection and Skincare Recommendations")

# Image Upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Predict skin type (Replace this with an actual model prediction when available)
    detected_skin_type = predict_skin_type(image)
    st.write(f"**Detected Skin Type (Predicted):** {detected_skin_type}")

    # Manual selection for skin type (for testing or user control)
    skin_type = st.selectbox("Select Skin Type (Override Prediction)", options=["Oily", "Combination", "Dry", "Normal"], index=["Oily", "Combination", "Dry", "Normal"].index(detected_skin_type))

    # Concern Selection
    concerns = st.multiselect("Select Concerns", ["Hydration", "Acne", "Whitehead/Blackhead", "Sun protection", "Pimples"])

    # Get Recommended Products
    recommended_products = get_products(skin_type, concerns)

    # Display Recommended Products in Grid
    st.subheader("Recommended Products")
    num_columns = 3  # Number of products per row
    columns = st.columns(num_columns)
    
    for idx, product in recommended_products.iterrows():
        # Cycle through columns to create a grid
        col = columns[idx % num_columns]
        
        # Display product information
        with col:
            st.write(f"[{product['Product']}]({product['product_url']})")
            
            # Fetch and display image with error handling
            try:
                response = requests.get(product['product_pic'])
                if response.status_code == 200:
                    product_image = Image.open(BytesIO(response.content))
                    st.image(product_image, caption=product['Product'], use_container_width=True)
                else:
                    st.write("Image not available")
            except (UnidentifiedImageError, requests.exceptions.RequestException):
                st.write("Could not load image")



