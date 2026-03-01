from sqlalchemy import false

from utils.calc import calc_time, goc_tai_tham_so_thu_nhat, convert_to_px,calculating_accuracy, calculating_distance, get_form
from utils.detecting import check_distance_between_knee_and_sholder, isBalance, isReadyVisibility, drawtext, update_history, check_view
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
import cv2
class exercise_Service:
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService,data):
        self.count_total = 0
        self.count_good = 0
        self.require = ""
        self.estimate = "estimate. . ."
        self.state = "up"
        self.pose = pose
        self.draw = draw
        self.capture = capture
        self.record_couting = []
        self.max_frame = 10
        self.current_frame = 0
        self.type = data.type
        # setting
        self.isMake_Result = True   
        self.isDrawing = data.isDrawing
        self.isAnalyst = data.isAnalyst
        self.isCheck_view = data.isCheck_view
        self.Analyst_FPS = data.Analyst_FPS
        self.Analyst_state = data.Analyst_state
        self.Analyst_count = data.Analyst_count
        self.Analyst_count_good = data.Analyst_count_good
        self.Analyst_estimate = data.Analyst_estimate
        self.isEstimate = True
        self.history_x_sholder = []
        self.history_x_hip = []
        self.origin = 0
        self.time_start = 0
        self.time_end  = 0
    def check_view(self,pose_landmark):
        result_check_oriantation = self.pose.check_oriantation(pose_landmark)
        update_history(self.history_x_hip,result_check_oriantation['hip_dis'])
        update_history(self.history_x_sholder,result_check_oriantation['shoulder_dis'])
        view = check_view(self.history_x_hip,self.history_x_sholder)
        return view
    
    def show_analyst(self,frame):
        if self.Analyst_state:
            drawtext(frame,(20,150),f"State: {str(self.state)}",(128,0,0))
        if self.Analyst_FPS:
            drawtext(frame,(20,300),f'FPS: {str(self.capture.getFPS())}',(0,128,128))
        if self.Analyst_count:
            drawtext(frame,(20,100),f"Reps: {str(self.count_total)}",(128,0,0))
        if self.Analyst_estimate:
            drawtext(frame,(20,250),self.estimate,(128,0,0))
        if self.Analyst_count_good:
            drawtext(frame,(20,200),f'Good: {str(self.count_good)}',(128,0,0))
        cv2.line(frame,(310,0),(310,310),(255,0,0),5)
        cv2.line(frame,(0,310),(310,310),(255,0,0),5)

    def run_detection(self,frame):
        self.push_frame()
        result = self.pose.run_process(frame)
        if result.pose_landmarks:
            pose_landmark = result.pose_landmarks[0]
            drawtext(frame,(10,50),f"Exercise: {self.type}",(0,0,255))
            if self.isAnalyst:
                self.show_analyst(frame)
            # if self.isCheck_view:
            #     if check_view:
            #         drawtext(frame,(10,50),"view: Horizontal",(0,0,255))
            #     else:
            #         drawtext(frame,(10,50),"View: Vertical",(0,0,255))
            if self.isDrawing:
                self.draw.draw_skeleton(frame,pose_landmark)
            if self.isMake_Result:
                self.capture.makeResult(frame)  
            self.run_estimate(pose_landmark,frame)
    # def set_setting(self,input):
    #     self.isDrawing = input.isDrawing
    #     self.isAnalyst = input.isAnalyst
    #     self.isCheck_view = input.isCheck_view
    #     self.Analyst_FPS = input.Analyst_FPS
    #     self.Analyst_state = input.Analyst_state
    #     self.Analyst_count = input.Analyst_count
    #     self.Analyst_count_good = input.Analyst_count_good
    #     self.Analyst_estimate = input.Analyst_estimate
    def run_estimate(self,pose_landmark,frame):
        pass
    def getResult(self):
        accuracy = calculating_accuracy(self.count_good,self.count_total)
        data = {
            "total" : self.count_total,
            "good" : self.count_good,
            "accuracy" : accuracy,
            "record" : self.record_couting,
            "src_output": self.capture.get_file_name(), 
            "size" :self.capture.get_size(),
            "form" :get_form(accuracy),
            "time" : calc_time(),
            "time_video" : self.capture.get_time_video()
        }
        return data
    def getResult_live(self):
        accuracy = calculating_accuracy(self.count_good,self.count_total)
        data = {
            "total" : self.count_total,
            "good" : self.count_good,
            "accuracy" : accuracy,
            "record" : self.record_couting,
            "form" :get_form(accuracy),
         }
        return data   
    def show_camera_not_make_video(self):
        self.isMake_Result = False

    def push_frame(self):
        self.current_frame+=1