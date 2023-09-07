# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:28:00 2023

@author: M
"""

import streamlit as st

from sidebars import video_analyse
 

def main():

    st.set_page_config(
        page_title="EdTech",
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
            column2.header("MVP")
        elif st.session_state.sidebars == 1:
            video_analyse.view_side_bar("Преподаватель 1", column2)


if __name__ == "__main__":
    main()
