import sys
sys.path.append('../') 
from utils import *
import streamlit as st

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Label Analyzer</h1>", unsafe_allow_html=True)

with st.form("my_form"):
    photo= st.file_uploader("Upload a picture of a label of clothes", type=["jpg", "png", "jpeg"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        if photo is not None:
            pil_image= Image.open(photo)
            texto= get_label_info(pil_image)
            st.markdown(texto)