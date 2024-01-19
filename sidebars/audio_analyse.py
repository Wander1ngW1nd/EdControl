# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:45:21 2023

@author: M
"""
import cv2
import streamlit as st
import os
import diarization as dz
from plotlycharts import charts

#функция для отображения экспандеров до загрузки видео, аргумент - колонка, в которой все отображается
def default_expanders(teacher):

    with teacher.expander(":red[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":green[ФИО_дата_время1.mp4]"):
        st.write("...")
    with teacher.expander(":orange[ФИО_дата_время1.mp4]"):
        st.write("...")

def count_video_length(path, name):
    
    path_to_video = os.path.join(path, name)
    cap = cv2.VideoCapture(path_to_video)
    fps = cap.get(cv2.CAP_PROP_FPS) 
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    length = duration / 60  # duration in minutes
    
    return length

#view, отображаемая по нажатию на препода
def view_side_bar(name, teacher, path):
    teacher.header("📸"+name)

    rating, info = teacher.columns([3,5])

    rating.header("Рейтинг")
    rating.text("⭐⭐⭐")

    info.header("Информация")
    info.text("email, phone")

    videoFile_dz = teacher.file_uploader("Загрузить видео для перевода в текст", type='mp4',\
                                      accept_multiple_files=False)
    
    #если видео загружено, сохраняем и отрисовываем больше экспандеров
    if videoFile_dz is not None:
    
        #скачивание файла в дирректорию
        with open(os.path.join(path, videoFile_dz.name),"wb") as f:
            f.write(videoFile_dz.getbuffer())
        videoLength = count_video_length(path, videoFile_dz.name)
        if videoLength <=3 and videoLength >= 0.01:
            with teacher.status("Обработка"):
                dz.path_for_audio(path,videoFile_dz.name)
                audio = './audio.wav'
                dz.dz_result(audio)
                with open('transcript.txt') as input:
                    st.text(input.read())

        else:
            teacher.error("Длинное видео")
            teacher.header("Выбор урока")
            default_expanders(teacher)
    #иначе отрисовываем дефолтное кол-во экспандеров
    else:

        teacher.header("Выбор видео")

        default_expanders(teacher)
   