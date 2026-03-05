import threading
import queue
import cv2
from datetime import datetime
import numpy as np

class websocket_service:
    def __init__(self):
        # self.fileName = self.create_file_name()
        # self.output_path = self.getNewPath()
        # self.fourcc = cv2.VideoWriter_fourcc(*"avc1")
        # self.output = cv2.VideoWriter(
        #     self.output_path,
        #     self.fourcc,
        #     30,
        #     self.shape)
# da luon tang toc do xu ly
        self.q = queue.Queue(maxsize=200)
        self.is_read_frame = True
    def start(self,data):
        if data is None: 
            return
        thread = threading.Thread(target=self.read_frame(data),args=())
        thread.daemon = True
        thread.start()
        return self
    def read_frame(self,data):
        try:
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is None:
                self.q.get()
            self.q.put(frame)

        except Exception as e:
            print(f"Error decoding frame: {e}")
    def get_frame(self):
        try:
            return self.q.get(timeout=1)
        except queue.Empty:
            return None

  