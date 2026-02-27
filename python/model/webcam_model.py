from pydantic import BaseModel #type: ignore

class webcam_model(BaseModel):
    isDrawing: bool = True
    isAnalyst: bool = True
    isCheck_view: bool = True
    Analyst_FPS: bool = True
    Analyst_state: bool = True
    type: str = "dafault"
    Analyst_count: bool = True
    Analyst_count_good: bool = True
    Analyst_estimate: bool = True
    path_video: str = "Live"