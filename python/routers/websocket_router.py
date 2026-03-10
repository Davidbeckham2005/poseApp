import threading

from services.drawing_service import DrawingService
from services.pushup_service import pushupService
from services.plank_service import plankService
# from services.webcam import websocket_service
from services.webcam import FrameBuffer,ResultBuffer
from services.squat_services import squatService
from services.pose_service import PoseDetector
from schemas.video_schemas import Webcam_Schemas
from fastapi import APIRouter,WebSocket, WebSocketDisconnect# type: ignore
import numpy as np
import cv2, json, time
import asyncio
router = APIRouter(prefix="/websocket")

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket,exercise_type:str):
    await websocket.accept()
    print("client contected! exercise:",exercise_type)
    frame_buffer = FrameBuffer()
    result_buffer = ResultBuffer()
    # ===================================================================
    detector = PoseDetector()
    draw = DrawingService(detector)
    data = Webcam_Schemas(Analyst_FPS=False,type=exercise_type)
    # capture = websocket_service()
    # capture.start(data=None)
    if exercise_type == 'squat':
        service = squatService(draw, detector ,None,data)
    elif exercise_type == 'pushup':
        service = pushupService(draw, detector, None,data)
    elif exercise_type == 'plank':
        service = plankService(draw, detector, None,data)
    else:
        print("đóng nối kết do không có bài tập đó!")
        await websocket.close()
        return
    service.show_camera_not_make_video()
    count = 0

    # khai bao luong moi
    thread = threading.Thread(target=detection_loop,args=(frame_buffer,result_buffer,service))
    thread.daemon = True
    thread.start()
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
            frame_buffer.set_frame(data)
            result = result_buffer.get()
            # capture.read_frame(data)
            # frame = capture.get_frame()
            # if frame is not None:
            #     print(count) 
            #     count+=1
            #     frame = cv2.flip(frame,1)
            #     cv2.imshow("frontend camera", frame)
            #     cv2.waitKey(1)
            #     service.run_detection(frame)   
            #     output = service.get_data_live()
            await websocket.send_text(json.dumps(result))
    
    except Exception as e:
        print("Có lỗi xãy ra trong lòng lặp:",e)
    finally:
        print("close by backend")
        if websocket.client_state.name != 'DISCONNECTED':
            await websocket.close()

def detection_loop(frane_buffer, result_buffer, service):
    while True:
        frame = frane_buffer.get_frame()
      
        if frame is None:
            time.sleep(0.01)
            continue
       
        frame = cv2.flip(frame,1)
        service.run_detection(frame)
        # debug camera
        # cv2.imshow("frontend camera", frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break   
        data_result = service.get_data_live()
        result_buffer.set(data_result)

