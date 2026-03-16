# day la ham kiem tra su on dinh voi eps = 2 do va 3 pose gan nhat
# tra ve true nghia la on dinh roi
import cv2
import numpy as np
def isBalance(history, eps=2, n=4,require_ratio=0.8):
    """
    Check if the last `n` values in the history are within the `eps` threshold.
    Returns True if balanced, False otherwise.
    """
    if not history or len(history) < n:
        return False  # Not enough data to determine balance
    # Calculate differences using numpy for efficiency
    differences = np.abs(np.diff(history[-n:]))
    state_count = np.sum(differences <= eps)
    require_count = int((n-1) * require_ratio)
    print(history, differences, state_count, require_count)
    return state_count >= require_count 
# bat ki phan tu args nao co gia tri visibility deu se return ve false nghia la thieu 1 trong 3 se la false
def isReadyVisibility(*args):
    for x in args:
        if x.visibility < 0.3: 
            return False
    return True
def update_history(history,value,n=5):
    history.append(value)
    if(len(history)>n):
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
    return (hip_np>=shoulder_np)


def get_landmark(pose_landmarks):
    # Giả sử pose_landmarks là kết quả từ vòng lặp: for pose_landmarks in result.pose_landmarks:
    landmarks_dict = {
# Khuôn mặt (Face)
"nose": pose_landmarks[0],
"left_eye_inner": pose_landmarks[1],
"left_eye": pose_landmarks[2],
"left_eye_outer": pose_landmarks[3],
"right_eye_inner": pose_landmarks[4],
"right_eye": pose_landmarks[5],
"right_eye_outer": pose_landmarks[6],
"left_ear": pose_landmarks[7],
"right_ear": pose_landmarks[8],
"mouth_left": pose_landmarks[9],
"mouth_right": pose_landmarks[10],

# Thân trên (Upper Body)
"left_shoulder": pose_landmarks[11],
"right_shoulder": pose_landmarks[12],
"left_elbow": pose_landmarks[13],
"right_elbow": pose_landmarks[14],
"left_wrist": pose_landmarks[15],
"right_wrist": pose_landmarks[16],
"left_pinky": pose_landmarks[17],
"right_pinky": pose_landmarks[18],
"left_index": pose_landmarks[19],
"right_index": pose_landmarks[20],
"left_thumb": pose_landmarks[21],
"right_thumb": pose_landmarks[22],

# Thân dưới (Lower Body)
"left_hip": pose_landmarks[23],
"right_hip": pose_landmarks[24],
"left_knee": pose_landmarks[25],
"right_knee": pose_landmarks[26],
"left_ankle": pose_landmarks[27],
"right_ankle": pose_landmarks[28],
"left_heel": pose_landmarks[29],
"right_heel": pose_landmarks[30],
"left_foot_index": pose_landmarks[31],
"right_foot_index": pose_landmarks[32],
}
    return landmarks_dict