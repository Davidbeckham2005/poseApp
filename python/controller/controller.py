from services.video_services import VideoService
from services.squat_services import squatService
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.exercise_service import exercise_Service
from services.pushup_service import pushupService
from services.plank_service import plankService

# from services.webcam import WebcamService

# them luong
import cv2
from pathlib import Path
from urllib.parse import unquote

def process(data):
# su ly path
    # path_video_encode = data['path_video']
    path_video_encode = data.path_video
    path_video = unquote(path_video_encode)
    type = data.type
    # count_frame = 0
    capture = VideoService(path_video)
    capture.start()
    detector = PoseDetector()
    draw = DrawingService(detector)
    if type == 'squat':
        service = squatService(draw, detector ,capture,data)
    if type == 'pushup':
        service = pushupService(draw, detector, capture,data)
    if type == 'plank':
        service = plankService(draw, detector, capture,data)
    if not capture.getCap().isOpened():
        return False
    
    while True:
        frame = capture.get_frame()

        if frame is None:
            # Nếu không lấy được frame và luồng đọc đã kết thúc -> Thoát
            if not capture.is_read_frame:
                break
            # Nếu luồng đọc vẫn đang chạy mà chưa có frame -> Chờ một chút
            continue
        service.run_detection(frame)
    # # cho phep thay doi kich thuoc bang chuot
    # cv2.namedWindow("video", cv2.WINDOW_NORMAL) 
    # while True:    
    #     ret, frame = capture.read()
    #     if not ret:
    #         break  
    #     frame = cv2.resize(frame,capture.getShape())
    #     service.run_detection(frame)
       
    # capture.writer_release()       
    # capture.release()
    cv2.destroyAllWindows()

    data = {
        "status" : True,
        "result" : service.getResult(),
        "type" : type
    }
    return data

