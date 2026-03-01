from fastapi import APIRouter # type: ignore
from controller.controller import show_cam
from schemas.video_schemas import Webcam_Schemas

router = APIRouter(prefix="/service")
# show_camera o phia backend 
@router.post("/show_camera")
def show_webcam(input: Webcam_Schemas):
    show_cam(input)