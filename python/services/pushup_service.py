from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh, convert_to_px
from utils.detecting import  isBalance, isReadyVisibility, update_history, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
class pushupService(exercise_Service):
    down_standard = 130
    up_standard = 140
    good_standard = 90  
    bad_standard = 32
    def __init__(self,draw: DrawingService, pose: PoseDetector, capture :VideoService,data):    
        super().__init__(draw,pose,capture,data)
        self.history_origin_pushup = []
        self.history_y_hip = []
        self.history_y_shoulder = []
    
    def run_estimate(self, pose_landmark, frame):
        # return super().run_estimate(pose_landmark, frame)
        data = get_landmark(pose_landmark)
        left_shoulder=data["left_shoulder"]
        right_shoulder=data["right_shoulder"]
        left_elbow=data["left_elbow"]
        right_elbow=data["right_elbow"]
        left_wrist=data["left_wrist"]
        right_wrist=data["right_wrist"]
        left_hip = data["left_hip"]
        right_hip = data["right_hip"]
        # left_shoulder_px = convert_to_px(left_shoulder, frame)
        # right_shoulder_px = convert_to_px(right_shoulder, frame)
        # left_elbow_px = convert_to_px(left_elbow, frame)
        # right_elbow_px = convert_to_px(right_elbow, frame)
        # left_wrist_px = convert_to_px(left_wrist, frame)
        # right_wrist_px = convert_to_px(right_wrist, frame)
        # print(left_elbow_px)
        left_ready = isReadyVisibility(left_shoulder, left_elbow, left_wrist)
        right_ready = isReadyVisibility(right_shoulder, right_elbow, right_wrist)
        if not (left_ready or right_ready):
            return False    
        

        # left_elbow_origin = goc_tai_tham_so_thu_nhat(left_elbow,left_shoulder,left_wrist)
        # right_elbow_origin = goc_tai_tham_so_thu_nhat(right_elbow,right_shoulder,right_wrist)
        
        origin = self.choose_arm(right_elbow,right_shoulder,right_wrist,left_elbow,left_shoulder,left_wrist)
       
        # cv2.putText(frame,str(origin),(left_elbow_px[0]-10,left_elbow_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        # cv2.putText(frame,str(origin),(right_elbow_px[0]-10,right_elbow_px[1]+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
      

        update_history(self.history_origin_pushup,origin)
        if origin < self.down_standard:
            if isBalance(self.history_origin_pushup) and self.isEstimate:
                self.evaluate_form(origin)
                # self.time_start = self.capture.get_current_time_video(self.current_frame)
                self.isEstimate = False
                self.state = "down"
        elif origin>self.up_standard and self.state=="down":
            
            # self.time_end = self.capture.get_current_time_video(self.current_frame)
            self.isEstimate = True
            record = {
            "count" : self.count_total,
            "estimate" : self.estimate,
            "require" : self.require,
            "origin" : self.origin,
            }
            self.state = "up"
            self.record_couting.append(record)
            self.estimate="estimate"
        self.setData_live_websocket(origin)

        return True
    def evaluate_form(self,origin):
        if origin < self.bad_standard:
            self.estimate = "bad"
            self.count_total+=1
            self.require = f"Vai quá thấp hãy giữ cao lên!"
            self.origin = origin
        elif origin< self.good_standard:
            self.estimate = "good"
            self.count_good+=1
            self.count_total+=1
            self.require = "Tốt rồi, hãy giữ tư thế này!"
            self.origin = origin             
        else:
            self.count_total+=1
            self.require = f"Cao quá, hãy giữ thấp xuống!"
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