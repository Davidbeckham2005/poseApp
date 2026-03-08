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
    good_standard = 90  
    bad_standard = 32
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
        print(left_elbow_px)
        if not isReadyVisibility(left_elbow,right_elbow,left_shoulder,right_shoulder,left_wrist,right_wrist):
            return
        
        self.draw.draw_line(frame,left_shoulder_px,left_elbow_px,(0,255,0))
        self.draw.draw_line(frame,right_shoulder_px,right_elbow_px,(0,255,0))
        self.draw.draw_line(frame,left_wrist_px,left_elbow_px,(0,255,0))
        self.draw.draw_line(frame,right_wrist_px,right_elbow_px,(0,255,0))

        left_elbow_origin = goc_tai_tham_so_thu_nhat(left_elbow,left_shoulder,left_wrist)
        right_elbow_origin = goc_tai_tham_so_thu_nhat(right_elbow,right_shoulder,right_wrist)
        
        origin = round((left_elbow_origin+right_elbow_origin/2),2)
        # cv2.circle(frame, point_px, 8, (255, 255, 255), cv2.FILLED)
        # cv2.circle(frame, point_px, 10, (0, 255, 0), 2)
        cv2.putText(frame,str(left_elbow_origin),(left_elbow_px[0]-10,left_elbow_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.putText(frame,str(right_elbow_origin),(right_elbow_px[0]-10,right_elbow_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        # self.draw.draw_origin_at_intersection(frame,left_elbow_origin,right_elbow_origin,left_elbow_px,right_elbow_px,(0,0,255))
        
        # shoulder_y = trungbinh(left_shoulder.y, right_shoulder.y)
        # hip_y = trungbinh(left_hip.y,right_hip.y)

        update_history(self.history_origin_pushup,origin)
        # update_history(self.history_y_hip,hip_y)
        # update_history(self.history_y_shoulder,shoulder_y)
        if origin < self.down_standard:
            print(origin)
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
        