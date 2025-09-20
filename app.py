import streamlit as st
from PIL import Image
from style_transfer_para import style_transfer as style_para
from style_transfer import style_transfer as style_mono
from utils import get_stylized_rgb
from time import perf_counter
from plotting import plot_for_streamlit   # use modified function
import numpy as np
from PIL import Image

st.set_page_config(page_title="Patch-Based Style Transfer", layout="centered")

st.title("🎨 Patch-Based Style Transfer Demo")

# Upload images
content_file = st.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])
style_file = st.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

# Mode selection
mode = st.selectbox("Processing Mode", 
                    ["Non-Parallel Processing", "Parallel Processing"])

# Sliders
patch_size = st.slider("Patch Size (smaller = better but slower)", 1, 32, 12)
stride = st.slider("Stride (smaller = better but slower)", 1, 32, 12)

# Run style transfer
if content_file and style_file:
    content_img = Image.open(content_file).convert("RGB")
    style_img = Image.open(style_file).convert("RGB")

    # 🔥 Convert to NumPy arrays for your functions
    content_arr = np.array(content_img)
    style_arr = np.array(style_img)

    if st.button("Run Style Transfer"):
        with st.spinner("Processing... please wait"):
            st_time = perf_counter()

            if mode == "Parallel Processing":
                st_img = style_para(content_arr, style_arr, patch_size=patch_size, stride=stride)
            else:
                st_img = style_mono(content_arr, style_arr, patch_size=patch_size, stride=stride)

            ed_time = perf_counter()
            elapsed = ed_time - st_time

        st.success(f"✅ Done! Time taken: {elapsed:.2f} seconds")

        # Use arrays here as well
        fig = plot_for_streamlit([st_img], [content_arr], [style_arr])
        st.pyplot(fig)