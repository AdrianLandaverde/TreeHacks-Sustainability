import sys
sys.path.append('../') 
from utils import *
import streamlit as st


st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Earth Voice</h1>", unsafe_allow_html=True)

if 'n_place' not in st.session_state:
    st.session_state['n_place'] = 0

places_names= ["Amazon Rain Forest", "Mesoamerican Reef"]
places_images= ["https://files.worldwildlife.org/wwfcmsprod/images/Amazon_River_New_Hero_Image/hero_full/96jxl0p02y_Amazon_River_Hero.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Mesoamerican_Reef_7.25.12_Places/hero_full/22f6g3tjgi_Circle_and_hero_image.jpg"]



col1, col2, col3= st.columns([1, 10, 1])
with col1:
    left_button= st.button("👈")
    if left_button:
        st.session_state['n_place']= (st.session_state['n_place'] - 1) % len(places_names)

with col3:
    right_button= st.button("👉")
    if right_button:
        st.session_state['n_place']= (st.session_state['n_place'] + 1) % len(places_names)

with col2:
    st.markdown(f"<h3 style='text-align: center; color: black;'>{places_names[st.session_state['n_place']]}</h3>", unsafe_allow_html=True)

st.image(places_images[st.session_state['n_place']], use_column_width=True)

with st.form("my-form"):

    col1, col2= st.columns([8, 1])

    with col1:
        question = st.text_input(f"Ask something to the {places_names[st.session_state['n_place']]}", 'What are your biggest fears?')

    with col2:
        submitted = st.form_submit_button("Ask")

    if submitted:
        RAG_planet(place=places_names[st.session_state['n_place']], question=question)



