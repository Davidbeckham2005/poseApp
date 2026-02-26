import os
from urllib.parse import unquote
path_video_encode = "C%3A%5CUsers%5Cdinhh%5CDownloads%5Cpushup01.mp4"
path_video = unquote(path_video_encode)
size = os.path.getsize(path_video)
time = os.path.getmtime(path_video)
print(f"byte: ",size)
print(f"size: {(size/1024):.2f} MB")
print(f"time: {time} sec")