from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh, convert_to_px
from utils.detecting import  isBalance, isReadyVisibility, update_history, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2
class bicep_service(exercise_Service):
    # Ngưỡng duỗi tay (để bắt đầu hoặc kết thúc 1 rep)
    down_standard = 160  
    # Ngưỡng co tay (để tính là đã hoàn thành động tác đi lên)
    up_standard = 50     
    
    # Tiêu chuẩn đánh giá form
    good_standard = 45   # Co sâu dưới 45 độ là rất tốt
    bad_standard = 90    # Co chưa tới 90 độ là form nông (bad)

    def __init__(self, draw: DrawingService, pose: PoseDetector, capture: VideoService, data):    
        super().__init__(draw, pose, capture, data)
        self.history_origin = [] # Đổi tên cho tổng quát
        # Trạng thái ban đầu nên là "down" (đang duỗi tay)
        self.state = "down" 

    def run_estimate(self, pose_landmark, frame):
        data = get_landmark(pose_landmark)
        print("here")
        # Lấy các điểm cần thiết
        left_shoulder = data["left_shoulder"]
        right_shoulder = data["right_shoulder"]
        left_elbow = data["left_elbow"]
        right_elbow = data["right_elbow"]
        left_wrist = data["left_wrist"]
        right_wrist = data["right_wrist"]

        # Kiểm tra độ hiển thị của các điểm
        left_ready = isReadyVisibility(left_shoulder, left_elbow, left_wrist)
        right_ready = isReadyVisibility(right_shoulder, right_elbow, right_wrist)
        
        if not (left_ready or right_ready):
            return False    

        # Chọn tay có độ hiển thị (visibility) tốt nhất để tính toán
        origin = self.choose_arm(right_elbow, right_shoulder, right_wrist, 
                                 left_elbow, left_shoulder, left_wrist)

        update_history(self.history_origin, origin)

        # LOGIC ĐẾM REP (Ngược với Push-up/Squat)
        # 1. Nếu đang ở trạng thái duỗi (down) và co tay lên quá ngưỡng up_standard
        if origin < self.up_standard and self.state == "down":
            if isBalance(self.history_origin) and self.isEstimate:
                self.evaluate_form(origin)
                self.isEstimate = False # Khóa lại để không đếm trùng trong 1 lần co
                self.state = "up"
        
        # 2. Nếu đang ở trạng thái co (up) và duỗi tay ra quá ngưỡng down_standard
        elif origin > self.down_standard and self.state == "up":
            self.isEstimate = True # Sẵn sàng cho rep tiếp theo
            record = {
                "count": self.count_total,
                "estimate": self.estimate,
                "require": self.require,
                "origin": origin,
            }
            self.state = "down"
            self.record_couting.append(record)

        # Cập nhật dữ liệu hiển thị lên UI
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
        # Đối với Bicep, origin càng nhỏ (góc hẹp) thì form càng tốt
        if origin <= self.good_standard:
            self.estimate = "good"
            self.count_good += 1
            self.count_total += 1
            self.require = "Tuyệt vời! Co tay rất sâu."
        elif origin <= self.bad_standard:
            self.estimate = "normal"
            self.count_total += 1
            self.require = "Tạm được, hãy cố co tay sâu hơn."
        else:
            self.estimate = "bad"
            self.count_total += 1
            self.require = "Form nông! Hãy co tay lên cao hơn."
        
        self.origin = origin
    def choose_arm(self,right_elbow,right_shoulder,right_wrist,left_elbow,left_shoulder,left_wrist):
        left_score = self.check_visibility(left_elbow,left_shoulder,left_wrist)
        right_score = self.check_visibility(right_elbow,right_shoulder,right_wrist)
        if(left_score<right_score):
            right_elbow_origin = goc_tai_tham_so_thu_nhat(right_elbow,right_shoulder,right_wrist)
            return right_elbow_origin
        else:
            left_elbow_origin = goc_tai_tham_so_thu_nhat(left_elbow,left_shoulder,left_wrist)
            return left_elbow_origin
    
    def check_visibility(self,a,b,c):
        return a.visibility+b.visibility+c.visibility