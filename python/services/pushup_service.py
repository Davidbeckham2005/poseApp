from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh
from utils.detecting import  isBalance, isReadyVisibility, update_history,check_y_hip_and_shoulder, drawtext
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2
class pushupService(exercise_Service):
    down_standard = 130
    up_standard = 160
    good_standard = 90  
    bad_standard = 60
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService,data):    
        super().__init__(draw,pose,capture,data)
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
        # print(left_elbow_px)
        if not isReadyVisibility(left_elbow,right_elbow,left_shoulder,right_shoulder,left_wrist,right_wrist):
            return
        

        # left_elbow_origin = goc_tai_tham_so_thu_nhat(left_elbow,left_shoulder,left_wrist)
        # right_elbow_origin = goc_tai_tham_so_thu_nhat(right_elbow,right_shoulder,right_wrist)
        
        origin = self.choose_arm(right_elbow,right_shoulder,right_wrist,left_elbow,left_shoulder,left_wrist)
       
        cv2.putText(frame,str(origin),(left_elbow_px[0]-10,left_elbow_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.putText(frame,str(origin),(right_elbow_px[0]-10,right_elbow_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
      

        update_history(self.history_origin_pushup,origin)
        if origin < self.down_standard:
            if isBalance(self.history_origin_pushup) and self.isEstimate:
                self.evaluate_form(origin)
                # self.time_start = self.capture.get_current_time_video(self.current_frame)
                self.isEstimate = False
                self.state = "down"
        elif origin>self.up_standard and self.state=="down":
            self.state = "up"
            # self.time_end = self.capture.get_current_time_video(self.current_frame)
            self.isEstimate = True
            record = {
            "count" : self.count_total,
            "estimate" : self.estimate,
            "require" : self.require,
            "origin" : self.origin,
            }
            self.data_on_rep = {
                "total" : self.count_total,
                "estimate" : self.estimate,
                "good" : self.count_good
            }
            self.record_couting.append(record)
            self.estimate="estimate"
    def evaluate_form(self,origin):
        if origin < self.bad_standard:
            self.estimate = "bad"
            self.count_total+=1
            self.require = f"Lower than threshold!"
            self.origin = origin
        elif origin< self.good_standard:
            self.estimate = "good"
            self.count_good+=1
            self.count_total+=1
            self.require = "good form detected!"
            self.origin = origin             
        else:
            self.count_total+=1
            self.require = f"Higher than threshold!"
            self.estimate = "high"
            self.origin = origin
        
    def check_visibility(self,a,b,c):
        return a.visibility+b.visibility+c.visibility
    
    def choose_arm(self,right_elbow,right_shoulder,right_wrist,left_elbow,left_shoulder,left_wrist):
        left_score = self.check_visibility(left_elbow,left_shoulder,left_wrist)
        right_score = self.check_visibility(right_elbow,right_shoulder,right_wrist)
        if(left_score<right_score):
            right_elbow_origin = goc_tai_tham_so_thu_nhat(right_elbow,right_shoulder,right_wrist)
            return right_elbow_origin
        else:
            left_elbow_origin = goc_tai_tham_so_thu_nhat(left_elbow,left_shoulder,left_wrist)
            return left_elbow_origin