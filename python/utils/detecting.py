# day la ham kiem tra su on dinh voi eps = 2 do va 3 pose gan nhat
# tra ve true nghia la on dinh roi
import cv2
import numpy as np
def isBalance(history,eps=2,n=3):
    if len(history) < n:
        return False  
    for i in range (1,n):
        if abs(history[-i] - history[-i-1])>eps:
            return False
    return True 
# bat ki phan tu args nao co gia tri visibility deu se return ve false nghia la thieu 1 trong 3 se la false
def isReadyVisibility(*args):
    for x in args:
        if x.visibility < 0.1: 
            return False
    return True
def update_history(history,value,max_frame=5):
    history.append(value)
    if(len(history)>max_frame):
        history.pop(0)
def drawtext(frame,coord,text,color):
    cv2.putText(frame,text,coord,cv2.FONT_HERSHEY_COMPLEX,1,color,2)

def check_view(history_hip, history_shoulder,n=5):
    if len(history_hip) < n or len(history_shoulder) < n:
        return False
    hip = np.mean(history_hip)
    shoulder = np.mean(history_shoulder)
    if hip>0.04 and hip<0.17 and shoulder<0.27 and shoulder > 0.07:
        return True
    
def check_distance_between_knee_and_sholder(history_knee,history_shoulder,n=5):
    if len(history_knee) < n or len(history_shoulder) < n:
        return False
    knee = np.mean(history_knee)
    shoulder = np.mean(history_shoulder)
    return knee>=shoulder 

def check_y_hip_and_shoulder(history_y_hip,history_y_shoulder):
    hip_np = np.mean(history_y_hip)
    shoulder_np = np.mean(history_y_shoulder)
    print(hip_np, shoulder_np)
    return (hip_np>=shoulder_np)