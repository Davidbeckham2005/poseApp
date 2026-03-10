from services.lungue_service import lungService
from services.pushup_service import pushupService
from services.pose_service import PoseDetector
from services.drawing_service import DrawingService
from schemas.video_schemas import Webcam_Schemas
import cv2

pose = PoseDetector()
draw = DrawingService(pose) 
data = Webcam_Schemas(type="lungue",Analyst_FPS=False,isMake_Result=False)
service = lungService(data=data, draw=draw, pose=pose,capture=None)

capture = cv2.VideoCapture(r"C:\Users\dinhh\Downloads\lungue01.mp4")
while True:
    ret, frame = capture.read()
    if not ret:
        break
    frame = cv2.flip(frame,1)
    service.run_detection(frame)
    cv2.imshow("test window",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()

