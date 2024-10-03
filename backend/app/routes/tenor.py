# app/routes/tenor.py

from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(
    prefix="/tenor",
    tags=["tenor"]
)

TENOR_API_KEY = "AIzaSyD2REh5IisbuYAcIHLEg2J_LTu9NFI3XyM"  # Replace with your Tenor API key

@router.post("/upload")
def upload_gif_to_tenor(gif_path: str):
    try:
        # Placeholder upload logic to Tenor
        response = requests.post(
            "https://api.tenor.com/v1/gifs",
            headers={"Authorization": f"Bearer {TENOR_API_KEY}"},
            files={"file": open(gif_path, "rb")},
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
