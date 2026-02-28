from typing import List
from pydantic import BaseModel #type: ignore


class Webcam_Schemas(BaseModel):
    isDrawing: bool = True
    isAnalyst: bool = True
    isCheck_view: bool = True
    Analyst_FPS: bool = True
    Analyst_state: bool = True
    type: str = "squat"
    Analyst_count: bool = True
    Analyst_count_good: bool = True
    Analyst_estimate: bool = True
   
class Video_Schemas(Webcam_Schemas):
    path_video: str = "LIVE"
class Delete_Video_Schemas(BaseModel):
    output_path: str

class Delete_List_video_Schemas(BaseModel):
    output_paths: List[str]