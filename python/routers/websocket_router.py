from services.drawing_service import DrawingService
from services.pushup_service import pushupService
from services.plank_service import plankService
from services.webcam import websocket_service
from services.squat_services import squatService
from services.pose_service import PoseDetector
from schemas.video_schemas import Webcam_Schemas
from fastapi import APIRouter,WebSocket# type: ignore

import cv2, json
router = APIRouter(prefix="/websocket")

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    exercise_type = 'squat'
    print("client contected!")
    detector = PoseDetector()
    draw = DrawingService(detector)
    data = Webcam_Schemas(Analyst_FPS=False)
    if exercise_type == 'squat':
        service = squatService(draw, detector ,None,data)
    if exercise_type == 'pushup':
        service = pushupService(draw, detector, None,data)
    if exercise_type == 'plank':
        service = plankService(draw, detector, None,data)
    # service = squatService(draw,detector,None,data)
    service.show_camera_not_make_video()
    capture = websocket_service()
    capture.start(data=None)
    # count = 0
    try:
        while True:
            data = await websocket.receive_bytes()
            capture.read_frame(data)
            frame = capture.get_frame()
            if frame is not None:
                # print(count)
                # count+=1
                frame = cv2.flip(frame,1)
                service.run_detection(frame)   
                cv2.imshow("Kiem tra frame", frame)
                cv2.waitKey(1) # Phải có dòng này nó mới hiện ảnh
                output = service.getResult_live()
            
            
            await websocket.send_text(json.dumps(output))
    except Exception as e:
        print(e)
    finally:
        cv2.destroyAllWindows()
        if not websocket.client_state.name == 'DISCONNECTED':
            await websocket.close()