
import string
from fastapi import FastAPI, Request
import random
import string
import boto3
import os
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


# importing the module
from pytube import YouTube


app = FastAPI()

s3 = boto3.resource("s3")
# //allowing the origin
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():

    return {"message": "Hello World"}


@app.post("/download")
async def downloadFile(request: Request):
    body = await request.json()
    print(body["Link"])
    link = body["Link"]

    try:
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(7))
        yt = YouTube(link)
        response = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=f"{result_str}.mp4")
        print("downloaded")
        uploadVideo = s3.meta.client.upload_file(
             f'{result_str}.mp4', "ytbot-cloud-video-storage-bucket", f"{result_str}.mp4")
        print("uploaded")
        # Delete the video from current directory 
        os.remove(f"{result_str}.mp4")
        return {
            "link":f"https://ytbot-cloud-video-storage-bucket.s3.amazonaws.com/{result_str}.mp4"
        }
    except:
        return {"error":"Connection Error"}  # to handle exception


  