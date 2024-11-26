from pydantic import BaseModel

class ProcessedVideoResponse(BaseModel):
    message: str
    in_count: int
    out_count: int
    processed_video_link: str

class ProcessedImageResponse(BaseModel):
    message: str
    num_objects: int
    processed_image_link: str
