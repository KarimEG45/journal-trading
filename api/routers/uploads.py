from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from pathlib import Path
import os

from db import get_session                    
from models import Trade                      
from utils.storage import save_screenshot     
from fastapi.responses import FileResponse

router = APIRouter(tags=["uploads"])

@router.post("/api/trades/{trade_id}/screenshots/{tf}")
def upload_screenshot(trade_id: UUID, tf: str, file: UploadFile = File(...), session: Session = Depends(get_session)):
    trade = session.get(Trade, trade_id)
    if not trade:
        raise HTTPException(404)
    url = save_screenshot(str(trade_id), tf.upper(), file)
    if tf.upper() == "4H": trade.shot_4h_url = url
    if tf.upper() == "1H": trade.shot_1h_url = url
    if tf.upper() == "30M": trade.shot_30m_url = url
    if tf.upper() == "15M": trade.shot_15m_url = url
    session.add(trade); session.commit(); session.refresh(trade)
    return {"url": url}

FILES_ROOT = Path(os.getenv("UPLOAD_DIR", "/app/data/uploads")).resolve()

@router.get("/files/{trade_id}/{filename}")
def get_file(trade_id: str, filename: str):
    path = FILES_ROOT / trade_id / filename
    if not path.exists():
        raise HTTPException(404)
    return FileResponse(path)
