import sys
sys.path.append('../') 
from utils import *
import streamlit as st


st.markdown("<h1 style='text-align: center; color: black;'>Sustainable Resturants near me</h1>", unsafe_allow_html=True)

with st.form('my_form'):
    address = st.text_input('Address', 'Stanford University')

    submitted = st.form_submit_button("Submit")
    if submitted:
        restaurants_response= get_green_restaurants(address)

        restaurants_list= restaurants_response["names"]
        restaurants_map= restaurants_response["static_map"]
        col1, col2= st.columns([1, 2])

        with col1:
            st.markdown("\n".join([f"{i + 1}. {item}" for i, item in enumerate(restaurants_list)]))

        with col2:
            st.image(restaurants_map, use_column_width=True)