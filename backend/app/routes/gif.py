import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
URL = "https://video-to-gifs.onrender.com"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

@router.get("/")
def get_gifs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    gifs = db.query(GIF).offset(skip).limit(limit).all()
    base_url = URL+"/gifs/"  # Ensure this matches your static files URL
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
        upload_gif_to_tenor2(gif_file)

        # upload_gif_to_tenor_v2(gif_file)

    return {"gifs": gif_paths}


def upload_gif_to_tenor_v2(gif_path):
    # url = 'https://tenor.googleapis.com/upload/v2/upload'
    access_token = "ya29.a0AcM612wFocZa4j4KM_J7sVLVj_sCzK9QzkcTIumDRAaBSHUNh9nQXSrTUXK8O5z7zMB-KXEjSio2wFed177HS0i4UP5HPBUdMljX1BvyycaOD0skgnljygWpk1xcMjPakCPwb_63n-OgdmpNcsoEE_5qwzdmQYuk9Kjzq2FqaCgYKAYYSARISFQHGX2MiAHZqUzGLXD-1Q5uqBMxCDw0175"; 
    url = "https://tenor.googleapis.com/v1/upload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "image/gif",
    }
    api_key = "AIzaSyD2REh5IisbuYAcIHLEg2J_LTu9NFI3XyM"
    
    # Include the API key as a query parameter
    params = {
        "key": api_key
    }
    
    with open(gif_path, 'rb') as gif_file:
        response = requests.post(url, headers=headers, files={'file': gif_file}, params=params)
    
    if response.status_code == 200:
        print("GIF uploaded successfully:", response.json())
    else:
        print("Failed to upload GIF:", response.status_code, response.text)

# Example usage
# upload_gif_to_tenor_v2('/path/to/your/gif/file.gif')


def upload_gif_to_tenor(gif_file: str):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    
    # Automatically manage ChromeDriver version
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to Tenor's upload page
        driver.get("https://tenor.com/")

        # Click on the "SIGN IN" button
        # tenor_cookies = load_cookies()

        signin_button = driver.find_element(By.XPATH, '//button[text()="SIGN IN"]')
        signin_button.click()
        time.sleep(7)

        google_auth_button = driver.find_element(By.NAME, 'google-auth-button')
        google_auth_button.click()
        
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[1])

        # Wait for the email input to be present
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'identifierId'))
        )
        # Locate the email input field by ID and fill in the email
        email_field = driver.find_element(By.ID, 'identifierId')
        email_field.send_keys('moabjal.spring@gmail.com')
        email_field.send_keys(Keys.ENTER)

        time.sleep(3)

        # Fill in the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )

        time.sleep(3)
        
        # Enter the password
        password_input.send_keys('Spring332#') 
        password_input.send_keys(Keys.ENTER)

        time.sleep(20)
        driver.switch_to.window(driver.window_handles[0])
        # Find the "Create" button by class name and click it
        create_button = driver.find_element(By.CLASS_NAME, 'upload-button')
        create_button.click()


        # Wait for the upload page to load
        time.sleep(2)

        base_url = URL+"/gifs/"
        gifd = base_url + os.path.basename(gif_file)
        gif_file_path = gifd.replace(URL, os.getcwd())  

        # Locate the file input element and upload the GIF
        file_input = driver.find_element(By.ID, 'upload_file_dropzone-upload-file-section-button')
        file_input.send_keys(gif_file_path)

        time.sleep(3)

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

def upload_gif_to_tenor2(gif_file: str):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to Tenor's upload page
        driver.get("https://tenor.com/")

        # Wait until the "SIGN IN" button is clickable, then click it
        signin_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="SIGN IN"]'))
        )
        signin_button.click()

        # Wait for the Google Auth button to be clickable
        google_auth_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'google-auth-button'))
        )
        google_auth_button.click()

        # Switch to the Google sign-in window
        WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the email input to be present, then input the email
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'identifierId'))
        )
        email_input.send_keys('moabjal.spring@gmail.com')
        email_input.send_keys(Keys.ENTER)

        # Wait for the password input to be present, then input the password
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )
        password_input.send_keys('Spring332#')
        password_input.send_keys(Keys.ENTER)

        # Switch back to the main window
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(driver.window_handles[0])

        # Wait until the "Create" button is clickable, then click it
        create_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'upload-button'))
        )
        create_button.click()

        # Wait for the file input field to be present, then upload the GIF
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'upload_file_dropzone-upload-file-section-button'))
        )
        base_url = URL+"/gifs/"
        gifd = base_url + os.path.basename(gif_file)
        gif_file_path = gifd.replace(URL, os.getcwd())
        file_input.send_keys(gif_file_path)

        # Wait for the tag input box to be present, then input tags
        tag_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'upload_tags_0'))
        )
        tag_input.send_keys('ABC')
        tag_input.send_keys(Keys.ENTER)

        # Wait for the "Upload to Tenor" button to be clickable, then click it
        upload_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'button-content'))
        )
        upload_button.click()

        # Wait for the upload to complete (optional)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Upload Complete")]'))  # Example condition
        )

    finally:
        driver.quit()

# upload_gif_to_tenor('http://localhost:8000/gifs/afzal-video.gif')