from utils.calc import goc_tai_tham_so_thu_nhat, convert_to_px
from utils.detecting import isBalance, isReadyVisibility, update_history
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2
class lungService(exercise_Service):
    down_standard = 100
    up_standard = 160
    good_standard = 110
    bad_standard = 60
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService,data):
        super().__init__(draw,pose,capture,data)
        self.history_origin_lungue = []
    def run_estimate(self,pose_landmark,frame):
        data = self.pose.get_landmark(pose_landmark)
        # print(data)
        left_knee = data["left_knee"]
        right_knee = data["right_knee"]
        right_hip = data["right_hip"]
        left_hip = data["left_hip"]
        right_ankle =data["right_ankle"]
        left_ankle = data["left_ankle"]
        

        right_knee_px =  convert_to_px(right_knee,frame)
        left_knee_px =  convert_to_px(left_knee,frame)
    
        if not isReadyVisibility(left_ankle,left_hip,left_knee,right_ankle,right_hip,right_knee):
            return
       

        knee_origin_left = goc_tai_tham_so_thu_nhat(left_knee,left_ankle,left_hip)
        knee_origin_right = goc_tai_tham_so_thu_nhat(right_knee,right_ankle,right_hip)

        knee_origin_left = round(knee_origin_left,2) 
        knee_origin_right = round(knee_origin_right,2)
        origin = max(knee_origin_left,knee_origin_right)
        cv2.putText(frame,str(origin),(left_knee_px[0]-10,left_knee_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.putText(frame,str( origin),(right_knee_px[0]-10,right_knee_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        origin = (knee_origin_left+knee_origin_right)/2.0
        self.lungue_counting(origin,data)
    def lungue_counting(self, origin,data):
        update_history(self.history_origin_lungue,origin)
        balance = isBalance(self.history_origin_lungue)
        if origin<self.down_standard:
            # print(self.history_origin_lungue)
            if balance and self.isEstimate:
                self.evaluate_form(origin)
                # self.time_start = self.capture.get_current_time_video(self.current_frame)
                self.isEstimate = False
                self.state = "down"
        elif origin>self.up_standard and self.state=="down":
            self.state = "up"
            # self.time_end = self.capture.get_current_time_video(self.current_frame)
            self.count_total +=1
            self.isEstimate = True
            self.data_on_rep = {
                "total" : self.count_total,
                "estimate" : self.estimate,
                "good" : self.count_good,
            }
            record = {
            "count" : self.count_total,
            "estimate" : self.estimate,
            "require" : self.require,
            "start" : self.time_start,
            "end" : self.time_end         
            }
            self.record_couting.append(record)
            self.estimate="estimate"

    def evaluate_form(self,origin):
        if origin<self.bad_standard:
            self.estimate = "bad"
            self.require = f"Lower than threshold!"
        elif origin< self.good_standard:
            self.estimate = "good"
            self.count_good+=1           
            self.require = "good form detected!"
        else:
            self.require = f"Higher than threshold!"
            self.estimate = "high"

            