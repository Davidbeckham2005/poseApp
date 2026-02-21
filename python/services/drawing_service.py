import numpy as np
import cv2
from services.pose_service import PoseDetector
class DrawingService:
    def __init__(self,detector: PoseDetector):
        self.detector = detector
        self.CONNECTIONS = [
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Tay & Vai
            (11, 23), (12, 24), (23, 24),                   # Thân
            (23, 25), (25, 27), (24, 26), (26, 28)          # Chân (Quan trọng cho Squat)
        ]
      
    def draw_skeleton(self,frame,pose_landmarks):
        h, w, _ = frame.shape
        landmarks_px = []
        for lm in pose_landmarks:
            landmarks_px.append((int(lm.x * w), int(lm.y * h)))

        # 2. Vẽ các đường nối (Connections)
        for connection in self.CONNECTIONS:
            start_idx, end_idx = connection
            pt1 = landmarks_px[start_idx]
            pt2 = landmarks_px[end_idx]
            
            # Vẽ đường xương (Màu xanh lá)
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # 3. Vẽ các khớp tròn (Joints)
        for pt in landmarks_px:
            # Chỉ vẽ các điểm chính (từ vai trở xuống) để tránh rối mắt
            cv2.circle(frame, pt, 4, (0, 0, 255), 1)

    def draw_at_point_face(self,frame,pose_landmarks):
        face_px = self.detector.get_on_face_px(frame,pose_landmarks)
        # chuyen tu dict sang array don thuan 
       
        for x, y in face_px.values():
            cv2.circle(frame, (x, y), 4, (0,255,0), -1)
    def draw_line(self,frame, Point_A_px, Point_B_px,color): 
        cv2.line(frame,Point_A_px,Point_B_px,color,10)

    def draw_origin_at_intersection(self,frame,origin_left,origin_right,line_left,line_right,color):
        cv2.putText(frame,str(origin_left),(line_left[0]-10,line_left[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,color,2)
        cv2.putText(frame,str(origin_right),(line_right[0]-10,line_right[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,color,2)