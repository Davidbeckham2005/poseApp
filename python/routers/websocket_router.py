from services.drawing_service import DrawingService
from services.pushup_service import pushupService
from services.plank_service import plankService
from services.webcam import websocket_service
from services.squat_services import squatService
from services.pose_service import PoseDetector
from schemas.video_schemas import Webcam_Schemas
from fastapi import APIRouter,WebSocket, WebSocketDisconnect# type: ignore
import numpy as np
import cv2, json
import asyncio
router = APIRouter(prefix="/websocket")

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket,exercise_type:str):
    await websocket.accept()
    print("client contected! exercise:",exercise_type)

    # ===================================================================
    detector = PoseDetector()
    draw = DrawingService(detector)
    data = Webcam_Schemas(Analyst_FPS=False,type=exercise_type)
    capture = websocket_service()
    capture.start(data=None)
    if exercise_type == 'squat':
        service = squatService(draw, detector ,capture,data)
    elif exercise_type == 'pushup':
        service = pushupService(draw, detector, capture,data)
    elif exercise_type == 'plank':
        service = plankService(draw, detector, capture,data)
    else:
        print("đóng nối kết do không có bài tập đó!")
        await websocket.close()
        return
    service.show_camera_not_make_video()
    count = 0
    # ===================================================================
    try:
        while True:
            try:
                data = await websocket.receive_bytes()
            except WebSocketDisconnect:
                print("client disconnected")
                break
            except asyncio.CancelledError:
                print("task cancelled")
                break
            capture.read_frame(data)
            frame = capture.get_frame()
            if frame is not None:
                print(count) 
                count+=1
                frame = cv2.flip(frame,1)
                service.run_detection(frame)   
                output = service.get_data_live()
                await websocket.send_text(json.dumps(output))
    
    except Exception as e:
        print("Có lỗi xãy ra trong lòng lặp:",e)
    finally:
        print("close by backend")
        if websocket.client_state.name != 'DISCONNECTED':
            await websocket.close()