"""
Warmup Jumping Jack Service
Simplified jumping jack detection with relaxed form standards for warm-up phase
Tracks vertical movement, arm extension, and leg positioning
"""

from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh, calculating_accuracy, calc_time, calculating_caloris
from utils.detecting import isBalance, isReadyVisibility, update_history, check_y_hip_and_shoulder, drawtext, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2

class warmup_jumping_jack_service(exercise_Service):
    # Very relaxed thresholds for warm-up jumping jacks
    down_standard = 40       # Very relaxed arms down position
    up_standard = 70         # Very relaxed arms up position
    good_standard = 85       # Easy good form standard
    bad_standard = 100       # Very relaxed bad threshold
    
    def __init__(self, draw: DrawingService, pose: PoseDetector, capture: VideoService, data):   
        super().__init__(draw, pose, capture, data)
        self.history_jumping_jack = []
        self.history_y_hip = []
        self.history_y_shoulder = []
        self.state = "down"
    
    def run_estimate(self, pose_landmark, frame):
        """Track jumping jack movement"""
        # Count every frame processed
        # self.count_total += 1
        
        data = get_landmark(pose_landmark)
        data_px = self.pose.get_for_push_up_px(frame, pose_landmark)
        
        left_shoulder = data["left_shoulder"]
        right_shoulder = data["right_shoulder"]
        left_elbow = data["left_elbow"]
        right_elbow = data["right_elbow"]
        left_wrist = data["left_wrist"]
        right_wrist = data["right_wrist"]
        left_hip = data["left_hip"]
        right_hip = data["right_hip"]
        
        # Calculate shoulder angles
        left_shoulder_angle = goc_tai_tham_so_thu_nhat(left_shoulder, left_elbow, left_hip)
        right_shoulder_angle = goc_tai_tham_so_thu_nhat(right_shoulder, right_elbow, right_hip)
        
        # Average angle represents arm position
        origin = (left_shoulder_angle + right_shoulder_angle) / 2.0
        
        # Track hip and shoulder y positions
        shoulder_y = trungbinh(left_shoulder.y, right_shoulder.y)
        hip_y = trungbinh(left_hip.y, right_hip.y)
        
        update_history(self.history_jumping_jack, origin)
        update_history(self.history_y_hip, hip_y)
        update_history(self.history_y_shoulder, shoulder_y)
        
        # Detect jumping jacks movement pattern
        if origin > self.down_standard and self.estimate and isBalance(self.history_jumping_jack):
            if origin < self.good_standard:
                self.estimate = "good"
                self.count_good += 1
                self.require = "Good form!"
            else:
                self.estimate = "okay"
                self.require = "Keep going!"
            
            self.isEstimate = False
            self.state = "up"
        elif origin <= self.down_standard and self.state == "up":
            self.state = "down"
            self.isEstimate = True
        
        self.data_on_rep = {
            "total": self.count_total,
            "estimate": self.estimate,
            "good": self.count_good,
            "state": self.state,
        }
        return True
