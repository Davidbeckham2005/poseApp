"""
Warmup Shoulder Stretch Service
Simplified shoulder stretch detection with relaxed form standards for warm-up phase
Maps arm movements and shoulder rotations
"""

from utils.calc import goc_tai_tham_so_thu_nhat, trungbinh, convert_to_px
from utils.detecting import isBalance, isReadyVisibility, update_history, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service
import cv2

class warmup_shoulder_stretch_service(exercise_Service):
    # Relaxed thresholds for warm-up (easier to achieve)
    down_standard = 100      # More relaxed shoulder extension
    up_standard = 130        # Lower threshold for arm raise
    good_standard = 75       # Easy good form standard
    bad_standard = 20        # Very relaxed bad threshold
    
    def __init__(self, draw: DrawingService, pose: PoseDetector, capture: VideoService, data):    
        super().__init__(draw, pose, capture, data)
        self.history_shoulder_stretch = []
        self.history_y_shoulder = []
    
    def run_estimate(self, pose_landmark, frame):
        data = get_landmark(pose_landmark)
        left_shoulder = data["left_shoulder"]
        right_shoulder = data["right_shoulder"]
        left_elbow = data["left_elbow"]
        right_elbow = data["right_elbow"]
        left_wrist = data["left_wrist"]
        right_wrist = data["right_wrist"]
        
        # Check if arms are visible
        left_ready = isReadyVisibility(left_shoulder, left_elbow, left_wrist)
        right_ready = isReadyVisibility(right_shoulder, right_elbow, right_wrist)
        
        if not (left_ready or right_ready):
            return False    
        
        # Calculate shoulder angle
        origin = self.choose_arm(
            right_elbow, right_shoulder, right_wrist,
            left_elbow, left_shoulder, left_wrist
        )
        
        # Track shoulder y position
        shoulder_y = trungbinh(left_shoulder.y, right_shoulder.y)
        update_history(self.history_y_shoulder, shoulder_y)
        update_history(self.history_shoulder_stretch, origin)
        
        # Detect movement phases
        if origin < self.down_standard:
            if isBalance(self.history_shoulder_stretch) and self.isEstimate:
                self.evaluate_form(origin)
                self.isEstimate = False
                self.state = "down"
        elif origin > self.up_standard and self.state == "down":
            self.isEstimate = True
            self.count_total += 1
            # Simple good form detection
            if origin < self.good_standard:
                self.count_good += 1
                self.estimate = "good"
            else:
                self.estimate = "estimate"
            
            record = {
                "count": self.count_total,
                "estimate": self.estimate,
                "require": self.require,
            }
            self.state = "up"
            self.record_couting.append(record)
        
        self.data_on_rep = {
            "total": self.count_total,
            "estimate": self.estimate,
            "good": self.count_good,
            'state': self.state,
        }
        return True
    
    def evaluate_form(self, origin):
        if origin < self.bad_standard:
            self.estimate = "bad"
            self.require = "Extend arms more!"
        elif origin < self.good_standard:
            self.estimate = "good"
            self.require = "Good form!"
        else:
            self.estimate = "okay"
            self.require = "Keep going!"
    
    def choose_arm(self, right_elbow, right_shoulder, right_wrist, left_elbow, left_shoulder, left_wrist):
        """Choose the arm with better visibility"""
        right_angle = goc_tai_tham_so_thu_nhat(right_elbow, right_shoulder, right_wrist)
        left_angle = goc_tai_tham_so_thu_nhat(left_elbow, left_shoulder, left_wrist)
        
        right_angle = round(right_angle, 2)
        left_angle = round(left_angle, 2)
        
        # Return average of both arms
        return (right_angle + left_angle) / 2.0
