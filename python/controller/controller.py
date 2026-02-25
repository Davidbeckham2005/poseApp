from services.video_services import VideoService
from services.squat_services import squatService
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from services.exercise_service import exercise_Service
from services.pushup_service import pushupService
from services.plank_service import plankService

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
    detector = PoseDetector()
    draw = DrawingService(detector)
    if type == 'squat':
        service = squatService(draw, detector ,capture)
    if type == 'pushup':
        service = pushupService(draw, detector, capture)
    if type == 'plank':
        service = plankService(draw, detector, capture)
    if not capture.getCap().isOpened():
        return False
    service.set_setting(data)
    # cho phep thay doi kich thuoc bang chuot
    cv2.namedWindow("video", cv2.WINDOW_NORMAL) 
    while True:    
        ret, frame = capture.read()
        if not ret:
            break
        # count_frame+=1
        # print(f"from control: {count_frame}")
        frame = cv2.resize(frame,capture.getShape())
        # frame = cv2.resize(frame,(520,1280))
        # print(service.capture.set_current_time_ms())
        service.run_detection(frame)    
        # cv2.imshow("video",frame)
        
        # wait_time = max(30,int(800/capture.getFPS()))
        # if cv2.waitKey(wait_time) & 0xFF == ord("q"):
        #     break
    capture.writer_release()       
    capture.release()
    cv2.destroyAllWindows()

    data = {
        "status" : True,
        "result" : service.getResult(),
        "type" : type
    }
    return data