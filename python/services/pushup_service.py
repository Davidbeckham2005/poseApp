from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh
from utils.detecting import  isBalance, isReadyVisibility, update_history,check_y_hip_and_shoulder, drawtext
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2
class pushupService(exercise_Service):
    down_standard = 110
    up_standard = 160
    good_standard = 60
    bad_standard = 32
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService):    
        super().__init__(draw,pose,capture)
        self.history_origin_pushup = []
        self.history_y_hip = []
        self.history_y_shoulder = []
    
    def run_estimate(self, pose_landmark, frame):
        # return super().run_estimate(pose_landmark, frame)
        data = self.pose.get_for_push_up(pose_landmark)
        data_px = self.pose.get_for_push_up_px(frame,pose_landmark)
        left_shoulder=data["left_shoulder"]
        right_shoulder=data["right_shoulder"]
        left_elbow=data["left_elbow"]
        right_elbow=data["right_elbow"]
        left_wrist=data["left_wrist"]
        right_wrist=data["right_wrist"]
        left_hip = data["left_hip"]
        right_hip = data["right_hip"]
        left_shoulder_px=data_px["left_shoulder_px"]
        right_shoulder_px=data_px["right_shoulder_px"]
        left_elbow_px=data_px["left_elbow_px"]
        right_elbow_px=data_px["right_elbow_px"]
        left_wrist_px=data_px["left_wrist_px"]
        right_wrist_px=data_px["right_wrist_px"]
        
        if not isReadyVisibility(left_elbow,right_elbow,left_shoulder,right_shoulder,left_wrist,right_wrist):
            return
        
        self.draw.draw_line(frame,left_shoulder_px,left_elbow_px,(0,255,0))
        self.draw.draw_line(frame,right_shoulder_px,right_elbow_px,(0,255,0))
        self.draw.draw_line(frame,left_wrist_px,left_elbow_px,(0,255,0))
        self.draw.draw_line(frame,right_wrist_px,right_elbow_px,(0,255,0))

        left_elbow_origin = goc_tai_tham_so_thu_nhat(left_elbow,left_shoulder,left_wrist)
        right_elbow_origin = goc_tai_tham_so_thu_nhat(right_elbow,right_shoulder,right_wrist)
        
        origin = (left_elbow_origin+right_elbow_origin)/2.0

        self.draw.draw_origin_at_intersection(frame,left_elbow_origin,right_elbow_origin,left_elbow_px,right_elbow_px,(0,0,255))
        
        shoulder_y = trungbinh(left_shoulder.y, right_shoulder.y)
        hip_y = trungbinh(left_hip.y,right_hip.y)

        update_history(self.history_origin_pushup,origin)
        update_history(self.history_y_hip,hip_y)
        update_history(self.history_y_shoulder,shoulder_y)

        if origin < self.down_standard:
            if isBalance(self.history_origin_pushup) and self.isEstimate:
                if origin < self.bad_standard:
                    self.estimate = "bad"
                    self.count_total+=1
                    self.require = f"Lower than threshold!"
                    self.origin = origin
                elif origin< self.good_standard:
                    if(check_y_hip_and_shoulder(self.history_y_hip,self.history_y_shoulder)): 
                        self.estimate = "good"
                        self.count_good+=1
                        self.count_total+=1
                        self.require = "good form detected!"
                        self.origin = origin             
                    else:
                        self.estimate = "Hips are too high!"
                        self.count_total+=1
                        self.require = "Lower your hips!"
                else:
                    self.count_total+=1
                    self.require = f"Higher than threshold!"
                    self.estimate = "high"
                    self.origin = origin

                self.isEstimate = False
                self.state = "down"
        elif origin>self.up_standard and self.state=="down":
            self.state = "up"
            
            self.isEstimate = True
            record = {
            "count" : self.count_total,
            "estimate" : self.estimate,
            "require" : self.require,
            "origin" : self.origin         
            }
            self.record_couting.append(record)
            self.estimate="estimate"
      
        