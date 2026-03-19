"""
Warmup Squat Service
Simplified squat detection with relaxed form standards for warm-up phase
Tracks light squatting movement with easier thresholds
"""

from utils.calc import goc_tai_tham_so_thu_nhat, convert_to_px
from utils.detecting import isBalance, isReadyVisibility, drawtext, update_history, get_landmark
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.video_services import VideoService
from services.exercise_service import exercise_Service

class warmup_squat_service(exercise_Service):
    # Very relaxed thresholds for warm-up (light movement only)
    down_standard = 130      # Very easy down position
    up_standard = 150        # Very easy up position
    good_standard = 85       # Relaxed good form standard
    bad_standard = 25        # Very relaxed bad threshold
    
    def __init__(self, draw: DrawingService, pose: PoseDetector, capture: VideoService, data):
        super().__init__(draw, pose, capture, data)
        self.history_warmup_squat = []
    
    def run_estimate(self, pose_landmark, frame):
        data = get_landmark(pose_landmark)
        
        left_knee = data["left_knee"]
        right_knee = data["right_knee"]
        right_hip = data["right_hip"]
        left_hip = data["left_hip"]
        right_ankle = data["right_ankle"]
        left_ankle = data["left_ankle"]
        left_shoulder = data['left_shoulder']
        right_shoulder = data['right_shoulder']
        
        # Verify visibility of required joints
        if not isReadyVisibility(
            left_ankle, left_hip, left_knee,
            right_ankle, right_hip, right_knee,
            right_shoulder, left_shoulder
        ):
            return False
        
        # Calculate knee angles
        knee_origin_left = goc_tai_tham_so_thu_nhat(left_knee, left_ankle, left_hip)
        knee_origin_right = goc_tai_tham_so_thu_nhat(right_knee, right_ankle, right_hip)
        
        knee_origin_left = round(knee_origin_left, 2) 
        knee_origin_right = round(knee_origin_right, 2)
        
        # Average both knees
        origin = (knee_origin_left + knee_origin_right) / 2.0
        self.warmup_squat_counting(origin, data)
        return True
    
    def warmup_squat_counting(self, origin, data):
        update_history(self.history_warmup_squat, origin)
        balance = isBalance(self.history_warmup_squat)
        
        if origin < self.down_standard:
            if balance and self.isEstimate:
                self.evaluate_form(origin)
                self.isEstimate = False
                self.state = "down"
        elif origin > self.up_standard and self.state == "down":
            self.count_total += 1
            self.isEstimate = True
            
            record = {
                "count": self.count_total,
                "estimate": self.estimate,
                "require": self.require,
            }
            self.record_couting.append(record)
            self.estimate = "estimate"
            self.state = "up"
        
        self.data_on_rep = {
            "total": self.count_total,
            "estimate": self.estimate,
            "good": self.count_good,
            "state": self.state,
        }
    
    def evaluate_form(self, origin):
        if origin < self.bad_standard:
            self.estimate = "bad"
            self.require = "Squat deeper!"
        elif origin < self.good_standard:
            self.estimate = "good"
            self.count_good += 1           
            self.require = "Good squat form!"
        else:
            self.require = "Keep moving!"
            self.estimate = "okay"
