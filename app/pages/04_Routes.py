import sys
sys.path.append('../') 
from utils import *
import streamlit as st

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>My green pathway</h1>", unsafe_allow_html=True)

with st.form('my_form'):

    col1, col2= st.columns([1, 1])
    with col1:
        origin= st.text_input('Origin', 'Stanford University')
        mode= st.selectbox('Mode to travel',('Walking', 'Transit', 'Driving'))

    with col2:
        destination= st.text_input('Destination', 'San Francisco International Airport')

    submitted = st.form_submit_button("Submit")

    if submitted:
        iframe_html = f"""<iframe src="{route_map(origin, destination, mode)}" width="800" height="600"></iframe>"""

        # Display the iframe using st.components.html
        st.components.v1.html(iframe_html, width=800, height=600)