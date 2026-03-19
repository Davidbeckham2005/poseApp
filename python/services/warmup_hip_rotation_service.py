"""
Warmup Hip Rotation Service
Simplified hip rotation detection with relaxed form standards for warm-up phase
Tracks knee bending and hip movement
"""

from utils.calc import goc_tai_tham_so_thu_nhat, convert_to_px
from utils.detecting import isBalance, isReadyVisibility, update_history, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2

class warmup_hip_rotation_service(exercise_Service):
    # Relaxed thresholds for warm-up
    down_standard = 80       # More relaxed bend threshold
    up_standard = 140        # Lower threshold for straightening
    good_standard = 100      # Easy good form standard
    bad_standard = 50        # Very relaxed bad threshold
    
    def __init__(self, draw: DrawingService, pose: PoseDetector, capture: VideoService, data):
        super().__init__(draw, pose, capture, data)
        self.history_hip_rotation = []
    
    def run_estimate(self, pose_landmark, frame):
        data = get_landmark(pose_landmark)
        
        left_knee = data["left_knee"]
        right_knee = data["right_knee"]
        right_hip = data["right_hip"]
        left_hip = data["left_hip"]
        right_ankle = data["right_ankle"]
        left_ankle = data["left_ankle"]
        
        # Verify visibility of required joints
        if not isReadyVisibility(
            left_ankle, left_hip, left_knee,
            right_ankle, right_hip, right_knee
        ):
            return False
        
        # Calculate knee angles
        knee_origin_left = goc_tai_tham_so_thu_nhat(left_knee, left_ankle, left_hip)
        knee_origin_right = goc_tai_tham_so_thu_nhat(right_knee, right_ankle, right_hip)
        
        knee_origin_left = round(knee_origin_left, 2) 
        knee_origin_right = round(knee_origin_right, 2)
        
        # Use the maximum angle (deepest bend)
        origin = max(knee_origin_left, knee_origin_right)
        
        self.hip_rotation_counting(origin, data)
        return True
    
    def hip_rotation_counting(self, origin, data):
        update_history(self.history_hip_rotation, origin)
        
        if origin < self.down_standard:
            if isBalance(self.history_hip_rotation) and self.isEstimate:
                self.evaluate_form(origin)
                self.isEstimate = False
                self.state = "down"
        elif origin > self.up_standard and self.state == "down":
            self.state = "up"
            self.count_total += 1
            self.isEstimate = True
            
            record = {
                "count": self.count_total,
                "estimate": self.estimate,
                "require": self.require,
            }
            self.record_couting.append(record)
            self.estimate = "estimate"
        
        self.data_on_rep = {
            "total": self.count_total,
            "estimate": self.estimate,
            "good": self.count_good,
            "state": self.state,
        }
        return True
    
    def evaluate_form(self, origin):
        if origin < self.bad_standard:
            self.estimate = "bad"
            self.require = "Bend more!"
        elif origin < self.good_standard:
            self.estimate = "good"
            self.count_good += 1           
            self.require = "Good rotation!"
        else:
            self.require = "Keep rotating!"
            self.estimate = "okay"
