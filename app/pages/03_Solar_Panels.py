import sys
sys.path.append('../') 
from utils import *
import streamlit as st

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>Solar Panels</h1>", unsafe_allow_html=True)

with st.form('my_form'):
    address = st.text_input('Address', 'Stanford University')

    submitted = st.form_submit_button("Submit")
    if submitted:
        solar_panels_heatmap= heatmap_solar_panels(address)

        col1, col2= st.columns([1, 2])
        
        with col2:
            st.image(solar_panels_heatmap, use_column_width=True)

