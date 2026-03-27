from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh, convert_to_px
from utils.detecting import  isBalance, isReadyVisibility, update_history, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2
class ShoulderPressServices(exercise_Service):
    # Ngưỡng tay co lại ở vai (chuẩn bị đẩy)
    down_standard = 110  
    # Ngưỡng tay duỗi thẳng trên đầu
    up_standard = 150     
    good_standard = 170   # Đẩy thẳng tay hoàn toàn
    bad_standard = 140    # Đẩy nửa vời

    def __init__(self, draw, pose, capture, data):    
        super().__init__(draw, pose, capture, data)
        self.history_origin = []

    def run_estimate(self, pose_landmark, frame):
        data = get_landmark(pose_landmark)
        # Các điểm: Shoulder, Elbow, Wrist
        origin = self.choose_arm(data["right_elbow"], data["right_shoulder"], data["right_wrist"], 
                                 data["left_elbow"], data["left_shoulder"], data["left_wrist"])
        update_history(self.history_origin, origin)

        # Đẩy lên (Up)
        if origin > self.up_standard and self.state == "down":
            if isBalance(self.history_origin) and self.isEstimate:
                self.evaluate_form(origin)
                self.isEstimate = False
                self.state = "up"
        
        # Hạ xuống (Down)
        elif origin < self.down_standard and self.state == "up":
            self.isEstimate = True
            self.state = "down"
            self.record_couting.append({"count": self.count_total, "estimate": self.estimate})
        self.data_on_rep = {
            "total": self.count_total,
            "estimate": self.estimate,
            "good": self.count_good,
            'state': self.state,
            "origin": origin,
            "good_standard": self.good_standard,
            "up_standard": self.up_standard, # Ngưỡng để tính là hoàn thành lượt lên
        }
        
        return True

    def evaluate_form(self, origin):
        if origin >= self.good_standard:
            self.estimate, self.require = "good", "Đẩy vai rất tốt!"
            self.count_good += 1
        elif origin >= self.bad_standard:
            self.estimate, self.require = "normal", "Hãy đẩy thẳng tay thêm."
        else:
            self.estimate, self.require = "bad", "Tay chưa đủ độ cao!"
        self.count_total += 1
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