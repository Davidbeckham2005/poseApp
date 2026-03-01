from utils.calc import get_form, goc_tai_tham_so_thu_nhat, trungbinh, calculating_accuracy, calc_time, get_time_video
from utils.detecting import  isBalance, isReadyVisibility, update_history,check_y_hip_and_shoulder, drawtext
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2

class plankService(exercise_Service):
    down_standard = 50
    up_standard = 60
    good_standard = 80
    bad_standard = 95 
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService,data):   
        self.correct_time = 0  
        self.total_time = 0
        super().__init__(draw,pose,capture,data)
        self.history_origin_plank = []
        self.history_y_hip = []
        self.history_y_shoulder = []
        self.state = "down"
        
    def get_total_time(self):
        fps = self.capture.getFPS()
        self.total_time = self.count_total/fps
        return round(self.total_time,2)
    def get_correct_time(self):
        fps = self.capture.getFPS()
        self.correct_time = self.count_good/fps
        return round(self.correct_time,2)
    def show_analyst(self, frame):
        drawtext(frame,(20,250),self.estimate,(128,0,0))
        drawtext(frame,(20,300),f'FPS: {str(self.capture.getFPS())}',(0,128,128))
        drawtext(frame,(20,150),f"Time: {str(self.get_total_time())}s",(128,0,0))
        drawtext(frame,(20,100),f"Correct Time: {str(self.get_correct_time())}s",(128,0,0))
        drawtext(frame,(20,200),f"State: {self.state}",(128,0,0))
        cv2.line(frame,(340,0),(340,340),(255,0,0),5)
        cv2.line(frame,(0,340),(340,340),(255,0,0),5)
    def run_estimate(self, pose_landmark, frame):
        self.count_total+=1
        # print(self.count_good,self.count_total)
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
        
        # if not isReadyVisibility(left_elbow,right_elbow,left_shoulder,right_shoulder,left_wrist,right_wrist):
        #     return
        
        self.draw.draw_line(frame,left_shoulder_px,left_elbow_px,(0,255,0))
        self.draw.draw_line(frame,right_shoulder_px,right_elbow_px,(0,255,0))
        self.draw.draw_line(frame,left_wrist_px,left_elbow_px,(0,255,0))
        self.draw.draw_line(frame,right_wrist_px,right_elbow_px,(0,255,0))

        left_shoulder_origin = goc_tai_tham_so_thu_nhat(left_shoulder,left_elbow,left_hip)
        right_shoulder_origin = goc_tai_tham_so_thu_nhat(right_shoulder,right_elbow,right_hip)
        
        origin = (left_shoulder_origin+right_shoulder_origin)/2.0

        self.draw.draw_origin_at_intersection(frame,left_shoulder_origin,right_shoulder_origin,left_shoulder_px,right_shoulder_px,(0,0,255))
        
        shoulder_y = trungbinh(left_shoulder.y, right_shoulder.y)
        hip_y = trungbinh(left_hip.y,right_hip.y)

        update_history(self.history_origin_plank,origin)
        update_history(self.history_y_hip,hip_y)
        update_history(self.history_y_shoulder,shoulder_y)
        
        if origin>self.down_standard and self.estimate and isBalance(self.history_origin_plank):
                if origin < self.good_standard:
                    self.estimate = "bad"
                    self.require = f"Lower than threshold!"
                elif origin< self.bad_standard:
                    if check_y_hip_and_shoulder(self.history_y_hip,self.history_y_shoulder):
                        self.estimate = "good"
                        self.count_good+=1
                        self.require = "good form detected!"
                    else:
                        self.estimate = "Hip is too high!"
                        self.require = "Lower your hip!"
                else:
                    self.require = f"Higher than threshold!"
                    self.estimate = "high"
                self.isEstimate = False
                self.state = "up"
        elif origin<=self.down_standard and self.state=="up":
            self.state = "down"
            self.isEstimate = True
            self.estimate="estimate"
            # record = {
            # "count" : self.count_total,
            # "estimate" : self.estimate,
            # "require" : self.require         
            # }
            # self.record_couting.append(record)
    def getResult(self):
        accuracy = calculating_accuracy(self.count_good,self.count_total)
        data = {
            "total" : round(self.total_time,2),
            "good" : round(self.correct_time,2),
            "accuracy" : accuracy,
            "record" : self.record_couting,
            "src_output": self.capture.get_file_name(), 
            "size": self.capture.get_size(),
            "form" : get_form(accuracy),
            "time" : calc_time(),
            "time_video" : get_time_video()

        }
        return data