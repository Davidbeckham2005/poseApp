from turtle import right
import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils.calc import convert_to_px
import time
class PoseDetector:
    def __init__(self, model_path='C:/Users/dinhh/Desktop/nienluan/PoseApp/python/pose_landmarker_full.task'):
        self.base_options = python.BaseOptions(model_asset_path=model_path)
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(self.options)
        
    def run_process(self,frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(time.time() * 1000)
        # timestamp_ms = self.capture.get_timestamps_ms()
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)
        return result
    # def get_mp_pose(self):
    #     return self.mp_pose
    
    def get_landmark(self,pose_landmarks):
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
    # def get_pose_landmark(self,result):
    #     return result.pose_landmarks
    
    # def get_land_mark(self,result):
    #     return result.pose_landmarks.landmark
    def get_for_push_up(self, pose_landmarks):
        data = {
        "left_shoulder": pose_landmarks[11],
        "right_shoulder": pose_landmarks[12],
        "left_elbow": pose_landmarks[13],
        "right_elbow": pose_landmarks[14],
        "left_wrist": pose_landmarks[15],
        "right_wrist": pose_landmarks[16],
         "left_hip": pose_landmarks[23],
        "right_hip": pose_landmarks[24],
        }
        return data
    def get_for_push_up_px(self,frame, pose_landmarks):
        data = self.get_for_push_up(pose_landmarks)
        data_px = {
        "left_shoulder_px": convert_to_px(data["left_shoulder"],frame),
        "right_shoulder_px": convert_to_px(data["right_shoulder"],frame),
        "left_elbow_px": convert_to_px(data["left_elbow"],frame),
        "right_elbow_px": convert_to_px(data["right_elbow"],frame),
        "left_wrist_px": convert_to_px(data["left_wrist"],frame),
        "right_wrist_px": convert_to_px(data["right_wrist"],frame),
        "left_hip_px": convert_to_px(data["left_hip"],frame),
        "right_hip_px": convert_to_px(data["right_hip"],frame),

        }
        return data_px
    def get_on_face(self,pose_landmarks):
        face_dict = {
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
        }
        return face_dict
    def get_on_face_px(self,frame,pose_landmarks):
        face = self.get_on_face(pose_landmarks)
        face_px = {
        "nose_px": convert_to_px(face['nose'], frame),
        "left_eye_inner_px": convert_to_px(face['left_eye_inner'], frame),
        "left_eye_px": convert_to_px(face['left_eye'], frame),
        "left_eye_outer_px": convert_to_px(face['left_eye_outer'], frame),
        "right_eye_inner_px": convert_to_px(face['right_eye_inner'], frame),
        "right_eye_px": convert_to_px(face['right_eye'], frame),
        "right_eye_outer_px": convert_to_px(face['right_eye_outer'], frame),
        "left_ear_px": convert_to_px(face['left_ear'], frame),
        "right_ear_px": convert_to_px(face['right_ear'], frame),
        "mouth_left_px": convert_to_px(face['mouth_left'], frame),
        "mouth_right_px": convert_to_px(face['mouth_right'], frame),
        }
        return face_px
    def get_left_body(self,pose_landmarks):
        left_body = {
        "shoulder": pose_landmarks[11],
        "elbow": pose_landmarks[13],
        "wrist": pose_landmarks[15],
        "pinky": pose_landmarks[17],
        "index": pose_landmarks[19],
        "thumb": pose_landmarks[21],

        "hip": pose_landmarks[23],
        "knee": pose_landmarks[25],
        "ankle": pose_landmarks[27],
        "heel": pose_landmarks[29],
        "foot_index": pose_landmarks[31],
}         
        return left_body
    def get_right_body(self,pose_landmarks):
        right_body = {
        "shoulder": pose_landmarks[12],
        "elbow": pose_landmarks[14],
        "wrist": pose_landmarks[16],
        "pinky": pose_landmarks[18],
        "index": pose_landmarks[20],
        "thumb": pose_landmarks[22],

        "hip": pose_landmarks[24],
        "knee": pose_landmarks[26],
        "ankle": pose_landmarks[28],
        "heel": pose_landmarks[30],
        "foot_index": pose_landmarks[32],
        }
        return right_body
    def get_right_body_px(self,frame,pose_landmarks):
        right_body = self.get_right_body(pose_landmarks)
        right_body_px = {
        "shoulder": convert_to_px(right_body["shoulder"], frame),
        "elbow": convert_to_px(right_body["elbow"], frame),
        "wrist": convert_to_px(right_body["wrist"], frame),
        "pinky": convert_to_px(right_body["pinky"], frame),
        "index": convert_to_px(right_body["index"], frame),
        "thumb": convert_to_px(right_body["thumb"], frame),

        "hip": convert_to_px(right_body["hip"], frame),
        "knee": convert_to_px(right_body["knee"], frame),
        "ankle": convert_to_px(right_body["ankle"], frame),
        "heel": convert_to_px(right_body["heel"], frame),
        "foot_index": convert_to_px(right_body["foot_index"], frame),
}       
        return right_body_px
    
    def get_left_body_px(self,frame,pose_landmarks):
        left_body = self.get_left_body(pose_landmarks)
        left_body_px = {
        "shoulder": convert_to_px(left_body["shoulder"], frame),
        "elbow": convert_to_px(left_body["elbow"], frame),
        "wrist": convert_to_px(left_body["wrist"], frame),
        "pinky": convert_to_px(left_body["pinky"], frame),
        "index": convert_to_px(left_body["index"], frame),
        "thumb": convert_to_px(left_body["thumb"], frame),

        "hip": convert_to_px(left_body["hip"], frame),
        "knee": convert_to_px(left_body["knee"], frame),
        "ankle": convert_to_px(left_body["ankle"], frame),
        "heel": convert_to_px(left_body["heel"], frame),
        "foot_index": convert_to_px(left_body["foot_index"], frame),
}       
        return left_body_px
    
    def check_oriantation(self,pose_landmarks):
        left_shoulder = self.get_left_body(pose_landmarks)["shoulder"]
        right_shoulder = self.get_right_body(pose_landmarks)['shoulder']

        left_hip = self.get_left_body(pose_landmarks)['hip']
        right_hip = self.get_right_body(pose_landmarks)['hip']
        
        # hip_dis = abs(left_hip.x-right_hip.x)
        # shouulder_dis = abs(left_shoulder.x-right_shoulder.x)
        return{
          "hip_dis":  abs(left_hip.x-right_hip.x),
           "shoulder_dis": abs(left_shoulder.x-right_shoulder.x)
        }