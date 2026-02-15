from fastapi import FastAPI, UploadFile, File, Form,Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import Post, create_db_and_tables, get_async_session
from contextlib import asynccontextmanager
from app.images import imagekit
import shutil
import tempfile
import os

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield
app=FastAPI(lifespan=lifespan)


@app.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    caption: str= Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path=None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result=imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            use_unique_file_name=True,
            tags=['backend-upload']
        )

        post=Post(
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type.startswith("video/") else "image",
            file_name=upload_result.name
        )

        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()