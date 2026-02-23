from re import S

from utils.calc import goc_tai_tham_so_thu_nhat, convert_to_px,calculating_accuracy, calculating_distance
from utils.detecting import check_distance_between_knee_and_sholder, isBalance, isReadyVisibility, drawtext, update_history, check_view
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2
class squatService(exercise_Service):
    down_standard = 120
    up_standard = 160
    good_standard = 60
    bad_standard = 30
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService):
        super().__init__(draw,pose,capture)
        self.history_origin_squat = []
        self.history_distance_knee = []
        self.history_distance_shoulder = []

        # return super().show_analyst(frame)
    
    def run_estimate(self,pose_landmark,frame):
        data = self.pose.get_landmark(pose_landmark)
        
        left_knee = data["left_knee"]
        right_knee = data["right_knee"]
        right_hip = data["right_hip"]
        left_hip = data["left_hip"]
        right_ankle =data["right_ankle"]
        left_ankle = data["left_ankle"]
        left_shoulder = data['left_shoulder']
        right_shoulder = data['right_shoulder']

        right_ankle_px = convert_to_px(right_ankle,frame)
        right_hip_px =  convert_to_px(right_hip,frame)
        right_knee_px =  convert_to_px(right_knee,frame)
        left_ankle_px = convert_to_px(left_ankle,frame)
        left_hip_px =  convert_to_px(left_hip,frame)
        left_knee_px =  convert_to_px(left_knee,frame)
    
        if not isReadyVisibility(left_ankle,left_hip,left_knee,right_ankle,right_hip,right_knee,right_shoulder,left_shoulder):
            return
        self.draw.draw_line(frame,left_ankle_px,left_knee_px,(0,255,0))
        self.draw.draw_line(frame,left_hip_px,left_knee_px,(0,255,0))
        self.draw.draw_line(frame,right_ankle_px,right_knee_px,(0,255,0))
        self.draw.draw_line(frame,right_hip_px,right_knee_px,(0,255,0))

        knee_origin_left = goc_tai_tham_so_thu_nhat(left_knee,left_ankle,left_hip)
        knee_origin_right = goc_tai_tham_so_thu_nhat(right_knee,right_ankle,right_hip)
    # lam tron thoi chu co cai deo gi
        knee_origin_left = round(knee_origin_left,2) 
        knee_origin_right = round(knee_origin_right,2)
        self.draw.draw_origin_at_intersection(frame,knee_origin_left,knee_origin_right,left_knee_px,right_knee_px,(0,0,255)) 
        origin = (knee_origin_left+knee_origin_right)/2.0
        
        self.squat_counting(origin,pose_landmark)
    def squat_counting(self, origin,pose_landmark):
        data = self.pose.get_landmark(pose_landmark)
        left_knee = data["left_knee"]
        right_knee = data["right_knee"]
        left_shoulder = data['left_shoulder']
        right_shoulder = data['right_shoulder']
        distance_knee = calculating_distance(left_knee,right_knee)
        distance_shoulder = calculating_distance(left_shoulder,right_shoulder)
        update_history(self.history_distance_shoulder,distance_shoulder)
        update_history(self.history_distance_knee,distance_knee)
        update_history(self.history_origin_squat,origin)
        if origin<self.down_standard:
            if isBalance(self.history_origin_squat) and self.isEstimate:
                if origin < self.bad_standard:
                    self.estimate = "bad"
                    self.count_total+=1
                    self.require = f"Lower than threshold!"
                elif origin< self.good_standard:
                    if check_distance_between_knee_and_sholder(self.history_distance_knee,self.history_distance_shoulder):
                        self.estimate = "good"
                        self.count_good+=1
                        self.count_total+=1
                        self.require = "good form detected!"
                    else:
                        self.estimate = "Stance is too narrow!"
                        self.count_total+=1
                        self.require = "Widen your stance!"
                else:
                    self.count_total+=1
                    self.require = f"Higher than threshold!"
                    self.estimate = "high"
                self.isEstimate = False
                self.state = "down"
        elif origin>self.up_standard and self.state=="down":
            self.state = "up"
            # print(f"rep {self.}")
            self.isEstimate = True
            record = {
            "count" : self.count_total,
            "estimate" : self.estimate,
            "require" : self.require         
            }
            self.record_couting.append(record)
            self.estimate="estimate"
        else:
            record = {
            "count" : self.count_total,
            "estimate" : self.estimate,
            "require" : self.require         
            }
            self.record_couting.append(record)