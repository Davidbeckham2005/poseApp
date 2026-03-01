from services.drawing_service import DrawingService
from services.pushup_service import pushupService
from services.plank_service import plankService
from services.video_services import VideoService
from services.squat_services import squatService
from services.pose_service import PoseDetector
from schemas.video_schemas import Webcam_Schemas
from fastapi import APIRouter,WebSocket# type: ignore

import numpy as np
import cv2, json
router = APIRouter(prefix="/websocket")

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("client contected!")
    detector = PoseDetector()
    draw = DrawingService(detector)
    # if type == 'squat':
    data = Webcam_Schemas(Analyst_FPS=False)
    service = squatService(draw, detector ,None,data)
    # if type == 'pushup':
    #     service = pushupService(draw, detector, None,data)
    # if type == 'plank':
    #     service = plankService(draw, detector, None,data)
    service.show_camera_not_make_video()
    
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            out = {
                "dfd": "fd"
            }
            if frame is not None:
                frame = cv2.flip(frame,1)
                service.run_detection(frame)   
                cv2.imshow("Kiem tra frame", frame)
                cv2.waitKey(1) # Phải có dòng này nó mới hiện ảnh
                output = service.getResult_live()
            
            
            await websocket.send_text(json.dumps(output))
    except Exception as e:
        print(e)
    finally:
        if not websocket.client_state.name == 'DISCONNECTED':
            await websocket.close()