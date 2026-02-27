
from model.db_model import get_db
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, status
from model.video_model import video

def create_video(result,db: Session = Depends(get_db)):
    new_video = video(
    output_path = result["result"]["src_output"],
    total = result["result"]["total"],
    count_good = result["result"]["good"],
    accuracy_good = result["result"]["accuracy"],
    record_detail = result["result"]["record"],
    type = result['type'],
    size_video = result['result']['size'],
    form = result['result']['form'],
    time = result['result']['time']
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video
def read_video(output_path,db: Session = Depends(get_db)):
    video_content = db.query(video).filter(video.output_path==output_path).first()
    if not video_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy video trong hệ thống"
        )
    return video_content
   

def delete_video(data,db: Session = Depends(get_db) ):
    video_to_delete = db.query(video).filter(video.output_path == data.output_path).first()
    if not video_to_delete:
        raise HTTPException(status_code=404, detail="Video không tồn tại")
    try:
        db.delete(video_to_delete)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa: {str(e)}")
    return{
        "message" : "xóa thành công!"
    }
def delete_list_video(data,db: Session = Depends(get_db) ):
    videos = db.query(video).filter(video.output_path.in_(data.output_paths))
    count = videos.count()
    if count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy video nào")
    try:
        videos.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback() # Hoàn tác nếu có lỗi xảy ra
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa: {str(e)}")
    return {
        "message": f"xóa thành công {count} videos"
    }
def read_all_video(db: Session = Depends(get_db)):
    videos = db.query(video).all()
    total_video = len(videos)
    return {
         "total" : total_video,
         "video_items" : videos
    }