import threading

from services.drawing_service import DrawingService
from services.pushup_service import pushupService
from services.plank_service import plankService
from services.lungue_service import lungService
from services.webcam import FrameBuffer,ResultBuffer
from services.squat_services import squatService
from services.pose_service import PoseDetector
from schemas.video_schemas import Webcam_Schemas
from fastapi import APIRouter,WebSocket, WebSocketDisconnect# type: ignore
import numpy as np
import cv2, json, time
import asyncio
import base64
router = APIRouter(prefix="/websocket")

async def receive_loop(websocket, frame_buffer):

    while True:
        try:
            data = await websocket.receive_bytes()
        except WebSocketDisconnect:
            break

        frame_buffer.set_frame(data)
async def send_loop(websocket, result_buffer):

    while True:

        result = result_buffer.get()

        if result is None:
            await asyncio.sleep(0.003)
            continue

        try:
            await websocket.send_bytes(result)
        except:
            break
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
    elif exercise_type == 'lungue':
        service = lungService(draw, detector, None,data)
    else:
        print("đóng nối kết do không có bài tập đó!")
        await websocket.close()
        return
    service.show_camera_not_make_video()
    count = 0
    stop_event = threading.Event()
    # khai bao luong moi
    thread = threading.Thread(target=detection_loop,args=(frame_buffer,result_buffer,service,stop_event))
    thread.daemon = True
    thread.start()
    # ===================================================================
   
    try:
        await asyncio.gather(
        receive_loop(websocket, frame_buffer),
        send_loop(websocket, result_buffer)
        )

    except Exception as e:
        print("Có lỗi xãy ra trong lòng lặp:",e)
    finally:
        print("close by backend")
        stop_event.set()
        if websocket.client_state.name != 'DISCONNECTED':
            await websocket.close()

def detection_loop(frane_buffer, result_buffer, service,stop_event):
    while not stop_event.is_set():
        data = frane_buffer.get_frame()
        if data is None:
            time.sleep(0.003)
            continue
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            continue
        small = cv2.resize(frame,(320,240))
        frame = cv2.flip(frame,1)
        frame = service.run_detection(frame)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        success, buffer = cv2.imencode(".jpg", frame,encode_param)
        if not success:
            continue
        data_result = service.get_data_live()
        frame_bytes = buffer.tobytes()
        meta = json.dumps(data_result).encode()
        payload = len(meta).to_bytes(4, "big") + meta + frame_bytes
        # frame_base64 = base64.b64encode(buffer).decode("utf-8")
        # debug camera
        # cv2.imshow("frontend camera", frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break   
        result_buffer.set(payload)

        time.sleep(0.003)