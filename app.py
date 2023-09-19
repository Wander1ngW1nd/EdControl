# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:28:00 2023

@author: M
"""

import streamlit as st
import os

from sidebars import video_analyse


VIDEO_PATH = "videos"

def main():
    st.set_page_config(
        page_title="EdConrol",
        page_icon="👁‍🗨",
        layout="wide",
        initial_sidebar_state="expanded",
    )




    column1, column2 = st.columns([1, 10])

    #отображение страницы при обновлении страницы по умолчанию - home
    if "sidebars" not in st.session_state:
        st.session_state.sidebars = 0

    with st.sidebar:
        home = st.button("🏠")
        st.title("Преподаватели")

        analyse = st.button("Преподаватель 1")

        #уловия по нажатию на кнопки
        if home:
            st.session_state.sidebars = 0
        elif analyse:
            st.session_state.sidebars = 1

        if st.session_state.sidebars == 0:
            #column2.header("EdControl") 
            video_analyse.draw_readme(column2)
        elif st.session_state.sidebars == 1:
            if not os.path.exists(VIDEO_PATH):
                os.mkdir(VIDEO_PATH)
                video_analyse.view_side_bar("Преподаватель 1", column2, VIDEO_PATH)
            else:
                video_analyse.view_side_bar("Преподаватель 1", column2, VIDEO_PATH)

if __name__ == "__main__":
    main()
