import os
from pathlib import Path
from fastapi import UploadFile
from typing import Literal

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/data/uploads")).resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

Timeframe = Literal["4H","1H","30M","15M"]

def save_screenshot(trade_id: str, tf: Timeframe, file: UploadFile) -> str:
    folder = UPLOAD_DIR / trade_id
    folder.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename).suffix or ".png"
    dest = folder / f"{tf}{suffix}"
    with dest.open("wb") as f:
        f.write(file.file.read())
    # URL returned to client (simple local path)
    return f"/files/{trade_id}/{dest.name}"

def file_path_from_url(url: str) -> Path:
    # expected /files/<trade_id>/<filename>
    parts = Path(url).parts
    return UPLOAD_DIR / parts[-2] / parts[-1]
