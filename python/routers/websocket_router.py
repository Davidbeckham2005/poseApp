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
async def websocket_endpoint(websocket: WebSocket,exercise_type:str = 'squat'):
    await websocket.accept()
    print("client contected! exercise: ",exercise_type)
    detector = PoseDetector()
    draw = DrawingService(detector)
    data = Webcam_Schemas(Analyst_FPS=False,type=exercise_type)
    capture = websocket_service()
    capture.start(data=None)
    print("exercise_type:", exercise_type)
    if exercise_type == 'squat':
        service = squatService(draw, detector ,capture,data)
    elif exercise_type == 'pushup':
        service = pushupService(draw, detector, capture,data)
    elif exercise_type == 'plank':
        service = plankService(draw, detector, capture,data)
    else:
        # Trường hợp default hoặc lỗi type
        await websocket.close()
        return
    service.show_camera_not_make_video()
    count = 0
    # window_name = f"Backend Stream: {exercise_type}"
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL) 
    # black_screen = np.zeros((480, 640, 3), dtype=np.uint8)
    # cv2.putText(black_screen, "Waiting for frontend stream...", (100, 240), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    # cv2.imshow(window_name, black_screen)
    # cv2.waitKey(1)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_bytes(), timeout=10)
            except(WebSocketDisconnect, asyncio.CancelledError, asyncio.TimeoutError):
                break
            capture.read_frame(data)
            frame = capture.get_frame()
            if frame is not None:
                print(count)
                count+=1
                frame = cv2.flip(frame,1)
                service.run_detection(frame)   
                # cv2.imshow(window_name, frame)
                # cv2.waitKey(1)
                output = service.get_data_live()
                await websocket.send_text(json.dumps(output))
    except WebSocketDisconnect:
        # Bắt lỗi 1005/1000 ở đây để nó không in ra "Exception in ASGI"
        print(f"INFO: Connection closed by client for {exercise_type}")           
    except Exception as e:
        print(e)
    finally:
        # cv2.destroyWindow(window_name)
        cv2.waitKey(1)
        if not websocket.client_state.name == 'DISCONNECTED':
            await websocket.close()