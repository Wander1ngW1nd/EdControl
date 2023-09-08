# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:45:21 2023

@author: M
"""
import cv2
import glob
import streamlit as st
import time
import os

from plotlycharts import charts


#VIDEO_PATH = "C:\\Users\\ПК\\Videos"

README_IMG_FOLDER = ".//Documents//GitHub//EdControl//img"
README_FILE_PATH = './/Documents//GitHub//EdControl//Readme_for_main_page.txt'

EMOTIONS_RU = {"angry":"Злость", "disgust":"Отвращение", "fear":"Страх",
            "happy":"Счастье", "sad":"Грусть", "surprise":"Удивление"}

def draw_readme(column):
    with open(README_FILE_PATH, 'r') as f:
        readme_line = f.readlines()
        buffer = []
        resourses = [os.path.basename(x) for x in glob.glob(README_IMG_FOLDER + "//*")]
    for line in readme_line:
        buffer.append(line)
        for imgFolder in resourses:
            if imgFolder in line:
                column.markdown(''.join(buffer[:-1])) 
                column.image(README_IMG_FOLDER + f'//{imgFolder}', use_column_width = True)
                buffer.clear()
    column.markdown(''.join(buffer))

def seconds_to_time(seconds):
    
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    time = "%d:%02d:%02d" % (hour, minutes, seconds) 
     
    return time

def count_video_length(path, name):
    
    path_to_video = os.path.join(path, name)
    cap = cv2.VideoCapture(path_to_video)
    fps = cap.get(cv2.CAP_PROP_FPS) 
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    length = duration / 60  # duration in minutes
    
    return length

#функция для отображения экспандеров до загрузки видео, аргумент - колонка, в которой все отображается
def default_expanders(teacher):

    with teacher.expander(":red[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":green[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":orange[ФИО_дата_время1.mp4]"):
        st.write("...")

#функция для отображения экспандеров после загрузки видео, аргументы-колонка и видеофайл
def add_expander(teacher, video, path):


    with teacher.expander(":green[загруженное видео]"):
        st.write("Аналитика")
        info, timeStamps = st.columns([4, 6])

   #video read
        video_file = open(path +"\\"+ video.name, 'rb')
        video_bytes = video_file.read()
        #info.write("videoplayer")
        info.video(video_bytes)

        timeStamps.text("Вреременные отметки ⬇")
        #data = метод_модели()
        
        data = [{"время": "5:10", "Эмоция":"Удивление", "Score":0.4},
                {"время": "8:09", "Эмоция":"Грусть", "Score":0.6},
                {"время": "11:14", "Эмоция":"Счастье", "Score":0.34}]
        
        timeStamps.data_editor(data, disabled = True)

        
        #selectbox выбора типа графика
        option = info.selectbox(
            'Форма представления',
                ('Пятиугольник', 'Bar chart'))

        if option == 'Пятиугольник':
            radio = charts.radio_chart()
            info.plotly_chart(radio, use_container_width=True)
            st.write("...")
        elif option == 'Bar chart':
            bar = charts.bar_chart()
            info.plotly_chart(bar, use_container_width=True)
            st.write("...")



    with teacher.expander(":red[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":green[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":orange[ФИО_дата_время1.mp4]"):
        st.write("...")

#view, отображаемая по нажатию на препода
def view_side_bar(name, teacher, path):
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
        with open(os.path.join(path, videoFile.name),"wb") as f:
            f.write(videoFile.getbuffer())
        videoLength = count_video_length(path, videoFile.name)
        if videoLength <=17 and videoLength >= 0.01:
            with teacher.status("Обработка"):
                time.sleep(3)
                
            teacher.header("Выбор видео")
            add_expander(teacher, videoFile, path)
        else:
            teacher.error("Длинное видео")
            teacher.header("Выбор видео")
            default_expanders(teacher)
    #иначе отрисовываем дефолтное кол-во экспандеров
    else:
        
        teacher.header("Выбор видео")

        default_expanders(teacher)
