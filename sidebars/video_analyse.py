# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:45:21 2023

@author: M
"""
import streamlit as st
import time
import os

from plotlycharts import charts

#функция для отображения экспандеров до загрузки видео, аргумент - колонка, в которой все отображается
def default_expanders(teacher):

    with teacher.expander(":red[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":green[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":orange[ФИО_дата_время1.mp4]"):
        st.write("...")

#функция для отображения экспандеров после загрузки видео, аргументы-колонка и видеофайл
def add_expander(teacher, video):


    with teacher.expander(":green[загруженное видео]"):
        st.write("Аналитика")
        info, timeStamps = st.columns([4, 6])

   #video read
        #video_file = open('C\\ путь \\имя файла.mp4', 'rb')
        #video_bytes = video_file.read()
        info.write("videoplayer")
        #info.video(video_bytes)

        timeStamps.text("График с времеными отметками ⬇")

        #selectbox выбора типа графика
        option = info.selectbox(
            'Форма представления',
                ('Пятиугольник', 'Piechart'))

        if option == 'Пятиугольник':
            radio = charts.radio_chart()
            info.plotly_chart(radio, use_container_width=True)
            st.write("...")
        elif option == 'Piechart':
            st.write("...")



    with teacher.expander(":red[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":green[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":orange[ФИО_дата_время1.mp4]"):
        st.write("...")

#view, отображаемая по нажатию на препода
def view_side_bar(name, teacher):
    teacher.header("📸"+name)

    rating, info = teacher.columns([3,5])

    rating.header("Рейтинг")
    rating.text("⭐⭐⭐")

    info.header("Информация")
    info.text("email, phone")

    #upload файла
    videoFile = teacher.file_uploader("Загрузить видео", type='mp4',\
                                      accept_multiple_files=False)

    #если видео загружено, сохраняем и отрисовываем больше экспандеров
    if videoFile is not None:
        #скачивание файла в дирректорию
        with open(os.path.join("директория", videoFile.name),"wb") as f:
            f.write(videoFile.getbuffer())

        with teacher.status("Обработка"):
            time.sleep(3)
        teacher.header("Выбор видео")

        add_expander(teacher, videoFile)

    #иначе отрисовываем дефолтное кол-во экспандеров
    else:

        teacher.header("Выбор видео")

        default_expanders(teacher)
