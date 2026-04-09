import threading

from services import shoulder_press_service
from services.drawing_service import DrawingService
from services.pushup_service import pushupService
from services.plank_service import plankService
from services.lungue_service import lungService
from services.squat_services import squatService
from services.warmup_shoulder_stretch_service import warmup_shoulder_stretch_service
from services.warmup_hip_rotation_service import warmup_hip_rotation_service
from services.warmup_squat_service import warmup_squat_service
from services.warmup_jumping_jack_service import warmup_jumping_jack_service
from services.webcam import FrameBuffer,ResultBuffer
from services.pose_service import PoseDetector
from schemas.video_schemas import Webcam_Schemas
from services.bicep_service import bicep_service
from services.shoulder_press_service import ShoulderPressServices
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
    
    # Regular exercises
    if exercise_type == 'squat':
        service = squatService(draw, detector ,None,data)
    elif exercise_type == 'pushup':
        service = pushupService(draw, detector, None,data)
    elif exercise_type == 'plank':
        service = plankService(draw, detector, None,data)
    elif exercise_type == 'lungue':
        service = lungService(draw, detector, None,data)
    elif exercise_type == 'warmup_shoulder_stretch':
        service = warmup_shoulder_stretch_service(draw, detector, None, data)
    elif exercise_type == 'warmup_hip_rotation':
        service = warmup_hip_rotation_service(draw, detector, None, data)
    elif exercise_type == 'warmup_squat':
        service = warmup_squat_service(draw, detector, None, data)
    elif exercise_type == 'warmup_jumping_jack':
        service = warmup_jumping_jack_service(draw, detector, None, data)
    elif exercise_type == 'bicep_curls':
        service = bicep_service(draw,detector, None, data)
    elif exercise_type == "shoulder_press":
        service = shoulder_press_service(draw,detector, None,data)
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
        thread.join(timeout=1)
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

        frame = cv2.flip(frame,1)
        value = service.run_detection(frame)
        # print(value)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        success, buffer = cv2.imencode(".jpg", frame,encode_param)
        if not success:
            continue
        data_result = service.get_data_live()
        data_result["ready"] = value
        frame_bytes = buffer.tobytes()
        meta = json.dumps(data_result).encode()
        payload = len(meta).to_bytes(4, "big") + meta + frame_bytes
        # frame_base64 = base64.b64encode(buffer).decode("utf-8")
        # debug camera
        # cv2.imshow("frontend camera", frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break   
        result_buffer.set(payload)
class Landmark:
    def __init__(self,data):
        self.x = data["x"]
        self.y = data["y"]
        self.z = data["z"]
        self.visibility = data["visibility"]
@router.websocket("/live2")
async def websocket_endpoint(websocket: WebSocket,exercise_type:str):
    await websocket.accept()
    print("client connected! exercise:", exercise_type)

    data = Webcam_Schemas(Analyst_FPS=False, type=exercise_type)

    # Regular exercises
    if exercise_type == 'squat':
        service = squatService(None, None, None, data)
    elif exercise_type == 'pushup':
        service = pushupService(None, None, None, data)
    elif exercise_type == 'plank':
        service = plankService(None, None, None, data)
    elif exercise_type == 'lungue':
        service = lungService(None, None, None, data)
    # Warmup exercises
    elif exercise_type == 'warmup_shoulder_stretch':
        service = warmup_shoulder_stretch_service(None, None, None, data)
    elif exercise_type == 'warmup_hip_rotation':
        service = warmup_hip_rotation_service(None, None, None, data)
    elif exercise_type == 'warmup_squat':
        service = warmup_squat_service(None, None, None, data)
    elif exercise_type == 'warmup_jumping_jack':
        service = warmup_jumping_jack_service(None, None, None, data)
    elif exercise_type == 'bicep_curls':
        service = bicep_service(None,None, None, data)
    elif exercise_type == "shoulder_press":
        service = shoulder_press_service(None,None, None,data)
    else:
        print("not found exercise")
        await websocket.close()
        return

    try:
        while True:

            data = await websocket.receive_json()

            landmarks = data["landmarks"]
            landmarks = [Landmark(x) for x in landmarks]
            service.run_estimate(landmarks,None)

            result = service.get_data_live()
            # print(result)
            await websocket.send_json(result)

    except WebSocketDisconnect:
        print("client disconnected")

from services.game_services.controller_game import WorkoutController
@router.websocket("/live_workout")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    workout_plan = [{"type": "bicep_curls", "target": 6}]
    raw_plan = websocket.query_params.get("plan")
    if raw_plan:
        try:
            parsed_plan = json.loads(raw_plan)
            if isinstance(parsed_plan, list) and parsed_plan:
                workout_plan = [
                    {
                        "type": item.get("type", "bicep_curls"),
                        "target": int(item.get("target", 6))
                    }
                    for item in parsed_plan
                    if isinstance(item, dict)
                ] or workout_plan
        except Exception:
            print("Invalid workout plan received, using default plan")
    controller = WorkoutController(workout_plan)
    try:
        while not controller.is_finish:
            data = await websocket.receive_json()
            landmarks = data["landmarks"]
            landmarks = [Landmark(x) for x in landmarks]
            await controller.update(landmarks,websocket)
    except WebSocketDisconnect:
        print("Client disconected")
    finally:
        if not websocket.client_state.name == "DISCONNECTED":
            print("close by finnaly")
            await websocket.close()
    # data = Webcam_Schemas(Analyst_FPS=False, type=exercise_type)

