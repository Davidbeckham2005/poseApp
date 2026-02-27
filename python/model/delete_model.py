from typing import List
from pydantic import BaseModel
class VideoDelete(BaseModel):
    output_path: str

class ListVideoDelete(BaseModel):
    output_paths: List[str]