# tinh goc giu 3 diem, can tinh goc tai tham so thu nhat
from datetime import datetime
import numpy as np
def goc_tai_tham_so_thu_nhat(a,b,c):
    k = np.array([a.x,a.y]) 
    h = np.array([b.x,b.y])
    m = np.array([c.x,c.y])
    hk = k-h
    km = k-m
    cos_a = np.dot(hk,km)/(np.linalg.norm(hk) * (np.linalg.norm(km)))
    cos_a = np.clip(cos_a,-1.0,1.0)

    a = np.degrees(np.arccos(cos_a))
    a = round(a,0)
    return a

def convert_to_px(component,frame):
    h,w,_ = frame.shape
    return (int(component.x*w),int(component.y*h))

def calculating_accuracy(good,total):
    accuracy = 0
    if total == 0:
        return accuracy
    return round((good/total)*100,0)

def calculating_distance(a,b):
    A = np.array([a.x,a.y])
    B = np.array([b.x,b.y])
    distance = np.linalg.norm(B-A)
    return distance

def trungbinh(a,b):
    return round(((a+b)/2.0),2)

def create_time_video(frame,fps):
    return round(frame/fps,2)

def get_form(accuracy):
    form = ""

    if accuracy <= 40:
        form = "Needs Work"
    elif accuracy<80:
        form = "Good"
    else:
        form = "Excellent"
    return form
def calc_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


import cv2
from pathlib import Path
from urllib.parse import unquote
def get_time_video(path):
    path_video_encode = path
    path_video = unquote(path_video_encode)

    cap = cv2.VideoCapture(str(path_video))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps <=0:
        fps=30
    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    time_video = round(total_frame/fps,0)
    print(path_video,fps,total_frame)
    return time_video