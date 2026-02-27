from controller.controller import process, show_cam
from model.video_model import video_model
from python.model.webcam_model import data_video
data2 = data_video()
data = video_model(type="camera",path_video="fd")
print(data.dict())
print(data2.dict())

# data = {
#     "webcam": True,
#     "type" : "plank"
#  }

# show_cam(data)