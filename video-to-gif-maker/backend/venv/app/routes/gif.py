# app/routes/gif.py

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..utils.video_processing import convert_video_to_gif
from ..database import get_db
from ..models import GIF
import json
import os
from typing import List  # Add this import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time  # Optional, for waits in case the page load is slow

router = APIRouter(
    prefix="/gifs",
    tags=["gifs"]
)

UPLOAD_DIR = "./uploads"
GIF_DIR = "./gifs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

@router.get("/")
def get_gifs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    gifs = db.query(GIF).offset(skip).limit(limit).all()
    base_url = "http://localhost:8000/gifs/"  # Ensure this matches your static files URL
    return [{"gif_url": base_url + os.path.basename(gif.file_path)} for gif in gifs]


@router.post("/create")
async def create_gif(file: UploadFile = File(...), db: Session = Depends(get_db)):
    video_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded video file
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # Convert video to multiple GIFs
    gif_files = convert_video_to_gif(video_path, GIF_DIR)

    # Save each GIF path to the database and upload it to Tenor
    gif_paths = []
    for gif_file in gif_files:
        # Create a new GIF record in the database
        db_gif = GIF(file_path=gif_file, user_id=1)  # Placeholder user_id
        db.add(db_gif)
        db.commit()
        db.refresh(db_gif)
        gif_paths.append(gif_file)

        # Upload the created GIF to Tenor
        upload_gif_to_tenor(gif_file)

    return {"gifs": gif_paths}


# @router.post("/create")
# async def create_gif(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     video_path = os.path.join(UPLOAD_DIR, file.filename)
    
#     # Save the uploaded video file
#     with open(video_path, "wb") as buffer:
#         buffer.write(await file.read())

#     # Convert video to multiple GIFs
#     gif_files = convert_video_to_gif(video_path, GIF_DIR)

#     # Save each GIF path to the database
#     gif_paths = []
#     for gif_file in gif_files:
#         # Create a new GIF record in the database
#         db_gif = GIF(file_path=gif_file, user_id=1)  # Placeholder user_id
#         db.add(db_gif)
#         db.commit()
#         db.refresh(db_gif)
#         gif_paths.append(gif_file)

#     return {"gifs": gif_paths}

def upload_gif_to_tenor(gif_file: str):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    
    # Automatically manage ChromeDriver version
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to Tenor's upload page
        driver.get("https://tenor.com/")

        # Click on the "SIGN IN" button
        # tenor_cookies = load_cookies()

        time.sleep(1)
        # Find the "Create" button by class name and click it
        create_button = driver.find_element(By.CLASS_NAME, 'upload-button')
        create_button.click()

        # Wait for the upload page to load
        time.sleep(2)

        base_url = "http://localhost:8000/gifs/"
        gifd = base_url + os.path.basename(gif_file)
        gif_file_path = gifd.replace('http://localhost:8000', os.getcwd())  

        # Locate the file input element and upload the GIF
        file_input = driver.find_element(By.ID, 'upload_file_dropzone-upload-file-section-button')
        file_input.send_keys(gif_file_path)

        time.sleep(5)

        # Find the tag input box by its id and add tags
        tag_input = driver.find_element(By.ID, 'upload_tags_0')
        tag_input.send_keys('ABC')

        # Optional: Simulate pressing 'Enter' to add the tag
        tag_input.send_keys("\n")

        # Find the "Upload To Tenor" button by class name and click it
        upload_button = driver.find_element(By.CLASS_NAME, 'button-content')
        upload_button.click()

        # Optional: Wait for upload to complete
        time.sleep(5)

    finally:
        driver.quit()
    