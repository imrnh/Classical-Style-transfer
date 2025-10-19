import streamlit as st
from PIL import Image
import numpy as np
from time import perf_counter

from style_transfer_parallel import style_transfer as style_para
from style_transfer import style_transfer as style_mono
from utils import get_stylized_rgb

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Patch-Based Style Transfer", layout="wide")

st.title("🎨 Patch-Based Style Transfer")
st.markdown(
    """
    Upload a **content image** and a **style image**, then choose processing mode and parameters.  
    The algorithm transfers the artistic style from the style image onto the content image.
    """
)

# 🔥 Sidebar width customization
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 400px;
        max-width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"]{
        min-width: 350px;
        max-width: 350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("⚙️ Settings")

content_file = st.sidebar.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])
style_file = st.sidebar.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

mode = st.sidebar.selectbox(
    "Processing Mode",
    ["Parallel Processing", "Non-Parallel Processing"]
)

patch_size = st.sidebar.slider("Patch Size (smaller = sharper but slower)", 1, 32, 12)
stride = st.sidebar.slider("Stride (smaller = sharper but slower)", 1, 32, 12)

run_button = st.sidebar.button("🚀 Run Style Transfer")

# -------------------------------
# Main App Logic
# -------------------------------
if content_file and style_file:
    content_img = Image.open(content_file).convert("RGB")
    style_img = Image.open(style_file).convert("RGB")

    # # Show previews before processing
    # st.subheader("📥 Uploaded Images")
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.image(content_img, caption="Content Image", use_container_width=True)
    # with col2:
    #     st.image(style_img, caption="Style Image", use_container_width=True)

    # Show input images (smaller preview)
    st.subheader("Input Images Preview")
    col1, col2 = st.columns(2)

    with col1:
        st.caption("🖼️ Content Image")
        st.image(content_img, width=350)  # Smaller preview

    with col2:
        st.caption("🎨 Style Image")
        st.image(style_img, width=350)  # Smaller preview


    if run_button:
        content_arr = np.array(content_img)
        style_arr = np.array(style_img)

        with st.spinner("✨ Running style transfer... please wait."):
            st_time = perf_counter()
            if mode == "Parallel Processing":
                st_img = style_para(content_arr, style_arr, patch_size=patch_size, stride=stride)
            else:
                st_img = style_mono(content_arr, style_arr, patch_size=patch_size, stride=stride)
            ed_time = perf_counter()

        elapsed = ed_time - st_time
        st.success(f"✅ Done! Processing time: {elapsed:.2f} seconds")

        # Show only output image
        st.subheader("🎨 Stylized Output")
        st.image(get_stylized_rgb(st_img), caption="Stylized Image", use_container_width=True)

else:
    st.info("⬅️ Please upload both a content image and a style image from the sidebar to begin.")
