from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from pathlib import Path
import os

from app.interactors.files.save import SaveFileInteractor
from app.interactors.files.delete import DeleteFileInteractor

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    route_class=DishkaRoute,
)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    save_file_interactor: FromDishka[SaveFileInteractor] = None,
):
    """Upload a file and return file information"""
    try:
        result = await save_file_interactor.execute(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download a file by filename"""
    file_path = Path("uploads/documents") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )


@router.delete("/{filename}")
async def delete_file(
    filename: str,
    delete_file_interactor: FromDishka[DeleteFileInteractor] = None,
):
    """Delete a file by filename"""
    try:
        await delete_file_interactor.execute(filename)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
