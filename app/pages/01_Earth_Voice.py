import sys
sys.path.append('../') 
from utils import *
import streamlit as st
import base64
from gtts import gTTS 
from pygame import mixer
import os
import time


st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Earth Voice</h1>", unsafe_allow_html=True)

if 'n_place' not in st.session_state:
    st.session_state['n_place'] = 0

places_names= ["Amazon Rain Forest", "Mesoamerican Reef", "Northern Great Plains", "Chihuahuan Dessert", "Galapagos", 
                "Pantanal", "Southern Chile", "Amur Heilong", "Arctic", "Atlantic Forest",
                "Coastal East Africa", "Congo Basin", "Coral Triangle", "Eastern Himalayas",
                "Greater Mekong", "Madagascar", "Namibia", "Yagtze"]
places_images= ["https://files.worldwildlife.org/wwfcmsprod/images/Amazon_River_New_Hero_Image/hero_full/96jxl0p02y_Amazon_River_Hero.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Mesoamerican_Reef_7.25.12_Places/hero_full/22f6g3tjgi_Circle_and_hero_image.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/NGP_main/hero_full/24wjafaqa8_NGP_Hargreaves.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/SCR_54662.jpg/hero_full/77rwlrshwd_SCR_54662.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/galapagos_new_hero.jpg/hero_full/2s7crl90mn_galapagos_new_hero.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Pantanal_Aerial_Wetlands/hero_full/36ov1ebhi7_aerial_2.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Southern_Chile_Hero_Image/hero_full/4mepz9fp17_Southern_Chile_Hero_image__c__Edward_Parker_WWF_Canon.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Amur_Heilong_Hero_image__c__Hartmut_Jungius_WWF_Canon.jpg/hero_full/2tkc8stjhs_Amur_Heilong_Hero_image__c__Hartmut_Jungius_WWF_Canon.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Arctic_New_Hero_Image/hero_full/8d0vth7mei_Arctic_Hero.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Atlantic_Forests_new_splash/hero_full/e19dgh2sh__WW194933.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Coastal_East_Africa/hero_full/6i1sv146n1_Coastal_East_Africa_07302012_Hero.JPG",
                "https://files.worldwildlife.org/wwfcmsprod/images/Luilaka_River_Salonga_National_Park/hero_full/18fjf16qab_Medium_WW243241.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Raja_Ampat_underwater_Coral_Triangle_Places/hero_full/53mgowfv4g__c__Robert_Delfs_WWF_Canon.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Thanza_valley_Bhutan_Eastern_Himalayas/hero_full/1kta7qft4d_Eastern_Himalaya_1600x600px.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Greater_Mekong_8.7.2012_Hero_and_Circle_XL_282296.jpg/hero_full/116gharqsd_Greater_Mekong_8.7.2012_Hero_and_Circle_XL_282296.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/mountain_07182012_HI_259967.jpg/hero_full/7kziu8alpe_mountain_07182012_HI_259967.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Namibia_7.26.2012_hero_and_circle_MID_202444.jpg/hero_full/ojsz6hq4a_Namibia_7.26.2012_hero_and_circle_MID_202444.jpg",
                "https://files.worldwildlife.org/wwfcmsprod/images/Yangtze_River_191642/hero_full/5ynoi1x0v_Yangtze_Hero_image_GPN_105755__c__Michel_Gunther_WWF_Canon_.jpg"



                ]



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
        with st.spinner('Let me think...'):
            rag_answer= RAG_planet(place=places_names[st.session_state['n_place']], question=question)

            st.markdown(rag_answer["Answer"])

            language = 'en'
  
            myobj = gTTS(text=rag_answer["Answer"], lang=language, slow=False) 
            
            myobj.save("audio.mp3") 
            mixer.init()
            mixer.music.load("audio.mp3")
            mixer.music.play()
        
        time.sleep(30)
        mixer.quit()
        os.remove("audio.mp3")

