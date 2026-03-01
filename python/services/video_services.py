import threading
import queue
import cv2
from pathlib import Path
from datetime import datetime
import os, time

class VideoService:
    def __init__(self, path: str):
        self.path = Path(path)
        self.cap = cv2.VideoCapture(str(self.path))
        # doan nay cho viec su ly ket qua
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if self.fps <=0:
            self.fps=30
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.shape = self.width, self.height
        self.fileName = self.create_file_name()
        self.output_path = self.getNewPath()
        self.fourcc = cv2.VideoWriter_fourcc(*"avc1")
        self.output = cv2.VideoWriter(
            self.output_path,
            self.fourcc,
            self.fps,
            self.shape)
       
        self.current_time_ms = 0
# da luon tang toc do xu ly
        self.q = queue.Queue(maxsize=200)
        self.is_read_frame = True
     
        # dung cho video
        # self.timestamp_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC)) 
    
    def start(self):
        thread = threading.Thread(target=self.read_frame,args=())
        thread.daemon = True
        thread.start()
        return self
    def read_frame(self):
        while True:
            if not self.is_read_frame:
                break
            if not self.q.full():
                ret, frame = self.read()
                if not ret:
                    self.is_read_frame = False
                    break
                self.q.put(frame)
            else:
                time.sleep(0.01)
        self.release()
    def get_frame(self):
        try:
            return self.q.get(timeout=1)
        except queue.Empty:
            return None

    def get_file_name(self):
        return self.fileName
    def getNewPath(self):
        return fr"C:\Users\dinhh\Desktop\nienluan\PoseApp\src\assets\videos\{self.fileName}.mp4"
        # return newPath
    def create_file_name(self):
        name = self.path.stem
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{name}_{now}"
    def makeResult(self,frame):
        self.output.write(frame)
    def getShape(self):
        return self.shape
    def read(self):
        return self.cap.read()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    def getFPS(self):
        return self.fps
    def getCap(self):
        return self.cap
    def release(self):
        self.cap.release()
    def writer_release(self):       
        self.output.release()
    def get_timestamps_ms(self):
        return self.timestamp_ms
    def get_output_path(self):
        return self.output_path
    
    # def get_real_time_seconds(self):
    #     return self.real_time_secons
    
    # def get_real_time_mili(self):
    #     return self.real_time_limisecon
    
    def set_current_time_ms(self):
        self.current_time_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        return self.current_time_ms
    
    def get_size(self):
        size = os.path.getsize(self.path)
        return f"{(size/1024**2):.2f}MB"